#!/usr/bin/env python3
"""
🧠 Demographics Brain Module v2.0 - Learning & Intelligence Integration
Connects demographics handling to Quenito's central knowledge base.

This module manages:
- Learning from successful automations
- Retrieving learned responses and strategies
- Reporting successes/failures to knowledge base
- Getting user demographic data
- Applying intelligence to improve automation

ARCHITECTURE: Bridge between demographics handler and knowledge base
"""

import time
from typing import Dict, Any, Optional, List, Tuple


class DemographicsBrain:
    """
    🧠 Brain Integration for Demographics Questions
    
    Manages all learning and intelligence:
    - Retrieves learned responses from knowledge base
    - Applies successful strategies
    - Reports outcomes for continuous learning
    - Gets user profile data
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize brain integration with knowledge base
        
        Args:
            knowledge_base: Reference to Quenito's central knowledge base
        """
        self.brain = knowledge_base
        self.last_strategy_used = None
        self.last_question_type = None
        print("🧠 DemographicsBrain initialized with knowledge base connection")
    
    # ========================================
    # LEARNED RESPONSE RETRIEVAL
    # ========================================
    
    async def get_learned_response(self, question_type: str, content: str = "") -> Optional[Dict[str, Any]]:
        """
        🧠 FIXED: Get learned response from correct knowledge base structure
        
        Looks in the RIGHT places:
        1. demographics_questions[question_type]['responses'] - Basic stored responses
        2. detailed_intervention_learning - Successful automation records  
        3. user_profile - Fallback demographic values
        """
        try:
            print(f"🧠 Checking learned responses for {question_type}...")
            
            # ✅ METHOD 1: Check demographics_questions structure
            if self.brain:
                demographics_questions = self.brain.get("demographics_questions", {})
                question_data = demographics_questions.get(question_type, {})
                responses = question_data.get("responses", [])
                
                if responses:
                    # Use the first response as the primary learned response
                    response = responses[0]
                    print(f"🎯 Found stored response for {question_type}: '{response}'")
                    return {
                        'response': response,
                        'element_type': 'auto_detect',  # Will auto-detect element type
                        'learned_from': 'demographics_questions',
                        'confidence': 0.9
                    }
            
            # ✅ METHOD 2: Check detailed_intervention_learning for successful automations
            if self.brain:
                detailed_learning = self.brain.get("detailed_intervention_learning", {})
                
                for intervention_key, learning_data in detailed_learning.items():
                    # Look for successful automations of this question type
                    if (learning_data.get('question_type') == question_type and 
                        learning_data.get('result') == 'SUCCESS' and
                        learning_data.get('automation_success') == True):
                        
                        response_value = learning_data.get('response_value')
                        element_type = learning_data.get('element_type', 'auto_detect')
                        
                        if response_value:
                            print(f"🎯 Found successful automation record: '{response_value}'")
                            return {
                                'response': response_value,
                                'element_type': element_type,
                                'learned_from': intervention_key,
                                'confidence': 1.0  # High confidence - proven success
                            }
            
            # ✅ METHOD 3: Check user_profile as fallback
            if self.brain:
                user_profile = self.brain.get("user_profile", {})
                
                # Map question types to user profile fields
                profile_mappings = {
                    'age': user_profile.get('age'),
                    'gender': user_profile.get('gender'), 
                    'location': user_profile.get('location'),
                    'occupation': user_profile.get('occupation'),
                    'education': user_profile.get('education'),
                    'income': user_profile.get('personal_income'),
                    'employment': user_profile.get('employment_status'),
                    'marital_status': user_profile.get('marital_status'),
                    'household_size': user_profile.get('household_size'),
                    'postcode': user_profile.get('postcode'),
                    'birth_location': user_profile.get('birth_country'),
                    'industry': user_profile.get('industry'),
                    'pets': user_profile.get('pets'),
                    'children': user_profile.get('children')
                }
                
                profile_value = profile_mappings.get(question_type)
                if profile_value:
                    print(f"🎯 Using profile value for {question_type}: '{profile_value}'")
                    return {
                        'response': str(profile_value),
                        'element_type': 'auto_detect',
                        'learned_from': 'user_profile',
                        'confidence': 0.8
                    }
            
            print(f"❌ No learned response found for {question_type}")
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving learned response: {e}")
            return None
    
    # ========================================
    # LEARNED STRATEGY RETRIEVAL
    # ========================================
    
    async def get_learned_strategy(self, question_type: str, element_type: str) -> Optional[Dict[str, Any]]:
        """🧠 Get previously learned successful strategy from brain"""
        try:
            if self.brain and hasattr(self.brain, 'get_preferred_strategy'):
                learned_strategy = await self.brain.get_preferred_strategy(
                    question_type=question_type,
                    element_type=element_type
                )
                
                if learned_strategy:
                    print(f"🧠 USING LEARNED STRATEGY: {learned_strategy['name']} "
                          f"(success rate: {learned_strategy.get('success_rate', 0.0):.1%})")
                    return learned_strategy
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting learned strategy: {e}")
            return None
    
    # ========================================
    # USER RESPONSE RETRIEVAL
    # ========================================
    
    def get_user_response(self, question_type: str, question_text: str = "") -> str:
        """🧠 Get appropriate response value from brain's knowledge base"""
        try:
            # Get user demographics from brain
            demographics = self.get_demographics()
            
            print(f"🧠 Getting response for question type: {question_type}")
            
            # Direct mappings from question type to user data
            direct_mappings = {
                'age': demographics.get('age', '45'),
                'gender': demographics.get('gender', 'Male'),
                'location': demographics.get('location', 'New South Wales'),
                'occupation': demographics.get('occupation', 'Data Analyst'),
                'birth_location': demographics.get('birth_country', 'Australia'),
                'employment': demographics.get('employment_status', 'Full-time'),
                'industry': demographics.get('industry', 'Retail'),
                'education': demographics.get('education', 'High school education'),
                'marital_status': demographics.get('marital_status', 'Married/civil partnership'),
                'household_size': demographics.get('household_size', '4'),
                'children': demographics.get('children', 'Yes'),
                'pets': demographics.get('pets', 'Yes'),
                'postcode': demographics.get('postcode', '2217'),
                'work_sector': demographics.get('work_sector', 'Private Sector'),
                'work_arrangement': demographics.get('work_arrangement', 'Mix of on-site and home-based'),
                'sub_industry': demographics.get('sub_industry', 'Supermarkets'),
                'occupation_level': demographics.get('occupation_level', 'Academic/Professional')
            }
            
            # Check for income type (personal vs household)
            if question_type == 'income':
                if 'household' in question_text.lower():
                    response = demographics.get('household_income', '$200,000 to $499,999')
                else:
                    response = demographics.get('personal_income', '$100,000 to $149,999')
                print(f"🧠 Brain response for income: {response}")
                return response
            
            # Get direct mapping
            response = direct_mappings.get(question_type)
            if response:
                print(f"🧠 Brain response for {question_type}: {response}")
                return str(response)
            
            # Fallback - check question text for clues
            if 'gender' in question_text.lower() or 'male' in question_text.lower():
                return demographics.get('gender', 'Male')
            elif 'age' in question_text.lower():
                return str(demographics.get('age', '45'))
            else:
                print(f"⚠️ Unknown question type: {question_type}, using age as fallback")
                return str(demographics.get('age', '45'))
                
        except Exception as e:
            print(f"❌ Error getting user response from brain: {e}")
            # Fallback response
            if 'gender' in question_text.lower():
                return 'Male'
            else:
                return '45'
    
    # ========================================
    # DEMOGRAPHICS DATA ACCESS
    # ========================================
    
    def get_demographics(self) -> Dict[str, Any]:
        """🧠 Get user demographics from knowledge base"""
        try:
            if self.brain:
                # First try direct method
                if hasattr(self.brain, 'get_demographics'):
                    return self.brain.get_demographics()
                
                # Fallback to get method
                user_profile = self.brain.get("user_profile", {})
                return user_profile
            
            # Default demographics if no brain connection
            return {
                'age': '45',
                'gender': 'Male',
                'location': 'New South Wales',
                'postcode': '2217',
                'occupation': 'Data Analyst',
                'employment_status': 'Full-time',
                'industry': 'Retail',
                'personal_income': '$100,000 to $149,999',
                'household_income': '$200,000 to $499,999',
                'education': 'High school education',
                'marital_status': 'Married/civil partnership',
                'household_size': '4',
                'children': 'Yes',
                'pets': 'Yes'
            }
            
        except Exception as e:
            print(f"❌ Error getting demographics: {e}")
            return {}
    
    # ========================================
    # SUCCESS REPORTING
    # ========================================
    
    async def report_success(self, strategy_used: str, execution_time: float,
                           question_text: str, response_value: str,
                           question_type: str = None, confidence_score: float = 0.0):
        """🧠 Report successful automation to brain for learning"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"automation_{int(time.time())}",
                "question_type": question_type or self.last_question_type or "unknown",
                "question_text": question_text[:200],  # Limit length
                "strategy_used": strategy_used,
                "execution_time": execution_time,
                "confidence_score": confidence_score,
                "response_value": response_value,
                "result": "SUCCESS",
                "element_type": self._determine_element_type(strategy_used),
                "automation_success": True
            }
            
            # Store for future reference
            self.last_strategy_used = strategy_used
            self.last_question_type = question_type
            
            # 🧠 CRITICAL: Report to brain AND save
            if self.brain and hasattr(self.brain, 'learn_successful_automation'):
                success = await self.brain.learn_successful_automation(learning_data)
                if success:
                    print(f"🧠 SUCCESS LEARNED: {strategy_used} for {question_type}")
                    
                    # Also update demographics questions if possible
                    await self._update_demographics_questions(question_type, response_value)
                else:
                    print(f"⚠️ Failed to save learning data")
            else:
                print(f"⚠️ Brain connection not available for learning")
                
        except Exception as e:
            print(f"❌ Error reporting success to brain: {e}")
    
    # ========================================
    # FAILURE REPORTING
    # ========================================
    
    async def report_failure(self, error_message: str, question_text: str,
                           question_type: str = None, confidence_score: float = 0.0):
        """🧠 Report automation failure to brain for learning"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"automation_{int(time.time())}",
                "question_type": question_type or self.last_question_type or "unknown",
                "question_text": question_text[:200],  # Limit length
                "error_message": error_message,
                "confidence_score": confidence_score,
                "result": "FAILURE",
                "automation_success": False
            }
            
            # 🧠 Report failure for learning
            if self.brain and hasattr(self.brain, 'learn_from_failure'):
                await self.brain.learn_from_failure(learning_data)
                print(f"🧠 FAILURE LEARNED: {error_message}")
            else:
                print(f"⚠️ Brain connection not available for failure learning")
                
        except Exception as e:
            print(f"❌ Error reporting failure to brain: {e}")
    
    # ========================================
    # CONFIDENCE ADJUSTMENTS
    # ========================================
    
    def get_confidence_adjustment(self, question_type: str, base_confidence: float) -> float:
        """🧠 Get confidence adjustment based on learning history"""
        try:
            if self.brain and hasattr(self.brain, 'get_confidence_adjustment_suggestions'):
                adjustment = self.brain.get_confidence_adjustment_suggestions(
                    handler_name="demographics_handler",
                    question_type=question_type
                )
                
                if adjustment:
                    # Apply conservative adjustments to preserve working automation
                    if adjustment > 0:
                        # Positive adjustments applied fully
                        return adjustment
                    else:
                        # Negative adjustments applied conservatively (50%)
                        return adjustment * 0.5
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error getting confidence adjustment: {e}")
            return 0.0
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    def _determine_element_type(self, strategy_used: str) -> str:
        """Determine element type from strategy name"""
        if 'text' in strategy_used or 'input' in strategy_used or 'fill' in strategy_used:
            return 'text_input'
        elif 'radio' in strategy_used:
            return 'radio'
        elif 'dropdown' in strategy_used or 'select' in strategy_used:
            return 'dropdown'
        elif 'checkbox' in strategy_used:
            return 'checkbox'
        else:
            return 'unknown'
    
    async def _update_demographics_questions(self, question_type: str, response_value: str):
        """Update demographics questions with successful response"""
        try:
            if self.brain:
                demographics_questions = self.brain.get("demographics_questions", {})
                
                if question_type not in demographics_questions:
                    demographics_questions[question_type] = {
                        "patterns": [],
                        "responses": [],
                        "learned_patterns": [],
                        "confidence_threshold": 0.5,
                        "success_rate": 0.0
                    }
                
                # Add response if not already present
                responses = demographics_questions[question_type].get("responses", [])
                if response_value not in responses:
                    responses.append(response_value)
                    demographics_questions[question_type]["responses"] = responses
                    
                    # Update in knowledge base
                    self.brain.set("demographics_questions", demographics_questions)
                    
                    # Save to disk
                    if hasattr(self.brain, 'save_data'):
                        self.brain.save_data()
                    
                    print(f"🧠 Updated demographics questions with: {question_type} → {response_value}")
                    
        except Exception as e:
            print(f"❌ Error updating demographics questions: {e}")
    
    # ========================================
    # LEARNING STATE TRACKING
    # ========================================
    
    def set_detected_question_type(self, question_type: str):
        """Set the currently detected question type"""
        self.last_question_type = question_type
    
    def get_last_question_type(self) -> Optional[str]:
        """Get the last detected question type"""
        return self.last_question_type
    
    def get_last_strategy_used(self) -> Optional[str]:
        """Get the last strategy that was used"""
        return self.last_strategy_used
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def __str__(self) -> str:
        """String representation"""
        return f"DemographicsBrain(connected={self.brain is not None})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"DemographicsBrain(knowledge_base={self.brain.__class__.__name__ if self.brain else 'None'})"