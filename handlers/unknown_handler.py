"""
Unknown Handler Module
Fallback handler for unrecognized question types with smart intervention.
"""

from .base_handler import BaseQuestionHandler

class UnknownHandler(BaseQuestionHandler):
    """Enhanced unknown question handler with conservative automation"""
    
    def can_handle(self, page_content: str) -> bool:
        """Unknown handler can theoretically handle anything, but with very low confidence"""
        return True  # Always can handle, but should be last resort
    
    def handle(self) -> bool:
        """Enhanced unknown question handling - prioritize manual intervention"""
        print("❓ Handling unknown question type")
        
        page_content = self.page.inner_text('body')
        content_lower = page_content.lower()
        
        # Only try automated approaches for very simple, safe cases
        # This conservative approach prevents errors and provides learning data
        
        try:
            # Strategy 1: Try very safe default options
            if self.try_safe_default_options(content_lower):
                return True
            
            # Strategy 2: Try neutral/middle options for scales
            if self.try_neutral_scale_options(content_lower):
                return True
            
            # Strategy 3: Try common "don't know" options
            if self.try_dont_know_options(content_lower):
                return True
            
            # If no safe automation worked, request manual intervention
            print("🔄 No safe automation pattern found - requesting manual intervention")
            print("💡 This ensures data quality and provides learning opportunities")
            return False
            
        except Exception as e:
            print(f"❌ Error in unknown handler: {e}")
            return False
    
    def try_safe_default_options(self, content_lower):
        """Try very safe default options that are unlikely to cause errors"""
        
        safe_options = [
            {"keywords": ["don't know", "not sure"], 
             "selectors": ['*:has-text("Don\'t know")', '*:has-text("Not sure")', '*:has-text("Unsure")'],
             "description": "don't know option"},
            
            {"keywords": ["neutral", "neither"], 
             "selectors": ['*:has-text("Neutral")', '*:has-text("Neither")', '*:has-text("No preference")'],
             "description": "neutral option"},
            
            {"keywords": ["sometimes", "occasionally"], 
             "selectors": ['*:has-text("Sometimes")', '*:has-text("Occasionally")', '*:has-text("Rarely")'],
             "description": "frequency option"}
        ]
        
        for option_group in safe_options:
            # Check if keywords match
            if any(keyword in content_lower for keyword in option_group["keywords"]):
                
                # Try to select the option
                for selector in option_group["selectors"]:
                    try:
                        element = self.page.query_selector(selector)
                        if element and element.is_visible() and not element.is_disabled():
                            element.click()
                            self.human_like_delay(500, 1000)
                            print(f"✅ Selected safe option: {option_group['description']}")
                            return True
                    except Exception:
                        continue
        
        return False
    
    def try_neutral_scale_options(self, content_lower):
        """Try to find and select neutral/middle options on rating scales"""
        
        # Only attempt if this looks like a rating scale
        scale_indicators = ["scale", "rate", "rating", "1", "2", "3", "4", "5"]
        if not any(indicator in content_lower for indicator in scale_indicators):
            return False
        
        # Look for middle/neutral options on common scales
        neutral_scale_options = [
            # For 1-5 scales
            {"selectors": ['*:has-text("3")', 'input[value="3"]'], "scale": "1-5 scale", "value": "3"},
            
            # For 1-7 scales  
            {"selectors": ['*:has-text("4")', 'input[value="4"]'], "scale": "1-7 scale", "value": "4"},
            
            # For agree/disagree scales
            {"selectors": ['*:has-text("Neither agree nor disagree")', '*:has-text("Neutral")'], 
             "scale": "agreement scale", "value": "neutral"},
            
            # For frequency scales
            {"selectors": ['*:has-text("Sometimes")', '*:has-text("Occasionally")'], 
             "scale": "frequency scale", "value": "sometimes"}
        ]
        
        for option in neutral_scale_options:
            for selector in option["selectors"]:
                try:
                    elements = self.page.query_selector_all(selector)
                    
                    # Additional safety: make sure we're selecting from a group of options
                    if len(elements) >= 1:
                        element = elements[0]
                        if element and element.is_visible() and not element.is_disabled():
                            
                            # Extra safety check: ensure this is part of a form element group
                            if self.is_part_of_option_group(element):
                                element.click()
                                self.human_like_delay(500, 1000)
                                print(f"✅ Selected neutral scale option: {option['value']} ({option['scale']})")
                                return True
                except Exception:
                    continue
        
        return False
    
    def try_dont_know_options(self, content_lower):
        """Try to find and select 'don't know' or similar uncertainty options"""
        
        uncertainty_options = [
            {'text': "Don't know", 'variations': ["Don't know", "Do not know", "Don't Know"]},
            {'text': "Not sure", 'variations': ["Not sure", "Unsure", "Not Sure"]},
            {'text': "No opinion", 'variations': ["No opinion", "No Opinion"]},
            {'text': "Prefer not to say", 'variations': ["Prefer not to say", "Prefer not to answer"]},
            {'text': "None of the above", 'variations': ["None of the above", "None of these"]}
        ]
        
        for option_group in uncertainty_options:
            for variation in option_group['variations']:
                selectors = [
                    f'*:has-text("{variation}")',
                    f'label:has-text("{variation}")',
                    f'input[value="{variation}"]',
                    f'option:has-text("{variation}")'
                ]
                
                for selector in selectors:
                    try:
                        element = self.page.query_selector(selector)
                        if element and element.is_visible() and not element.is_disabled():
                            element.click()
                            self.human_like_delay(500, 1000)
                            print(f"✅ Selected uncertainty option: {variation}")
                            return True
                    except Exception:
                        continue
        
        return False
    
    def is_part_of_option_group(self, element):
        """Check if element is part of a legitimate option group (safety check)"""
        try:
            # Check if there are other similar elements nearby (indicating a group)
            if element.tag_name.lower() == 'input':
                input_type = element.get_attribute('type')
                if input_type in ['radio', 'checkbox']:
                    # Count similar inputs with same name
                    name = element.get_attribute('name')
                    if name:
                        similar_elements = self.page.query_selector_all(f'input[name="{name}"]')
                        return len(similar_elements) > 1  # Should be part of a group
            
            elif element.tag_name.lower() == 'option':
                # Options should be part of a select element
                return True
            
            # For other elements, check if there are similar clickable elements nearby
            parent = element.locator('xpath=parent::*').first
            clickable_siblings = parent.query_selector_all('*[role="button"], button, input, *:has-text("1"), *:has-text("2")')
            return len(clickable_siblings) > 1
            
        except Exception:
            return False
    
    def analyze_unknown_question(self, page_content):
        """Analyze unknown question to provide insights for future handler development"""
        
        content_lower = page_content.lower()
        analysis = {
            "potential_question_type": "unknown",
            "detected_elements": [],
            "suggested_handler": None,
            "confidence_level": "low"
        }
        
        try:
            # Analyze form elements
            radio_count = len(self.page.query_selector_all('input[type="radio"]'))
            checkbox_count = len(self.page.query_selector_all('input[type="checkbox"]'))
            select_count = len(self.page.query_selector_all('select'))
            text_input_count = len(self.page.query_selector_all('input[type="text"], input[type="number"]'))
            
            analysis["detected_elements"] = {
                "radio_buttons": radio_count,
                "checkboxes": checkbox_count,
                "select_dropdowns": select_count,
                "text_inputs": text_input_count
            }
            
            # Suggest potential question type based on content
            if any(word in content_lower for word in ["age", "gender", "income", "employment"]):
                analysis["potential_question_type"] = "demographics"
                analysis["suggested_handler"] = "demographics_handler"
            elif any(word in content_lower for word in ["familiar", "brand", "heard"]):
                analysis["potential_question_type"] = "brand_familiarity"
                analysis["suggested_handler"] = "brand_familiarity_handler"
            elif any(word in content_lower for word in ["trustworthy", "trust", "reliable"]):
                analysis["potential_question_type"] = "trust_rating"
                analysis["suggested_handler"] = "trust_rating_handler"
            elif any(word in content_lower for word in ["sponsor", "venue", "stadium"]):
                analysis["potential_question_type"] = "research_required"
                analysis["suggested_handler"] = "research_handler"
            elif checkbox_count > 3:
                analysis["potential_question_type"] = "multi_select"
                analysis["suggested_handler"] = "multi_select_handler"
            elif radio_count > 3:
                analysis["potential_question_type"] = "rating_matrix"
                analysis["suggested_handler"] = "rating_matrix_handler"
            
            # Log analysis for improvement
            print(f"📊 Unknown question analysis: {analysis['potential_question_type']}")
            if analysis["suggested_handler"]:
                print(f"💡 Suggested handler for future: {analysis['suggested_handler']}")
            
        except Exception as e:
            print(f"Warning: Could not analyze unknown question: {e}")
        
        return analysis