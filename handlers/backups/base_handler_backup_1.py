"""
Base Handler Module
Abstract base class for all question handlers with common functionality.
"""

from abc import ABC, abstractmethod
import random
import time


class BaseQuestionHandler(ABC):
    """
    Abstract base class for all question handlers.
    Provides common functionality and enforces handler interface.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        self.page = page
        self.knowledge_base = knowledge_base
        self.intervention_manager = intervention_manager
    
    @abstractmethod
    def can_handle(self, page_content: str) -> float:
        """
        Determine if this handler can process the current question.
        
        Args:
            page_content: The text content of the current page
            
        Returns:
            float: Confidence score between 0.0 and 1.0
                  0.0 = Cannot handle at all
                  1.0 = Perfect match, definitely can handle
        """
        pass
    
    @abstractmethod
    def handle(self) -> bool:
        """
        Process the current question.
        
        Returns:
            bool: True if successfully handled, False if manual intervention needed
        """
        pass
    
    # Common utility methods available to all handlers
    
    def human_like_delay(self, min_ms=1500, max_ms=4000):
        """Generate human-like delays with variation."""
        delay = random.randint(min_ms, max_ms) / 1000
        time.sleep(delay)
    
    def get_user_profile(self):
        """Get user profile from knowledge base."""
        return self.knowledge_base.get("user_profile", {})
    
    def get_demographics(self):
        """Get user demographics from knowledge base."""
        return self.get_user_profile().get("demographics", {})
    
    def get_brand_preferences(self):
        """Get user brand preferences from knowledge base."""
        return self.get_user_profile().get("existing_brands", {})
    
    def get_interests(self):
        """Get user interests from knowledge base."""
        return self.get_user_profile().get("interests_and_preferences", {})
    
    def get_question_patterns(self):
        """Get question patterns from knowledge base."""
        return self.knowledge_base.get("question_patterns", {})
    
    def log_success(self, action_description: str):
        """Log successful action with consistent formatting."""
        print(f"✅ {action_description}")
    
    def log_attempt(self, action_description: str):
        """Log attempt with consistent formatting."""
        print(f"🔍 {action_description}")
    
    def log_failure(self, reason: str):
        """Log failure with consistent formatting."""
        print(f"❌ {reason}")
    
    def request_intervention(self, reason: str):
        """Request manual intervention through the intervention manager."""
        if self.intervention_manager:
            question_type = self.__class__.__name__.replace('Handler', '').lower()
            page_content = self.get_page_content()
            return self.intervention_manager.request_manual_intervention(
                question_type, 
                reason, 
                page_content
            )
        else:
            print(f"⚠️ Manual intervention needed: {reason}")
            return False
    
    def get_page_content(self):
        """Safely get page content."""
        try:
            if self.page:
                return self.page.inner_text('body')
        except Exception as e:
            print(f"Error getting page content: {e}")
        return ""
    
    def get_page_content_lower(self):
        """Get page content in lowercase for pattern matching."""
        return self.get_page_content().lower()
    
    def find_elements_safely(self, selector: str):
        """Safely find elements with error handling."""
        try:
            if self.page:
                return self.page.query_selector_all(selector)
        except Exception as e:
            print(f"Error finding elements with selector '{selector}': {e}")
        return []
    
    def find_element_safely(self, selector: str):
        """Safely find single element with error handling."""
        try:
            if self.page:
                return self.page.query_selector(selector)
        except Exception as e:
            print(f"Error finding element with selector '{selector}': {e}")
        return None
    
    def click_element_safely(self, element, description="element"):
        """Safely click an element with error handling."""
        try:
            if element and element.is_visible() and not element.is_disabled():
                element.click()
                self.human_like_delay(300, 800)
                self.log_success(f"Clicked {description}")
                return True
            else:
                self.log_failure(f"Cannot click {description} - not visible or disabled")
                return False
        except Exception as e:
            self.log_failure(f"Error clicking {description}: {e}")
            return False
    
    # FIX 3: Enhanced Radio Button Clicking Method
    def click_radio_button_safely(self, radio_element, description="radio button"):
            """
            Safely click radio buttons with label interference handling and TIMEOUT FIX.
            """
            try:
                if not radio_element:
                    self.log_failure(f"Radio element not found for {description}")
                    return False
                
                # Method 1: Try direct click with timeout
                try:
                    if radio_element.is_visible() and not radio_element.is_disabled():
                        # TIMEOUT FIX: Use shorter timeout
                        radio_element.click(timeout=3000)  # 3 seconds instead of 30
                        self.human_like_delay(300, 800)
                        self.log_success(f"Clicked {description} (direct)")
                        return True
                except Exception as e:
                    self.log_attempt(f"Direct click failed for {description}: {e}")
                
                # Method 2: Try clicking associated label with timeout
                try:
                    radio_id = radio_element.get_attribute('id')
                    if radio_id:
                        label = self.find_element_safely(f"label[for='{radio_id}']")
                        if label and label.is_visible():
                            label.click(timeout=3000)  # TIMEOUT FIX
                            self.human_like_delay(300, 800)
                            self.log_success(f"Clicked {description} (via label)")
                            return True
                except Exception as e:
                    self.log_attempt(f"Label click failed for {description}: {e}")
                
                # Method 3: Force click using JavaScript (no timeout issues)
                try:
                    self.page.evaluate("(element) => element.click()", radio_element)
                    self.human_like_delay(300, 800)
                    self.log_success(f"Clicked {description} (JavaScript)")
                    return True
                except Exception as e:
                    self.log_attempt(f"JavaScript click failed for {description}: {e}")
                
                # Method 4: Try checking the radio button programmatically
                try:
                    self.page.evaluate("(element) => element.checked = true", radio_element)
                    # Trigger change event
                    self.page.evaluate("(element) => element.dispatchEvent(new Event('change', { bubbles: true }))", radio_element)
                    self.human_like_delay(300, 800)
                    self.log_success(f"Checked {description} (programmatic)")
                    return True
                except Exception as e:
                    self.log_failure(f"All click methods failed for {description}: {e}")
                
                return False
                
            except Exception as e:
                self.log_failure(f"Error clicking radio button {description}: {e}")
                return False
    
    def fill_input_safely(self, element, text, description="input"):
        """Safely fill a text input with error handling."""
        try:
            if element and element.is_visible() and not element.is_disabled():
                element.fill(text)
                self.human_like_delay(300, 700)
                self.log_success(f"Filled {description} with: {text}")
                return True
            else:
                self.log_failure(f"Cannot fill {description} - not visible or disabled")
                return False
        except Exception as e:
            self.log_failure(f"Error filling {description}: {e}")
            return False
    
    def select_dropdown_safely(self, element, value, description="dropdown"):
        """Safely select dropdown option with multiple fallback methods."""
        try:
            if element and element.is_visible() and not element.is_disabled():
                # Try by value first
                try:
                    element.select_option(value=value)
                    self.human_like_delay(300, 700)
                    self.log_success(f"Selected {description} by value: {value}")
                    return True
                except:
                    # Try by label
                    try:
                        element.select_option(label=value)
                        self.human_like_delay(300, 700)
                        self.log_success(f"Selected {description} by label: {value}")
                        return True
                    except:
                        self.log_failure(f"Could not select '{value}' in {description}")
                        return False
            else:
                self.log_failure(f"Cannot select {description} - not visible or disabled")
                return False
        except Exception as e:
            self.log_failure(f"Error selecting {description}: {e}")
            return False
    
    def check_keywords_in_content(self, keywords, content=None):
        """Check if any keywords are present in content."""
        if content is None:
            content = self.get_page_content_lower()
        
        return any(keyword.lower() in content for keyword in keywords)
    
    def count_keyword_matches(self, keywords, content=None):
        """Count how many keywords match in content."""
        if content is None:
            content = self.get_page_content_lower()
        
        return sum(1 for keyword in keywords if keyword.lower() in content)
    
    def get_handler_name(self):
        """Get the handler name for logging."""
        return self.__class__.__name__.replace('Handler', '')
    
    def log_handler_start(self):
        """Log when handler starts processing."""
        print(f"🔧 {self.get_handler_name()} handler processing...")
    
    def calculate_base_confidence(self, required_keywords, page_content=None):
        """
        Calculate base confidence score based on keyword matching.
        
        Args:
            required_keywords: List of keywords that should be present
            page_content: Page content to check (defaults to current page)
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        if page_content is None:
            page_content = self.get_page_content_lower()
        
        if not required_keywords:
            return 0.0
        
        matches = self.count_keyword_matches(required_keywords, page_content)
        return min(matches / len(required_keywords), 1.0)
    
    def validate_required_elements(self, selectors):
        """
        Validate that required form elements are present and usable.
        
        Args:
            selectors: List of CSS selectors to check
            
        Returns:
            bool: True if all required elements are present and usable
        """
        for selector in selectors:
            elements = self.find_elements_safely(selector)
            usable_elements = [el for el in elements if el.is_visible() and not el.is_disabled()]
            
            if not usable_elements:
                self.log_failure(f"Required element not found or not usable: {selector}")
                return False
        
        return True