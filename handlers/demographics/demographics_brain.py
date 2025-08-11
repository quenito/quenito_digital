# handlers/demographics/brain.py
"""Demographics Brain - Detection and classification logic"""

from typing import Dict, Optional

class DemographicsBrain:
    """Brain for demographic questions - ONLY handles personal questions"""
    
    @staticmethod
    def is_demographics_question(question_text: str) -> bool:
        """Check if this is REALLY a demographics question about the user"""
        
        text_lower = question_text.lower()
        
        # Must be asking about the USER personally
        personal_indicators = [
            'your age', 'your gender', 'your income',
            'how old are you', 'are you male', 'are you female',
            'what is your', "what's your",
            'please select your', 'please indicate your',
            'year were you born', 'your birth',
            'your postcode', 'your occupation'
        ]
        
        # Check for personal questions
        is_personal = any(phrase in text_lower for phrase in personal_indicators)
        
        # Make sure it's NOT about brands/others
        third_party_indicators = [
            'brands', 'companies', 'for children', 
            'for teenagers', 'platforms', 'websites',
            'committed to', 'supports', 'improving',
            'safety', 'online environment'
        ]
        
        is_about_others = any(phrase in text_lower for phrase in third_party_indicators)
        
        # Only return True if it's personal AND not about others
        return is_personal and not is_about_others
    
    @staticmethod
    def classify_demographic_type(question_text: str) -> str:
        """Classify the specific type of demographic question"""
        
        text_lower = question_text.lower()
        
        # Only classify if it's actually about the user
        if not DemographicsBrain.is_demographics_question(question_text):
            return 'not_demographics'
        
        # Now classify the specific type
        if any(phrase in text_lower for phrase in ['your age', 'how old are you', 'birth year', 'year were you born']):
            return 'age'
        elif any(phrase in text_lower for phrase in ['your gender', 'are you male', 'are you female']):
            return 'gender'
        elif 'postcode' in text_lower or 'zip' in text_lower or 'postal code' in text_lower:
            return 'postcode'
        elif 'income' in text_lower and ('your' in text_lower or 'household' in text_lower):
            return 'income'
        elif any(word in text_lower for word in ['occupation', 'employment', 'work']) and 'your' in text_lower:
            return 'occupation'
        elif any(word in text_lower for word in ['education', 'degree', 'qualification']) and 'your' in text_lower:
            return 'education'
        elif any(word in text_lower for word in ['marital', 'married', 'single']) and 'your' in text_lower:
            return 'marital_status'
        elif 'state' in text_lower or 'region' in text_lower:
            return 'location'
        
        return 'unknown_demographic'
    
    @staticmethod
    def get_confidence_boost(question_text: str) -> float:
        """Get confidence boost based on how clear the question is"""
        
        text_lower = question_text.lower()
        
        # Very clear personal questions get a boost
        very_clear_patterns = [
            'what is your age',
            'please enter your age',
            'what is your gender',
            'are you male or female',
            'what is your postcode',
            'please enter your postcode'
        ]
        
        if any(pattern in text_lower for pattern in very_clear_patterns):
            return 0.1  # 10% boost
        
        # Questions with "your" get a small boost
        if 'your' in text_lower:
            return 0.05  # 5% boost
        
        return 0.0  # No boost
    
    @staticmethod
    def validate_response(question_type: str, response_value: str) -> bool:
        """Validate that the response makes sense for the question type"""
        
        if not response_value:
            return False
        
        if question_type == 'age':
            # Check if it's a valid age or age range
            if response_value.isdigit():
                age = int(response_value)
                return 18 <= age <= 100
            elif '-' in response_value:
                # Age range like "25-34"
                return any(r in response_value for r in ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
            
        elif question_type == 'gender':
            # Valid gender options
            return response_value.lower() in ['male', 'female', 'other', 'prefer not to say']
        
        elif question_type == 'postcode':
            # Australian postcodes are 4 digits
            return response_value.isdigit() and len(response_value) == 4
        
        elif question_type == 'income':
            # Should contain dollar sign or numbers
            return '$' in response_value or 'prefer not' in response_value.lower()
        
        # Default - assume valid
        return True
    
    @staticmethod
    def should_skip_question(question_text: str) -> bool:
        """Determine if demographics handler should skip this question entirely"""
        
        text_lower = question_text.lower()
        
        # Definitely skip these
        skip_patterns = [
            'which brands',
            'which companies',
            'which platforms',
            'for children and teenagers',
            'committed to improving',
            'supports a safe',
            'online environment',
            'social media platforms'
        ]
        
        return any(pattern in text_lower for pattern in skip_patterns)