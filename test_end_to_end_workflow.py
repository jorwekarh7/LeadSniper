"""
End-to-End Workflow Test
Tests the complete pipeline: Apify Scraping → CrewAI Processing → Nevermined Protection → UI Display
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.apify_scraper import ApifyLeadScraper
from agents.crew_setup import process_lead
from integrate_scraper_agents import scrape_and_process_leads
import requests
import json
from datetime import datetime

load_dotenv()

API_BASE_URL = "http://localhost:8000"


def test_apify_connection():
    """Test Apify connection"""
    print("\n" + "=" * 60)
    print("Step 1: Testing Apify Connection")
    print("=" * 60)
    
    try:
        scraper = ApifyLeadScraper()
        print("✅ Apify client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Apify connection failed: {e}")
        print("   Make sure APIFY_API_TOKEN is set in .env")
        return False


def test_scraping(keywords, max_per_source=5):
    """Test scraping leads from Reddit and LinkedIn"""
    print("\n" + "=" * 60)
    print("Step 2: Scraping Leads from Reddit & LinkedIn")
    print("=" * 60)
    print(f"Keywords: {keywords}")
    print(f"Max per source: {max_per_source}")
    
    try:
        scraper = ApifyLeadScraper()
        
        # Scrape Reddit
        print("\n📡 Scraping Reddit...")
        reddit_leads = scraper.scrape_reddit(
            keywords=keywords,
            subreddits=["startups", "entrepreneur", "SaaS"],
            max_posts=max_per_source
        )
        print(f"✅ Found {len(reddit_leads)} Reddit leads")
        
        # Scrape LinkedIn
        print("\n📡 Scraping LinkedIn...")
        linkedin_leads = scraper.scrape_linkedin(
            keywords=keywords,
            location="United States",
            max_results=max_per_source
        )
        print(f"✅ Found {len(linkedin_leads)} LinkedIn leads")
        
        total = len(reddit_leads) + len(linkedin_leads)
        print(f"\n✅ Total leads scraped: {total}")
        
        return {
            "reddit": reddit_leads,
            "linkedin": linkedin_leads,
            "total": total
        }
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_processing_via_api(lead_data):
    """Test processing a lead through the FastAPI endpoint"""
    print("\n" + "=" * 60)
    print("Step 3: Processing Lead via FastAPI")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/process",
            json={"lead_data": lead_data},
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            lead_id = result.get("lead_id")
            buyability_score = result.get("buyability_score")
            
            print(f"✅ Lead processed successfully!")
            print(f"   Lead ID: {lead_id}")
            print(f"   Buyability Score: {buyability_score}")
            print(f"   Is High Value: {result.get('is_high_value', False)}")
            
            return result
        else:
            print(f"❌ Processing failed: {response.status_code}")
            print(f"   {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return None


def test_full_pipeline_via_api(keywords, max_per_source=3, process_limit=3):
    """Test the complete pipeline via API endpoint"""
    print("\n" + "=" * 60)
    print("Step 4: Full Pipeline via API (/api/scrape-and-process)")
    print("=" * 60)
    
    try:
        payload = {
            "keywords": keywords,
            "reddit_subreddits": ["startups", "entrepreneur"],
            "max_per_source": max_per_source,
            "process_limit": process_limit
        }
        
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print("\n⏳ Running pipeline (this may take a few minutes)...")
        
        response = requests.post(
            f"{API_BASE_URL}/api/scrape-and-process",
            json=payload,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Pipeline completed!")
            print(f"   Scraped: {result.get('scrape_results', {}).get('total', 0)} leads")
            print(f"   Processed: {result.get('processed_leads_count', 0)} leads")
            print(f"   Failed: {result.get('failed_leads_count', 0)} leads")
            
            return result
        else:
            print(f"❌ Pipeline failed: {response.status_code}")
            print(f"   {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_leads_in_ui():
    """Verify leads are accessible via API"""
    print("\n" + "=" * 60)
    print("Step 5: Verifying Leads in API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/leads?limit=10&offset=0")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            leads = data.get("leads", [])
            
            print(f"✅ API returned {total} total leads")
            print(f"   Displaying {len(leads)} leads")
            
            if leads:
                print("\n   Sample leads:")
                for i, lead in enumerate(leads[:3], 1):
                    title = lead.get("original_lead", {}).get("title", "N/A")
                    source = lead.get("original_lead", {}).get("source", "N/A")
                    score = lead.get("buyability_score", "N/A")
                    print(f"   {i}. {title[:50]}... (Source: {source}, Score: {score})")
            
            return True
        else:
            print(f"❌ Failed to fetch leads: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run complete end-to-end test"""
    print("=" * 60)
    print("Lead Sniper AI - End-to-End Workflow Test")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"API Base URL: {API_BASE_URL}")
    
    # Test 1: Apify Connection
    if not test_apify_connection():
        print("\n❌ Cannot proceed without Apify connection")
        return
    
    # Test 2: Scraping
    keywords = ["CRM", "project management", "hiring", "looking for", "need"]
    scrape_results = test_scraping(keywords, max_per_source=5)
    
    if not scrape_results or scrape_results["total"] == 0:
        print("\n⚠️  No leads scraped. Cannot proceed with processing.")
        return
    
    # Test 3: Process a single lead via API
    if scrape_results["reddit"]:
        sample_lead = scrape_results["reddit"][0]
        print(f"\n📝 Processing sample Reddit lead: {sample_lead.get('title', 'N/A')[:50]}...")
        processed_result = test_processing_via_api(sample_lead)
        
        if processed_result:
            print("\n✅ Single lead processing works!")
    
    # Test 4: Full pipeline via API
    print("\n" + "=" * 60)
    print("Running Full Pipeline (Scrape + Process)")
    print("=" * 60)
    print("This will:")
    print("  1. Scrape leads from Reddit & LinkedIn")
    print("  2. Process them through CrewAI agents")
    print("  3. Store them in the API")
    print("  4. Make them available in the UI")
    print("\n⚠️  This may take 5-10 minutes depending on API response times...")
    
    pipeline_result = test_full_pipeline_via_api(
        keywords=keywords,
        max_per_source=3,  # Small number for testing
        process_limit=3     # Process 3 leads
    )
    
    # Test 5: Verify leads are accessible
    verify_leads_in_ui()
    
    # Final Summary
    print("\n" + "=" * 60)
    print("End-to-End Test Summary")
    print("=" * 60)
    
    if pipeline_result:
        print("✅ Full pipeline completed successfully!")
        print(f"\n📊 Results:")
        print(f"   - Leads scraped: {pipeline_result.get('scrape_results', {}).get('total', 0)}")
        print(f"   - Leads processed: {pipeline_result.get('processed_leads_count', 0)}")
        print(f"   - Leads failed: {pipeline_result.get('failed_leads_count', 0)}")
        print(f"\n🌐 View leads in UI: http://localhost:3000")
        print(f"📡 API endpoint: {API_BASE_URL}/api/leads")
    else:
        print("⚠️  Pipeline had issues. Check logs above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
