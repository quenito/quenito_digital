"""
🧠 Enhanced Knowledge Base with Digital Brain Integration v2.0
Handles loading, saving, and accessing the survey automation knowledge base.
NOW WITH BRAIN LEARNING CAPABILITIES - Quenito gets smarter with every interaction!

New Digital Brain Features:
- ✅ Auto-Learning from interventions  
- ✅ Pattern recognition improvement
- ✅ Confidence calibration evolution
- ✅ Handler performance tracking
- ✅ Question mapping expansion
- ✅ Success pattern storage
"""

import json
import os
import time
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path


class KnowledgeBase:
    """
    🧠 Enhanced Knowledge Base with Digital Brain Integration
    Manages the survey automation knowledge base with user preferences,
    question patterns, response strategies, AND LEARNING CAPABILITIES.
    
    The brain gets smarter with every interaction!
    """
    
    def __init__(self, knowledge_base_path="data/knowledge_base.json"):
        self.path = knowledge_base_path
        self.data = {}
        
        # 🧠 Brain learning tracking
        self.learning_session = {
            "session_id": f"brain_session_{int(time.time())}",
            "learning_events": [],
            "performance_improvements": [],
            "new_patterns_discovered": []
        }
        
        self.load()
        
        # Initialize brain learning structures if missing
        self._ensure_brain_structures()
    
    def load(self):
        """Load the knowledge base from JSON file."""
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                print("✅ Knowledge base loaded successfully")
                print(f"📊 Loaded patterns for: {list(self.data.get('question_patterns', {}).keys())}")
                
                # 🧠 Brain status report
                brain_data = self.data.get('brain_learning', {})
                total_interventions = len(brain_data.get('intervention_history', []))
                success_patterns = len(brain_data.get('success_patterns', {}))
                print(f"🧠 Brain Status: {total_interventions} interventions learned, {success_patterns} success patterns")
                
            else:
                print(f"⚠️ Knowledge base file not found: {self.path}")
                print("🔧 Creating minimal fallback knowledge base")
                self._create_fallback_knowledge_base()
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            print("🔧 Creating minimal fallback knowledge base")
            self._create_fallback_knowledge_base()
    
    def save(self):
        """Save the knowledge base back to the JSON file with brain learning data."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            
            # 🧠 Add current learning session data before saving
            if 'brain_learning' not in self.data:
                self.data['brain_learning'] = {}
            
            # Store learning session data
            self.data['brain_learning']['last_session'] = self.learning_session
            self.data['brain_learning']['last_updated'] = time.time()
            
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            print("💾 Knowledge base updated and saved")
            print(f"🧠 Brain learning data updated with {len(self.learning_session['learning_events'])} new events")
            return True
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
            return False
    
    # ========================================
    # 🧠 DIGITAL BRAIN LEARNING METHODS
    # ========================================
    
    def learn_from_intervention(self, question_text: str, answer_provided: str, 
                              question_type: str, selector_used: str, success: bool,
                              confidence_before: float, context: Dict[str, Any] = None):
        """
        🧠 BRAIN LEARNING: Learn from manual interventions
        This is how Quenito gets smarter!
        """
        intervention_data = {
            "timestamp": time.time(),
            "question_text": question_text.lower(),
            "answer_provided": answer_provided,
            "question_type": question_type,
            "selector_used": selector_used,
            "success": success,
            "confidence_before": confidence_before,
            "context": context or {}
        }
        
        # Store in brain learning
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'intervention_history' not in self.data['brain_learning']:
            self.data['brain_learning']['intervention_history'] = []
        
        self.data['brain_learning']['intervention_history'].append(intervention_data)
        
        # Add to current session
        self.learning_session['learning_events'].append(intervention_data)
        
        # 🧠 Extract learning patterns
        self._extract_learning_patterns(intervention_data)
        
        print(f"🧠 BRAIN LEARNED: '{question_text[:50]}...' -> '{answer_provided}' (Success: {success})")
        
    def learn_successful_pattern(self, question_text: str, successful_strategy: Dict[str, Any]):
        """
        🧠 BRAIN LEARNING: Store successful automation strategies
        """
        pattern_key = self._generate_pattern_key(question_text)
        
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'success_patterns' not in self.data['brain_learning']:
            self.data['brain_learning']['success_patterns'] = {}
        
        self.data['brain_learning']['success_patterns'][pattern_key] = {
            "timestamp": time.time(),
            "question_text": question_text,
            "strategy": successful_strategy,
            "usage_count": self.data['brain_learning']['success_patterns'].get(pattern_key, {}).get('usage_count', 0) + 1
        }
        
        print(f"🧠 SUCCESS PATTERN STORED: {pattern_key}")
    
    def get_learned_strategy(self, question_text: str) -> Optional[Dict[str, Any]]:
        """
        🧠 BRAIN RETRIEVAL: Get previously learned successful strategy
        """
        pattern_key = self._generate_pattern_key(question_text)
        success_patterns = self.data.get('brain_learning', {}).get('success_patterns', {})
        
        if pattern_key in success_patterns:
            strategy = success_patterns[pattern_key]
            print(f"🧠 BRAIN RECALL: Found learned strategy for '{question_text[:30]}...'")
            return strategy['strategy']
        
        return None
    
    def update_confidence_calibration(self, handler_type: str, question_pattern: str, 
                                    predicted_confidence: float, actual_success: bool):
        """
        🧠 BRAIN LEARNING: Calibrate confidence predictions based on actual results
        """
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'confidence_calibration' not in self.data['brain_learning']:
            self.data['brain_learning']['confidence_calibration'] = {}
        
        calibration_key = f"{handler_type}_{question_pattern}"
        
        if calibration_key not in self.data['brain_learning']['confidence_calibration']:
            self.data['brain_learning']['confidence_calibration'][calibration_key] = {
                "predictions": [],
                "accuracy_rate": 0.0,
                "recommended_threshold": 0.4
            }
        
        # Add new prediction result
        self.data['brain_learning']['confidence_calibration'][calibration_key]['predictions'].append({
            "predicted_confidence": predicted_confidence,
            "actual_success": actual_success,
            "timestamp": time.time()
        })
        
        # Recalculate accuracy and adjust threshold
        self._recalibrate_confidence_threshold(calibration_key)
        
        print(f"🧠 CONFIDENCE CALIBRATED: {calibration_key} -> Predicted: {predicted_confidence:.2f}, Success: {actual_success}")
    
    def get_recommended_confidence_threshold(self, handler_type: str, question_pattern: str = "general") -> float:
        """
        🧠 BRAIN INTELLIGENCE: Get learned confidence threshold for handler/pattern combination
        """
        calibration_key = f"{handler_type}_{question_pattern}"
        calibration_data = self.data.get('brain_learning', {}).get('confidence_calibration', {})
        
        if calibration_key in calibration_data:
            threshold = calibration_data[calibration_key]['recommended_threshold']
            print(f"🧠 BRAIN THRESHOLD: {calibration_key} -> {threshold:.2f}")
            return threshold
        
        # Fallback to default thresholds
        defaults = {
            "demographics": 0.4,
            "brand_familiarity": 0.5,
            "rating_matrix": 0.6,
            "multi_select": 0.4,
            "research": 0.3
        }
        
        return defaults.get(handler_type, 0.4)
    
    def add_discovered_question_pattern(self, question_text: str, question_type: str, 
                                      keywords_found: List[str], successful_response: str):
        """
        🧠 BRAIN EXPANSION: Add newly discovered question patterns
        """
        pattern_data = {
            "question_text": question_text,
            "question_type": question_type,
            "keywords": keywords_found,
            "successful_response": successful_response,
            "discovery_timestamp": time.time(),
            "usage_count": 1
        }
        
        # Determine pattern category
        category = self._categorize_question(question_text, keywords_found)
        
        if 'question_patterns' not in self.data:
            self.data['question_patterns'] = {}
        if category not in self.data['question_patterns']:
            self.data['question_patterns'][category] = {'discovered_patterns': []}
        if 'discovered_patterns' not in self.data['question_patterns'][category]:
            self.data['question_patterns'][category]['discovered_patterns'] = []
        
        self.data['question_patterns'][category]['discovered_patterns'].append(pattern_data)
        
        # Add to current session discoveries
        self.learning_session['new_patterns_discovered'].append(pattern_data)
        
        print(f"🧠 NEW PATTERN DISCOVERED: {category} -> '{question_text[:40]}...'")
    
    def get_handler_performance_history(self, handler_type: str) -> Dict[str, Any]:
        """
        🧠 BRAIN ANALYTICS: Get performance history for a handler
        """
        performance_data = self.data.get('brain_learning', {}).get('handler_performance', {})
        return performance_data.get(handler_type, {
            "total_attempts": 0,
            "successful_attempts": 0,
            "success_rate": 0.0,
            "average_confidence": 0.0,
            "improvement_trend": "stable"
        })
    
    def update_handler_performance(self, handler_type: str, confidence: float, success: bool):
        """
        🧠 BRAIN TRACKING: Update handler performance metrics
        """
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'handler_performance' not in self.data['brain_learning']:
            self.data['brain_learning']['handler_performance'] = {}
        
        if handler_type not in self.data['brain_learning']['handler_performance']:
            self.data['brain_learning']['handler_performance'][handler_type] = {
                "total_attempts": 0,
                "successful_attempts": 0,
                "success_rate": 0.0,
                "confidence_history": [],
                "average_confidence": 0.0,
                "improvement_trend": "stable",
                "last_updated": time.time()
            }
        
        perf = self.data['brain_learning']['handler_performance'][handler_type]
        
        # Update metrics
        perf['total_attempts'] += 1
        if success:
            perf['successful_attempts'] += 1
        
        perf['success_rate'] = perf['successful_attempts'] / perf['total_attempts']
        perf['confidence_history'].append(confidence)
        perf['average_confidence'] = sum(perf['confidence_history']) / len(perf['confidence_history'])
        perf['last_updated'] = time.time()
        
        # Calculate improvement trend
        if len(perf['confidence_history']) >= 5:
            recent = perf['confidence_history'][-5:]
            older = perf['confidence_history'][-10:-5] if len(perf['confidence_history']) >= 10 else perf['confidence_history'][:-5]
            
            if older:
                recent_avg = sum(recent) / len(recent)
                older_avg = sum(older) / len(older)
                
                if recent_avg > older_avg + 0.05:
                    perf['improvement_trend'] = "improving"
                elif recent_avg < older_avg - 0.05:
                    perf['improvement_trend'] = "declining"
                else:
                    perf['improvement_trend'] = "stable"
        
        print(f"🧠 PERFORMANCE UPDATED: {handler_type} -> {perf['success_rate']:.1%} success, trending {perf['improvement_trend']}")
    
    # ========================================
    # 🧠 BRAIN INTELLIGENCE HELPERS
    # ========================================
    
    def _ensure_brain_structures(self):
        """Ensure all brain learning structures exist"""
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        
        brain_defaults = {
            'intervention_history': [],
            'success_patterns': {},
            'confidence_calibration': {},
            'handler_performance': {},
            'pattern_evolution': {},
            'learning_metrics': {
                'total_interventions': 0,
                'automation_improvement_rate': 0.0,
                'last_learning_session': None
            }
        }
        
        for key, default in brain_defaults.items():
            if key not in self.data['brain_learning']:
                self.data['brain_learning'][key] = default
    
    def _extract_learning_patterns(self, intervention_data: Dict[str, Any]):
        """Extract patterns from intervention data for future learning"""
        question_text = intervention_data['question_text']
        answer = intervention_data['answer_provided']
        
        # Extract keywords that might be useful for future pattern matching
        important_keywords = []
        keywords_to_check = ['age', 'gender', 'male', 'female', 'location', 'state', 'income', 'employment']
        
        for keyword in keywords_to_check:
            if keyword in question_text:
                important_keywords.append(keyword)
        
        # Store pattern insights
        if important_keywords:
            pattern_insight = {
                "keywords": important_keywords,
                "successful_answer": answer,
                "question_length": len(question_text),
                "extraction_timestamp": time.time()
            }
            
            if 'pattern_insights' not in self.data['brain_learning']:
                self.data['brain_learning']['pattern_insights'] = []
            
            self.data['brain_learning']['pattern_insights'].append(pattern_insight)
    
    def _generate_pattern_key(self, question_text: str) -> str:
        """Generate a key for pattern matching"""
        # Simple pattern key based on important words
        important_words = ['age', 'gender', 'male', 'female', 'location', 'state', 'income', 'employment', 'work', 'household']
        found_words = [word for word in important_words if word in question_text.lower()]
        
        if found_words:
            return "_".join(sorted(found_words))
        else:
            # Fallback to length-based categorization
            if len(question_text) < 30:
                return "short_question"
            elif len(question_text) < 60:
                return "medium_question"
            else:
                return "long_question"
    
    def _categorize_question(self, question_text: str, keywords: List[str]) -> str:
        """Categorize discovered questions"""
        question_lower = question_text.lower()
        
        # Demographics patterns
        if any(word in question_lower for word in ['age', 'gender', 'male', 'female', 'location', 'state']):
            return "demographics_questions"
        
        # Brand patterns  
        if any(word in question_lower for word in ['brand', 'familiar', 'use', 'purchase', 'buy']):
            return "brand_familiarity_questions"
        
        # Rating patterns
        if any(word in question_lower for word in ['rate', 'rating', 'scale', 'agree', 'disagree']):
            return "rating_questions"
        
        # Default category
        return "general_questions"
    
    def _recalibrate_confidence_threshold(self, calibration_key: str):
        """Recalibrate confidence threshold based on prediction accuracy"""
        calibration_data = self.data['brain_learning']['confidence_calibration'][calibration_key]
        predictions = calibration_data['predictions']
        
        if len(predictions) >= 3:  # Need minimum data points
            # Calculate accuracy of high-confidence predictions
            high_conf_predictions = [p for p in predictions if p['predicted_confidence'] >= 0.6]
            
            if high_conf_predictions:
                accuracy = sum(1 for p in high_conf_predictions if p['actual_success']) / len(high_conf_predictions)
                calibration_data['accuracy_rate'] = accuracy
                
                # Adjust threshold based on accuracy
                if accuracy >= 0.9:  # Very accurate - can lower threshold
                    calibration_data['recommended_threshold'] = max(0.3, calibration_data['recommended_threshold'] - 0.1)
                elif accuracy < 0.7:  # Not accurate enough - raise threshold
                    calibration_data['recommended_threshold'] = min(0.8, calibration_data['recommended_threshold'] + 0.1)
    
    # ========================================
    # EXISTING METHODS (Enhanced)
    # ========================================
    
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
        
        self.data['research_cache'][query] = {
            'results': results,
            'timestamp': time.time()
        }
    
    def get_research_result(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached research results."""
        cache = self.data.get('research_cache', {})
        result = cache.get(query)
        
        if result:
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
        """Create a minimal fallback knowledge base with brain structures."""
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
            },
            # 🧠 Brain learning structures
            "brain_learning": {
                "intervention_history": [],
                "success_patterns": {},
                "confidence_calibration": {},
                "handler_performance": {},
                "pattern_evolution": {},
                "learning_metrics": {
                    "total_interventions": 0,
                    "automation_improvement_rate": 0.0,
                    "last_learning_session": None
                }
            }
        }
        print("🔧 Fallback knowledge base created with brain learning structures")
    
    def print_summary(self):
        """Print a comprehensive summary of the knowledge base including brain learning."""
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
        
        # 🧠 Brain learning summary
        brain_data = self.data.get('brain_learning', {})
        if brain_data:
            print(f"\n🧠 BRAIN LEARNING SUMMARY:")
            print(f"   Total Interventions: {len(brain_data.get('intervention_history', []))}")
            print(f"   Success Patterns: {len(brain_data.get('success_patterns', {}))}")
            print(f"   Confidence Calibrations: {len(brain_data.get('confidence_calibration', {}))}")
            print(f"   Handler Performance Tracking: {len(brain_data.get('handler_performance', {}))}")
            
            # Performance insights
            handler_perf = brain_data.get('handler_performance', {})
            if handler_perf:
                print(f"   🎯 Handler Success Rates:")
                for handler, perf in handler_perf.items():
                    success_rate = perf.get('success_rate', 0) * 100
                    trend = perf.get('improvement_trend', 'unknown')
                    print(f"      {handler}: {success_rate:.1f}% (trending {trend})")
            
            # Learning session info
            current_session = self.learning_session
            print(f"   📈 Current Session: {len(current_session['learning_events'])} events, "
                  f"{len(current_session['new_patterns_discovered'])} new patterns")
    
    def print_brain_intelligence_report(self):
        """
        🧠 Print detailed brain intelligence and learning report
        """
        print(f"\n🧠 ===============================================")
        print(f"🧠 QUENITO'S DIGITAL BRAIN INTELLIGENCE REPORT")
        print(f"🧠 ===============================================")
        
        brain_data = self.data.get('brain_learning', {})
        
        # Learning History Analysis
        interventions = brain_data.get('intervention_history', [])
        if interventions:
            print(f"\n📚 LEARNING HISTORY:")
            print(f"   Total Interventions: {len(interventions)}")
            
            # Success rate over time
            recent_interventions = interventions[-10:] if len(interventions) >= 10 else interventions
            success_rate = sum(1 for i in recent_interventions if i.get('success', False)) / len(recent_interventions) * 100
            print(f"   Recent Success Rate: {success_rate:.1f}%")
            
            # Most common question types
            question_types = {}
            for intervention in interventions:
                q_type = intervention.get('question_type', 'unknown')
                question_types[q_type] = question_types.get(q_type, 0) + 1
            
            if question_types:
                print(f"   Most Common Question Types:")
                for q_type, count in sorted(question_types.items(), key=lambda x: x[1], reverse=True)[:3]:
                    print(f"      {q_type}: {count} interventions")
        
        # Success Patterns Analysis
        success_patterns = brain_data.get('success_patterns', {})
        if success_patterns:
            print(f"\n🎯 SUCCESS PATTERNS STORED:")
            print(f"   Total Patterns: {len(success_patterns)}")
            
            # Most used patterns
            sorted_patterns = sorted(success_patterns.items(), 
                                   key=lambda x: x[1].get('usage_count', 0), reverse=True)
            
            print(f"   Most Used Patterns:")
            for pattern_key, pattern_data in sorted_patterns[:3]:
                usage = pattern_data.get('usage_count', 0)
                question = pattern_data.get('question_text', '')[:40]
                print(f"      {pattern_key}: {usage} uses - '{question}...'")
        
        # Confidence Calibration Analysis
        calibrations = brain_data.get('confidence_calibration', {})
        if calibrations:
            print(f"\n🎯 CONFIDENCE CALIBRATION:")
            for handler_pattern, cal_data in calibrations.items():
                accuracy = cal_data.get('accuracy_rate', 0) * 100
                threshold = cal_data.get('recommended_threshold', 0.4)
                predictions = len(cal_data.get('predictions', []))
                print(f"   {handler_pattern}: {accuracy:.1f}% accuracy, "
                      f"threshold: {threshold:.2f}, {predictions} predictions")
        
        # Handler Performance Analysis
        handler_perf = brain_data.get('handler_performance', {})
        if handler_perf:
            print(f"\n📊 HANDLER PERFORMANCE INTELLIGENCE:")
            for handler, perf in handler_perf.items():
                attempts = perf.get('total_attempts', 0)
                success_rate = perf.get('success_rate', 0) * 100
                avg_confidence = perf.get('average_confidence', 0)
                trend = perf.get('improvement_trend', 'unknown')
                
                print(f"   {handler}:")
                print(f"      Attempts: {attempts}, Success Rate: {success_rate:.1f}%")
                print(f"      Avg Confidence: {avg_confidence:.2f}, Trend: {trend}")
        
        # Learning Session Summary
        session = self.learning_session
        print(f"\n📈 CURRENT LEARNING SESSION:")
        print(f"   Session ID: {session['session_id']}")
        print(f"   Learning Events: {len(session['learning_events'])}")
        print(f"   New Patterns Discovered: {len(session['new_patterns_discovered'])}")
        print(f"   Performance Improvements: {len(session['performance_improvements'])}")
        
        # Brain Growth Potential
        print(f"\n🚀 BRAIN GROWTH POTENTIAL:")
        total_interventions = len(interventions)
        if total_interventions > 0:
            automation_potential = (len(success_patterns) / total_interventions) * 100
            print(f"   Automation Potential: {automation_potential:.1f}%")
            print(f"   Knowledge Coverage: {len(brain_data.get('question_patterns', {}))}/50 pattern types")
            
            # Growth recommendations
            if total_interventions < 10:
                print(f"   🎯 Recommendation: Need more learning data (current: {total_interventions})")
            elif len(success_patterns) < 5:
                print(f"   🎯 Recommendation: Focus on identifying success patterns")
            else:
                print(f"   🎯 Recommendation: Ready for advanced automation testing")
        
        print(f"\n🧠 ===============================================")
        print(f"🧠 END OF BRAIN INTELLIGENCE REPORT")
        print(f"🧠 ===============================================\n")
    
    def get_brain_learning_summary(self) -> Dict[str, Any]:
        """
        🧠 Get a structured summary of brain learning data for other components
        """
        brain_data = self.data.get('brain_learning', {})
        
        return {
            "total_interventions": len(brain_data.get('intervention_history', [])),
            "success_patterns_count": len(brain_data.get('success_patterns', {})),
            "calibrated_handlers": len(brain_data.get('confidence_calibration', {})),
            "tracked_handlers": len(brain_data.get('handler_performance', {})),
            "current_session_events": len(self.learning_session['learning_events']),
            "current_session_discoveries": len(self.learning_session['new_patterns_discovered']),
            "brain_intelligence_level": self._calculate_intelligence_level(),
            "automation_readiness": self._calculate_automation_readiness()
        }
    
    def _calculate_intelligence_level(self) -> str:
        """Calculate current brain intelligence level"""
        brain_data = self.data.get('brain_learning', {})
        
        interventions = len(brain_data.get('intervention_history', []))
        success_patterns = len(brain_data.get('success_patterns', {}))
        calibrations = len(brain_data.get('confidence_calibration', {}))
        
        # Calculate intelligence score
        score = 0
        if interventions >= 5:
            score += 25
        if interventions >= 20:
            score += 25
        if success_patterns >= 3:
            score += 25
        if calibrations >= 2:
            score += 25
        
        if score >= 75:
            return "Advanced"
        elif score >= 50:
            return "Intermediate"
        elif score >= 25:
            return "Learning"
        else:
            return "Beginner"
    
    def _calculate_automation_readiness(self) -> float:
        """Calculate automation readiness percentage"""
        brain_data = self.data.get('brain_learning', {})
        
        # Factors contributing to automation readiness
        interventions = len(brain_data.get('intervention_history', []))
        success_patterns = len(brain_data.get('success_patterns', {}))
        handler_performance = brain_data.get('handler_performance', {})
        
        readiness_score = 0.0
        
        # Learning data availability (40% weight)
        if interventions >= 10:
            readiness_score += 0.4
        elif interventions >= 5:
            readiness_score += 0.2
        
        # Success pattern coverage (30% weight)
        if success_patterns >= 5:
            readiness_score += 0.3
        elif success_patterns >= 2:
            readiness_score += 0.15
        
        # Handler performance (30% weight)
        if handler_performance:
            avg_success_rate = sum(perf.get('success_rate', 0) for perf in handler_performance.values()) / len(handler_performance)
            readiness_score += avg_success_rate * 0.3
        
        return min(readiness_score * 100, 100.0)  # Cap at 100%