#!/bin/bash

# Quick script to add test leads for Nevermined testing

API_URL="http://localhost:8000"

echo "=" * 60
echo "Adding Test Leads for Nevermined Testing"
echo "=" * 60
echo ""

# Check if API is running
if ! curl -s "$API_URL/health" > /dev/null 2>&1; then
    echo "❌ API is not running!"
    echo "   Start it with: python api/run_server.py"
    exit 1
fi

echo "✅ API is running"
echo ""

# Add test leads
echo "Adding test leads..."
RESPONSE=$(curl -s -X POST "$API_URL/api/test/add-leads" \
  -H "Content-Type: application/json")

if echo "$RESPONSE" | grep -q '"status":"success"'; then
    echo "✅ Test leads added successfully!"
    echo ""
    echo "$RESPONSE" | python3 -m json.tool
    
    echo ""
    echo "🌐 View leads in UI: http://localhost:3000"
    echo "📡 API endpoint: $API_URL/api/leads"
else
    echo "❌ Failed to add test leads"
    echo "$RESPONSE"
fi
