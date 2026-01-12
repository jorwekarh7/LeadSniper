"""
FastAPI Backend for Lead Sniper AI
Integrates Apify Scraper with CrewAI Agents Workflow
"""

import os
import sys
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.apify_scraper import ApifyLeadScraper
from agents.crew_setup import process_lead
from integrate_scraper_agents import scrape_and_process_leads
from api.nevermined_middleware import nevermined_middleware

load_dotenv()

app = FastAPI(
    title="Lead Sniper AI API",
    description="B2B SaaS lead generation with AI processing - Scrape leads from Reddit/LinkedIn and process through CrewAI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for processed leads (use database in production)
processed_leads_store: Dict[str, Dict[str, Any]] = {}


# Pydantic Models
class ScrapeRequest(BaseModel):
    keywords: List[str] = Field(..., description="Keywords to search for (e.g., ['hiring', 'looking for', 'need'])")
    reddit_subreddits: Optional[List[str]] = Field(None, description="Optional list of subreddits to target")
    linkedin_location: Optional[str] = Field(None, description="Optional location filter for LinkedIn")
    max_per_source: int = Field(10, description="Maximum number of leads per source", ge=1, le=100)


class ProcessLeadRequest(BaseModel):
    lead_data: Dict[str, Any] = Field(..., description="Raw lead data from scraper")


class ScrapeAndProcessRequest(BaseModel):
    keywords: List[str] = Field(..., description="Keywords to search for")
    reddit_subreddits: Optional[List[str]] = None
    linkedin_location: Optional[str] = None
    max_per_source: int = Field(10, ge=1, le=100)
    process_limit: int = Field(3, ge=1, le=10, description="Maximum leads to process through agents")


class LeadResponse(BaseModel):
    lead_id: str
    status: str
    source: str
    title: str
    processed_at: Optional[str] = None
    buyability_score: Optional[float] = None
    is_approved: Optional[bool] = None


class UnlockRequest(BaseModel):
    lead_id: str
    payment_token: Optional[str] = None
    payment_method: str = "nevermined"


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Lead Sniper AI API",
        "version": "1.0.0",
            "endpoints": {
            "health": "/health",
            "scrape": "/api/scrape",
            "process": "/api/process",
            "scrape_and_process": "/api/scrape-and-process",
            "leads": "/api/leads",
            "lead_by_id": "/api/leads/{lead_id}",
            "unlock": "/api/unlock",
            "payment_status": "/api/leads/{lead_id}/payment-status",
            "protected_assets": "/api/protected-assets",
            "stats": "/api/stats"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "apify": "ready" if os.getenv("APIFY_API_TOKEN") else "not_configured",
            "crewai": "ready" if os.getenv("OPENAI_API_KEY") else "not_configured",
            "nevermined": "ready" if os.getenv("NVM_API_KEY") or os.getenv("NEVERMINED_API_KEY") else "not_configured",
            "api": "running"
        }
    }


