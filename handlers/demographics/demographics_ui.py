#!/usr/bin/env python3
"""
🖱️ Demographics UI Module v2.1 - UI Interaction & Element Detection
Handles all UI interactions for demographics questions.

This module manages:
- Element detection (dropdowns, radio buttons, text inputs)
- Element interaction (clicking, filling, selecting)
- Demographics-specific UI patterns
- Specialized matching logic

ARCHITECTURE: Extends BaseUI with demographics-specific functionality
"""

import time
import random
from typing import Dict, Any, List, Optional, Tuple
from playwright.async_api import Page, ElementHandle
from handlers.shared.base_ui import BaseUI


class DemographicsUI(BaseUI):
    """
    🖱️ UI Interaction Handler for Demographics Questions
    
    Extends BaseUI with demographics-specific functionality:
    - Specialized element detection
    - Demographics-specific interaction strategies
    - Custom matching logic for demographic data
    """
    
    def __init__(self, page: Page):
        """Initialize with base UI functionality"""
        super().__init__(page)
        print("🖱️ DemographicsUI initialized with BaseUI foundation")
    
    # ========================================
    # ELEMENT DETECTION METHODS (Simplified)
    # ========================================
    
    async def detect_dropdown_elements(self) -> List[ElementHandle]:
        """Detect dropdown/select elements on the page"""
        elements = await self.find_visible_elements('select')
        print(f"📋 Found {len(elements)} visible dropdown elements")
        return elements
    
    async def detect_radio_elements(self) -> List[ElementHandle]:
        """Detect radio button elements on the page"""
        elements = await self.find_visible_elements('input[type="radio"]')
        print(f"🔘 Found {len(elements)} visible radio buttons")
        return elements
    
    async def detect_text_input_elements(self) -> List[ElementHandle]:
        """Detect text input elements on the page"""
        try:
            # Multiple selectors for text inputs
            selectors = [
                'input[type="text"]',
                'input[type="number"]',
                'input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="radio"]):not([type="checkbox"])',
                'textarea'
            ]
            
            all_inputs = []
            for selector in selectors:
                inputs = await self.find_visible_elements(selector)
                all_inputs.extend(inputs)
            
            # Remove duplicates
            unique_inputs = []
            for inp in all_inputs:
                if inp not in unique_inputs:
                    unique_inputs.append(inp)
            
            print(f"📝 Found {len(unique_inputs)} visible text input elements")
            return unique_inputs
            
        except Exception as e:
            print(f"❌ Error detecting text inputs: {e}")
            return []
    
    async def detect_checkbox_elements(self) -> List[ElementHandle]:
        """Detect checkbox elements on the page"""
        elements = await self.find_visible_elements('input[type="checkbox"]')
        print(f"☑️ Found {len(elements)} visible checkboxes")
        return elements
    
    # ========================================
    # TEXT INPUT STRATEGIES (Demographics-specific)
    # ========================================
    
    async def robust_click_and_fill_strategy(self, value: str) -> bool:
        """🧠 Standard click and fill strategy"""
        try:
            inputs = await self.detect_text_input_elements()
            
            for input_elem in inputs:
                if await self.safe_click(input_elem) and await self.safe_fill(input_elem, str(value)):
                    print(f"🧠 ✅ Standard click strategy successful")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Standard click strategy failed: {e}")
            return False

    async def force_click_strategy(self, value: str) -> bool:
        """🧠 Force click strategy"""
        try:
            inputs = await self.detect_text_input_elements()
            
            for input_elem in inputs:
                if await self.safe_click(input_elem, force=True) and await self.safe_fill(input_elem, str(value)):
                    print(f"🧠 ✅ Force click strategy successful")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Force click strategy failed: {e}")
            return False

    async def javascript_strategy(self, value: str) -> bool:
        """🧠 JavaScript strategy"""
        try:
            inputs = await self.detect_text_input_elements()
            
            for input_elem in inputs:
                try:
                    await self.page.evaluate('(element) => element.click()', input_elem)
                    await self.page.wait_for_timeout(300)
                    if await self.safe_fill(input_elem, str(value)):
                        print(f"🧠 ✅ JavaScript strategy successful")
                        return True
                except Exception:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ JavaScript strategy failed: {e}")
            return False

    async def keyboard_focus_strategy(self, value: str) -> bool:
        """🧠 Keyboard focus strategy"""
        try:
            inputs = await self.detect_text_input_elements()
            
            for input_elem in inputs:
                try:
                    await input_elem.focus()
                    await self.page.wait_for_timeout(300)
                    if await self.safe_fill(input_elem, str(value)):
                        print(f"🧠 ✅ Keyboard focus strategy successful")
                        return True
                except Exception:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Keyboard focus strategy failed: {e}")
            return False

    async def coordinate_click_strategy(self, value: str) -> bool:
        """🧠 Coordinate click strategy"""
        try:
            inputs = await self.detect_text_input_elements()
            
            for input_elem in inputs:
                try:
                    bbox = await input_elem.bounding_box()
                    if bbox:
                        x = bbox['x'] + bbox['width'] / 2
                        y = bbox['y'] + bbox['height'] / 2
                        await self.page.mouse.click(x, y)
                        await self.page.wait_for_timeout(300)
                        if await self.safe_fill(input_elem, str(value)):
                            print(f"🧠 ✅ Coordinate click strategy successful")
                            return True
                except Exception:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Coordinate click strategy failed: {e}")
            return False
    
    async def robust_click_and_fill(self, input_elem: ElementHandle, value: str) -> bool:
        """🧠 Robust clicking and filling with multiple strategies"""
        strategies = [
            ("standard click", lambda: self.safe_click(input_elem)),
            ("force click", lambda: self.safe_click(input_elem, force=True)),
            ("focus", lambda: input_elem.focus()),
            ("JS click", lambda: self.page.evaluate('(element) => element.click()', input_elem)),
            ("JS value", lambda: self.page.evaluate(
                f'(element) => {{ element.value = "{value}"; '
                f'element.dispatchEvent(new Event("input", {{ bubbles: true }})); '
                f'element.dispatchEvent(new Event("change", {{ bubbles: true }})); }}', 
                input_elem
            ))
        ]
        
        for i, (name, strategy) in enumerate(strategies, 1):
            try:
                await strategy()
                if i < 5:  # Don't fill after JS value strategy
                    await self.safe_fill(input_elem, str(value))
                print(f"🧠 ✅ Strategy {i} ({name}) successful")
                return True
            except Exception as e:
                print(f"⚠️ Strategy {i} failed: {e}")
                continue
        
        print(f"❌ All click strategies failed")
        return False
    
    # ========================================
    # RADIO BUTTON METHODS (Demographics-specific)
    # ========================================
    
    async def radio_button_strategy(self, response_value: str) -> bool:
        """🔘 PROVEN: Radio button selection strategy for gender/choice questions"""
        try:
            print(f"🔘 Trying radio button strategy for: {response_value}")
            
            radios = await self.detect_radio_elements()
            print(f"🔘 Found {len(radios)} radio buttons")
            
            if not radios:
                print("❌ No radio buttons found on page")
                return False
            
            for i, radio in enumerate(radios):
                try:
                    label_text = await self.get_radio_label_text_enhanced(radio)
                    print(f"🔘 Radio {i+1}: '{label_text}'")
                    
                    if self.radio_matches_response(response_value, label_text):
                        print(f"🎯 MATCH FOUND: '{response_value}' matches '{label_text}'")
                        
                        if await self.safe_click(radio, force=True):
                            await self.page.wait_for_timeout(500)
                            
                            if await self.is_element_checked(radio):
                                print(f"🔘 ✅ Successfully selected: {label_text}")
                                return True
                            else:
                                print(f"⚠️ Radio clicked but not checked, trying check method")
                                await radio.check()
                                await self.page.wait_for_timeout(500)
                                
                                if await self.is_element_checked(radio):
                                    print(f"🔘 ✅ Force selection succeeded: {label_text}")
                                    return True
                            
                except Exception as e:
                    print(f"⚠️ Error with radio {i+1}: {e}")
                    continue
            
            print(f"❌ No matching radio button found for: {response_value}")
            return False
            
        except Exception as e:
            print(f"❌ Radio button strategy failed: {e}")
            return False
    
    async def select_radio_option(self, target_value: str, keywords: List[str]) -> bool:
        """🧠 Select a radio button option based on target value and keywords"""
        try:
            radios = await self.detect_radio_elements()
            
            for radio in radios:
                label_text = await self.get_radio_label_text(radio)
                
                if self.text_matches(label_text, target_value, keywords):
                    if await self.safe_click(radio):
                        print(f"🧠 ✅ Selected radio option: {label_text}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting radio option: {e}")
            return False
    
    # ========================================
    # DROPDOWN METHODS (Demographics-specific)
    # ========================================
    
    async def select_dropdown_option(self, target_value: str) -> bool:
        """🧠 Select a dropdown option"""
        try:
            selects = await self.detect_dropdown_elements()
            
            for select in selects:
                options = await select.query_selector_all('option')
                
                for option in options:
                    option_text = await self.get_element_text(option)
                    if self.text_matches(option_text, target_value, []):
                        option_value = await option.get_attribute('value')
                        await select.select_option(value=option_value)
                        await self.page.wait_for_timeout(300)
                        print(f"🧠 ✅ Selected dropdown option: {option_text}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting dropdown option: {e}")
            return False
    
    async def select_dropdown_option_enhanced(self, response_value: str) -> bool:
        """Enhanced dropdown selection with better matching"""
        try:
            selects = await self.detect_dropdown_elements()
            
            for select in selects:
                try:
                    options = await select.query_selector_all('option')
                    
                    for option in options:
                        option_text = await self.get_element_text(option)
                        option_value = await self.get_element_value(option)
                        
                        if (response_value.lower() in option_text.lower() or 
                            response_value.lower() in option_value.lower()):
                            
                            await select.select_option(value=option_value)
                            print(f"📋 ✅ Selected dropdown option: {option_text}")
                            return True
                            
                except Exception as e:
                    print(f"⚠️ Error with select element: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Enhanced dropdown selection failed: {e}")
            return False
    
    # ========================================
    # CHECKBOX METHODS (Demographics-specific)
    # ========================================
    
    async def select_checkbox_option(self, target_value: str, keywords: List[str]) -> bool:
        """🧠 Select a checkbox option based on target value and keywords"""
        try:
            checkboxes = await self.detect_checkbox_elements()
            
            for checkbox in checkboxes:
                label_text = await self.get_checkbox_label_text(checkbox)
                
                if self.text_matches(label_text, target_value, keywords):
                    if not await self.is_element_checked(checkbox):
                        if await self.safe_click(checkbox):
                            print(f"🧠 ✅ Selected checkbox option: {label_text}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting checkbox option: {e}")
            return False
    
    # ========================================
    # TEXT INPUT METHODS (Simplified)
    # ========================================
    
    async def fill_text_input(self, value: str) -> bool:
        """🧠 Fill a text input field"""
        try:
            inputs = await self.detect_text_input_elements()
            
            for input_elem in inputs:
                if await self.robust_click_and_fill(input_elem, value):
                    print(f"🧠 ✅ Filled text input: {value}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error filling text input: {e}")
            return False
    
    # ========================================
    # NAVIGATION (Use base class)
    # ========================================
    
    async def try_navigation(self) -> bool:
        """🧠 Enhanced navigation using base class methods"""
        # Add SurveyMonkey-specific selectors
        custom_selectors = [
            ".sv-next-button",
            ".sv_next_btn", 
            "[data-testid='next-button']",
            ".notranslate.btn.btn-primary",
            "button.btn.btn-primary",
            ".survey-button-next"
        ]
        
        return await self.click_navigation_button(custom_selectors=custom_selectors)
    
    # ========================================
    # LABEL TEXT EXTRACTION (Demographics-specific)
    # ========================================
    
    async def get_radio_label_text(self, radio_element: ElementHandle) -> str:
        """🧠 Get the label text associated with a radio button"""
        try:
            # Try ID-based label
            label_id = await radio_element.get_attribute('id')
            if label_id:
                label = await self.find_first_visible_element(f'label[for="{label_id}"]')
                if label:
                    return await self.get_element_text(label)
            
            # Try parent element text
            parent = radio_element.locator('..')
            if parent:
                return await parent.inner_text()
            
            return ""
            
        except Exception:
            return ""
    
    async def get_radio_label_text_enhanced(self, radio: ElementHandle) -> str:
        """Get the text label associated with a radio button (enhanced version)"""
        try:
            # Method 1: Check for associated label
            text = await self.get_radio_label_text(radio)
            if text:
                return text.strip()
            
            # Method 2: Check parent label
            try:
                parent_label = await radio.query_selector('xpath=ancestor::label[1]')
                if parent_label:
                    text = await self.get_element_text(parent_label)
                    return text.strip()
            except:
                pass
            
            # Method 3: Check next sibling text
            try:
                next_sibling = await radio.evaluate_handle('node => node.nextSibling')
                if next_sibling:
                    text = await next_sibling.evaluate('node => node.textContent || ""')
                    if text.strip():
                        return text.strip()
            except:
                pass
            
            # Method 4: Check value attribute
            value = await self.get_element_value(radio)
            if value:
                return value
            
            return "Unknown label"
            
        except Exception as e:
            print(f"⚠️ Error getting radio label: {e}")
            return "Error getting label"
    
    async def get_checkbox_label_text(self, checkbox_element: ElementHandle) -> str:
        """🧠 Get the label text associated with a checkbox"""
        # Use same logic as radio buttons
        return await self.get_radio_label_text(checkbox_element)
    
    # ========================================
    # MATCHING METHODS (Demographics-specific)
    # ========================================
    
    def text_matches(self, text: str, target: str, keywords: List[str]) -> bool:
        """🧠 Check if text matches target or contains keywords"""
        if not text:
            return False
        
        text_lower = text.lower()
        target_lower = target.lower()
        
        # Direct match
        if target_lower in text_lower:
            return True
        
        # Keyword matches
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False
    
    def radio_matches_response(self, response_value: str, label_text: str) -> bool:
        """Check if a radio button label matches our intended response"""
        response_lower = response_value.lower().strip()
        label_lower = label_text.lower().strip()
        
        # Direct match
        if response_lower == label_lower:
            return True
        
        # Gender-specific matching
        if response_lower == "male" and any(word in label_lower for word in ["male", "man", "m"]):
            return True
        
        if response_lower == "female" and any(word in label_lower for word in ["female", "woman", "f"]):
            return True
        
        # Contains matching
        if response_lower in label_lower or label_lower in response_value.lower():
            return True
        
        # Location matching (for state questions)
        location_mappings = {
            "new south wales": ["nsw", "new south wales", "sydney"],
            "victoria": ["vic", "victoria", "melbourne"],
            "queensland": ["qld", "queensland", "brisbane"],
            "south australia": ["sa", "south australia", "adelaide"],
            "western australia": ["wa", "western australia", "perth"],
            "tasmania": ["tas", "tasmania", "hobart"],
            "northern territory": ["nt", "northern territory", "darwin"],
            "australian capital territory": ["act", "australian capital territory", "canberra"]
        }
        
        for full_name, variations in location_mappings.items():
            if response_lower in variations and any(var in label_lower for var in variations):
                return True
        
        return False