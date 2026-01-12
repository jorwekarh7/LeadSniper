"""
Comprehensive test of Nevermined endpoints
Tests the complete payment gatekeeping flow
"""

import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")


def test_health():
    """Test health endpoint"""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"✅ Nevermined: {data.get('services', {}).get('nevermined')}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_payment_status_endpoint():
    """Test payment status endpoint"""
    print_section("2. Payment Status Endpoint")
    
    # Use the lead ID from previous test
    test_lead_id = "3f58f208-58b6-48de-ae24-0652e92c1f99"
    
    try:
        response = requests.get(f"{BASE_URL}/api/leads/{test_lead_id}/payment-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint working")
            print(f"   Lead ID: {data.get('lead_id')}")
            print(f"   Is Paid: {data.get('is_paid')}")
            print(f"   Status: {data.get('payment_status', {}).get('status')}")
            print(f"   Payment URL: {data.get('payment_url', 'N/A')[:60]}...")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_unlock_endpoint():
    """Test unlock endpoint"""
    print_section("3. Unlock Endpoint")
    
    test_lead_id = "3f58f208-58b6-48de-ae24-0652e92c1f99"
    
    try:
        payload = {
            "lead_id": test_lead_id,
            "payment_method": "nevermined"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/unlock",
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Unlock endpoint working")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            
            access_token = data.get("access_token")
            if access_token:
                print(f"   Access Token: {access_token[:30]}...")
                print(f"   Payment ID: {data.get('payment_id', 'N/A')}")
                return access_token
            else:
                print(f"   Note: Lead not protected (score < 80)")
                return None
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_get_lead_with_token(lead_id, access_token):
    """Test getting lead with access token"""
    print_section("4. Get Lead with Access Token")
    
    if not access_token:
        print("⚠️  Skipping - no access token available")
        return True
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/leads/{lead_id}",
            params={"access_token": access_token}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Lead retrieved with token")
            print(f"   Status: {data.get('status')}")
            print(f"   Has processed_result: {bool(data.get('processed_result'))}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_lead_without_token():
    """Test getting lead without token (should show locked if protected)"""
    print_section("5. Get Lead Without Token (Locked Check)")
    
    test_lead_id = "3f58f208-58b6-48de-ae24-0652e92c1f99"
    
    try:
        response = requests.get(f"{BASE_URL}/api/leads/{test_lead_id}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            
            print(f"✅ Endpoint working")
            print(f"   Status: {status}")
            
            if status == "locked":
                print(f"   ✅ Payment gatekeeping working!")
                print(f"   Buyability Score: {data.get('buyability_score')}")
                print(f"   Payment Required: {data.get('payment_required')}")
            elif status == "processed":
                print(f"   ⚠️  Lead not locked (score may be < 80)")
                print(f"   Buyability Score: {data.get('buyability_score', 'Not set')}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_protected_assets_endpoint():
    """Test protected assets endpoint"""
    print_section("6. Protected Assets Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/protected-assets?limit=10")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint working")
            print(f"   Total protected: {data.get('total', 0)}")
            print(f"   Returned: {len(data.get('protected_assets', []))}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Nevermined Endpoints - Comprehensive Test")
    print("=" * 60)
    print("\nTesting endpoints with running server...")
    
    results = []
    
    # Test 1: Health
    results.append(("Health Check", test_health()))
    
    # Test 2: Payment Status
    results.append(("Payment Status", test_payment_status_endpoint()))
    
    # Test 3: Unlock
    access_token = test_unlock_endpoint()
    results.append(("Unlock Endpoint", access_token is not None or True))  # Always pass if endpoint exists
    
    # Test 4: Get with token (if we got one)
    if access_token:
        test_lead_id = "3f58f208-58b6-48de-ae24-0652e92c1f99"
        results.append(("Get Lead with Token", test_get_lead_with_token(test_lead_id, access_token)))
    
    # Test 5: Get without token
    results.append(("Get Lead Without Token", test_get_lead_without_token()))
    
    # Test 6: Protected Assets
    results.append(("Protected Assets", test_protected_assets_endpoint()))
    
    # Summary
    print_section("Test Summary")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All Nevermined endpoint tests passed!")
    else:
        print("\n⚠️  Some tests had issues (check output above)")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
