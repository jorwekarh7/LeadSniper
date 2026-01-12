# Expanded Search Configuration

## What Changed

The search scope has been significantly expanded to capture more high-intent leads:

### 1. Expanded Keywords (25+ keywords)
- **Original**: 4 keywords (CRM, project management, hiring, looking for)
- **New**: 25+ keywords including:
  - Software/Tools: "software", "tool", "platform", "solution", "system"
  - Buying Intent: "alternatives", "replace", "switching", "evaluate", "comparing"
  - Recommendations: "best", "recommend", "suggest", "implement", "integrate"
  - Business Functions: "automation", "marketing", "sales", "analytics", "dashboard"

### 2. More Subreddits (8 instead of 3)
- **Original**: startups, entrepreneur (2 subreddits)
- **New**: 8 subreddits including:
  - startups, entrepreneur, SaaS, smallbusiness
  - entrepreneurship, startup, business, marketing
  - sales, productivity, webdev, programming
  - technology, software, tech, consulting

### 3. Increased Post Limits
- **Reddit**: 30 posts per subreddit (was 20)
- **LinkedIn**: Multiple date ranges (Past 24 hours, Past week, Past month)
- **Total**: Up to 15 leads per source (was 5)

### 4. Expanded Intent Keywords (30+ signals)
- **Original**: 8 intent keywords
- **New**: 30+ intent keywords including:
  - Need signals: "need", "want", "looking for", "seeking"
  - Problem signals: "frustrated", "problem", "issue", "struggling", "challenge", "pain"
  - Evaluation signals: "evaluate", "comparing", "deciding", "choose", "select"
  - Action signals: "purchase", "buy", "implement", "integrate", "migrate", "upgrade"

### 5. Processing Limits
- **Process limit**: 10 leads (was 3) - More leads processed = higher chance of score > 80

## Expected Results

With these changes, you should see:
- **More leads scraped**: 20-30+ leads total (vs 6-10 before)
- **Higher quality signals**: More posts with strong buying intent
- **Better scores**: More leads with buyability_score >= 80
- **Nevermined testing**: At least one lead should trigger the payment gate

## Usage

Run the expanded workflow:

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
./START_WORKFLOW.sh
```

Or use the API directly:

```bash
curl -X POST http://localhost:8000/api/scrape-and-process \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": [
      "CRM", "project management", "hiring", "looking for", "need",
      "software", "tool", "platform", "solution", "system",
      "alternatives", "replace", "switching", "evaluate", "comparing",
      "best", "recommend", "suggest", "implement", "integrate",
      "automation", "marketing", "sales", "analytics", "dashboard"
    ],
    "reddit_subreddits": [
      "startups", "entrepreneur", "SaaS", "smallbusiness",
      "marketing", "sales", "productivity"
    ],
    "max_per_source": 15,
    "process_limit": 10
  }'
```

## Monitoring

Watch for leads with `buyability_score >= 80` - these will:
1. ✅ Be marked as high-value leads
2. ✅ Create Protected Assets in Nevermined
3. ✅ Show "Unlock" button in UI
4. ✅ Require payment to view full details

Check results:
```bash
# View all leads
curl http://localhost:8000/api/leads | python -m json.tool

# Check for high-value leads (score >= 80)
curl http://localhost:8000/api/leads | python -c "import sys, json; leads=json.load(sys.stdin)['leads']; high_value=[l for l in leads if l.get('buyability_score', 0) >= 80]; print(f'High-value leads: {len(high_value)}')"
```
