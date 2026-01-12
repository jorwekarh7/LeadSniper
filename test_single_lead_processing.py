"""
Test single lead processing to debug why processing is failing
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.crew_setup import process_lead
import traceback

load_dotenv()

# Test with a simple lead
test_lead = {
    "source": "reddit",
    "platform": "reddit",
    "title": "Looking for CRM solution",
    "content": "We need a CRM that integrates with Slack. Our current one is terrible and we're looking for alternatives.",
    "author": "test_user",
    "subreddit": "startups",
    "url": "https://reddit.com/r/startups/test",
    "upvotes": 10,
    "comments": 5
}

print("=" * 60)
print("Testing Single Lead Processing")
print("=" * 60)
print(f"\nLead: {test_lead['title']}")
print(f"Content: {test_lead['content'][:100]}...")
print("\n⏳ Processing...")

try:
    result = process_lead(test_lead)
    
    print("\n" + "=" * 60)
    print("Result:")
    print("=" * 60)
    print(f"Success: {result.get('success')}")
    print(f"Status: {result.get('status')}")
    
    if result.get('success'):
        print("\n✅ Processing successful!")
        print(f"\nProcessed result keys: {list(result.keys())}")
        
        if 'processed_result' in result:
            proc_result = result['processed_result']
            print(f"\nProcessed result type: {type(proc_result)}")
            if hasattr(proc_result, 'raw'):
                print(f"Raw output: {proc_result.raw[:500]}...")
            if hasattr(proc_result, 'tasks_output'):
                print(f"Tasks output: {proc_result.tasks_output}")
    else:
        print(f"\n❌ Processing failed!")
        print(f"Error: {result.get('error', 'No error message')}")
        
except Exception as e:
    print(f"\n❌ Exception occurred: {e}")
    traceback.print_exc()
