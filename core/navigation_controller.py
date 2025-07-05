"""
Navigation Controller Module
Handles page navigation, button detection, and consent handling.
"""

import time
import random


class NavigationController:
    """
    Manages page navigation and button detection with manual intervention fallback.
    """
    
    def __init__(self):
        self.navigation_stats = {
            "buttons_found_automatically": 0,
            "manual_navigation_required": 0,
            "consent_pages_handled": 0,
            "navigation_failures": []
        }
    
    def find_and_click_next_button(self, page, intervention_manager=None):
        """
        Enhanced next button detection with DONE button support and debugging.
        """
        print("🔍 Moving to next question or completing survey...")
        
        # Check if we're on the last question (look for Done button first)
        page_content = page.inner_text('body').lower()
        if 'done' in page_content or '3 of 3 answered' in page_content:
            print("🎯 Detected final question - looking specifically for Done button...")
            
            # Run debug to understand the Done button structure
            self.debug_done_button(page)
            return True
        
        # PRIORITY 1: Survey completion buttons (DONE, FINISH, SUBMIT)
        completion_selectors = [
            'button:has-text("Done")',
            'button:has-text("DONE")', 
            'input[type="submit"][value="Done"]',
            'input[value="DONE"]',
            'button:has-text("Finish")',
            'button:has-text("FINISH")',
            'button:has-text("Submit")',
            'button:has-text("SUBMIT")',
            'button:has-text("Complete")',
            'button:has-text("COMPLETE")',
            '[onclick*="done"]',
            '[onclick*="finish"]',
            '[onclick*="submit"]',
            '[onclick*="complete"]'
        ]
        
        # PRIORITY 2: Standard navigation buttons (NEXT, CONTINUE)
        navigation_selectors = [
            'button:has-text("Next")',
            'button:has-text("NEXT")',
            'input[type="submit"][value="NEXT"]',
            'input[value="NEXT"]', 
            'button:has-text("Continue")',
            'button:has-text("OK")',
            'input[type="submit"][value*="Next"]',
            'input[type="submit"][value*="Continue"]',
            '[onclick*="next"]',
            '[onclick*="Next"]'
        ]
        
        # Try completion buttons first
        print("🔍 Looking for survey completion buttons...")
        for selector in completion_selectors:
            try:
                buttons = page.query_selector_all(selector)
                for button in buttons:
                    if button.is_visible():
                        button_text = button.get_attribute('value') or button.inner_text() or 'DONE'
                        print(f"🎯 Found completion button: '{button_text.strip()}'")
                        button.click()
                        self._human_like_delay(2000, 3000)
                        self.navigation_stats["buttons_found_automatically"] += 1
                        
                        # After clicking completion button, check for survey completion
                        self._human_like_delay(3000, 5000)  # Wait for completion page
                        return True
            except Exception as e:
                print(f"❌ Error with completion selector {selector}: {e}")
                continue
        
        # Try standard navigation buttons  
        print("🔍 Looking for navigation buttons...")
        for selector in navigation_selectors:
            try:
                buttons = page.query_selector_all(selector)
                for button in buttons:
                    if button.is_visible():
                        button_text = button.get_attribute('value') or button.inner_text() or 'NEXT'
                        print(f"✅ Clicking navigation button: '{button_text.strip()}'")
                        button.click()
                        self._human_like_delay(2000, 3000)
                        self.navigation_stats["buttons_found_automatically"] += 1
                        return True
            except Exception as e:
                print(f"❌ Error with navigation selector {selector}: {e}")
                continue
        
        # Enhanced fallback with completion buttons
        fallback_selectors = [
            '*:has-text("Done")', '*:has-text("DONE")',
            '*:has-text("Finish")', '*:has-text("Submit")', 
            '*:has-text("NEXT")', '*:has-text("Next")',
            '*:has-text("Continue")', '*:has-text("Submit")',
            '[class*="done"]', '[class*="finish"]',
            '[class*="next"]', '[class*="continue"]',
            '[id*="done"]', '[id*="finish"]',
            '[id*="next"]', '[id*="continue"]'
        ]
        
        print("🔍 Trying enhanced fallback selectors...")
        for selector in fallback_selectors:
            try:
                elements = page.query_selector_all(selector)
                for element in elements:
                    if element.is_visible():
                        element_text = element.inner_text().strip()
                        print(f"✅ Clicking fallback element: '{element_text}'")
                        element.click()
                        self._human_like_delay(2000, 3000)
                        self.navigation_stats["buttons_found_automatically"] += 1
                        return True
            except Exception as e:
                continue
    
        # Manual intervention for next button
        print("❌ Could not find any next/continue button automatically")
        return self._request_navigation_assistance(page, intervention_manager)

    def handle_consent_agreement_page(self, page):
        """
        Handle consent/agreement pages with enhanced detection.
        """
        print("🔍 Checking for consent/agreement page...")
        
        try:
            page_content = page.inner_text('body').lower()
            
            # Strong consent indicators
            strong_consent_indicators = [
                'before starting this survey', 
                'please read the following statements',
                'indicate your agreement',
                'i understand that any data'
            ]
            
            # Check for strong indicators
            has_strong_indicator = any(indicator in page_content for indicator in strong_consent_indicators)
            
            # Survey question exclusions
            survey_question_indicators = [
                'what year were you born', 'what is your gender',
                'select your', 'rate your', 'how likely'
            ]
            
            is_survey_question = any(indicator in page_content for indicator in survey_question_indicators)
            
            # Only treat as consent page if we have strong indicators and it's not a survey question
            if has_strong_indicator and not is_survey_question:
                print("📋 Detected consent/agreement page")
                
                # Look for agreement options
                agreement_selectors = [
                    'input[type="radio"][value*="agree"]',
                    'label:has-text("I agree")',
                    'button:has-text("I agree")',
                    'button:has-text("Agree")'
                ]
                
                for selector in agreement_selectors:
                    try:
                        element = page.query_selector(selector)
                        if element and element.is_visible():
                            print(f"✅ Clicking agreement: {selector}")
                            element.click()
                            self._human_like_delay(1000, 2000)
                            print("✅ Agreement/consent handled")
                            self.navigation_stats["consent_pages_handled"] += 1
                            return True
                    except:
                        continue
        
        except Exception as e:
            print(f"Error checking consent page: {e}")
        
        print("ℹ️  No consent page detected - proceeding to question processing")
        return False

    def wait_for_page_load(self, page, timeout=10000):
        """
        Wait for page to load with timeout.
        """
        try:
            page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except Exception as e:
            print(f"⚠️ Page load timeout: {e}")
            return False

    def scroll_page(self, page, direction="down", amount=500):
        """
        Scroll the page to reveal more content.
        """
        try:
            if direction == "down":
                page.evaluate(f"window.scrollBy(0, {amount})")
            elif direction == "up":
                page.evaluate(f"window.scrollBy(0, -{amount})")
            elif direction == "top":
                page.evaluate("window.scrollTo(0, 0)")
            elif direction == "bottom":
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            
            self._human_like_delay(500, 1000)
            return True
        except Exception as e:
            print(f"Error scrolling page: {e}")
            return False

    def check_for_errors(self, page):
        """
        Check for validation errors on the page.
        """
        try:
            # Common error indicators
            error_indicators = [
                '.error', '.alert', '.warning', '.required',
                '[class*="error"]', '[class*="alert"]', '[class*="warning"]',
                '*:has-text("Please answer")', '*:has-text("Required")',
                '*:has-text("This question requires")', '*:has-text("You must")'
            ]
            
            for selector in error_indicators:
                try:
                    error_elements = page.query_selector_all(selector)
                    for element in error_elements:
                        if element.is_visible():
                            error_text = element.inner_text().lower()
                            if any(phrase in error_text for phrase in ['please answer', 'required', 'must answer', 'select']):
                                print(f"❌ Validation error detected: {error_text[:50]}...")
                                return True
                except:
                    continue
            
            # Check for specific validation messages in page content
            page_content = page.inner_text('body').lower()
            validation_failures = [
                'please answer this question',
                'this question requires an answer',
                'you must select',
                'please select',
                'answer is required',
                'required field'
            ]
            
            for failure_phrase in validation_failures:
                if failure_phrase in page_content:
                    print(f"❌ Validation failure detected: {failure_phrase}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking for validation errors: {e}")
            return False

    def get_navigation_stats(self):
        """
        Get navigation statistics.
        """
        return self.navigation_stats.copy()

    def _request_navigation_assistance(self, page, intervention_manager):
        """
        Request manual intervention for navigation.
        """
        if intervention_manager:
            # Show current page elements for debugging
            try:
                page_content = page.inner_text('body')
                print("\n📄 Current page content sample:")
                print("-" * 40)
                print(page_content[:300] + "..." if len(page_content) > 300 else page_content)
                print("-" * 40)
            except:
                print("Could not retrieve page content for debugging")
            
            # Request manual intervention for navigation
            print("\n" + "="*80)
            print("🚫 NAVIGATION ASSISTANCE REQUIRED")
            print("="*80)
            print("❌ Could not automatically find the next/continue button")
            print()
            print("🔧 MANUAL NAVIGATION INSTRUCTIONS:")
            print("1. 👀 Look for the Next/Continue/Submit button on the page")
            print("2. 🖱️  Click the button to move to the next question")
            print("3. ⏳ Wait for the next page to load completely")
            print("4. ✅ Press Enter here to resume automation")
            print()
            print("💡 This helps us learn about new button formats!")
            print("="*80)
            
            # Log this as a navigation intervention
            self.navigation_stats["manual_navigation_required"] += 1
            self.navigation_stats["navigation_failures"].append({
                "url": page.url,
                "timestamp": time.time(),
                "reason": "Could not automatically detect next/continue button"
            })
            
            # Wait for user to click next button manually
            input("✋ Press Enter AFTER you've clicked the next button and the next page has loaded...")
            
            print("🚀 Resuming automation...")
            print("="*80 + "\n")
            
            return True
        else:
            # Fallback without intervention manager
            print("❌ Navigation failed and no intervention manager available")
            return False

    def _human_like_delay(self, min_ms=1500, max_ms=4000):
        """
        Generate human-like delays with variation.
        """
        delay = random.randint(min_ms, max_ms) / 1000
        time.sleep(delay)

    def click_element_safely(self, page, element, description="element"):
        """
        Safely click an element with error handling.
        """
        try:
            if element and element.is_visible() and not element.is_disabled():
                element.click()
                self._human_like_delay(500, 1000)
                print(f"✅ Clicked {description}")
                return True
            else:
                print(f"❌ Cannot click {description} - not visible or disabled")
                return False
        except Exception as e:
            print(f"❌ Error clicking {description}: {e}")
            return False

    def fill_text_input_safely(self, page, input_element, text, description="input"):
        """
        Safely fill a text input with error handling.
        """
        try:
            if input_element and input_element.is_visible() and not input_element.is_disabled():
                input_element.fill(text)
                self._human_like_delay(300, 700)
                print(f"✅ Filled {description} with: {text}")
                return True
            else:
                print(f"❌ Cannot fill {description} - not visible or disabled")
                return False
        except Exception as e:
            print(f"❌ Error filling {description}: {e}")
            return False

    def select_dropdown_option_safely(self, page, select_element, option_value, description="dropdown"):
        """
        Safely select a dropdown option with error handling.
        """
        try:
            if select_element and select_element.is_visible() and not select_element.is_disabled():
                # Try by value first
                try:
                    select_element.select_option(value=option_value)
                    self._human_like_delay(300, 700)
                    print(f"✅ Selected {description} option by value: {option_value}")
                    return True
                except:
                    # Try by label
                    try:
                        select_element.select_option(label=option_value)
                        self._human_like_delay(300, 700)
                        print(f"✅ Selected {description} option by label: {option_value}")
                        return True
                    except:
                        print(f"❌ Could not select option {option_value} in {description}")
                        return False
            else:
                print(f"❌ Cannot select {description} - not visible or disabled")
                return False
        except Exception as e:
            print(f"❌ Error selecting {description}: {e}")
            return False
        
    def debug_done_button(self, page):
        """
        Debug method to understand why Done button isn't being found.
        Add this temporarily to navigation_controller.py
        """
        print("🔍 DONE BUTTON DEBUG - Starting comprehensive search...")
        
        # Method 1: Look for all buttons
        try:
            all_buttons = page.query_selector_all('button')
            print(f"📊 Found {len(all_buttons)} total buttons")
            
            for i, button in enumerate(all_buttons):
                if button.is_visible():
                    button_text = button.inner_text() or ""
                    button_value = button.get_attribute('value') or ""
                    button_id = button.get_attribute('id') or ""
                    button_class = button.get_attribute('class') or ""
                    
                    print(f"   Button {i+1}: text='{button_text}', value='{button_value}', id='{button_id}', class='{button_class}'")
                    
                    # Check if this looks like our Done button
                    if 'done' in button_text.lower() or 'done' in button_value.lower():
                        print(f"   🎯 FOUND POTENTIAL DONE BUTTON: {i+1}")
        except Exception as e:
            print(f"❌ Error checking buttons: {e}")
        
        # Method 2: Look for all inputs
        try:
            all_inputs = page.query_selector_all('input')
            print(f"📊 Found {len(all_inputs)} total inputs")
            
            for i, input_elem in enumerate(all_inputs):
                if input_elem.is_visible():
                    input_type = input_elem.get_attribute('type') or ""
                    input_value = input_elem.get_attribute('value') or ""
                    input_id = input_elem.get_attribute('id') or ""
                    
                    if input_type in ['submit', 'button']:
                        print(f"   Input {i+1}: type='{input_type}', value='{input_value}', id='{input_id}'")
                        
                        # Check if this looks like our Done button  
                        if 'done' in input_value.lower():
                            print(f"   🎯 FOUND POTENTIAL DONE INPUT: {i+1}")
        except Exception as e:
            print(f"❌ Error checking inputs: {e}")
        
        # Method 3: Look for elements with "Done" text
        try:
            done_elements = page.query_selector_all('*:has-text("Done")')
            print(f"📊 Found {len(done_elements)} elements containing 'Done'")
            
            for i, element in enumerate(done_elements):
                if element.is_visible():
                    tag_name = element.tag_name
                    element_text = element.inner_text() or ""
                    element_id = element.get_attribute('id') or ""
                    element_class = element.get_attribute('class') or ""
                    
                    print(f"   Element {i+1}: tag='{tag_name}', text='{element_text}', id='{element_id}', class='{element_class}'")
        except Exception as e:
            print(f"❌ Error checking Done elements: {e}")
        
        print("🔍 DONE BUTTON DEBUG - Complete!")
        
        # Ask user to manually identify the button
        print("\n" + "="*60)
        print("🔧 MANUAL IDENTIFICATION NEEDED")
        print("="*60)
        print("Looking at the page, can you see the 'Done' button?")
        print("If yes, please manually click it and press Enter to continue.")
        print("This will help us understand the exact element structure.")
        print("="*60)
        
        input("Press Enter AFTER clicking Done manually...")
        return True