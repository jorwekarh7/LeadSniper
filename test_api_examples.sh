#!/bin/bash

# Lead Sniper AI - API Test Examples
# Run these commands to populate the UI with test data

BASE_URL="http://localhost:8000"

echo "🚀 Lead Sniper AI - API Test Examples"
echo "======================================"
echo ""

# Check if server is running
echo "1. Checking server health..."
curl -s "$BASE_URL/health" | python -m json.tool
echo ""
echo ""

# Example 1: Process a single high-value lead
echo "2. Processing a single high-value lead..."
LEAD_1=$(curl -s -X POST "$BASE_URL/api/process" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "platform": "reddit",
      "title": "URGENT: Need CRM solution - current one is terrible",
      "content": "We are a growing SaaS company and our current CRM is driving us crazy. It is slow, the UI is outdated, and it does not integrate with Slack. We need something modern and fast. Anyone have recommendations? We are ready to switch ASAP. Budget approved.",
      "url": "https://reddit.com/r/startups/example1",
      "author": "frustrated_founder",
      "subreddit": "startups"
    }
  }')

echo "$LEAD_1" | python -m json.tool
LEAD_1_ID=$(echo "$LEAD_1" | python -c "import sys, json; print(json.load(sys.stdin).get('lead_id', ''))")
echo ""
echo "Lead ID: $LEAD_1_ID"
echo ""
echo ""

# Example 2: Process another lead
echo "3. Processing another lead..."
LEAD_2=$(curl -s -X POST "$BASE_URL/api/process" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "reddit",
      "platform": "reddit",
      "title": "Looking for project management tool",
      "content": "Our team is struggling with our current PM tool. It is clunky and does not scale. Looking for recommendations for a modern solution that integrates with GitHub.",
      "url": "https://reddit.com/r/startups/example2",
      "author": "tech_lead_2024",
      "subreddit": "startups"
    }
  }')

echo "$LEAD_2" | python -m json.tool
LEAD_2_ID=$(echo "$LEAD_2" | python -c "import sys, json; print(json.load(sys.stdin).get('lead_id', ''))")
echo ""
echo "Lead ID: $LEAD_2_ID"
echo ""
echo ""

# Example 3: Process a LinkedIn-style lead
echo "4. Processing LinkedIn-style lead..."
LEAD_3=$(curl -s -X POST "$BASE_URL/api/process" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_data": {
      "source": "linkedin",
      "platform": "linkedin",
      "title": "Hiring: Senior DevOps Engineer",
      "content": "We are hiring a Senior DevOps Engineer to help us scale our infrastructure. We are currently using AWS and Kubernetes but need someone to optimize our setup. This is urgent as we are experiencing scaling issues.",
      "url": "https://linkedin.com/jobs/example",
      "author": "Tech Startup Inc",
      "location": "San Francisco"
    }
  }')

echo "$LEAD_3" | python -m json.tool
LEAD_3_ID=$(echo "$LEAD_3" | python -c "import sys, json; print(json.load(sys.stdin).get('lead_id', ''))")
echo ""
echo "Lead ID: $LEAD_3_ID"
echo ""
echo ""

# Get all leads
echo "5. Fetching all processed leads..."
curl -s "$BASE_URL/api/leads?limit=10&offset=0" | python -m json.tool
echo ""
echo ""

# Get stats
echo "6. Getting statistics..."
curl -s "$BASE_URL/api/stats" | python -m json.tool
echo ""
echo ""

# Get protected assets
echo "7. Getting protected assets (high-value leads)..."
curl -s "$BASE_URL/api/protected-assets" | python -m json.tool
echo ""
echo ""

echo "✅ Test examples completed!"
echo ""
echo "📊 View leads in the UI: http://localhost:3000"
echo "🔗 API Docs: http://localhost:8000/docs"
