#!/usr/bin/env python3
"""
☑️ Multi Select Patterns Module
Centralizes all pattern definitions from knowledge_base.json
Following the same architecture as brand_familiarity_patterns.py
"""

from typing import Dict, List, Any, Optional
import re

class MultiSelectPatterns:
    """Pattern definitions and detection for multi-select questions"""
    
    def __init__(self, patterns_data: Optional[Dict[str, Any]] = None):
        """Initialize with patterns from knowledge base"""
        # Patterns are passed directly, already extracted by handler
        self.patterns_data = patterns_data or {}
        
        # Extract pattern categories from centralized source
        self.keywords = self.patterns_data.get('keywords', [])
        self.primary_indicators = self.patterns_data.get('primary_indicators', [])
        self.enhanced_patterns = self.patterns_data.get('enhanced_patterns', [])
        self.exclusive_options = self.patterns_data.get('exclusive_options', [])
        self.common_topics = self.patterns_data.get('common_topics', {})
        self.checkbox_layouts = self.patterns_data.get('checkbox_layouts', [])
        self.confidence_thresholds = self.patterns_data.get('confidence_thresholds', {})
        self.selection_strategies = self.patterns_data.get('selection_strategies', {})
        self.selection_rules = self.patterns_data.get('selection_rules', {})
        
        print(f"☑️ Multi-Select Patterns initialized from centralized brain")
        print(f"   - {len(self.keywords)} keywords loaded")
        print(f"   - {len(self.primary_indicators)} primary indicators")
        print(f"   - {len(self.exclusive_options)} exclusive options")
    
    def detect_question_type(self, content: str) -> Optional[str]:
        """Detect if this is a multi-select question"""
        if not content:
            return None
            
        content_lower = content.lower()
        
        # Check for primary indicators
        for indicator in self.primary_indicators:
            if indicator in content_lower:
                return 'multi_select_primary'
        
        # Check enhanced patterns
        for pattern in self.enhanced_patterns:
            if re.search(pattern, content_lower):
                return 'multi_select_pattern'
        
        # Check keyword density
        keyword_count = sum(1 for keyword in self.keywords if keyword in content_lower)
        if keyword_count >= 2:
            return 'multi_select_keywords'
        
        return None
    
    def calculate_keyword_confidence(self, content: str, question_type: str) -> float:
        """Calculate confidence based on keyword matches"""
        content_lower = content.lower()
        confidence = 0.0
        
        # Base confidence from keywords
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content_lower)
        confidence += min(keyword_matches * 0.1, self.confidence_thresholds.get('base', 0.4))
        
        # Primary indicator boost
        if any(indicator in content_lower for indicator in self.primary_indicators):
            confidence += self.confidence_thresholds.get('indicator_boost', 0.3)
        
        # Pattern matching boost
        pattern_matches = sum(1 for pattern in self.enhanced_patterns 
                            if re.search(pattern, content_lower))
        if pattern_matches > 0:
            confidence += self.confidence_thresholds.get('pattern_boost', 0.2)
        
        # Checkbox detection boost (simplified)
        checkbox_hints = ['checkbox', '☐', '□', '[ ]']
        if any(hint in content_lower for hint in checkbox_hints):
            confidence += self.confidence_thresholds.get('checkbox_boost', 0.2)
        
        return min(confidence, 0.98)
    
    def is_exclusive_option(self, option_text: str) -> bool:
        """Check if an option is exclusive (like 'None of the above')"""
        option_lower = option_text.lower().strip()
        
        for exclusive in self.exclusive_options:
            if exclusive.lower() in option_lower:
                return True
        
        return False
    
    def has_exclusive_option(self, content: str) -> bool:
        """Check if the question has exclusive options"""
        content_lower = content.lower()
        
        for exclusive in self.exclusive_options:
            if exclusive.lower() in content_lower:
                return True
        
        return False
    
    def detect_topic_category(self, content: str) -> Optional[str]:
        """Detect which topic category this question belongs to"""
        content_lower = content.lower()
        
        for category, topic_keywords in self.common_topics.items():
            matches = sum(1 for keyword in topic_keywords if keyword in content_lower)
            if matches >= 2:  # At least 2 topic keywords
                return category
        
        return None
    
    def get_selection_strategy(self, context: Dict[str, Any]) -> str:
        """Determine which selection strategy to use"""
        # Could be enhanced with more logic
        # For now, return a strategy name
        has_exclusive = context.get('has_exclusive', False)
        option_count = context.get('option_count', 5)
        
        if has_exclusive and context.get('prefer_none', False):
            return 'none_strategy'
        elif option_count <= 3:
            return 'conservative'
        elif option_count <= 6:
            return 'moderate'
        else:
            return 'comprehensive'
    
    def get_selection_limits(self, strategy: str) -> Dict[str, int]:
        """Get min/max selections for a strategy"""
        strategy_data = self.selection_strategies.get(strategy, {})
        return {
            'min': strategy_data.get('min', 1),
            'max': strategy_data.get('max', 3)
        }