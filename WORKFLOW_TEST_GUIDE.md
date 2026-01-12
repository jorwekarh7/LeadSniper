# 🚀 End-to-End Workflow Test Guide

## Prerequisites

1. **FastAPI Server Running**:
   ```bash
   cd /Users/oabolade/agents_app_build/lead_sniper_ai
   source venv/bin/activate
   python api/run_server.py
   ```

2. **Frontend Running** (optional, for UI):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Environment Variables Set**:
   - `APIFY_API_TOKEN` - Your Apify API token
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `NVM_API_KEY` or `NEVERMINED_API_KEY` - Your Nevermined API key (optional)

## Quick Test (Recommended)

### Option 1: Use the API Endpoint Directly

```bash
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["CRM", "project management", "hiring"],
    "reddit_subreddits": ["startups", "entrepreneur"],
    "max_per_source": 5,
    "process_limit": 3
  }'
```

This will:
1. ✅ Scrape leads from Reddit & LinkedIn
2. ✅ Process them through CrewAI agents
3. ✅ Store them in the API
4. ✅ Make them available in the UI

### Option 2: Use Python Test Script

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python test_workflow_step_by_step.py
```

### Option 3: Process Individual Leads

If you already have leads scraped, process them individually:

```bash
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "title": "Looking for CRM solution",
      "content": "We need a CRM that integrates with Slack. Our current one is terrible.",
      "subreddit": "startups"
    }
  }'
```

## What Happens During the Workflow

### Phase 1: Scraping (2-5 minutes)
- **Reddit**: Searches subreddits (`startups`, `entrepreneur`) for buying intent keywords
- **LinkedIn**: Searches job postings for hiring/tech stack signals
- **Filtering**: Only includes posts with buying intent keywords

### Phase 2: Processing (3-5 minutes per lead)
Each lead goes through 4 CrewAI agents:

1. **Signal Scout** (Intent Data Analyst):
   - Identifies active intent signals
   - Extracts trigger text
   - Assigns confidence score

2. **Researcher** (Business Intelligence Analyst):
   - Gathers company intelligence
   - Finds value propositions
   - Researches recent news

3. **Pitch Architect** (Strategic Growth Copywriter):
   - Creates custom pitch
   - Generates hook
   - Personalizes messaging

4. **Auditor** (Quality Assurance):
   - Validates lead quality
   - Calculates buyability_score (0-100)
   - Provides feedback

### Phase 3: Storage & Protection
- Leads stored in FastAPI
- High-value leads (score >= 80) automatically:
  - Created as Protected Assets
  - Require payment to unlock
  - Generate MCP notifications

### Phase 4: Display
- Leads appear in UI at http://localhost:3000
- Grouped by source (Reddit, LinkedIn)
- Dashboard stats updated
- "View Details" buttons available

## Expected Timeline

- **Small test** (2 leads, 1 processed): ~5-8 minutes
- **Medium test** (5 leads, 3 processed): ~10-15 minutes
- **Full test** (10 leads, 5 processed): ~20-30 minutes

## Monitoring Progress

### Check API Status
```bash
curl http://localhost:8000/health
```

### Check Current Leads
```bash
curl http://localhost:8000/api/leads?limit=10 | python -m json.tool
```

### Check Stats
```bash
curl http://localhost:8000/api/stats | python -m json.tool
```

### Watch Server Logs
The server logs will show:
- Scraping progress
- Agent processing steps
- Any errors

## Troubleshooting

### No Leads Scraped
- Check `APIFY_API_TOKEN` is set
- Verify Apify MCP is connected in Cursor
- Try different keywords
- Check subreddit names are correct

### Processing Fails
- Check `OPENAI_API_KEY` is set
- Verify CrewAI dependencies installed
- Check server logs for specific errors
- Try processing a single lead first

### Leads Not Appearing in UI
- Refresh the browser
- Check browser console for errors
- Verify API returns data: `curl http://localhost:8000/api/leads`
- Check React Query cache (hard refresh: Cmd+Shift+R)

## Test with Real Data

### Recommended Test Configuration

```json
{
  "keywords": ["CRM", "project management", "hiring", "looking for"],
  "reddit_subreddits": ["startups", "entrepreneur"],
  "max_per_source": 5,
  "process_limit": 3
}
```

This will:
- Scrape ~10 leads total (5 Reddit + 5 LinkedIn)
- Process 3 through agents
- Complete in ~10-15 minutes
- Give you real data to test the UI

## Next Steps After Testing

1. ✅ Verify leads appear in UI
2. ✅ Check dashboard stats update
3. ✅ Test "View Details" buttons
4. ✅ Test unlock flow for high-value leads
5. ✅ Verify Nevermined integration

---

**Ready to test? Run the curl command above or use the Python script!**
