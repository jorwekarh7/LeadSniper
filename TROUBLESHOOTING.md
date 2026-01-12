# Troubleshooting Guide

## Common Issues and Solutions

### Issue: All Leads Processing Fail (0% Success Rate)

**Symptoms:**
- Scraping works (leads are found)
- Processing fails for all leads
- Response shows: `"total_processed": 0, "total_failed": 3`

**Common Causes:**

#### 1. OpenAI API Quota Exceeded (Most Common)

**Error Message:** `"You exceeded your current quota, please check your plan and billing details"`

**Solution:**
1. Check your OpenAI account: https://platform.openai.com/account/billing
2. Add credits to your account
3. Verify your `OPENAI_API_KEY` in `.env` is correct
4. Check if you're using the right API key (not a test/expired key)

**How to Verify:**
```bash
# Test your OpenAI API key
python -c "from openai import OpenAI; client = OpenAI(); print('✅ API key works')"
```

#### 2. Invalid OpenAI API Key

**Error Message:** `"401 Unauthorized"` or `"Invalid API key"`

**Solution:**
1. Check `.env` file has `OPENAI_API_KEY=sk-...`
2. Verify the key is correct (no extra spaces, correct format)
3. Regenerate API key if needed: https://platform.openai.com/api-keys

#### 3. Rate Limit Exceeded

**Error Message:** `"Rate limit exceeded"`

**Solution:**
1. Wait a few minutes and retry
2. Reduce `process_limit` in your request (process fewer leads at once)
3. Check your OpenAI tier limits

### Issue: No Leads Scraped

**Symptoms:**
- `"total_scraped": 0`
- No leads found from Reddit/LinkedIn

**Common Causes:**

#### 1. Apify API Token Missing/Invalid

**Solution:**
1. Check `.env` has `APIFY_API_TOKEN=apify_api_...`
2. Verify token at: https://console.apify.com/account/integrations
3. Ensure Apify MCP is connected in Cursor settings

#### 2. No Matching Content

**Solution:**
1. Try different keywords (e.g., "hiring", "looking for", "need")
2. Check subreddit names are correct (case-sensitive)
3. Try broader search terms

### Issue: Leads Not Appearing in UI

**Symptoms:**
- API returns leads (`/api/leads` shows data)
- UI shows empty or no cards

**Common Causes:**

#### 1. Frontend Not Connected to API

**Solution:**
1. Check `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
2. Restart frontend: `cd frontend && npm run dev`
3. Check browser console for errors

#### 2. React Query Cache Issue

**Solution:**
1. Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Clear browser cache
3. Check Network tab in DevTools for API calls

#### 3. Data Format Mismatch

**Solution:**
1. Check API response format matches what frontend expects
2. Verify `buyability_score` is being parsed correctly
3. Check browser console for parsing errors

### Issue: Processing Takes Too Long

**Symptoms:**
- Request times out
- Processing hangs

**Solution:**
1. Reduce `process_limit` (process fewer leads at once)
2. Check OpenAI API status: https://status.openai.com/
3. Increase timeout in API request (default is 600 seconds)

## Debugging Steps

### Step 1: Check API Health

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "services": {
    "apify": "ready",
    "crewai": "ready",
    "nevermined": "ready",
    "api": "running"
  }
}
```

### Step 2: Test Scraping Only

```bash
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["test"],
    "max_per_source": 1,
    "process_limit": 0
  }'
```

This will scrape but not process (to test scraping separately).

### Step 3: Test Processing Single Lead

```bash
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "title": "Test lead",
      "content": "Looking for CRM solution"
    }
  }'
```

### Step 4: Check Server Logs

Watch the FastAPI server logs for detailed error messages:
- Look for OpenAI API errors
- Check for import errors
- Verify environment variables are loaded

### Step 5: Verify Environment Variables

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('APIFY:', 'SET' if os.getenv('APIFY_API_TOKEN') else 'MISSING'); print('OPENAI:', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')"
```

## Getting Help

If issues persist:

1. **Check Error Details**: The API now returns `failed_leads_errors` array with specific error messages
2. **Review Logs**: Check server console output for detailed error traces
3. **Test Components**: Use the test scripts in the project root:
   - `test_single_lead_processing.py` - Test processing
   - `test_workflow_step_by_step.py` - Test full workflow
   - `test_apify_connection.py` - Test Apify connection

## Quick Fixes

### Reset Everything

```bash
# Stop servers
pkill -f "python.*run_server"
pkill -f "next-server"

# Restart API
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python api/run_server.py

# Restart Frontend (in another terminal)
cd frontend
npm run dev
```

### Clear and Retry

```bash
# Clear processed leads (if needed)
curl -X DELETE http://localhost:8000/api/leads/all

# Run workflow again
./START_WORKFLOW.sh
```
