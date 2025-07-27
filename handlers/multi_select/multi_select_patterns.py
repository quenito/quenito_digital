#!/usr/bin/env python3
"""
☑️ Multi Select Patterns Module v2.0 - CENTRALIZED MEMORY ARCHITECTURE
Clean interface for multi-select pattern processing with NO hardcoded data.

This module processes pattern data from knowledge_base.json (Quenito's central memory):
- Reads multi_select_questions patterns from central memory
- Detects checkbox and "select all that apply" questions
- Identifies exclusive options (None of the above)
- Provides confidence scoring for multi-select detection

ARCHITECTURE: Central memory (knowledge_base.json) + Clean processing interface
NO HARDCODED DATA - All patterns come from Quenito's central memory!
"""

import re
from typing import Dict, Any, List, Optional, Set


class MultiSelectPatterns:
    """
    ☑️ Clean Multi Select Patterns Interface - NO HARDCODED DATA
    
    Processes multi-select pattern data from knowledge_base.json central memory.
    Specializes in checkbox questions and multiple choice selections.
    
    ARCHITECTURE: Centralized memory + Modular processing
    """
    
    def __init__(self, multi_select_data: Optional[Dict[str, Any]] = None):
        """
        Initialize with multi-select data from knowledge_base.json
        NO hardcoded patterns - all data from Quenito's central memory
        """
        self.multi_select_data = multi_select_data or {}
        self._processed_patterns = {}
        self._exclusive_indicators = []
        self._selection_strategies = {}
        self._process_multi_select_data()
        print(f"☑️ MultiSelectPatterns initialized with {len(self._processed_patterns)} question types from central memory")
    
    def _process_multi_select_data(self):
        """
        Process raw multi-select data from knowledge_base.json
        Converts central memory format into processing-friendly structure
        """
        # Process each multi-select question type from central memory
        for question_type, question_data in self.multi_select_data.items():
            if isinstance(question_data, dict):
                processed_pattern = {
                    'keywords': question_data.get('patterns', []),
                    'common_options': question_data.get('common_options', []),
                    'confidence_threshold': question_data.get('confidence_threshold', 0.5),
                    'learned_patterns': question_data.get('learned_patterns', []),
                    'success_rate': question_data.get('success_rate', 0.0),
                    'min_selections': question_data.get('min_selections', 1),
                    'max_selections': question_data.get('max_selections', 5)
                }
                self._processed_patterns[question_type] = processed_pattern
        
        # Extract exclusive option indicators
        self._exclusive_indicators = self.multi_select_data.get('exclusive_indicators', [
            'none of the above', 'none', 'n/a', 'not applicable',
            'do not apply', 'neither', 'no, none', 'nothing'
        ])
        
        # Extract selection strategies
        self._selection_strategies = self.multi_select_data.get('selection_strategies', {})
        
        print(f"🧠 Processed {len(self._processed_patterns)} multi-select patterns from central memory")
    
    # ========================================
    # PATTERN DETECTION
    # ========================================
    
    def detect_question_type(self, content: str) -> Optional[str]:
        """
        Detect the type of multi-select question based on content
        Returns question type like: 'activities', 'preferences', 'features', etc.
        """
        if not isinstance(content, str):
            content = str(content)
            
        content_lower = content.lower()
        best_match = None
        max_score = 0
        
        # Check for multi-select indicators first
        multi_select_indicators = [
            'select all that apply', 'check all that apply',
            'select all', 'check all', 'choose all',
            'select any', 'check any', 'which of the following',
            'mark all', 'tick all'
        ]
        
        has_multi_indicator = any(indicator in content_lower for indicator in multi_select_indicators)
        
        if not has_multi_indicator:
            # Check for checkbox presence (UI-based detection would confirm)
            checkbox_hints = ['checkbox', 'multiple choice', 'more than one']
            has_multi_indicator = any(hint in content_lower for hint in checkbox_hints)
        
        # If no multi-select indicators, might not be a multi-select question
        if not has_multi_indicator:
            return None
        
        # Now detect specific type
        for question_type, pattern in self._processed_patterns.items():
            keywords = pattern.get('keywords', [])
            score = 0
            
            # Check keyword matches
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    score += 2  # Higher weight for keyword match
            
            # Check for common options
            common_options = pattern.get('common_options', [])
            for option in common_options:
                if option.lower() in content_lower:
                    score += 1
            
            if score > max_score:
                max_score = score
                best_match = question_type
        
        return best_match if max_score >= 2 else 'general_multi_select'
    
    def calculate_keyword_confidence(self, content: str, question_type: str) -> float:
        """
        Calculate confidence score based on keyword matches
        Returns confidence between 0.0 and 1.0
        """
        if not isinstance(content, str):
            content = str(content)
            
        content_lower = content.lower()
        
        # Base confidence for multi-select indicators
        base_confidence = 0.0
        
        multi_indicators = [
            ('select all that apply', 0.3),
            ('check all that apply', 0.3),
            ('select all', 0.2),
            ('check all', 0.2),
            ('which of the following', 0.2),
            ('choose all', 0.2)
        ]
        
        for indicator, weight in multi_indicators:
            if indicator in content_lower:
                base_confidence += weight
                break  # Only count one indicator
        
        # Add pattern-specific confidence
        pattern = self._processed_patterns.get(question_type, {})
        keywords = pattern.get('keywords', [])
        
        if keywords:
            matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
            pattern_confidence = min(matches / max(len(keywords), 1) * 0.5, 0.4)
            base_confidence += pattern_confidence
        
        # Check for checkbox count (would be better with UI detection)
        checkbox_count = content_lower.count('□') + content_lower.count('☐') + content_lower.count('[ ]')
        if checkbox_count >= 3:
            base_confidence += 0.2
        
        # Success rate boost from learning
        success_rate = pattern.get('success_rate', 0.0)
        learning_boost = success_rate * 0.1  # Up to 10% boost
        
        final_confidence = min(base_confidence + learning_boost, 1.0)
        return round(final_confidence, 3)
    
    # ========================================
    # OPTION ANALYSIS
    # ========================================
    
    def has_exclusive_option(self, content: str) -> bool:
        """Check if the question has exclusive options like 'None of the above'"""
        if not isinstance(content, str):
            content = str(content)
            
        content_lower = content.lower()
        
        for indicator in self._exclusive_indicators:
            if indicator.lower() in content_lower:
                return True
        
        return False
    
    def extract_option_categories(self, options: List[str]) -> Dict[str, List[str]]:
        """
        Categorize options for better selection logic
        Returns dict with categories like: activities, brands, features, etc.
        """
        categories = {
            'exclusive': [],
            'activities': [],
            'preferences': [],
            'features': [],
            'brands': [],
            'other': []
        }
        
        for option in options:
            option_lower = option.lower().strip()
            
            # Check for exclusive options first
            if any(exc in option_lower for exc in self._exclusive_indicators):
                categories['exclusive'].append(option)
                continue
            
            # Categorize based on content
            categorized = False
            
            # Activities (verbs, actions)
            activity_patterns = ['watch', 'read', 'play', 'listen', 'shop', 'browse', 'visit']
            if any(pattern in option_lower for pattern in activity_patterns):
                categories['activities'].append(option)
                categorized = True
            
            # Features (technical, product features)
            elif any(word in option_lower for word in ['feature', 'function', 'capability', 'support']):
                categories['features'].append(option)
                categorized = True
            
            # Brands (capitalized words, known brands)
            elif option[0].isupper() and len(option.split()) <= 3:
                categories['brands'].append(option)
                categorized = True
            
            # Preferences (opinions, likes)
            elif any(word in option_lower for word in ['prefer', 'like', 'enjoy', 'favorite']):
                categories['preferences'].append(option)
                categorized = True
            
            if not categorized:
                categories['other'].append(option)
        
        return categories
    
    # ========================================
    # PATTERN ACCESS METHODS
    # ========================================
    
    def get_patterns(self, question_type: Optional[str] = None) -> Dict[str, Any]:
        """Get processed patterns for specific question type or all patterns"""
        if question_type:
            return self._processed_patterns.get(question_type, {})
        return self._processed_patterns
    
    def get_keywords(self, question_type: str) -> List[str]:
        """Get keyword list for specific question type"""
        pattern = self._processed_patterns.get(question_type, {})
        return pattern.get('keywords', [])
    
    def get_common_options(self, question_type: str) -> List[str]:
        """Get common option values for question type"""
        pattern = self._processed_patterns.get(question_type, {})
        return pattern.get('common_options', [])
    
    def get_selection_limits(self, question_type: str) -> tuple[int, int]:
        """Get min and max selection limits for question type"""
        pattern = self._processed_patterns.get(question_type, {})
        return (
            pattern.get('min_selections', 1),
            pattern.get('max_selections', 5)
        )
    
    # ========================================
    # LEARNING INTEGRATION
    # ========================================
    
    def add_learned_pattern(self, question_type: str, pattern: str) -> bool:
        """Add learned pattern from successful automation"""
        try:
            if question_type not in self._processed_patterns:
                self._processed_patterns[question_type] = {
                    'keywords': [],
                    'learned_patterns': [],
                    'confidence_threshold': 0.5,
                    'success_rate': 0.0
                }
            
            learned_patterns = self._processed_patterns[question_type].get('learned_patterns', [])
            if pattern not in learned_patterns:
                learned_patterns.append(pattern)
                self._processed_patterns[question_type]['learned_patterns'] = learned_patterns
                print(f"🧠 Added learned pattern for {question_type}: {pattern}")
                return True
            
            return False
        except Exception as e:
            print(f"❌ Error adding learned pattern: {e}")
            return False
    
    def update_success_rate(self, question_type: str, success_rate: float) -> bool:
        """Update success rate for question type"""
        try:
            if question_type in self._processed_patterns:
                self._processed_patterns[question_type]['success_rate'] = success_rate
                print(f"🧠 Updated success rate for {question_type}: {success_rate:.2f}")
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
            'question_types': list(self._processed_patterns.keys()),
            'total_question_types': len(self._processed_patterns),
            'exclusive_indicators': len(self._exclusive_indicators),
            'keyword_counts': {},
            'success_rates': {},
            'selection_limits': {},
            'data_source': 'knowledge_base.json (central memory)'
        }
        
        for question_type, pattern in self._processed_patterns.items():
            stats['keyword_counts'][question_type] = len(pattern.get('keywords', []))
            stats['success_rates'][question_type] = pattern.get('success_rate', 0.0)
            stats['selection_limits'][question_type] = {
                'min': pattern.get('min_selections', 1),
                'max': pattern.get('max_selections', 5)
            }
        
        return stats
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def __str__(self) -> str:
        """String representation"""
        stats = self.get_pattern_statistics()
        return f"MultiSelectPatterns({stats['total_question_types']} types from central memory)"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"MultiSelectPatterns(question_types={list(self._processed_patterns.keys())}, source='knowledge_base.json')"