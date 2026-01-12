#!/bin/bash

# Lead Sniper AI - Start End-to-End Workflow
# This script kicks off the complete pipeline

API_URL="http://localhost:8000"

echo "🚀 Lead Sniper AI - Starting End-to-End Workflow"
echo "============================================================"
echo ""

# Check if API is running
echo "Checking API status..."
HEALTH=$(curl -s "$API_URL/health" 2>&1)
if ! echo "$HEALTH" | grep -q "healthy"; then
    echo "❌ API is not running!"
    echo ""
    echo "Please start the API server first:"
    echo "  cd /Users/oabolade/agents_app_build/lead_sniper_ai"
    echo "  source venv/bin/activate"
    echo "  python api/run_server.py"
    exit 1
fi

echo "✅ API is running"
echo ""

# Display current leads count
CURRENT=$(curl -s "$API_URL/api/leads?limit=1" 2>&1)
CURRENT_COUNT=$(echo "$CURRENT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('total', 0))" 2>/dev/null || echo "0")
echo "Current leads in system: $CURRENT_COUNT"
echo ""

# Run the pipeline
echo "Starting pipeline with EXPANDED search scope:"
echo "  Keywords: CRM, project management, hiring, software, tool, platform,"
echo "            solution, alternatives, automation, marketing, sales, analytics"
echo "  Reddit subreddits: startups, entrepreneur, SaaS, smallbusiness,"
echo "                     marketing, sales, productivity"
echo "  Max per source: 15"
echo "  Process limit: 10"
echo ""
echo "⏳ This will take approximately 20-30 minutes..."
echo "   (Scraping: 5-10 min, Processing: 3-5 min per lead)"
echo ""

PAYLOAD='{
  "keywords": [
    "CRM", "project management", "hiring", "looking for", "need",
    "software", "tool", "platform", "solution", "system",
    "alternatives", "replace", "switching", "evaluate", "comparing",
    "best", "recommend", "suggest", "implement", "integrate",
    "automation", "marketing", "sales", "analytics", "dashboard"
  ],
  "reddit_subreddits": ["startups", "entrepreneur", "SaaS", "smallbusiness", "marketing", "sales", "productivity"],
  "max_per_source": 15,
  "process_limit": 10
}'

RESPONSE=$(curl -s -X POST "$API_URL/api/scrape-and-process" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  --max-time 600)

# Parse response
if echo "$RESPONSE" | grep -q '"status":"success"'; then
    echo ""
    echo "✅ Pipeline completed successfully!"
    echo ""
    
    # Extract key metrics
    SCRAPED=$(echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('scrape_results', {}).get('total', 0))" 2>/dev/null || echo "0")
    PROCESSED=$(echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('processed_leads_count', 0))" 2>/dev/null || echo "0")
    FAILED=$(echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('failed_leads_count', 0))" 2>/dev/null || echo "0")
    
    echo "📊 Results:"
    echo "   Scraped: $SCRAPED leads"
    echo "   Processed: $PROCESSED leads"
    echo "   Failed: $FAILED leads"
    echo ""
    
    # Check final count
    sleep 2
    FINAL=$(curl -s "$API_URL/api/leads?limit=1")
    FINAL_COUNT=$(echo "$FINAL" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('total', 0))" 2>/dev/null || echo "0")
    
    echo "📈 Total leads in system: $FINAL_COUNT"
    echo ""
    echo "🌐 View leads in UI: http://localhost:3000"
    echo "📡 API endpoint: $API_URL/api/leads"
    echo "📚 API docs: $API_URL/docs"
    
else
    echo ""
    echo "⚠️  Pipeline had issues. Response:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE" | head -20
fi

echo ""
echo "============================================================"
