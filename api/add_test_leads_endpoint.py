"""
Script to add test leads directly to the processed_leads_store
Run this to populate the system with test leads for Nevermined testing
"""

import sys
import os
import json
import uuid
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the store from main.py
# We'll need to import it directly
from api.main import processed_leads_store

# Test leads with high buyability scores
test_leads_data = [
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
        "processed_result": {
            "raw": json.dumps({
                "buyability_score": 85,
                "protected_asset": {
                    "lead_data": {
                        "company_name": "TechStart Inc",
                        "confidence_score": 9,
                        "value_proposition": "B2B SaaS platform for project management",
                        "recent_news": [
                            "Raised $5M Series A in Q4 2024",
                            "Expanding team from 30 to 50 employees"
                        ],
                        "likely_rejection_reason": "Current tool satisfaction",
                        "hook": "Congratulations on your Series A! With your team doubling, you'll need a CRM that scales.",
                        "pitch": "Hi! I saw you're looking for a CRM solution. Given your recent Series A and team expansion, you need a platform that grows with you. Our CRM integrates seamlessly with Slack and provides real-time analytics that your current solution lacks. Would you be open to a 15-minute demo to see how we can help you scale more efficiently?",
                        "trigger_text": "Looking for CRM solution - our current one is terrible"
                    }
                }
            }),
            "tasks_output": [
                {
                    "agent": "Intent Data Analyst",
                    "raw": 'Trigger Text: "Looking for CRM solution - our current one is terrible"',
                    "summary": "High intent signal detected"
                },
                {
                    "agent": "Strategic Growth Copywriter",
                    "raw": 'Pitch: "Hi! I saw you\'re looking for a CRM solution..."',
                    "summary": "Custom pitch generated"
                }
            ]
        },
        "buyability_score": 85,
        "status": "processed",
        "processed_at": datetime.now().isoformat()
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
        "processed_result": {
            "raw": json.dumps({
                "buyability_score": 88,
                "protected_asset": {
                    "lead_data": {
                        "company_name": "GrowthCo",
                        "confidence_score": 9,
                        "value_proposition": "B2B marketing automation platform",
                        "recent_news": [
                            "Migrating from Marketo - urgent need",
                            "Hiring for marketing automation role"
                        ],
                        "likely_rejection_reason": "Budget constraints",
                        "hook": "I noticed you're migrating from Marketo - that's a big move!",
                        "pitch": "Hi GrowthCo team! I saw you're hiring a Marketing Automation Specialist and migrating from Marketo. We specialize in helping companies transition to modern marketing platforms with zero downtime. Our platform offers better analytics and integrates with your existing stack. Would you be interested in a quick call to discuss how we can make your migration seamless?",
                        "trigger_text": "Migrating from Marketo to a more modern platform"
                    }
                }
            }),
            "tasks_output": [
                {
                    "agent": "Intent Data Analyst",
                    "raw": 'Trigger Text: "Migrating from Marketo to a more modern platform"',
                    "summary": "Very high intent - active migration"
                },
                {
                    "agent": "Strategic Growth Copywriter",
                    "raw": 'Pitch: "Hi GrowthCo team! I saw you\'re hiring..."',
                    "summary": "Custom pitch generated"
                }
            ]
        },
        "buyability_score": 88,
        "status": "processed",
        "processed_at": datetime.now().isoformat()
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
        "processed_result": {
            "raw": json.dumps({
                "buyability_score": 82,
                "protected_asset": {
                    "lead_data": {
                        "company_name": "Creative Agency LLC",
                        "confidence_score": 8,
                        "value_proposition": "Creative agency specializing in digital marketing",
                        "recent_news": [
                            "Growing from 15 to 20 employees",
                            "Expanding client base"
                        ],
                        "likely_rejection_reason": "Price sensitivity",
                        "hook": "I see you're growing your team - that's exciting!",
                        "pitch": "Hi! I noticed you're looking for a more affordable project management solution. With your team growing, you need a tool that scales without breaking the bank. Our platform offers all the features you mentioned at a fraction of your current cost. We've helped many agencies like yours reduce costs while improving productivity. Would you be open to a quick demo?",
                        "trigger_text": "Need project management tool - current one is too expensive"
                    }
                }
            }),
            "tasks_output": [
                {
                    "agent": "Intent Data Analyst",
                    "raw": 'Trigger Text: "Need project management tool - current one is too expensive"',
                    "summary": "High intent - price-driven but active search"
                },
                {
                    "agent": "Strategic Growth Copywriter",
                    "raw": 'Pitch: "Hi! I noticed you\'re looking for..."',
                    "summary": "Custom pitch generated"
                }
            ]
        },
        "buyability_score": 82,
        "status": "processed",
        "processed_at": datetime.now().isoformat()
    }
]

def add_test_leads_to_store():
    """Add test leads directly to the processed_leads_store"""
    print("=" * 60)
    print("Adding Test Leads to System")
    print("=" * 60)
    
    added_leads = []
    
    for i, lead_data in enumerate(test_leads_data, 1):
        lead_id = str(uuid.uuid4())
        
        # Create full lead structure
        full_lead = {
            "lead_id": lead_id,
            **lead_data
        }
        
        # Add to store
        processed_leads_store[lead_id] = full_lead
        added_leads.append({
            "lead_id": lead_id,
            "title": lead_data["original_lead"]["title"],
            "score": lead_data["buyability_score"]
        })
        
        print(f"✅ Lead {i} added:")
        print(f"   ID: {lead_id}")
        print(f"   Title: {lead_data['original_lead']['title'][:60]}...")
        print(f"   Score: {lead_data['buyability_score']}")
        print(f"   Source: {lead_data['original_lead']['source']}")
        print()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Added {len(added_leads)} test leads")
    print(f"📊 Total leads in system: {len(processed_leads_store)}")
    print("\n📋 Lead IDs:")
    for lead in added_leads:
        print(f"   - {lead['lead_id']}: {lead['title'][:50]}... (Score: {lead['score']})")
    
    print("\n🌐 Test the unlock flow:")
    print(f"   curl -X POST http://localhost:8000/api/unlock \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -d '{{\"lead_id\": \"{added_leads[0]['lead_id']}\", \"payment_method\": \"nevermined\"}}'")
    
    return added_leads

if __name__ == "__main__":
    try:
        added = add_test_leads_to_store()
        print("\n✅ Test leads added successfully!")
        print("   You can now test the Nevermined unlock workflow in the UI.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
