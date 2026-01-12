# CrewAI Agents System - Lead Sniper AI

## ✅ System Overview

The Lead Sniper AI uses a 4-agent CrewAI system to process leads from scraping to personalized pitch creation.

## 🤖 The 4 Agents

### 1. Signal Scout
**Role**: Identifies buying intent signals  
**Goal**: Extract buying intent signals from raw lead data  
**Capabilities**:
- Recognizes trigger events (hiring, expansion, tech changes)
- Identifies pain points and urgent needs
- Detects decision-maker signals
- Spots urgency indicators
- Finds context clues indicating readiness to buy

**Output**: Structured JSON with signals, trigger events, urgency level, pain points, and confidence score

### 2. Lead Researcher
**Role**: Enriches lead data with company information  
**Goal**: Research and enrich lead data with comprehensive context  
**Capabilities**:
- Company research (size, industry, funding, growth)
- Tech stack analysis
- Recent news and events discovery
- Individual background research (for LinkedIn leads)
- Personalization hook identification

**Output**: Enriched lead data with company info, tech stack, recent news, and personalization hooks

### 3. Pitch Architect
**Role**: Creates hyper-personalized pitches  
**Goal**: Create video scripts and email pitches that reference specific trigger events  
**Capabilities**:
- Creates 2-3 minute video scripts
- Writes personalized email pitches
- References specific details (never generic)
- Balances professionalism with authenticity
- Includes relevant social proof

**Output**: Video script (2-3 min) and email pitch, both hyper-personalized

### 4. Lead Auditor
**Role**: Validates lead quality  
**Goal**: Ensure only high-quality leads proceed  
**Capabilities**:
- Validates data completeness
- Checks buying intent strength
- Verifies personalization quality
- Uses Rilo/pycalib for scoring
- Enforces quality thresholds (>= 60/100)

**Output**: Validation report with quality score, approval status, issues, and recommendations

## 🔄 Processing Flow

```
Raw Lead Data
    ↓
[Signal Scout] → Identifies buying intent signals
    ↓
[Researcher] → Enriches with company/individual context
    ↓
[Pitch Architect] → Creates personalized video script + email
    ↓
[Auditor] → Validates quality and approves/rejects
    ↓
Processed Lead Package (ready for sales team)
```

## 📁 File Structure

```
agents/
├── __init__.py
├── crew_setup.py          # Main crew configuration and processing
└── agent_personas.py      # Detailed personas and prompts (customizable)
```

## 🚀 Usage

### Basic Usage

```python
from agents.crew_setup import process_lead

lead_data = {
    "source": "reddit",
    "title": "Looking for CRM solution",
    "content": "We need a CRM that integrates with Slack...",
    "url": "https://reddit.com/...",
    # ... other fields
}

result = process_lead(lead_data)
```

### Custom Crew Setup

```python
from agents.crew_setup import create_lead_processing_crew

crew = create_lead_processing_crew()
result = crew.kickoff(inputs={"lead_data": formatted_lead_string})
```

### Individual Agents

```python
from agents.crew_setup import (
    create_signal_scout_agent,
    create_researcher_agent,
    create_pitch_architect_agent,
    create_auditor_agent
)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
scout = create_signal_scout_agent(llm)
# ... use individual agents
```

## 🧪 Testing

Run the test suite:

```bash
source venv/bin/activate
python test_crewai_agents.py
```

This tests:
- ✅ Crew initialization
- ✅ Validation tool
- ✅ Individual agent creation
- ✅ Lead processing function

## 🔧 Configuration

### Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key  # Required for CrewAI agents
```

### Customizing Agents

Edit `agents/agent_personas.py` to customize:
- Agent personas and backstories
- Task prompts
- Validation criteria

### LLM Settings

In `agents/crew_setup.py`, you can modify:
- Model name (default: "gpt-4")
- Temperature (default: 0.7)
- Other LLM parameters

## 📊 Validation Tool

The `LeadValidationTool` uses:
- **Kalibr**: For observability and tracking
- **pycalib**: For calibrated scoring

Validation checks:
- Required fields presence (20 points)
- Content quality/length (30 points)
- Buying intent keywords (30 points)
- Contact/company info (20 points)

Minimum quality score: **60/100** to pass

## 🎯 Integration Points

### With Apify Scraper

```python
from tools.apify_scraper import ApifyLeadScraper
from agents.crew_setup import process_lead

scraper = ApifyLeadScraper()
leads = scraper.scrape_all(keywords=["hiring", "looking for"])

for lead in leads["reddit"] + leads["linkedin"]:
    processed = process_lead(lead)
    if processed["success"]:
        print(f"✅ Processed: {lead.get('title')}")
```

### With FastAPI Backend

The agents can be integrated into the FastAPI backend (`api/main.py`) to process leads via API endpoints.

## 📝 Output Format

Processed lead includes:
```python
{
    "original_lead": {...},           # Raw lead data
    "processed_result": {
        "signals": {...},             # From Signal Scout
        "research": {...},            # From Researcher
        "pitch": {
            "video_script": "...",    # From Pitch Architect
            "email": "..."            # From Pitch Architect
        },
        "validation": {...}           # From Auditor
    },
    "status": "processed",
    "success": True
}
```

## 🔍 Monitoring

Kalibr automatically instruments:
- ✅ OpenAI SDK calls
- ✅ Agent execution tracking
- ✅ Performance metrics

Check `/tmp/kalibr_otel_spans.jsonl` for observability data.

## 🎉 Status

**All systems operational!** The 4-agent crew is ready to process leads.
