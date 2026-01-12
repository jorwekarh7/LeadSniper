"""
Step-by-Step Workflow Test
Tests each phase separately for better debugging
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.apify_scraper import ApifyLeadScraper
from agents.crew_setup import process_lead
import requests
import json

load_dotenv()

API_BASE_URL = "http://localhost:8000"


def test_step_1_scraping():
    """Test Step 1: Scraping"""
    print("=" * 60)
    print("STEP 1: Testing Apify Scraping")
    print("=" * 60)
    
    try:
        scraper = ApifyLeadScraper()
        print("✅ Apify client initialized")
        
        keywords = ["CRM", "project management"]
        print(f"\n📡 Scraping Reddit with keywords: {keywords}")
        
        reddit_leads = scraper.scrape_reddit(
            keywords=keywords,
            subreddits=["startups"],
            max_posts=3
        )
        
        print(f"✅ Scraped {len(reddit_leads)} Reddit leads")
        
        if reddit_leads:
            print("\n   Sample lead:")
            lead = reddit_leads[0]
            print(f"   Title: {lead.get('title', 'N/A')[:60]}...")
            print(f"   Source: {lead.get('source')}")
            print(f"   Subreddit: {lead.get('subreddit')}")
        
        return reddit_leads
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        return []


def test_step_2_processing(lead_data):
    """Test Step 2: Processing via API"""
    print("\n" + "=" * 60)
    print("STEP 2: Testing Lead Processing via API")
    print("=" * 60)
    
    try:
        print(f"📝 Processing lead: {lead_data.get('title', 'N/A')[:50]}...")
        
        response = requests.post(
            f"{API_BASE_URL}/api/process",
            json={"lead_data": lead_data},
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Lead processed successfully!")
            print(f"   Lead ID: {result.get('lead_id')}")
            print(f"   Buyability Score: {result.get('buyability_score')}")
            return result
        else:
            print(f"❌ Processing failed: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_step_3_verify():
    """Test Step 3: Verify leads in API"""
    print("\n" + "=" * 60)
    print("STEP 3: Verifying Leads in API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/leads?limit=10")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            leads = data.get("leads", [])
            
            print(f"✅ Found {total} total leads")
            
            if leads:
                print(f"\n   Recent leads:")
                for i, lead in enumerate(leads[:3], 1):
                    title = lead.get("original_lead", {}).get("title", "N/A")
                    source = lead.get("original_lead", {}).get("source", "N/A")
                    score = lead.get("buyability_score", "N/A")
                    print(f"   {i}. {title[:50]}...")
                    print(f"      Source: {source} | Score: {score}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run step-by-step test"""
    print("=" * 60)
    print("Lead Sniper AI - Step-by-Step Workflow Test")
    print("=" * 60)
    print("\nThis test will:")
    print("  1. Scrape a few leads from Reddit")
    print("  2. Process one lead through CrewAI agents")
    print("  3. Verify it's stored in the API")
    print("  4. Check it appears in the UI")
    print()
    
    # Step 1: Scrape
    leads = test_step_1_scraping()
    
    if not leads:
        print("\n⚠️  No leads scraped. Cannot proceed.")
        print("   Check:")
        print("   - APIFY_API_TOKEN is set in .env")
        print("   - Apify MCP is connected in Cursor")
        return
    
    # Step 2: Process first lead
    if leads:
        result = test_step_2_processing(leads[0])
        
        if result:
            print("\n✅ Processing successful!")
        else:
            print("\n⚠️  Processing failed. Check server logs.")
    
    # Step 3: Verify
    test_step_3_verify()
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print("\n🌐 View leads in UI: http://localhost:3000")
    print("📡 API: http://localhost:8000/api/leads")


if __name__ == "__main__":
    main()
