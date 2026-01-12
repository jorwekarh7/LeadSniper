# FastAPI Backend Documentation

## Overview

The FastAPI backend provides REST API endpoints to scrape leads from Reddit/LinkedIn and process them through the CrewAI agents workflow.

## 🚀 Quick Start

### Start the Server

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate

# Option 1: Using the run script
python api/run_server.py

# Option 2: Using uvicorn directly
cd api && uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### 1. Health Check

**GET** `/health`

Check API health and service status.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "apify": "ready",
    "crewai": "ready",
    "api": "running"
  }
}
```

### 2. Scrape Leads

**POST** `/api/scrape`

Scrape leads from Reddit and LinkedIn without processing.

**Request Body:**
```json
{
  "keywords": ["hiring", "looking for", "need"],
  "reddit_subreddits": ["startups", "entrepreneur"],
  "linkedin_location": "United States",
  "max_per_source": 10
}
```

**Response:**
```json
{
  "status": "success",
  "total_leads": 20,
  "reddit_leads": 12,
  "linkedin_leads": 8,
  "leads": [...],
  "timestamp": "2025-01-10T20:00:00"
}
```

### 3. Process Single Lead

**POST** `/api/process`

Process a single lead through the CrewAI agents pipeline.

**Request Body:**
```json
{
  "lead_data": {
    "source": "reddit",
    "platform": "reddit",
    "title": "Looking for CRM solution",
    "content": "We need a CRM that integrates with Slack...",
    "url": "https://reddit.com/example",
    "author": "user123"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "lead_id": "uuid-here",
  "result": {
    "original_lead": {...},
    "processed_result": {...},
    "status": "processed",
    "success": true
  },
  "message": "Lead processed successfully"
}
```

### 4. Scrape and Process (Complete Pipeline)

**POST** `/api/scrape-and-process`

Complete pipeline: Scrape leads and process them through agents.

**Request Body:**
```json
{
  "keywords": ["hiring", "looking for"],
  "reddit_subreddits": ["startups"],
  "linkedin_location": "United States",
  "max_per_source": 10,
  "process_limit": 3
}
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_scraped": 20,
    "total_processed": 3,
    "total_failed": 0,
    "success_rate": 100.0
  },
  "scrape_results": {
    "total": 20,
    "reddit": 12,
    "linkedin": 8
  },
  "processed_leads_count": 3,
  "failed_leads_count": 0,
  "processed_leads": [...],
  "timestamp": "2025-01-10T20:00:00"
}
```

### 5. Get All Leads

**GET** `/api/leads?limit=10&offset=0`

Get all processed leads with pagination.

**Query Parameters:**
- `limit` (optional): Number of leads to return (default: 10)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "total": 25,
  "limit": 10,
  "offset": 0,
  "leads": [...]
}
```

### 6. Get Lead by ID

**GET** `/api/leads/{lead_id}`

Get a specific processed lead by ID.

**Response:**
```json
{
  "lead_id": "uuid-here",
  "original_lead": {...},
  "processed_result": {...},
  "status": "processed",
  "processed_at": "2025-01-10T20:00:00"
}
```

### 7. Delete Lead

**DELETE** `/api/leads/{lead_id}`

Delete a processed lead.

**Response:**
```json
{
  "status": "success",
  "message": "Lead uuid-here deleted"
}
```

### 8. Get Statistics

**GET** `/api/stats`

Get statistics about processed leads.

**Response:**
```json
{
  "total_leads": 25,
  "successful": 23,
  "failed": 2,
  "success_rate": 92.0
}
```

## 🔄 Workflow Integration

The API integrates the complete workflow:

```
1. Scrape Leads (Apify)
   ↓
2. Intent Data Analyst (Signal Scout)
   ↓ Identifies Active Intent
3. Business Intelligence Analyst (Researcher)
   ↓ Creates Context Profile
4. Strategic Growth Copywriter (Pitch Architect)
   ↓ Creates 3-part Pitch
5. Quality Assurance & MCP Bridge (Auditor)
   ↓ Scores Buyability, Formats Asset
6. Processed Lead Package
```

## 📝 Example Usage

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Scrape leads
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["hiring", "looking for"],
    "max_per_source": 5
  }'

# Process a lead
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "title": "Looking for CRM",
      "content": "We need a CRM solution..."
    }
  }'

# Complete pipeline
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["hiring"],
    "max_per_source": 5,
    "process_limit": 2
  }'
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Scrape and process
response = requests.post(
    f"{BASE_URL}/api/scrape-and-process",
    json={
        "keywords": ["hiring", "looking for"],
        "max_per_source": 10,
        "process_limit": 3
    }
)

data = response.json()
print(f"Processed {data['processed_leads_count']} leads")
```

## ⚙️ Configuration

### Environment Variables

```bash
APIFY_API_TOKEN=your_apify_token
OPENAI_API_KEY=your_openai_key
API_HOST=0.0.0.0
API_PORT=8000
```

### Default Settings

- Host: `0.0.0.0` (all interfaces)
- Port: `8000`
- CORS: Enabled for all origins (change in production)

## 🧪 Testing

Run the test suite:

```bash
# Start the server first
python api/run_server.py

# In another terminal, run tests
python test_api.py
```

## 📊 Response Format

All processed leads include:

```json
{
  "lead_id": "uuid",
  "original_lead": {
    "source": "reddit",
    "title": "...",
    "content": "..."
  },
  "processed_result": {
    "signals": {...},        # From Signal Scout
    "context_profile": {...}, # From Researcher
    "pitch": {...},          # From Pitch Architect
    "audit": {...}           # From Auditor
  },
  "status": "processed",
  "processed_at": "2025-01-10T20:00:00"
}
```

## 🔒 Production Considerations

1. **Database**: Replace in-memory storage with a database (PostgreSQL, MongoDB)
2. **Authentication**: Add API key or OAuth authentication
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **CORS**: Restrict CORS to specific origins
5. **Error Handling**: Enhanced error handling and logging
6. **Background Jobs**: Use Celery or similar for async processing
7. **Caching**: Add Redis for caching frequently accessed data

## 🎉 Status

**FastAPI Backend: ✅ Ready**

All endpoints are functional and integrated with the Apify scraper and CrewAI agents workflow.
