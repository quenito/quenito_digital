#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're teaching Quenito to UNDERSTAND surveys, not just fill them.
Every decision should make him smarter, not just more mechanical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Automation Service - Orchestrating intelligence, not mechanics
Priority: LLM understanding > Mechanical handlers
"""
from typing import Dict, Any, List, Optional
import time
from services.llm_automation_service import LLMAutomationService
from services.knowledge_manager import knowledge
from services.vision_service import VisionService
from services.page_orchestrator import PageOrchestrator

# Import all specialized handlers (most will be disabled)
from services.demographics_handler import DemographicsHandler
from services.brand_selection_handler import BrandSelectionHandler
from services.carousel_handler import CarouselBrandHandler
from services.rating_handler import RatingScaleHandler
from services.brand_association_handler import BrandAssociationHandler


class AutomationService:
    """Service for attempting automation - Multi-handler approach with smart routing!"""
    
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.confidence_manager = self.kb.confidence_manager
        
        # Initialize Vision Service
        try:
            self.vision_service = VisionService()
            print("   👁️ Vision Service ENABLED for page analysis!")
        except Exception as e:
            self.vision_service = None
            print(f"   ⚠️ Vision Service disabled: {e}")
        
        # Initialize LLM service - PRIORITY 1!
        try:
            self.llm = LLMAutomationService()
            print("   🧠 LLM Automation ENABLED with GPT-4o-mini! (PRIORITY 1)")
        except Exception as e:
            self.llm = None
            print(f"   ⚠️ LLM disabled: {e}")
        
        # Initialize specialized handlers - Most are DISABLED in favor of LLM
        
        # Demographics Handler - DISABLED (LLM handles these better)
        self.demographics_handler = DemographicsHandler(knowledge_base)
        print("   ⚠️ Demographics handler initialized but DISABLED (LLM priority)")
        
        # Keep these complex handlers that LLM can't handle well
        try:
            self.brand_selection_handler = BrandSelectionHandler(knowledge_base)
            print("   ✅ Brand Selection handler (for complex matrices)")
        except TypeError:
            self.brand_selection_handler = BrandSelectionHandler()
            
        try:
            self.carousel_handler = CarouselBrandHandler(knowledge_base)
            print("   ✅ Carousel handler (for complex UI)")
        except TypeError:
            self.carousel_handler = CarouselBrandHandler()
        
        # Rating Handler - DISABLED (LLM handles these fine)    
        try:
            self.rating_handler = RatingScaleHandler(knowledge_base)
            print("   ⚠️ Rating handler initialized but DISABLED (LLM priority)")
        except TypeError:
            self.rating_handler = RatingScaleHandler()
            
        try:
            self.brand_association_handler = BrandAssociationHandler(knowledge_base)
            print("   ✅ Brand Association handler (for complex matching)")
        except TypeError:
            self.brand_association_handler = BrandAssociationHandler()
        
        print("\n   📊 AUTOMATION PRIORITY ORDER:")
        print("   🎯 PAGE ORCHESTRATOR - Handles structure & transitions")
        print("   1️⃣ LLM (GPT-4o-mini) - Handles 90% of questions")
        print("   2️⃣ Brand Selection - Complex matrices only")
        print("   3️⃣ Carousel - Complex UI patterns")
        print("   4️⃣ Brand Association - Complex matching")
        print("   ❌ Demographics - DISABLED (LLM handles)")
        print("   ❌ Rating Scales - DISABLED (LLM handles)")
        print("   ❌ Multi-Question - DISABLED (orchestrator handles)")
        print("")
    
    async def take_screenshot(self, page):
        """Take screenshot and return base64 encoded string"""
        try:
            screenshot = await page.screenshot()
            import base64
            return base64.b64encode(screenshot).decode('utf-8')
        except Exception as e:
            print(f"   ⚠️ Screenshot error: {e}")
            return None
    
    async def handle_page(self, page, page_number: int):
        """
        Enhanced page handling with learning integration
        Records manual interventions when automation fails
        """
        result = {'success': False, 'reason': 'not_attempted'}
        
        try:
            # Get question details
            question_data = await self._analyze_question(page)
            question_text = question_data.get('question_text', '')
            element_type = question_data.get('element_type', 'unknown')
            
            # Try automation
            result = await self.attempt_automation_with_orchestrator(
                page, 
                None,  # handler_factory if you have one
                None,  # vision_result if available
                page_number
            )
            
            # If automation failed, record manual intervention
            if not result.get('success'):
                print("\n⏸️  MANUAL INTERVENTION REQUIRED")
                print(f"   Question: {question_text[:100]}...")
                print(f"   Reason: {result.get('reason', 'unknown')}")
                
                # Wait for user to manually answer
                manual_answer = await self._wait_for_manual_answer(page, element_type)
                
                if manual_answer and self.llm:
                    # Record for learning
                    self.llm.record_manual_intervention(
                        question_text,
                        manual_answer,
                        element_type
                    )
                    print(f"   📝 Manual intervention recorded: {manual_answer}")
                else:
                    print("   ⚠️ Could not capture manual answer")
        
        except Exception as e:
            print(f"   ❌ Page handling error: {e}")
            result = {'success': False, 'reason': f'error: {str(e)}'}
        
        return result
    
    async def complete_survey(self, survey_url: str, browser_manager=None):
        """
        Complete survey with session saving
        Saves learning session at the end
        Note: Navigation is handled by main runner (quenito_main.py)
        """
        
        success = False
        
        try:
            # Your survey handling logic here
            # Main runner will handle navigation with its superior _click_next() method
            pass
            
        except Exception as e:
            print(f"❌ Survey completion error: {e}")
            
        finally:
            # ALWAYS save learning session at the end
            if self.llm:
                print("\n💾 Saving learning session...")
                self.llm.save_session()
                
                # Show learning progress
                stats = self.llm.get_learning_stats()
                print(f"\n📊 Learning Progress:")
                print(f"   Total Q&As learned: {stats['learned_responses']['total']}")
                print(f"   High confidence: {stats['learned_responses']['high_confidence']}")
                print(f"   Patterns: {stats['patterns']['total']}")
                print(f"   This session automated: {stats['current_session']['automated']}")
                print(f"   This session manual: {stats['current_session']['manual']}")
        
        return success
    
    async def _wait_for_manual_answer(self, page, element_type: str):
        """
        Helper to detect what the user entered manually
        Waits for user input and tries to capture the value
        """
        try:
            # Give user time to answer
            print("   ⏳ Please answer manually, then press Enter...")
            input()  # Wait for user confirmation
            
            # Try to capture what was entered based on element type
            if element_type == "text":
                # Find filled text input
                inputs = await page.query_selector_all('input[type="text"], input[type="number"]')
                for inp in inputs:
                    value = await inp.input_value()
                    if value and value.strip():
                        return value.strip()
            
            elif element_type == "radio":
                # Find selected radio
                radios = await page.query_selector_all('input[type="radio"]:checked')
                for radio in radios:
                    # Try to get label
                    radio_id = await radio.get_attribute('id')
                    if radio_id:
                        label = await page.query_selector(f'label[for="{radio_id}"]')
                        if label:
                            return await label.inner_text()
                    # Try value attribute
                    value = await radio.get_attribute('value')
                    if value:
                        return value
            
            elif element_type == "checkbox":
                # Find all checked checkboxes
                checked = []
                checkboxes = await page.query_selector_all('input[type="checkbox"]:checked')
                for checkbox in checkboxes:
                    # Try to get label
                    checkbox_id = await checkbox.get_attribute('id')
                    if checkbox_id:
                        label = await page.query_selector(f'label[for="{checkbox_id}"]')
                        if label:
                            text = await label.inner_text()
                            if text.strip():
                                checked.append(text.strip())
                    # Try value attribute as fallback
                    if not checked:
                        value = await checkbox.get_attribute('value')
                        if value:
                            checked.append(value)
                
                if checked:
                    return checked if len(checked) > 1 else checked[0]
            
            elif element_type in ["select", "dropdown"]:
                # Find selected option
                selects = await page.query_selector_all('select')
                for select in selects:
                    selected_option = await select.query_selector('option:checked')
                    if selected_option:
                        text = await selected_option.inner_text()
                        if text and text.strip():
                            return text.strip()
            
            elif element_type == "textarea":
                # Find filled textarea
                textareas = await page.query_selector_all('textarea')
                for textarea in textareas:
                    value = await textarea.input_value()
                    if value and value.strip():
                        return value.strip()
            
        except Exception as e:
            print(f"   ⚠️ Error capturing manual answer: {e}")
        
        return None
    
    # ========== EXISTING METHODS CONTINUE BELOW ==========
    
    async def attempt_automation_with_orchestrator(self, page, handler_factory, 
                                                  vision_result: Optional[Dict], 
                                                  question_num: int) -> Dict[str, Any]:
        """
        NEW METHOD: Attempt automation with Page Orchestrator integration
        Handles multi-question pages, transitions, and completion detection
        """
        
        # Take screenshot for vision analysis
        screenshot = await self.take_screenshot(page)
        
        # If we have vision service and screenshot, use orchestrator
        if self.vision_service and screenshot:
            print("\n🎯 PAGE ORCHESTRATOR ACTIVE")
            
            # Create orchestrator instance
            orchestrator = PageOrchestrator(
                self,
                self.llm,
                self.vision_service,
                page
            )
            
            # Let orchestrator handle the page
            result = await orchestrator.handle_page(screenshot)
            
            # Check orchestrator result
            if result.get('status') == 'complete':
                # Survey is done!
                print("🎉 SURVEY COMPLETED - Stopping automation")
                return {
                    'success': True,
                    'handler_used': 'PageOrchestrator',
                    'response_value': 'Survey Complete',
                    'confidence': 1.0,
                    'reason': 'survey_complete',
                    'stop_automation': True
                }
                
            elif result.get('status') == 'transition':
                # Transition page handled
                print("🔄 Transition page handled")
                return {
                    'success': True,
                    'handler_used': 'PageOrchestrator',
                    'response_value': 'Transition',
                    'confidence': 1.0,
                    'reason': 'transition_page'
                }
                
            elif result.get('status') == 'success':
                # Multi-question page handled
                automated_count = len(result.get('automated', []))
                manual_count = len(result.get('manual', []))
                
                if automated_count > 0:
                    return {
                        'success': True,
                        'handler_used': 'PageOrchestrator',
                        'response_value': f'{automated_count} questions automated',
                        'confidence': 0.9,
                        'reason': 'multi_question_handled',
                        'partial_manual': manual_count > 0
                    }
            
            # If orchestrator says use standard flow, continue below
            elif result.get('status') != 'use_standard_flow':
                # Some other orchestrator result
                return {
                    'success': False,
                    'handler_used': 'PageOrchestrator',
                    'response_value': None,
                    'confidence': 0,
                    'reason': result.get('status', 'orchestrator_unknown')
                }
        
        # Fall through to standard automation if orchestrator doesn't handle it
        return await self.attempt_automation(page, handler_factory, vision_result, question_num)
    
    # [ALL YOUR OTHER EXISTING METHODS REMAIN THE SAME BELOW]
    # Including: attempt_automation, _apply_llm_response, _analyze_question, 
    # find_matching_age_range, _apply_response, etc.
    
    async def attempt_automation(self, page, handler_factory, 
                                vision_result: Optional[Dict], 
                                question_num: int) -> Dict[str, Any]:
        """
        Original automation method - now called AFTER orchestrator check
        Attempt automation - LLM FIRST, then specialized handlers for complex cases
        """
        
        result = {
            'success': False,
            'handler_used': None,
            'response_value': None,
            'confidence': 0,
            'reason': 'not_attempted'
        }
        
        # Extract question details first
        question_data = await self._analyze_question(page)
        question_text = question_data.get('question_text', '')
        element_type = question_data.get('element_type', 'unknown')
        
        print(f"   🔍 Question: {question_text[:100]}...")
        print(f"   📋 Element type: {element_type}")
        
        # 🎯 PRIORITY 1: TRY LLM FIRST! (Handles 90% of questions)
        if self.llm:
            try:
                # Get options for radio/dropdown/checkbox
                options = []
                if element_type in ["radio", "dropdown", "select", "checkbox"]:
                    if element_type == "radio":
                        labels = await page.query_selector_all('label')
                        for label in labels:
                            text = await label.inner_text()
                            if text.strip() and text.strip() != question_text:
                                options.append(text.strip())
                    elif element_type in ["dropdown", "select"]:
                        select = await page.query_selector('select')
                        if select:
                            option_elements = await select.query_selector_all('option')
                            for opt in option_elements:
                                text = await opt.inner_text()
                                if text.strip() and text.strip() not in ['', 'Select', 'Please select', '--']:
                                    options.append(text.strip())
                    elif element_type == "checkbox":
                        # Get checkbox options
                        checkboxes = await page.query_selector_all('input[type="checkbox"]')
                        for checkbox in checkboxes:
                            # Try to get label
                            checkbox_id = await checkbox.get_attribute('id')
                            if checkbox_id:
                                label = await page.query_selector(f'label[for="{checkbox_id}"]')
                                if label:
                                    text = await label.inner_text()
                                    if text.strip():
                                        options.append(text.strip())
                            # Also try parent label
                            parent = await checkbox.evaluate_handle('el => el.parentElement')
                            if parent:
                                parent_text = await parent.inner_text()
                                if parent_text.strip() and parent_text.strip() not in options:
                                    options.append(parent_text.strip())
                
                if options:
                    print(f"   📋 Options: {options[:5]}...")  # First 5 options
                
                # Build context for LLM with vision insights
                llm_context = {
                    "question": question_text,
                    "vision_analysis": vision_result,
                    "element_type": element_type,
                    "options": options
                }
                
                # Use enhanced method if vision available, otherwise standard
                if vision_result and vision_result.get('confidence_rating', 0) > 70:
                    llm_response = await self.llm.get_response_with_context(llm_context)
                else:
                    llm_response = await self.llm.get_response(
                        question_text,
                        options if options else None,
                        element_type
                    )
                
                if llm_response['success']:
                    success = await self._apply_llm_response(
                        page,
                        llm_response['value'],
                        element_type,
                        options  # Pass options for fallback logic
                    )
                    
                    if success:
                        print(f"   🎉 LLM AUTOMATED: {llm_response['value']}")
                        
                        # Record successful automation for learning
                        if self.llm and hasattr(self.llm, 'learning'):
                            self.llm.learning.record_successful_automation(
                                question_text,
                                llm_response['value'],
                                element_type,
                                llm_response.get('confidence', 0.85)
                            )
                        
                        # Track for session history
                        if not hasattr(self, 'qa_history'):
                            self.qa_history = []
                        
                        self.qa_history.append({
                            "question": question_text[:100],
                            "answer": llm_response['value'],
                            "type": element_type,
                            "confidence": llm_response['confidence']
                        })
                        
                        # Record success for learning
                        self.confidence_manager.record_automation_result(
                            'LLM-GPT4o-mini',
                            'llm',
                            llm_response['confidence'],
                            True
                        )
                        
                        return {
                            'success': True,
                            'handler_used': 'LLM-GPT4o-mini',
                            'response_value': llm_response['value'],
                            'confidence': llm_response['confidence'],
                            'reason': 'llm_automated'
                        }
                    else:
                        print(f"   ⚠️ LLM gave answer but couldn't apply it: {llm_response['value']}")
                        
            except Exception as e:
                print(f"   ⚠️ LLM attempt error: {e}")
        
        # [REST OF YOUR EXISTING AUTOMATION CODE CONTINUES HERE]
        # Including all the handler checks, fallback logic, etc.
        
        # 🎯 PRIORITY 2: CHECK BRAND AWARENESS/SELECTION (Keep - complex logic)
        if 'which of the following' in question_text.lower() or 'aware of' in question_text.lower():
            print("   🏢 Brand selection detected!")
            success = await self.brand_selection_handler.detect_and_handle_brand_selection(
                page, 
                question_text
            )
            if success:
                return {
                    'success': True,
                    'handler_used': 'BrandSelectionHandler',
                    'response_value': 'Brands selected',
                    'confidence': 0.85,
                    'reason': 'brand_selection_automated'
                }
        
        # [Continue with rest of existing attempt_automation method...]
        
        return result
    
    # [Include all your other existing methods here: _apply_llm_response, _analyze_question, etc.]
    async def _apply_llm_response(self, page, value: str, element_type: str, 
                                  options: Optional[List[str]] = None) -> bool:
        """Apply LLM's response to the page - ENHANCED WITH INDUSTRY SCREENING FALLBACK"""
        try:
            print(f"   🔧 Applying: {value} to {element_type}")
            
            if element_type == "text":
                # Text input
                inputs = await page.query_selector_all('input[type="text"], input[type="number"]')
                for inp in inputs:
                    if await inp.is_visible():
                        await inp.click()
                        await page.wait_for_timeout(100)
                        await inp.fill('')
                        await inp.fill(value)
                        await page.wait_for_timeout(200)
                        print(f"   ✅ Filled text input")
                        return True
                        
            elif element_type == "radio":
                # Radio button - try exact match
                try:
                    await page.click(f'label:has-text("{value}")')
                    await page.wait_for_timeout(200)
                    print(f"   ✅ Selected radio option")
                    return True
                except:
                    # Try partial match
                    labels = await page.query_selector_all('label')
                    for label in labels:
                        text = await label.inner_text()
                        if value.lower() in text.lower() or text.lower() in value.lower():
                            await label.click()
                            await page.wait_for_timeout(200)
                            print(f"   ✅ Selected radio via partial match")
                            return True
                            
            elif element_type == "dropdown":
                # Dropdown
                selects = await page.query_selector_all('select')
                for select in selects:
                    if await select.is_visible():
                        try:
                            await select.select_option(label=value)
                            await page.wait_for_timeout(200)
                            print(f"   ✅ Selected dropdown option")
                            return True
                        except:
                            # Try by value attribute
                            await select.select_option(value=value)
                            await page.wait_for_timeout(200)
                            print(f"   ✅ Selected dropdown by value")
                            return True
                            
            elif element_type == "checkbox":
                # ENHANCED CHECKBOX HANDLING WITH INDUSTRY SCREENING FALLBACK
                values_to_select = value if isinstance(value, list) else [value]
                success_count = 0
                
                for val in values_to_select:
                    # If it's an index (old behavior), skip
                    if isinstance(val, int):
                        print(f"   ⚠️ Skipping index-based selection: {val}")
                        continue
                    
                    # Try different selection methods
                    clicked = False
                    try:
                        # Method 1: Click label with text
                        await page.click(f'label:has-text("{val}")')
                        await page.wait_for_timeout(200)
                        success_count += 1
                        clicked = True
                        print(f"   ✅ Checked checkbox: {val}")
                    except:
                        # Method 2: Find checkbox by value
                        try:
                            await page.click(f'input[type="checkbox"][value*="{val}"]')
                            await page.wait_for_timeout(200)
                            success_count += 1
                            clicked = True
                            print(f"   ✅ Checked checkbox by value: {val}")
                        except:
                            # Method 3: Partial text match
                            labels = await page.query_selector_all('label')
                            for label in labels:
                                text = await label.inner_text()
                                if val.lower() in text.lower() or text.lower() in val.lower():
                                    await label.click()
                                    await page.wait_for_timeout(200)
                                    success_count += 1
                                    clicked = True
                                    print(f"   ✅ Checked checkbox via partial match: {val}")
                                    break
                    
                    # INDUSTRY SCREENING FALLBACK
                    if not clicked and "retail" in val.lower():
                        # Retail not found, look for "None of the above"
                        print("   🔄 Retail not available, looking for 'None of the above'...")
                        
                        labels = await page.query_selector_all('label')
                        for label in labels:
                            text = await label.inner_text()
                            if "none" in text.lower() and ("above" in text.lower() or "these" in text.lower()):
                                await label.click()
                                await page.wait_for_timeout(200)
                                success_count += 1
                                print("   ✅ Selected 'None of the above' (retail not in list)")
                                break
                        
                        # Also check for checkboxes with value containing "none"
                        if success_count == 0:
                            try:
                                await page.click('input[type="checkbox"][value*="none" i]')
                                await page.wait_for_timeout(200)
                                success_count += 1
                                print("   ✅ Selected 'None' checkbox (retail not available)")
                            except:
                                pass
                
                return success_count > 0
                    
        except Exception as e:
            print(f"   ❌ Error applying LLM response: {e}")
        
        return False
    
    async def _analyze_question(self, page) -> Dict[str, Any]:
        """Analyze current question - ENHANCED demographics detection"""
        data = {
            'question_text': '',
            'question_type': '',
            'element_type': 'unknown'
        }
        
        # Extract question text
        selectors = ['h2:has-text("?")', 'h3:has-text("?")', '.question-text', 'legend', 'h2', 'h3', 'p']
        for selector in selectors:
            try:
                elem = await page.query_selector(selector)
                if elem:
                    text = await elem.inner_text()
                    if len(text) > 10:
                        data['question_text'] = text.strip()
                        if '?' in text:  # Prefer questions with ?
                            break
            except:
                continue
        
        # Get full page text for better context
        try:
            page_text = await page.inner_text('body')
            page_text_lower = page_text.lower()
        except:
            page_text_lower = data['question_text'].lower()
        
        # Detect element type first
        if await page.query_selector('input[type="radio"]'):
            data['element_type'] = 'radio'
        elif await page.query_selector('input[type="checkbox"]'):
            data['element_type'] = 'checkbox'
        elif await page.query_selector('select'):
            data['element_type'] = 'select'
        elif await page.query_selector('input[type="text"], input[type="number"]'):
            data['element_type'] = 'text'
        elif await page.query_selector('textarea'):
            data['element_type'] = 'textarea'
        elif await page.query_selector('input[type="range"]'):
            data['element_type'] = 'slider'
        
        # ENHANCED: Classify question with better demographics detection
        text_lower = data['question_text'].lower()
        
        # Check for gender questions - ENHANCED!
        if ('are you' in text_lower and data['element_type'] == 'radio'):
            # Check if Male/Female options are present
            if 'male' in page_text_lower and 'female' in page_text_lower:
                data['question_type'] = 'gender'
                print(f"   🎯 Detected gender question via 'Are you?' + Male/Female options")
            else:
                data['question_type'] = 'general'
        elif 'gender' in text_lower or 'sex' in text_lower:
            data['question_type'] = 'gender'
        elif 'age' in text_lower or 'old' in text_lower or 'birth' in text_lower:
            data['question_type'] = 'age'
        elif 'postcode' in text_lower or 'postal' in text_lower or 'zip' in text_lower:
            data['question_type'] = 'postcode'
        elif 'state' in text_lower or 'territory' in text_lower or 'region' in text_lower:
            data['question_type'] = 'state'
        elif 'income' in text_lower or 'salary' in text_lower or 'earn' in text_lower:
            data['question_type'] = 'income'
        elif 'employ' in text_lower or 'occupation' in text_lower or 'work' in text_lower:
            data['question_type'] = 'employment'
        elif 'household' in text_lower or 'live with' in text_lower:
            data['question_type'] = 'household'
        elif 'children' in text_lower or 'kids' in text_lower:
            data['question_type'] = 'children'
        elif 'education' in text_lower or 'qualification' in text_lower:
            data['question_type'] = 'education'
        elif 'marital' in text_lower or 'married' in text_lower:
            data['question_type'] = 'marital'
        # Check for state dropdown by looking at options
        elif data['element_type'] == 'select' and any(state in page_text_lower for state in ['new south wales', 'victoria', 'queensland']):
            data['question_type'] = 'state'
            print(f"   🎯 Detected state question via dropdown options")
        else:
            data['question_type'] = 'general'
        
        return data
    
    def find_matching_age_range(self, actual_age: int, age_ranges: List[str]) -> Optional[str]:
        """
        Find the age range that contains the actual age.
        Handles various formats: "45-54", "45 to 54", "45-49", "40-49", etc.
        """
        import re
        
        for age_range in age_ranges:
            # Extract numbers from the range
            numbers = re.findall(r'\d+', age_range)
            
            if len(numbers) >= 2:
                try:
                    min_age = int(numbers[0])
                    max_age = int(numbers[1])
                    
                    # Check if actual age falls within this range
                    if min_age <= actual_age <= max_age:
                        print(f"   🎯 Age {actual_age} matches range: {age_range}")
                        return age_range
                        
                except ValueError:
                    continue
            
            # Handle "65+" or "75+" format
            elif len(numbers) == 1 and ('+' in age_range or 'over' in age_range.lower()):
                try:
                    min_age = int(numbers[0])
                    if actual_age >= min_age:
                        print(f"   🎯 Age {actual_age} matches range: {age_range}")
                        return age_range
                except ValueError:
                    continue
            
            # Handle "Under 18" format
            elif 'under' in age_range.lower() and len(numbers) == 1:
                try:
                    max_age = int(numbers[0])
                    if actual_age < max_age:
                        print(f"   🎯 Age {actual_age} matches range: {age_range}")
                        return age_range
                except ValueError:
                    continue
        
        return None

    async def _apply_response(self, page, response_value: str, element_type: str) -> bool:
        """Apply response to page elements - ENHANCED for all types with FIXES"""
        # [Your existing _apply_response method code here]
        try:
            print(f"   🔧 Applying {response_value} to {element_type} element")
            
            # ENHANCED TEXT INPUT HANDLING
            if element_type == 'text' or element_type == 'number' or element_type == 'textarea':
                # Find all text/number inputs
                inputs = await page.query_selector_all('input[type="text"], input[type="number"], textarea')
                
                for input_elem in inputs:
                    try:
                        # Check if visible
                        is_visible = await input_elem.is_visible()
                        if is_visible:
                            # Click to focus
                            await input_elem.click()
                            await page.wait_for_timeout(100)
                            
                            # Clear existing value
                            await input_elem.fill('')
                            await page.wait_for_timeout(50)
                            
                            # Fill new value
                            await input_elem.fill(str(response_value))
                            print(f"   ✅ Filled text input with: {response_value}")
                            await page.wait_for_timeout(200)
                            return True
                    except Exception as e:
                        print(f"   ⚠️ Error with input element: {e}")
                        continue
                
                print(f"   ❌ No visible text/number inputs found")
                return False
            
            # [Continue with rest of your existing _apply_response method]
            
        except Exception as e:
            print(f"   ❌ Error applying response: {e}")
            import traceback
            traceback.print_exc()
        
        return False