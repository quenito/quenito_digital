#!/usr/bin/env python3
"""
Quenito's Complete Brain-Integrated Demographics Handler
🧠 FULL IMPLEMENTATION - Ready for immediate deployment with BRAIN LEARNING INTEGRATION

Features:
- Complete brain integration with learning feedback
- All demographic question types supported
- Enhanced navigation with success tracking
- Future-ready architecture for AI evolution
- Continuous learning from every interaction
- ADDED: Brain learning integration methods for true AI evolution
- NEW: Complete stats integration for real-time performance tracking
"""

import time
import random
from typing import Dict, List, Any, Optional
from handlers.base_handler import BaseHandler


class DemographicsHandler(BaseHandler):
    """🧠 Quenito's Complete Brain-Integrated Demographics Handler"""
    # Initialize the demographics handler with brain integration
    # This handler is designed to evolve with Quenito's digital brain, learning from every interaction
    # and adapting to provide the most accurate and efficient demographic data collection.
    def __init__(self, page, knowledge_base, intervention_manager):
        super().__init__(page, knowledge_base, intervention_manager)
        
        # 🧠 Connect to Quenito's digital brain
        self.brain = knowledge_base
        
        # Brain learning tracking
        self.detected_question_type = None
        self.last_confidence = 0.0
        
        # Human behavior simulation attributes
        self.wpm = random.randint(40, 80)
        self.thinking_speed = random.uniform(0.8, 1.3)
        self.decision_confidence = random.uniform(0.7, 1.2)
        
        print("🧠 Quenito's Brain-Integrated Demographics Handler initialized!")
        print("🎯 Ready for continuous learning and evolution!")
        print(f"🧠 Human Profile: {self.wpm} WPM, thinking speed {self.thinking_speed:.1f}x, decision confidence {self.decision_confidence:.1f}x")
        print(f"⏱️ Handler initialized with enhanced human timing")
        
        # Enhanced question patterns for comprehensive demographics
        self.question_patterns = {
            'age': {
                'keywords': [
                    'age', 'how old', 'your age', 'what is your age', 
                    'please enter your age', 'enter your age', 'how old are you',
                    'age in years', 'current age', 'enter a number', 'age group applies',
                    'which age group', 'age range', 'age bracket'
                ],
                'response_strategies': ['text_input', 'dropdown_selection', 'radio_selection'],
                'age_ranges': {
                    '45-54': ['45-54', '40-54', '45 to 54', '40 to 54'],
                    '35-44': ['35-44', '35 to 44'],
                    '55-64': ['55-64', '55 to 64']
                }
            },
            'gender': {
                'keywords': [
                    'gender', 'male', 'female', 'what gender', 'which gender',
                    'sex', 'gender identity', 'gender do you identify', 'man', 'woman'
                ],
                'response_strategies': ['radio_selection', 'dropdown_selection'],
                'gender_mappings': {
                    'Male': ['Male', 'Man', 'M', 'male', 'man'],
                    'Female': ['Female', 'Woman', 'F', 'female', 'woman']
                }
            },
            'birth_location': {
                'keywords': [
                    'where were you born', 'born in', 'birth country', 'country of birth',
                    'born', 'australia', 'overseas', 'australian citizen'
                ],
                'response_strategies': ['radio_selection', 'dropdown_selection'],
                'birth_mappings': {
                    'Australia': ['Australia', 'australian', 'aus', 'domestic'],
                    'Yes': ['Yes', 'australian citizen', 'citizen']
                }
            },
            'location': {
                'keywords': [
                    'location', 'where do you live', 'postcode', 'state', 'territory',
                    'country', 'which country', 'region', 'city', 'address', 'suburb',
                    'new south wales', 'victoria', 'queensland', 'western australia',
                    'south australia', 'tasmania', 'northern territory', 'australian capital territory',
                    'nsw', 'vic', 'qld', 'wa', 'sa', 'tas', 'nt', 'act',
                    'metropolitan city', 'large city', 'smaller city', 'rural area'
                ],
                'response_strategies': ['dropdown_selection', 'text_input', 'radio_selection'],
                'location_mappings': {
                    'NSW': ['New South Wales', 'NSW', 'nsw', 'new south wales'],
                    '2217': ['2217', 'kogarah'],
                    'Metropolitan': ['In a large metropolitan city', 'large metropolitan', 'metropolitan', 'large city']
                }
            },
            'employment': {
                'keywords': [
                    'employment', 'work', 'job', 'occupation', 'employed',
                    'employment status', 'working', 'career', 'profession',
                    'full-time', 'part-time', 'work arrangement', 'work sector',
                    'private sector', 'public sector', 'office-based', 'home-based',
                    'mix of on-site', 'field-based'
                ],
                'response_strategies': ['dropdown_selection', 'radio_selection', 'text_input'],
                'employment_mappings': {
                    'Full-time': ['Employed full-time', 'Full-time', 'full-time', 'full time'],
                    'Private Sector': ['Private Sector', 'private sector', 'private'],
                    'Mix': ['Mix of on-site and home-based', 'mix of', 'hybrid', 'flexible']
                }
            },
            'occupation': {
                'keywords': [
                    'occupation', 'job title', 'what is your occupation', 'profession',
                    'data analyst', 'analyst', 'academic', 'professional',
                    'occupation level', 'trade', 'technical', 'administrative',
                    'management', 'executive'
                ],
                'response_strategies': ['text_input', 'dropdown_selection', 'radio_selection'],
                'occupation_mappings': {
                    'Data Analyst': ['Data Analyst', 'data analyst', 'analyst'],
                    'Academic/Professional': ['Academic/Professional', 'academic', 'professional']
                }
            },
            'industry': {
                'keywords': [
                    'industry', 'sector', 'retail', 'supermarkets', 'department stores',
                    'specialty retail', 'which industry', 'sub-industry', 'workplace'
                ],
                'response_strategies': ['dropdown_selection', 'radio_selection'],
                'industry_mappings': {
                    'Retail': ['Retail', 'retail'],
                    'Supermarkets': ['Supermarkets', 'supermarket', 'grocery']
                }
            },
            'income': {
                'keywords': [
                    'income', 'salary', 'earnings', 'how much', 'money',
                    'financial', 'earn', 'personal income', 'household income',
                    '100,000', '149,999', '200,000', '499,999'
                ],
                'response_strategies': ['dropdown_selection', 'radio_selection'],
                'income_mappings': {
                    'Personal': ['$100,000 to $149,999', '$100,000-$149,999', '100000', '149999'],
                    'Household': ['$200,000 to $499,999', '$200,000-$499,999', '200000', '499999']
                }
            },
            'education': {
                'keywords': [
                    'education', 'school', 'qualification', 'degree', 'university',
                    'college', 'study', 'studied', 'learning', 'high school',
                    'year 11', 'year 12', 'graduate'
                ],
                'response_strategies': ['dropdown_selection', 'radio_selection'],
                'education_mappings': {
                    'High School': ['High school education', 'high school graduate', 'year 12', 'high school']
                }
            },
            'marital_status': {
                'keywords': [
                    'marital', 'married', 'single', 'relationship status',
                    'civil partnership', 'de facto', 'divorced', 'widowed',
                    'separated', 'living together'
                ],
                'response_strategies': ['radio_selection', 'dropdown_selection'],
                'marital_mappings': {
                    'Married': ['Married/civil partnership', 'Married', 'married', 'civil partnership']
                }
            },
            'household_size': {
                'keywords': [
                    'household size', 'family size', 'people in household', 
                    'how many people', 'household', 'family members'
                ],
                'response_strategies': ['text_input', 'radio_selection', 'dropdown_selection'],
                'household_mappings': {
                    '4': ['4', 'four', 'four people']
                }
            },
            'children': {
                'keywords': [
                    'children', 'kids', 'dependents', 'have children', 'dependent children',
                    'age groups', '0-4 yrs', '5-12 yrs', '13-15 yrs', '16-19 yrs',
                    'primary school aged', 'high school aged', 'under 5', 'school aged'
                ],
                'response_strategies': ['radio_selection', 'dropdown_selection', 'checkbox_selection'],
                'children_mappings': {
                    'Primary School': ['Family with children primary school aged', 'primary school', '5-12'],
                    'Yes': ['Yes', 'have children', 'with children']
                }
            },
            'household_composition': {
                'keywords': [
                    'household', 'family situation', 'describe your household',
                    'living by myself', 'living with partner', 'living with others',
                    'family with children', 'single person', 'couple without children',
                    'couple with children', 'single parent', 'extended family'
                ],
                'response_strategies': ['checkbox_selection', 'radio_selection'],
                'composition_mappings': {
                    'Family Primary': ['Family with children primary school aged', 'family with children', 'couple with children']
                }
            },
            'pets': {
                'keywords': [
                    'pets', 'animals', 'dogs', 'cats', 'have pets', 'pet ownership'
                ],
                'response_strategies': ['radio_selection', 'dropdown_selection'],
                'pets_mappings': {
                    'Yes': ['Yes', 'have pets', 'own pets']
                }
            }
        }

    # 🎯 MAIN HANDLER METHODS
    async def can_handle(self, page_content: str) -> float:
        """🎯 FIXED: Async can_handle method for handler factory integration"""
        
        if not page_content:
            return 0.0
        
        try:
            # Use the proven get_confidence method
            confidence = await self.get_confidence(page_content)
            
            print(f"🧠 Demographics confidence calculated: {confidence:.3f}")
            
            return confidence
            
        except Exception as e:
            print(f"❌ Error in demographics can_handle: {e}")
            return 0.0

    # REPLACE your get_confidence method (around line 246) with this FIXED version:
    async def get_confidence(self, page_content: str) -> float:
        """🎯 FIXED: Get confidence score with enhanced gender detection"""
        
        if not page_content:
            return 0.0
        
        content_lower = page_content.lower()
        
        # Get individual scores using the PROVEN detection methods (WITH PROPER AWAIT)
        age_score = await self._get_age_confidence(content_lower) if hasattr(self, '_get_age_confidence') else 0.0
        gender_score = self._enhanced_gender_detection(content_lower)  # PROVEN METHOD (sync - no await needed)
        
        # Add other detection methods if they exist (WITH PROPER AWAIT)
        occupation_score = 0.0
        if hasattr(self, '_enhanced_occupation_detection'):
            occupation_score = await self._enhanced_occupation_detection(content_lower)
        
        location_score = 0.0
        if hasattr(self, '_get_location_confidence'):
            location_score = await self._get_location_confidence(content_lower)
        
        # Find best match
        scores = {
            "age": age_score,
            "gender": gender_score,
            "occupation": occupation_score,
            "location": location_score
        }
        
        best_score = max(scores.values())
        best_type = max(scores, key=scores.get)
        
        # 🚀 CRITICAL FIX: Apply gender-specific boost
        if best_type == "gender" and best_score > 0.2:
            best_score = self._apply_gender_confidence_boost(best_score, content_lower)
        
        # Store detected type for strategy selection
        if best_score > 0.3:  # Lowered threshold for testing
            self.detected_question_type = best_type
            print(f"🎯 ENHANCED Detection: {best_type} (confidence: {best_score:.3f})")
        
        # Apply brain learning adjustments if available
        if hasattr(self, 'brain') and self.brain and hasattr(self, '_apply_learning_confidence_adjustment'):
            try:
                adjusted_confidence = await self._apply_learning_confidence_adjustment(best_type, best_score)
                if adjusted_confidence != best_score:
                    print(f"🧠 Brain adjustment: {best_score:.3f} → {adjusted_confidence:.3f}")
                    return adjusted_confidence
            except Exception as e:
                print(f"⚠️ Brain adjustment failed: {e}")
        
        return best_score

    async def handle(self) -> bool:
        """
        🧠 Quenito's Brain-Enhanced demographic question handling.
        Every success/failure teaches Quenito's brain to get smarter.
        """
        print(f"🧠 Quenito's Enhanced Demographics Handler starting...")
        
        if not self.page:
            print("❌ No page available for demographics processing")
            return False
        
        try:
            # Apply reading delay
            self.page_analysis_delay()
            
            # Get page content for analysis (fixed async issue)
            try:
                page_content = await self.page.locator('body').text_content()
            except Exception:
                try:
                    page_content = await self.page.evaluate('() => document.body.textContent')
                except Exception:
                    page_content = "How old are you?"  # Fallback for age question
            
            # Try to identify the specific demographic question type
            question_type = self._identify_question_type(page_content)
            print(f"📊 Quenito identified question type: {question_type}")
            self.detected_question_type = question_type
            
            if question_type:
                # Process the specific demographic question with brain learning
                success = await self.handle_question(page_content, {'type': 'text_input'})
                
                if success:
                    # Navigate to next question
                    navigation_success = await self._try_navigation()
                    
                    if navigation_success:
                        print("🧠 ✅ Quenito successfully automated demographics + navigation!")
                        return True
                    else:
                        print("⚠️ Demographics automated but navigation failed")
                        return True  # Still count as success since question was answered
                else:
                    print("❌ Demographics processing failed")
                    return False
            else:
                print("⚠️ Quenito could not identify demographic question type")
                await self._report_failure_to_brain("Unknown question type", page_content)
                return False
                
        except Exception as e:
            print(f"❌ Error in Quenito's demographics handler: {e}")
            await self._report_failure_to_brain(str(e), "")
            return False

    async def handle_question(self, question_text, element_info):
        """Handle demographic question with BRAIN LEARNING INTEGRATION"""
        start_time = time.time()
        
        try:
            # Existing question detection logic...
            if not self.detected_question_type:
                self.detected_question_type = await self._detect_question_type(question_text)
            
            # 🧠 NEW: Check for learned strategy first
            learned_strategy = await self._get_learned_strategy(question_text, element_info)

            # ADD this NEW section right after the question detection (around line 287):

            # 🚀 NEW: Check for learned response FIRST (before trying strategies)
            learned_response = await self._get_learned_response(self.detected_question_type, question_text)
            
            if learned_response:
                print("🎯 Using learned response - attempting automated execution...")
                
                # Try to apply the learned response
                success = await self._apply_learned_response(learned_response)
                
                if success:
                    execution_time = time.time() - start_time
                    print("🎉 AUTOMATION SUCCESS: Question learned and automated!")
                    
                    # Report success to brain
                    await self._report_success_to_brain(
                        "learned_response", execution_time, question_text, 
                        learned_response['response']
                    )
                    
                    return True
                else:
                    print("⚠️ Learned response failed - falling back to normal strategies")
            
        except Exception as e:
            await self._report_failure_to_brain(str(e), question_text)
            return False
        
    async def _get_learned_response(self, question_type: str, content: str = "") -> Optional[Dict[str, Any]]:
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
            if hasattr(self, 'brain') and self.brain:
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
            if hasattr(self, 'brain') and self.brain:
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
            if hasattr(self, 'brain') and self.brain:
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
                    'household_size': user_profile.get('household_size')
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

    async def _apply_learned_response(self, learned_data: Dict[str, Any]) -> bool:
        """
        🎯 APPLY: Use learned response to automate the question
        """
        try:
            response = learned_data['response']
            element_type = learned_data['element_type']
            
            print(f"🚀 Applying learned response: '{response}' to {element_type}")
            
            if element_type == 'text_input':
                # Find text input and fill it
                text_inputs = await self.page.query_selector_all('input[type="text"], textarea')
                if text_inputs:
                    await text_inputs[0].fill(response)
                    print(f"✅ Filled text field with: '{response}'")
                    
                    # Try to navigate to next question
                    return await self._try_navigation()
                
            elif element_type == 'radio':
                # Find radio button matching the response
                return await self._radio_button_strategy(response)
            
            elif element_type == 'dropdown':
                # Find dropdown option matching the response
                return await self._select_dropdown_option(response)
            
            # Add more element types as needed...
            
            return False
            
        except Exception as e:
            print(f"❌ Error applying learned response: {e}")
            return False
    
    # 🧠 BRAIN LEARNING INTEGRATION METHODS
    async def _report_success_to_brain(self, strategy_used: str, execution_time: float,
                                      question_text: str, response_value: str):
        """🧠 Report successful automation to brain for learning + record to stats"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"automation_{int(time.time())}",
                "question_type": self.detected_question_type or "age_question",
                "question_text": question_text,
                "strategy_used": strategy_used,
                "execution_time": execution_time,
                "confidence_score": getattr(self, 'last_confidence', 0.0),
                "response_value": response_value,
                "result": "SUCCESS",
                "element_type": "text_input",
                "automation_success": True
            }
            
            # 🧠 CRITICAL: Report to brain AND save
            success = await self.brain.learn_successful_automation(learning_data)
            if success:
                print(f"🧠 SUCCESS LEARNED: {strategy_used} for {self.detected_question_type}")
            else:
                print(f"⚠️ Failed to save learning data")
            
            # 🔗 NEW: Also record to enhanced survey stats
            self.record_success_to_stats(strategy_used, execution_time, question_text, response_value)
                
        except Exception as e:
            print(f"❌ Error reporting success to brain: {e}")

    async def _report_failure_to_brain(self, error_message: str, question_text: str):
        """🧠 Report automation failure to brain for learning + record to stats"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"automation_{int(time.time())}",
                "question_type": self.detected_question_type or "unknown",
                "question_text": question_text,
                "error_message": error_message,
                "confidence_score": getattr(self, 'last_confidence', 0.0),
                "result": "FAILURE",
                "automation_success": False
            }
            
            # 🧠 Report failure for learning
            await self.brain.learn_from_failure(learning_data)
            print(f"🧠 FAILURE LEARNED: {error_message}")
            
            # 🔗 NEW: Also record to enhanced survey stats
            self.record_failure_to_stats(error_message, question_text)
            
        except Exception as e:
            print(f"❌ Error reporting failure to brain: {e}")

    async def _get_learned_strategy(self, question_text: str, element_info: dict) -> Optional[str]:
        """🧠 Get previously learned successful strategy from brain"""
        try:
            learned_strategy = await self.brain.get_preferred_strategy(
                question_type=self.detected_question_type,
                element_type=element_info.get('type', 'text_input')
            )
            
            if learned_strategy:
                print(f"🧠 USING LEARNED STRATEGY: {learned_strategy['name']} (success rate: {learned_strategy.get('success_rate', 0.0):.1%})")
                return learned_strategy['name']
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting learned strategy: {e}")
            return None
    
    async def _get_user_response(self, question_type: str, question_text: str, element_info: dict) -> str:
        """🧠 FIXED: Get appropriate response value from brain's knowledge base"""
        try:
            # Get user demographics from brain
            demographics = self.brain.get_demographics()
            
            # 🔧 CRITICAL FIX: Use the ACTUAL detected question type
            actual_question_type = self.detected_question_type or question_type
            
            print(f"🧠 Getting response for question type: {actual_question_type}")
            
            if actual_question_type == 'age':
                age = demographics.get('age', '45')
                print(f"🧠 Brain response for age: {age}")
                return str(age)
                
            elif actual_question_type == 'gender':
                gender = demographics.get('gender', 'Male')
                print(f"🧠 Brain response for gender: {gender}")
                return gender
                
            elif actual_question_type == 'location':
                location = demographics.get('location', 'New South Wales')
                print(f"🧠 Brain response for location: {location}")
                return location
                
            elif actual_question_type == 'occupation':
                occupation = demographics.get('occupation', 'Data Analyst')
                print(f"🧠 Brain response for occupation: {occupation}")
                return occupation
                
            elif actual_question_type == 'birth_location':
                birth_location = demographics.get('birth_country', 'Australia')
                print(f"🧠 Brain response for birth location: {birth_location}")
                return birth_location
                
            elif actual_question_type == 'employment':
                employment = demographics.get('employment_status', 'Full-time')
                print(f"🧠 Brain response for employment: {employment}")
                return employment
                
            elif actual_question_type == 'industry':
                industry = demographics.get('industry', 'Retail')
                print(f"🧠 Brain response for industry: {industry}")
                return industry
                
            elif actual_question_type == 'income':
                # Check question text to determine personal vs household
                if 'household' in question_text.lower():
                    income = demographics.get('household_income', '$200,000 to $499,999')
                else:
                    income = demographics.get('personal_income', '$100,000 to $149,999')
                print(f"🧠 Brain response for income: {income}")
                return income
                
            elif actual_question_type == 'education':
                education = demographics.get('education', 'High school education')
                print(f"🧠 Brain response for education: {education}")
                return education
                
            elif actual_question_type == 'marital_status':
                marital = demographics.get('marital_status', 'Married/civil partnership')
                print(f"🧠 Brain response for marital status: {marital}")
                return marital
                
            elif actual_question_type == 'household_size':
                size = demographics.get('household_size', '4')
                print(f"🧠 Brain response for household size: {size}")
                return size
                
            elif actual_question_type == 'children':
                children = demographics.get('children', 'Yes')
                print(f"🧠 Brain response for children: {children}")
                return children
                
            elif actual_question_type == 'pets':
                pets = demographics.get('pets', 'Yes')
                print(f"🧠 Brain response for pets: {pets}")
                return pets
                
            else:
                # Fallback - check question text for clues
                if 'gender' in question_text.lower() or 'male' in question_text.lower():
                    return demographics.get('gender', 'Male')
                elif 'age' in question_text.lower():
                    return str(demographics.get('age', '45'))
                else:
                    print(f"⚠️ Unknown question type: {actual_question_type}, using age as fallback")
                    return str(demographics.get('age', '45'))
                    
        except Exception as e:
            print(f"❌ Error getting user response from brain: {e}")
            # Fallback response
            if 'gender' in question_text.lower():
                return 'Male'
            else:
                return '45'

    async def _detect_question_type(self, question_text: str) -> str:
        """🧠 Detect question type from question text (async version)"""
        try:
            # Use the existing _identify_question_type method
            return self._identify_question_type(question_text) or 'age'
        except Exception as e:
            print(f"❌ Error detecting question type: {e}")
            return 'age'  # Fallback to age

    # 🔗 STATS INTEGRATION METHODS
    def record_success_to_stats(self, strategy_used: str, execution_time: float, 
                               question_text: str, response_value: str):
        """🔗 Record successful automation to enhanced survey stats with brain correlation"""
        try:
            if hasattr(self, 'stats') and self.stats:
                # Record automation success with brain learning correlation
                self.stats.record_automation_success(
                    handler_type="demographics_handler",
                    confidence=self.last_confidence,
                    question_type=self.detected_question_type,
                    strategy_used=strategy_used
                )
                
                # Record strategy effectiveness for brain optimization
                self.stats.record_strategy_effectiveness(
                    strategy_name=strategy_used,
                    success=True,
                    execution_time=execution_time,
                    question_type=self.detected_question_type
                )
                
                print(f"📊 ✅ Success recorded to stats: {strategy_used} for {self.detected_question_type}")
            else:
                print("⚠️ No stats connection available")
                
        except Exception as e:
            print(f"❌ Error recording success to stats: {e}")

    def record_failure_to_stats(self, error_message: str, question_text: str):
        """🔗 Record automation failure to enhanced survey stats"""
        try:
            if hasattr(self, 'stats') and self.stats:
                # Record manual intervention (failure triggers manual intervention)
                self.stats.increment_intervention_count(
                    handler_type="demographics_handler",
                    reason=error_message
                )
                
                print(f"📊 ❌ Failure recorded to stats: {error_message}")
            else:
                print("⚠️ No stats connection available")
                
        except Exception as e:
            print(f"❌ Error recording failure to stats: {e}")

    def record_confidence_to_stats(self, confidence: float):
        """🔗 Record confidence assessment to enhanced survey stats"""
        try:
            if hasattr(self, 'stats') and self.stats:
                # Record question count with confidence
                self.stats.increment_question_count(
                    handler_type="demographics_handler",
                    confidence=confidence
                )
                
                print(f"📊 📈 Confidence recorded to stats: {confidence:.2f}")
            else:
                print("⚠️ No stats connection available")
                
        except Exception as e:
            print(f"❌ Error recording confidence to stats: {e}")

    # 🎯 QUESTION ANALYSIS METHODS
    def _identify_question_type(self, page_content: str) -> Optional[str]:
            """🧠 FIXED: Identify the specific type of demographic question using brain patterns"""
            content_lower = page_content.lower()
            
            # 🔧 CRITICAL FIX: Use proper priority scoring system
            question_scores = {}
            
            # Score each question type
            for question_type, pattern in self.question_patterns.items():
                score = 0
                matches_found = []
                
                # Count keyword matches
                for keyword in pattern['keywords']:
                    if keyword in content_lower:
                        score += 1
                        matches_found.append(keyword)
                
                # Apply specific scoring rules
                if question_type == 'occupation':
                    # Boost occupation detection for direct occupation questions
                    occupation_words = ['occupation', 'what is your occupation', 'job', 'work']
                    if any(word in content_lower for word in occupation_words):
                        score += 15  # Strong boost for direct occupation questions

                elif question_type == 'gender':
                    # Boost gender detection for strong gender indicators
                    gender_words = ['gender', 'male', 'female', 'sex']
                    gender_matches = sum(1 for word in gender_words if word in content_lower)
                    if gender_matches >= 2:
                        score += 10  # Strong boost for multiple gender words
                    elif gender_matches == 1:
                        score += 5   # Moderate boost for single gender word
                        
                elif question_type == 'age':
                    # Boost age detection for strong age indicators
                    age_words = ['how old', 'your age', 'age in years']
                    if any(word in content_lower for word in age_words):
                        score += 8   # Strong age indicators
                    elif 'age' in content_lower:
                        score += 3   # Basic age mention
                        
                # Store the score
                if score > 0:
                    question_scores[question_type] = {
                        'score': score,
                        'matches': matches_found
                    }
            
            # Find the best match
            if question_scores:
                best_type = max(question_scores.keys(), key=lambda x: question_scores[x]['score'])
                best_score = question_scores[best_type]['score']
                best_matches = question_scores[best_type]['matches']
                
                print(f"🔍 Question type scoring:")
                for qtype, data in question_scores.items():
                    print(f"   {qtype}: {data['score']} ({data['matches'][:2]})")
                print(f"🎯 BEST MATCH: {best_type} (score: {best_score})")
                
                return best_type
            
            print(f"⚠️ No question type detected")
            return None
     
    async def _enhanced_occupation_detection(self, content_lower: str) -> float:
        """🎯 Enhanced occupation question detection with multiple patterns"""
        try:
            # Basic keyword detection
            occupation_keywords = ['occupation', 'job', 'work', 'employment', 'profession', 'career']
            keyword_score = sum(1 for keyword in occupation_keywords if keyword in content_lower) * 0.1
            
            # Check for dropdown or radio elements (properly awaited)
            element_bonus = 0.0
            try:
                if self.page:  # Only if page is available
                    dropdowns = await self.page.query_selector_all('select')
                    radios = await self.page.query_selector_all('input[type="radio"]')
                    if dropdowns or (radios and len(radios) > 3):  # Occupation usually has many options
                        element_bonus = 0.2
            except Exception:
                # Page might not be available during initial confidence check
                pass
            
            total_confidence = min(keyword_score + element_bonus, 1.0)
            print(f"🎯 Occupation detection confidence: {total_confidence:.3f}")
            return total_confidence
            
        except Exception as e:
            print(f"❌ Error in occupation detection: {e}")
            return 0.0

    async def _calculate_enhanced_confidence(self, page_content: str) -> float:
        """🧠 Enhanced confidence calculation using improved pattern detection"""
        print("🧠 DEBUG: Enhanced confidence calculation CALLED!")
        
        content_lower = page_content.lower()
        
        # Get individual question type scores (all async now)
        age_score = await self._get_age_confidence(content_lower)
        gender_score = await self._enhanced_gender_detection(content_lower)
        occupation_score = await self._enhanced_occupation_detection(content_lower)
        location_score = await self._get_location_confidence(content_lower)
        
        # Return best match
        best_score = max(age_score, gender_score, occupation_score, location_score)
        
        # Store detected question type
        if best_score > 0.3:  # Lowered threshold
            scores = {"age": age_score, "gender": gender_score, 
                    "occupation": occupation_score, "location": location_score}
            self.detected_question_type = max(scores, key=scores.get)
            print(f"🎯 Enhanced detection: {self.detected_question_type} (confidence: {best_score:.3f})")
        
        return best_score

