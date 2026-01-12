# Add Test Leads for Nevermined Testing

## Quick Method (Recommended)

Run the script:

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
./add_test_leads.sh
```

Or use curl directly:

```bash
curl -X POST http://localhost:8000/api/test/add-leads \
  -H "Content-Type: application/json"
```

## What This Does

Adds 3 test leads with high buyability scores (82, 85, 88) directly to the system:
- ✅ Lead 1: CRM solution search (Score: 85)
- ✅ Lead 2: Marketing automation migration (Score: 88)  
- ✅ Lead 3: Project management tool search (Score: 82)

All leads have `buyability_score >= 80`, so they will:
- Show "🔓 Unlock with Nevermined" button in UI
- Require payment to view full details
- Test the Nevermined unlock workflow

## Verify Leads Were Added

```bash
# Check total leads
curl http://localhost:8000/api/leads | python -m json.tool

# Check stats
curl http://localhost:8000/api/stats | python -m json.tool
```

## Test Unlock Flow

After adding leads, you can test the unlock:

1. **View in UI**: http://localhost:3000
2. **Click "View Details"** on any lead with score >= 80
3. **Click "🔓 Unlock with Nevermined"** button
4. **Check browser console** for unlock logs
5. **Check server logs** for payment processing

## Troubleshooting

### Endpoint Not Found
- **Cause**: Server needs restart after adding endpoint
- **Fix**: Restart server: `./restart_server.sh`

### No Leads Showing
- **Cause**: Frontend cache or API not returning data
- **Fix**: 
  - Hard refresh browser (Cmd+Shift+R)
  - Check API directly: `curl http://localhost:8000/api/leads`

### Unlock Button Not Working
- **Cause**: Lead score < 80 or unlock endpoint issue
- **Fix**: 
  - Verify lead has score >= 80
  - Check browser console for errors
  - Check server logs for unlock requests

## Expected Results

After running `./add_test_leads.sh`:

```json
{
  "status": "success",
  "message": "Added 3 test leads",
  "leads": [
    {
      "lead_id": "...",
      "title": "Looking for CRM solution...",
      "buyability_score": 85
    },
    ...
  ],
  "total_leads": 3
}
```

Then in the UI, you should see 3 leads, all with "Unlock with Nevermined" buttons!
