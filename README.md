# Lead Sniper AI 🎯

An agentic system that optimizes leads based on true signals and intent. Built for B2B SaaS sales teams who struggle with low response rates from generic cold outreach.

## 🚀 Features

- **Multi-Source Lead Scraping**: Scrapes buying intent signals from Reddit and LinkedIn using Apify
- **AI-Powered Processing**: 4-agent CrewAI system (Signal Scout, Researcher, Pitch Architect, Auditor)
- **Intent Detection**: Identifies active buying intent signals and trigger events
- **Hyper-Personalized Pitches**: Generates custom outreach messages in under 2 minutes
- **Quality Scoring**: Validates leads using Kalibr/Pycalib with buyability scores (0-100)
- **Monetization**: Nevermined integration for payment gatekeeping on high-value leads (score >= 80)
- **Modern UI**: Next.js frontend with dark, futuristic "cyber-pro" theme
- **MCP Integration**: Exposes results via Model Context Protocol for Cursor integration

## 🏗️ Architecture

```
Apify Scraper → CrewAI Agents → Kalibr/Pycalib Validation → Nevermined Monetization → Next.js UI
```

### Components

1. **Apify Scraper** (`tools/apify_scraper.py`)
   - Scrapes Reddit and LinkedIn for buying intent signals
   - Filters posts with intent keywords
   - Returns structured lead data

2. **CrewAI Agents** (`agents/crew_setup.py`)
   - **Signal Scout**: Identifies active intent signals
   - **Researcher**: Gathers company intelligence
   - **Pitch Architect**: Creates custom pitches
   - **Auditor**: Validates and scores leads

3. **FastAPI Backend** (`api/main.py`)
   - RESTful API for lead management
   - Nevermined integration endpoints
   - Protected asset creation

4. **Next.js Frontend** (`frontend/`)
   - Dashboard with lead feed
   - Lead detail modals
   - Unlock mechanism for high-value leads

## 📋 Prerequisites

- Python 3.13+
- Node.js 18+
- OpenAI API key
- Apify API token
- Nevermined API key (optional, for monetization)

## 🛠️ Setup

### 1. Clone Repository

```bash
git clone https://github.com/oabolade/Lead_Sniper_AI.git
cd Lead_Sniper_AI
```

### 2. Backend Setup

```bash
# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY
# - APIFY_API_TOKEN
# - NVM_API_KEY (optional)
```

### 3. Frontend Setup

```bash
cd frontend
npm install

# Set up environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 4. Start Services

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python api/run_server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🎯 Usage

### Quick Start

```bash
# Run the complete workflow
./START_WORKFLOW.sh

# Or add test leads for testing
./add_test_leads.sh
```

### API Endpoints

- `GET /health` - Health check
- `GET /api/leads` - Get all leads
- `POST /api/scrape-and-process` - Scrape and process leads
- `POST /api/process` - Process a single lead
- `POST /api/unlock` - Unlock a protected lead
- `GET /docs` - Interactive API documentation

### Workflow

1. **Scrape Leads**: Use expanded keywords and multiple sources
2. **Process**: Leads go through 4-agent CrewAI pipeline
3. **Score**: Each lead gets a buyability_score (0-100)
4. **Protect**: High-value leads (score >= 80) are protected
5. **Unlock**: Users pay via Nevermined to unlock full details

## 📊 Project Structure

```
lead_sniper_ai/
├── agents/              # CrewAI agent definitions
│   ├── crew_setup.py    # Main crew configuration
│   └── agent_personas.py # Agent personas
├── tools/               # Apify scraper tools
│   └── apify_scraper.py
├── api/                 # FastAPI backend
│   ├── main.py          # Main API server
│   ├── nevermined_middleware.py
│   └── run_server.py
├── frontend/            # Next.js frontend
│   ├── app/
│   ├── components/
│   └── lib/
└── requirements.txt     # Python dependencies
```

## 🔐 Security

- `.env` files are gitignored
- API keys should never be committed
- Use environment variables for all secrets

## 📝 Documentation

- [API Documentation](API_DOCUMENTATION.md)
- [Frontend Setup](FRONTEND_SETUP.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [End-to-End Testing](END_TO_END_TEST.md)

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## 📄 License

MIT License

## 🙏 Acknowledgments

Built for a 24-hour hackathon. Uses:
- [CrewAI](https://github.com/joaomdmoura/crewAI) for agent orchestration
- [Apify](https://apify.com) for web scraping
- [Nevermined](https://nevermined.io) for monetization
- [Next.js](https://nextjs.org) for frontend

## 🚧 Status

✅ Core functionality complete
✅ End-to-end workflow tested
✅ UI implemented
✅ Nevermined integration ready

---

**Built with ❤️ for the hackathon**
