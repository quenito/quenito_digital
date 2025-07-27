#!/usr/bin/env python3
"""
🎯 Brand Familiarity Patterns Module
Centralizes all pattern definitions from knowledge_base.json

This module:
- Loads patterns from the centralized brain (knowledge_base.json)
- Detects brand familiarity question types
- Calculates confidence scores
- Identifies brand categories
"""

from typing import Dict, List, Any, Optional
import re


class BrandFamiliarityPatterns:
    """Pattern definitions and detection for brand familiarity questions"""
    
    def __init__(self, patterns_data: Optional[Dict[str, Any]] = None):
        """Initialize with patterns from knowledge base"""
        self.patterns_data = patterns_data or {}
        
        # Extract pattern categories from centralized brain
        self.keywords = self.patterns_data.get('keywords', [
            'familiar', 'brand', 'heard of', 'currently use', 
            'aware of', 'recognize', 'know', 'experience with'
        ])
        
        self.matrix_indicators = self.patterns_data.get('matrix_indicators', [
            'how familiar are you with',
            'rate your familiarity',
            'please indicate your familiarity'
        ])
        
        self.enhanced_patterns = self.patterns_data.get('enhanced_patterns', [])
        self.response_levels = self.patterns_data.get('response_levels', {})
        self.matrix_layouts = self.patterns_data.get('matrix_layouts', [])
        self.common_brands = self.patterns_data.get('common_brands', {})
        self.default_response = self.patterns_data.get('default_response', 'somewhat_familiar')
        self.confidence_thresholds = self.patterns_data.get('confidence_thresholds', {
            'base': 0.4,
            'matrix_boost': 0.3,
            'pattern_boost': 0.2,
            'option_boost': 0.2
        })
        
        print(f"🎯 Brand Familiarity Patterns initialized")
        print(f"   - Keywords: {len(self.keywords)}")
        print(f"   - Matrix indicators: {len(self.matrix_indicators)}")
        print(f"   - Brand categories: {len(self.common_brands)}")
    
    def detect_question_type(self, content: str) -> Optional[str]:
        """
        Detect if this is a brand familiarity question
        
        Returns:
            'brand_matrix' - Multiple brands in matrix layout
            'brand_single' - Single brand question
            None - Not a brand question
        """
        content_lower = content.lower()
        
        # Check for matrix indicators first (highest priority)
        for indicator in self.matrix_indicators:
            if indicator in content_lower:
                # Check if multiple brands present
                brand_count = self._count_brands_in_content(content_lower)
                if brand_count >= 3:
                    return 'brand_matrix'
                else:
                    return 'brand_single'
        
        # Check general brand keywords
        keyword_count = sum(1 for keyword in self.keywords if keyword in content_lower)
        if keyword_count >= 2:
            # Determine if matrix or single based on structure
            if self._detect_matrix_structure(content_lower):
                return 'brand_matrix'
            else:
                return 'brand_single'
        
        return None
    
    def calculate_keyword_confidence(self, content: str, question_type: str) -> float:
        """
        Calculate confidence based on keyword matches
        
        Uses thresholds from centralized brain configuration
        """
        content_lower = content.lower()
        confidence = 0.0
        
        # Base confidence from keyword matches
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content_lower)
        if keyword_matches > 0:
            confidence += min(
                keyword_matches * 0.1, 
                self.confidence_thresholds.get('base', 0.4)
            )
        
        # Matrix indicator boost
        matrix_matches = sum(1 for indicator in self.matrix_indicators 
                           if indicator in content_lower)
        if matrix_matches > 0:
            confidence += self.confidence_thresholds.get('matrix_boost', 0.3)
        
        # Enhanced pattern matching using regex
        if self.enhanced_patterns:
            pattern_matches = sum(1 for pattern in self.enhanced_patterns 
                                if re.search(pattern, content_lower))
            if pattern_matches > 0:
                confidence += self.confidence_thresholds.get('pattern_boost', 0.2)
        
        # Response level detection boost
        response_count = 0
        for level_name, level_keywords in self.response_levels.items():
            for keyword in level_keywords:
                if keyword in content_lower:
                    response_count += 1
        
        if response_count >= 2:
            confidence += self.confidence_thresholds.get('option_boost', 0.2)
        
        # Cap at 0.98 to match ultra-conservative threshold
        return min(confidence, 0.98)
    
    def detect_brand_categories(self, content: str) -> List[str]:
        """Detect which brand categories are present in the content"""
        content_lower = content.lower()
        detected_categories = []
        
        for category, brands in self.common_brands.items():
            brand_count = sum(1 for brand in brands if brand in content_lower)
            if brand_count >= 2:
                detected_categories.append(category)
        
        return detected_categories
    
    def get_response_mapping(self, response_text: str) -> str:
        """Map response text to standardized level"""
        response_lower = response_text.lower()
        
        for level_name, level_keywords in self.response_levels.items():
            for keyword in level_keywords:
                if keyword in response_lower:
                    return level_name
        
        return self.default_response
    
    def get_brands_from_content(self, content: str) -> List[str]:
        """Extract brand names from content"""
        content_lower = content.lower()
        found_brands = []
        
        # Check all known brands
        for category_brands in self.common_brands.values():
            for brand in category_brands:
                if brand in content_lower and brand not in found_brands:
                    found_brands.append(brand)
        
        return found_brands
    
    def _count_brands_in_content(self, content_lower: str) -> int:
        """Count how many brands are mentioned"""
        count = 0
        for category_brands in self.common_brands.values():
            for brand in category_brands:
                if brand in content_lower:
                    count += 1
        return count
    
    def _detect_matrix_structure(self, content_lower: str) -> bool:
        """Detect if content has matrix-like structure"""
        # Check for matrix layout indicators
        for layout in self.matrix_layouts:
            if layout in content_lower:
                return True
        
        # Check for multiple response options repeated
        response_option_sets = 0
        for level_keywords in self.response_levels.values():
            if any(keyword in content_lower for keyword in level_keywords):
                response_option_sets += 1
        
        # Matrix likely if we see multiple response option sets
        return response_option_sets >= 2
    
    def validate_patterns(self) -> Dict[str, Any]:
        """Validate pattern configuration"""
        return {
            'has_keywords': len(self.keywords) > 0,
            'has_matrix_indicators': len(self.matrix_indicators) > 0,
            'has_response_levels': len(self.response_levels) > 0,
            'has_brands': len(self.common_brands) > 0,
            'total_brands': sum(len(brands) for brands in self.common_brands.values()),
            'confidence_thresholds_set': len(self.confidence_thresholds) > 0
        }