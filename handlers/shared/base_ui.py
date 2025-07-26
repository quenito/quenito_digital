#!/usr/bin/env python3
"""
🎯 Base UI Module v1.0 - Common UI Functionality for All Handlers
Provides shared UI interaction methods that all survey handlers can use.

This module provides:
- Common element detection methods
- Basic interaction strategies
- Navigation functionality
- Element visibility and state checking
- Human-like timing utilities

ARCHITECTURE: Base class for all handler-specific UI modules
"""

import time
import random
from typing import List, Optional, Any, Tuple, Dict 
from playwright.async_api import Page, ElementHandle, Locator


class BaseUI:
    """
    🎯 Base UI Handler - Common UI Functionality
    
    Provides shared UI methods that all survey handlers can inherit.
    Specific handlers (demographics, likert, matrix) extend this base.
    """
    
    def __init__(self, page: Page):
        """
        Initialize base UI handler
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        
        # Human-like behavior settings
        self.min_think_time = 0.5
        self.max_think_time = 2.0
        self.min_type_delay = 0.1
        self.max_type_delay = 0.3
        
        print("🎯 BaseUI initialized")
    
    # ========================================
    # COMMON ELEMENT DETECTION
    # ========================================
    
    async def find_visible_elements(self, selector: str) -> List[ElementHandle]:
        """Find all visible elements matching a selector"""
        try:
            elements = await self.page.query_selector_all(selector)
            visible_elements = []
            
            for element in elements:
                if await element.is_visible():
                    visible_elements.append(element)
            
            return visible_elements
            
        except Exception as e:
            print(f"❌ Error finding elements with selector '{selector}': {e}")
            return []
    
    async def find_first_visible_element(self, selector: str) -> Optional[ElementHandle]:
        """Find the first visible element matching a selector"""
        try:
            elements = await self.find_visible_elements(selector)
            return elements[0] if elements else None
            
        except Exception as e:
            print(f"❌ Error finding first element with selector '{selector}': {e}")
            return None
    
    async def element_exists(self, selector: str) -> bool:
        """Check if an element exists on the page"""
        try:
            element = await self.page.query_selector(selector)
            return element is not None
            
        except Exception:
            return False
    
    async def element_is_visible(self, selector: str) -> bool:
        """Check if an element exists and is visible"""
        try:
            element = await self.page.query_selector(selector)
            if element:
                return await element.is_visible()
            return False
            
        except Exception:
            return False
    
    # ========================================
    # COMMON INTERACTIONS
    # ========================================
    
    async def safe_click(self, element: ElementHandle, force: bool = False) -> bool:
        """Safely click an element with error handling"""
        try:
            if force:
                await element.click(force=True)
            else:
                await element.click()
            await self.page.wait_for_timeout(300)
            return True
            
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False
    
    async def safe_fill(self, element: ElementHandle, value: str, clear_first: bool = True) -> bool:
        """Safely fill an input element"""
        try:
            if clear_first:
                await element.fill('')
                await self.page.wait_for_timeout(100)
            
            await element.fill(str(value))
            await self.page.wait_for_timeout(200)
            return True
            
        except Exception as e:
            print(f"❌ Fill failed: {e}")
            return False
    
    async def scroll_to_element(self, element: ElementHandle) -> bool:
        """Scroll an element into view"""
        try:
            await element.scroll_into_view_if_needed()
            await self.page.wait_for_timeout(300)
            return True
            
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
            return False
    
    # ========================================
    # NAVIGATION METHODS
    # ========================================
    
    async def find_navigation_button(self, 
                                   button_texts: List[str] = None,
                                   custom_selectors: List[str] = None) -> Optional[ElementHandle]:
        """
        Find navigation buttons (Next, Continue, Submit, etc.)
        
        Args:
            button_texts: List of button texts to search for
            custom_selectors: Additional selectors to try
        """
        try:
            # Default button texts
            if not button_texts:
                button_texts = [
                    "Next", "next", "NEXT",
                    "Continue", "continue", "CONTINUE",
                    "Submit", "submit", "SUBMIT",
                    "Done", "done", "DONE",
                    "Proceed", "proceed", "PROCEED",
                    "Forward", "forward", "FORWARD"
                ]
            
            # Try exact text matches
            for text in button_texts:
                selectors = [
                    f"button:has-text('{text}')",
                    f"input[type='submit'][value='{text}']",
                    f"input[type='button'][value='{text}']",
                    f"a:has-text('{text}')",
                    f"[role='button']:has-text('{text}')"
                ]
                
                for selector in selectors:
                    element = await self.find_first_visible_element(selector)
                    if element:
                        print(f"✅ Found navigation button: '{text}'")
                        return element
            
            # Try attribute-based selectors
            attribute_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button[class*='next']",
                "button[class*='continue']",
                "button[class*='submit']",
                ".btn-primary",
                ".btn-next",
                ".continue-button",
                ".submit-button"
            ]
            
            # Add custom selectors if provided
            if custom_selectors:
                attribute_selectors.extend(custom_selectors)
            
            for selector in attribute_selectors:
                element = await self.find_first_visible_element(selector)
                if element:
                    text = await self.get_element_text(element)
                    print(f"✅ Found navigation button by selector: '{text}'")
                    return element
            
            print("❌ No navigation button found")
            return None
            
        except Exception as e:
            print(f"❌ Error finding navigation button: {e}")
            return None
    
    async def click_navigation_button(self, 
                                    button_texts: List[str] = None,
                                    custom_selectors: List[str] = None) -> bool:
        """Find and click a navigation button"""
        try:
            button = await self.find_navigation_button(button_texts, custom_selectors)
            
            if not button:
                return False
            
            # Try multiple click strategies
            strategies = [
                lambda: button.click(),
                lambda: button.click(force=True),
                lambda: button.evaluate("element => element.click()"),
                lambda: self._keyboard_click(button)
            ]
            
            for i, strategy in enumerate(strategies):
                try:
                    await strategy()
                    await self.page.wait_for_timeout(500)
                    print(f"✅ Navigation successful with strategy {i+1}")
                    return True
                except Exception as e:
                    print(f"⚠️ Strategy {i+1} failed: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Error clicking navigation: {e}")
            return False
    
    async def _keyboard_click(self, element: ElementHandle) -> None:
        """Click using keyboard (focus + Enter)"""
        await element.focus()
        await self.page.keyboard.press("Enter")
    
    # ========================================
    # ELEMENT STATE & TEXT
    # ========================================
    
    async def get_element_text(self, element: ElementHandle) -> str:
        """Get text content of an element"""
        try:
            # Try inner_text first
            text = await element.inner_text()
            if text:
                return text.strip()
            
            # Try text_content
            text = await element.text_content()
            if text:
                return text.strip()
            
            # Try value attribute (for inputs)
            text = await element.get_attribute("value")
            if text:
                return text.strip()
            
            return ""
            
        except Exception:
            return ""
    
    async def get_element_value(self, element: ElementHandle) -> str:
        """Get value of an input element"""
        try:
            value = await element.get_attribute("value")
            return value or ""
            
        except Exception:
            return ""
    
    async def is_element_enabled(self, element: ElementHandle) -> bool:
        """Check if an element is enabled"""
        try:
            return await element.is_enabled()
            
        except Exception:
            return False
    
    async def is_element_checked(self, element: ElementHandle) -> bool:
        """Check if a checkbox/radio is checked"""
        try:
            return await element.is_checked()
            
        except Exception:
            return False
    
    # ========================================
    # WAIT METHODS
    # ========================================
    
    async def wait_for_element(self, selector: str, timeout: int = 10000) -> Optional[ElementHandle]:
        """Wait for an element to appear"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return await self.page.query_selector(selector)
            
        except Exception as e:
            print(f"⏱️ Timeout waiting for element '{selector}': {e}")
            return None
    
    async def wait_for_element_visible(self, selector: str, timeout: int = 10000) -> Optional[ElementHandle]:
        """Wait for an element to be visible"""
        try:
            await self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return await self.page.query_selector(selector)
            
        except Exception as e:
            print(f"⏱️ Timeout waiting for visible element '{selector}': {e}")
            return None
    
    async def wait_for_navigation(self, timeout: int = 30000) -> bool:
        """Wait for page navigation to complete"""
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            return True
            
        except Exception:
            # Try domcontentloaded as fallback
            try:
                await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                return True
            except Exception:
                return False
    
    # ========================================
    # HUMAN-LIKE TIMING
    # ========================================
    
    def human_delay(self, 
                   delay_type: str = "think",
                   min_delay: Optional[float] = None,
                   max_delay: Optional[float] = None) -> None:
        """Add human-like delays"""
        
        if delay_type == "think":
            min_d = min_delay or self.min_think_time
            max_d = max_delay or self.max_think_time
        elif delay_type == "type":
            min_d = min_delay or self.min_type_delay
            max_d = max_delay or self.max_type_delay
        else:
            min_d = min_delay or 0.3
            max_d = max_delay or 1.0
        
        delay = random.uniform(min_d, max_d)
        time.sleep(delay)
    
    def set_human_timing(self, 
                        min_think: float = 0.5,
                        max_think: float = 2.0,
                        min_type: float = 0.1,
                        max_type: float = 0.3) -> None:
        """Configure human-like timing parameters"""
        self.min_think_time = min_think
        self.max_think_time = max_think
        self.min_type_delay = min_type
        self.max_type_delay = max_type
    
    # ========================================
    # PAGE CONTENT HELPERS
    # ========================================
    
    async def get_page_text(self) -> str:
        """Get all text content from the page"""
        try:
            # Try body text first
            text = await self.page.locator('body').text_content()
            if text:
                return text
                
        except Exception:
            pass
        
        try:
            # Try JavaScript evaluation
            text = await self.page.evaluate('() => document.body.textContent')
            if text:
                return text
                
        except Exception:
            pass
        
        return ""
    
    async def get_page_title(self) -> str:
        """Get the page title"""
        try:
            return await self.page.title()
            
        except Exception:
            return ""
    
    async def get_page_url(self) -> str:
        """Get the current page URL"""
        try:
            return self.page.url
            
        except Exception:
            return ""
    
    # ========================================
    # SCREENSHOT & DEBUG
    # ========================================
    
    async def take_screenshot(self, filename: str = None) -> Optional[str]:
        """Take a screenshot for debugging"""
        try:
            if not filename:
                filename = f"screenshot_{int(time.time())}.png"
            
            await self.page.screenshot(path=filename)
            print(f"📸 Screenshot saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None
    
    async def debug_element_info(self, element: ElementHandle) -> Dict[str, Any]:
        """Get debug information about an element"""
        try:
            info = {
                "tag": await element.evaluate("el => el.tagName"),
                "id": await element.get_attribute("id"),
                "class": await element.get_attribute("class"),
                "type": await element.get_attribute("type"),
                "name": await element.get_attribute("name"),
                "value": await element.get_attribute("value"),
                "text": await self.get_element_text(element),
                "visible": await element.is_visible(),
                "enabled": await element.is_enabled()
            }
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def __str__(self) -> str:
        """String representation"""
        return "BaseUI(Common UI Handler)"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"BaseUI(page_url={self.page.url if self.page else 'None'})"