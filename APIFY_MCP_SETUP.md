# Apify MCP Server Setup Guide

## ✅ MCP Server Configuration Created

I've created the MCP server configuration file at `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com"
    }
  }
}
```

## 🔐 Next Steps to Connect

### 1. Add Your Apify API Token to .env

Create or update your `.env` file in the project root:

```bash
APIFY_API_TOKEN=your_apify_api_token_here
```

Get your API token from: https://console.apify.com/account/integrations

### 2. Restart Cursor

After adding the MCP configuration, restart Cursor to load the MCP server connection.

### 3. Test the Connection

Once Cursor restarts, you can test the Apify MCP connection by:

1. **Using the test script:**
   ```bash
   source venv/bin/activate
   python test_apify_connection.py
   ```

2. **Or test directly in Python:**
   ```python
   from tools.apify_scraper import ApifyLeadScraper
   scraper = ApifyLeadScraper()
   # Test with a small query
   ```

### 4. Using Apify MCP Tools in Cursor

After the MCP server is connected, you can use Apify tools directly through Cursor's MCP interface. The MCP server will handle authentication via OAuth when you first use it.

## 📋 Available Apify Tools

Once connected, you'll have access to:

- **Reddit Scraper** - Scrape Reddit posts for buying intent signals
- **LinkedIn Scraper** - Scrape LinkedIn profiles and posts
- **Custom Actors** - Run any Apify actor from your account

## 🧪 Testing the Connection

Run the test script to verify everything works:

```bash
cd /Users/oabolade/agents_app_build/lead_sniper_ai
source venv/bin/activate
python test_apify_connection.py
```

This will:
- ✅ Test your API token
- ✅ Verify the Apify client connection
- ✅ Test the scraper wrapper functions

## 🔗 Resources

- Apify Console: https://console.apify.com
- Apify MCP Docs: https://docs.apify.com/platform/integrations/mcp
- Get API Token: https://console.apify.com/account/integrations