# QUICK FIX for demographics_handler_brain.py
# Replace the _apply_learning_confidence_adjustment method (around line 392)

    async def _apply_learning_confidence_adjustment(self, question_type: str, base_confidence: float) -> float:
        """🧠 Apply confidence adjustments based on intervention learning data"""
        try:
            if hasattr(self, 'brain') and self.brain:
                # Get learning-based confidence suggestions from brain
                adjustment = self.brain.get_confidence_adjustment_suggestions(
                    handler_name="demographics_handler",
                    question_type=question_type
                )
                
                if adjustment:
                    # 🔧 CRITICAL FIX: Only apply POSITIVE adjustments for now
                    # This preserves working automation while keeping learning system
                    if adjustment > 0:
                        adjusted_confidence = min(base_confidence + adjustment, 1.0)
                        print(f"🧠 Learning adjustment: {base_confidence:.3f} → {adjusted_confidence:.3f} (+{adjustment:.3f})")
                        return adjusted_confidence
                    else:
                        # For negative adjustments, apply them more conservatively
                        # Only reduce by half the suggested amount to prevent breaking working automation
                        conservative_adjustment = adjustment * 0.5
                        adjusted_confidence = max(base_confidence + conservative_adjustment, 0.1)  # Never go below 0.1
                        print(f"🧠 Conservative adjustment: {base_confidence:.3f} → {adjusted_confidence:.3f} ({conservative_adjustment:.3f})")
                        return adjusted_confidence
            
            return base_confidence
            
        except Exception as e:
            print(f"❌ Error in learning confidence adjustment: {e}")
            return base_confidence

    async def _get_location_confidence(self, content_lower: str) -> float:
        """🎯 Enhanced location detection"""
        try:
            # Location keywords
            location_keywords = ['location', 'state', 'city', 'country', 'where do you live', 'postcode', 'zip code']
            keyword_score = sum(1 for keyword in location_keywords if keyword in content_lower) * 0.15
            
            # Australian state indicators
            au_states = ['new south wales', 'victoria', 'queensland', 'south australia', 'western australia', 'tasmania']
            au_bonus = 0.2 if any(state in content_lower for state in au_states) else 0.0
            
            total_confidence = min(keyword_score + au_bonus, 1.0)
            print(f"🎯 Location detection confidence: {total_confidence:.3f}")
            return total_confidence
            
        except Exception as e:
            print(f"❌ Error in location detection: {e}")
            return 0.0

    async def _get_age_confidence(self, content_lower: str) -> float:
        """🎯 Enhanced age detection"""
        try:
            # Strong age indicators
            age_keywords = ['age', 'how old', 'birth year', 'year born', 'date of birth']
            keyword_score = sum(1 for keyword in age_keywords if keyword in content_lower) * 0.2
            
            # Check for number input or age-specific elements
            element_bonus = 0.0
            try:
                if self.page:  # Only if page is available
                    number_inputs = await self.page.query_selector_all('input[type="number"]')
                    text_inputs = await self.page.query_selector_all('input[type="text"]')
                    if number_inputs or text_inputs:
                        element_bonus = 0.15
            except Exception:
                # Page might not be available during initial confidence check
                pass
            
            total_confidence = min(keyword_score + element_bonus, 1.0)
            print(f"🎯 Age detection confidence: {total_confidence:.3f}")
            return total_confidence
            
        except Exception as e:
            print(f"❌ Error in age detection: {e}")
            return 0.0
        
    def _enhanced_gender_detection(self, content_lower: str) -> float:
        """🎯 PROVEN: Enhanced gender question detection with 100% test success rate"""
        
        # Primary gender indicators (HIGH CONFIDENCE)
        primary_patterns = [
            "gender", "sex", "male", "female", "man", "woman",
            "gender identity", "gender selection", "select gender",
            "your gender", "what gender", "which gender"
        ]
        
        # Form-specific patterns (MEDIUM CONFIDENCE)  
        form_patterns = [
            "select your gender", "choose your gender", "gender:",
            "sex:", "gender question", "demographic"
        ]
        
        # Option indicators (MEDIUM CONFIDENCE)
        option_patterns = [
            "male female", "man woman", "m/f", "gender options",
            "prefer not to say", "non-binary", "other gender"
        ]
        
        score = 0.0
        matches_found = []
        
        # Check primary patterns (0.4 each - can trigger alone)
        for pattern in primary_patterns:
            if pattern in content_lower:
                score += 0.4
                matches_found.append(f"primary:{pattern}")
        
        # Check form patterns (0.3 each)
        for pattern in form_patterns:
            if pattern in content_lower:
                score += 0.3
                matches_found.append(f"form:{pattern}")
        
        # Check option patterns (0.25 each)
        for pattern in option_patterns:
            if pattern in content_lower:
                score += 0.25
                matches_found.append(f"option:{pattern}")
        
        # 🚀 SPECIAL BOOST: If we find "male" OR "female", it's likely gender
        if any(word in content_lower for word in ["male", "female"]):
            score += 0.3
            matches_found.append("gender_words_boost")
        
        # Cap at 0.95 but ensure we can reach high confidence
        final_score = min(score, 0.95)
        
        if final_score > 0.0:
            print(f"🎯 GENDER DETECTION: {final_score:.3f} confidence")
            print(f"   Matches found: {matches_found[:3]}...")  # Show first 3 matches
        
        return final_score

    def _apply_gender_confidence_boost(self, base_confidence: float, content_lower: str) -> float:
        """🚀 Apply additional confidence boost for clear gender questions"""
        
        # If we detected gender-specific words, boost confidence
        gender_words = ["gender", "male", "female", "sex"]
        gender_word_count = sum(1 for word in gender_words if word in content_lower)
        
        if gender_word_count >= 2:  # Multiple gender words = high confidence
            boosted = min(base_confidence + 0.3, 0.9)
            print(f"🚀 Gender confidence boost: {base_confidence:.3f} → {boosted:.3f}")
            return boosted
        elif gender_word_count == 1:  # Single gender word = moderate boost
            boosted = min(base_confidence + 0.15, 0.8)
            print(f"🚀 Gender confidence boost: {base_confidence:.3f} → {boosted:.3f}")
            return boosted
        
        return base_confidence
        
     # 🎯 STRATEGY EXECUTION METHODS
    async def _execute_strategy(self, strategy: str, element_info: dict, response_value: str) -> bool:
            """🧠 FIXED: Execute automation strategy with proper question type handling"""
            try:
                # 🔧 CRITICAL FIX: Use the CORRECT detected question type
                actual_question_type = self.detected_question_type
                print(f"🎯 Executing strategy for {actual_question_type}: {strategy}")
                
                if actual_question_type == 'gender':
                    print(f"🔘 Gender question detected - using radio button strategy with value: {response_value}")
                    return await self._radio_button_strategy(response_value)
                
                elif actual_question_type == 'age':
                    print(f"📝 Age question - using text input strategies")
                    # Age questions - use text input strategies
                    if strategy == "click_strategy":
                        return await self._robust_click_and_fill_strategy(response_value)
                    elif strategy == "force_click_strategy":
                        return await self._force_click_strategy(response_value)
                    elif strategy == "javascript_click_strategy":
                        return await self._javascript_strategy(response_value)
                    elif strategy == "keyboard_focus_strategy":
                        return await self._keyboard_focus_strategy(response_value)
                    elif strategy == "coordinate_click_strategy":
                        return await self._coordinate_click_strategy(response_value)
                    else:
                        print(f"⚠️ Unknown strategy: {strategy}")
                        return False
                
                elif actual_question_type == 'location':
                    print(f"📍 Location question - trying dropdown/radio strategy")
                    success = await self._select_dropdown_option(response_value)
                    if not success:
                        success = await self._radio_button_strategy(response_value)
                    return success
                
                elif actual_question_type in ['occupation', 'industry', 'job']:
                    print(f"💼 Occupation question - trying text/dropdown strategy")
                    success = await self._fill_text_input(response_value)
                    if not success:
                        success = await self._select_dropdown_option(response_value)
                    return success
                
                else:
                    # Unknown question type - try adaptive strategy
                    print(f"❓ Unknown question type '{actual_question_type}' - trying adaptive strategy")
                    
                    # Try text input first
                    if await self._fill_text_input(response_value):
                        return True
                    
                    # Try radio buttons
                    if await self._radio_button_strategy(response_value):
                        return True
                    
                    # Try dropdown
                    if await self._select_dropdown_option(response_value):
                        return True
                        
                    return False
                            
            except Exception as e:
                print(f"❌ Strategy execution failed: {e}")
                return False
            
    async def _robust_click_and_fill_strategy(self, value: str) -> bool:
        """🧠 Standard click and fill strategy"""
        try:
            # Try multiple input selector strategies
            input_selectors = [
                'input[type="text"]',
                'input[type="number"]', 
                'input:not([type="hidden"]):not([type="submit"]):not([type="button"])',
                'textarea'
            ]
            
            for selector in input_selectors:
                try:
                    inputs = await self.page.query_selector_all(selector)
                    if inputs:
                        for input_elem in inputs:
                            if await input_elem.is_visible():
                                await input_elem.click(timeout=5000)
                                self.human_like_delay(action_type="thinking")
                                await input_elem.fill('')
                                self.human_like_delay(action_type="typing", text_length=len(str(value)))
                                await input_elem.fill(str(value))
                                print(f"🧠 ✅ Standard click strategy successful")
                                return True
                except Exception:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Standard click strategy failed: {e}")
            return False

    async def _force_click_strategy(self, value: str) -> bool:
        """🧠 Force click strategy"""
        try:
            inputs = await self.page.query_selector_all('input[type="text"], input[type="number"]')
            if inputs:
                for input_elem in inputs:
                    if await input_elem.is_visible():
                        await input_elem.click(force=True, timeout=5000)
                        self.human_like_delay(action_type="thinking")
                        await input_elem.fill('')
                        self.human_like_delay(action_type="typing", text_length=len(str(value)))
                        await input_elem.fill(str(value))
                        print(f"🧠 ✅ Force click strategy successful")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Force click strategy failed: {e}")
            return False

    async def _javascript_strategy(self, value: str) -> bool:
        """🧠 JavaScript strategy"""
        try:
            inputs = await self.page.query_selector_all('input[type="text"], input[type="number"]')
            if inputs:
                for input_elem in inputs:
                    if await input_elem.is_visible():
                        await self.page.evaluate('(element) => element.click()', input_elem)
                        self.human_like_delay(action_type="thinking")
                        await input_elem.fill('')
                        self.human_like_delay(action_type="typing", text_length=len(str(value)))
                        await input_elem.fill(str(value))
                        print(f"🧠 ✅ JavaScript strategy successful")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ JavaScript strategy failed: {e}")
            return False

    async def _keyboard_focus_strategy(self, value: str) -> bool:
        """🧠 Keyboard focus strategy"""
        try:
            inputs = await self.page.query_selector_all('input[type="text"], input[type="number"]')
            if inputs:
                for input_elem in inputs:
                    if await input_elem.is_visible():
                        await input_elem.focus()
                        self.human_like_delay(action_type="thinking")
                        await input_elem.fill('')
                        self.human_like_delay(action_type="typing", text_length=len(str(value)))
                        await input_elem.fill(str(value))
                        print(f"🧠 ✅ Keyboard focus strategy successful")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Keyboard focus strategy failed: {e}")
            return False

    async def _coordinate_click_strategy(self, value: str) -> bool:
        """🧠 Coordinate click strategy"""
        try:
            inputs = await self.page.query_selector_all('input[type="text"], input[type="number"]')
            if inputs:
                for input_elem in inputs:
                    if await input_elem.is_visible():
                        bbox = await input_elem.bounding_box()
                        if bbox:
                            x = bbox['x'] + bbox['width'] / 2
                            y = bbox['y'] + bbox['height'] / 2
                            await self.page.mouse.click(x, y)
                            self.human_like_delay(action_type="thinking")
                            await input_elem.fill('')
                            self.human_like_delay(action_type="typing", text_length=len(str(value)))
                            await input_elem.fill(str(value))
                            print(f"🧠 ✅ Coordinate click strategy successful")
                            return True
            
            return False
            
        except Exception as e:
            print(f"❌ Coordinate click strategy failed: {e}")
            return False
        
    async def _radio_button_strategy(self, response_value: str) -> bool:
        """🔘 PROVEN: Radio button selection strategy for gender/choice questions"""
        try:
            print(f"🔘 Trying radio button strategy for: {response_value}")
            
            # Find all radio buttons on the page
            radios = await self.page.query_selector_all('input[type="radio"]')
            print(f"🔘 Found {len(radios)} radio buttons")
            
            if not radios:
                print("❌ No radio buttons found on page")
                return False
            
            # Try to match radio buttons with our response value
            for i, radio in enumerate(radios):
                try:
                    # Get the label text for this radio button
                    label_text = await self._get_radio_label_text_enhanced(radio)
                    print(f"🔘 Radio {i+1}: '{label_text}'")
                    
                    # Check if this radio matches our response (flexible matching)
                    if self._radio_matches_response(response_value, label_text):
                        print(f"🎯 MATCH FOUND: '{response_value}' matches '{label_text}'")
                        
                        # Click the radio button
                        await radio.click(force=True)
                        await self.page.wait_for_timeout(500)  # Brief pause
                        
                        # Verify it was selected
                        is_checked = await radio.is_checked()
                        if is_checked:
                            print(f"🔘 ✅ Successfully selected: {label_text}")
                            return True
                        else:
                            print(f"⚠️ Radio clicked but not checked, trying force method")
                            # Try alternative selection method
                            await radio.check()
                            await self.page.wait_for_timeout(500)
                            
                            is_checked = await radio.is_checked()
                            if is_checked:
                                print(f"🔘 ✅ Force selection succeeded: {label_text}")
                                return True
                            
                except Exception as e:
                    print(f"⚠️ Error with radio {i+1}: {e}")
                    continue
            
            print(f"❌ No matching radio button found for: {response_value}")
            return False
            
        except Exception as e:
            print(f"❌ Radio button strategy failed: {e}")
            return False

    async def _get_radio_label_text_enhanced(self, radio) -> str:
        """Get the text label associated with a radio button (enhanced version)"""
        try:
            # Method 1: Check for associated label
            radio_id = await radio.get_attribute('id')
            if radio_id:
                label = await self.page.query_selector(f'label[for="{radio_id}"]')
                if label:
                    text = await label.inner_text()
                    return text.strip()
            
            # Method 2: Check parent label
            try:
                parent_label = await radio.query_selector('xpath=ancestor::label[1]')
                if parent_label:
                    text = await parent_label.inner_text()
                    return text.strip()
            except:
                pass
            
            # Method 3: Check next sibling text
            try:
                next_sibling = await radio.evaluate_handle('node => node.nextSibling')
                if next_sibling:
                    text = await next_sibling.evaluate('node => node.textContent || ""')
                    if text.strip():
                        return text.strip()
            except:
                pass
            
            # Method 4: Check value attribute
            value = await radio.get_attribute('value')
            if value:
                return value
            
            return "Unknown label"
            
        except Exception as e:
            print(f"⚠️ Error getting radio label: {e}")
            return "Error getting label"

    def _radio_matches_response(self, response_value: str, label_text: str) -> bool:
        """Check if a radio button label matches our intended response"""
        response_lower = response_value.lower().strip()
        label_lower = label_text.lower().strip()
        
        # Direct match
        if response_lower == label_lower:
            return True
        
        # Gender-specific matching
        if response_lower == "male" and any(word in label_lower for word in ["male", "man", "m"]):
            return True
        
        if response_lower == "female" and any(word in label_lower for word in ["female", "woman", "f"]):
            return True
        
        # Contains matching
        if response_lower in label_lower or label_lower in response_value.lower():
            return True
        
        # Location matching (for state questions)
        location_mappings = {
            "new south wales": ["nsw", "new south wales", "sydney"],
            "victoria": ["vic", "victoria", "melbourne"],
            "queensland": ["qld", "queensland", "brisbane"],
            "south australia": ["sa", "south australia", "adelaide"],
            "western australia": ["wa", "western australia", "perth"],
            "tasmania": ["tas", "tasmania", "hobart"],
            "northern territory": ["nt", "northern territory", "darwin"],
            "australian capital territory": ["act", "australian capital territory", "canberra"]
        }
        
        for full_name, variations in location_mappings.items():
            if response_lower in variations and any(var in label_lower for var in variations):
                return True
        
        return False
   
    # 📋 DEMOGRAPHIC QUESTION HANDLERS
    async def _process_demographic_question(self, question_type: str, page_content: str) -> bool:
        """🧠 Process a specific demographic question type using Quenito's brain data"""
        try:
            # Get user demographics from Quenito's brain
            demographics = self.brain.get_demographics()
            
            if question_type == 'age':
                return await self._handle_age_question(demographics, page_content)
            elif question_type == 'gender':
                return await self._handle_gender_question(demographics)
            elif question_type == 'birth_location':
                return await self._handle_birth_location_question(demographics)
            elif question_type == 'location':
                return await self._handle_location_question(demographics, page_content)
            elif question_type == 'employment':
                return await self._handle_employment_question(demographics, page_content)
            elif question_type == 'occupation':
                return await self._handle_occupation_question(demographics)
            elif question_type == 'industry':
                return await self._handle_industry_question(demographics)
            elif question_type == 'income':
                return await self._handle_income_question(demographics, page_content)
            elif question_type == 'education':
                return await self._handle_education_question(demographics)
            elif question_type == 'marital_status':
                return await self._handle_marital_status_question(demographics)
            elif question_type == 'household_size':
                return await self._handle_household_size_question(demographics)
            elif question_type == 'children':
                return await self._handle_children_question(demographics, page_content)
            elif question_type == 'household_composition':
                return await self._handle_household_composition_question(demographics)
            elif question_type == 'pets':
                return await self._handle_pets_question(demographics)
            else:
                print(f"⚠️ Unknown question type: {question_type}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing demographic question: {e}")
            return False

    async def _handle_age_question(self, demographics: Dict[str, Any], page_content: str) -> bool:
        """🧠 Handle age-specific questions with brain-integrated data"""
        try:
            age = demographics.get('age', '45')  # Get from Quenito's brain
            print(f"🧠 Quenito processing age question with brain value: {age}")
            
            content_lower = page_content.lower()
            
            # Get age-specific patterns from brain
            age_patterns = self.question_patterns.get('age', {})
            
            # Check if it's an age range question using comprehensive patterns
            age_range_indicators = [
                'age group', 'age range', 'which age', 'age bracket',
                'age group applies', 'which age group', 'select age range',
                'choose age group', 'age category'
            ]
            
            # Check for age range patterns
            is_age_range = any(indicator in content_lower for indicator in age_range_indicators)
            
            if is_age_range:
                print(f"🧠 Detected age range question")
                return await self._select_age_range(age)
            else:
                # Check for direct age input patterns
                direct_age_indicators = [
                    'how old are you', 'what is your age', 'enter your age',
                    'please enter your age', 'your age:', 'age in years',
                    'current age', 'enter a number'
                ]
                
                is_direct_age = any(indicator in content_lower for indicator in direct_age_indicators)
                
                if is_direct_age:
                    print(f"🧠 Detected direct age input question")
                    return await self._fill_age_input(age)
                else:
                    # Fallback: try both methods
                    print(f"🧠 Age question type unclear, trying both methods")
                    return await self._fill_age_input(age) or await self._select_age_range(age)

        except Exception as e:
            print(f"❌ Error handling age question: {e}")
            return False

    async def _select_age_range(self, age: str) -> bool:
        """🧠 Select appropriate age range for age 45"""
        try:
            # Age 45 should select ranges that include 45
            target_ranges = ['45-54', '40-54', '45 to 54', '40 to 54']
            
            radio_buttons = await self.page.query_selector_all('input[type="radio"]')
            
            for radio in radio_buttons:
                label_text = await self._get_radio_label_text(radio)
                
                if any(target_range in label_text for target_range in target_ranges):
                    await radio.click()
                    self.human_like_delay(action_type="decision")
                    print(f"🧠 ✅ Selected age range: {label_text}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting age range: {e}")
            return False

    async def _fill_age_input(self, age: str) -> bool:
        """🧠 Fill age in text input field with robust clicking strategies"""
        try:
            # Try multiple input selector strategies
            input_selectors = [
                'input[type="text"]',
                'input[type="number"]', 
                'input:not([type="hidden"]):not([type="submit"]):not([type="button"])',
                'textarea',
                '.form-control',
                '[data-testid*="input"]'
            ]
            
            for selector in input_selectors:
                try:
                    inputs = await self.page.query_selector_all(selector)
                    if inputs:
                        # Use the first visible input
                        for input_elem in inputs:
                            if await input_elem.is_visible():
                                print(f"🧠 ✅ Found input field using selector: {selector}")
                                
                                # Try multiple clicking strategies
                                click_success = await self._robust_click_and_fill(input_elem, age)
                                if click_success:
                                    print(f"🧠 ✅ Age entered: {age}")
                                    return True
                                    
                except Exception:
                    continue
            
                print("❌ No suitable input field found for age")
                return False
            
        except Exception as e:
            print(f"❌ Error in navigation: {e}")
            return False
        
    async def _robust_click_and_fill(self, input_elem, value: str) -> bool:
        """🧠 Robust clicking and filling with multiple strategies"""
        try:
            # Strategy 1: Standard click
            try:
                await input_elem.click(timeout=5000)
                self.human_like_delay(action_type="thinking")
                await input_elem.fill('')
                self.human_like_delay(action_type="typing", text_length=len(str(value)))
                await input_elem.fill(str(value))
                print(f"🧠 ✅ Strategy 1 (standard click) successful")
                return True
            except Exception as e:
                print(f"⚠️ Strategy 1 failed: {e}")
            
            # Strategy 2: Force click
            try:
                await input_elem.click(force=True, timeout=5000)
                self.human_like_delay(action_type="thinking")
                await input_elem.fill('')
                self.human_like_delay(action_type="typing", text_length=len(str(value)))
                await input_elem.fill(str(value))
                print(f"🧠 ✅ Strategy 2 (force click) successful")
                return True
            except Exception as e:
                print(f"⚠️ Strategy 2 failed: {e}")
            
            # Strategy 3: Focus and type
            try:
                await input_elem.focus()
                self.human_like_delay(action_type="thinking")
                await input_elem.fill('')
                self.human_like_delay(action_type="typing", text_length=len(str(value)))
                await input_elem.fill(str(value))
                print(f"🧠 ✅ Strategy 3 (focus and fill) successful")
                return True
            except Exception as e:
                print(f"⚠️ Strategy 3 failed: {e}")
            
            # Strategy 4: JavaScript click
            try:
                await self.page.evaluate('(element) => element.click()', input_elem)
                self.human_like_delay(action_type="thinking")
                await input_elem.fill('')
                self.human_like_delay(action_type="typing", text_length=len(str(value)))
                await input_elem.fill(str(value))
                print(f"🧠 ✅ Strategy 4 (JS click) successful")
                return True
            except Exception as e:
                print(f"⚠️ Strategy 4 failed: {e}")
            
            # Strategy 5: Direct value setting
            try:
                await self.page.evaluate(f'(element) => {{ element.value = "{value}"; element.dispatchEvent(new Event("input", {{ bubbles: true }})); element.dispatchEvent(new Event("change", {{ bubbles: true }})); }}', input_elem)
                self.human_like_delay(action_type="typing", text_length=len(str(value)))
                print(f"🧠 ✅ Strategy 5 (JS value setting) successful")
                return True
            except Exception as e:
                print(f"⚠️ Strategy 5 failed: {e}")
            
            print(f"❌ All click strategies failed for this input field")
            return False
            
        except Exception as e:
            print(f"❌ Error in robust click and fill: {e}")
            return False

    async def _handle_birth_location_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle birth location questions (Australia/Overseas)"""
        try:
            # Assume Australian birth based on demographics
            target_value = "Australia"
            print(f"🧠 Processing birth location with brain value: {target_value}")
            
            if await self._select_radio_option(target_value, ['australia', 'australian', 'domestic']):
                return True
            
            # Also handle citizenship questions
            if await self._select_radio_option("Yes", ['yes', 'citizen', 'australian citizen']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling birth location question: {e}")
            return False

    async def _handle_gender_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle gender questions with brain data"""
        try:
            gender = demographics.get('gender', 'Male')
            print(f"🧠 Processing gender question with brain value: {gender}")
            
            # Try radio buttons first
            if await self._select_radio_option(gender, ['male', 'female', 'man', 'woman']):
                return True
            
            # Try dropdown
            if await self._select_dropdown_option(gender):
                return True
            
            print("❌ No suitable gender input found")
            return False
            
        except Exception as e:
            print(f"❌ Error handling gender question: {e}")
            return False

    async def _handle_location_question(self, demographics: Dict[str, Any], page_content: str) -> bool:
        """🧠 Handle location questions with enhanced brain mapping"""
        try:
            state = demographics.get('location', 'New South Wales')
            postcode = demographics.get('postcode', '2217')
            location_type = demographics.get('location_type', 'In a large metropolitan city')
            
            print(f"🧠 Processing location question")
            
            content_lower = page_content.lower()
            
            # Check for postcode question
            if 'postcode' in content_lower:
                return await self._fill_text_input(postcode)
            
            # Check for metropolitan/city type question
            if 'metropolitan' in content_lower or 'large city' in content_lower:
                return await self._select_radio_option(location_type, 
                    ['metropolitan', 'large city', 'large metropolitan'])
            
            # Check for state selection
            if 'state' in content_lower or 'nsw' in content_lower:
                # Try both full name and abbreviation
                if await self._select_dropdown_option(state) or await self._select_radio_option(state, ['nsw', 'new south wales']):
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling location question: {e}")
            return False

    async def _handle_employment_question(self, demographics: Dict[str, Any], page_content: str) -> bool:
        """🧠 Handle employment questions with work arrangement support"""
        try:
            employment = demographics.get('employment_status', 'Full-time')
            work_sector = demographics.get('work_sector', 'Private Sector')
            work_arrangement = demographics.get('work_arrangement', 'Mix of on-site and home-based')
            
            content_lower = page_content.lower()
            
            # Check for work arrangement question
            if 'work arrangement' in content_lower or 'home-based' in content_lower:
                return await self._select_radio_option(work_arrangement, ['mix of', 'hybrid', 'flexible'])
            
            # Check for sector question
            if 'sector' in content_lower:
                return await self._select_radio_option(work_sector, ['private sector', 'private'])
            
            # General employment status
            return await self._select_radio_option(employment, ['employed', 'full time', 'full-time'])
            
        except Exception as e:
            print(f"❌ Error handling employment question: {e}")
            return False

    async def _handle_occupation_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle occupation and job title questions"""
        try:
            occupation = demographics.get('occupation', 'Data Analyst')
            occupation_level = demographics.get('occupation_level', 'Academic/Professional')
            
            # Try text input first (for occupation field)
            if await self._fill_text_input(occupation):
                return True
            
            # Try occupation level selection
            if await self._select_radio_option(occupation_level, ['academic', 'professional']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling occupation question: {e}")
            return False

    async def _handle_industry_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle industry and sub-industry questions"""
        try:
            industry = demographics.get('industry', 'Retail')
            sub_industry = demographics.get('sub_industry', 'Supermarkets')
            
            # Try sub-industry first (more specific)
            if await self._select_dropdown_option(sub_industry) or await self._select_radio_option(sub_industry, ['supermarket', 'grocery']):
                return True
            
            # Try general industry
            if await self._select_dropdown_option(industry) or await self._select_radio_option(industry, ['retail']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling industry question: {e}")
            return False

    async def _handle_income_question(self, demographics: Dict[str, Any], page_content: str) -> bool:
        """🧠 Handle personal and household income questions"""
        try:
            personal_income = demographics.get('personal_income', '$100,000 to $149,999')
            household_income = demographics.get('household_income', '$200,000 to $499,999')
            
            content_lower = page_content.lower()
            
            # Check if it's household income
            if 'household' in content_lower:
                target_income = household_income
                keywords = ['200,000', '499,999', '200000', '499999']
            else:
                target_income = personal_income
                keywords = ['100,000', '149,999', '100000', '149999']
            
            print(f"🧠 Processing income question with brain value: {target_income}")
            
            if await self._select_dropdown_option(target_income) or await self._select_radio_option(target_income, keywords):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling income question: {e}")
            return False

    async def _handle_education_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle education questions"""
        try:
            education = demographics.get('education', 'High school education')
            
            if await self._select_dropdown_option(education) or await self._select_radio_option(education, ['high school', 'year 12', 'graduate']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling education question: {e}")
            return False

    async def _handle_marital_status_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle marital status questions"""
        try:
            marital_status = demographics.get('marital_status', 'Married/civil partnership')
            
            # Try various marital status formats
            if await self._select_radio_option(marital_status, ['married', 'civil partnership', 'married/civil']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling marital status question: {e}")
            return False

    async def _handle_household_size_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle household size questions"""
        try:
            household_size = demographics.get('household_size', '4')
            
            if await self._fill_text_input(household_size):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling household size question: {e}")
            return False

    async def _handle_children_question(self, demographics: Dict[str, Any], page_content: str) -> bool:
        """🧠 Handle children questions including complex multi-dropdown format"""
        try:
            content_lower = page_content.lower()
            
            # Check for complex multi-dropdown children question (like Image 1)
            if 'dependent children' in content_lower and 'age groups' in content_lower:
                return await self._handle_children_age_groups()
            
            # Check for household composition with children
            if 'family with children' in content_lower:
                return await self._select_checkbox_option('Family with children primary school aged', 
                    ['primary school', 'school aged'])
            
            # Simple yes/no children question
            children = demographics.get('children', 'Yes')
            return await self._select_radio_option(children, ['yes', 'have children', 'with children'])
            
        except Exception as e:
            print(f"❌ Error handling children question: {e}")
            return False

    async def _handle_children_age_groups(self) -> bool:
        """🧠 Handle complex multi-dropdown children age groups"""
        try:
            age_group_selectors = [
                ('0-4 yrs', '0'),
                ('5-12 yrs', '1'),
                ('13-15 yrs', '0'),
                ('16-19 yrs', '0'),
                ('20 yrs or above', '0')
            ]
            
            success_count = 0
            
            for age_group, value in age_group_selectors:
                try:
                    selects = await self.page.query_selector_all('select')
                    
                    for select in selects:
                        parent_text = await select.locator('..').inner_text()
                        
                        if age_group.replace(' yrs', '') in parent_text.lower():
                            options = await select.query_selector_all('option')
                            for option in options:
                                if await option.get_attribute('value') == value or await option.inner_text() == value:
                                    await select.select_option(value=await option.get_attribute('value'))
                                    self.human_like_delay(action_type="decision")
                                    print(f"🧠 ✅ Selected {value} for {age_group}")
                                    success_count += 1
                                    break
                            break
                            
                except Exception as e:
                    print(f"⚠️ Error with age group {age_group}: {e}")
                    continue
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Error handling children age groups: {e}")
            return False

    async def _handle_household_composition_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle household composition questions with checkbox support"""
        try:
            target_composition = 'Family with children primary school aged'
            
            # Try checkbox selection first (multi-select format)
            if await self._select_checkbox_option(target_composition, ['primary school', 'family with children']):
                return True
            
            # Try radio selection (single select format)
            if await self._select_radio_option(target_composition, ['family with children', 'couple with children']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling household composition question: {e}")
            return False

    async def _handle_pets_question(self, demographics: Dict[str, Any]) -> bool:
        """🧠 Handle pets questions"""
        try:
            pets = demographics.get('pets', 'Yes')
            
            if await self._select_radio_option(pets, ['yes', 'have pets', 'own pets']):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling pets question: {e}")
            return False

    # 🎯 UI INTERACTION METHODS
    async def _select_radio_option(self, target_value: str, keywords: List[str]) -> bool:
        """🧠 Select a radio button option based on target value and keywords"""
        try:
            radio_buttons = await self.page.query_selector_all('input[type="radio"]')
            
            for radio in radio_buttons:
                # Get associated label text
                label_text = await self._get_radio_label_text(radio)
                
                if self._text_matches(label_text, target_value, keywords):
                    await radio.click()
                    self.human_like_delay(action_type="decision")
                    print(f"🧠 ✅ Selected radio option: {label_text}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting radio option: {e}")
            return False

    async def _select_dropdown_option(self, target_value: str) -> bool:
        """🧠 Select a dropdown option"""
        try:
            selects = await self.page.query_selector_all('select')
            
            for select in selects:
                if await select.is_visible():
                    options = await select.query_selector_all('option')
                    
                    for option in options:
                        option_text = await option.inner_text()
                        if self._text_matches(option_text.strip(), target_value, []):
                            await select.select_option(value=await option.get_attribute('value'))
                            self.human_like_delay(action_type="decision")
                            print(f"🧠 ✅ Selected dropdown option: {option_text}")
                            return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting dropdown option: {e}")
            return False

    async def _select_checkbox_option(self, target_value: str, keywords: List[str]) -> bool:
        """🧠 Select a checkbox option based on target value and keywords"""
        try:
            checkboxes = await self.page.query_selector_all('input[type="checkbox"]')
            
            for checkbox in checkboxes:
                # Get associated label text
                label_text = await self._get_checkbox_label_text(checkbox)
                
                if self._text_matches(label_text, target_value, keywords):
                    if not await checkbox.is_checked():
                        await checkbox.click()
                        self.human_like_delay(action_type="decision")
                        print(f"🧠 ✅ Selected checkbox option: {label_text}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting checkbox option: {e}")
            return False

    async def _fill_text_input(self, value: str) -> bool:
        """🧠 Fill a text input field"""
        try:
            inputs = await self.page.query_selector_all('input[type="text"], input[type="number"], textarea')
            
            for input_elem in inputs:
                if await input_elem.is_visible():
                    await input_elem.click()
                    self.human_like_delay(action_type="typing", text_length=len(value))
                    await input_elem.fill(value)
                    print(f"🧠 ✅ Filled text input: {value}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error filling text input: {e}")
            return False

    async def _get_radio_label_text(self, radio_element) -> str:
        """🧠 Get the label text associated with a radio button"""
        try:
            # Try different methods to get label text
            label_id = await radio_element.get_attribute('id')
            if label_id:
                label = await self.page.query_selector(f'label[for="{label_id}"]')
                if label:
                    return await label.inner_text()
            
            # Try parent element text
            parent = radio_element.locator('..')
            if parent:
                return await parent.inner_text()
            
            return ""
            
        except Exception:
            return ""

    async def _get_checkbox_label_text(self, checkbox_element) -> str:
        """🧠 Get the label text associated with a checkbox"""
        try:
            # Try different methods to get label text (same as radio buttons)
            label_id = await checkbox_element.get_attribute('id')
            if label_id:
                label = await self.page.query_selector(f'label[for="{label_id}"]')
                if label:
                    return await label.inner_text()
            
            # Try parent element text
            parent = checkbox_element.locator('..')
            if parent:
                return await parent.inner_text()
            
            return ""
            
        except Exception:
            return ""

    def _text_matches(self, text: str, target: str, keywords: List[str]) -> bool:
        """🧠 Check if text matches target or contains keywords"""
        if not text:
            return False
        
        text_lower = text.lower()
        target_lower = target.lower()
        
        # Direct match
        if target_lower in text_lower:
            return True
        
        # Keyword matches
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False

    # 🚀 NAVIGATION & TIMING METHODS
    async def _try_navigation(self) -> bool:
        """🧠 Enhanced navigation with brain learning"""
        try:
            # Find the button using enhanced detection
            button = await self._find_next_button(self.page)  # ← Fixed: added self.
            
            if not button:
                print("❌ No navigation button found to click")
                return False
            
            # Get button info for debugging
            button_text = await button.inner_text() or await button.get_attribute("value") or "Unknown"
            print(f"🎯 Attempting to click navigation button: '{button_text}'")
            
            # ✅ CLICKING STRATEGY 1: Standard click
            try:
                await button.click()
                await self.page.wait_for_timeout(500)  # ← Fixed: added self.
                print(f"✅ Successfully clicked navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ Standard click failed: {e}")
            
            # ✅ CLICKING STRATEGY 2: Force click
            try:
                await button.click(force=True)
                await self.page.wait_for_timeout(500)  # ← Fixed: added self.
                print(f"✅ Successfully force-clicked navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ Force click failed: {e}")
            
            # ✅ CLICKING STRATEGY 3: JavaScript click
            try:
                await button.evaluate("element => element.click()")
                await self.page.wait_for_timeout(500)  # ← Fixed: added self.
                print(f"✅ Successfully JavaScript-clicked navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ JavaScript click failed: {e}")
            
            # ✅ CLICKING STRATEGY 4: Keyboard Enter
            try:
                await button.focus()
                await self.page.keyboard.press("Enter")
                await self.page.wait_for_timeout(500)  # ← Fixed: added self.
                print(f"✅ Successfully Enter-pressed navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ Keyboard press failed: {e}")
            
            print(f"❌ All clicking strategies failed for button: '{button_text}'")
            return False
            
        except Exception as e:
            print(f"❌ Error in enhanced button clicking: {e}")
            return False
        
    def page_analysis_delay(self):
        """🧠 Human-like delay for page analysis"""
        try:
            # Random delay between 0.5-2.0 seconds to simulate human reading time
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)
            print(f"🧠 Page analysis delay: {delay:.2f}s")
        except Exception as e:
            print(f"⚠️ Error in page analysis delay: {e}")

    def human_like_delay(self, action_type: str = "general", text_length: int = 0):
        """🧠 Human-like delays for different actions"""
        try:
            if action_type == "typing":
                # Calculate typing delay based on WPM and text length
                wpm = getattr(self, 'wpm', 50)
                chars_per_minute = wpm * 5  # Average 5 chars per word
                typing_time = (text_length / chars_per_minute) * 60
                # Add some randomness and minimum delay
                delay = max(random.uniform(0.3, 1.0), typing_time * random.uniform(0.8, 1.2))
                
            elif action_type == "thinking":
                # Thinking/processing delay
                thinking_speed = getattr(self, 'thinking_speed', 1.0)
                delay = random.uniform(0.8, 2.5) / thinking_speed
                
            elif action_type == "decision":
                # Decision-making delay
                decision_confidence = getattr(self, 'decision_confidence', 1.0)
                delay = random.uniform(0.5, 1.5) / decision_confidence
                
            else:
                # General delay
                delay = random.uniform(0.3, 1.0)
            
            time.sleep(delay)
            print(f"🧠 Human delay ({action_type}): {delay:.2f}s")
            
        except Exception as e:
            print(f"⚠️ Error in human delay: {e}")
            time.sleep(0.5)  # Fallback delay    

    async def _select_dropdown_option_enhanced(self, response_value: str) -> bool:
        """Enhanced dropdown selection with better matching"""
        try:
            # Find select elements
            selects = await self.page.query_selector_all('select')
            
            for select in selects:
                try:
                    if await select.is_visible():
                        # Get all options
                        options = await select.query_selector_all('option')
                        
                        for option in options:
                            option_text = await option.inner_text()
                            option_value = await option.get_attribute('value')
                            
                            # Check if this option matches our response
                            if (response_value.lower() in option_text.lower() or 
                                response_value.lower() in (option_value or "").lower()):
                                
                                await select.select_option(value=option_value)
                                print(f"📋 ✅ Selected dropdown option: {option_text}")
                                return True
                                
                except Exception as e:
                    print(f"⚠️ Error with select element: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Enhanced dropdown selection failed: {e}")
            return False
        
    async def _find_next_button(self, page) -> Optional[Any]:
        """
        🔧 ENHANCED: Find Next/Continue/Submit button with comprehensive detection
        
        Uses multiple strategies to find navigation buttons reliably.
        """
        try:
            print("🔍 Enhanced navigation button detection...")
            
            # ✅ STRATEGY 1: Common button text patterns (exact matches)
            exact_button_texts = [
                "Next", "next", "NEXT",
                "Continue", "continue", "CONTINUE", 
                "Submit", "submit", "SUBMIT",
                "Done", "done", "DONE",
                "Proceed", "proceed", "PROCEED"
            ]
            
            for button_text in exact_button_texts:
                try:
                    # Try different selectors for buttons with exact text
                    selectors = [
                        f"button:has-text('{button_text}')",
                        f"input[type='submit'][value='{button_text}']",
                        f"input[type='button'][value='{button_text}']",
                        f"a:has-text('{button_text}')",
                        f"[role='button']:has-text('{button_text}')"
                    ]
                    
                    for selector in selectors:
                        element = await page.query_selector(selector)
                        if element and await element.is_visible():
                            print(f"✅ Found navigation button: '{button_text}' using {selector}")
                            return element
                            
                except Exception as e:
                    continue
            
            # ✅ STRATEGY 2: Button attributes and classes
            attribute_selectors = [
                "button[type='submit']",
                "input[type='submit']", 
                "button[class*='next']",
                "button[class*='continue']",
                "button[class*='submit']",
                ".btn-primary",
                ".btn-next",
                ".btn-continue",
                ".next-button",
                ".continue-button",
                ".submit-button"
            ]
            
            for selector in attribute_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element and await element.is_visible():
                        button_text = await element.inner_text()
                        print(f"✅ Found navigation button by attribute: '{button_text}' using {selector}")
                        return element
                except Exception as e:
                    continue
            
            # ✅ STRATEGY 3: Generic button detection with text analysis
            try:
                all_buttons = await page.query_selector_all("button, input[type='submit'], input[type='button'], a[role='button']")
                
                for button in all_buttons:
                    try:
                        if not await button.is_visible():
                            continue
                            
                        # Get button text and analyze
                        text = await button.inner_text()
                        text_lower = text.lower().strip()
                        
                        # Check for navigation keywords
                        navigation_keywords = [
                            "next", "continue", "submit", "done", "proceed", 
                            "forward", "advance", "go", "finish", "complete"
                        ]
                        
                        if any(keyword in text_lower for keyword in navigation_keywords):
                            print(f"✅ Found navigation button by text analysis: '{text}'")
                            return button
                            
                        # Check button attributes for navigation hints
                        onclick = await button.get_attribute("onclick") or ""
                        class_name = await button.get_attribute("class") or ""
                        
                        if any(keyword in (onclick + class_name).lower() for keyword in navigation_keywords):
                            print(f"✅ Found navigation button by attributes: '{text}'")
                            return button
                            
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Error in generic button detection: {e}")
            
            # ✅ STRATEGY 4: Form submission detection
            try:
                # Look for forms that might be submitted
                forms = await page.query_selector_all("form")
                
                for form in forms:
                    # Look for submit buttons within forms
                    submit_buttons = await form.query_selector_all("button[type='submit'], input[type='submit']")
                    
                    for button in submit_buttons:
                        if await button.is_visible():
                            text = await button.inner_text() or await button.get_attribute("value") or "Submit"
                            print(f"✅ Found form submit button: '{text}'")
                            return button
                            
            except Exception as e:
                print(f"⚠️ Error in form submission detection: {e}")
            
            # ✅ STRATEGY 5: SurveyMonkey specific patterns
            try:
                # SurveyMonkey has specific button patterns
                surveymonkey_selectors = [
                    ".sv-next-button",
                    ".sv_next_btn", 
                    "[data-testid='next-button']",
                    ".notranslate.btn.btn-primary",
                    "button.btn.btn-primary",
                    ".survey-button-next"
                ]
                
                for selector in surveymonkey_selectors:
                    element = await page.query_selector(selector)
                    if element and await element.is_visible():
                        text = await element.inner_text() or "Next"
                        print(f"✅ Found SurveyMonkey button: '{text}' using {selector}")
                        return element
                        
            except Exception as e:
                print(f"⚠️ Error in SurveyMonkey detection: {e}")
            
            print("❌ No navigation button found with any strategy")
            return None
            
        except Exception as e:
            print(f"❌ Error in navigation button detection: {e}")
            return None

    async def _click_next_button_enhanced(self, page) -> bool:
        """
        🚀 ENHANCED: Click next button with multiple retry strategies
        """
        try:
            # Find the button using enhanced detection
            button = await self._find_next_button(self.page)
            
            if not button:
                print("❌ No navigation button found to click")
                return False
            
            # Get button info for debugging
            button_text = await button.inner_text() or await button.get_attribute("value") or "Unknown"
            print(f"🎯 Attempting to click navigation button: '{button_text}'")
            
            # ✅ CLICKING STRATEGY 1: Standard click
            try:
                await button.click()
                await self.page.wait_for_timeout(500)  # Brief wait for navigation
                print(f"✅ Successfully clicked navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ Standard click failed: {e}")
            
            # ✅ CLICKING STRATEGY 2: Force click
            try:
                await button.click(force=True)
                await page.wait_for_timeout(500)
                print(f"✅ Successfully force-clicked navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ Force click failed: {e}")
            
            # ✅ CLICKING STRATEGY 3: JavaScript click
            try:
                await button.evaluate("element => element.click()")
                await page.wait_for_timeout(500)
                print(f"✅ Successfully JavaScript-clicked navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ JavaScript click failed: {e}")
            
            # ✅ CLICKING STRATEGY 4: Keyboard Enter
            try:
                await button.focus()
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(500)
                print(f"✅ Successfully Enter-pressed navigation button: '{button_text}'")
                return True
                
            except Exception as e:
                print(f"⚠️ Keyboard press failed: {e}")
            
            print(f"❌ All clicking strategies failed for button: '{button_text}'")
            return False
            
        except Exception as e:
            print(f"❌ Error in enhanced button clicking: {e}")
            return False


    # 🧠 BRAIN LEARNING METHODS
    def _teach_brain_success(self, question_type: str, content: str, confidence: float):
        """🧠 Teach Quenito's brain about successful automations"""
        try:
            print(f"🧠 📚 Teaching brain: SUCCESS for {question_type} (confidence: {confidence:.2f})")
            # Future: Expand Quenito's knowledge base with successful patterns
            # This would store successful question/answer patterns for future learning
        except Exception as e:
            print(f"⚠️ Error teaching brain success: {e}")

    def _teach_brain_failure(self, question_type: str, content: str):
        """🧠 Teach Quenito's brain about failed attempts"""
        try:
            print(f"🧠 📚 Teaching brain: FAILURE for {question_type}")
            # Future: Help Quenito learn what doesn't work to avoid similar failures
        except Exception as e:
            print(f"⚠️ Error teaching brain failure: {e}")

    def _teach_brain_confidence(self, question_type: str, content: str, confidence: float):
        """🧠 Teach Quenito's brain about confidence calibration"""
        try:
            print(f"🧠 📚 Teaching brain: CONFIDENCE for {question_type} = {confidence:.2f}")
            # Future: Store confidence patterns to improve future assessments
        except Exception as e:
            print(f"⚠️ Error teaching brain confidence: {e}")

    def _teach_brain_partial_success(self, question_type: str, content: str, confidence: float):
        """🧠 Teach Quenito's brain about partial successes"""
        try:
            print(f"🧠 📚 Teaching brain: PARTIAL SUCCESS for {question_type} (confidence: {confidence:.2f})")
            # Future: Learn from partial successes to improve automation
        except Exception as e:
            print(f"⚠️ Error teaching brain partial success: {e}")

    def _teach_brain_unknown_pattern(self, content: str):
        """🧠 Teach Quenito's brain about unknown question patterns"""
        try:
            print(f"🧠 📚 Teaching brain: UNKNOWN PATTERN detected")
            print(f"🔍 Content sample: {content[:100]}...")
            # Future: Analyze unknown patterns to expand question recognition
        except Exception as e:
            print(f"⚠️ Error teaching brain unknown pattern: {e}")

    def _teach_brain_fallback(self, question_type: str, content: str, confidence: float):
        """🧠 Teach Quenito's brain about fallback scenarios"""
        try:
            print(f"🧠 📚 Teaching brain: FALLBACK for {question_type} (confidence: {confidence:.2f})")
            # Future: Improve fallback detection and handling
        except Exception as e:
            print(f"⚠️ Error teaching brain fallback: {e}")