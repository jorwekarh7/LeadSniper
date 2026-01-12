"""
Test the unlock endpoint to debug Nevermined integration
"""

import requests
import json

API_URL = "http://localhost:8000"

# First, get a list of leads to find one with score >= 80
print("=" * 60)
print("Testing Nevermined Unlock Endpoint")
print("=" * 60)

print("\n1. Fetching leads...")
response = requests.get(f"{API_URL}/api/leads?limit=10")
if response.status_code == 200:
    data = response.json()
    leads = data.get("leads", [])
    print(f"   Found {len(leads)} leads")
    
    # Find a high-value lead (score >= 80)
    high_value_leads = [l for l in leads if l.get("buyability_score", 0) >= 80]
    
    if high_value_leads:
        test_lead = high_value_leads[0]
        lead_id = test_lead.get("lead_id")
        score = test_lead.get("buyability_score")
        
        print(f"\n2. Found high-value lead:")
        print(f"   Lead ID: {lead_id}")
        print(f"   Score: {score}")
        
        print(f"\n3. Testing unlock endpoint...")
        unlock_response = requests.post(
            f"{API_URL}/api/unlock",
            json={
                "lead_id": lead_id,
                "payment_method": "nevermined"
            }
        )
        
        print(f"   Status: {unlock_response.status_code}")
        
        if unlock_response.status_code == 200:
            unlock_data = unlock_response.json()
            print(f"   ✅ Unlock successful!")
            print(f"   Response: {json.dumps(unlock_data, indent=2)}")
            
            if unlock_data.get("access_token"):
                print(f"\n4. Testing access with token...")
                access_response = requests.get(
                    f"{API_URL}/api/leads/{lead_id}",
                    params={"access_token": unlock_data["access_token"]}
                )
                print(f"   Status: {access_response.status_code}")
                if access_response.status_code == 200:
                    print(f"   ✅ Access granted!")
                else:
                    print(f"   ❌ Access denied: {access_response.text}")
        else:
            print(f"   ❌ Unlock failed!")
            print(f"   Response: {unlock_response.text}")
    else:
        print("\n   ⚠️  No high-value leads found (score >= 80)")
        print("   Run the workflow to generate high-value leads first")
else:
    print(f"   ❌ Failed to fetch leads: {response.status_code}")
    print(f"   Response: {response.text}")

print("\n" + "=" * 60)
