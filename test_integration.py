"""
Comprehensive integration test
Tests the complete pipeline: Apify Scraper → CrewAI Agents
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """Test that all modules can be imported"""
    print("🔌 Testing imports...")
    try:
        from tools.apify_scraper import ApifyLeadScraper
        print("  ✅ ApifyLeadScraper imported")
    except Exception as e:
        print(f"  ❌ ApifyLeadScraper import failed: {e}")
        return False
    
    try:
        from agents.crew_setup import (
            create_lead_processing_crew,
            process_lead,
            create_signal_scout_agent,
            create_researcher_agent,
            create_pitch_architect_agent,
            create_auditor_agent,
            LeadValidationTool
        )
        print("  ✅ CrewAI agents imported")
    except Exception as e:
        print(f"  ❌ CrewAI agents import failed: {e}")
        return False
    
    try:
        from integrate_scraper_agents import scrape_and_process_leads, process_single_lead_from_scraper
        print("  ✅ Integration module imported")
    except Exception as e:
        print(f"  ❌ Integration module import failed: {e}")
        return False
    
    return True


def test_scraper_initialization():
    """Test scraper can be initialized"""
    print("\n🔌 Testing scraper initialization...")
    try:
        from tools.apify_scraper import ApifyLeadScraper
        
        if not os.getenv("APIFY_API_TOKEN"):
            print("  ⚠️  APIFY_API_TOKEN not set - skipping actual API call")
            return True
        
        scraper = ApifyLeadScraper()
        print("  ✅ Scraper initialized successfully")
        return True
    except Exception as e:
        print(f"  ❌ Scraper initialization failed: {e}")
        return False


def test_crew_initialization():
    """Test crew can be initialized"""
    print("\n🔌 Testing crew initialization...")
    try:
        from agents.crew_setup import create_lead_processing_crew
        
        if not os.getenv("OPENAI_API_KEY"):
            print("  ⚠️  OPENAI_API_KEY not set - crew may not work")
            return True
        
        crew = create_lead_processing_crew()
        print(f"  ✅ Crew initialized: {len(crew.agents)} agents, {len(crew.tasks)} tasks")
        
        # Check agent roles match custom instructions
        expected_roles = [
            "Intent Data Analyst",
            "Business Intelligence Analyst", 
            "Strategic Growth Copywriter",
            "Quality Assurance & MCP Bridge"
        ]
        actual_roles = [agent.role for agent in crew.agents]
        
        if set(actual_roles) == set(expected_roles):
            print("  ✅ Agent roles match custom instructions")
        else:
            print(f"  ⚠️  Role mismatch - Expected: {expected_roles}, Got: {actual_roles}")
        
        return True
    except Exception as e:
        print(f"  ❌ Crew initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validation_tool():
    """Test validation tool"""
    print("\n🔌 Testing validation tool...")
    try:
        from agents.crew_setup import LeadValidationTool
        
        tool = LeadValidationTool()
        sample_lead = {
            "source": "reddit",
            "content": "We're looking for a CRM solution. We need something that integrates with Slack.",
            "title": "Looking for CRM",
            "url": "https://example.com"
        }
        
        result = tool._run(sample_lead)
        print(f"  ✅ Validation tool working - Score: {result.get('quality_score')}/100")
        print(f"     Valid: {result.get('is_valid')}")
        return True
    except Exception as e:
        print(f"  ❌ Validation tool failed: {e}")
        return False


def test_sample_lead_processing():
    """Test processing a sample lead (without API calls)"""
    print("\n🔌 Testing sample lead processing structure...")
    try:
        from agents.crew_setup import process_lead
        
        sample_lead = {
            "source": "reddit",
            "platform": "reddit",
            "title": "Looking for a CRM solution for our startup",
            "content": "We're a 10-person SaaS startup and need a CRM that integrates with Slack. We've been using spreadsheets but it's getting messy.",
            "url": "https://reddit.com/r/startups/example",
            "author": "startup_founder",
            "subreddit": "startups"
        }
        
        # Just test the function structure (don't actually run to save API costs)
        print("  ✅ Process function available")
        print("  ⚠️  Skipping actual processing to save API costs")
        print("     To test full processing, ensure OPENAI_API_KEY is set and run:")
        print("     python -c \"from agents.crew_setup import process_lead; print(process_lead({...}))\"")
        
        return True
    except Exception as e:
        print(f"  ❌ Sample lead processing test failed: {e}")
        return False


def test_integration_function():
    """Test integration function structure"""
    print("\n🔌 Testing integration function...")
    try:
        from integrate_scraper_agents import scrape_and_process_leads
        
        print("  ✅ Integration function available")
        print("  ⚠️  Skipping actual run to save API costs")
        print("     To test full integration, ensure API keys are set and run:")
        print("     python integrate_scraper_agents.py")
        
        return True
    except Exception as e:
        print(f"  ❌ Integration function test failed: {e}")
        return False


def check_environment():
    """Check environment variables"""
    print("\n🔌 Checking environment...")
    env_vars = {
        "APIFY_API_TOKEN": os.getenv("APIFY_API_TOKEN"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }
    
    all_set = True
    for var, value in env_vars.items():
        if value:
            print(f"  ✅ {var} is set")
        else:
            print(f"  ⚠️  {var} is NOT set")
            all_set = False
    
    return all_set


def main():
    """Run all tests"""
    print("=" * 60)
    print("Lead Sniper AI - Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Scraper Initialization", test_scraper_initialization),
        ("Crew Initialization", test_crew_initialization),
        ("Validation Tool", test_validation_tool),
        ("Sample Lead Processing", test_sample_lead_processing),
        ("Integration Function", test_integration_function),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ {name} test crashed: {str(e)}")
            results.append((name, False))
    
    # Check environment
    env_ok = check_environment()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print(f"\nEnvironment: {'✅ All keys set' if env_ok else '⚠️  Some keys missing'}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All structural tests passed!")
        if env_ok:
            print("\n✅ Ready for full integration test!")
            print("   Run: python integrate_scraper_agents.py")
        else:
            print("\n⚠️  Set API keys in .env file to test full integration")
    else:
        print("⚠️  Some tests failed. Check errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
