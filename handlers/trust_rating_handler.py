"""
Trust Rating Handler Module
Handles trust and rating scale questions.
"""

from .base_handler import BaseQuestionHandler
import random

class TrustRatingHandler(BaseQuestionHandler):
    """Handler for trust rating questions"""
    
    def can_handle(self, page_content: str) -> bool:
        """Check if this is a trust rating question"""
        content_lower = page_content.lower()
        trust_indicators = [
            "trustworthy", "trust", "rate", "how much do you trust",
            "trust level", "reliability", "credible", "how trustworthy",
            "rate the trustworthiness", "how reliable"
        ]
        
        # Must have trust keywords AND rating elements
        has_trust_keywords = any(indicator in content_lower for indicator in trust_indicators)
        has_rating_elements = self.has_rating_elements()
        
        return has_trust_keywords and has_rating_elements
    
    def has_rating_elements(self):
        """Check if page has rating scale elements"""
        try:
            # Look for common rating patterns
            rating_selectors = [
                'input[type="radio"]',
                '*:has-text("1")', '*:has-text("2")', '*:has-text("3")',
                '*:has-text("very trustworthy")', '*:has-text("not trustworthy")',
                'select', 'option'
            ]
            
            for selector in rating_selectors:
                elements = self.page.query_selector_all(selector)
                if len(elements) > 1:  # Multiple rating options suggest a scale
                    return True
            
            return False
        except Exception:
            return False
    
    def handle(self) -> bool:
        """Handle trust rating questions"""
        print("⭐ Handling trust rating question")
        
        page_content = self.page.inner_text('body')
        content_lower = page_content.lower()
        
        try:
            # Strategy 1: Look for specific trust rating text options
            if self.try_text_based_trust_rating(content_lower):
                return True
            
            # Strategy 2: Look for numeric ratings (typically 1-7 or 1-10 scale)
            if self.try_numeric_trust_rating(content_lower):
                return True
            
            # Strategy 3: Look for Likert scale options
            if self.try_likert_scale_rating(content_lower):
                return True
            
            # If no strategy worked, return False for manual intervention
            print("🔄 No trust rating pattern matched - requesting manual intervention")
            return False
            
        except Exception as e:
            print(f"❌ Error in trust rating handler: {e}")
            return False
    
    def try_text_based_trust_rating(self, content_lower):
        """Try to find and select text-based trust ratings"""
        
        # Ordered from most positive to neutral (we'll pick moderate-positive)
        trust_rating_patterns = [
            {"text": "very trustworthy", "priority": 2},
            {"text": "trustworthy", "priority": 1},  # Preferred choice
            {"text": "somewhat trustworthy", "priority": 1},  # Preferred choice
            {"text": "moderately trustworthy", "priority": 1},  # Preferred choice
            {"text": "fairly trustworthy", "priority": 3},
            {"text": "neutral", "priority": 4},
            {"text": "neither trustworthy nor untrustworthy", "priority": 4}
        ]
        
        # Sort by priority (1 = highest priority)
        trust_rating_patterns.sort(key=lambda x: x["priority"])
        
        for pattern in trust_rating_patterns:
            if pattern["text"] in content_lower:
                selectors = [
                    f'*:has-text("{pattern["text"]}")',
                    f'label:has-text("{pattern["text"]}")',
                    f'input[value="{pattern["text"]}"]',
                    f'option:has-text("{pattern["text"]}")'
                ]
                
                for selector in selectors:
                    try:
                        element = self.page.query_selector(selector)
                        if element and element.is_visible() and not element.is_disabled():
                            element.click()
                            self.human_like_delay(500, 1000)
                            print(f"✅ Selected trust rating: {pattern['text']}")
                            return True
                    except Exception:
                        continue
        
        return False
    
    def try_numeric_trust_rating(self, content_lower):
        """Try to select appropriate numeric trust rating"""
        
        # Detect scale type by looking for scale indicators
        scale_type = self.detect_rating_scale(content_lower)
        
        if scale_type == "1-7":
            # For 1-7 scale, choose 5 or 6 (moderate to good trust)
            preferred_ratings = ["5", "6", "4"]
        elif scale_type == "1-10":
            # For 1-10 scale, choose 6, 7, or 8 (moderate to good trust)
            preferred_ratings = ["7", "6", "8"]
        elif scale_type == "1-5":
            # For 1-5 scale, choose 4 or 3 (moderate trust)
            preferred_ratings = ["4", "3"]
        else:
            # Generic moderate ratings
            preferred_ratings = ["5", "4", "6", "3", "7"]
        
        for rating in preferred_ratings:
            selectors = [
                f'input[value="{rating}"]',
                f'*:has-text("{rating}")',
                f'label:has-text("{rating}")',
                f'option[value="{rating}"]'
            ]
            
            for selector in selectors:
                try:
                    element = self.page.query_selector(selector)
                    if element and element.is_visible() and not element.is_disabled():
                        # Additional check: make sure this is actually a rating element
                        if self.is_rating_element(element, rating):
                            element.click()
                            self.human_like_delay(500, 1000)
                            print(f"✅ Selected trust rating: {rating} ({scale_type} scale)")
                            return True
                except Exception:
                    continue
        
        return False
    
    def detect_rating_scale(self, content_lower):
        """Detect the type of rating scale being used"""
        
        # Look for scale indicators in content
        if any(indicator in content_lower for indicator in ["1 to 7", "1-7", "scale of 1 to 7"]):
            return "1-7"
        elif any(indicator in content_lower for indicator in ["1 to 10", "1-10", "scale of 1 to 10"]):
            return "1-10"
        elif any(indicator in content_lower for indicator in ["1 to 5", "1-5", "scale of 1 to 5"]):
            return "1-5"
        
        # Try to detect scale by counting numeric options
        try:
            numeric_elements = []
            for i in range(1, 11):  # Check numbers 1-10
                elements = self.page.query_selector_all(f'*:has-text("{i}")')
                if elements:
                    numeric_elements.append(i)
            
            if len(numeric_elements) >= 7 and 7 in numeric_elements:
                return "1-7"
            elif len(numeric_elements) >= 10 and 10 in numeric_elements:
                return "1-10"
            elif len(numeric_elements) >= 5 and 5 in numeric_elements and 6 not in numeric_elements:
                return "1-5"
        except Exception:
            pass
        
        return "unknown"
    
    def is_rating_element(self, element, rating_value):
        """Check if element is actually a rating scale element (not just text containing the number)"""
        try:
            # Check if it's an input element
            if element.tag_name.lower() == 'input':
                return True
            
            # Check if it's an option element
            if element.tag_name.lower() == 'option':
                return True
            
            # Check if it's associated with a radio button
            element_text = element.inner_text().strip()
            if element_text == rating_value:
                # Look for nearby radio buttons
                parent = element.locator('xpath=parent::*').first
                radio_inputs = parent.query_selector_all('input[type="radio"]')
                if radio_inputs:
                    return True
            
            return False
        except Exception:
            return False
    
    def try_likert_scale_rating(self, content_lower):
        """Try to select Likert scale options (Agree/Disagree style)"""
        
        # Look for Likert scale patterns
        likert_patterns = [
            {"text": "somewhat agree", "priority": 1},
            {"text": "agree", "priority": 2},
            {"text": "neither agree nor disagree", "priority": 3},
            {"text": "neutral", "priority": 3},
            {"text": "slightly agree", "priority": 1}
        ]
        
        # Check if this looks like a Likert scale
        has_likert = any(pattern in content_lower for pattern in ["agree", "disagree", "strongly"])
        
        if has_likert:
            # Sort by priority
            likert_patterns.sort(key=lambda x: x["priority"])
            
            for pattern in likert_patterns:
                if pattern["text"] in content_lower:
                    selectors = [
                        f'*:has-text("{pattern["text"]}")',
                        f'label:has-text("{pattern["text"]}")',
                        f'input[value="{pattern["text"]}"]',
                        f'option:has-text("{pattern["text"]}")'
                    ]
                    
                    for selector in selectors:
                        try:
                            element = self.page.query_selector(selector)
                            if element and element.is_visible() and not element.is_disabled():
                                element.click()
                                self.human_like_delay(500, 1000)
                                print(f"✅ Selected Likert rating: {pattern['text']}")
                                return True
                        except Exception:
                            continue
        
        return False