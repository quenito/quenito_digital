#!/usr/bin/env python3
"""
🖱️ Trust Rating UI Module
Handles all UI interactions for trust rating questions.

This module manages:
- Text-based trust option selection
- Numeric scale selection (1-5, 1-7, 1-10, etc.)
- Visual scale clicking
- Radio button and dropdown handling
- Trust rating specific navigation

ARCHITECTURE: Extends BaseUI with trust-rating-specific functionality
"""

import asyncio
from typing import Dict, Any, List, Optional
from playwright.async_api import Page, ElementHandle
from handlers.shared.base_ui import BaseUI


class TrustRatingUI(BaseUI):
    """
    🖱️ UI Interaction Handler for Trust Rating Questions
    
    Extends BaseUI with trust-specific functionality:
    - Trust text option selection
    - Numeric rating selection
    - Scale clicking
    - Trust-specific element detection
    """
    
    def __init__(self, page: Page):
        """Initialize with base UI functionality"""
        super().__init__(page)
        print("🖱️ TrustRatingUI initialized with BaseUI foundation")
    
    # ========================================
    # TEXT OPTION SELECTION
    # ========================================
    
    async def select_trust_text_option(self, text_option: str) -> bool:
        """
        Select a text-based trust option (e.g., "Very trustworthy")
        
        Args:
            text_option: The text to look for and select
            
        Returns:
            True if successfully selected
        """
        try:
            # Multiple selectors for different implementations
            selectors = [
                f'label:has-text("{text_option}")',
                f'*:has-text("{text_option}")',
                f'input[value="{text_option}"]',
                f'option:has-text("{text_option}")'
            ]
            
            for selector in selectors:
                elements = await self.find_visible_elements(selector)
                
                for element in elements:
                    # Check if it's selectable
                    if await self._is_selectable_element(element):
                        await element.click()
                        await self.human_delay()
                        print(f"✅ Selected trust option: {text_option}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting trust text option: {e}")
            return False
    
    # ========================================
    # NUMERIC OPTION SELECTION
    # ========================================
    
    async def select_trust_numeric_option(self, value: int, scale_type: str) -> bool:
        """
        Select a numeric trust rating
        
        Args:
            value: The numeric value to select
            scale_type: Type of scale for context
            
        Returns:
            True if successfully selected
        """
        try:
            value_str = str(value)
            
            # Try radio buttons first
            radio_selectors = [
                f'input[type="radio"][value="{value_str}"]',
                f'input[type="radio"][id*="{value_str}"]',
                f'input[type="radio"][name*="trust"][value="{value_str}"]'
            ]
            
            for selector in radio_selectors:
                elements = await self.find_visible_elements(selector)
                if elements:
                    await elements[0].click()
                    await self.human_delay()
                    print(f"✅ Selected trust rating: {value}")
                    return True
            
            # Try clickable labels with numbers
            label_selectors = [
                f'label:has-text("{value_str}")',
                f'span:has-text("{value_str}")',
                f'div[role="radio"]:has-text("{value_str}")'
            ]
            
            for selector in label_selectors:
                elements = await self.find_visible_elements(selector)
                
                for element in elements:
                    # Verify this is a rating element (not just text)
                    if await self._is_rating_element(element, value_str):
                        await element.click()
                        await self.human_delay()
                        print(f"✅ Selected trust rating: {value}")
                        return True
            
            # Try dropdown selection
            if await self._select_dropdown_value(value_str):
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error selecting numeric trust option: {e}")
            return False
    
    # ========================================
    # SCALE CLICKING
    # ========================================
    
    async def click_scale_position(self, value: int, scale_data: Dict[str, Any]) -> bool:
        """
        Click on a visual scale at the appropriate position
        
        Args:
            value: The value to select
            scale_data: Scale configuration data
            
        Returns:
            True if successfully clicked
        """
        try:
            # Look for scale containers
            scale_selectors = [
                '.trust-scale', '.rating-scale', '.scale-container',
                '[role="slider"]', '.slider-container'
            ]
            
            for selector in scale_selectors:
                scales = await self.find_visible_elements(selector)
                
                for scale in scales:
                    # Get scale dimensions
                    box = await scale.bounding_box()
                    if not box:
                        continue
                    
                    # Calculate click position
                    scale_range = scale_data.get('range', [])
                    if scale_range:
                        min_val = min(scale_range)
                        max_val = max(scale_range)
                        
                        # Calculate percentage position
                        percentage = (value - min_val) / (max_val - min_val)
                        
                        # Calculate click coordinates
                        click_x = box['x'] + (box['width'] * percentage)
                        click_y = box['y'] + (box['height'] / 2)
                        
                        # Click at calculated position
                        await self.page.mouse.click(click_x, click_y)
                        await self.human_delay()
                        print(f"✅ Clicked scale at position for value: {value}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error clicking scale position: {e}")
            return False
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    async def _is_selectable_element(self, element: ElementHandle) -> bool:
        """Check if element is selectable (clickable for selection)"""
        try:
            # Check if it's an input element
            tag_name = await element.evaluate('el => el.tagName.toLowerCase()')
            
            if tag_name in ['input', 'option']:
                return True
            
            # Check if it has role attributes suggesting selectability
            role = await element.get_attribute('role')
            if role in ['radio', 'checkbox', 'option']:
                return True
            
            # Check if it's associated with an input
            for_attr = await element.get_attribute('for')
            if for_attr:
                return True
            
            # Check if it contains a radio/checkbox
            has_input = await element.evaluate('''el => {
                return el.querySelector('input[type="radio"], input[type="checkbox"]') !== null;
            }''')
            
            return has_input
            
        except Exception:
            return False
    
    async def _is_rating_element(self, element: ElementHandle, value: str) -> bool:
        """Verify element is actually a rating element"""
        try:
            text = await element.inner_text()
            
            # Should be just the number or number with minimal text
            if text.strip() == value:
                return True
            
            # Check if it's within a rating context
            parent_text = await element.evaluate('''el => {
                const parent = el.parentElement;
                return parent ? parent.innerText : '';
            }''')
            
            # Look for rating context clues
            rating_keywords = ['trust', 'rate', 'scale', 'score']
            return any(keyword in parent_text.lower() for keyword in rating_keywords)
            
        except Exception:
            return False
    
    async def _select_dropdown_value(self, value: str) -> bool:
        """Select value from dropdown"""
        try:
            selects = await self.find_visible_elements('select')
            
            for select in selects:
                # Check if this is a trust-related dropdown
                name = await select.get_attribute('name') or ''
                id_attr = await select.get_attribute('id') or ''
                
                if any(word in name.lower() + id_attr.lower() for word in ['trust', 'rate', 'rating']):
                    await select.select_option(value)
                    await self.human_delay()
                    print(f"✅ Selected trust rating from dropdown: {value}")
                    return True
            
            return False
            
        except Exception:
            return False
    
    # ========================================
    # NAVIGATION
    # ========================================
    
    async def try_navigation(self) -> bool:
        """Navigate to next page after trust rating"""
        # Trust rating specific navigation selectors
        custom_selectors = [
            ".trust-next", ".rating-submit", 
            "button[type='submit']", ".continue-button"
        ]
        
        return await self.click_navigation_button(custom_selectors=custom_selectors)