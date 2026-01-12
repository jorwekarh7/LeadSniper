"""
Check which OpenAI account an API key belongs to and its status
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("OpenAI API Key Account Check")
print("=" * 60)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env")
    sys.exit(1)

print(f"✅ API Key found: {api_key[:15]}...{api_key[-10:]}")
print()

try:
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    
    print("⏳ Checking account information...")
    
    # Try to get account info by making a simple API call
    # We'll use the models endpoint which doesn't cost anything
    try:
        models = client.models.list()
        print("✅ API Key is VALID and has access")
        print(f"   Available models: {len(list(models))} models accessible")
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            print("⚠️  API Key is valid but QUOTA EXCEEDED")
        elif "401" in str(e) or "unauthorized" in str(e).lower():
            print("❌ API Key is INVALID or EXPIRED")
        else:
            print(f"⚠️  Error: {e}")
    
    # Try a small test call to see the exact error
    print("\n⏳ Testing with a small API call...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("✅ API Key works! Account has credits available.")
        print(f"   Response received successfully")
        
    except Exception as e:
        error_str = str(e)
        
        if "quota" in error_str.lower() or "insufficient_quota" in error_str.lower():
            print("❌ QUOTA EXCEEDED - Account has no credits")
            print("\n💡 Solutions:")
            print("   1. Add credits to the OpenAI account this key belongs to")
            print("   2. Go to: https://platform.openai.com/account/billing")
            print("   3. Add a payment method and purchase credits")
            print("   4. Or use a different API key from an account with credits")
            
        elif "401" in error_str or "unauthorized" in error_str.lower():
            print("❌ API Key is INVALID")
            print("   The key may be expired or revoked")
            print("   Generate a new key at: https://platform.openai.com/api-keys")
            
        elif "rate_limit" in error_str.lower():
            print("⚠️  RATE LIMIT - Too many requests")
            print("   Wait a few minutes and try again")
            
        else:
            print(f"❌ Error: {error_str}")
            print("\n💡 This could mean:")
            print("   - The account has no credits")
            print("   - The account has exceeded its quota")
            print("   - The API key is invalid")
            print("\n   Check the account at: https://platform.openai.com/account/billing")

except ImportError:
    print("❌ OpenAI package not installed")
    print("   Run: pip install openai")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print("✅ Any OpenAI account's API key will work")
print("⚠️  The account associated with this key needs credits/quota")
print("\n📋 Next Steps:")
print("   1. Identify which account this key belongs to")
print("   2. Add credits to that account: https://platform.openai.com/account/billing")
print("   3. Or use a different API key from an account with credits")
print("=" * 60)
