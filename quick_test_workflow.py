"""
Quick End-to-End Workflow Test
Tests the complete pipeline via FastAPI endpoint
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"


def test_api_health():
    """Test API is running"""
    print("=" * 60)
    print("Step 1: Testing API Health")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is running")
            print(f"   Services: {json.dumps(data.get('services', {}), indent=2)}")
            return True
        else:
            print(f"❌ API returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print(f"   Make sure FastAPI server is running: python api/run_server.py")
        return False


def test_full_pipeline():
    """Test the complete pipeline via API"""
    print("\n" + "=" * 60)
    print("Step 2: Running Full Pipeline (Scrape + Process)")
    print("=" * 60)
    
    keywords = ["CRM", "project management", "hiring", "looking for"]
    
    payload = {
        "keywords": keywords,
        "reddit_subreddits": ["startups", "entrepreneur"],
        "max_per_source": 5,  # Small number for testing
        "process_limit": 3    # Process 3 leads
    }
    
    print(f"Keywords: {keywords}")
    print(f"Max per source: {payload['max_per_source']}")
    print(f"Process limit: {payload['process_limit']}")
    print("\n⏳ Starting pipeline (this may take 5-10 minutes)...")
    print("   - Scraping Reddit & LinkedIn")
    print("   - Processing through CrewAI agents")
    print("   - Storing in API")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/scrape-and-process",
            json=payload,
            timeout=600  # 10 minute timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ Pipeline completed successfully!")
            print(f"\n📊 Results:")
            print(f"   Scraped:")
            print(f"     - Total: {result.get('scrape_results', {}).get('total', 0)}")
            print(f"     - Reddit: {result.get('scrape_results', {}).get('reddit', 0)}")
            print(f"     - LinkedIn: {result.get('scrape_results', {}).get('linkedin', 0)}")
            print(f"   Processed: {result.get('processed_leads_count', 0)} leads")
            print(f"   Failed: {result.get('failed_leads_count', 0)} leads")
            
            return result
        else:
            print(f"\n❌ Pipeline failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print("\n⏱️  Request timed out (scraping may take longer)")
        print("   Check server logs for progress")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_leads():
    """Verify leads are in the API"""
    print("\n" + "=" * 60)
    print("Step 3: Verifying Leads in API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/leads?limit=10&offset=0", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            leads = data.get("leads", [])
            
            print(f"✅ Found {total} total leads in API")
            print(f"   Displaying {len(leads)} leads")
            
            if leads:
                print("\n   Sample leads:")
                for i, lead in enumerate(leads[:5], 1):
                    title = lead.get("original_lead", {}).get("title", "N/A")
                    source = lead.get("original_lead", {}).get("source", "N/A")
                    score = lead.get("buyability_score", "N/A")
                    print(f"   {i}. {title[:60]}...")
                    print(f"      Source: {source} | Score: {score}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run end-to-end test"""
    print("=" * 60)
    print("Lead Sniper AI - End-to-End Workflow Test")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_BASE_URL}")
    
    # Step 1: Check API health
    if not test_api_health():
        print("\n❌ Cannot proceed - API not available")
        print("   Start the server: python api/run_server.py")
        return
    
    # Step 2: Run full pipeline
    result = test_full_pipeline()
    
    # Step 3: Verify leads
    verify_leads()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if result:
        print("✅ End-to-end workflow completed!")
        print(f"\n🌐 View leads in UI: http://localhost:3000")
        print(f"📡 API endpoint: {API_BASE_URL}/api/leads")
        print(f"📚 API docs: {API_BASE_URL}/docs")
    else:
        print("⚠️  Workflow had issues - check logs above")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
