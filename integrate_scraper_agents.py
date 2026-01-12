"""
Integration: Apify Scraper + CrewAI Agents Workflow
Scrapes leads and processes them through the 4-agent crew pipeline
"""

import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.apify_scraper import ApifyLeadScraper
from agents.crew_setup import process_lead

load_dotenv()


def scrape_and_process_leads(
    keywords: List[str],
    reddit_subreddits: List[str] = None,
    linkedin_location: str = None,
    max_per_source: int = 10,
    process_limit: int = 3
) -> Dict[str, Any]:
    """
    Complete pipeline: Scrape leads from Apify and process through CrewAI agents
    
    Args:
        keywords: Keywords to search for (e.g., ["hiring", "looking for", "need"])
        reddit_subreddits: Optional list of subreddits to target
        linkedin_location: Optional location filter for LinkedIn
        max_per_source: Maximum leads to scrape per source
        process_limit: Maximum number of leads to process through agents (to control costs)
        
    Returns:
        Dictionary with scraping results and processed leads
    """
    print("=" * 60)
    print("Lead Sniper AI - Scrape & Process Pipeline")
    print("=" * 60)
    
    # Step 1: Scrape leads
    print(f"\n📡 Step 1: Scraping leads with keywords: {keywords}")
    scraper = ApifyLeadScraper()
    
    try:
        scrape_results = scraper.scrape_all(
            keywords=keywords,
            reddit_subreddits=reddit_subreddits,
            linkedin_location=linkedin_location,
            max_per_source=max_per_source
        )
        
        print(f"✅ Scraped {scrape_results['total']} total leads")
        print(f"   - Reddit: {len(scrape_results['reddit'])} leads")
        print(f"   - LinkedIn: {len(scrape_results['linkedin'])} leads")
        
        # Step 2: Process leads through CrewAI agents
        all_leads = scrape_results['reddit'] + scrape_results['linkedin']
        processed_leads = []
        failed_leads = []
        
        # Limit processing to control API costs
        leads_to_process = all_leads[:process_limit]
        
        print(f"\n🤖 Step 2: Processing {len(leads_to_process)} leads through CrewAI agents...")
        print("   (Processing through: Signal Scout → Researcher → Pitch Architect → Auditor)")
        
        for i, lead in enumerate(leads_to_process, 1):
            print(f"\n   Processing lead {i}/{len(leads_to_process)}: {lead.get('title', lead.get('name', 'Unknown'))[:50]}...")
            
            try:
                result = process_lead(lead)
                
                if result.get('success'):
                    processed_leads.append(result)
                    print(f"   ✅ Lead {i} processed successfully")
                else:
                    error_msg = result.get('error', 'Unknown error')
                    failed_leads.append({
                        'lead': lead,
                        'error': error_msg,
                        'result': result  # Include full result for debugging
                    })
                    print(f"   ❌ Lead {i} failed: {error_msg}")
                    # Print more details for debugging
                    if 'processed_result' in result:
                        print(f"      Result type: {type(result.get('processed_result'))}")
                    
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                failed_leads.append({
                    'lead': lead,
                    'error': str(e),
                    'traceback': error_details
                })
                print(f"   ❌ Lead {i} exception: {str(e)}")
                print(f"      Traceback: {error_details[:200]}...")
        
        # Step 3: Summary
        print("\n" + "=" * 60)
        print("Pipeline Summary")
        print("=" * 60)
        print(f"Total leads scraped: {scrape_results['total']}")
        print(f"Leads processed: {len(processed_leads)}")
        print(f"Leads failed: {len(failed_leads)}")
        
        return {
            "scrape_results": scrape_results,
            "processed_leads": processed_leads,
            "failed_leads": failed_leads,
            "summary": {
                "total_scraped": scrape_results['total'],
                "total_processed": len(processed_leads),
                "total_failed": len(failed_leads),
                "success_rate": len(processed_leads) / len(leads_to_process) * 100 if leads_to_process else 0
            }
        }
        
    except Exception as e:
        print(f"\n❌ Pipeline error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "scrape_results": None,
            "processed_leads": [],
            "failed_leads": []
        }


def process_single_lead_from_scraper(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single lead that was scraped from Apify
    
    Args:
        lead_data: Lead data from Apify scraper
        
    Returns:
        Processed lead result
    """
    print(f"\n🤖 Processing lead: {lead_data.get('title', lead_data.get('name', 'Unknown'))}")
    return process_lead(lead_data)


if __name__ == "__main__":
    # Example usage
    print("Lead Sniper AI - Scraper + Agents Integration")
    print("\nExample: Scraping and processing leads...")
    
    keywords = ["hiring", "looking for", "need", "seeking"]
    
    # Run the pipeline
    results = scrape_and_process_leads(
        keywords=keywords,
        max_per_source=5,  # Small number for testing
        process_limit=2     # Process only 2 leads to save API costs
    )
    
    if results.get("processed_leads"):
        print("\n✅ Pipeline completed successfully!")
        print(f"\nProcessed {len(results['processed_leads'])} leads")
    else:
        print("\n⚠️  No leads were processed successfully")
