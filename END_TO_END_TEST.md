# End-to-End Workflow Test Guide

## Quick Start

### Option 1: Use the Test Script (Recommended)

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python quick_test_workflow.py
```

### Option 2: Use the Shell Script

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
./run_workflow.sh
```

### Option 3: Use curl Directly

```bash
# Run the full pipeline
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["CRM", "project management", "hiring", "looking for"],
    "reddit_subreddits": ["startups", "entrepreneur"],
    "max_per_source": 5,
    "process_limit": 3
  }'

# Check results
curl http://localhost:8000/api/leads?limit=10
```

## What the Pipeline Does

1. **Scraping Phase** (2-5 minutes):
   - Searches Reddit subreddits (`startups`, `entrepreneur`) for buying intent keywords
   - Searches LinkedIn jobs for hiring/tech stack signals
   - Filters results for buying intent signals

2. **Processing Phase** (3-5 minutes per lead):
   - Processes each lead through 4 CrewAI agents:
     - **Signal Scout**: Identifies intent signals
     - **Researcher**: Gathers company intelligence
     - **Pitch Architect**: Creates custom pitch
     - **Auditor**: Validates and scores (buyability_score)

3. **Storage Phase**:
   - Stores processed leads in FastAPI
   - Creates Protected Assets for high-value leads (score >= 80)
   - Generates MCP notifications

4. **Display Phase**:
   - Leads appear in UI at http://localhost:3000
   - Grouped by source (Reddit, LinkedIn)
   - Dashboard stats updated

## Expected Results

After running the pipeline, you should see:

- **Dashboard Stats Cards**:
  - Total Leads count
  - Average Score
  - Intent Signals count
  - Top Source breakdown

- **Lead Groups**:
  - Reddit leads grouped together
  - LinkedIn leads grouped together
  - Each with "View Details" buttons

- **Lead Details**:
  - Full lead information
  - Buyability score
  - Intent signal
  - Custom pitch
  - Unlock button (if score >= 80)

## Troubleshooting

### API Not Running
```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python api/run_server.py
```

### Apify Connection Issues
- Check `.env` file has `APIFY_API_TOKEN`
- Verify token is valid: https://console.apify.com/account/integrations

### No Leads Scraped
- Check Apify actor availability
- Verify keywords match real content
- Check subreddit names are correct

### Processing Fails
- Check OpenAI API key in `.env`
- Verify CrewAI dependencies installed
- Check server logs for errors

## Test with Smaller Dataset

For faster testing, use smaller limits:

```json
{
  "keywords": ["CRM"],
  "reddit_subreddits": ["startups"],
  "max_per_source": 2,
  "process_limit": 1
}
```

This will:
- Scrape 2 Reddit posts
- Process only 1 lead through agents
- Complete in ~3-5 minutes

## Monitor Progress

Watch the server logs:
```bash
# In another terminal
tail -f /tmp/fastapi_nevermined.log
```

Or check API directly:
```bash
# Check current leads
curl http://localhost:8000/api/leads

# Check stats
curl http://localhost:8000/api/stats
```
