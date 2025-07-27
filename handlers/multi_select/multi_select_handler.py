#!/usr/bin/env python3
"""
☑️ Multi Select Handler v2.0 - REFACTORED MODULAR ARCHITECTURE
Orchestrates multi-select question automation using clean module separation.

This handler coordinates:
- Pattern matching (multi_select_patterns.py)
- UI interactions (multi_select_ui.py)
- Brain learning (multi_select_brain.py)

Handles checkbox questions, multiple choice selections, and "select all that apply" formats.

ARCHITECTURE: Clean orchestration with delegated responsibilities
"""

import time
import random
from typing import Dict, List, Any, Optional, Set
from handlers.base_handler import BaseHandler
from .multi_select_patterns import MultiSelectPatterns
from .multi_select_ui import MultiSelectUI
from .multi_select_brain import MultiSelectBrain


class MultiSelectHandler(BaseHandler):
    """
    ☑️ Refactored Multi Select Handler - Clean Orchestration
    
    Coordinates pattern matching, UI interaction, and brain learning
    for automated multi-select/checkbox question handling.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Initialize modular components
        multi_select_data = knowledge_base.get("multi_select_questions", {}) if knowledge_base else {}
        self.patterns = MultiSelectPatterns(multi_select_data)
        self.ui = MultiSelectUI(page)
        self.brain = MultiSelectBrain(knowledge_base)
        
        # Handler state
        self.detected_question_type = None
        self.detected_options = []
        self.last_confidence = 0.0
        self.is_exclusive_type = False  # "None of the above" type questions
        
        # Human behavior simulation
        self.wpm = random.randint(40, 80)
        self.thinking_speed = random.uniform(0.8, 1.3)
        self.decision_confidence = random.uniform(0.7, 1.2)
        
        print("☑️ Refactored Multi Select Handler initialized!")
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
            # FIX for 'list' attribute error - ensure string type
            if isinstance(page_content, list):
                page_content = ' '.join(str(item) for item in page_content)
            elif not isinstance(page_content, str):
                page_content = str(page_content)
            
            confidence = await self.get_confidence(page_content)
            print(f"☑️ Multi Select confidence: {confidence:.3f}")
            return confidence
            
        except Exception as e:
            print(f"❌ Error in multi select can_handle: {e}")
            return 0.0
    
    async def get_confidence(self, page_content: str) -> float:
        """Calculate confidence score for multi-select detection"""
        if not page_content:
            return 0.0
        
        try:
            # Ensure string type
            if not isinstance(page_content, str):
                page_content = str(page_content)
            
            content_lower = page_content.lower()
            
            # Use patterns module to detect question type
            detected_type = self.patterns.detect_question_type(page_content)
            
            if detected_type:
                # Calculate keyword confidence
                base_confidence = self.patterns.calculate_keyword_confidence(page_content, detected_type)
                
                # Detect available options
                self.detected_options = await self._detect_checkbox_options()
                
                # Check for exclusive options
                self.is_exclusive_type = self.patterns.has_exclusive_option(page_content)
                
                # Apply brain learning adjustments
                adjustment = self.brain.get_confidence_adjustment(detected_type, base_confidence)
                final_confidence = min(base_confidence + adjustment, 1.0)
                
                # Store detection results
                self.detected_question_type = detected_type
                self.last_confidence = final_confidence
                self.brain.set_detected_question_type(detected_type)
                
                print(f"🎯 Detected: {detected_type} (confidence: {final_confidence:.3f})")
                print(f"☑️ Options found: {len(self.detected_options)}")
                print(f"🚫 Exclusive type: {self.is_exclusive_type}")
                
                return final_confidence
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error calculating confidence: {e}")
            return 0.0
    
    async def handle(self) -> bool:
        """Main handler execution - orchestrates the automation"""
        print(f"☑️ Multi Select Handler starting...")
        
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
                self.detected_options = await self._detect_checkbox_options()
            
            if self.detected_question_type:
                print(f"☑️ Processing {self.detected_question_type} question")
                print(f"📋 Available options: {len(self.detected_options)}")
                
                # Process the multi-select question
                success = await self.process_multi_select(
                    self.detected_question_type,
                    self.detected_options,
                    page_content
                )
                
                if success:
                    # Try navigation
                    nav_success = await self.ui.try_navigation()
                    if nav_success:
                        print("✅ Multi-select automated + navigation successful!")
                    return True
                
                return False
            else:
                print("⚠️ Could not identify multi-select question type")
                await self.brain.report_failure(
                    "Unknown question type",
                    page_content[:200],
                    confidence_score=self.last_confidence
                )
                return False
                
        except Exception as e:
            print(f"❌ Error in multi select handler: {e}")
            await self.brain.report_failure(str(e), "", confidence_score=self.last_confidence)
            return False
    
    # ========================================
    # MULTI-SELECT PROCESSING
    # ========================================
    
    async def process_multi_select(self, question_type: str, options: List[Dict], 
                                  page_content: str) -> bool:
        """Process a multi-select question by selecting appropriate options"""
        start_time = time.time()
        
        try:
            # Step 1: Get learned selections or generate new ones
            selections = await self.brain.get_learned_selections(question_type, page_content)
            
            if not selections:
                # Generate selections based on question type
                selections = await self._generate_selections(question_type, options, page_content)
            
            print(f"🎯 Planning to select {len(selections)} options: {selections[:3]}...")
            
            # Step 2: Apply selections
            selected_count = 0
            
            for option in options:
                option_text = option.get('text', '').strip()
                
                # Check if this option should be selected
                should_select = self._should_select_option(option_text, selections)
                
                if should_select:
                    # Check for exclusive options
                    if self._is_exclusive_option(option_text):
                        # If selecting "None", deselect all others first
                        await self.ui.deselect_all_checkboxes()
                    
                    success = await self.ui.select_checkbox(option['element'])
                    if success:
                        selected_count += 1
                        print(f"✅ Selected: {option_text}")
                        self.thinking_delay()  # Human-like delay
                
            # Calculate success
            success_rate = selected_count / len(selections) if selections else 0
            execution_time = time.time() - start_time
            
            if selected_count > 0:
                print(f"✅ Multi-select successful! Selected {selected_count} options")
                
                # Save successful selections
                await self.brain.save_selections(question_type, selections, page_content)
                
                await self.brain.report_success(
                    strategy_used="checkbox_selection",
                    execution_time=execution_time,
                    question_type=question_type,
                    selections_made=selected_count,
                    success_rate=success_rate,
                    confidence_score=self.last_confidence
                )
                return True
            else:
                print(f"⚠️ No options selected")
                await self.brain.report_failure(
                    "Failed to select any options",
                    page_content[:200],
                    question_type=question_type,
                    confidence_score=self.last_confidence
                )
                return False
                
        except Exception as e:
            print(f"❌ Error processing multi-select: {e}")
            await self.brain.report_failure(
                str(e),
                page_content[:200],
                question_type=question_type,
                confidence_score=self.last_confidence
            )
            return False
    
    # ========================================
    # SELECTION GENERATION
    # ========================================
    
    async def _generate_selections(self, question_type: str, options: List[Dict], 
                                  content: str) -> List[str]:
        """Generate appropriate selections based on question type"""
        option_texts = [opt.get('text', '') for opt in options]
        
        # Use brain to generate intelligent selections
        selections = self.brain.generate_selections(
            question_type,
            option_texts,
            content,
            min_selections=1,
            max_selections=min(5, len(option_texts))  # Reasonable limit
        )
        
        return selections
    
    def _should_select_option(self, option_text: str, selections: List[str]) -> bool:
        """Determine if an option should be selected"""
        option_lower = option_text.lower().strip()
        
        for selection in selections:
            selection_lower = selection.lower().strip()
            
            # Exact match
            if option_lower == selection_lower:
                return True
            
            # Partial match (contains)
            if selection_lower in option_lower or option_lower in selection_lower:
                return True
            
            # Word overlap
            option_words = set(option_lower.split())
            selection_words = set(selection_lower.split())
            if len(option_words & selection_words) >= 2:  # At least 2 words match
                return True
        
        return False
    
    def _is_exclusive_option(self, option_text: str) -> bool:
        """Check if option is exclusive (like 'None of the above')"""
        exclusive_patterns = [
            'none of', 'none', 'n/a', 'not applicable',
            'do not', "don't", 'neither', 'no ', 'nothing'
        ]
        option_lower = option_text.lower()
        return any(pattern in option_lower for pattern in exclusive_patterns)
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    async def _get_page_content(self) -> str:
        """Get page content with fallback strategies"""
        try:
            content = await self.page.locator('body').text_content()
            if content:
                return content
        except:
            pass
        
        try:
            content = await self.page.evaluate('() => document.body.textContent')
            if content:
                return content
        except:
            pass
        
        return "Unable to extract page content"
    
    async def _detect_checkbox_options(self) -> List[Dict[str, Any]]:
        """Detect available checkbox options on the page"""
        if not self.page:
            return []
        
        try:
            checkboxes = await self.ui.detect_all_checkboxes()
            options = []
            
            for checkbox in checkboxes:
                # Get associated text
                text = await self.ui.get_checkbox_label(checkbox)
                if text:
                    options.append({
                        'element': checkbox,
                        'text': text,
                        'checked': await checkbox.is_checked()
                    })
            
            return options
            
        except Exception as e:
            print(f"❌ Error detecting checkbox options: {e}")
            return []
    
    def page_analysis_delay(self):
        """Human-like delay for page analysis"""
        delay = random.uniform(0.5, 2.0) * self.thinking_speed
        time.sleep(delay)
        print(f"🧠 Page analysis delay: {delay:.2f}s")
    
    def thinking_delay(self):
        """Human-like delay between selections"""
        delay = random.uniform(0.2, 0.8) * self.thinking_speed
        time.sleep(delay)
    
    def human_like_delay(self, action_type: str = "general"):
        """Human-like delays for different actions"""
        if action_type == "thinking":
            delay = random.uniform(0.8, 2.5) / self.thinking_speed
        elif action_type == "decision":
            delay = random.uniform(0.5, 1.5) / self.decision_confidence
        elif action_type == "clicking":
            delay = random.uniform(0.2, 0.5)
        else:
            delay = random.uniform(0.3, 1.0)
        
        time.sleep(delay)
        print(f"⏱️ Human delay ({action_type}): {delay:.2f}s")