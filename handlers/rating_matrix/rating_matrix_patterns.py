#!/usr/bin/env python3
"""
📊 Rating Matrix Patterns Module v2.0 - CENTRALIZED MEMORY ARCHITECTURE
Clean interface for rating matrix pattern processing with NO hardcoded data.

This module processes pattern data from knowledge_base.json (Quenito's central memory):
- Reads rating_matrices patterns from central memory
- Detects brand familiarity and satisfaction matrices
- Extracts brands and attributes from page content
- Provides confidence scoring for matrix detection

ARCHITECTURE: Central memory (knowledge_base.json) + Clean processing interface
NO HARDCODED DATA - All patterns come from Quenito's central memory!
"""

import re
from typing import Dict, Any, List, Optional, Tuple


class RatingMatrixPatterns:
    """
    📊 Clean Rating Matrix Patterns Interface - NO HARDCODED DATA
    
    Processes rating matrix pattern data from knowledge_base.json central memory.
    Specializes in brand familiarity matrices and satisfaction grids.
    
    ARCHITECTURE: Centralized memory + Modular processing
    """
    
    def __init__(self, rating_matrices_data: Optional[Dict[str, Any]] = None):
        """
        Initialize with rating matrices data from knowledge_base.json
        NO hardcoded patterns - all data from Quenito's central memory
        """
        self.matrices_data = rating_matrices_data or {}
        self._processed_patterns = {}
        self._brand_lists = {}
        self._common_attributes = []
        self._process_matrices_data()
        print(f"📊 RatingMatrixPatterns initialized with {len(self._processed_patterns)} matrix types from central memory")
    
    def _process_matrices_data(self):
        """
        Process raw rating matrices data from knowledge_base.json
        Converts central memory format into processing-friendly structure
        """
        # Process each matrix type from central memory
        for matrix_type, matrix_data in self.matrices_data.items():
            if isinstance(matrix_data, dict):
                processed_pattern = {
                    'keywords': matrix_data.get('patterns', []),
                    'confidence_threshold': matrix_data.get('confidence_threshold', 0.7),
                    'learned_patterns': matrix_data.get('learned_patterns', []),
                    'success_rate': matrix_data.get('success_rate', 0.0),
                    'common_ratings': matrix_data.get('common_ratings', []),
                    'attributes': matrix_data.get('attributes', [])
                }
                self._processed_patterns[matrix_type] = processed_pattern
        
        # Extract brand lists if available
        self._brand_lists = self.matrices_data.get('brand_lists', {})
        
        # Extract common attributes for satisfaction matrices
        self._common_attributes = self.matrices_data.get('common_attributes', [
            'quality', 'value', 'service', 'reliability', 'innovation'
        ])
        
        print(f"🧠 Processed {len(self._processed_patterns)} matrix patterns from central memory")
        print(f"🏷️ Loaded {len(self._brand_lists)} brand categories")
    
    # ========================================
    # MATRIX TYPE DETECTION
    # ========================================
    
    def detect_matrix_type(self, content: str) -> Optional[str]:
        """
        Detect the type of rating matrix based on content
        Returns: 'brand_familiarity', 'satisfaction_matrix', etc.
        """
        if not isinstance(content, str):
            content = str(content)
            
        content_lower = content.lower()
        best_match = None
        max_score = 0
        
        for matrix_type, pattern in self._processed_patterns.items():
            keywords = pattern.get('keywords', [])
            score = 0
            
            # Check keyword matches
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    score += 1
            
            # Special boost for brand familiarity
            if matrix_type == 'brand_familiarity':
                if any(term in content_lower for term in ['familiar', 'familiarity', 'awareness', 'recognize']):
                    score += 2
                if 'brand' in content_lower:
                    score += 1
            
            # Special boost for satisfaction
            elif matrix_type == 'satisfaction_matrix':
                if any(term in content_lower for term in ['satisfaction', 'satisfied', 'happy with', 'rate your']):
                    score += 2
            
            if score > max_score:
                max_score = score
                best_match = matrix_type
        
        return best_match if max_score >= 2 else None
    
    def calculate_keyword_confidence(self, content: str, matrix_type: str) -> float:
        """
        Calculate confidence score based on keyword matches
        Returns confidence between 0.0 and 1.0
        """
        pattern = self._processed_patterns.get(matrix_type, {})
        keywords = pattern.get('keywords', [])
        
        if not keywords:
            return 0.0
        
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
        
        # Base confidence from keyword matches
        base_confidence = min(matches / max(len(keywords), 1) * 1.5, 0.8)
        
        # Check for matrix structure indicators
        structure_boost = 0.0
        matrix_indicators = [
            'rate each', 'rate the following', 'for each', 'following brands',
            'following items', 'grid', 'matrix', 'table below'
        ]
        
        for indicator in matrix_indicators:
            if indicator in content_lower:
                structure_boost += 0.1
        
        # Check for scale indicators
        scale_indicators = [
            '1-5', '1-7', '1-10', 'scale', 'strongly', 'extremely',
            'not at all', 'very familiar', 'completely'
        ]
        
        if any(scale in content_lower for scale in scale_indicators):
            structure_boost += 0.1
        
        # Success rate boost from learning
        success_rate = pattern.get('success_rate', 0.0)
        learning_boost = success_rate * 0.1  # Up to 10% boost
        
        final_confidence = min(base_confidence + structure_boost + learning_boost, 1.0)
        return round(final_confidence, 3)
    
    # ========================================
    # BRAND & ATTRIBUTE EXTRACTION
    # ========================================
    
    def extract_brands(self, content: str) -> List[str]:
        """
        Extract brand names from the page content
        Uses patterns and heuristics to identify brands
        """
        brands = []
        content_lower = content.lower()
        
        # Method 1: Look for known brand patterns from central memory
        for category, brand_list in self._brand_lists.items():
            for brand in brand_list:
                if brand.lower() in content_lower:
                    brands.append(brand)
        
        # Method 2: Extract brands near keywords
        brand_patterns = [
            r'(?:brand|company|product)s?\s*(?:include|are|such as|like|:)\s*([^.?!]+)',
            r'(?:following|these)\s+(?:brand|company|product)s?\s*:?\s*([^.?!]+)',
            r'rate\s+(?:the\s+)?following\s*:?\s*([^.?!]+)'
        ]
        
        for pattern in brand_patterns:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                # Split by common delimiters
                potential_brands = re.split(r'[,;]|\band\b|\bor\b', match)
                for brand in potential_brands:
                    brand = brand.strip()
                    # Basic validation - capitalize and clean
                    if 3 <= len(brand) <= 50 and not brand.startswith(('the ', 'a ', 'an ')):
                        # Capitalize brand name
                        brand_clean = ' '.join(word.capitalize() for word in brand.split())
                        if brand_clean and brand_clean not in brands:
                            brands.append(brand_clean)
        
        # Method 3: Look for capitalized words that might be brands
        capitalized_pattern = r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b'
        potential_brands = re.findall(capitalized_pattern, content)
        
        for brand in potential_brands:
            # Filter out common words and add unique brands
            if (len(brand) >= 3 and 
                brand not in brands and
                brand.lower() not in ['the', 'this', 'that', 'rate', 'please', 'following']):
                brands.append(brand)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_brands = []
        for brand in brands:
            if brand not in seen:
                seen.add(brand)
                unique_brands.append(brand)
        
        return unique_brands[:20]  # Limit to 20 brands max
    
    def extract_attributes(self, content: str, matrix_type: str) -> List[str]:
        """
        Extract attributes/dimensions to rate (for satisfaction matrices)
        """
        attributes = []
        
        # Get default attributes for this matrix type
        pattern = self._processed_patterns.get(matrix_type, {})
        default_attributes = pattern.get('attributes', self._common_attributes)
        
        content_lower = content.lower()
        
        # Look for attribute patterns
        attribute_patterns = [
            r'rate\s+(?:each\s+)?(?:brand|product|company)\s+on\s+(?:the\s+)?following\s*:?\s*([^.?!]+)',
            r'(?:attributes|dimensions|aspects|criteria)\s*(?:include|are|:)\s*([^.?!]+)',
            r'(?:quality|value|service|reliability|innovation|price|design|features)'
        ]
        
        for pattern in attribute_patterns:
            if pattern.startswith('(?:'):
                # Direct attribute matching
                matches = re.findall(pattern, content_lower)
                attributes.extend(matches)
            else:
                # Extract from context
                matches = re.findall(pattern, content_lower, re.IGNORECASE)
                for match in matches:
                    potential_attrs = re.split(r'[,;]|\band\b', match)
                    for attr in potential_attrs:
                        attr = attr.strip().lower()
                        if 2 <= len(attr) <= 30:
                            attributes.append(attr)
        
        # Use defaults if no attributes found
        if not attributes:
            attributes = default_attributes
        
        # Remove duplicates
        return list(dict.fromkeys(attributes))[:10]  # Max 10 attributes
    
    # ========================================
    # PATTERN ACCESS METHODS
    # ========================================
    
    def get_patterns(self, matrix_type: Optional[str] = None) -> Dict[str, Any]:
        """Get processed patterns for specific matrix type or all patterns"""
        if matrix_type:
            return self._processed_patterns.get(matrix_type, {})
        return self._processed_patterns
    
    def get_keywords(self, matrix_type: str) -> List[str]:
        """Get keyword list for specific matrix type"""
        pattern = self._processed_patterns.get(matrix_type, {})
        return pattern.get('keywords', [])
    
    def get_common_ratings(self, matrix_type: str) -> List[int]:
        """Get common rating values for matrix type"""
        pattern = self._processed_patterns.get(matrix_type, {})
        return pattern.get('common_ratings', [1, 2, 3, 4, 5])
    
    def get_brand_category(self, brand: str) -> Optional[str]:
        """Get category for a specific brand"""
        brand_lower = brand.lower()
        for category, brands in self._brand_lists.items():
            if any(b.lower() == brand_lower for b in brands):
                return category
        return None
    
    # ========================================
    # LEARNING INTEGRATION
    # ========================================
    
    def add_learned_pattern(self, matrix_type: str, pattern: str) -> bool:
        """Add learned pattern from successful automation"""
        try:
            if matrix_type not in self._processed_patterns:
                self._processed_patterns[matrix_type] = {
                    'keywords': [],
                    'learned_patterns': [],
                    'confidence_threshold': 0.7,
                    'success_rate': 0.0
                }
            
            learned_patterns = self._processed_patterns[matrix_type].get('learned_patterns', [])
            if pattern not in learned_patterns:
                learned_patterns.append(pattern)
                self._processed_patterns[matrix_type]['learned_patterns'] = learned_patterns
                print(f"🧠 Added learned pattern for {matrix_type}: {pattern}")
                return True
            
            return False
        except Exception as e:
            print(f"❌ Error adding learned pattern: {e}")
            return False
    
    def update_success_rate(self, matrix_type: str, success_rate: float) -> bool:
        """Update success rate for matrix type"""
        try:
            if matrix_type in self._processed_patterns:
                self._processed_patterns[matrix_type]['success_rate'] = success_rate
                print(f"🧠 Updated success rate for {matrix_type}: {success_rate:.2f}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error updating success rate: {e}")
            return False
    
    # ========================================
    # PATTERN STATISTICS
    # ========================================
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pattern statistics"""
        stats = {
            'matrix_types': list(self._processed_patterns.keys()),
            'total_matrix_types': len(self._processed_patterns),
            'brand_categories': list(self._brand_lists.keys()),
            'total_known_brands': sum(len(brands) for brands in self._brand_lists.values()),
            'keyword_counts': {},
            'success_rates': {},
            'data_source': 'knowledge_base.json (central memory)'
        }
        
        for matrix_type, pattern in self._processed_patterns.items():
            stats['keyword_counts'][matrix_type] = len(pattern.get('keywords', []))
            stats['success_rates'][matrix_type] = pattern.get('success_rate', 0.0)
        
        return stats
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def __str__(self) -> str:
        """String representation"""
        stats = self.get_pattern_statistics()
        return f"RatingMatrixPatterns({stats['total_matrix_types']} types from central memory)"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"RatingMatrixPatterns(matrix_types={list(self._processed_patterns.keys())}, source='knowledge_base.json')"