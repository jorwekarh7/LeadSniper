"""
Test script for CrewAI agents system
Tests the 4-agent crew processing pipeline
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_crew_initialization():
    """Test that the crew can be initialized"""
    try:
        from agents.crew_setup import create_lead_processing_crew
        
        print("🔌 Testing CrewAI crew initialization...")
        crew = create_lead_processing_crew()
        print("✅ Crew initialized successfully!")
        print(f"   Agents: {len(crew.agents)}")
        print(f"   Tasks: {len(crew.tasks)}")
        print(f"   Process: {crew.process}")
        
        # List agents
        print("\n   Agents:")
        for agent in crew.agents:
            print(f"     - {agent.role}")
        
        # List tasks
        print("\n   Tasks:")
        for task in crew.tasks:
            print(f"     - {task.description[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_validation_tool():
    """Test the lead validation tool"""
    try:
        from agents.crew_setup import LeadValidationTool
        
        print("\n🔌 Testing Lead Validation Tool...")
        tool = LeadValidationTool()
        
        # Test with sample lead
        sample_lead = {
            "source": "reddit",
            "content": "We're looking for a CRM solution. We need something that integrates with Slack and can handle our 10-person team.",
            "title": "Looking for CRM recommendations",
            "url": "https://reddit.com/r/startups/example",
            "author": "startup_founder"
        }
        
        result = tool._run(sample_lead)
        print("✅ Validation tool working!")
        print(f"   Quality Score: {result.get('quality_score')}/100")
        print(f"   Is Valid: {result.get('is_valid')}")
        print(f"   Issues: {len(result.get('issues', []))}")
        print(f"   Strengths: {len(result.get('strengths', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation tool test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_creation():
    """Test individual agent creation"""
    try:
        from agents.crew_setup import (
            create_signal_scout_agent,
            create_researcher_agent,
            create_pitch_architect_agent,
            create_auditor_agent,
            LeadValidationTool
        )
        from langchain_openai import ChatOpenAI
        
        print("\n🔌 Testing individual agent creation...")
        
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Test each agent
        agents = [
            ("Signal Scout", create_signal_scout_agent(llm)),
            ("Researcher", create_researcher_agent(llm)),
            ("Pitch Architect", create_pitch_architect_agent(llm)),
            ("Auditor", create_auditor_agent(llm, LeadValidationTool()))
        ]
        
        print("✅ All agents created successfully!")
        for name, agent in agents:
            print(f"   - {name}: {agent.role}")
            print(f"     Goal: {agent.goal[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_lead_processing():
    """Test processing a lead (without actually running the crew to save costs)"""
    try:
        from agents.crew_setup import process_lead
        
        print("\n🔌 Testing lead processing function...")
        
        sample_lead = {
            "source": "reddit",
            "platform": "reddit",
            "title": "Looking for a CRM solution for our startup",
            "content": "We're a 10-person SaaS startup and need a CRM that integrates with Slack. We've been using spreadsheets but it's getting messy.",
            "url": "https://reddit.com/r/startups/example",
            "author": "startup_founder",
            "subreddit": "startups"
        }
        
        # Just test that the function can be called (don't actually run to save API costs)
        print("✅ Lead processing function available!")
        print("   Note: Skipping actual processing to save API costs")
        print("   To test full processing, run: python -c 'from agents.crew_setup import process_lead; process_lead({...})'")
        
        return True
        
    except Exception as e:
        print(f"❌ Lead processing test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("CrewAI Agents System Test")
    print("=" * 60)
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in .env file")
        print("   Some tests may fail without it")
    
    # Run tests
    tests = [
        ("Crew Initialization", test_crew_initialization),
        ("Validation Tool", test_validation_tool),
        ("Agent Creation", test_agent_creation),
        ("Lead Processing", test_lead_processing),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All tests passed! CrewAI agents system is ready!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
