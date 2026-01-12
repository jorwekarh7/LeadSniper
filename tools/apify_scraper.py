"""
Apify Lead Scraper for Reddit and LinkedIn
Scrapes buying intent signals from social platforms
"""

import os
from typing import List, Dict, Any, Optional
from apify_client import ApifyClient


class ApifyLeadScraper:
    """Scrapes leads from Reddit and LinkedIn using Apify actors"""
    
    def __init__(self, api_token: str = None):
        """Initialize Apify client"""
        self.api_token = api_token or os.getenv("APIFY_API_TOKEN")
        if not self.api_token:
            raise ValueError("APIFY_API_TOKEN not found in environment variables")
        self.client = ApifyClient(self.api_token)
    
    def scrape_reddit(self, 
                     keywords: List[str],
                     subreddits: List[str] = None,
                     max_posts: int = 50) -> List[Dict[str, Any]]:
        """
        Scrape Reddit for buying intent signals
        
        Uses: benthepythondev/reddit-scraper (affordable, good success rate)
        
        Args:
            keywords: List of keywords to search for (e.g., ["hiring", "looking for", "need"])
            subreddits: Optional list of subreddits to target
            max_posts: Maximum number of posts to scrape
            
        Returns:
            List of lead dictionaries with buying intent signals
        """
        # Expanded subreddit list - more sources for high-intent leads
        default_subreddits = [
            "startups", "entrepreneur", "SaaS", "smallbusiness", 
            "entrepreneurship", "startup", "business", "marketing",
            "sales", "productivity", "webdev", "programming",
            "technology", "software", "tech", "consulting"
        ]
        subreddits = subreddits or default_subreddits
        
        all_leads = []
        
        # Search in more subreddits (increased from 3 to 8)
        for subreddit in subreddits[:8]:
            try:
                # Use more keywords in search (increased from 3 to 5)
                search_query = " OR ".join(keywords[:5])
                
                run_input = {
                    "mode": "search",
                    "searchQuery": search_query,
                    "searchSubreddit": subreddit,
                    "sort": "relevance",
                    "maxPosts": min(max_posts, 30),  # Increased from 20 to 30 per subreddit
                    "outputFormat": "text",
                    "includeComments": False,  # Faster, cheaper
                }
                
                print(f"  Searching r/{subreddit} for: {search_query}")
                run = self.client.actor("benthepythondev/reddit-scraper").call(run_input=run_input)
                
                # Extract leads from dataset
                dataset_id = run.get("defaultDatasetId")
                if dataset_id:
                    for item in self.client.dataset(dataset_id).iterate_items():
                        # Check if post content matches buying intent keywords
                        title = item.get("title", "")
                        text = item.get("text", "") or item.get("body", "") or ""
                        content = f"{title} {text}".lower()
                        
                        # Expanded intent keywords - more signals to catch
                        intent_keywords = [
                            "need", "looking for", "hiring", "seeking", "want", "searching", 
                            "recommend", "suggest", "best", "alternatives", "replace", "switching",
                            "evaluate", "comparing", "deciding", "choose", "select", "purchase",
                            "buy", "implement", "integrate", "migrate", "upgrade", "frustrated",
                            "problem", "issue", "struggling", "challenge", "pain", "solution",
                            "help", "advice", "opinion", "experience", "review", "trial"
                        ]
                        if any(keyword in content for keyword in intent_keywords):
                            lead = {
                                "source": "reddit",
                                "platform": "reddit",
                                "title": title,
                                "content": text or title,
                                "author": item.get("author", ""),
                                "subreddit": subreddit,
                                "url": item.get("url", ""),
                                "upvotes": item.get("upvotes", item.get("score", 0)),
                                "comments": item.get("numComments", item.get("comments", 0)),
                                "posted_at": item.get("createdAt", item.get("created", "")),
                                "raw_data": item
                            }
                            all_leads.append(lead)
                            
                            if len(all_leads) >= max_posts:
                                break
                
            except Exception as e:
                print(f"  ⚠️  Error scraping r/{subreddit}: {e}")
                continue
        
        print(f"  ✅ Found {len(all_leads)} Reddit leads with buying intent")
        return all_leads[:max_posts]
    
    def scrape_linkedin(self,
                       keywords: List[str],
                       location: str = None,
                       max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Scrape LinkedIn for buying intent signals
        
        Uses: freshdata/linkedin-job-scraper (for job postings indicating hiring/tech stack changes)
        
        Args:
            keywords: List of keywords to search for
            location: Optional location filter
            max_results: Maximum number of results
            
        Returns:
            List of lead dictionaries with buying intent signals
        """
        try:
            # Use more keywords (increased from 3 to 5)
            search_keywords = " ".join(keywords[:5])
            
            # Try multiple date ranges to get more results
            all_leads = []
            date_ranges = ["Past 24 hours", "Past week", "Past month"]  # Multiple timeframes
            
            for date_range in date_ranges:
                if len(all_leads) >= max_results:
                    break
                    
                run_input = {
                    "keywords": search_keywords,
                    "geo_code": 92000000,  # United States (default)
                    "date_posted": date_range,
                    "sort_by": "Most recent",
                    "start": 0
                }
                
                print(f"  Searching LinkedIn jobs ({date_range}) for: {search_keywords}")
                try:
                    run = self.client.actor("freshdata/linkedin-job-scraper").call(run_input=run_input)
                    
                    dataset_id = run.get("defaultDatasetId")
                    
                    if dataset_id:
                        for item in self.client.dataset(dataset_id).iterate_items():
                            # Job postings indicate hiring/tech stack changes (buying intent)
                            lead = {
                                "source": "linkedin",
                                "platform": "linkedin",
                                "title": item.get("title", item.get("jobTitle", "")),
                                "content": item.get("description", item.get("jobDescription", "")),
                                "company": item.get("companyName", item.get("company", "")),
                                "location": item.get("location", location or ""),
                                "url": item.get("jobUrl", item.get("url", "")),
                                "posted_at": item.get("postedDate", item.get("datePosted", "")),
                                "raw_data": item
                            }
                            all_leads.append(lead)
                            
                            if len(all_leads) >= max_results:
                                break
                except Exception as e:
                    print(f"  ⚠️  Error searching {date_range}: {e}")
                    continue
            
            print(f"  ✅ Found {len(all_leads)} LinkedIn leads")
            return all_leads[:max_results]
            
        except Exception as e:
            print(f"  ⚠️  LinkedIn scraping error: {e}")
            # Fallback: return empty list
            return []
    
    def scrape_all(self, 
                  keywords: List[str],
                  reddit_subreddits: List[str] = None,
                  linkedin_location: str = None,
                  max_per_source: int = 50) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scrape both Reddit and LinkedIn
        
        Returns:
            Dictionary with 'reddit' and 'linkedin' keys containing lists of leads
        """
        reddit_leads = self.scrape_reddit(
            keywords=keywords,
            subreddits=reddit_subreddits,
            max_posts=max_per_source
        )
        
        linkedin_leads = self.scrape_linkedin(
            keywords=keywords,
            location=linkedin_location,
            max_results=max_per_source
        )
        
        return {
            "reddit": reddit_leads,
            "linkedin": linkedin_leads,
            "total": len(reddit_leads) + len(linkedin_leads)
        }


if __name__ == "__main__":
    # Example usage
    scraper = ApifyLeadScraper()
    keywords = ["hiring", "looking for", "need", "seeking"]
    results = scraper.scrape_all(keywords=keywords, max_per_source=10)
    print(f"Found {results['total']} total leads")
