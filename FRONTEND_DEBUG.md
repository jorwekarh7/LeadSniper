# Frontend Debugging Guide

## Issue: Data not displaying despite 200 response

### Symptoms:
- API returns 200 OK
- Console shows "Leads fetched: 2 total"
- UI shows unformatted text instead of Lead Cards

### Debugging Steps:

1. **Check Browser Console:**
   - Open DevTools (F12)
   - Look for:
     - `📊 Leads fetched: X total`
     - `📦 Response structure:` logs
     - `🎴 LeadCard mounted:` logs
     - Any red errors

2. **Check Network Tab:**
   - Verify `/api/leads` request returns 200
   - Check response body contains `leads` array
   - Verify CORS headers are present

3. **Check React Query State:**
   - In console, run:
     ```javascript
     // Check if React Query has data
     window.__REACT_QUERY_STATE__
     ```

4. **Verify Data Structure:**
   ```bash
   curl "http://localhost:8000/api/leads?limit=1" | python -m json.tool
   ```

### Common Issues:

1. **React Query Cache:**
   - Clear cache: Hard refresh (Cmd+Shift+R / Ctrl+Shift+R)
   - Or disable cache temporarily in `LeadFeed.tsx`

2. **CSS Not Loading:**
   - Check if Tailwind classes are being applied
   - Verify `globals.css` is imported

3. **Type Mismatch:**
   - Check TypeScript errors in console
   - Verify `Lead` interface matches API response

### Quick Fixes Applied:

1. ✅ Added safety checks in `LeadCard`
2. ✅ Added debug logging throughout
3. ✅ Disabled auto-refresh to reduce noise
4. ✅ Added error boundaries
5. ✅ Improved data extraction logic

### Next Steps:

If cards still don't render:
1. Check browser console for specific errors
2. Verify CSS is loading (check Computed styles)
3. Try rendering a simple test card manually
4. Check if React Query is actually returning data
