#!/bin/bash

# Lead Sniper AI - End-to-End Workflow Runner
# This script runs the complete pipeline: Scrape → Process → Display

API_URL="http://localhost:8000"

echo "============================================================"
echo "Lead Sniper AI - End-to-End Workflow"
echo "============================================================"
echo ""

# Step 1: Check API health
echo "Step 1: Checking API health..."
HEALTH=$(curl -s "$API_URL/health" 2>&1)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ API is running"
else
    echo "❌ API is not running!"
    echo "   Start it with: python api/run_server.py"
    exit 1
fi

echo ""
echo "Step 2: Running full pipeline..."
echo "   This will:"
echo "   1. Scrape leads from Reddit & LinkedIn"
echo "   2. Process them through CrewAI agents"
echo "   3. Store them in the API"
echo ""
echo "⏳ This may take 5-10 minutes..."
echo ""

# Step 2: Run the pipeline
PAYLOAD='{
  "keywords": ["CRM", "project management", "hiring", "looking for", "need"],
  "reddit_subreddits": ["startups", "entrepreneur"],
  "max_per_source": 5,
  "process_limit": 3
}'

RESPONSE=$(curl -s -X POST "$API_URL/api/scrape-and-process" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  --max-time 600)

if echo "$RESPONSE" | grep -q "status.*success"; then
    echo "✅ Pipeline completed!"
    echo ""
    echo "$RESPONSE" | python -m json.tool | head -30
else
    echo "⚠️  Pipeline response:"
    echo "$RESPONSE" | head -20
fi

echo ""
echo "Step 3: Verifying leads..."
LEADS=$(curl -s "$API_URL/api/leads?limit=10&offset=0")
TOTAL=$(echo "$LEADS" | python -c "import sys, json; d=json.load(sys.stdin); print(d.get('total', 0))" 2>/dev/null || echo "0")

if [ "$TOTAL" -gt 0 ]; then
    echo "✅ Found $TOTAL leads in API"
    echo ""
    echo "🌐 View in UI: http://localhost:3000"
    echo "📡 API: $API_URL/api/leads"
else
    echo "⚠️  No leads found yet"
fi

echo ""
echo "============================================================"
echo "Workflow complete!"
echo "============================================================"
