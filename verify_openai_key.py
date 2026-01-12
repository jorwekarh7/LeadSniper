"""
Verify OpenAI API Key is Loaded Correctly
Tests that the new API key from .env is being used
"""

import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 60)
print("OpenAI API Key Verification")
print("=" * 60)

# Get the key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in environment")
    print("   Make sure .env file exists and contains OPENAI_API_KEY")
    sys.exit(1)

# Show first and last few characters (for security)
key_preview = f"{api_key[:10]}...{api_key[-10:]}" if len(api_key) > 20 else "***"
print(f"✅ API Key found: {key_preview}")
print(f"   Full length: {len(api_key)} characters")
print(f"   Starts with: {api_key[:7]}")

# Test the key with OpenAI
print("\n" + "=" * 60)
print("Testing API Key with OpenAI")
print("=" * 60)

try:
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    
    # Make a simple test call
    print("⏳ Making test API call...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'API key works' if you can read this."}],
        max_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"✅ API Key is VALID!")
    print(f"   Response: {result}")
    print(f"   Model used: {response.model}")
    
except Exception as e:
    error_str = str(e)
    
    if "401" in error_str or "unauthorized" in error_str.lower():
        print("❌ API Key is INVALID or EXPIRED")
        print("   Error: Unauthorized - Check your API key")
    elif "429" in error_str or "quota" in error_str.lower():
        print("⚠️  API Key is valid but QUOTA EXCEEDED")
        print("   Error: Quota exceeded - Add credits to your OpenAI account")
    elif "rate limit" in error_str.lower():
        print("⚠️  API Key is valid but RATE LIMITED")
        print("   Error: Rate limit - Wait a moment and try again")
    else:
        print(f"❌ Error testing API key: {error_str}")
        print("   Check your internet connection and OpenAI service status")

print("\n" + "=" * 60)
print("Verification Complete")
print("=" * 60)
