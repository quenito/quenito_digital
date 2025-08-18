#!/usr/bin/env python3
"""
🎯 Page Orchestrator v3.0 - NOW WITH LLM POWER!
Coordinates multiple handlers on multi-question pages using GPT-4o-mini.
Shows which handlers contribute to page completion.
"""
from typing import List, Dict, Any, Tuple, Optional
import time

class PageOrchestrator:
    """
    Orchestrates multiple handlers to work together on the same page.
    Now with LLM intelligence for better automation!
    """
    
    def __init__(self, handler_factory, page, knowledge_base):
        self.handler_factory = handler_factory
        self.page = page
        self.kb = knowledge_base
        self.handled_elements = []
        self.handlers_used = []  # Track which handlers were used
        
        # Check if LLM is available through automation service
        self.llm = None
        try:
            if hasattr(handler_factory, 'automation_service'):
                self.llm = handler_factory.automation_service.llm
            elif hasattr(knowledge_base, 'automation_service'):
                self.llm = knowledge_base.automation_service.llm
        except:
            pass
        
        if self.llm:
            print("   🧠 PageOrchestrator: LLM integration active!")
        
    async def analyze_page(self) -> Dict[str, Any]:
        """
        Analyze page to detect all questions present.
        Returns a map of questions to appropriate handlers.
        """
        page_analysis = {
            "questions_detected": [],
            "handlers_needed": {},
            "is_multi_question": False,
            "question_elements": {},
            "handler_assignments": {}  # Track handler assignments
        }
        
        # Check for age inputs (text or number)
        age_inputs = await self.page.query_selector_all('input[type="text"][name*="age"], input[type="number"][name*="age"], input[placeholder*="age"], input[placeholder*="Age"], input[placeholder*="years"]')
        if age_inputs:
            for elem in age_inputs:
                if await elem.is_visible():
                    page_analysis["questions_detected"].append("age")
                    page_analysis["handlers_needed"]["age"] = "demographics"
                    page_analysis["question_elements"]["age"] = elem
                    page_analysis["handler_assignments"]["age"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
                    break
        
        # Check for gender (radio buttons or dropdown)
        gender_radios = await self.page.query_selector_all('input[type="radio"][name*="gender"], input[type="radio"][value="Male"], input[type="radio"][value="Female"]')
        if gender_radios:
            page_analysis["questions_detected"].append("gender")
            page_analysis["handlers_needed"]["gender"] = "demographics"
            page_analysis["question_elements"]["gender"] = gender_radios
            page_analysis["handler_assignments"]["gender"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
        else:
            # Check for gender dropdown
            gender_select = await self.page.query_selector('select[name*="gender"]')
            if gender_select and await gender_select.is_visible():
                page_analysis["questions_detected"].append("gender")
                page_analysis["handlers_needed"]["gender"] = "demographics"
                page_analysis["question_elements"]["gender"] = gender_select
                page_analysis["handler_assignments"]["gender"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
        
        # Check for postcode
        postcode_inputs = await self.page.query_selector_all('input[name*="postcode"], input[name*="zip"], input[placeholder*="postcode"], input[placeholder*="Postcode"]')
        if postcode_inputs:
            for elem in postcode_inputs:
                if await elem.is_visible():
                    page_analysis["questions_detected"].append("postcode")
                    page_analysis["handlers_needed"]["postcode"] = "demographics"
                    page_analysis["question_elements"]["postcode"] = elem
                    page_analysis["handler_assignments"]["postcode"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
                    break
        
        # Check for state/region dropdowns
        state_selects = await self.page.query_selector_all('select[name*="state"], select[name*="region"], select:has(option:text("New South Wales"))')
        if state_selects:
            for elem in state_selects:
                if await elem.is_visible():
                    page_analysis["questions_detected"].append("state")
                    page_analysis["handlers_needed"]["state"] = "demographics"
                    page_analysis["question_elements"]["state"] = elem
                    page_analysis["handler_assignments"]["state"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
                    break
        
        # Check for income dropdowns
        income_selects = await self.page.query_selector_all('select[name*="income"], select:has(option:text("$50,000"))')
        if income_selects:
            for elem in income_selects:
                if await elem.is_visible():
                    page_analysis["questions_detected"].append("income")
                    page_analysis["handlers_needed"]["income"] = "demographics"
                    page_analysis["question_elements"]["income"] = elem
                    page_analysis["handler_assignments"]["income"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
                    break
        
        # Check for employment/occupation
        employment_selects = await self.page.query_selector_all('select[name*="employ"], select[name*="occupation"], select[name*="work"]')
        if employment_selects:
            for elem in employment_selects:
                if await elem.is_visible():
                    page_analysis["questions_detected"].append("employment")
                    page_analysis["handlers_needed"]["employment"] = "demographics"
                    page_analysis["question_elements"]["employment"] = elem
                    page_analysis["handler_assignments"]["employment"] = "LLM-GPT4o-mini" if self.llm else "DemographicsHandler"
                    break
        
        # Check for multi-select checkboxes (brands, products, etc)
        checkbox_groups = await self.page.query_selector_all('input[type="checkbox"][name*="brand"], input[type="checkbox"][name*="product"]')
        if len(checkbox_groups) > 3:  # Multiple checkboxes suggest multi-select
            page_analysis["questions_detected"].append("multi_select")
            page_analysis["handlers_needed"]["multi_select"] = "multi_select"
            page_analysis["question_elements"]["multi_select"] = checkbox_groups
            page_analysis["handler_assignments"]["multi_select"] = "LLM-GPT4o-mini" if self.llm else "MultiSelectHandler"
        
        # Determine if multi-question
        total_questions = len(page_analysis["questions_detected"])
        page_analysis["is_multi_question"] = total_questions > 1
        
        if total_questions > 0:
            print(f"📊 Page Analysis: {total_questions} question(s) detected")
            print(f"   Questions: {', '.join(page_analysis['questions_detected'])}")
            
            # Show handler assignments
            unique_handlers = set(page_analysis["handler_assignments"].values())
            print(f"   🤖 Handlers Required: {', '.join(unique_handlers)}")
        
        return page_analysis
    
    async def handle_multi_question_page(self) -> int:
        """
        Orchestrate multiple handlers to complete all questions on the page.
        Returns number of questions successfully handled (0 if not multi-question).
        """
        # Reset tracking
        self.handlers_used = []
        
        # Analyze what's on the page
        page_analysis = await self.analyze_page()
        
        if not page_analysis["is_multi_question"]:
            # Not a multi-question page
            return 0
            
        print(f"\n🎯 MULTI-QUESTION PAGE ORCHESTRATION")
        print(f"{'='*50}")
        print(f"📝 Questions Found: {len(page_analysis['questions_detected'])}")
        
        # Show handler coordination plan
        handler_plan = {}
        for q in page_analysis["questions_detected"]:
            handler_name = page_analysis["handler_assignments"].get(q, "Unknown")
            if handler_name not in handler_plan:
                handler_plan[handler_name] = []
            handler_plan[handler_name].append(q)
        
        print(f"\n🤖 HANDLER COORDINATION PLAN:")
        for handler, questions in handler_plan.items():
            print(f"   • {handler}: {', '.join(questions)}")
        
        print(f"\n📋 EXECUTING ORCHESTRATION:")
        print(f"{'-'*50}")
        
        success_count = 0
        
        # Handle each question in sequence
        for i, question_type in enumerate(page_analysis["questions_detected"], 1):
            handler_name = page_analysis["handler_assignments"].get(question_type, "Unknown")
            print(f"\n   [{i}/{len(page_analysis['questions_detected'])}] {question_type.upper()}")
            print(f"       Handler: {handler_name}")
            
            # Handle based on question type
            try:
                if question_type == "age":
                    success = await self.handle_age_input(page_analysis["question_elements"].get("age"))
                elif question_type == "gender":
                    success = await self.handle_gender_selection(page_analysis["question_elements"].get("gender"))
                elif question_type == "postcode":
                    success = await self.handle_postcode_input(page_analysis["question_elements"].get("postcode"))
                elif question_type == "state":
                    success = await self.handle_state_dropdown(page_analysis["question_elements"].get("state"))
                elif question_type == "income":
                    success = await self.handle_income_dropdown(page_analysis["question_elements"].get("income"))
                elif question_type == "employment":
                    success = await self.handle_employment_dropdown(page_analysis["question_elements"].get("employment"))
                elif question_type == "multi_select":
                    success = await self.handle_multi_select(page_analysis["question_elements"].get("multi_select"))
                else:
                    success = False
                    
                if success:
                    success_count += 1
                    print(f"       ✅ Success!")
                    if handler_name not in self.handlers_used:
                        self.handlers_used.append(handler_name)
                else:
                    print(f"       ⚠️ Manual input needed")
                    
            except Exception as e:
                print(f"       ❌ Error: {e}")
        
        print(f"\n{'-'*50}")
        
        # Summary
        if success_count == len(page_analysis["questions_detected"]):
            print(f"✅ ORCHESTRATION COMPLETE!")
            print(f"   • Questions Handled: {success_count}/{len(page_analysis['questions_detected'])}")
            print(f"   • Handlers Used: {', '.join(self.handlers_used)}")
            print(f"   • Status: Ready to proceed")
            
            # Click the next button
            await self.click_next_button()
            return success_count
            
        elif success_count > 0:
            print(f"⚠️ PARTIAL ORCHESTRATION")
            print(f"   • Questions Handled: {success_count}/{len(page_analysis['questions_detected'])}")
            print(f"   • Handlers Used: {', '.join(self.handlers_used)}")
            print(f"   • Status: Manual completion required")
            return 0  # Return 0 to indicate incomplete
            
        else:
            print(f"❌ ORCHESTRATION FAILED")
            print(f"   • No questions could be automated")
            print(f"   • Status: Full manual input required")
            return 0
    
    async def handle_age_input(self, element) -> bool:
        """Handle age input field - USING LLM!"""
        try:
            # Try LLM first
            if self.llm and element:
                from services.llm_automation_service import LLMAutomationService
                
                # Get the question text if available
                question_text = "What is your age?"
                try:
                    label = await self.get_label_for_element(element)
                    if label:
                        question_text = label
                except:
                    pass
                
                response = await self.llm.get_response(
                    question_text,
                    None,
                    "text"
                )
                
                if response['success']:
                    await element.click()
                    await element.fill('')
                    await element.fill(str(response['value']))
                    await self.page.wait_for_timeout(300)
                    print(f"       🤖 LLM filled: {response['value']}")
                    return True
            
            # Fallback to profile
            age = self.kb.user_profile.get_response("age") if self.kb else "45"
            if age and element:
                await element.fill(str(age))
                await self.page.wait_for_timeout(300)
                return True
                
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    async def handle_gender_selection(self, elements) -> bool:
        """Handle gender selection - USING LLM!"""
        try:
            # Try LLM first
            if self.llm:
                # Get available options
                options = []
                if isinstance(elements, list):
                    for radio in elements:
                        # Get the label for this radio
                        label = await self.get_label_for_element(radio)
                        if label:
                            options.append(label)
                        else:
                            # Try to get value
                            value = await radio.get_attribute('value')
                            if value:
                                options.append(value)
                
                response = await self.llm.get_response(
                    "What is your gender?",
                    options if options else ["Male", "Female"],
                    "radio"
                )
                
                if response['success']:
                    # Try to click the right option
                    if isinstance(elements, list):
                        for radio in elements:
                            label = await self.get_label_for_element(radio)
                            value = await radio.get_attribute('value')
                            
                            if (label and label.lower() == response['value'].lower()) or \
                               (value and value.lower() == response['value'].lower()):
                                await radio.click()
                                await self.page.wait_for_timeout(300)
                                print(f"       🤖 LLM selected: {response['value']}")
                                return True
                    
                    # Try clicking by label text
                    try:
                        await self.page.click(f'label:has-text("{response["value"]}")')
                        await self.page.wait_for_timeout(300)
                        print(f"       🤖 LLM selected: {response['value']}")
                        return True
                    except:
                        pass
            
            # Fallback to profile
            gender = self.kb.user_profile.get_response("gender") if self.kb else "Male"
            if not gender:
                return False
                
            if isinstance(elements, list):
                for radio in elements:
                    value = await radio.get_attribute('value')
                    if value and value.lower() == gender.lower():
                        await radio.click()
                        await self.page.wait_for_timeout(300)
                        return True
                
                # Try clicking label
                try:
                    await self.page.click(f'label:has-text("{gender}")')
                    await self.page.wait_for_timeout(300)
                    return True
                except:
                    pass
                    
            elif elements:
                await elements.select_option(label=gender)
                await self.page.wait_for_timeout(300)
                return True
                
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    async def handle_postcode_input(self, element) -> bool:
        """Handle postcode input field - USING LLM!"""
        try:
            if self.llm and element:
                # Get the question text
                question_text = "What is your postcode?"
                try:
                    label = await self.get_label_for_element(element)
                    if label:
                        question_text = label
                except:
                    pass
                
                response = await self.llm.get_response(
                    question_text,
                    None,
                    "text"
                )
                
                if response['success']:
                    await element.click()
                    await element.fill('')
                    await element.fill(str(response['value']))
                    await self.page.wait_for_timeout(300)
                    print(f"       🤖 LLM filled: {response['value']}")
                    return True
            
            # Fallback to profile
            postcode = self.kb.user_profile.get_response("postcode") if self.kb else "2217"
            if postcode and element:
                await element.fill(str(postcode))
                await self.page.wait_for_timeout(300)
                return True
                
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    async def handle_state_dropdown(self, element) -> bool:
        """Handle state/region dropdown - USING LLM!"""
        try:
            if self.llm and element:
                # Get dropdown options
                options = []
                option_elements = await element.query_selector_all('option')
                for opt in option_elements:
                    text = await opt.inner_text()
                    if text.strip():
                        options.append(text.strip())
                
                response = await self.llm.get_response(
                    "What is your state?",
                    options,
                    "dropdown"
                )
                
                if response['success']:
                    try:
                        await element.select_option(label=response['value'])
                        await self.page.wait_for_timeout(300)
                        print(f"       🤖 LLM selected: {response['value']}")
                        return True
                    except:
                        # Try by value
                        await element.select_option(value=response['value'])
                        await self.page.wait_for_timeout(300)
                        return True
            
            # Fallback to profile
            state = self.kb.user_profile.get_response("state") if self.kb else "NSW"
            if not state or not element:
                return False
                
            state_mappings = {
                'NSW': 'New South Wales',
                'VIC': 'Victoria',
                'QLD': 'Queensland',
                'WA': 'Western Australia',
                'SA': 'South Australia',
                'TAS': 'Tasmania',
                'ACT': 'Australian Capital Territory',
                'NT': 'Northern Territory'
            }
            
            try:
                await element.select_option(value=state)
                await self.page.wait_for_timeout(300)
                return True
            except:
                full_name = state_mappings.get(state, state)
                try:
                    await element.select_option(label=full_name)
                    await self.page.wait_for_timeout(300)
                    return True
                except:
                    pass
                    
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    async def handle_income_dropdown(self, element) -> bool:
        """Handle income dropdown - USING LLM!"""
        try:
            if self.llm and element:
                # Get dropdown options
                options = []
                option_elements = await element.query_selector_all('option')
                for opt in option_elements:
                    text = await opt.inner_text()
                    if text.strip() and '$' in text:  # Income options usually have $
                        options.append(text.strip())
                
                response = await self.llm.get_response(
                    "What is your household income?",
                    options,
                    "dropdown"
                )
                
                if response['success']:
                    # Try to select the option
                    for opt in option_elements:
                        text = await opt.inner_text()
                        if response['value'] in text or text in response['value']:
                            value = await opt.get_attribute('value')
                            if value:
                                await element.select_option(value=value)
                                await self.page.wait_for_timeout(300)
                                print(f"       🤖 LLM selected: {response['value']}")
                                return True
            
            # Fallback to profile
            income = self.kb.user_profile.get_response("income") or \
                    self.kb.user_profile.get_response("personal_income") or \
                    self.kb.user_profile.get_response("household_income")
            
            if income and element:
                options = await element.query_selector_all('option')
                for option in options:
                    text = await option.inner_text()
                    if income in text or text in income:
                        value = await option.get_attribute('value')
                        if value:
                            await element.select_option(value=value)
                            await self.page.wait_for_timeout(300)
                            return True
                            
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    async def handle_employment_dropdown(self, element) -> bool:
        """Handle employment/occupation dropdown - USING LLM!"""
        try:
            if self.llm and element:
                # Get dropdown options
                options = []
                option_elements = await element.query_selector_all('option')
                for opt in option_elements:
                    text = await opt.inner_text()
                    if text.strip():
                        options.append(text.strip())
                
                response = await self.llm.get_response(
                    "What is your employment status?",
                    options,
                    "dropdown"
                )
                
                if response['success']:
                    try:
                        await element.select_option(label=response['value'])
                        await self.page.wait_for_timeout(300)
                        print(f"       🤖 LLM selected: {response['value']}")
                        return True
                    except:
                        # Try partial match
                        for opt in option_elements:
                            text = await opt.inner_text()
                            if response['value'].lower() in text.lower() or text.lower() in response['value'].lower():
                                value = await opt.get_attribute('value')
                                if value:
                                    await element.select_option(value=value)
                                    await self.page.wait_for_timeout(300)
                                    return True
            
            # Fallback to profile
            employment = self.kb.user_profile.get_response("employment") or \
                        self.kb.user_profile.get_response("occupation")
            
            if employment and element:
                try:
                    await element.select_option(label=employment)
                    await self.page.wait_for_timeout(300)
                    return True
                except:
                    options = await element.query_selector_all('option')
                    for option in options:
                        text = await option.inner_text()
                        if employment.lower() in text.lower() or text.lower() in employment.lower():
                            value = await option.get_attribute('value')
                            if value:
                                await element.select_option(value=value)
                                await self.page.wait_for_timeout(300)
                                return True
                                
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    async def handle_multi_select(self, elements) -> bool:
        """Handle multi-select checkboxes - USING LLM!"""
        try:
            if self.llm and elements:
                # Get all checkbox options
                options = []
                for checkbox in elements:
                    label = await self.get_label_for_element(checkbox)
                    if label:
                        options.append(label)
                
                # For now, we'll select a few common ones
                # This could be enhanced with better prompting
                response = await self.llm.get_response(
                    "Select all that apply",
                    options[:10],  # Limit to first 10 for LLM
                    "checkbox"
                )
                
                if response['success']:
                    # Select the suggested options
                    # Note: For multi-select, we might need better logic
                    print(f"       🤖 LLM suggested: {response['value']}")
                    # For now, return False to handle manually
                    return False
            
            # Multi-select is complex, usually needs manual handling
            return False
            
        except Exception as e:
            print(f"       Error: {e}")
        return False
    
    def find_matching_age_range(self, actual_age: int, age_ranges: list) -> str:
        """Find the age range that contains the actual age - LOCAL HELPER"""
        import re
        
        for age_range in age_ranges:
            # Extract numbers from the range
            numbers = re.findall(r'\d+', age_range)
            
            if len(numbers) >= 2:
                try:
                    min_age = int(numbers[0])
                    max_age = int(numbers[1])
                    
                    if min_age <= actual_age <= max_age:
                        return age_range
                        
                except ValueError:
                    continue
            
            # Handle "65+" or "75+" format
            elif len(numbers) == 1 and ('+' in age_range or 'over' in age_range.lower()):
                try:
                    min_age = int(numbers[0])
                    if actual_age >= min_age:
                        return age_range
                except ValueError:
                    continue
            
            # Handle "Under 18" format
            elif 'under' in age_range.lower() and len(numbers) == 1:
                try:
                    max_age = int(numbers[0])
                    if actual_age < max_age:
                        return age_range
                except ValueError:
                    continue
        
        return None
    
    async def click_next_button(self):
        """Click the next/continue button after all questions are answered"""
        try:
            selectors = [
                'button:has-text("Next")',
                'button:has-text("NEXT")',
                'button:has-text("Continue")',
                'button:has-text("CONTINUE")',
                'input[type="submit"]',
                'button[type="submit"]'
            ]
            
            for selector in selectors:
                try:
                    button = await self.page.query_selector(selector)
                    if button and await button.is_visible():
                        await button.click()
                        print("   ➡️ Clicked NEXT button")
                        return
                except:
                    continue
                    
            print("   ⚠️ Could not find/click next button")
        except Exception as e:
            print(f"   ❌ Error clicking next: {e}")
    
    async def get_label_for_element(self, element) -> str:
        """Get the label text for a form element"""
        try:
            elem_id = await element.get_attribute('id')
            if elem_id:
                label = await self.page.query_selector(f'label[for="{elem_id}"]')
                if label:
                    return await label.inner_text()
            
            parent_text = await element.evaluate('''(el) => {
                const label = el.closest('label');
                return label ? label.textContent.trim() : '';
            }''')
            
            if parent_text:
                return parent_text
                
            prev_text = await element.evaluate('''(el) => {
                const prev = el.previousElementSibling;
                return prev && prev.tagName === 'LABEL' ? prev.textContent.trim() : '';
            }''')
            
            return prev_text or ""
            
        except:
            return ""