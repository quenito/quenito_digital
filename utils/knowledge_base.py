"""
Knowledge Base Module
Handles loading, saving, and accessing the survey automation knowledge base.
"""

import json
import os
from typing import Dict, Any, List, Optional


class KnowledgeBase:
    """
    Manages the survey automation knowledge base with user preferences,
    question patterns, and response strategies.
    """
    
    def __init__(self, knowledge_base_path="data/enhanced_myopinions_knowledge_base.json"):
        self.path = knowledge_base_path
        self.data = {}
        self.load()
    
    def load(self):
        """Load the knowledge base from JSON file."""
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                print("✅ Knowledge base loaded successfully")
                print(f"📊 Loaded patterns for: {list(self.data.get('question_patterns', {}).keys())}")
            else:
                print(f"⚠️ Knowledge base file not found: {self.path}")
                print("🔧 Creating minimal fallback knowledge base")
                self._create_fallback_knowledge_base()
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            print("🔧 Creating minimal fallback knowledge base")
            self._create_fallback_knowledge_base()
    
    def save(self):
        """Save the knowledge base back to the JSON file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            print("💾 Knowledge base updated and saved")
            return True
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get a value from the knowledge base."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a value in the knowledge base."""
        self.data[key] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple values in the knowledge base."""
        self.data.update(updates)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get the complete user profile."""
        return self.data.get("user_profile", {})
    
    def get_demographics(self) -> Dict[str, Any]:
        """Get user demographics."""
        return self.get_user_profile().get("demographics", {})
    
    def get_brand_preferences(self) -> Dict[str, Any]:
        """Get user brand preferences."""
        return self.get_user_profile().get("existing_brands", {})
    
    def get_interests(self) -> Dict[str, Any]:
        """Get user interests and preferences."""
        return self.get_user_profile().get("interests_and_preferences", {})
    
    def get_question_patterns(self) -> Dict[str, Any]:
        """Get question detection patterns."""
        return self.data.get("question_patterns", {})
    
    def get_question_pattern(self, pattern_name: str) -> Dict[str, Any]:
        """Get a specific question pattern."""
        patterns = self.get_question_patterns()
        return patterns.get(pattern_name, {})
    
    def get_automation_settings(self) -> Dict[str, Any]:
        """Get automation configuration settings."""
        return self.data.get("automation_settings", {})
    
    def get_research_patterns(self) -> Dict[str, Any]:
        """Get research configuration patterns."""
        return self.data.get("research_patterns", {})
    
    def add_research_result(self, query: str, results: List[Dict[str, Any]]):
        """Add research results to the cache."""
        if 'research_cache' not in self.data:
            self.data['research_cache'] = {}
        
        import time
        self.data['research_cache'][query] = {
            'results': results,
            'timestamp': time.time()
        }
    
    def get_research_result(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached research results."""
        cache = self.data.get('research_cache', {})
        result = cache.get(query)
        
        if result:
            import time
            # Check if result is less than 24 hours old
            if time.time() - result['timestamp'] < 86400:  # 24 hours
                return result['results']
        
        return None
    
    def get_known_brands(self, category: str = "currently_use") -> List[str]:
        """Get list of known brands for a category."""
        brands = self.get_brand_preferences()
        return brands.get(category, [])
    
    def get_user_interests_by_level(self, level: str) -> List[str]:
        """Get user interests by level (high, medium, low)."""
        interests = self.get_interests()
        return interests.get(f"{level}_interest", [])
    
    def get_location_mappings(self) -> Dict[str, List[str]]:
        """Get location format mappings for different survey platforms."""
        demographics_patterns = self.get_question_pattern("demographics_questions")
        location_questions = demographics_patterns.get("location_questions", {})
        return location_questions.get("location_mappings", {})
    
    def get_activity_patterns(self) -> Dict[str, Any]:
        """Get activity likelihood patterns for recency questions."""
        recency_patterns = self.get_question_pattern("recency_activities_questions")
        return recency_patterns.get("activity_patterns", {})
    
    def get_brand_familiarity_levels(self) -> Dict[str, List[str]]:
        """Get brand familiarity response mappings."""
        brand_patterns = self.get_question_pattern("brand_familiarity_questions")
        return brand_patterns.get("response_levels", {})
    
    def add_used_brand(self, brand: str):
        """Track used brands to avoid repetition."""
        if 'used_brands' not in self.data:
            self.data['used_brands'] = []
        
        if brand not in self.data['used_brands']:
            self.data['used_brands'].append(brand)
    
    def get_used_brands(self) -> List[str]:
        """Get list of brands already used in current session."""
        return self.data.get('used_brands', [])
    
    def clear_used_brands(self):
        """Clear the used brands list (for new survey sessions)."""
        self.data['used_brands'] = []
    
    def update_user_profile(self, updates: Dict[str, Any]):
        """Update user profile with new information."""
        if 'user_profile' not in self.data:
            self.data['user_profile'] = {}
        
        self.data['user_profile'].update(updates)
    
    def add_question_pattern(self, pattern_name: str, pattern_data: Dict[str, Any]):
        """Add a new question pattern to the knowledge base."""
        if 'question_patterns' not in self.data:
            self.data['question_patterns'] = {}
        
        self.data['question_patterns'][pattern_name] = pattern_data
    
    def get_fallback_brands(self, category: str) -> List[str]:
        """Get fallback brand lists for research failures."""
        brand_patterns = self.get_question_pattern("brand_naming_questions")
        product_categories = brand_patterns.get("product_categories", {})
        category_data = product_categories.get(category, {})
        return category_data.get("fallback_brands", [])
    
    def get_research_query_for_category(self, category: str) -> str:
        """Get research query template for a product category."""
        brand_patterns = self.get_question_pattern("brand_naming_questions")
        product_categories = brand_patterns.get("product_categories", {})
        category_data = product_categories.get(category, {})
        return category_data.get("research_query", "")
    
    def get_confirmed_survey_domains(self) -> List[str]:
        """Get list of confirmed survey domains."""
        automation_settings = self.get_automation_settings()
        return automation_settings.get("confirmed_survey_domains", [
            "yoursurveynow.com",
            "qualtrics.com", 
            "decipherinc.com",
            "surveycmix.com"
        ])
    
    def get_selection_limits(self) -> Dict[str, int]:
        """Get selection limits for various question types."""
        automation_settings = self.get_automation_settings()
        return automation_settings.get("selection_limits", {
            "multi_select_max": 5,
            "brand_personality_max": 3,
            "interests_max": 8
        })
    
    def get_delay_settings(self) -> Dict[str, str]:
        """Get human-like delay settings."""
        automation_settings = self.get_automation_settings()
        return automation_settings.get("delays", {
            "between_actions": "1500-4000ms",
            "after_research": "2000-3000ms",
            "page_load": "2000-3000ms",
            "checkbox_selection": "300-700ms",
            "matrix_navigation": "200-500ms"
        })
    
    def _create_fallback_knowledge_base(self):
        """Create a minimal fallback knowledge base."""
        self.data = {
            "user_profile": {
                "demographics": {
                    "age": "45",
                    "birth_year": "1980",
                    "gender": "Male",
                    "location": "New South Wales",
                    "postcode": "2217",
                    "household_size": "4",
                    "marital_status": "Married",
                    "employment_status": "Full-time",
                    "education": "High school"
                },
                "existing_brands": {
                    "currently_use": [
                        "Netflix", "Spotify", "Commonwealth Bank", "Toyota", "Telstra"
                    ],
                    "familiar_with": [
                        "Samsung", "LG", "Sony", "Westpac", "ANZ"
                    ]
                },
                "interests_and_preferences": {
                    "high_interest": ["technology", "news", "finance"],
                    "medium_interest": ["sports", "music", "travel"],
                    "low_interest": ["fashion", "celebrities"]
                }
            },
            "question_patterns": {},
            "automation_settings": {
                "confirmed_survey_domains": [
                    "yoursurveynow.com",
                    "qualtrics.com",
                    "decipherinc.com", 
                    "surveycmix.com"
                ]
            }
        }
        print("🔧 Fallback knowledge base created")
    
    def print_summary(self):
        """Print a summary of the knowledge base contents."""
        print(f"\n📊 KNOWLEDGE BASE SUMMARY:")
        print(f"   File: {self.path}")
        print(f"   User Profile: {'✅' if 'user_profile' in self.data else '❌'}")
        print(f"   Question Patterns: {len(self.data.get('question_patterns', {}))}")
        print(f"   Research Cache: {len(self.data.get('research_cache', {}))}")
        print(f"   Used Brands: {len(self.data.get('used_brands', []))}")
        
        demographics = self.get_demographics()
        if demographics:
            print(f"   Demographics: Age {demographics.get('age', 'N/A')}, "
                  f"Gender {demographics.get('gender', 'N/A')}, "
                  f"Location {demographics.get('location', 'N/A')}")
        
        brands = self.get_brand_preferences()
        if brands:
            currently_use = len(brands.get('currently_use', []))
            familiar_with = len(brands.get('familiar_with', []))
            print(f"   Brands: {currently_use} currently use, {familiar_with} familiar with")
