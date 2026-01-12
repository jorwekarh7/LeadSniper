# Unlock Button Debugging Guide

## Issue: "Unlock with Nevermined" button not working

## What I've Fixed

1. ✅ **Added detailed logging** to the unlock endpoint
2. ✅ **Added error handling** in the frontend API client
3. ✅ **Verified API key** is loaded correctly (NVM_API_KEY is SET)
4. ✅ **Verified Nevermined middleware** shows as "ready" in health check

## Debugging Steps

### 1. Check Browser Console

Open your browser's Developer Tools (F12) and check the Console tab when clicking "Unlock with Nevermined". Look for:
- `🔓 Unlocking lead: <lead_id>` - Frontend is calling the API
- `✅ Unlock response:` - API call succeeded
- `❌ Unlock error:` - API call failed (check the error details)

### 2. Check Server Logs

When you click the unlock button, the server should log:
```
🔓 Unlock request received for lead_id: <id>
   Payment method: nevermined
   Lead found, buyability_score: <score>
   ✅ Lead is protected, processing payment...
   Payment result: success=True
   ✅ Payment successful, returning access token
```

### 3. Common Issues

#### Issue: "Lead not found"
- **Cause**: Lead ID doesn't match what's in the store
- **Fix**: Check that the lead was processed and stored correctly

#### Issue: "Lead is not protected"
- **Cause**: Buyability score < 80
- **Fix**: Need a lead with score >= 80 to test unlock

#### Issue: CORS Error
- **Cause**: Frontend can't reach backend
- **Fix**: Check API_BASE_URL in frontend/.env.local

#### Issue: Network Error
- **Cause**: Backend server not running
- **Fix**: Start the server: `python api/run_server.py`

### 4. Test the Endpoint Directly

```bash
# Get a lead ID first
curl http://localhost:8000/api/leads | python -m json.tool

# Test unlock (replace <lead_id> with actual ID)
curl -X POST http://localhost:8000/api/unlock \
  -H "Content-Type: application/json" \
  -d '{"lead_id": "<lead_id>", "payment_method": "nevermined"}'
```

### 5. Verify Nevermined API Key

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('NVM_API_KEY:', 'SET' if os.getenv('NVM_API_KEY') else 'MISSING')"
```

## Expected Flow

1. User clicks "🔓 Unlock with Nevermined" button
2. Frontend calls `POST /api/unlock` with `lead_id`
3. Backend checks if lead exists and is protected (score >= 80)
4. Backend processes payment via Nevermined middleware
5. Backend returns `access_token` if successful
6. Frontend uses `access_token` to fetch full lead details
7. Frontend displays unlocked content

## Next Steps

1. **Check browser console** for errors
2. **Check server logs** for unlock requests
3. **Verify you have a lead with score >= 80**
4. **Test the endpoint directly** with curl
5. **Restart the server** if API key was recently added

## If Still Not Working

Share:
- Browser console errors
- Server log output
- Lead ID you're trying to unlock
- Buyability score of the lead
