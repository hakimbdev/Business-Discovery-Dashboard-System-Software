"""
Google Search OSINT Module
Uses Google Custom Search API and search operators to discover new business pages
"""

import requests
import time
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from src.core.config_manager import config
from src.core.database import DatabaseHandler
from src.core.lead_scorer import LeadScorer
from src.core.logger import get_logger

logger = get_logger(__name__)


class GoogleScraper:
    """
    Use Google search to discover newly indexed Facebook and LinkedIn pages
    This is often the most effective method for finding new business pages
    """
    
    def __init__(self, db_handler: DatabaseHandler):
        self.db = db_handler
        self.scorer = LeadScorer()
        
        # Load configuration
        self.api_key = config.get_api_key('google', 'api_key')
        self.search_engine_id = config.get_api_key('google', 'search_engine_id')
        self.rate_limit = config.get_rate_limit('google')
        
        # Google Custom Search API endpoint
        self.search_url = "https://www.googleapis.com/customsearch/v1"
        
        logger.info("Google scraper initialized")
    
    def build_search_queries(self) -> List[Dict[str, str]]:
        """
        Build Google search queries (dorks) for discovering business pages
        """
        queries = []
        
        categories = config.get_keywords()
        location_signals = config.get_location_signals()
        detection_settings = config.get_detection_settings()
        
        # Time filter for recent pages
        time_filter = detection_settings.get('google_time_filter', 'qdr:w')
        
        # Major cities to search
        cities = location_signals.get('major_cities', [])[:10]  # Limit to top 10
        
        for category_name, category_data in categories.items():
            keywords = category_data.get('keywords', [])[:3]  # Limit keywords
            
            for keyword in keywords:
                for city in cities[:3]:  # Top 3 cities per keyword
                    # Facebook search query
                    fb_query = f'site:facebook.com/pages {keyword} {city} Nigeria'
                    queries.append({
                        'query': fb_query,
                        'platform': 'Facebook',
                        'category': category_name,
                        'time_filter': time_filter
                    })
                    
                    # LinkedIn search query
                    li_query = f'site:linkedin.com/company {keyword} {city} Nigeria'
                    queries.append({
                        'query': li_query,
                        'platform': 'LinkedIn',
                        'category': category_name,
                        'time_filter': time_filter
                    })
        
        logger.info(f"Built {len(queries)} search queries")
        return queries
    
    def search_google(self, query: str, time_filter: str = None, 
                     num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Execute Google Custom Search API query
        """
        if not self.api_key or not self.search_engine_id:
            logger.warning("Google API credentials not configured")
            return []
        
        results = []
        
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': min(num_results, 10)  # API limit is 10 per request
            }
            
            # Add time filter if specified
            if time_filter:
                params['dateRestrict'] = time_filter
            
            response = requests.get(self.search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract search results
            items = data.get('items', [])
            
            for item in items:
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'display_link': item.get('displayLink', '')
                }
                results.append(result)
            
            logger.info(f"Google search returned {len(results)} results for: {query}")
            
            # Respect rate limits
            self._rate_limit_delay()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.warning("Google API rate limit exceeded")
            else:
                logger.error(f"Google API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error searching Google: {str(e)}")
        
        return results
    
    def discover_new_pages(self) -> List[Dict[str, Any]]:
        """
        Main discovery method using Google search
        """
        discovered = []
        
        # Build search queries
        search_queries = self.build_search_queries()
        
        # Execute searches
        for query_data in search_queries:
            query = query_data['query']
            platform = query_data['platform']
            category = query_data['category']
            time_filter = query_data.get('time_filter')
            
            # Search Google
            results = self.search_google(query, time_filter)
            
            # Process results
            for result in results:
                url = result['url']
                
                # Skip if already in database
                if self.db.business_exists(url):
                    continue
                
                # Extract business data from search result
                business_data = self._extract_from_search_result(
                    result, platform, category
                )
                
                if business_data:
                    # Score the lead
                    scored_data = self.scorer.score_business(business_data)
                    
                    # Check minimum confidence
                    min_score = config.get_detection_settings().get('min_confidence_score', 60)
                    if scored_data['confidence_score'] >= min_score:
                        # Add to database
                        if self.db.add_business(scored_data):
                            discovered.append(scored_data)
                            logger.info(f"New {platform} page discovered via Google: "
                                      f"{scored_data['business_name']}")
            
            # Log search history
            self.db.add_search_history(platform, query, len(results))
        
        return discovered
    
    def _extract_from_search_result(self, result: Dict[str, Any], 
                                    platform: str, category: str) -> Optional[Dict[str, Any]]:
        """
        Extract business data from Google search result
        """
        try:
            business_data = {
                'business_name': self._extract_business_name(result['title'], platform),
                'platform': platform,
                'page_url': result['url'],
                'category': category,
                'location': self._extract_location(result['snippet']),
                'phone': '',
                'email': '',
                'description': result['snippet'],
                'page_created_date': '',
                'metadata': {
                    'discovered_via': 'Google Search',
                    'search_snippet': result['snippet']
                }
            }
            
            return business_data
            
        except Exception as e:
            logger.error(f"Error extracting data from search result: {str(e)}")
            return None
    
    def _extract_business_name(self, title: str, platform: str) -> str:
        """Extract business name from page title"""
        # Remove platform-specific suffixes
        if platform == 'Facebook':
            title = title.replace(' - Facebook', '')
            title = title.replace(' | Facebook', '')
        elif platform == 'LinkedIn':
            title = title.replace(' - LinkedIn', '')
            title = title.replace(' | LinkedIn', '')
        
        return title.strip()
    
    def _extract_location(self, text: str) -> str:
        """Extract location from snippet text"""
        location_signals = config.get_location_signals()
        
        # Check for cities
        for city in location_signals.get('major_cities', []):
            if city.lower() in text.lower():
                return city
        
        # Check for country
        if 'nigeria' in text.lower():
            return 'Nigeria'
        
        return ''
    
    def _rate_limit_delay(self):
        """Add delay between requests to respect rate limits"""
        delay = random.uniform(
            self.rate_limit['delay_min'],
            self.rate_limit['delay_max']
        )
        time.sleep(delay)

