"""
Base Handler Module
Abstract base class for all question handlers with common functionality.
Enhanced with Human-Like Timing Manager integration for realistic automation behavior.
"""

from abc import ABC, abstractmethod
import random
import time
from utils.human_timing_manager import HumanLikeTimingManager


class BaseQuestionHandler(ABC):
    """
    Abstract base class for all question handlers.
    Provides common functionality and enforces handler interface.
    Enhanced with realistic human timing patterns.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        self.page = page
        self.knowledge_base = knowledge_base
        self.intervention_manager = intervention_manager
        
        # Initialize enhanced timing manager
        try:
            self.timing_manager = HumanLikeTimingManager()
            print(f"⏱️ Handler initialized with enhanced human timing")
        except Exception as e:
            print(f"⚠️ Could not initialize timing manager: {e}")
            self.timing_manager = None
    
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
    
    # Enhanced human-like delay with realistic timing patterns
    
    def human_like_delay(self, min_ms=None, max_ms=None, action_type="general", question_content=""):
        """Enhanced human-like delay with realistic timing patterns."""
        
        if hasattr(self, 'timing_manager') and self.timing_manager:
            # Use enhanced timing with question context
            question_type = getattr(self, 'question_type', self._get_handler_question_type())
            complexity = self._assess_question_complexity(question_content)
            
            return self.timing_manager.apply_human_delay(
                action_type=action_type,
                question_type=question_type,
                complexity=complexity,
                question_content=question_content
            )
        else:
            # Fallback to original method
            delay = random.randint(min_ms or 1500, max_ms or 4000) / 1000
            time.sleep(delay)
            return delay

    def _get_handler_question_type(self):
        """Get question type from handler class name."""
        handler_name = self.__class__.__name__.replace('Handler', '').lower()
        
        # Map handler names to timing categories
        timing_map = {
            'demographics': 'demographics',
            'enhanceddemographics': 'demographics',
            'brandgamiliarity': 'brand_familiarity',
            'ratingmatrix': 'rating_matrix',
            'multiselect': 'multi_select',
            'trustrating': 'trust_rating',
            'research': 'research_required',
            'recencyactivities': 'multi_select',
            'unknown': 'unknown'
        }
        
        return timing_map.get(handler_name, 'unknown')

    def _assess_question_complexity(self, question_content):
        """Assess question complexity for timing calculations."""
        if not question_content:
            # Use page content if no specific question content provided
            question_content = self.get_page_content()
        
        if not question_content:
            return "medium"
        
        content_lower = question_content.lower()
        
        # Simple indicators
        simple_keywords = ['age', 'gender', 'name', 'yes', 'no', 'select one', 'choose one']
        if any(word in content_lower for word in simple_keywords):
            return "simple"
        
        # Complex indicators  
        complex_keywords = ['compare', 'analyze', 'evaluate', 'explain', 'why do you think', 
                          'what factors', 'how likely', 'rate the importance', 'consider all']
        if any(word in content_lower for word in complex_keywords):
            return "complex"
        
        # Medium complexity indicators
        medium_keywords = ['opinion', 'feel', 'think', 'rate', 'scale', 'familiar', 'trust']
        if any(word in content_lower for word in medium_keywords):
            return "medium"
        
        return "medium"
    
    # Enhanced action methods with context-aware timing
    
    def reading_delay(self, content_length=None):
        """Apply realistic reading delay based on content length."""
        if hasattr(self, 'timing_manager') and self.timing_manager:
            if content_length is None:
                content_length = len(self.get_page_content())
            return self.timing_manager.reading_delay(content_length)
        else:
            # Fallback reading delay
            delay = random.uniform(1.0, 3.0)
            time.sleep(delay)
            return delay
    
    def typing_delay(self, text):
        """Apply realistic typing delay for text input."""
        if hasattr(self, 'timing_manager') and self.timing_manager:
            return self.timing_manager.typing_delay_for_text(text)
        else:
            # Fallback typing delay
            delay = len(text) * random.uniform(0.05, 0.15)
            time.sleep(delay)
            return delay
    
    # Common utility methods available to all handlers
    
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
        """Safely click an element with error handling and enhanced timing."""
        try:
            if element and element.is_visible() and not element.is_disabled():
                # Apply human-like delay before clicking
                self.human_like_delay(action_type="clicking", question_content=description)
                
                element.click()
                
                # Apply shorter delay after clicking
                if hasattr(self, 'timing_manager') and self.timing_manager:
                    self.timing_manager.quick_delay(0.3, 0.8)
                else:
                    time.sleep(random.uniform(0.3, 0.8))
                
                self.log_success(f"Clicked {description}")
                return True
            else:
                self.log_failure(f"Cannot click {description} - not visible or disabled")
                return False
        except Exception as e:
            self.log_failure(f"Error clicking {description}: {e}")
            return False
    
    # Enhanced Radio Button Clicking Method with timing integration
    def click_radio_button_safely(self, radio_element, description="radio button"):
        """
        Safely click radio buttons with label interference handling, timeout fix, and enhanced timing.
        """
        try:
            if not radio_element:
                self.log_failure(f"Radio element not found for {description}")
                return False
            
            # Apply thinking delay before radio button interaction
            self.human_like_delay(action_type="thinking", question_content=f"radio button: {description}")
            
            # Method 1: Try direct click with timeout
            try:
                if radio_element.is_visible() and not radio_element.is_disabled():
                    # TIMEOUT FIX: Use shorter timeout
                    radio_element.click(timeout=3000)  # 3 seconds instead of 30
                    
                    # Apply quick delay after successful click
                    if hasattr(self, 'timing_manager') and self.timing_manager:
                        self.timing_manager.quick_delay(0.3, 0.8)
                    else:
                        time.sleep(random.uniform(0.3, 0.8))
                    
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
                        
                        # Apply quick delay after successful click
                        if hasattr(self, 'timing_manager') and self.timing_manager:
                            self.timing_manager.quick_delay(0.3, 0.8)
                        else:
                            time.sleep(random.uniform(0.3, 0.8))
                        
                        self.log_success(f"Clicked {description} (via label)")
                        return True
            except Exception as e:
                self.log_attempt(f"Label click failed for {description}: {e}")
            
            # Method 3: Force click using JavaScript (no timeout issues)
            try:
                self.page.evaluate("(element) => element.click()", radio_element)
                
                # Apply quick delay after successful click
                if hasattr(self, 'timing_manager') and self.timing_manager:
                    self.timing_manager.quick_delay(0.3, 0.8)
                else:
                    time.sleep(random.uniform(0.3, 0.8))
                
                self.log_success(f"Clicked {description} (JavaScript)")
                return True
            except Exception as e:
                self.log_attempt(f"JavaScript click failed for {description}: {e}")
            
            # Method 4: Try checking the radio button programmatically
            try:
                self.page.evaluate("(element) => element.checked = true", radio_element)
                # Trigger change event
                self.page.evaluate("(element) => element.dispatchEvent(new Event('change', { bubbles: true }))", radio_element)
                
                # Apply quick delay after successful operation
                if hasattr(self, 'timing_manager') and self.timing_manager:
                    self.timing_manager.quick_delay(0.3, 0.8)
                else:
                    time.sleep(random.uniform(0.3, 0.8))
                
                self.log_success(f"Checked {description} (programmatic)")
                return True
            except Exception as e:
                self.log_failure(f"All click methods failed for {description}: {e}")
            
            return False
            
        except Exception as e:
            self.log_failure(f"Error clicking radio button {description}: {e}")
            return False
    
    def fill_input_safely(self, element, text, description="input"):
        """Safely fill a text input with error handling and realistic typing timing."""
        try:
            if element and element.is_visible() and not element.is_disabled():
                # Apply thinking delay before typing
                self.human_like_delay(action_type="thinking", question_content=f"filling {description}")
                
                # Apply realistic typing delay
                self.typing_delay(text)
                
                element.fill(text)
                
                # Brief delay after filling
                if hasattr(self, 'timing_manager') and self.timing_manager:
                    self.timing_manager.quick_delay(0.3, 0.7)
                else:
                    time.sleep(random.uniform(0.3, 0.7))
                
                self.log_success(f"Filled {description} with: {text}")
                return True
            else:
                self.log_failure(f"Cannot fill {description} - not visible or disabled")
                return False
        except Exception as e:
            self.log_failure(f"Error filling {description}: {e}")
            return False
    
    def select_dropdown_safely(self, element, value, description="dropdown"):
        """Safely select dropdown option with multiple fallback methods and enhanced timing."""
        try:
            if element and element.is_visible() and not element.is_disabled():
                # Apply thinking delay before dropdown interaction
                self.human_like_delay(action_type="thinking", question_content=f"selecting from {description}")
                
                # Try by value first
                try:
                    element.select_option(value=value)
                    
                    # Apply delay after selection
                    if hasattr(self, 'timing_manager') and self.timing_manager:
                        self.timing_manager.quick_delay(0.3, 0.7)
                    else:
                        time.sleep(random.uniform(0.3, 0.7))
                    
                    self.log_success(f"Selected {description} by value: {value}")
                    return True
                except:
                    # Try by label
                    try:
                        element.select_option(label=value)
                        
                        # Apply delay after selection
                        if hasattr(self, 'timing_manager') and self.timing_manager:
                            self.timing_manager.quick_delay(0.3, 0.7)
                        else:
                            time.sleep(random.uniform(0.3, 0.7))
                        
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
    
    def page_analysis_delay(self):
        """Apply realistic delay for page analysis and reading."""
        page_content = self.get_page_content()
        content_length = len(page_content) if page_content else 500
        
        if hasattr(self, 'timing_manager') and self.timing_manager:
            # Use reading delay for page analysis
            return self.timing_manager.reading_delay(min(content_length, 1000))  # Cap at 1000 chars for analysis
        else:
            # Fallback analysis delay
            delay = random.uniform(1.0, 3.0)
            time.sleep(delay)
            return delay