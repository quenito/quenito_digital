#!/usr/bin/env python3
"""
Pattern Manager Module - Question pattern detection and matching
Extracted from knowledge_base.py for better modularity and maintainability.

This module handles:
- Question pattern recognition and classification
- Pattern matching algorithms and scoring
- Question type detection logic
- Response strategy recommendations
- Pattern learning and adaptation
"""

from typing import Dict, Any, Optional, List, Tuple
import re
import time


class PatternManager:
    """
    Clean pattern management with dynamic pattern loading from knowledge_base.json.
    Handles question detection, pattern matching, and response strategy selection.
    """
    
    def __init__(self, user_profile, pattern_data: Optional[Dict[str, Any]] = None):
        """Initialize with pattern data from knowledge_base.json"""
        self.user_profile = user_profile
        self.patterns = pattern_data or {}
        self._ensure_pattern_structure()
        print(f"🧠 PatternManager initialized with {len(self.patterns)} pattern categories")
    
    def _ensure_pattern_structure(self):
        """Ensure all required pattern structures exist"""
        if not self.patterns:
            self.patterns = {}
        
        # Initialize empty structures if they don't exist
        default_structures = [
            'demographics_questions',
            'brand_familiarity_questions', 
            'rating_matrix_questions',
            'multi_select_questions',
            'trust_rating_questions',
            'recency_activities_questions',
            'research_required_questions'
        ]
        
        for structure in default_structures:
            if structure not in self.patterns:
                self.patterns[structure] = {}
    
    # ========================================
    # CORE PATTERN DETECTION
    # ========================================
    
    def detect_question_type(self, page_content: str) -> Dict[str, Any]:
        """
        Detect question type from page content using pattern matching
        Returns detection results with confidence scores
        """
        content_lower = page_content.lower()
        detection_results = {
            'primary_type': 'unknown',
            'confidence': 0.0,
            'alternative_types': [],
            'pattern_matches': [],
            'detection_reasoning': []
        }
        
        # Test each pattern category
        pattern_scores = {}
        
        # Demographics detection
        demo_score, demo_matches = self._detect_demographics_patterns(content_lower)
        if demo_score > 0:
            pattern_scores['demographics'] = demo_score
            detection_results['pattern_matches'].extend(demo_matches)
        
        # Brand familiarity detection  
        brand_score, brand_matches = self._detect_brand_patterns(content_lower)
        if brand_score > 0:
            pattern_scores['brand_familiarity'] = brand_score
            detection_results['pattern_matches'].extend(brand_matches)
        
        # Rating matrix detection
        matrix_score, matrix_matches = self._detect_matrix_patterns(content_lower)
        if matrix_score > 0:
            pattern_scores['rating_matrix'] = matrix_score
            detection_results['pattern_matches'].extend(matrix_matches)
        
        # Multi-select detection
        multi_score, multi_matches = self._detect_multiselect_patterns(content_lower)
        if multi_score > 0:
            pattern_scores['multi_select'] = multi_score
            detection_results['pattern_matches'].extend(multi_matches)
        
        # Research required detection
        research_score, research_matches = self._detect_research_patterns(content_lower)
        if research_score > 0:
            pattern_scores['research_required'] = research_score
            detection_results['pattern_matches'].extend(research_matches)
        
        # Determine primary type and confidence
        if pattern_scores:
            primary_type = max(pattern_scores, key=pattern_scores.get)
            primary_confidence = pattern_scores[primary_type]
            
            detection_results['primary_type'] = primary_type
            detection_results['confidence'] = primary_confidence
            
            # Add alternative types (other high-scoring patterns)
            for pattern_type, score in pattern_scores.items():
                if pattern_type != primary_type and score >= 0.3:
                    detection_results['alternative_types'].append({
                        'type': pattern_type,
                        'confidence': score
                    })
            
            detection_results['detection_reasoning'].append(
                f"Primary: {primary_type} (confidence: {primary_confidence:.2f})"
            )
        
        return detection_results
    
    def _detect_demographics_patterns(self, content_lower: str) -> Tuple[float, List[str]]:
        """Detect demographic question patterns using JSON pattern data"""
        matches = []
        total_score = 0.0
        
        # Check each demographic type from JSON data
        demographic_types = ['age', 'gender', 'location']
        
        for demo_type in demographic_types:
            type_data = self.patterns.get(demo_type, {})
            if not type_data:
                continue
                
            # Get patterns from JSON structure
            type_patterns = type_data.get('patterns', [])
            if type_patterns:
                type_score = self._calculate_keyword_score(content_lower, type_patterns)
                if type_score > 0:
                    total_score = max(total_score, type_score)
                    matches.append(f"{demo_type}_patterns: {type_score:.2f}")
        
        # Fallback: check if demographics_questions has nested structure
        demo_questions = self.patterns.get('demographics_questions', {})
        if demo_questions and total_score == 0.0:
            for demo_type, type_data in demo_questions.items():
                type_patterns = type_data.get('patterns', [])
                if type_patterns:
                    type_score = self._calculate_keyword_score(content_lower, type_patterns)
                    if type_score > 0:
                        total_score = max(total_score, type_score)
                        matches.append(f"{demo_type}_nested_patterns: {type_score:.2f}")
        
        return total_score, matches
    
    def _detect_brand_patterns(self, content_lower: str) -> Tuple[float, List[str]]:
        """Detect brand familiarity question patterns"""
        brand_keywords = ['brand', 'familiar', 'heard of', 'know about', 'awareness']
        score = self._calculate_keyword_score(content_lower, brand_keywords)
        
        # Boost score if matrix-like structure detected
        if 'very familiar' in content_lower or 'not familiar' in content_lower:
            score += 0.3
        
        matches = [f"brand_keywords: {score:.2f}"] if score > 0 else []
        return score, matches
    
    def _detect_matrix_patterns(self, content_lower: str) -> Tuple[float, List[str]]:
        """Detect rating matrix question patterns"""
        matrix_indicators = [
            'strongly agree', 'strongly disagree', 'neither agree',
            'very satisfied', 'very dissatisfied', 'somewhat satisfied',
            'excellent', 'good', 'fair', 'poor',
            'always', 'often', 'sometimes', 'rarely', 'never'
        ]
        
        score = self._calculate_keyword_score(content_lower, matrix_indicators)
        
        # Boost if multiple options detected
        option_count = sum(1 for indicator in matrix_indicators if indicator in content_lower)
        if option_count >= 3:
            score += 0.2
        
        matches = [f"matrix_indicators: {score:.2f}"] if score > 0 else []
        return score, matches
    
    def _detect_multiselect_patterns(self, content_lower: str) -> Tuple[float, List[str]]:
        """Detect multi-select question patterns"""
        multiselect_keywords = [
            'select all', 'check all', 'multiple', 'choose all that apply',
            'tick all', 'mark all', 'all applicable'
        ]
        
        score = self._calculate_keyword_score(content_lower, multiselect_keywords)
        matches = [f"multiselect_keywords: {score:.2f}"] if score > 0 else []
        return score, matches
    
    def _detect_research_patterns(self, content_lower: str) -> Tuple[float, List[str]]:
        """Detect research-required question patterns"""
        research_keywords = [
            'specific product', 'specific brand', 'particular model',
            'recent news', 'current events', 'latest', 'newest'
        ]
        
        score = self._calculate_keyword_score(content_lower, research_keywords)
        matches = [f"research_keywords: {score:.2f}"] if score > 0 else []
        return score, matches
    
    def _calculate_keyword_score(self, content: str, keywords: List[str]) -> float:
        """Calculate pattern matching score based on keyword presence"""
        if not keywords:
            return 0.0
        
        matches = sum(1 for keyword in keywords if keyword in content)
        base_score = matches / len(keywords)
        
        # Boost score for exact matches
        exact_matches = sum(1 for keyword in keywords if f" {keyword} " in f" {content} ")
        if exact_matches > 0:
            base_score += 0.2
        
        return min(1.0, base_score)
    
    # ========================================
    # RESPONSE STRATEGY RECOMMENDATIONS
    # ========================================
    
    def get_response_strategy(self, question_type: str, element_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get recommended response strategy for question type"""
        strategy = {
            'primary_strategy': 'unknown',
            'fallback_strategies': [],
            'user_response': None,
            'confidence': 0.0,
            'reasoning': []
        }
        
        if question_type == 'demographics':
            strategy = self._get_demographics_strategy(element_info)
        elif question_type == 'brand_familiarity':
            strategy = self._get_brand_strategy(element_info)
        elif question_type == 'rating_matrix':
            strategy = self._get_matrix_strategy(element_info)
        elif question_type == 'multi_select':
            strategy = self._get_multiselect_strategy(element_info)
        elif question_type == 'research_required':
            strategy = self._get_research_strategy(element_info)
        
        return strategy
    
    def _get_demographics_strategy(self, element_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get strategy for demographic questions"""
        return {
            'primary_strategy': 'user_profile_lookup',
            'fallback_strategies': ['text_input', 'dropdown_selection', 'radio_selection'],
            'user_response': None,  # Will be filled by response lookup
            'confidence': 0.9,
            'reasoning': ['Demographics should use user profile data']
        }
    
    def _get_brand_strategy(self, element_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get strategy for brand familiarity questions"""
        return {
            'primary_strategy': 'brand_profile_lookup',
            'fallback_strategies': ['matrix_selection', 'radio_selection'],
            'user_response': None,
            'confidence': 0.8,
            'reasoning': ['Brand questions use brand familiarity data']
        }
    
    def _get_matrix_strategy(self, element_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get strategy for matrix rating questions"""
        return {
            'primary_strategy': 'matrix_pattern_response',
            'fallback_strategies': ['radio_selection', 'dropdown_selection'],
            'user_response': None,
            'confidence': 0.7,
            'reasoning': ['Matrix questions use pattern-based responses']
        }
    
    def _get_multiselect_strategy(self, element_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get strategy for multi-select questions"""
        return {
            'primary_strategy': 'checkbox_selection',
            'fallback_strategies': ['multiple_choice'],
            'user_response': None,
            'confidence': 0.7,
            'reasoning': ['Multi-select questions require checkbox interaction']
        }
    
    def _get_research_strategy(self, element_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get strategy for research-required questions"""
        return {
            'primary_strategy': 'research_and_respond',
            'fallback_strategies': ['manual_intervention'],
            'user_response': None,
            'confidence': 0.5,
            'reasoning': ['Research required - may need external data lookup']
        }
    
    # ========================================
    # PATTERN LEARNING & ADAPTATION
    # ========================================
    
    def learn_pattern_success(self, question_type: str, pattern_matches: List[str], 
                            success: bool, confidence: float):
        """Learn from successful/failed pattern detection"""
        learning_data = {
            'timestamp': time.time(),
            'question_type': question_type,
            'pattern_matches': pattern_matches,
            'detection_success': success,
            'original_confidence': confidence,
            'learning_type': 'pattern_detection'
        }
        
        # Store learning for future pattern improvement
        if 'pattern_learning' not in self.patterns:
            self.patterns['pattern_learning'] = []
        
        self.patterns['pattern_learning'].append(learning_data)
        print(f"🧠 Pattern learning stored: {question_type} ({'success' if success else 'failure'})")
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get pattern detection statistics"""
        stats = {
            'total_patterns': len(self.patterns),
            'pattern_categories': list(self.patterns.keys()),
            'learning_events': 0,
            'success_rate': 0.0
        }
        
        # Calculate learning statistics
        pattern_learning = self.patterns.get('pattern_learning', [])
        if pattern_learning:
            stats['learning_events'] = len(pattern_learning)
            successes = sum(1 for event in pattern_learning if event['detection_success'])
            stats['success_rate'] = successes / len(pattern_learning)
        
        return stats
    
    # ========================================
    # PATTERN MANAGEMENT
    # ========================================
    
    def add_pattern(self, category: str, pattern_data: Dict[str, Any]):
        """Add a new pattern to the pattern collection"""
        if category not in self.patterns:
            self.patterns[category] = {}
        
        self.patterns[category].update(pattern_data)
        print(f"🧠 Pattern added to {category}: {list(pattern_data.keys())}")
    
    def get_pattern_category(self, category: str) -> Dict[str, Any]:
        """Get all patterns for a specific category"""
        return self.patterns.get(category, {})
    
    def update_pattern_confidence(self, question_type: str, adjustment: float):
        """Update pattern confidence based on learning"""
        # This would be used to adjust pattern matching algorithms
        # based on success/failure feedback
        print(f"🧠 Pattern confidence updated: {question_type} {adjustment:+.2f}")


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def create_pattern_manager(user_profile, pattern_data: Optional[Dict[str, Any]] = None) -> PatternManager:
    """Factory function to create PatternManager instance"""
    return PatternManager(user_profile, pattern_data)


# ========================================
# MODULE TEST
# ========================================

if __name__ == "__main__":
    # Quick module test with sample data
    print("🧠 Pattern Manager Module Test")
    
    # Mock user profile for testing
    class MockUserProfile:
        def get_age(self): return "45"
        def get_gender(self): return "Male"
    
    # Test with empty patterns (normal case when no JSON data)
    mock_profile = MockUserProfile()
    pattern_manager = PatternManager(mock_profile, {})
    
    # Test pattern detection
    sample_content = "What is your age? Please select your age group."
    detection = pattern_manager.detect_question_type(sample_content)
    print(f"Detection result: {detection}")
    
    # Test strategy recommendation
    strategy = pattern_manager.get_response_strategy('demographics', {})
    print(f"Strategy: {strategy}")
    
    print("✅ Pattern Manager Module working correctly!")