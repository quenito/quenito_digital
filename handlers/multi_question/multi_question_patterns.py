"""Pattern management for multi-question responses"""

from typing import Dict, Any, Optional
import random

class MultiQuestionPatterns:
    """Manages response patterns for different question categories"""
    
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
        self._init_default_patterns()
    
    def _init_default_patterns(self):
        """Initialize default response patterns"""
        
        self.default_patterns = {
            # Demographics
            'gender': ['Male', 'Female'],
            'birth_year': ['1980', '1985', '1990', '1995'],
            'sexuality': ['Heterosexual', 'Prefer not to say'],
            'country': ['Australia'],
            'state': ['NSW', 'New South Wales', 'VIC', 'Victoria'],
            'postcode': ['2000', '2010', '2317', '3000'],
            
            # Education/Work
            'education': ['Bachelor degree', 'High school', 'Diploma'],
            'income': ['$50,000 - $74,999', 'Prefer not to say'],
            'employment': ['Full-time', 'Part-time', 'Self-employed'],
            
            # Default
            'unknown': ['']
        }
    
    def get_response_for_category(self, category: str) -> str:
        """Get appropriate response for question category"""
        
        # First check learned patterns from knowledge base
        if self.kb and hasattr(self.kb, 'data'):
            learned = self._get_learned_response(category)
            if learned:
                return learned
        
        # Use default patterns
        if category in self.default_patterns:
            options = self.default_patterns[category]
            # For now, return first option (can randomize later)
            return options[0] if options else ''
        
        return ''
    
    def _get_learned_response(self, category: str) -> Optional[str]:
        """Get learned response from knowledge base"""
        
        if not self.kb:
            return None
        
        # Check detailed_intervention_learning for this category
        learning_data = self.kb.data.get('detailed_intervention_learning', {})
        
        for key, entry in learning_data.items():
            if entry.get('question_type') == category:
                response = entry.get('response_value')
                if response:
                    return response
        
        return None
    
    def update_pattern(self, category: str, value: str, success: bool):
        """Update patterns based on automation results"""
        
        if not self.kb:
            return
        
        # Store successful patterns
        if success:
            if 'multi_question_patterns' not in self.kb.data:
                self.kb.data['multi_question_patterns'] = {}
            
            if category not in self.kb.data['multi_question_patterns']:
                self.kb.data['multi_question_patterns'][category] = []
            
            if value not in self.kb.data['multi_question_patterns'][category]:
                self.kb.data['multi_question_patterns'][category].append(value)
            
            self.kb.save()