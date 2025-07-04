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
        Enhanced next button detection with manual intervention fallback.
        """
        print("🔍 Moving to next question...")
        
        # PRIORITY 1: CMIX-specific selectors (based on testing)
        cmix_selectors = [
            'input[type="submit"][value="NEXT"]',
            'button:has-text("NEXT")',
            'input[value="NEXT"]',
            '[onclick*="next"]',
            '[onclick*="Next"]'
        ]
        
        # PRIORITY 2: Standard navigation selectors
        standard_navigation_selectors = [
            'button:has-text("Next")',
            'button:has-text("Continue")', 
            'button:has-text("OK")',
            'input[type="submit"][value*="Next"]',
            'input[type="submit"][value*="Continue"]'
        ]
        
        # PRIORITY 3: Generic submit selectors
        generic_submit_selectors = [
            'button:has-text("Submit")',
            'input[type="submit"]',
            'button[type="submit"]'
        ]
        
        # Try CMIX selectors first
        for selector in cmix_selectors:
            try:
                buttons = page.query_selector_all(selector)
                for button in buttons:
                    if button.is_visible():
                        button_text = button.get_attribute('value') or button.inner_text() or 'NEXT'
                        print(f"✅ Clicking CMIX button: '{button_text.strip()}'")
                        button.click()
                        self._human_like_delay(2000, 3000)
                        self.navigation_stats["buttons_found_automatically"] += 1
                        return True
            except Exception as e:
                print(f"Error with CMIX selector {selector}: {e}")
                continue
        
        # Try standard navigation buttons
        for selector in standard_navigation_selectors:
            try:
                buttons = page.query_selector_all(selector)
                for button in buttons:
                    if button.is_visible():
                        button_text = button.inner_text().strip()
                        print(f"✅ Clicking navigation button: '{button_text}'")
                        button.click()
                        self._human_like_delay(2000, 3000)
                        self.navigation_stats["buttons_found_automatically"] += 1
                        return True
            except Exception as e:
                print(f"Error with navigation selector {selector}: {e}")
                continue
        
        # Try generic submit buttons
        for selector in generic_submit_selectors:
            try:
                buttons = page.query_selector_all(selector)
                for button in buttons:
                    if button.is_visible():
                        button_text = button.inner_text().strip()
                        print(f"✅ Clicking submit button: '{button_text}'")
                        button.click()
                        self._human_like_delay(2000, 3000)
                        self.navigation_stats["buttons_found_automatically"] += 1
                        return True
            except Exception as e:
                print(f"Error with submit selector {selector}: {e}")
                continue
        
        # Enhanced fallback: Look for any clickable element with next-like text
        fallback_selectors = [
            '*:has-text("NEXT")',
            '*:has-text("Next")', 
            '*:has-text("Continue")',
            '*:has-text("Submit")',
            '[class*="next"]',
            '[class*="continue"]',
            '[id*="next"]',
            '[id*="continue"]'
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