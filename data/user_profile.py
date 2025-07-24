#!/usr/bin/env python3
"""
User Profile Module - Clean demographic data management
Extracted from knowledge_base.py for better modularity and maintainability.

This module handles:
- User demographic data storage and retrieval
- Profile validation and formatting
- Response mappings for different survey formats
- Location and demographic response standardization
"""

from typing import Dict, Any, Optional, List
import time


class UserProfile:
    """
    Clean user profile management with zero dependencies.
    Handles all user demographic data, validation, and response formatting.
    """
    
    def __init__(self, user_data: Optional[Dict[str, Any]] = None):
        """
        Initialize with user profile data from knowledge_base.json
        NO static defaults - all data comes from Quenito's central memory
        """
        self.data = user_data or {}
        print(f"🧠 UserProfile initialized with {len(self.data)} profile fields from knowledge_base.json")
    
    # ========================================
    # CORE USER DATA ACCESS
    # ========================================
    
    def get_response(self, question_type: str) -> Optional[str]:
        """Get user response for a specific question type"""
        response = self.data.get(question_type)
        if response:
            print(f"🧠 Retrieved {question_type}: {response}")
            return str(response)
        else:
            print(f"⚠️ No {question_type} found in user profile")
            return None
    
    def get_age(self) -> Optional[str]:
        """Get user age"""
        return self.get_response('age')
    
    def get_gender(self) -> Optional[str]:
        """Get user gender"""
        return self.get_response('gender')
    
    def get_location(self) -> Optional[str]:
        """Get user location"""
        return self.get_response('location')
    
    def get_occupation(self) -> Optional[str]:
        """Get user occupation"""
        return self.get_response('occupation')
    
    def get_education(self) -> Optional[str]:
        """Get user education level"""
        return self.get_response('education')
    
    def get_income(self) -> Optional[str]:
        """Get user personal income"""
        return self.get_response('personal_income')
    
    def get_household_income(self) -> Optional[str]:
        """Get user household income"""
        return self.get_response('household_income')
    
    def get_marital_status(self) -> Optional[str]:
        """Get user marital status"""
        return self.get_response('marital_status')
    
    def get_household_size(self) -> Optional[str]:
        """Get household size"""
        return self.get_response('household_size')
    
    def get_children(self) -> Optional[str]:
        """Get children status"""
        return self.get_response('children')
    
    def get_employment_status(self) -> Optional[str]:
        """Get employment status"""
        return self.get_response('employment_status')
    
    def get_industry(self) -> Optional[str]:
        """Get industry"""
        return self.get_response('industry')
    
    # ========================================
    # PROFILE VALIDATION & FORMATTING
    # ========================================
    
    def validate_profile(self) -> Dict[str, Any]:
        """Validate user profile completeness"""
        required_fields = ['age', 'gender', 'location', 'occupation']
        validation_result = {
            'is_complete': True,
            'missing_fields': [],
            'completeness_score': 0.0
        }
        
        total_fields = len(self.data)
        complete_fields = 0
        
        for field in required_fields:
            if not self.data.get(field):
                validation_result['missing_fields'].append(field)
                validation_result['is_complete'] = False
        
        for field, value in self.data.items():
            if value and str(value).strip():
                complete_fields += 1
        
        validation_result['completeness_score'] = complete_fields / total_fields
        return validation_result
    
    def format_for_survey_platform(self, platform: str = 'surveymonkey') -> Dict[str, str]:
        """Format responses for specific survey platform requirements"""
        formatted = {}
        
        for field, value in self.data.items():
            if value:
                if platform == 'surveymonkey':
                    formatted[field] = self._format_surveymonkey_response(field, value)
                elif platform == 'typeform':
                    formatted[field] = self._format_typeform_response(field, value)
                else:
                    formatted[field] = str(value)
        
        return formatted
    
    def _format_surveymonkey_response(self, field: str, value: str) -> str:
        """Format response for SurveyMonkey platform"""
        # Handle specific SurveyMonkey formatting requirements
        if field == 'location' and value == 'New South Wales':
            return 'NSW'  # Common abbreviation
        elif field == 'gender' and value == 'Male':
            return 'Male'  # Exact match
        elif field == 'children' and value == 'Yes':
            return 'Yes'  # Boolean response
        else:
            return str(value)
    
    def _format_typeform_response(self, field: str, value: str) -> str:
        """Format response for Typeform platform"""
        # Handle Typeform-specific formatting
        return str(value).lower() if field == 'gender' else str(value)
    
    # ========================================
    # RESPONSE MAPPINGS & ALTERNATIVES
    # ========================================
    
    def get_response_alternatives(self, field: str) -> List[str]:
        """Get alternative response formats for a field"""
        value = self.data.get(field)
        if not value:
            return []
        
        alternatives_map = {
            'age': [str(value), f"{value} years old", f"age {value}"],
            'gender': self._get_gender_alternatives(value),
            'location': self._get_location_alternatives(value),
            'education': self._get_education_alternatives(value),
            'marital_status': self._get_marital_alternatives(value),
            'children': ['Yes', 'Have children', 'With children'] if value == 'Yes' else ['No', 'No children'],
            'household_size': [str(value), f"{value} people", f"household of {value}"]
        }
        
        return alternatives_map.get(field, [str(value)])
    
    def _get_gender_alternatives(self, gender: str) -> List[str]:
        """Get gender response alternatives"""
        if gender.lower() == 'male':
            return ['Male', 'M', 'Man', 'male']
        elif gender.lower() == 'female':
            return ['Female', 'F', 'Woman', 'female']
        else:
            return [str(gender)]
    
    def _get_location_alternatives(self, location: str) -> List[str]:
        """Get location response alternatives"""
        if location == 'New South Wales':
            return ['New South Wales', 'NSW', 'N.S.W.', 'New South Wales, Australia']
        else:
            return [str(location)]
    
    def _get_education_alternatives(self, education: str) -> List[str]:
        """Get education response alternatives"""
        if 'high school' in education.lower():
            return ['High school education', 'High school graduate', 'Year 12', 'High school']
        else:
            return [str(education)]
    
    def _get_marital_alternatives(self, status: str) -> List[str]:
        """Get marital status alternatives"""
        if 'married' in status.lower():
            return ['Married/civil partnership', 'Married', 'Civil partnership']
        else:
            return [str(status)]
    
    # ========================================
    # PROFILE MANAGEMENT
    # ========================================
    
    def update_field(self, field: str, value: str):
        """Update a specific profile field"""
        self.data[field] = value
        print(f"🧠 Updated {field}: {value}")
    
    def update_profile(self, updates: Dict[str, str]):
        """Update multiple profile fields"""
        for field, value in updates.items():
            self.update_field(field, value)
    
    def get_full_profile(self) -> Dict[str, Any]:
        """Get complete user profile"""
        return self.data.copy()
    
    def get_demographics_summary(self) -> str:
        """Get human-readable demographics summary"""
        age = self.get_age()
        gender = self.get_gender()
        location = self.get_location()
        occupation = self.get_occupation()
        
        return f"{age}-year-old {gender} {occupation} from {location}"
    
    def is_field_available(self, field: str) -> bool:
        """Check if a profile field has data"""
        value = self.data.get(field)
        return bool(value and str(value).strip())
    
    def get_available_fields(self) -> List[str]:
        """Get list of fields with data"""
        return [field for field in self.data.keys() if self.is_field_available(field)]
    
    def get_missing_fields(self) -> List[str]:
        """Get list of fields without data"""
        all_fields = ['age', 'gender', 'location', 'occupation', 'education', 
                     'income', 'marital_status', 'household_size', 'children']
        return [field for field in all_fields if not self.is_field_available(field)]


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def create_user_profile(profile_data: Optional[Dict[str, Any]] = None) -> UserProfile:
    """Factory function to create UserProfile instance"""
    return UserProfile(profile_data)

def get_quenito_profile() -> UserProfile:
    """
    Get Quenito's profile - requires knowledge_base.json to be loaded first
    This should only be used for testing - normally called via KnowledgeBase
    """
    print("⚠️ get_quenito_profile() requires knowledge_base.json - use KnowledgeBase.user_profile instead")
    return UserProfile({})


# ========================================
# MODULE TEST
# ========================================

if __name__ == "__main__":
    # Quick module test with sample data (normally comes from knowledge_base.json)
    print("🧠 User Profile Module Test")
    
    # Test with empty profile (normal case when no JSON data)
    empty_profile = UserProfile({})
    print(f"Empty profile fields: {len(empty_profile.data)}")
    
    # Test with sample data (simulating data from knowledge_base.json)
    sample_data = {
        "age": "45",
        "gender": "Male", 
        "location": "New South Wales",
        "occupation": "Data Analyst"
    }
    profile = UserProfile(sample_data)
    print(f"Age: {profile.get_age()}")
    print(f"Gender: {profile.get_gender()}")
    print(f"Location: {profile.get_location()}")
    print(f"Summary: {profile.get_demographics_summary()}")
    print(f"Validation: {profile.validate_profile()}")
    print("✅ User Profile Module working correctly!")