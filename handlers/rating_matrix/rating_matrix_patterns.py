#!/usr/bin/env python3
"""
🎯 Rating Matrix Patterns Module
Centralizes all pattern definitions from knowledge_base.json
Following the same architecture as brand_familiarity_patterns.py
"""

from typing import Dict, List, Any, Optional
import re

class RatingMatrixPatterns:
    """Pattern definitions and detection for rating matrix questions"""
    
    def __init__(self, patterns_data: Optional[Dict[str, Any]] = None):
        """Initialize with patterns from knowledge base"""
        # Patterns are passed directly, already extracted by handler
        self.patterns_data = patterns_data or {}
        
        # Extract pattern categories from centralized source
        self.keywords = self.patterns_data.get('keywords', [])
        self.matrix_indicators = self.patterns_data.get('matrix_indicators', [])
        self.enhanced_patterns = self.patterns_data.get('enhanced_patterns', [])
        self.scale_types = self.patterns_data.get('scale_types', {})
        self.matrix_layouts = self.patterns_data.get('matrix_layouts', [])
        self.common_attributes = self.patterns_data.get('common_attributes', {})
        self.default_response = self.patterns_data.get('default_response', 3)
        self.confidence_thresholds = self.patterns_data.get('confidence_thresholds', {})
        self.response_strategies = self.patterns_data.get('response_strategies', {})
        
        print(f"🎯 Rating Matrix Patterns initialized from centralized brain")
        print(f"   - {len(self.keywords)} keywords loaded")
        print(f"   - {len(self.scale_types)} scale types configured")
        print(f"   - {len(self.response_strategies)} response strategies available")
    
    def detect_matrix_type(self, content: str) -> Optional[str]:
        """Detect if this is a rating matrix question and what type"""
        if not content:
            return None
            
        content_lower = content.lower()
        
        # Check for matrix indicators
        for indicator in self.matrix_indicators:
            if indicator in content_lower:
                # Determine specific type based on keywords
                if any(word in content_lower for word in ["satisfaction", "satisfied"]):
                    return 'satisfaction_matrix'
                elif any(word in content_lower for word in ["agree", "agreement", "disagree"]):
                    return 'agreement_matrix'
                elif any(word in content_lower for word in ["likely", "likelihood", "recommend"]):
                    return 'likelihood_matrix'
                elif any(word in content_lower for word in ["quality", "excellent", "poor"]):
                    return 'quality_matrix'
                else:
                    return 'general_rating_matrix'
        
        # Check enhanced patterns
        for pattern in self.enhanced_patterns:
            if re.search(pattern, content_lower):
                return 'rating_matrix'
        
        # Check keyword density
        keyword_count = sum(1 for keyword in self.keywords if keyword in content_lower)
        if keyword_count >= 3:
            return 'rating_keywords'
        
        return None
    
    def calculate_keyword_confidence(self, content: str, matrix_type: str) -> float:
        """Calculate confidence based on keyword matches"""
        content_lower = content.lower()
        confidence = 0.0
        
        # Base confidence from keywords
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content_lower)
        confidence += min(keyword_matches * 0.1, self.confidence_thresholds.get('base', 0.4))
        
        # Matrix indicator boost
        if any(indicator in content_lower for indicator in self.matrix_indicators):
            confidence += self.confidence_thresholds.get('matrix_boost', 0.3)
        
        # Pattern matching boost
        pattern_matches = sum(1 for pattern in self.enhanced_patterns 
                            if re.search(pattern, content_lower))
        if pattern_matches > 0:
            confidence += self.confidence_thresholds.get('pattern_boost', 0.2)
        
        # Scale detection boost
        if self.detect_scale_type(content):
            confidence += self.confidence_thresholds.get('scale_boost', 0.2)
        
        # Attribute detection boost
        if self.detect_attributes(content):
            confidence += self.confidence_thresholds.get('attribute_boost', 0.1)
        
        return min(confidence, 0.98)
    
    def detect_scale_type(self, content: str) -> Optional[str]:
        """Detect the type of rating scale being used"""
        content_lower = content.lower()
        
        # Check for specific scale patterns
        for scale_name, scale_info in self.scale_types.items():
            # Check if scale options are present
            option_matches = sum(1 for option in scale_info['options'] 
                               if str(option).lower() in content_lower)
            
            if option_matches >= 3:  # At least 3 options present
                return scale_name
        
        # Check for numeric scale patterns (e.g., "scale of 1 to 5")
        scale_pattern = r'scale\s+of\s+(\d+)\s+to\s+(\d+)'
        match = re.search(scale_pattern, content_lower)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            scale_size = end - start + 1
            
            if scale_size == 5:
                return 'likert_5'
            elif scale_size == 7:
                return 'likert_7'
            elif scale_size == 10 or scale_size == 11:
                return 'nps_11'
        
        return None
    
    def detect_attributes(self, content: str) -> List[str]:
        """Detect what attributes are being rated"""
        content_lower = content.lower()
        detected_attributes = []
        
        # Check each category of common attributes
        for category, attributes in self.common_attributes.items():
            for attribute in attributes:
                if attribute in content_lower:
                    detected_attributes.append(attribute)
        
        return detected_attributes
    
    def extract_brands(self, content: str) -> List[str]:
        """Extract brand names from content"""
        # This could be enhanced with NLP or pattern matching
        # For now, return empty list - brands might come from brain
        return []
    
    def extract_attributes(self, content: str, matrix_type: str) -> List[str]:
        """Extract attributes being rated in the matrix"""
        attributes = self.detect_attributes(content)
        
        # Add matrix-type specific attributes
        if matrix_type == 'satisfaction_matrix':
            default_attrs = ['overall satisfaction', 'experience', 'value']
        elif matrix_type == 'quality_matrix':
            default_attrs = ['quality', 'features', 'performance']
        else:
            default_attrs = []
        
        # Combine detected and default attributes
        all_attributes = list(set(attributes + default_attrs))
        return all_attributes[:10]  # Limit to 10 attributes
    
    def get_response_strategy(self, context: Dict[str, Any]) -> str:
        """Determine which response strategy to use"""
        # Could be enhanced with brain learning
        # For now, use weighted random selection
        import random
        
        strategies = list(self.response_strategies.keys())
        weights = [self.response_strategies[s].get('weight', 0.33) for s in strategies]
        
        return random.choices(strategies, weights=weights)[0]
    
    def get_scale_response(self, scale_type: str, strategy: str = 'mixed_realistic') -> int:
        """Get appropriate response for a given scale type and strategy"""
        if scale_type not in self.scale_types:
            return self.default_response
        
        strategy_data = self.response_strategies.get(strategy, {})
        scale_key = scale_type.split('_')[1]  # Extract scale size (5, 7, 10, etc.)
        
        # Get responses for this scale size
        responses = strategy_data.get(f'scale_{scale_key}', [])
        if responses:
            import random
            return random.choice(responses)
        
        # Fallback to scale default
        return self.scale_types[scale_type].get('default', self.default_response)