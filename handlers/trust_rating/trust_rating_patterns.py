#!/usr/bin/env python3
"""
🎯 Trust Rating Patterns Module
Centralizes all pattern definitions from knowledge_base.json
Following the same architecture as other refactored patterns modules
"""

from typing import Dict, List, Any, Optional
import re

class TrustRatingPatterns:
    """Pattern definitions and detection for trust rating questions"""
    
    def __init__(self, patterns_data: Optional[Dict[str, Any]] = None):
        """Initialize with patterns from knowledge base"""
        # Patterns are passed directly, already extracted by handler
        self.patterns_data = patterns_data or {}
        
        # Extract pattern categories from centralized source
        self.keywords = self.patterns_data.get('keywords', [])
        self.primary_indicators = self.patterns_data.get('primary_indicators', [])
        self.enhanced_patterns = self.patterns_data.get('enhanced_patterns', [])
        self.trust_text_options = self.patterns_data.get('trust_text_options', {})
        self.scale_types = self.patterns_data.get('scale_types', {})
        self.related_concepts = self.patterns_data.get('related_concepts', [])
        self.trust_entities = self.patterns_data.get('trust_entities', {})
        self.confidence_thresholds = self.patterns_data.get('confidence_thresholds', {})
        self.response_strategies = self.patterns_data.get('response_strategies', {})
        self.scale_detection_hints = self.patterns_data.get('scale_detection_hints', [])
        self.default_strategy = self.patterns_data.get('default_strategy', 'conservative_positive')
        
        print(f"🎯 Trust Rating Patterns initialized from centralized brain")
        print(f"   - {len(self.keywords)} keywords loaded")
        print(f"   - {len(self.scale_types)} scale types configured")
        print(f"   - {len(self.response_strategies)} response strategies available")
    
    def detect_question_type(self, content: str) -> Optional[str]:
        """Detect if this is a trust rating question"""
        if not content:
            return None
            
        content_lower = content.lower()
        
        # Check for primary indicators
        for indicator in self.primary_indicators:
            if indicator in content_lower:
                return 'trust_rating_primary'
        
        # Check enhanced patterns
        for pattern in self.enhanced_patterns:
            if re.search(pattern, content_lower):
                return 'trust_rating_pattern'
        
        # Check keyword density
        keyword_count = sum(1 for keyword in self.keywords if keyword in content_lower)
        if keyword_count >= 2:
            return 'trust_rating_keywords'
        
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
        
        # Scale detection boost
        if self.detect_scale_type(content):
            confidence += self.confidence_thresholds.get('scale_boost', 0.2)
        
        # Entity detection boost
        if self.detect_entity(content):
            confidence += self.confidence_thresholds.get('entity_boost', 0.1)
        
        return min(confidence, 0.98)
    
    def detect_scale_type(self, content: str) -> Optional[str]:
        """Detect the type of trust rating scale being used"""
        content_lower = content.lower()
        
        # Check for scale hints in content
        for hint in self.scale_detection_hints:
            if hint in content_lower:
                # Try to extract scale numbers
                numbers = re.findall(r'\b\d+\b', content_lower[content_lower.index(hint):content_lower.index(hint)+20])
                if numbers:
                    max_num = max(int(n) for n in numbers)
                    if max_num == 5:
                        return 'trust_5'
                    elif max_num == 7:
                        return 'trust_7'
                    elif max_num == 10:
                        return 'trust_10'
                    elif max_num == 100:
                        return 'trust_100'
        
        # Check for specific scale patterns
        for scale_name, scale_info in self.scale_types.items():
            scale_range = scale_info.get('range', [])
            if scale_range:
                # Check if scale endpoints are mentioned
                if str(min(scale_range)) in content_lower and str(max(scale_range)) in content_lower:
                    return scale_name
        
        # Check for text options to infer scale
        for level_type, options in self.trust_text_options.items():
            matches = sum(1 for option in options if option in content_lower)
            if matches >= 2:
                # Multiple text options suggest a text-based scale
                return 'trust_5'  # Default to 5-point for text scales
        
        return None
    
    def detect_entity(self, content: str) -> Optional[str]:
        """Detect what entity is being rated for trust"""
        content_lower = content.lower()
        
        # Look for entity types
        for entity_type, keywords in self.trust_entities.items():
            for keyword in keywords:
                # Look for pattern: "trust [in/of] [the] [entity]"
                patterns = [
                    f"trust.*{keyword}",
                    f"{keyword}.*trust",
                    f"rate.*{keyword}",
                    f"{keyword}.*reliab"
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, content_lower)
                    if match:
                        # Try to extract the actual entity name
                        # This is simplified - could be enhanced
                        return keyword.capitalize()
        
        # Look for quoted entities
        quoted = re.findall(r'"([^"]+)"', content)
        if quoted:
            return quoted[0]
        
        return None
    
    def get_trust_value(self, scale_type: str, strategy: str) -> int:
        """Get appropriate trust value for a scale and strategy"""
        scale_data = self.scale_types.get(scale_type, {})
        strategy_data = self.response_strategies.get(strategy, {})
        
        # Get preferred values for this strategy and scale
        preference_key = f"{scale_type.split('_')[0]}_{scale_type.split('_')[1]}_preference"
        preferred_values = strategy_data.get(preference_key, [])
        
        if preferred_values:
            # Return first preferred value (could randomize)
            return preferred_values[0]
        
        # Fallback to scale default
        return scale_data.get('default', 3)
    
    def get_text_options(self, strategy: str) -> List[str]:
        """Get text options based on strategy"""
        strategy_data = self.response_strategies.get(strategy, {})
        text_preferences = strategy_data.get('text_preference', [])
        
        # Return in order of preference
        return text_preferences
    
    def get_scale_data(self, scale_type: str) -> Dict[str, Any]:
        """Get full scale data for a scale type"""
        return self.scale_types.get(scale_type, {})
    
    def get_strategy_name(self, context: str) -> str:
        """Determine strategy based on context (if not specified by brain)"""
        # Could add context analysis here
        return self.default_strategy