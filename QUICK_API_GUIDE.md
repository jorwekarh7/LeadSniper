# 🚀 Quick API Guide - Populate Your UI

## Fastest Way to Get Leads in Your UI

### Option 1: Process Individual Leads (Recommended for Testing)

Run these commands to create test leads:

```bash
# Lead 1: High-value CRM lead
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "title": "URGENT: Need CRM solution - current one is terrible",
      "content": "We are a growing SaaS company and our current CRM is driving us crazy. It is slow, the UI is outdated, and it does not integrate with Slack. We need something modern and fast. Budget approved, ready to switch ASAP.",
      "subreddit": "startups"
    }
  }'

# Lead 2: Project Management tool
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "title": "Looking for project management tool",
      "content": "Our team is struggling with our current PM tool. It is clunky and does not scale. Looking for recommendations for a modern solution.",
      "subreddit": "startups"
    }
  }'

# Lead 3: DevOps hiring
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "linkedin",
      "title": "Hiring: Senior DevOps Engineer",
      "content": "We are hiring a Senior DevOps Engineer to help us scale our infrastructure. Currently using AWS and Kubernetes but need optimization. Urgent!",
      "location": "San Francisco"
    }
  }'
```

### Option 2: Use the Test Script

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
./test_api_examples.sh
```

### Option 3: Full Pipeline (Scrape + Process)

```bash
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["CRM", "project management", "need"],
    "reddit_subreddits": ["startups"],
    "max_per_source": 5,
    "process_limit": 3
  }'
```

## View Your Leads

1. **In the UI**: Open http://localhost:3000
2. **Via API**: `curl http://localhost:8000/api/leads?limit=20`

## Test Unlock Flow

1. Process a lead (see above)
2. Get the `lead_id` from the response
3. Check if it's protected: `curl http://localhost:8000/api/leads/{lead_id}`
4. If locked (score >= 80), unlock it:
   ```bash
   curl -X POST http://localhost:8000/api/unlock \
     -H "Content-Type: application/json" \
     -d '{"lead_id": "YOUR_LEAD_ID", "payment_method": "nevermined"}'
   ```

## All Available Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/api/leads` | Get all leads |
| GET | `/api/leads/{id}` | Get specific lead |
| POST | `/api/process` | Process single lead |
| POST | `/api/scrape-and-process` | Scrape + process |
| POST | `/api/unlock` | Unlock protected lead |
| GET | `/api/leads/{id}/payment-status` | Check payment |
| GET | `/api/protected-assets` | High-value leads |
| GET | `/api/stats` | Statistics |

See `API_ENDPOINTS.md` for full documentation.
