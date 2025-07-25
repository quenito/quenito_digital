#!/usr/bin/env python3
"""
📊 Demographics Patterns Module v2.0 - CENTRALIZED MEMORY ARCHITECTURE
Clean interface for demographics pattern processing with NO hardcoded data.

This module processes pattern data from knowledge_base.json (Quenito's central memory):
- Reads demographics_questions patterns from central memory
- Provides clean interface for pattern matching and detection  
- Processes keyword matching and confidence scoring
- Handles response mapping and strategy selection

ARCHITECTURE: Central memory (knowledge_base.json) + Clean processing interface
NO HARDCODED DATA - All patterns come from Quenito's central memory!
"""

from typing import Dict, Any, List, Optional


class DemographicsPatterns:
    """
    📊 Clean Demographics Patterns Interface - NO HARDCODED DATA
    
    Processes demographics pattern data from knowledge_base.json central memory.
    Provides clean interface for pattern matching, detection, and response mapping.
    
    ARCHITECTURE: Centralized memory + Modular processing
    """
    
    def __init__(self, demographics_questions_data: Optional[Dict[str, Any]] = None):
        """
        Initialize with demographics questions data from knowledge_base.json
        NO hardcoded patterns - all data from Quenito's central memory
        """
        self.demographics_data = demographics_questions_data or {}
        self._processed_patterns = {}
        self._process_demographics_data()
        print(f"📊 DemographicsPatterns initialized with {len(self._processed_patterns)} question types from central memory")
    
    def _process_demographics_data(self):
        """
        Process raw demographics data from knowledge_base.json into usable patterns
        Converts central memory format into processing-friendly structure
        """
        # Process each demographic question type from central memory
        for question_type, question_data in self.demographics_data.items():
            if isinstance(question_data, dict):
                processed_pattern = {
                    'keywords': question_data.get('patterns', []),
                    'responses': question_data.get('responses', []),
                    'confidence_threshold': question_data.get('confidence_threshold', 0.5),
                    'learned_patterns': question_data.get('learned_patterns', []),
                    'success_rate': question_data.get('success_rate', 0.0)
                }
                self._processed_patterns[question_type] = processed_pattern
        
        print(f"🧠 Processed {len(self._processed_patterns)} demographics patterns from central memory")
    
    # ========================================
    # PATTERN ACCESS METHODS (FROM CENTRAL MEMORY)
    # ========================================
    
    def get_patterns(self, question_type: Optional[str] = None) -> Dict[str, Any]:
        """Get processed patterns for specific question type or all patterns"""
        if question_type:
            return self._processed_patterns.get(question_type, {})
        return self._processed_patterns
    
    def get_keywords(self, question_type: str) -> List[str]:
        """Get keyword list for specific question type from central memory"""
        pattern = self._processed_patterns.get(question_type, {})
        return pattern.get('keywords', [])
    
    def get_responses(self, question_type: str) -> List[str]:
        """Get available responses for question type from central memory"""
        pattern = self._processed_patterns.get(question_type, {})
        return pattern.get('responses', [])
    
    def get_confidence_threshold(self, question_type: str) -> float:
        """Get confidence threshold for question type from central memory"""
        pattern = self._processed_patterns.get(question_type, {})
        return pattern.get('confidence_threshold', 0.5)
    
    def get_learned_patterns(self, question_type: str) -> List[str]:
        """Get learned patterns for question type from brain learning"""
        pattern = self._processed_patterns.get(question_type, {})
        return pattern.get('learned_patterns', [])
    
    # ========================================
    # PATTERN MATCHING METHODS  
    # ========================================
    
    def detect_question_type(self, content: str) -> Optional[str]:
        """
        Detect question type based on content keywords from central memory
        Returns the most likely question type or None
        """
        content_lower = content.lower()
        best_match = None
        max_matches = 0
        
        for question_type, pattern in self._processed_patterns.items():
            keywords = pattern.get('keywords', [])
            matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
            
            if matches > max_matches:
                max_matches = matches
                best_match = question_type
        
        return best_match if max_matches > 0 else None
    
    def calculate_keyword_confidence(self, content: str, question_type: str) -> float:
        """
        Calculate confidence score based on keyword matches from central memory
        Returns confidence between 0.0 and 1.0
        """
        pattern = self._processed_patterns.get(question_type, {})
        keywords = pattern.get('keywords', [])
        
        if not keywords:
            return 0.0
        
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
        
        # Calculate confidence based on match ratio
        base_confidence = min(matches / len(keywords) * 2.0, 1.0)
        
        # Boost confidence based on success rate from central memory
        success_rate = pattern.get('success_rate', 0.0)
        confidence_boost = success_rate * 0.2  # Up to 20% boost
        
        final_confidence = min(base_confidence + confidence_boost, 1.0)
        return round(final_confidence, 3)
    
    def find_matching_response(self, question_type: str, text: str) -> Optional[str]:
        """
        Find matching response from central memory based on text content
        Returns the best matching response if found
        """
        pattern = self._processed_patterns.get(question_type, {})
        responses = pattern.get('responses', [])
        text_lower = text.lower()
        
        # Direct match first
        for response in responses:
            if response.lower() in text_lower or text_lower in response.lower():
                return response
        
        # Partial match
        for response in responses:
            response_words = response.lower().split()
            text_words = text_lower.split()
            if any(word in text_words for word in response_words):
                return response
        
        return None
    
    # ========================================
    # BRAIN LEARNING INTEGRATION
    # ========================================
    
    def add_learned_pattern(self, question_type: str, pattern: str, success: bool = True) -> bool:
        """
        Add learned pattern from brain learning (updates central memory)
        This would typically update knowledge_base.json via the knowledge_base
        """
        try:
            if question_type not in self._processed_patterns:
                self._processed_patterns[question_type] = {
                    'keywords': [],
                    'responses': [],
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
        """Update success rate for question type (from brain learning)"""
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
    # PATTERN VALIDATION & STATS
    # ========================================
    
    def validate_patterns(self) -> Dict[str, Any]:
        """Validate pattern data integrity from central memory"""
        validation_result = {
            'valid': True,
            'question_types': len(self._processed_patterns),
            'total_keywords': 0,
            'total_responses': 0,
            'issues': []
        }
        
        for question_type, pattern in self._processed_patterns.items():
            # Count data
            validation_result['total_keywords'] += len(pattern.get('keywords', []))
            validation_result['total_responses'] += len(pattern.get('responses', []))
            
            # Check for empty patterns
            if not pattern.get('keywords') and not pattern.get('learned_patterns'):
                validation_result['issues'].append(f"No keywords or learned patterns for {question_type}")
        
        validation_result['valid'] = len(validation_result['issues']) == 0
        return validation_result
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pattern statistics from central memory"""
        stats = {
            'question_types': list(self._processed_patterns.keys()),
            'total_question_types': len(self._processed_patterns),
            'keyword_counts': {},
            'response_counts': {},
            'success_rates': {},
            'data_source': 'knowledge_base.json (central memory)'
        }
        
        for question_type, pattern in self._processed_patterns.items():
            stats['keyword_counts'][question_type] = len(pattern.get('keywords', []))
            stats['response_counts'][question_type] = len(pattern.get('responses', []))
            stats['success_rates'][question_type] = pattern.get('success_rate', 0.0)
        
        return stats
    
    # ========================================
    # CENTRAL MEMORY INTEGRATION
    # ========================================
    
    def sync_with_central_memory(self, updated_demographics_data: Dict[str, Any]) -> bool:
        """
        Sync with updated data from knowledge_base.json
        Called when central memory is updated by brain learning
        """
        try:
            self.demographics_data = updated_demographics_data
            self._processed_patterns = {}
            self._process_demographics_data()
            print(f"🧠 Synced with central memory - {len(self._processed_patterns)} patterns updated")
            return True
        except Exception as e:
            print(f"❌ Error syncing with central memory: {e}")
            return False
    
    def get_central_memory_update(self) -> Dict[str, Any]:
        """
        Get processed pattern data in format suitable for updating knowledge_base.json
        Used by knowledge_base to save learned patterns back to central memory
        """
        central_memory_format = {}
        
        for question_type, pattern in self._processed_patterns.items():
            central_memory_format[question_type] = {
                'patterns': pattern.get('keywords', []),
                'responses': pattern.get('responses', []),
                'learned_patterns': pattern.get('learned_patterns', []),
                'confidence_threshold': pattern.get('confidence_threshold', 0.5),
                'success_rate': pattern.get('success_rate', 0.0)
            }
        
        return central_memory_format
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def __str__(self) -> str:
        """String representation of patterns"""
        stats = self.get_pattern_statistics()
        return f"DemographicsPatterns({stats['total_question_types']} types from central memory)"
    
    def __repr__(self) -> str:
        """Detailed representation of patterns"""
        return f"DemographicsPatterns(question_types={list(self._processed_patterns.keys())}, source='knowledge_base.json')"