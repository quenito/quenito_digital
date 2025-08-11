# handlers/multi_select/handler.py
"""Multi-Select Handler - Fixed to return text values not indices"""

from dataclasses import dataclass
from typing import Optional
import random

@dataclass
class HandlerResponse:
    response_value: str
    response_type: str
    confidence: float

class MultiSelectHandler:
    """Handler for multi-select/checkbox questions"""
    
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
        self.default_options = {
            'platforms': ['YouTube', 'Facebook', 'Instagram'],
            'safety': ['None of the above'],
            'activities': ['Watching TV', 'Reading', 'Shopping online'],
            'brands': ['Apple', 'Google', 'Microsoft'],
            'general': ['None of the above']
        }
    
    def calculate_confidence(self, question_type: str, question_text: str) -> float:
        """Calculate confidence for handling multi-select questions"""
        
        text_lower = question_text.lower()
        
        # High confidence for clear multi-select patterns
        if any(phrase in text_lower for phrase in [
            'which of the following',
            'select all',
            'select as many',
            'check all that apply'
        ]):
            return 0.8
        
        # Medium confidence for brand/platform questions
        if any(word in text_lower for word in ['brands', 'platforms', 'companies']):
            return 0.75
        
        # Lower confidence for general questions
        if question_type == 'multi_select':
            return 0.6
        
        return 0.4
    
    def handle(self, question_text: str, element_type: str = None) -> HandlerResponse:
        """Generate response for multi-select questions - RETURNS TEXT VALUES"""
        
        text_lower = question_text.lower()
        
        # IMPORTANT: For checkboxes, return actual text values not indices!
        if element_type == 'checkbox':
            
            # Determine category of question
            if 'safety' in text_lower or 'children' in text_lower or 'teenagers' in text_lower:
                # Safety/children questions - conservative approach
                response = 'None of the above'
                
            elif any(word in text_lower for word in ['platform', 'social media', 'youtube', 'tiktok']):
                # Platform questions - pick popular ones
                options = ['YouTube', 'Facebook']
                response = random.choice(options)
                
            elif 'brands' in text_lower:
                # Brand questions
                if 'committed' in text_lower or 'support' in text_lower:
                    response = 'None of the above'  # Conservative
                else:
                    options = ['Apple', 'Google', 'Microsoft']
                    response = random.choice(options)
                    
            elif 'activities' in text_lower or 'do you' in text_lower:
                # Activity questions
                options = ['Watching TV', 'Shopping online', 'Reading']
                response = random.choice(options)
                
            else:
                # Default - safe option
                response = 'None of the above'
            
            # RETURN TEXT VALUE, NOT NUMBER!
            return HandlerResponse(
                response_value=response,  # This is now "YouTube" not "1"
                response_type='checkbox',
                confidence=0.7
            )
        
        # For other element types (shouldn't happen for multi-select)
        return HandlerResponse(
            response_value='',
            response_type='unknown',
            confidence=0.0
        )
    
    def get_learned_responses(self, question_text: str) -> list:
        """Get previously learned responses for similar questions"""
        
        if not self.kb:
            return []
        
        # Check learning data for similar questions
        learning_data = self.kb.data.get('detailed_intervention_learning', {})
        similar_responses = []
        
        text_lower = question_text.lower()
        
        for key, entry in learning_data.items():
            if entry.get('question_type') == 'multi_select':
                learned_text = entry.get('question_text', '').lower()
                
                # Check for similarity
                if any(word in learned_text for word in text_lower.split()[:5]):
                    if entry.get('response_value'):
                        # Make sure we're getting text values, not numbers
                        value = entry['response_value']
                        if not value.isdigit():  # Only add if it's not a number
                            similar_responses.append(value)
        
        return similar_responses