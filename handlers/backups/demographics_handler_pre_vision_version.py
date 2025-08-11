#!/usr/bin/env python3
"""
📊 Demographics Handler v3.0 - REFACTORED MODULAR ARCHITECTURE
Orchestrates demographics automation using clean module separation.

This handler coordinates:
- Pattern matching (demographics_patterns.py)
- UI interactions (demographics_ui.py)
- Brain learning (demographics_brain.py)

ARCHITECTURE: Clean orchestration with delegated responsibilities
"""

import time
import random
from typing import Dict, List, Any, Optional
from handlers.base_handler import BaseHandler
from .demographics_patterns import DemographicsPatterns
from .demographics_ui import DemographicsUI
from .demographics_brain import DemographicsBrain


class DemographicsHandler(BaseHandler):
    """
    📊 Refactored Demographics Handler - Clean Orchestration
    
    Coordinates pattern matching, UI interaction, and brain learning
    for automated demographics question handling.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Initialize modular components
        demographics_data = knowledge_base.get("demographics_questions", {}) if knowledge_base else {}
        self.patterns = DemographicsPatterns(demographics_data)
        self.ui = DemographicsUI(page)
        self.brain = DemographicsBrain(knowledge_base)
        
        # Handler state
        self.detected_question_type = None
        self.last_confidence = 0.0
        
        # Human behavior simulation
        self.wpm = random.randint(40, 80)
        self.thinking_speed = random.uniform(0.8, 1.3)
        self.decision_confidence = random.uniform(0.7, 1.2)
        
        print("📊 Refactored Demographics Handler initialized!")
        print("🧠 Modular architecture active: Patterns + UI + Brain")
        print(f"⏱️ Human simulation: {self.wpm} WPM, thinking {self.thinking_speed:.1f}x")
    
    # ========================================
    # MAIN HANDLER METHODS
    # ========================================
    
    async def can_handle(self, page_content: str) -> float:
        """Determine if this handler can process the current page"""
        if not page_content:
            return 0.0
        
        try:
            confidence = await self.get_confidence(page_content)
            print(f"📊 Demographics confidence: {confidence:.3f}")
            return confidence
            
        except Exception as e:
            print(f"❌ Error in demographics can_handle: {e}")
            return 0.0
    
    async def get_confidence(self, page_content: str) -> float:
        """Calculate confidence score for demographics detection"""
        if not page_content:
            return 0.0
        
        try:
            content_lower = page_content.lower()
            
            # Use patterns module to detect question type
            detected_type = self.patterns.detect_question_type(page_content)
            
            if detected_type:
                # Calculate keyword confidence
                base_confidence = self.patterns.calculate_keyword_confidence(page_content, detected_type)
                
                # Apply brain learning adjustments
                adjustment = self.brain.get_confidence_adjustment(detected_type, base_confidence)
                final_confidence = min(base_confidence + adjustment, 1.0)
                
                # Store detection results
                self.detected_question_type = detected_type
                self.last_confidence = final_confidence
                self.brain.set_detected_question_type(detected_type)
                
                print(f"🎯 Detected: {detected_type} (confidence: {final_confidence:.3f})")
                return final_confidence
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error calculating confidence: {e}")
            return 0.0
    
    async def handle(self) -> bool:
        """Main handler execution - orchestrates the automation"""
        print(f"📊 Demographics Handler starting...")
        
        if not self.page:
            print("❌ No page available")
            return False
        
        try:
            # Apply reading delay
            self.page_analysis_delay()
            
            # Get page content
            page_content = await self._get_page_content()
            
            # Detect question type if not already done
            if not self.detected_question_type:
                self.detected_question_type = self.patterns.detect_question_type(page_content)
            
            if self.detected_question_type:
                print(f"📊 Processing {self.detected_question_type} question")
                
                # Process the question
                success = await self.process_demographic_question(
                    self.detected_question_type, 
                    page_content
                )
                
                if success:
                    # Try navigation
                    nav_success = await self.ui.try_navigation()
                    if nav_success:
                        print("✅ Demographics automated + navigation successful!")
                    return True
                
                return False
            else:
                print("⚠️ Could not identify demographic question type")
                await self.brain.report_failure(
                    "Unknown question type", 
                    page_content[:200],
                    confidence_score=self.last_confidence
                )
                return False
                
        except Exception as e:
            print(f"❌ Error in demographics handler: {e}")
            await self.brain.report_failure(str(e), "", confidence_score=self.last_confidence)
            return False
    
    # ========================================
    # QUESTION PROCESSING
    # ========================================
    
    async def process_demographic_question(self, question_type: str, page_content: str) -> bool:
        """Process a specific demographic question type"""
        start_time = time.time()
        
        try:
            # Step 1: Check for learned response
            learned_response = await self.brain.get_learned_response(question_type, page_content)
            
            if learned_response:
                print(f"🎯 Using learned response: '{learned_response['response']}'")
                
                # Apply the learned response
                success = await self.apply_learned_response(learned_response)
                
                if success:
                    execution_time = time.time() - start_time
                    print(f"🎉 Learned response applied successfully!")
                    
                    # Report success
                    await self.brain.report_success(
                        strategy_used="learned_response",
                        execution_time=execution_time,
                        question_text=page_content[:200],
                        response_value=learned_response['response'],
                        question_type=question_type,
                        confidence_score=self.last_confidence
                    )
                    return True
                else:
                    print("⚠️ Learned response failed, trying other strategies")
            
            # Step 2: Get response value from brain
            response_value = self.brain.get_user_response(question_type, page_content)
            print(f"🧠 Response value: '{response_value}'")
            
            # Step 3: Try automation strategies
            success = await self.try_automation_strategies(question_type, response_value, page_content)
            
            if success:
                execution_time = time.time() - start_time
                await self.brain.report_success(
                    strategy_used=self.brain.get_last_strategy_used() or "unknown",
                    execution_time=execution_time,
                    question_text=page_content[:200],
                    response_value=response_value,
                    question_type=question_type,
                    confidence_score=self.last_confidence
                )
                return True
            else:
                await self.brain.report_failure(
                    "All strategies failed",
                    page_content[:200],
                    question_type=question_type,
                    confidence_score=self.last_confidence
                )
                return False
                
        except Exception as e:
            print(f"❌ Error processing demographic question: {e}")
            await self.brain.report_failure(
                str(e), 
                page_content[:200],
                question_type=question_type,
                confidence_score=self.last_confidence
            )
            return False
    
    # ========================================
    # AUTOMATION STRATEGIES
    # ========================================
    
    async def apply_learned_response(self, learned_data: Dict[str, Any]) -> bool:
        """Apply a learned response using appropriate UI strategy"""
        try:
            response = learned_data['response']
            element_type = learned_data.get('element_type', 'auto_detect')
            
            print(f"🚀 Applying learned response: '{response}' to {element_type}")
            
            # Auto-detect element type if needed
            if element_type == 'auto_detect':
                element_type = await self._detect_element_type()
            
            # Apply appropriate strategy based on element type
            if element_type == 'text_input':
                return await self.ui.fill_text_input(response)
            elif element_type == 'radio':
                return await self.ui.radio_button_strategy(response)
            elif element_type == 'dropdown':
                return await self.ui.select_dropdown_option(response)
            elif element_type == 'checkbox':
                keywords = self.patterns.get_keywords(self.detected_question_type)
                return await self.ui.select_checkbox_option(response, keywords)
            else:
                # Try all strategies
                return await self.try_automation_strategies(
                    self.detected_question_type, 
                    response, 
                    ""
                )
                
        except Exception as e:
            print(f"❌ Error applying learned response: {e}")
            return False
    
    async def try_automation_strategies(self, question_type: str, response_value: str, 
                                      page_content: str) -> bool:
        """Try various automation strategies based on question type"""
        try:
            # Get keywords for matching
            keywords = self.patterns.get_keywords(question_type)
            
            # Question-specific strategies
            if question_type == 'age':
                # Try text input first for age
                if await self.ui.fill_text_input(response_value):
                    return True
                # Try age range selection
                if await self._try_age_range_selection(response_value):
                    return True
                    
            elif question_type == 'gender':
                # Try radio buttons for gender
                if await self.ui.radio_button_strategy(response_value):
                    return True
                # Try dropdown
                if await self.ui.select_dropdown_option(response_value):
                    return True
                    
            elif question_type in ['location', 'employment', 'industry', 'education', 
                                  'marital_status', 'income']:
                # Try dropdown first
                if await self.ui.select_dropdown_option(response_value):
                    return True
                # Try radio buttons
                if await self.ui.select_radio_option(response_value, keywords):
                    return True
                    
            elif question_type in ['occupation', 'postcode', 'household_size']:
                # Try text input
                if await self.ui.fill_text_input(response_value):
                    return True
                    
            elif question_type in ['children', 'pets', 'birth_location']:
                # Try radio buttons
                if await self.ui.select_radio_option(response_value, keywords):
                    return True
                # Try dropdown
                if await self.ui.select_dropdown_option(response_value):
                    return True
            
            # Generic fallback - try all strategies
            print("⚠️ Trying generic strategies...")
            
            # Try text input
            if await self.ui.fill_text_input(response_value):
                return True
            
            # Try radio buttons
            if await self.ui.radio_button_strategy(response_value):
                return True
            
            # Try dropdown
            if await self.ui.select_dropdown_option(response_value):
                return True
            
            # Try checkboxes
            if await self.ui.select_checkbox_option(response_value, keywords):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error in automation strategies: {e}")
            return False
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    async def _get_page_content(self) -> str:
        """Get page content with fallback strategies"""
        try:
            # Try standard method
            content = await self.page.locator('body').text_content()
            if content:
                return content
        except:
            pass
        
        try:
            # Try JavaScript evaluation
            content = await self.page.evaluate('() => document.body.textContent')
            if content:
                return content
        except:
            pass
        
        # Fallback
        return "Unable to extract page content"
    
    async def _detect_element_type(self) -> str:
        """Detect the primary input element type on the page"""
        try:
            # Check for various element types
            if await self.ui.detect_text_input_elements():
                return 'text_input'
            elif await self.ui.detect_radio_elements():
                return 'radio'
            elif await self.ui.detect_dropdown_elements():
                return 'dropdown'
            elif await self.ui.detect_checkbox_elements():
                return 'checkbox'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    async def _try_age_range_selection(self, age: str) -> bool:
        """Try to select age range for numeric age"""
        try:
            age_num = int(age)
            
            # Define age range mappings
            if 45 <= age_num <= 54:
                range_keywords = ['45-54', '45 to 54', '40-54']
            elif 35 <= age_num <= 44:
                range_keywords = ['35-44', '35 to 44', '40-44']
            elif 55 <= age_num <= 64:
                range_keywords = ['55-64', '55 to 64']
            else:
                return False
            
            # Try radio button selection with range keywords
            for keyword in range_keywords:
                if await self.ui.select_radio_option(keyword, range_keywords):
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error in age range selection: {e}")
            return False
    
    def page_analysis_delay(self):
        """Human-like delay for page analysis"""
        delay = random.uniform(0.5, 2.0) * self.thinking_speed
        time.sleep(delay)
        print(f"🧠 Page analysis delay: {delay:.2f}s")
    
    def human_like_delay(self, action_type: str = "general", text_length: int = 0):
        """Human-like delays for different actions"""
        if action_type == "typing":
            chars_per_minute = self.wpm * 5
            typing_time = (text_length / chars_per_minute) * 60
            delay = max(random.uniform(0.3, 1.0), typing_time * random.uniform(0.8, 1.2))
        elif action_type == "thinking":
            delay = random.uniform(0.8, 2.5) / self.thinking_speed
        elif action_type == "decision":
            delay = random.uniform(0.5, 1.5) / self.decision_confidence
        else:
            delay = random.uniform(0.3, 1.0)
        
        time.sleep(delay)
        print(f"⏱️ Human delay ({action_type}): {delay:.2f}s")