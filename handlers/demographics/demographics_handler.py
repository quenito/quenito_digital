# handlers/demographics/handler.py
"""Demographics Handler - Fixed to avoid brand questions"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class HandlerResponse:
    response_value: str
    response_type: str
    confidence: float

class DemographicsHandler:
    """Handler for PERSONAL demographic questions only"""
    
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
    
    def calculate_confidence(self, question_type: str, question_text: str) -> float:
        """Calculate confidence for handling this question"""
        
        text_lower = question_text.lower()
        
        # VERIFY this is actually asking about PERSONAL demographics
        # Not just mentioning age/gender/etc in another context
        
        personal_indicators = [
            'your', 'you', 'are you', 'do you', 
            'please select', 'please indicate', 'please tell',
            'i am', "what's your", 'what is your'
        ]
        
        # Check if this is actually asking about the USER
        is_personal_question = any(indicator in text_lower for indicator in personal_indicators)
        
        # Also check for third-party questions that we should NOT handle
        third_party_indicators = [
            'brands', 'companies', 'platforms', 'websites',
            'for children', 'for teenagers', 'for kids',
            'committed to', 'supports', 'improving', 'safety'
        ]
        
        is_about_others = any(indicator in text_lower for indicator in third_party_indicators)
        
        # If it's about brands/companies, NOT a demographics question
        if is_about_others:
            print(f"   ⚠️ Demographics: Detected third-party question, confidence = 0")
            return 0.0  # Don't handle this!
        
        # If it's not clearly personal, lower confidence
        if not is_personal_question:
            return 0.3  # Low confidence
        
        # Now check for specific demographic patterns
        if question_type == 'age':
            # Must be asking for YOUR age specifically
            if any(phrase in text_lower for phrase in ['your age', 'how old are you', 'birth year', 'born']):
                return 0.85
            else:
                return 0.2  # Probably not an age question
                
        elif question_type == 'gender':
            # Must be asking for YOUR gender
            if any(phrase in text_lower for phrase in ['your gender', 'are you', 'you identify']):
                return 0.85
            else:
                return 0.2
                
        elif question_type == 'postcode':
            # Clear postcode question
            if any(word in text_lower for word in ['postcode', 'postal', 'zip']):
                return 0.9
                
        elif question_type == 'income':
            # Personal income question
            if 'your' in text_lower or 'household' in text_lower:
                return 0.8
            else:
                return 0.3
                
        # Default confidence for other demographic types
        return 0.65
    
    def handle(self, question_text: str, element_type: str = None) -> HandlerResponse:
        """Generate appropriate demographic response"""
        
        text_lower = question_text.lower()
        
        # DOUBLE-CHECK this is really asking about personal info
        third_party_indicators = [
            'brands', 'companies', 'platforms', 
            'for children', 'for teenagers',
            'committed to', 'supports', 'safety'
        ]
        
        if any(indicator in text_lower for indicator in third_party_indicators):
            # This is NOT a personal demographics question!
            print(f"   ❌ Demographics handler: Not a personal question, skipping")
            return HandlerResponse(
                response_value='',
                response_type='skip',
                confidence=0.0
            )
        
        # Age handling
        if any(phrase in text_lower for phrase in ['your age', 'how old are you', 'birth year']):
            if element_type == 'text':
                return HandlerResponse(
                    response_value='35',
                    response_type='text',
                    confidence=0.85
                )
            elif element_type == 'radio':
                # Age ranges
                return HandlerResponse(
                    response_value='35-44',
                    response_type='radio',
                    confidence=0.85
                )
        
        # Gender handling  
        elif any(phrase in text_lower for phrase in ['your gender', 'are you male or female']):
            return HandlerResponse(
                response_value='Male',
                response_type='radio',
                confidence=0.85
            )
        
        # Postcode
        elif 'postcode' in text_lower or 'postal' in text_lower:
            return HandlerResponse(
                response_value='2000',
                response_type='text',
                confidence=0.9
            )
        
        # Income
        elif 'income' in text_lower and ('your' in text_lower or 'household' in text_lower):
            return HandlerResponse(
                response_value='$50,000 - $74,999',
                response_type='radio',
                confidence=0.8
            )
        
        # If we get here, we're not confident about handling this
        return HandlerResponse(
            response_value='',
            response_type='unknown',
            confidence=0.0
        )