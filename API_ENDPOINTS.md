# Lead Sniper AI - API Endpoints Reference

Base URL: `http://localhost:8000`

## 📋 Table of Contents

1. [Health & Info](#health--info)
2. [Lead Scraping](#lead-scraping)
3. [Lead Processing](#lead-processing)
4. [Lead Management](#lead-management)
5. [Payment & Unlock](#payment--unlock)
6. [Statistics](#statistics)

---

## Health & Info

### GET `/`
Get API information and available endpoints.

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Lead Sniper AI API",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

### GET `/health`
Health check endpoint.

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
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

---

## Lead Scraping

### POST `/api/scrape`
Scrape leads from Reddit and LinkedIn (without processing).

**Request Body:**
```json
{
  "keywords": ["hiring", "looking for", "need", "searching"],
  "reddit_subreddits": ["startups", "entrepreneur", "SaaS"],
  "linkedin_location": "San Francisco",
  "max_per_source": 10
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["CRM", "looking for", "need"],
    "reddit_subreddits": ["startups", "entrepreneur"],
    "max_per_source": 5
  }'
```

**Response:**
```json
{
  "status": "success",
  "total_leads": 10,
  "reddit_leads": 5,
  "linkedin_leads": 5,
  "leads": [...],
  "timestamp": "2025-01-11T10:00:00"
}
```

---

## Lead Processing

### POST `/api/process`
Process a single lead through CrewAI agents pipeline.

**Request Body:**
```json
{
  "lead_data": {
    "source": "reddit",
    "platform": "reddit",
    "title": "Urgently looking for CRM solution",
    "content": "We're a growing SaaS company and our current CRM is driving us crazy. It's slow, the UI is outdated, and it doesn't integrate with Slack. We need something modern and fast.",
    "url": "https://reddit.com/r/startups/example",
    "author": "frustrated_founder",
    "subreddit": "startups"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "title": "Need project management tool ASAP",
      "content": "Our team is struggling with our current PM tool. It's clunky and doesn't scale. Looking for recommendations for a modern solution.",
      "subreddit": "startups"
    }
  }'
```

**Response:**
```json
{
  "status": "success",
  "lead_id": "uuid-here",
  "buyability_score": 85,
  "is_high_value": true,
  "protected_asset": {...},
  "mcp_notification": {...},
  "message": "Lead processed successfully"
}
```

### POST `/api/scrape-and-process`
Complete pipeline: Scrape leads AND process them through agents.

**Request Body:**
```json
{
  "keywords": ["hiring", "looking for"],
  "reddit_subreddits": ["startups"],
  "linkedin_location": null,
  "max_per_source": 10,
  "process_limit": 3
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["CRM", "project management", "need"],
    "reddit_subreddits": ["startups", "entrepreneur"],
    "max_per_source": 5,
    "process_limit": 3
  }'
```

**Response:**
```json
{
  "status": "success",
  "scrape_results": {
    "total": 10,
    "reddit": 5,
    "linkedin": 5
  },
  "processed_leads_count": 3,
  "failed_leads_count": 0,
  "processed_leads": [...]
}
```

---

## Lead Management

### GET `/api/leads`
Get all processed leads (with pagination).

**Query Parameters:**
- `limit` (default: 10) - Number of leads to return
- `offset` (default: 0) - Pagination offset

**Example:**
```bash
curl "http://localhost:8000/api/leads?limit=20&offset=0"
```

**Response:**
```json
{
  "total": 15,
  "limit": 20,
  "offset": 0,
  "leads": [
    {
      "lead_id": "uuid-1",
      "original_lead": {...},
      "processed_result": {...},
      "buyability_score": 85,
      "status": "processed",
      "processed_at": "2025-01-11T10:00:00"
    }
  ]
}
```

### GET `/api/leads/{lead_id}`
Get a specific lead by ID.

**Query Parameters:**
- `access_token` (optional) - Required for protected leads

**Example:**
```bash
# Without token (may show locked if score >= 80)
curl http://localhost:8000/api/leads/{lead_id}

# With access token (for unlocked leads)
curl "http://localhost:8000/api/leads/{lead_id}?access_token=token-here"
```

**Response (Unlocked):**
```json
{
  "lead_id": "uuid-here",
  "original_lead": {...},
  "processed_result": {
    "signals": {...},
    "pitch": "Custom pitch here...",
    "hook": "Hook here..."
  },
  "buyability_score": 85,
  "status": "processed"
}
```

**Response (Locked - score >= 80):**
```json
{
  "lead_id": "uuid-here",
  "status": "locked",
  "buyability_score": 85,
  "is_high_value": true,
  "payment_required": true,
  "payment_url": "https://nevermined.io/pay/...",
  "preview": {
    "source": "reddit",
    "title": "Urgently looking for...",
    "buyability_score": 85
  }
}
```

### DELETE `/api/leads/{lead_id}`
Delete a processed lead.

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/leads/{lead_id}
```

---

## Payment & Unlock

### POST `/api/unlock`
Unlock a protected lead (process payment).

**Request Body:**
```json
{
  "lead_id": "uuid-here",
  "payment_method": "nevermined",
  "payment_token": null
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/unlock \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "uuid-here",
    "payment_method": "nevermined"
  }'
```

**Response:**
```json
{
  "status": "success",
  "lead_id": "uuid-here",
  "unlocked": true,
  "access_token": "token-here",
  "payment_id": "payment-id",
  "message": "Lead unlocked successfully"
}
```

### GET `/api/leads/{lead_id}/payment-status`
Check payment status for a lead.

**Example:**
```bash
curl http://localhost:8000/api/leads/{lead_id}/payment-status
```

**Response:**
```json
{
  "lead_id": "uuid-here",
  "payment_status": {
    "is_paid": false,
    "status": "pending",
    "access_token": null
  },
  "payment_url": "https://nevermined.io/pay/...",
  "is_paid": false
}
```

### GET `/api/protected-assets`
Get list of protected assets (high-value leads, score >= 80).

**Query Parameters:**
- `limit` (default: 10)
- `offset` (default: 0)

**Example:**
```bash
curl "http://localhost:8000/api/protected-assets?limit=10&offset=0"
```

**Response:**
```json
{
  "total": 5,
  "limit": 10,
  "offset": 0,
  "protected_assets": [...]
}
```

---

## Statistics

### GET `/api/stats`
Get statistics about processed leads.

**Example:**
```bash
curl http://localhost:8000/api/stats
```

**Response:**
```json
{
  "total_leads": 15,
  "successful": 14,
  "failed": 1,
  "success_rate": 93.33
}
```

---

## 🚀 Quick Start Examples

### Example 1: Process a Single Lead (Best for UI Testing)

```bash
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "platform": "reddit",
      "title": "Looking for CRM solution - current one is terrible",
      "content": "We are a growing SaaS company and our current CRM is driving us crazy. It is slow, the UI is outdated, and it does not integrate with Slack. We need something modern and fast. Anyone have recommendations? We are ready to switch ASAP.",
      "url": "https://reddit.com/r/startups/example",
      "author": "frustrated_founder",
      "subreddit": "startups"
    }
  }'
```

### Example 2: Process Multiple Leads (Full Pipeline)

```bash
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["CRM", "project management", "need", "looking for"],
    "reddit_subreddits": ["startups", "entrepreneur"],
    "max_per_source": 5,
    "process_limit": 5
  }'
```

### Example 3: Get All Leads (For UI Display)

```bash
curl "http://localhost:8000/api/leads?limit=50&offset=0"
```

### Example 4: Unlock a High-Value Lead

```bash
# First, get the lead ID from /api/leads
# Then unlock it:
curl -X POST http://localhost:8000/api/unlock \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "YOUR_LEAD_ID_HERE",
    "payment_method": "nevermined"
  }'
```

---

## 📝 Notes

- All endpoints return JSON
- Protected leads (buyability_score >= 80) require payment to unlock
- The `/api/scrape-and-process` endpoint is the most comprehensive - it scrapes AND processes leads
- Use `/api/process` for testing individual leads
- Use `/api/leads` to fetch leads for the UI

---

## 🔗 Frontend Integration

The frontend at `http://localhost:3000` automatically connects to these endpoints:
- `GET /api/leads` - Fetches leads for the feed
- `GET /api/leads/{id}` - Gets individual lead details
- `POST /api/unlock` - Unlocks protected leads
- `GET /api/leads/{id}/payment-status` - Checks payment status
