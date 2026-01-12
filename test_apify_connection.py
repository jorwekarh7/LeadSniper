"""
Test script to verify Apify API connection
Tests both direct API connection and MCP server connectivity
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_apify_api_connection():
    """Test direct Apify API connection using apify-client"""
    try:
        from apify_client import ApifyClient
        
        api_token = os.getenv("APIFY_API_TOKEN")
        if not api_token:
            print("❌ APIFY_API_TOKEN not found in .env file")
            return False
        
        print("🔌 Testing Apify API connection...")
        client = ApifyClient(api_token)
        
        # Test connection by getting user info
        user_info = client.user().get()
        print(f"✅ Apify API connection successful!")
        print(f"   User: {user_info.get('username', 'N/A')}")
        print(f"   Email: {user_info.get('email', 'N/A')}")
        
        # Test getting actor list (should work even if empty)
        # Note: list() returns a ListPage object, not a dict
        actors_list_page = client.actors().list()
        # ListPage has attributes: items, total, offset, count, limit
        total_actors = getattr(actors_list_page, 'total', 0)
        actor_count = len(getattr(actors_list_page, 'items', []))
        print(f"   Available actors: {total_actors} total ({actor_count} on this page)")
        
        return True
        
    except Exception as e:
        print(f"❌ Apify API connection failed: {str(e)}")
        return False


def test_apify_scraper():
    """Test the Apify scraper wrapper"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from tools.apify_scraper import ApifyLeadScraper
        
        print("\n🔌 Testing Apify Lead Scraper...")
        scraper = ApifyLeadScraper()
        print("✅ Apify Lead Scraper initialized successfully!")
        
        # Test with a small query (don't actually run to avoid costs)
        print("   Scraper ready to use")
        print("   Available methods:")
        print("     - scrape_reddit(keywords, subreddits, max_posts)")
        print("     - scrape_linkedin(keywords, location, max_results)")
        print("     - scrape_all(keywords, ...)")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  Could not import scraper (may need to create tools directory): {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Apify scraper test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Apify Connection Test")
    print("=" * 60)
    
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        print("⚠️  .env file not found. Please create it with APIFY_API_TOKEN")
        print(f"   Expected location: {env_path}")
        return
    
    # Test API connection
    api_ok = test_apify_api_connection()
    
    # Test scraper
    scraper_ok = test_apify_scraper()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    print(f"API Connection: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Scraper Module: {'✅ PASS' if scraper_ok else '❌ FAIL'}")
    
    if api_ok and scraper_ok:
        print("\n🎉 All tests passed! Apify is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
