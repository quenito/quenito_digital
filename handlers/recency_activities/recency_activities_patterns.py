#!/usr/bin/env python3
"""
⏰ Recency Activities Patterns Module
Centralizes all pattern definitions from knowledge_base.json
"""

from typing import Dict, List, Any, Optional, Tuple
import re
from datetime import datetime

class RecencyActivitiesPatterns:
    """Pattern definitions and detection for recency/time-based activity questions"""
    
    def __init__(self, patterns_data: Optional[Dict[str, Any]] = None):
        """Initialize with patterns from knowledge base"""
        self.patterns_data = patterns_data or {}
        
        # Extract pattern categories
        self.keywords = self.patterns_data.get('keywords', [])
        self.primary_indicators = self.patterns_data.get('primary_indicators', [])
        self.enhanced_patterns = self.patterns_data.get('enhanced_patterns', [])
        self.time_frames = self.patterns_data.get('time_frames', {})
        self.activity_categories = self.patterns_data.get('activity_categories', {})
        self.common_activities = self.patterns_data.get('common_activities', [])
        self.confidence_thresholds = self.patterns_data.get('confidence_thresholds', {})
        self.selection_strategies = self.patterns_data.get('selection_strategies', {})
        self.seasonal_considerations = self.patterns_data.get('seasonal_considerations', {})
        self.response_logic = self.patterns_data.get('response_logic', {})
        
        print(f"⏰ Recency Activities Patterns initialized with {len(self.keywords)} keywords")
        print(f"📊 {len(self.activity_categories)} activity categories loaded")
    
    def calculate_confidence(self, question_text: str) -> float:
        """Calculate confidence score for recency/activity questions"""
        confidence = self.confidence_thresholds.get('base', 0.4)
        question_lower = question_text.lower()
        
        # Check primary indicators
        for indicator in self.primary_indicators:
            if indicator.lower() in question_lower:
                confidence += self.confidence_thresholds.get('indicator_boost', 0.3)
                print(f"🎯 Primary indicator matched: '{indicator}'")
                break
        
        # Check enhanced patterns
        for pattern in self.enhanced_patterns:
            if re.search(pattern, question_lower):
                confidence += self.confidence_thresholds.get('pattern_boost', 0.2)
                print(f"🔍 Enhanced pattern matched: '{pattern}'")
                break
        
        # Check time frames
        for time_frame, phrases in self.time_frames.items():
            for phrase in phrases:
                if phrase.lower() in question_lower:
                    confidence += self.confidence_thresholds.get('timeframe_boost', 0.2)
                    print(f"⏱️ Time frame detected: {time_frame}")
                    break
        
        # Check activity categories
        for category, activities in self.activity_categories.items():
            for activity in activities:
                if activity.lower() in question_lower:
                    confidence += self.confidence_thresholds.get('activity_boost', 0.1)
                    print(f"🎪 Activity category detected: {category}")
                    break
        
        return min(confidence, 1.0)
    
    def detect_time_frame(self, question_text: str) -> Optional[str]:
        """Detect the time frame from question text"""
        question_lower = question_text.lower()
        
        for time_frame, phrases in self.time_frames.items():
            for phrase in phrases:
                if phrase.lower() in question_lower:
                    return time_frame
        
        # Default to last year if time-based but no specific frame
        if any(keyword in question_lower for keyword in ['recent', 'past', 'last']):
            return 'last_year'
        
        return None
    
    def detect_activity_categories(self, question_text: str, options: List[str]) -> List[str]:
        """Detect which activity categories are present in the question"""
        detected_categories = []
        
        # Check question text
        question_lower = question_text.lower()
        for category, keywords in self.activity_categories.items():
            for keyword in keywords:
                if keyword.lower() in question_lower:
                    detected_categories.append(category)
                    break
        
        # Check options
        for option in options:
            option_lower = option.lower()
            for category, keywords in self.activity_categories.items():
                for keyword in keywords:
                    if keyword.lower() in option_lower:
                        if category not in detected_categories:
                            detected_categories.append(category)
                        break
        
        return detected_categories
    
    def get_selection_strategy(self, user_profile: Dict[str, Any] = None) -> Dict[str, Any]:
        """Determine selection strategy based on user profile"""
        # Default to moderate strategy
        strategy_name = 'moderate'
        
        if user_profile:
            age = user_profile.get('age', 35)
            
            # Younger users tend to be more active
            if age < 30:
                strategy_name = 'active'
            elif age > 60:
                strategy_name = 'conservative'
        
        return self.selection_strategies.get(strategy_name, self.selection_strategies['moderate'])
    
    def get_seasonal_activities(self) -> List[str]:
        """Get activities appropriate for current season"""
        month = datetime.now().month
        
        if month in [12, 1, 2]:  # Winter
            season = 'winter'
        elif month in [3, 4, 5]:  # Spring
            season = 'spring'
        elif month in [6, 7, 8]:  # Summer
            season = 'summer'
        else:  # Fall
            season = 'fall'
        
        return self.seasonal_considerations.get(season, [])
    
    def filter_activities_by_demographics(self, activities: List[str], user_profile: Dict[str, Any]) -> List[str]:
        """Filter activities based on user demographics"""
        if not user_profile:
            return activities
        
        age = user_profile.get('age', 35)
        filtered = []
        
        for activity in activities:
            activity_lower = activity.lower()
            
            # Age-based filtering
            if age < 21 and any(word in activity_lower for word in ['bar', 'alcohol', 'nightclub']):
                continue
            if age > 70 and any(word in activity_lower for word in ['extreme sports', 'bungee']):
                continue
            
            # Income-based filtering (if available)
            income = user_profile.get('income', '')
            if income and 'Under $25' in income:
                if any(word in activity_lower for word in ['luxury', 'first class', 'expensive']):
                    continue
            
            filtered.append(activity)
        
        return filtered
    
    def validate_activity_combination(self, selected_activities: List[str]) -> bool:
        """Check if selected activities make logical sense together"""
        if not self.response_logic.get('avoid_contradictions', True):
            return True
        
        # Convert to lowercase for comparison
        activities_lower = [a.lower() for a in selected_activities]
        
        # Check for contradictions
        contradictions = [
            ('moved to a new home', 'stayed at the same address'),
            ('changed jobs', 'same employer'),
            ('got married', 'got divorced'),
            ('had a baby', 'no children')
        ]
        
        for activity1, activity2 in contradictions:
            if any(activity1 in a for a in activities_lower) and any(activity2 in a for a in activities_lower):
                return False
        
        return True