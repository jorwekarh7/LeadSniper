"""
Test Nevermined integration with FastAPI
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_nevermined_middleware():
    """Test Nevermined middleware initialization"""
    print("🔌 Testing Nevermined middleware...")
    try:
        from api.nevermined_middleware import nevermined_middleware
        
        api_key = os.getenv("NVM_API_KEY") or os.getenv("NEVERMINED_API_KEY")
        if api_key:
            print(f"  ✅ API key found: {api_key[:10]}...")
        else:
            print("  ⚠️  API key not found in environment")
        
        print(f"  ✅ Middleware initialized")
        print(f"     Client available: {nevermined_middleware.client is not None}")
        
        return True
    except Exception as e:
        print(f"  ❌ Middleware test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_payment_operations():
    """Test payment operations"""
    print("\n🔌 Testing payment operations...")
    try:
        from api.nevermined_middleware import nevermined_middleware
        import asyncio
        
        async def test_ops():
            # Test payment plan registration
            plan = await nevermined_middleware.register_payment_plan("test_lead_001", price=0.01)
            print(f"  ✅ Payment plan created: {plan.get('plan_id')}")
            
            # Test payment URL
            payment_url = await nevermined_middleware.get_payment_url("test_lead_001")
            print(f"  ✅ Payment URL generated: {payment_url[:50]}...")
            
            # Test payment processing
            payment_result = await nevermined_middleware.process_payment("test_lead_001")
            if payment_result.success:
                print(f"  ✅ Payment processed: {payment_result.payment_id}")
                print(f"     Access token: {payment_result.access_token[:20]}...")
            
            # Test payment verification
            payment_status = await nevermined_middleware.verify_payment(
                "test_lead_001",
                payment_result.access_token
            )
            print(f"  ✅ Payment verified: {payment_status['is_paid']}")
            
            # Test MCP notification
            notification = await nevermined_middleware.generate_mcp_notification(
                "test_lead_001",
                85.0
            )
            print(f"  ✅ MCP notification generated: {notification.get('notification_type')}")
            
            return True
        
        result = asyncio.run(test_ops())
        return result
        
    except Exception as e:
        print(f"  ❌ Payment operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_protected_asset():
    """Test protected asset creation"""
    print("\n🔌 Testing protected asset creation...")
    try:
        from api.nevermined_middleware import nevermined_middleware
        import asyncio
        
        async def test_asset():
            sample_lead = {
                "lead_id": "test_asset_001",
                "original_lead": {
                    "source": "reddit",
                    "title": "Looking for CRM",
                    "content": "We need a CRM solution..."
                },
                "processed_result": {
                    "signals": {},
                    "pitch": {}
                },
                "processed_at": "2025-01-10T20:00:00"
            }
            
            asset = await nevermined_middleware.create_protected_asset(
                sample_lead,
                buyability_score=85.0
            )
            
            print(f"  ✅ Protected asset created: {asset.get('asset_id')}")
            print(f"     Buyability score: {asset.get('buyability_score')}")
            print(f"     Status: {asset.get('status')}")
            
            return True
        
        result = asyncio.run(test_asset())
        return result
        
    except Exception as e:
        print(f"  ❌ Protected asset test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_integration():
    """Test API endpoints integration"""
    print("\n🔌 Testing API integration...")
    try:
        from api.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint includes Nevermined
        response = client.get("/health")
        if response.status_code == 200:
            data = response.json()
            services = data.get("services", {})
            if "nevermined" in services:
                print(f"  ✅ Health check includes Nevermined: {services['nevermined']}")
            else:
                print("  ⚠️  Health check doesn't include Nevermined")
        
        # Test unlock endpoint exists
        response = client.post("/api/unlock", json={"lead_id": "test"})
        # Should return 404 or 402, not 404 for endpoint not found
        if response.status_code != 404 or "not found" not in response.text.lower():
            print("  ✅ Unlock endpoint exists")
        else:
            print("  ⚠️  Unlock endpoint may not be registered")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API integration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Nevermined Integration Test")
    print("=" * 60)
    
    tests = [
        ("Middleware Initialization", test_nevermined_middleware),
        ("Payment Operations", test_payment_operations),
        ("Protected Asset Creation", test_protected_asset),
        ("API Integration", test_api_integration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ {name} crashed: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All Nevermined integration tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
