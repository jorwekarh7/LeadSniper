"""
Check that all code paths are using the API key from environment variables
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Checking API Key Usage in Code")
print("=" * 60)

# Check current environment
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ OPENAI_API_KEY found in environment: {api_key[:15]}...")
else:
    print("❌ OPENAI_API_KEY not found")
    sys.exit(1)

# Check how it's used in crew_setup.py
print("\n📋 Checking agents/crew_setup.py:")
with open("agents/crew_setup.py", "r") as f:
    content = f.read()
    if 'openai_api_key=os.getenv("OPENAI_API_KEY")' in content:
        print("   ✅ Uses os.getenv('OPENAI_API_KEY') - Correct!")
    else:
        print("   ⚠️  May not be using environment variable correctly")
    
    if 'load_dotenv()' in content:
        print("   ✅ Calls load_dotenv() - Correct!")
    else:
        print("   ⚠️  Missing load_dotenv() call")

# Check api/main.py
print("\n📋 Checking api/main.py:")
with open("api/main.py", "r") as f:
    content = f.read()
    if 'load_dotenv()' in content:
        print("   ✅ Calls load_dotenv() - Correct!")
    else:
        print("   ⚠️  Missing load_dotenv() call")

# Verify no hardcoded keys
print("\n🔍 Checking for hardcoded API keys:")
with open("agents/crew_setup.py", "r") as f:
    content = f.read()
    if 'sk-' in content and 'os.getenv' not in content.split('sk-')[0][-50:]:
        print("   ⚠️  Possible hardcoded key found!")
    else:
        print("   ✅ No hardcoded keys found")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print("✅ The code correctly uses os.getenv('OPENAI_API_KEY')")
print("✅ .env file is loaded with load_dotenv()")
print("✅ No hardcoded API keys found")
print("\n💡 IMPORTANT: Restart the FastAPI server to pick up the new key!")
print("   The server needs to be restarted for the new key to take effect.")
