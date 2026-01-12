# OpenAI API Key Guide

## Can I Use Any Account's API Key?

**Yes!** Any OpenAI account's API key will work with this system. It doesn't need to be your personal account.

## Requirements

The only requirement is that **the account associated with the API key must have credits/quota available**.

## Common Issues

### Issue: "Quota Exceeded" Error

**Meaning:** The account this API key belongs to has:
- No credits remaining
- Exceeded its usage quota
- No payment method attached

**Solution:**
1. **Identify the account:** Log into https://platform.openai.com with the account that owns this API key
2. **Check billing:** Go to https://platform.openai.com/account/billing
3. **Add credits:** 
   - Add a payment method if needed
   - Purchase credits/add funds
   - Wait a few minutes for credits to activate

### Issue: "Invalid API Key" Error

**Meaning:** The API key is:
- Expired
- Revoked
- Incorrectly copied

**Solution:**
1. Generate a new API key: https://platform.openai.com/api-keys
2. Copy it carefully (no extra spaces)
3. Update `.env` file
4. Restart the server

## How to Check Which Account a Key Belongs To

1. Log into https://platform.openai.com
2. Go to API Keys: https://platform.openai.com/api-keys
3. Check if your key is listed there
4. If not, the key belongs to a different account

## Using Multiple Accounts

You can use API keys from multiple accounts:

1. **Option 1:** Use one key in `.env` for all processing
2. **Option 2:** Rotate keys if one account runs out of credits
3. **Option 3:** Use different keys for different environments (dev/prod)

## Best Practices

1. **Keep keys secure:** Never commit `.env` files to git
2. **Monitor usage:** Check billing regularly to avoid surprises
3. **Set limits:** Use OpenAI's usage limits to control costs
4. **Track costs:** Monitor API usage in the OpenAI dashboard

## Quick Verification

Run this to check your current API key:

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python check_openai_account.py
```

## Getting Help

- **OpenAI Support:** https://help.openai.com
- **Billing Issues:** https://platform.openai.com/account/billing
- **API Documentation:** https://platform.openai.com/docs
