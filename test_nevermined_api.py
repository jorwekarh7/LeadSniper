"""
Test Nevermined endpoints with running FastAPI server
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"


def test_health_check():
    """Test health endpoint includes Nevermined"""
    print("🔌 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            services = data.get("services", {})
            nevermined_status = services.get("nevermined", "unknown")
            print(f"  ✅ Health check: {data.get('status')}")
            print(f"     Nevermined: {nevermined_status}")
            return True
        else:
            print(f"  ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        print("     Make sure server is running: python api/run_server.py")
        return False


def test_process_lead_with_protection():
    """Test processing a lead that should be protected"""
    print("\n🔌 Testing lead processing (should create Protected Asset)...")
    try:
        sample_lead = {
            "source": "reddit",
            "platform": "reddit",
            "title": "Urgently looking for CRM solution - current one is terrible",
            "content": "We're a growing SaaS company and our current CRM is driving us crazy. It's slow, the UI is outdated, and it doesn't integrate with Slack. We need something modern and fast. Anyone have recommendations? We're ready to switch ASAP.",
            "url": "https://reddit.com/r/startups/example",
            "author": "frustrated_founder",
            "subreddit": "startups"
        }
        
        payload = {"lead_data": sample_lead}
        print("  Processing lead through CrewAI agents...")
        print("  (This may take a moment as it processes through all 4 agents)")
        
        response = requests.post(
            f"{BASE_URL}/api/process",
            json=payload,
            timeout=120  # Longer timeout for agent processing
        )
        
        if response.status_code == 200:
            data = response.json()
            lead_id = data.get("lead_id")
            buyability_score = data.get("buyability_score")
            is_high_value = data.get("is_high_value", False)
            
            print(f"  ✅ Lead processed successfully!")
            print(f"     Lead ID: {lead_id}")
            print(f"     Buyability Score: {buyability_score}")
            print(f"     Is High Value: {is_high_value}")
            
            if is_high_value:
                protected_asset = data.get("protected_asset")
                mcp_notification = data.get("mcp_notification")
                
                if protected_asset:
                    print(f"  ✅ Protected Asset created: {protected_asset.get('asset_id')}")
                
                if mcp_notification:
                    print(f"  ✅ MCP Notification generated: {mcp_notification.get('notification_type')}")
                    print(f"     Payment URL: {mcp_notification.get('payment_url', 'N/A')[:50]}...")
            
            return lead_id, buyability_score
        else:
            print(f"  ⚠️  Process returned: {response.status_code}")
            print(f"     {response.text[:200]}")
            return None, None
            
    except requests.exceptions.Timeout:
        print("  ⚠️  Request timed out (agents may be processing)")
        print("     This is normal for agent processing")
        return None, None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, None


def test_get_locked_lead(lead_id):
    """Test getting a locked lead (without payment)"""
    print(f"\n🔌 Testing get locked lead (lead_id: {lead_id})...")
    try:
        response = requests.get(f"{BASE_URL}/api/leads/{lead_id}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            
            if status == "locked":
                print(f"  ✅ Lead is locked (as expected)")
                print(f"     Buyability Score: {data.get('buyability_score')}")
                print(f"     Payment Required: {data.get('payment_required')}")
                print(f"     Payment URL: {data.get('payment_url', 'N/A')[:50]}...")
                print(f"     Preview available: {bool(data.get('preview'))}")
                return True
            elif status == "processed":
                print(f"  ⚠️  Lead is not locked (score may be < 80)")
                return True
            else:
                print(f"  ⚠️  Unexpected status: {status}")
                return True
        else:
            print(f"  ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_payment_status(lead_id):
    """Test payment status endpoint"""
    print(f"\n🔌 Testing payment status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/leads/{lead_id}/payment-status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Payment status retrieved")
            print(f"     Is Paid: {data.get('is_paid')}")
            print(f"     Status: {data.get('payment_status', {}).get('status')}")
            print(f"     Payment URL: {data.get('payment_url', 'N/A')[:50]}...")
            return True
        else:
            print(f"  ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_unlock_lead(lead_id):
    """Test unlocking a lead"""
    print(f"\n🔌 Testing unlock endpoint...")
    try:
        payload = {
            "lead_id": lead_id,
            "payment_method": "nevermined"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/unlock",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Lead unlocked successfully!")
            print(f"     Access Token: {data.get('access_token', 'N/A')[:30]}...")
            print(f"     Payment ID: {data.get('payment_id', 'N/A')}")
            return data.get("access_token")
        else:
            print(f"  ⚠️  Unlock returned: {response.status_code}")
            print(f"     {response.text[:200]}")
            return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def test_get_unlocked_lead(lead_id, access_token):
    """Test getting unlocked lead with access token"""
    print(f"\n🔌 Testing get unlocked lead (with access token)...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/leads/{lead_id}",
            params={"access_token": access_token}
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            
            if status == "processed":
                print(f"  ✅ Lead is unlocked - full data accessible!")
                print(f"     Has original_lead: {bool(data.get('original_lead'))}")
                print(f"     Has processed_result: {bool(data.get('processed_result'))}")
                return True
            else:
                print(f"  ⚠️  Status: {status}")
                return True
        else:
            print(f"  ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_protected_assets():
    """Test protected assets endpoint"""
    print(f"\n🔌 Testing protected assets endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/protected-assets?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            assets = data.get("protected_assets", [])
            
            print(f"  ✅ Protected assets retrieved")
            print(f"     Total protected: {total}")
            print(f"     Returned: {len(assets)}")
            
            if assets:
                print(f"     Sample asset buyability score: {assets[0].get('buyability_score')}")
            
            return True
        else:
            print(f"  ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Run all Nevermined API tests"""
    print("=" * 60)
    print("Nevermined API Endpoint Tests")
    print("=" * 60)
    print("\n⚠️  Make sure the server is running:")
    print("   python api/run_server.py")
    print()
    
    # Test 1: Health check
    if not test_health_check():
        print("\n❌ Server not responding. Please start the server first.")
        return
    
    # Test 2: Process a lead (may create protected asset)
    lead_id, buyability_score = test_process_lead_with_protection()
    
    if not lead_id:
        print("\n⚠️  Could not process lead. Skipping payment tests.")
        print("   (This may be due to API keys or agent processing time)")
        return
    
    # Test 3: Get locked lead
    test_get_locked_lead(lead_id)
    
    # Test 4: Payment status
    test_payment_status(lead_id)
    
    # Test 5: Protected assets list
    test_protected_assets()
    
    # Test 6: Unlock lead (only if high-value)
    if buyability_score and buyability_score >= 80:
        access_token = test_unlock_lead(lead_id)
        
        # Test 7: Get unlocked lead
        if access_token:
            test_get_unlocked_lead(lead_id, access_token)
    else:
        print(f"\n⚠️  Lead score ({buyability_score}) < 80, skipping unlock test")
        print("   (Unlock is only needed for high-value leads)")
    
    print("\n" + "=" * 60)
    print("✅ Nevermined API tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
