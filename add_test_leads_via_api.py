"""
Add test leads via API endpoint
This script adds test leads with high buyability scores for Nevermined testing
"""

import requests
import json
import uuid
from datetime import datetime

API_URL = "http://localhost:8000"

# Test leads - we'll add them as if they were processed
test_leads = [
    {
        "original_lead": {
            "source": "reddit",
            "platform": "reddit",
            "title": "Looking for CRM solution - our current one is terrible",
            "content": "We're a 50-person SaaS company and our current CRM is causing major issues. We're actively looking for alternatives that integrate with Slack and have better reporting. Budget is not an issue - we need something that works.",
            "author": "startup_founder_2024",
            "subreddit": "startups",
            "url": "https://reddit.com/r/startups/test1",
            "upvotes": 45,
            "comments": 12
        },
        "buyability_score": 85
    },
    {
        "original_lead": {
            "source": "linkedin",
            "platform": "linkedin",
            "title": "Hiring: Senior Marketing Automation Specialist",
            "content": "We're hiring a Senior Marketing Automation Specialist to help us migrate from Marketo to a more modern platform. Experience with HubSpot, Salesforce Marketing Cloud, or similar required. This is urgent - we're evaluating platforms now.",
            "company": "GrowthCo",
            "location": "San Francisco, CA",
            "url": "https://linkedin.com/jobs/test2"
        },
        "buyability_score": 88
    },
    {
        "original_lead": {
            "source": "reddit",
            "platform": "reddit",
            "title": "Need project management tool - current one is too expensive",
            "content": "We're a 20-person agency and paying $500/month for our current PM tool. It's way too expensive for what we get. Looking for alternatives that have good task management, time tracking, and client portals. Price is a factor but features matter more.",
            "author": "agency_owner",
            "subreddit": "smallbusiness",
            "url": "https://reddit.com/r/smallbusiness/test3",
            "upvotes": 32,
            "comments": 8
        },
        "buyability_score": 82
    }
]

def create_processed_result(lead_data, score):
    """Create a processed result structure"""
    return {
        "raw": json.dumps({
            "buyability_score": score,
            "protected_asset": {
                "lead_data": {
                    "company_name": lead_data["original_lead"].get("company", "Unknown Company"),
                    "confidence_score": 9 if score >= 85 else 8,
                    "value_proposition": "B2B SaaS platform",
                    "recent_news": [
                        "Active search for solutions",
                        "Budget approved for new tools"
                    ],
                    "likely_rejection_reason": "Current tool satisfaction",
                    "hook": f"I noticed you're looking for a solution - that's great timing!",
                    "pitch": f"Hi! I saw your post about {lead_data['original_lead']['title'][:30]}... We specialize in exactly what you need. Would you be open to a quick 15-minute demo to see how we can help?",
                    "trigger_text": lead_data["original_lead"]["title"]
                }
            }
        }),
        "tasks_output": [
            {
                "agent": "Intent Data Analyst",
                "raw": f'Trigger Text: "{lead_data["original_lead"]["title"]}"',
                "summary": "High intent signal detected"
            },
            {
                "agent": "Strategic Growth Copywriter",
                "raw": f'Pitch: "Hi! I saw your post..."',
                "summary": "Custom pitch generated"
            }
        ]
    }

def add_leads_via_api():
    """Add test leads via the API"""
    print("=" * 60)
    print("Adding Test Leads via API")
    print("=" * 60)
    
    # Check if API is running
    try:
        health = requests.get(f"{API_URL}/health", timeout=5)
        if health.status_code != 200:
            print("❌ API is not running or not healthy")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print(f"   Make sure the server is running: python api/run_server.py")
        return
    
    print("✅ API is running\n")
    
    added_leads = []
    
    for i, lead_data in enumerate(test_leads, 1):
        try:
            print(f"Adding lead {i}/{len(test_leads)}...")
            print(f"  Title: {lead_data['original_lead']['title'][:60]}...")
            print(f"  Score: {lead_data['buyability_score']}")
            
            # First, process the lead (this will create it in the store)
            response = requests.post(
                f"{API_URL}/api/process",
                json={"lead_data": lead_data["original_lead"]},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                lead_id = result.get("lead_id")
                
                # Now we need to update it with our test data
                # Since we can't directly modify the store, we'll need to use a workaround
                # Let's create an endpoint or use a direct method
                
                print(f"  ✅ Lead processed: {lead_id}")
                
                # For now, let's add a note that these need manual update
                # Or we can create a custom endpoint
                added_leads.append({
                    "lead_id": lead_id,
                    "title": lead_data["original_lead"]["title"],
                    "score": lead_data["buyability_score"],
                    "note": "Needs manual score update to test Nevermined"
                })
            else:
                print(f"  ❌ Failed: {response.status_code}")
                print(f"     {response.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Processed: {len(added_leads)} leads")
    
    if added_leads:
        print("\n📋 Lead IDs (for testing):")
        for lead in added_leads:
            print(f"   - {lead['lead_id']}")
            print(f"     Title: {lead['title'][:50]}...")
            print(f"     Expected Score: {lead['score']}")
            print()
    
    print("⚠️  Note: These leads were processed but may not have the exact scores.")
    print("   To test Nevermined unlock, you need leads with buyability_score >= 80.")
    print("\n   Option 1: Use the add_test_leads_endpoint.py script (requires server restart)")
    print("   Option 2: Manually update scores via API if endpoint exists")
    print("   Option 3: Run the workflow and wait for high-score leads")

if __name__ == "__main__":
    add_leads_via_api()