@app.post("/api/scrape")
async def scrape_leads(request: ScrapeRequest):
    """
    Scrape leads from Reddit and LinkedIn using Apify
    
    Returns raw leads without processing through agents
    """
    try:
        scraper = ApifyLeadScraper()
        results = scraper.scrape_all(
            keywords=request.keywords,
            reddit_subreddits=request.reddit_subreddits,
            linkedin_location=request.linkedin_location,
            max_per_source=request.max_per_source
        )
        
        return {
            "status": "success",
            "total_leads": results["total"],
            "reddit_leads": len(results["reddit"]),
            "linkedin_leads": len(results["linkedin"]),
            "leads": results["reddit"] + results["linkedin"],
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@app.post("/api/process")
async def process_single_lead(request: ProcessLeadRequest):
    """
    Process a single lead through the CrewAI agents pipeline
    
    Takes raw lead data and processes it through:
    1. Intent Data Analyst (Signal Scout)
    2. Business Intelligence Analyst (Researcher)
    3. Strategic Growth Copywriter (Pitch Architect)
    4. Quality Assurance & MCP Bridge (Auditor)
    
    If buyability score >= 80, creates a Protected Asset for Nevermined monetization.
    """
    try:
        result = process_lead(request.lead_data)
        
        if result.get("success"):
            # Generate lead ID and store
            lead_id = str(uuid.uuid4())
            
            # Extract buyability score from processed result (if available)
            processed_result = result.get("processed_result", {})
            buyability_score = None
            
            # Try to extract buyability score from auditor's output
            if isinstance(processed_result, dict):
                # Check various possible locations for the score
                audit_result = processed_result.get("audit") or processed_result.get("validation") or {}
                buyability_score = audit_result.get("buyability_score") or audit_result.get("quality_score")
                
                # If not found, try parsing from raw string (CrewAI output)
                if not buyability_score and isinstance(processed_result.get("raw"), str):
                    import json as json_lib
                    try:
                        raw_data = json_lib.loads(processed_result.get("raw", "{}"))
                        buyability_score = raw_data.get("buyability_score")
                    except:
                        # Try to extract from string if JSON parsing fails
                        raw_str = processed_result.get("raw", "")
                        if '"buyability_score":' in raw_str:
                            try:
                                # Extract buyability_score value from string
                                import re
                                match = re.search(r'"buyability_score":\s*(\d+(?:\.\d+)?)', raw_str)
                                if match:
                                    buyability_score = float(match.group(1))
                            except:
                                pass
            
            processed_lead_data = {
                "lead_id": lead_id,
                "original_lead": result["original_lead"],
                "processed_result": processed_result,
                "status": "processed",
                "processed_at": datetime.now().isoformat(),
                "buyability_score": buyability_score
            }
            
            processed_leads_store[lead_id] = processed_lead_data
            
            # If buyability score >= 80, create Protected Asset and MCP notification
            mcp_notification = None
            protected_asset = None
            
            if buyability_score and buyability_score >= 80:
                try:
                    # Create Protected Asset
                    protected_asset = await nevermined_middleware.create_protected_asset(
                        processed_lead_data,
                        buyability_score
                    )
                    
                    # Generate MCP notification
                    mcp_notification = await nevermined_middleware.generate_mcp_notification(
                        lead_id,
                        buyability_score
                    )
                except Exception as e:
                    print(f"Warning: Nevermined integration error: {e}")
            
            return {
                "status": "success",
                "lead_id": lead_id,
                "result": result,
                "buyability_score": buyability_score,
                "is_high_value": buyability_score >= 80 if buyability_score else False,
                "protected_asset": protected_asset,
                "mcp_notification": mcp_notification,
                "message": "Lead processed successfully"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Processing failed: {result.get('error', 'Unknown error')}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.post("/api/scrape-and-process")
async def scrape_and_process(request: ScrapeAndProcessRequest, background_tasks: BackgroundTasks):
    """
    Complete pipeline: Scrape leads and process them through CrewAI agents
    
    This endpoint:
    1. Scrapes leads from Reddit and LinkedIn
    2. Processes top leads through the 4-agent crew
    3. Returns both raw and processed leads
    """
    try:
        results = scrape_and_process_leads(
            keywords=request.keywords,
            reddit_subreddits=request.reddit_subreddits,
            linkedin_location=request.linkedin_location,
            max_per_source=request.max_per_source,
            process_limit=request.process_limit
        )
        
        # Store processed leads
        for processed in results.get("processed_leads", []):
            lead_id = str(uuid.uuid4())
            processed_leads_store[lead_id] = {
                "lead_id": lead_id,
                **processed,
                "processed_at": datetime.now().isoformat()
            }
        
        # Extract error details from failed leads for better debugging
        failed_errors = []
        if results.get("failed_leads"):
            for failed in results.get("failed_leads", [])[:3]:  # Show first 3 errors
                failed_errors.append({
                    "lead_title": failed.get("lead", {}).get("title", failed.get("lead", {}).get("name", "Unknown"))[:50],
                    "error": failed.get("error", "Unknown error")
                })
        
        return {
            "status": "success",
            "summary": results.get("summary", {}),
            "scrape_results": {
                "total": results.get("scrape_results", {}).get("total", 0),
                "reddit": len(results.get("scrape_results", {}).get("reddit", [])),
                "linkedin": len(results.get("scrape_results", {}).get("linkedin", []))
            },
            "processed_leads_count": len(results.get("processed_leads", [])),
            "failed_leads_count": len(results.get("failed_leads", [])),
            "processed_leads": results.get("processed_leads", []),
            "failed_leads_errors": failed_errors,  # Include error details
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


@app.get("/api/leads")
async def get_all_leads(limit: int = 10, offset: int = 0):
    """
    Get all processed leads
    
    Returns a list of processed leads with pagination
    """
    leads_list = list(processed_leads_store.values())
    
    # Simple pagination
    total = len(leads_list)
    paginated_leads = leads_list[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "leads": paginated_leads
    }


@app.get("/api/leads/{lead_id}")
async def get_lead_by_id(
    lead_id: str,
    access_token: Optional[str] = None
):
    """
    Get a specific processed lead by ID
    
    If the lead has buyability_score >= 80, it's protected and requires payment.
    Pass access_token if you've already paid for the lead.
    """
    if lead_id not in processed_leads_store:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead_data = processed_leads_store[lead_id]
    buyability_score = lead_data.get("buyability_score")
    
    # Check if lead is protected (high-value lead)
    if buyability_score and buyability_score >= 80:
        # Verify payment
        payment_status = await nevermined_middleware.verify_payment(lead_id, access_token)
        
        if not payment_status["is_paid"]:
            # Return locked version with payment URL
            payment_url = await nevermined_middleware.get_payment_url(lead_id)
            return {
                "lead_id": lead_id,
                "status": "locked",
                "buyability_score": buyability_score,
                "is_high_value": True,
                "payment_required": True,
                "payment_url": payment_url,
                "preview": {
                    "source": lead_data.get("original_lead", {}).get("source"),
                    "title": lead_data.get("original_lead", {}).get("title", "N/A")[:100],
                    "buyability_score": buyability_score
                },
                "message": "This is a high-value lead. Payment required to unlock full details."
            }
    
    # Return full lead data (either not protected or payment verified)
    return lead_data


@app.delete("/api/leads/{lead_id}")
async def delete_lead(lead_id: str):
    """
    Delete a processed lead
    """
    if lead_id not in processed_leads_store:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    del processed_leads_store[lead_id]
    return {"status": "success", "message": f"Lead {lead_id} deleted"}


@app.post("/api/unlock")
async def unlock_lead(request: UnlockRequest):
    """
    Unlock a protected lead by processing payment through Nevermined
    
    Returns an access token that can be used to access the full lead data.
    """
    try:
        print(f"🔓 Unlock request received for lead_id: {request.lead_id}")
        print(f"   Payment method: {request.payment_method}")
        
        if request.lead_id not in processed_leads_store:
            print(f"   ❌ Lead {request.lead_id} not found in store")
            print(f"   Available leads: {list(processed_leads_store.keys())[:5]}")
            raise HTTPException(status_code=404, detail=f"Lead {request.lead_id} not found")
        
        lead_data = processed_leads_store[request.lead_id]
        buyability_score = lead_data.get("buyability_score")
        
        print(f"   Lead found, buyability_score: {buyability_score}")
        
        # Check if lead is actually protected
        if not buyability_score or buyability_score < 80:
            print(f"   ⚠️  Lead not protected (score: {buyability_score})")
            return {
                "status": "success",
                "message": "Lead is not protected, no payment required",
                "lead_id": request.lead_id,
                "access_token": None,
                "unlocked": True
            }
        
        print(f"   ✅ Lead is protected, processing payment...")
        
        # Process payment
        payment_result = await nevermined_middleware.process_payment(
            lead_id=request.lead_id,
            payment_method=request.payment_method,
            payment_token=request.payment_token
        )
        
        print(f"   Payment result: success={payment_result.success}, error={payment_result.error}")
        
        if payment_result.success:
            print(f"   ✅ Payment successful, returning access token")
            return {
                "status": "success",
                "lead_id": request.lead_id,
                "unlocked": True,
                "access_token": payment_result.access_token,
                "payment_id": payment_result.payment_id,
                "message": "Lead unlocked successfully"
            }
        else:
            print(f"   ❌ Payment failed: {payment_result.error}")
            raise HTTPException(
                status_code=402,
                detail=f"Payment failed: {payment_result.error}"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"   ❌ Unlock error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unlock error: {str(e)}")


@app.get("/api/leads/{lead_id}/payment-status")
async def get_payment_status(lead_id: str, access_token: Optional[str] = None):
    """
    Check payment status for a lead
    """
    if lead_id not in processed_leads_store:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    payment_status = await nevermined_middleware.verify_payment(lead_id, access_token)
    payment_url = await nevermined_middleware.get_payment_url(lead_id)
    
    return {
        "lead_id": lead_id,
        "payment_status": payment_status,
        "payment_url": payment_url,
        "is_paid": payment_status["is_paid"]
    }


@app.get("/api/protected-assets")
async def get_protected_assets(limit: int = 10, offset: int = 0):
    """
    Get list of protected assets (high-value leads ready for monetization)
    """
    # Filter leads with buyability_score >= 80
    protected_leads = [
        lead for lead in processed_leads_store.values()
        if lead.get("buyability_score") and lead.get("buyability_score") >= 80
    ]
    
    total = len(protected_leads)
    paginated = protected_leads[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "protected_assets": paginated
    }


@app.post("/api/test/add-leads")
async def add_test_leads():
    """
    Add test leads with high buyability scores for testing Nevermined unlock
    This endpoint adds pre-processed leads directly to the store
    """
    import json as json_lib
    
    test_leads_data = [
        {
            "original_lead": {
                "source": "reddit",
                "platform": "reddit",
                "title": "Looking for CRM solution - our current one is terrible",
                "content": "We're a 50-person SaaS company and our current CRM is causing major issues. We're actively looking for alternatives that integrate with Slack and have better reporting. Budget is not an issue - we need something that works.",
                "author": "startup_founder_2024",
                "subreddit": "startups",
                "url": "https://reddit.com/r/startups/test1",
                "upvotes": 45,
                "comments": 12
            },
            "processed_result": {
                "raw": json_lib.dumps({
                    "buyability_score": 85,
                    "protected_asset": {
                        "lead_data": {
                            "company_name": "TechStart Inc",
                            "confidence_score": 9,
                            "value_proposition": "B2B SaaS platform for project management",
                            "recent_news": ["Raised $5M Series A in Q4 2024", "Expanding team from 30 to 50 employees"],
                            "likely_rejection_reason": "Current tool satisfaction",
                            "hook": "Congratulations on your Series A! With your team doubling, you'll need a CRM that scales.",
                            "pitch": "Hi! I saw you're looking for a CRM solution. Given your recent Series A and team expansion, you need a platform that grows with you. Our CRM integrates seamlessly with Slack and provides real-time analytics that your current solution lacks. Would you be open to a 15-minute demo to see how we can help you scale more efficiently?",
                            "trigger_text": "Looking for CRM solution - our current one is terrible"
                        }
                    }
                }),
                "tasks_output": [
                    {"agent": "Intent Data Analyst", "raw": 'Trigger Text: "Looking for CRM solution - our current one is terrible"', "summary": "High intent signal detected"},
                    {"agent": "Strategic Growth Copywriter", "raw": 'Pitch: "Hi! I saw you\'re looking for a CRM solution..."', "summary": "Custom pitch generated"}
                ]
            },
            "buyability_score": 85
        },
        {
            "original_lead": {
                "source": "linkedin",
                "platform": "linkedin",
                "title": "Hiring: Senior Marketing Automation Specialist",
                "content": "We're hiring a Senior Marketing Automation Specialist to help us migrate from Marketo to a more modern platform. Experience with HubSpot, Salesforce Marketing Cloud, or similar required. This is urgent - we're evaluating platforms now.",
                "company": "GrowthCo",
                "location": "San Francisco, CA",
                "url": "https://linkedin.com/jobs/test2"
            },
            "processed_result": {
                "raw": json_lib.dumps({
                    "buyability_score": 88,
                    "protected_asset": {
                        "lead_data": {
                            "company_name": "GrowthCo",
                            "confidence_score": 9,
                            "value_proposition": "B2B marketing automation platform",
                            "recent_news": ["Migrating from Marketo - urgent need", "Hiring for marketing automation role"],
                            "likely_rejection_reason": "Budget constraints",
                            "hook": "I noticed you're migrating from Marketo - that's a big move!",
                            "pitch": "Hi GrowthCo team! I saw you're hiring a Marketing Automation Specialist and migrating from Marketo. We specialize in helping companies transition to modern marketing platforms with zero downtime. Our platform offers better analytics and integrates with your existing stack. Would you be interested in a quick call to discuss how we can make your migration seamless?",
                            "trigger_text": "Migrating from Marketo to a more modern platform"
                        }
                    }
                }),
                "tasks_output": [
                    {"agent": "Intent Data Analyst", "raw": 'Trigger Text: "Migrating from Marketo to a more modern platform"', "summary": "Very high intent - active migration"},
                    {"agent": "Strategic Growth Copywriter", "raw": 'Pitch: "Hi GrowthCo team! I saw you\'re hiring..."', "summary": "Custom pitch generated"}
                ]
            },
            "buyability_score": 88
        },
        {
            "original_lead": {
                "source": "reddit",
                "platform": "reddit",
                "title": "Need project management tool - current one is too expensive",
                "content": "We're a 20-person agency and paying $500/month for our current PM tool. It's way too expensive for what we get. Looking for alternatives that have good task management, time tracking, and client portals. Price is a factor but features matter more.",
                "author": "agency_owner",
                "subreddit": "smallbusiness",
                "url": "https://reddit.com/r/smallbusiness/test3",
                "upvotes": 32,
                "comments": 8
            },
            "processed_result": {
                "raw": json_lib.dumps({
                    "buyability_score": 82,
                    "protected_asset": {
                        "lead_data": {
                            "company_name": "Creative Agency LLC",
                            "confidence_score": 8,
                            "value_proposition": "Creative agency specializing in digital marketing",
                            "recent_news": ["Growing from 15 to 20 employees", "Expanding client base"],
                            "likely_rejection_reason": "Price sensitivity",
                            "hook": "I see you're growing your team - that's exciting!",
                            "pitch": "Hi! I noticed you're looking for a more affordable project management solution. With your team growing, you need a tool that scales without breaking the bank. Our platform offers all the features you mentioned at a fraction of your current cost. We've helped many agencies like yours reduce costs while improving productivity. Would you be open to a quick demo?",
                            "trigger_text": "Need project management tool - current one is too expensive"
                        }
                    }
                }),
                "tasks_output": [
                    {"agent": "Intent Data Analyst", "raw": 'Trigger Text: "Need project management tool - current one is too expensive"', "summary": "High intent - price-driven but active search"},
                    {"agent": "Strategic Growth Copywriter", "raw": 'Pitch: "Hi! I noticed you\'re looking for..."', "summary": "Custom pitch generated"}
                ]
            },
            "buyability_score": 82
        }
    ]
    
    added_leads = []
    
    for lead_data in test_leads_data:
        lead_id = str(uuid.uuid4())
        full_lead = {
            "lead_id": lead_id,
            **lead_data,
            "status": "processed",
            "processed_at": datetime.now().isoformat()
        }
        processed_leads_store[lead_id] = full_lead
        added_leads.append({
            "lead_id": lead_id,
            "title": lead_data["original_lead"]["title"],
            "buyability_score": lead_data["buyability_score"]
        })
    
    return {
        "status": "success",
        "message": f"Added {len(added_leads)} test leads",
        "leads": added_leads,
        "total_leads": len(processed_leads_store)
    }


@app.get("/api/stats")
async def get_stats():
    """
    Get statistics about processed leads
    """
    total_leads = len(processed_leads_store)
    successful = sum(1 for lead in processed_leads_store.values() if lead.get("status") == "processed")
    failed = total_leads - successful
    
    return {
        "total_leads": total_leads,
        "successful": successful,
        "failed": failed,
        "success_rate": (successful / total_leads * 100) if total_leads > 0 else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000))
    )
