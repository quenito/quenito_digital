# handlers/demographics/demographics_handler.py
"""Demographics Handler - Enhanced for better pattern recognition"""

from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class HandlerResponse:
    response_value: str
    response_type: str
    confidence: float
    success: bool = True  # Add success field
    handler_name: str = "demographics"  # Add handler name

class DemographicsHandler:
    """Handler for PERSONAL demographic questions only"""
    
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
    
    def calculate_confidence(self, question_type: str, question_text: str) -> float:
        """Calculate confidence for handling this question - ENHANCED"""
        
        text_lower = question_text.lower()
        
        # First, check for third-party questions that we should NOT handle
        third_party_indicators = [
            'brands', 'companies', 'platforms', 'websites',
            'for children', 'for teenagers', 'for kids',
            'committed to', 'supports', 'improving', 'safety'
        ]
        
        is_about_others = any(indicator in text_lower for indicator in third_party_indicators)
        
        # If it's about brands/companies, NOT a demographics question
        if is_about_others:
            print(f"   ⚠️ Demographics: Detected third-party question, confidence = 0")
            return 0.0
        
        # ENHANCED: Special check for "Are you?" gender questions
        if 'are you?' in text_lower and 'please select one option only' in text_lower:
            # This is likely a gender question with Male/Female options
            print(f"   🎯 Demographics: 'Are you?' pattern detected")
            return 0.9
        
        # Check if page mentions Male/Female (strong gender indicator)
        if 'male' in text_lower and 'female' in text_lower and not is_about_others:
            print(f"   🎯 Demographics: Male/Female options detected")
            return 0.85
        
        # ENHANCED: Check for state/territory questions
        state_names = [
            'new south wales', 'victoria', 'queensland',
            'western australia', 'south australia', 'tasmania',
            'australian capital territory', 'northern territory',
            'nsw', 'vic', 'qld', 'wa', 'sa', 'tas', 'act', 'nt'
        ]
        
        if any(state in text_lower for state in state_names):
            print(f"   🎯 Demographics: Australian state options detected")
            return 0.85
        
        # ENHANCED: Age range detection - IMPROVED
        age_range_patterns = [
            r'\d{2}-\d{2}',  # 45-54
            r'\d{2}\s*to\s*\d{2}',  # 45 to 54
            r'\d{2}\s*-\s*\d{2}',  # 45 - 54
            r'under\s*\d{2}',  # under 18
            r'\d{2}\+',  # 65+
            r'over\s*\d{2}'  # over 65
        ]
        
        has_age_ranges = any(re.search(pattern, text_lower) for pattern in age_range_patterns)
        # ENHANCED: Check for more age-related keywords
        if has_age_ranges and ('age' in text_lower or 'old' in text_lower or 'year' in text_lower or 'born' in text_lower):
            print(f"   🎯 Demographics: Age range pattern detected")
            return 0.9
        
        # Personal indicators
        personal_indicators = [
            'your', 'you', 'are you', 'do you', 
            'please select', 'please indicate', 'please tell',
            'i am', "what's your", 'what is your'
        ]
        
        is_personal_question = any(indicator in text_lower for indicator in personal_indicators)
        
        if not is_personal_question:
            return 0.3  # Low confidence
        
        # Specific demographic patterns
        if question_type == 'age' or 'age' in text_lower:
            if any(phrase in text_lower for phrase in ['your age', 'how old are you', 'birth year', 'born', 'age group', 'which age']):
                return 0.85
                
        elif question_type == 'gender' or 'gender' in text_lower:
            if any(phrase in text_lower for phrase in ['your gender', 'are you', 'you identify']):
                return 0.85
                
        elif question_type == 'postcode' or any(word in text_lower for word in ['postcode', 'postal', 'zip']):
            return 0.9
            
        elif question_type == 'state' or 'state' in text_lower or 'territory' in text_lower:
            return 0.85
            
        elif question_type == 'income' or 'income' in text_lower:
            if 'your' in text_lower or 'household' in text_lower:
                return 0.8
                
        # Default confidence for other demographic types
        return 0.65
    
    def handle(self, question_text: str, element_type: str = None) -> HandlerResponse:
        """Generate appropriate demographic response - ENHANCED"""
        
        text_lower = question_text.lower()
        
        # DOUBLE-CHECK this is really asking about personal info
        third_party_indicators = [
            'brands', 'companies', 'platforms', 
            'for children', 'for teenagers',
            'committed to', 'supports', 'safety'
        ]
        
        if any(indicator in text_lower for indicator in third_party_indicators):
            print(f"   ❌ Demographics handler: Not a personal question, skipping")
            return HandlerResponse(
                response_value='',
                response_type='skip',
                confidence=0.0,
                success=False
            )
        
        # Get user profile data - FIXED METHOD NAMES!
        user_age = self.kb.user_profile.get_response("age") if self.kb else "45"
        user_gender = self.kb.user_profile.get_response("gender") if self.kb else "Male"
        user_postcode = self.kb.user_profile.get_response("postcode") if self.kb else "2000"
        user_state = self.kb.user_profile.get_response("state") if self.kb else "NSW"
        
        # Try to get income - might be under different keys
        user_income = None
        if self.kb:
            user_income = (self.kb.user_profile.get_response("income") or 
                          self.kb.user_profile.get_response("personal_income") or
                          self.kb.user_profile.get_response("household_income") or
                          "$50,000 - $74,999")
        else:
            user_income = "$50,000 - $74,999"
        
        # ENHANCED: "Are you?" gender question
        if 'are you?' in text_lower and ('male' in text_lower or 'female' in text_lower):
            return HandlerResponse(
                response_value=user_gender,
                response_type='radio',
                confidence=0.9,
                success=True
            )
        
        # Age handling - ENHANCED for dynamic ranges with MORE phrases
        elif any(phrase in text_lower for phrase in ['your age', 'how old are you', 'birth year', 'age group', 'which age', 'what age', 'age are you', 'what is your age']):
            if element_type == 'text' or element_type == 'number':
                # Direct age input
                return HandlerResponse(
                    response_value=str(user_age),
                    response_type='text',
                    confidence=0.85,
                    success=True
                )
            elif element_type == 'radio':
                # Age range selection - Special type to indicate dynamic range handling needed
                return HandlerResponse(
                    response_value=str(user_age),  # Pass actual age, not hardcoded range
                    response_type='radio_age_range',  # SPECIAL TYPE for age ranges
                    confidence=0.85,
                    success=True
                )
            elif element_type == 'select':
                # Age dropdown (less common but possible)
                return HandlerResponse(
                    response_value=str(user_age),
                    response_type='select_age_range',  # SPECIAL TYPE for age dropdowns
                    confidence=0.85,
                    success=True
                )
            else:
                # Default to radio if element type unknown but age question detected
                return HandlerResponse(
                    response_value=str(user_age),
                    response_type='radio_age_range',
                    confidence=0.75,
                    success=True
                )
        
        # Gender handling  
        elif any(phrase in text_lower for phrase in ['your gender', 'male or female', 'gender identity']):
            return HandlerResponse(
                response_value=user_gender,
                response_type='radio',
                confidence=0.85,
                success=True
            )
        
        # State/Territory handling
        elif 'state' in text_lower or 'territory' in text_lower or 'where do you live' in text_lower:
            return HandlerResponse(
                response_value=user_state,
                response_type='select',
                confidence=0.85,
                success=True
            )
        
        # Postcode
        elif 'postcode' in text_lower or 'postal' in text_lower or 'zip' in text_lower:
            return HandlerResponse(
                response_value=user_postcode,
                response_type='text',
                confidence=0.9,
                success=True
            )
        
        # Income
        elif 'income' in text_lower and ('your' in text_lower or 'household' in text_lower or 'earn' in text_lower):
            return HandlerResponse(
                response_value=user_income,
                response_type='radio',
                confidence=0.8,
                success=True
            )
        
        # If we get here, we're not confident about handling this
        return HandlerResponse(
            response_value='',
            response_type='unknown',
            confidence=0.0,
            success=False
        )
    
    # Add this method for consistency with other handlers
    def can_handle(self, page_content: str) -> float:
        """Alias for calculate_confidence for consistency"""
        # Try to extract question type from content
        content_lower = page_content.lower()
        
        if 'age' in content_lower or 'old' in content_lower or 'year' in content_lower:
            question_type = 'age'
        elif 'gender' in content_lower or ('male' in content_lower and 'female' in content_lower):
            question_type = 'gender'
        elif 'postcode' in content_lower or 'zip' in content_lower:
            question_type = 'postcode'
        elif 'state' in content_lower or 'territory' in content_lower:
            question_type = 'state'
        elif 'income' in content_lower or 'salary' in content_lower or 'earn' in content_lower:
            question_type = 'income'
        else:
            question_type = 'general'
        
        return self.calculate_confidence(question_type, page_content)