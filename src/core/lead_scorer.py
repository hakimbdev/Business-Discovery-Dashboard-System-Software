"""
Lead Scoring Engine
Assigns confidence scores and priority levels to discovered businesses
"""

import re
from typing import Dict, Any, List
from src.core.config_manager import config
from src.core.logger import get_logger

logger = get_logger(__name__)


class LeadScorer:
    """Score and prioritize discovered business leads"""
    
    def __init__(self):
        self.location_signals = config.get_location_signals()
        self.categories = config.get_keywords()
    
    def score_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate confidence score and priority for a business
        Returns updated business_data with score and priority
        """
        score = 0
        signals = []
        
        # Extract text fields for analysis
        text_fields = [
            business_data.get('business_name', ''),
            business_data.get('description', ''),
            business_data.get('location', ''),
            business_data.get('category', '')
        ]
        combined_text = ' '.join(text_fields).lower()
        
        # 1. Location signals (30 points max)
        location_score, location_signals = self._score_location(combined_text)
        score += location_score
        signals.extend(location_signals)
        
        # 2. Category match (25 points max)
        category_score, category_signals = self._score_category(
            combined_text, 
            business_data.get('category')
        )
        score += category_score
        signals.extend(category_signals)
        
        # 3. Contact information (20 points max)
        contact_score, contact_signals = self._score_contact_info(business_data)
        score += contact_score
        signals.extend(contact_signals)
        
        # 4. Page freshness (15 points max)
        freshness_score = self._score_freshness(business_data.get('page_created_date'))
        score += freshness_score
        if freshness_score > 0:
            signals.append(f"Freshness: {freshness_score} points")
        
        # 5. Content quality (10 points max)
        quality_score = self._score_content_quality(business_data)
        score += quality_score
        if quality_score > 0:
            signals.append(f"Content quality: {quality_score} points")
        
        # Determine priority based on score and category
        priority = self._determine_priority(score, business_data.get('category'))
        
        # Update business data
        business_data['confidence_score'] = min(score, 100)
        business_data['priority'] = priority
        business_data['scoring_signals'] = signals
        
        logger.info(f"Scored business '{business_data.get('business_name')}': "
                   f"Score={score}, Priority={priority}")
        
        return business_data
    
    def _score_location(self, text: str) -> tuple:
        """Score based on Nigerian location signals"""
        score = 0
        signals = []
        
        # Check for country mentions (10 points)
        for country in self.location_signals.get('country', []):
            if country.lower() in text:
                score += 10
                signals.append(f"Country: {country}")
                break
        
        # Check for major cities (15 points)
        cities_found = []
        for city in self.location_signals.get('major_cities', []):
            if city.lower() in text:
                cities_found.append(city)
        
        if cities_found:
            score += 15
            signals.append(f"Cities: {', '.join(cities_found[:3])}")
        
        # Check for phone patterns (5 points)
        for pattern in self.location_signals.get('phone_patterns', []):
            if pattern in text:
                score += 5
                signals.append(f"Phone pattern: {pattern}")
                break
        
        return min(score, 30), signals
    
    def _score_category(self, text: str, category: str) -> tuple:
        """Score based on category keyword matches"""
        score = 0
        signals = []
        
        if not category:
            return 0, []
        
        # Get keywords for this category
        category_data = self.categories.get(category, {})
        keywords = category_data.get('keywords', [])
        
        # Count keyword matches
        matches = []
        for keyword in keywords:
            if keyword.lower() in text:
                matches.append(keyword)
        
        if matches:
            # More matches = higher score (up to 25 points)
            score = min(len(matches) * 5, 25)
            signals.append(f"Category keywords: {', '.join(matches[:3])}")
        
        return score, signals
    
    def _score_contact_info(self, business_data: Dict[str, Any]) -> tuple:
        """Score based on available contact information"""
        score = 0
        signals = []
        
        if business_data.get('phone'):
            score += 10
            signals.append("Has phone")
        
        if business_data.get('email'):
            score += 10
            signals.append("Has email")
        
        return score, signals
    
    def _score_freshness(self, page_created_date: str) -> int:
        """Score based on how recently the page was created"""
        if not page_created_date:
            return 0
        
        # This is a simplified version
        # In production, calculate actual days difference
        return 15  # Assume all discovered pages are fresh
    
    def _score_content_quality(self, business_data: Dict[str, Any]) -> int:
        """Score based on content completeness"""
        score = 0
        
        description = business_data.get('description', '')
        if len(description) > 50:
            score += 5
        
        if business_data.get('business_name'):
            score += 5
        
        return score
    
    def _determine_priority(self, score: int, category: str) -> str:
        """Determine priority level"""
        # Get category priority
        category_data = self.categories.get(category, {})
        category_priority = category_data.get('priority', 'medium')
        
        # High score or high-priority category
        if score >= 80 or category_priority == 'high':
            return 'high'
        elif score >= 60:
            return 'medium'
        else:
            return 'low'

