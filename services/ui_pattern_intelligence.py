#!/usr/bin/env python3
"""
🧠 UI PATTERN INTELLIGENCE SYSTEM
Teaching Quenito to FEEL UI patterns, not memorize them.
This module gives Quenito digital intuition for complex UI interactions.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from playwright.async_api import Page, ElementHandle
import base64

class UIPatternIntelligence:
    """
    Quenito's Digital Intuition for UI Patterns
    Recognizes and interacts with complex UI elements through pattern understanding
    """
    
    def __init__(self, page: Page, vision_service=None, llm_service=None):
        self.page = page
        self.vision = vision_service
        self.llm = llm_service
        
        # Pattern confidence thresholds
        self.confidence_threshold = 0.7
        
        print("🧠 UI Pattern Intelligence initialized - Teaching digital intuition!")
    
    # ==========================================
    # MAIN PATTERN DETECTION & HANDLING
    # ==========================================
    
    async def detect_and_handle_pattern(self, question_text: str, screenshot_base64: str = None) -> Dict:
        """
        Main entry point - Detects UI pattern and handles accordingly
        Returns success status and details
        """
        try:
            # First, try to detect what pattern we're dealing with
            pattern_type = await self._detect_pattern_type(screenshot_base64)
            
            print(f"🎯 Pattern detected: {pattern_type}")
            
            # Route to appropriate handler based on pattern
            handlers = {
                'dropdown': self._handle_dropdown_pattern,
                'slider': self._handle_slider_pattern,
                'carousel': self._handle_carousel_pattern,
                'star_rating': self._handle_star_rating_pattern,
                'brand_grid': self._handle_brand_grid_pattern,
                'radio_matrix': self._handle_radio_matrix_pattern,
                'likert_scale': self._handle_likert_scale_pattern
            }
            
            if pattern_type in handlers:
                result = await handlers[pattern_type](question_text)
                return result
            else:
                return {'success': False, 'reason': 'No pattern detected'}
                
        except Exception as e:
            print(f"❌ Pattern detection error: {e}")
            return {'success': False, 'error': str(e)}
    
    # ==========================================
    # PATTERN DETECTION (Digital Intuition)
    # ==========================================
    
    async def _detect_pattern_type(self, screenshot_base64: str = None) -> str:
        """
        Detects what KIND of UI pattern we're dealing with
        This is where Quenito develops intuition!
        """
        
        # Check for dropdown patterns FIRST (critical!)
        if await self._feels_like_dropdown():
            return 'dropdown'
        
        # Check for slider patterns
        if await self._feels_like_slider():
            return 'slider'
        
        # Check for carousel patterns  
        if await self._feels_like_carousel():
            return 'carousel'
        
        # Check for star ratings
        if await self._feels_like_star_rating():
            return 'star_rating'
        
        # Check for brand grids
        if await self._feels_like_brand_grid():
            return 'brand_grid'
        
        # Check for radio matrix
        if await self._feels_like_radio_matrix():
            return 'radio_matrix'
        
        # Check for Likert scales
        if await self._feels_like_likert_scale():
            return 'likert_scale'
        
        return 'unknown'
    
    # ==========================================
    # CRITICAL: DROPDOWN HANDLING
    # ==========================================
    
    async def _feels_like_dropdown(self) -> bool:
        """Does this FEEL like a dropdown to Quenito?"""
        try:
            # Multiple ways to detect dropdowns
            selectors = [
                'select',  # Standard HTML select
                '[role="combobox"]',  # ARIA combobox
                '[role="listbox"]',  # ARIA listbox
                '.dropdown',  # Class-based
                '.select-wrapper',  # Wrapper classes
                'input[readonly]',  # Read-only inputs that trigger dropdowns
            ]
            
            for selector in selectors:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    print(f"📋 Dropdown intuition triggered by: {selector}")
                    return True
            
            # Also check for dropdown indicators in text
            page_text = await self.page.content()
            dropdown_hints = ['Please select', 'Choose', 'Select your', '-- Select --']
            for hint in dropdown_hints:
                if hint in page_text:
                    print(f"📋 Dropdown intuition triggered by text: {hint}")
                    return True
                    
            return False
        except:
            return False
    
    async def _handle_dropdown_pattern(self, question_text: str) -> Dict:
        """
        Handle dropdown selection with multiple strategies
        This is CRITICAL for automation rate!
        """
        print("🎯 DROPDOWN HANDLER ACTIVATED - Multiple strategies ready!")
        
        try:
            # Find all dropdowns on the page
            dropdowns = await self._find_all_dropdowns()
            
            if not dropdowns:
                print("❌ No dropdowns found")
                return {'success': False, 'reason': 'No dropdowns detected'}
            
            print(f"📋 Found {len(dropdowns)} dropdown(s)")
            
            # Get the answer from LLM for this question
            if self.llm:
                # Get dropdown options first
                dropdown_options = await self._get_dropdown_options(dropdowns[0])
                
                llm_response = await self.llm.get_response(
                    question_text,
                    dropdown_options,
                    'dropdown'
                )
                
                if not llm_response['success']:
                    return {'success': False, 'reason': 'LLM could not determine answer'}
                
                answer_value = llm_response['value']
                print(f"🤖 LLM says to select: {answer_value}")
            else:
                # Fallback - try to determine from context
                answer_value = await self._infer_dropdown_value(question_text)
            
            # Try multiple strategies to select the value
            success = await self._apply_dropdown_selection(dropdowns, answer_value, question_text)
            
            if success:
                print(f"✅ Successfully selected '{answer_value}' in dropdown!")
                return {
                    'success': True,
                    'pattern': 'dropdown',
                    'value': answer_value,
                    'confidence': 0.9
                }
            else:
                print(f"❌ Could not select '{answer_value}' in dropdown")
                return {'success': False, 'reason': 'Dropdown selection failed'}
                
        except Exception as e:
            print(f"❌ Dropdown handling error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _find_all_dropdowns(self) -> List[ElementHandle]:
        """Find all dropdown elements on the page"""
        dropdowns = []
        
        # Strategy 1: Standard HTML select elements
        selects = await self.page.query_selector_all('select')
        dropdowns.extend(selects)
        
        # Strategy 2: Custom dropdowns with specific attributes
        custom_selectors = [
            '[role="combobox"]',
            '[role="listbox"]',
            '.dropdown-toggle',
            'input[data-toggle="dropdown"]'
        ]
        
        for selector in custom_selectors:
            elements = await self.page.query_selector_all(selector)
            dropdowns.extend(elements)
        
        return dropdowns
    
    async def _get_dropdown_options(self, dropdown: ElementHandle) -> List[str]:
        """Extract options from a dropdown element"""
        options = []
        try:
            # For standard select elements
            tag_name = await dropdown.evaluate('el => el.tagName')
            if tag_name == 'SELECT':
                option_elements = await dropdown.query_selector_all('option')
                for option in option_elements:
                    text = await option.inner_text()
                    if text.strip() and text.strip() not in ['', 'Select', 'Please select', '--']:
                        options.append(text.strip())
        except:
            pass
        return options
    
    async def _apply_dropdown_selection(self, dropdowns: List, value: str, context: str = "") -> bool:
        """
        Apply selection to dropdown with multiple strategies
        This is where the magic happens!
        """
        
        for dropdown in dropdowns:
            try:
                # Strategy 1: Direct select for HTML select elements
                tag_name = await dropdown.evaluate('el => el.tagName')
                
                if tag_name == 'SELECT':
                    print(f"📋 Using standard select strategy for: {value}")
                    
                    # Try exact match first
                    try:
                        await dropdown.select_option(value)
                        await asyncio.sleep(0.5)  # Wait for any dynamic updates
                        return True
                    except:
                        pass
                    
                    # Try by label/text
                    try:
                        await dropdown.select_option(label=value)
                        await asyncio.sleep(0.5)
                        return True
                    except:
                        pass
                    
                    # Try partial match
                    options = await dropdown.query_selector_all('option')
                    for option in options:
                        option_text = await option.inner_text()
                        if value.upper() in option_text.upper() or option_text.upper() in value.upper():
                            option_value = await option.get_attribute('value')
                            if option_value:
                                await dropdown.select_option(option_value)
                                await asyncio.sleep(0.5)
                                print(f"✅ Selected by partial match: {option_text}")
                                return True
                
                # Strategy 2: Click to open, then click option
                else:
                    print(f"📋 Using click strategy for custom dropdown")
                    
                    # Click to open dropdown
                    await dropdown.click()
                    await asyncio.sleep(0.5)  # Wait for dropdown to open
                    
                    # Find and click the matching option
                    option_selectors = [
                        f'text="{value}"',
                        f'*:has-text("{value}")',
                        f'[data-value="{value}"]',
                        f'li:has-text("{value}")',
                        f'option:has-text("{value}")'
                    ]
                    
                    for selector in option_selectors:
                        try:
                            option = await self.page.wait_for_selector(selector, timeout=2000)
                            if option:
                                await option.click()
                                await asyncio.sleep(0.5)
                                print(f"✅ Clicked option: {value}")
                                return True
                        except:
                            continue
                            
            except Exception as e:
                print(f"⚠️ Dropdown strategy failed: {e}")
                continue
        
        return False
    
    async def _infer_dropdown_value(self, question_text: str) -> str:
        """Infer dropdown value from question context"""
        # This is a fallback when LLM is not available
        # Uses pattern matching based on question
        
        if 'state' in question_text.lower():
            return 'NSW'
        elif 'city' in question_text.lower():
            return 'KOGARAH'
        elif 'postal' in question_text.lower() or 'postcode' in question_text.lower():
            return '2217'
        
        return ""
    
    # ==========================================
    # SLIDER PATTERN HANDLING
    # ==========================================
    
    async def _feels_like_slider(self) -> bool:
        """Does this FEEL like a slider?"""
        try:
            slider_selectors = [
                'input[type="range"]',
                '[role="slider"]',
                '.slider',
                '.range-slider',
                '.ui-slider'
            ]
            
            for selector in slider_selectors:
                if await self.page.query_selector(selector):
                    return True
            return False
        except:
            return False
    
    async def _handle_slider_pattern(self, question_text: str) -> Dict:
        """Handle slider interactions"""
        print("🎚️ SLIDER HANDLER ACTIVATED")
        
        try:
            # Find the slider element
            slider = await self.page.query_selector('input[type="range"], [role="slider"], .slider')
            
            if not slider:
                return {'success': False, 'reason': 'No slider found'}
            
            # Get LLM's answer (1-5 scale typically)
            if self.llm:
                llm_response = await self.llm.get_response(question_text, None, 'slider')
                target_value = llm_response.get('value', '3')  # Default to middle
            else:
                target_value = '3'  # Default middle position
            
            # Strategy 1: Click at position on the slider track
            bounding_box = await slider.bounding_box()
            if bounding_box:
                # Calculate position based on value (assuming 1-5 scale)
                value_num = int(target_value) if target_value.isdigit() else 3
                position_ratio = (value_num - 1) / 4  # 0 to 1 ratio
                
                click_x = bounding_box['x'] + (bounding_box['width'] * position_ratio)
                click_y = bounding_box['y'] + (bounding_box['height'] / 2)
                
                await self.page.mouse.click(click_x, click_y)
                print(f"✅ Clicked slider at position for value: {target_value}")
                
                return {
                    'success': True,
                    'pattern': 'slider',
                    'value': target_value,
                    'confidence': 0.85
                }
            
            # Strategy 2: Try to set value directly
            await slider.evaluate(f'el => el.value = {target_value}')
            await slider.dispatch_event('change')
            
            return {
                'success': True,
                'pattern': 'slider',
                'value': target_value,
                'confidence': 0.8
            }
            
        except Exception as e:
            print(f"❌ Slider handling error: {e}")
            return {'success': False, 'error': str(e)}
    
    # ==========================================
    # CAROUSEL PATTERN HANDLING  
    # ==========================================
    
    async def _feels_like_carousel(self) -> bool:
        """Does this FEEL like a carousel?"""
        try:
            # Look for carousel indicators
            carousel_hints = [
                '.carousel',
                '.swiper',
                '.slick',
                '[role="navigation"] button',  # Nav buttons
                '.dots',  # Pagination dots
                'button[aria-label*="next"]',
                'button[aria-label*="previous"]'
            ]
            
            for hint in carousel_hints:
                if await self.page.query_selector(hint):
                    return True
                    
            # Also check for multiple images with navigation
            images = await self.page.query_selector_all('img')
            nav_buttons = await self.page.query_selector_all('button')
            
            if len(images) > 2 and len(nav_buttons) >= 2:
                print("🎠 Carousel intuition: Multiple images with navigation detected")
                return True
                
            return False
        except:
            return False
    
    async def _handle_carousel_pattern(self, question_text: str) -> Dict:
        """Handle carousel navigation and selection"""
        print("🎠 CAROUSEL HANDLER ACTIVATED")
        
        try:
            # Implementation would handle carousel navigation
            # For now, return a placeholder
            return {
                'success': False,
                'reason': 'Carousel handler in development',
                'pattern': 'carousel'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _handle_star_rating_pattern(self, question_text: str) -> Dict:
        """Handle star rating selection"""
        print("⭐ STAR RATING HANDLER ACTIVATED")
        
        try:
            # Placeholder for star rating handler
            return {
                'success': False,
                'reason': 'Star rating handler in development',
                'pattern': 'star_rating'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _handle_brand_grid_pattern(self, question_text: str) -> Dict:
        """Handle brand grid selection"""
        print("🏢 BRAND GRID HANDLER ACTIVATED")
        
        try:
            # Placeholder for brand grid handler
            return {
                'success': False,
                'reason': 'Brand grid handler in development',
                'pattern': 'brand_grid'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _handle_radio_matrix_pattern(self, question_text: str) -> Dict:
        """Handle radio button matrix selection"""
        print("📻 RADIO MATRIX HANDLER ACTIVATED")
        
        try:
            # Placeholder for radio matrix handler
            return {
                'success': False,
                'reason': 'Radio matrix handler in development',
                'pattern': 'radio_matrix'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _handle_likert_scale_pattern(self, question_text: str) -> Dict:
        """Handle Likert scale selection"""
        print("📊 LIKERT SCALE HANDLER ACTIVATED")
        
        try:
            # Placeholder for Likert scale handler
            return {
                'success': False,
                'reason': 'Likert scale handler in development',
                'pattern': 'likert_scale'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==========================================
    # LEARNING & EVOLUTION
    # ==========================================
    
    async def learn_from_interaction(self, pattern_type: str, success: bool, details: Dict):
        """
        Learn from each interaction to improve pattern recognition
        This is how Quenito develops better intuition over time!
        """
        learning_data = {
            'pattern_type': pattern_type,
            'success': success,
            'timestamp': asyncio.get_event_loop().time(),
            'details': details
        }
        
        # Save to learning system for pattern evolution
        print(f"🧠 Learning: {pattern_type} - Success: {success}")
        
        # This would integrate with the learning service
        # to improve pattern recognition over time