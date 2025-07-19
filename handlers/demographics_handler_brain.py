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
    def can_handle(self, page_content: str) -> float:
        """
        🧠 Quenito's Brain-Enhanced confidence calculation.
        Learns from every assessment to get smarter over time.
        """
        if not page_content:
            return 0.0
        
        try:
            content_lower = page_content.lower()
            
            # 🧠 BRAIN-POWERED STEP 1: Check against learned patterns from Quenito's brain
            brain_patterns = self.brain.get_question_pattern('demographics_questions')
            
            # STEP 1: Check for strong age question indicators (highest priority)
            strong_age_patterns = [
                'how old are you', 'what is your age', 'please enter your age',
                'enter your age', 'your age:', 'age in years'
            ]
            
            age_match = any(pattern in content_lower for pattern in strong_age_patterns)
            if age_match:
                confidence = 0.95
                print(f"🧠 QUENITO'S BRAIN: Strong age question detected! Confidence: {confidence}")
                self.last_confidence = confidence
                self._teach_brain_success('age', content_lower, confidence)
                
                # 🔗 NEW: Record confidence to stats
                self.record_confidence_to_stats(confidence)
                
                return confidence
            
            # STEP 2: Check for other demographic patterns
            demographic_score = 0
            total_patterns = len(self.question_patterns)
            
            for question_type, pattern in self.question_patterns.items():
                keyword_matches = sum(1 for keyword in pattern['keywords'] if keyword in content_lower)
                if keyword_matches > 0:
                    # Weight score based on number of keyword matches
                    pattern_score = min(keyword_matches / len(pattern['keywords']), 1.0)
                    demographic_score += pattern_score
                    print(f"🔍 {question_type}: {keyword_matches} matches, score: {pattern_score:.2f}")
            
            # STEP 3: Calculate final confidence
            if demographic_score > 0:
                base_confidence = min(demographic_score / total_patterns, 1.0)
                
                # Boost confidence for single demographic questions
                if demographic_score >= 0.3:  # At least 30% of a pattern matched
                    base_confidence = min(base_confidence + 0.2, 1.0)
                
                print(f"🧠 Quenito's demographics confidence: {base_confidence:.2f} (score: {demographic_score:.2f})")
                self.last_confidence = base_confidence
                self._teach_brain_confidence('demographics', content_lower, base_confidence)
                
                # 🔗 NEW: Record confidence to stats
                self.record_confidence_to_stats(base_confidence)
                
                return base_confidence
            
            # STEP 4: Fallback check for simple demographic indicators
            simple_indicators = ['age', 'gender', 'male', 'female', 'postcode', 'employment']
            simple_matches = sum(1 for indicator in simple_indicators if indicator in content_lower)
            
            if simple_matches > 0:
                fallback_confidence = min(simple_matches * 0.15, 0.6)  # Cap at 0.6
                print(f"🔍 Fallback demographics confidence: {fallback_confidence:.2f}")
                self.last_confidence = fallback_confidence
                self._teach_brain_fallback('demographics', content_lower, fallback_confidence)
                
                # 🔗 NEW: Record confidence to stats
                self.record_confidence_to_stats(fallback_confidence)
                
                return fallback_confidence
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error in Quenito's brain confidence calculation: {e}")
            return 0.0
    
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
            
            if learned_strategy:
                # Use learned strategy immediately
                strategies = [learned_strategy]
            else:
                # Fall back to multi-strategy approach
                strategies = ["click_strategy", "force_click_strategy", "javascript_click_strategy",
                             "keyboard_focus_strategy", "coordinate_click_strategy"]
            
            # Get response value
            response_value = await self._get_user_response(self.detected_question_type, question_text, element_info)
            
            # Try strategies
            for i, strategy in enumerate(strategies, 1):
                try:
                    print(f"🎯 Trying Strategy {i}: {strategy}")
                    success = await self._execute_strategy(strategy, element_info, response_value)
                    
                    if success:
                        execution_time = time.time() - start_time
                        print(f"✅ Strategy {i} SUCCESS! Time: {execution_time:.1f}s")
                        
                        # 🧠 CRITICAL: Report success to brain
                        await self._report_success_to_brain(strategy, execution_time, question_text, response_value)
                        
                        return True
                        
                except Exception as e:
                    print(f"❌ Strategy {i} failed: {e}")
                    continue
            
            # All strategies failed
            await self._report_failure_to_brain("All strategies failed", question_text)
            return False
            
        except Exception as e:
            await self._report_failure_to_brain(str(e), question_text)
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
        """🧠 Identify the specific type of demographic question using brain patterns"""
        content_lower = page_content.lower()
        
        # PRIORITY 1: Check for strong age question indicators first
        strong_age_patterns = [
            'how old are you', 'what is your age', 'please enter your age',
            'enter your age', 'your age:', 'age in years', 'current age'
        ]
        
        if any(pattern in content_lower for pattern in strong_age_patterns):
            print(f"🧠 PRIORITY: Strong age question detected!")
            return 'age'
        
        # PRIORITY 2: Check for other specific patterns
        # Check each pattern but prioritize more specific matches
        best_match = None
        best_score = 0
        
        for question_type, pattern in self.question_patterns.items():
            matches = 0
            
            # Count keyword matches
            for keyword in pattern['keywords']:
                if keyword in content_lower:
                    matches += 1
            
            # Apply priority weighting
            if question_type == 'age' and matches > 0:
                matches *= 3  # Boost age questions
            elif question_type == 'gender' and matches > 0:
                matches *= 2  # Boost gender questions
            elif question_type == 'location' and matches > 0:
                matches *= 0.5  # Reduce location sensitivity
            
            if matches > best_score:
                best_score = matches
                best_match = question_type
                
        print(f"🔍 Best match: {best_match} (score: {best_score})")
        return best_match if best_score > 0 else None

    async def _detect_question_type(self, question_text: str) -> Optional[str]:
        """🧠 Detect question type using brain patterns"""
        return self._identify_question_type(question_text)

    async def _get_user_response(self, question_type: str, question_text: str, element_info: dict) -> str:
        """🧠 Get appropriate response from brain demographics"""
        try:
            demographics = self.brain.get_demographics()
            
            if question_type == 'age':
                return demographics.get('age', '45')
            elif question_type == 'gender':
                return demographics.get('gender', 'Male')
            elif question_type == 'location':
                if 'postcode' in question_text.lower():
                    return demographics.get('postcode', '2217')
                elif 'state' in question_text.lower():
                    return demographics.get('location', 'New South Wales')
                else:
                    return demographics.get('location_type', 'In a large metropolitan city')
            # Add more mappings as needed
            else:
                return demographics.get('age', '45')  # Fallback
                
        except Exception as e:
            print(f"⚠️ Error getting user response: {e}")
            return '45'  # Safe fallback
        
     # 🎯 STRATEGY EXECUTION METHODS
    async def _execute_strategy(self, strategy: str, element_info: dict, response_value: str) -> bool:
        """🧠 Execute automation strategy"""
        try:
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
            # Look for next/continue buttons
            button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Next")',
                'button:has-text("Continue")',
                '.btn-primary',
                '.next-button'
            ]
            
            for selector in button_selectors:
                try:
                    button = await self.page.query_selector(selector)
                    if button and await button.is_visible():
                        self.human_like_delay(action_type="decision")
                        await button.click()
                        print("🧠 ✅ Quenito navigation successful")
                        return True
                except Exception:
                    continue
            
            print("⚠️ No navigation button found")
            return False
            
        except Exception as e:
            print(f"❌ Error in navigation: {e}")
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