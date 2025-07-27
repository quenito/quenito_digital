#!/usr/bin/env python3
"""
🖱️ Brand Familiarity UI Module
Handles all UI interactions for brand familiarity questions

This module:
- Detects brand matrix layouts
- Handles radio button selections
- Manages human-like interactions
- Navigates between questions
"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio
import random
import time


class BrandFamiliarityUI:
    """UI interaction methods for brand familiarity questions"""
    
    def __init__(self, page):
        """Initialize with page object"""
        self.page = page
        
        # Human simulation parameters
        self.wpm = random.randint(40, 80)
        self.thinking_speed = random.uniform(0.8, 1.3)
        
        print("🖱️ Brand Familiarity UI module initialized")
        print(f"   - Human simulation: {self.wpm} WPM, thinking {self.thinking_speed:.1f}x")
    
    async def detect_brand_matrix_elements(self) -> Dict[str, Any]:
        """
        Detect brand matrix layout elements
        
        Returns dict with:
        - brands: List of brand names/labels
        - radio_groups: Radio buttons grouped by brand
        - response_options: Available response levels
        - layout_type: 'table' or 'div' based layout
        """
        elements = {
            'brands': [],
            'radio_groups': {},
            'response_options': [],
            'layout_type': None
        }
        
        try:
            # Check for table-based matrix first
            tables = await self.page.query_selector_all('table')
            for table in tables:
                if await self._is_brand_matrix_table(table):
                    elements['layout_type'] = 'table'
                    return await self._extract_table_matrix(table)
            
            # Check for div-based matrix
            matrix_containers = await self.page.query_selector_all(
                'div[class*="matrix"], div[class*="grid"], div[class*="brand"]'
            )
            
            for container in matrix_containers:
                if await self._is_brand_matrix_div(container):
                    elements['layout_type'] = 'div'
                    return await self._extract_div_matrix(container)
            
            # Fallback: Look for radio button groups
            radio_groups = await self._detect_radio_groups()
            if len(radio_groups) >= 3:  # Multiple brands likely
                elements['layout_type'] = 'radio_groups'
                elements['radio_groups'] = radio_groups
                elements['brands'] = list(radio_groups.keys())
            
            return elements
            
        except Exception as e:
            print(f"❌ Error detecting matrix elements: {e}")
            return elements
    
    async def select_familiarity_level(self, brand: str, level: str) -> bool:
        """
        Select familiarity level for a specific brand
        
        Args:
            brand: Brand name to find
            level: Familiarity level to select
            
        Returns:
            True if successful
        """
        try:
            # Add human-like delay
            await self._thinking_delay()
            
            # Find brand row/section
            brand_element = await self._find_brand_element(brand)
            if not brand_element:
                print(f"❌ Could not find brand: {brand}")
                return False
            
            # Find radio buttons in same row/container
            radios = await self._get_brand_radio_buttons(brand_element)
            if not radios:
                print(f"❌ No radio buttons found for brand: {brand}")
                return False
            
            # Select the appropriate level
            for radio in radios:
                label_text = await self._get_radio_label_text(radio)
                if level.lower() in label_text.lower():
                    # Human-like hover and click
                    await self._human_like_click(radio)
                    print(f"✅ Selected '{level}' for {brand}")
                    return True
            
            # If exact match not found, try partial match
            for radio in radios:
                label_text = await self._get_radio_label_text(radio)
                if any(word in label_text.lower() for word in level.split('_')):
                    await self._human_like_click(radio)
                    print(f"✅ Selected '{label_text}' (closest match) for {brand}")
                    return True
            
            print(f"❌ Could not find level '{level}' for {brand}")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting familiarity level: {e}")
            return False
    
    async def handle_brand_matrix(self, brand_responses: Dict[str, str]) -> bool:
        """
        Handle complete brand matrix with multiple selections
        
        Args:
            brand_responses: Dict of {brand: response_level}
            
        Returns:
            True if at least one selection succeeded
        """
        success_count = 0
        total_brands = len(brand_responses)
        
        print(f"🖱️ Processing {total_brands} brands in matrix...")
        
        # Process brands with human-like pacing
        for i, (brand, response_level) in enumerate(brand_responses.items()):
            # Progress indicator
            print(f"   [{i+1}/{total_brands}] {brand} → {response_level}")
            
            if await self.select_familiarity_level(brand, response_level):
                success_count += 1
            
            # Human-like delay between brands (except last)
            if i < total_brands - 1:
                await self._inter_brand_delay()
        
        success_rate = (success_count / total_brands) * 100
        print(f"🖱️ Matrix completion: {success_count}/{total_brands} ({success_rate:.0f}%)")
        
        return success_count > 0
    
    async def click_next_button(self) -> bool:
        """Click next/continue button after matrix completion"""
        try:
            # Wait for any animations to complete
            await asyncio.sleep(0.5)
            
            # Common next button patterns
            next_selectors = [
                'button:has-text("Next")',
                'button:has-text("Continue")',
                'input[type="submit"][value="Next"]',
                'input[type="submit"][value="Continue"]',
                'button[class*="next"]',
                'button[class*="continue"]',
                'a:has-text("Next")',
                'a:has-text("→")'
            ]
            
            for selector in next_selectors:
                button = await self.page.query_selector(selector)
                if button and await button.is_visible():
                    await self._human_like_click(button)
                    print("✅ Clicked next button")
                    return True
            
            print("❌ Next button not found")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking next: {e}")
            return False
    
    # === Private Helper Methods ===
    
    async def _is_brand_matrix_table(self, table) -> bool:
        """Check if table contains brand matrix"""
        try:
            # Look for multiple rows with radio buttons
            rows = await table.query_selector_all('tr')
            radio_rows = 0
            
            for row in rows:
                radios = await row.query_selector_all('input[type="radio"]')
                if len(radios) >= 3:  # Multiple options per row
                    radio_rows += 1
            
            return radio_rows >= 3  # Multiple brands
            
        except:
            return False
    
    async def _is_brand_matrix_div(self, container) -> bool:
        """Check if div container has brand matrix"""
        try:
            # Look for repeated radio button groups
            radio_groups = await container.query_selector_all('[role="radiogroup"], .radio-group')
            return len(radio_groups) >= 3
            
        except:
            return False
    
    async def _extract_table_matrix(self, table) -> Dict[str, Any]:
        """Extract matrix data from table layout"""
        elements = {
            'brands': [],
            'radio_groups': {},
            'response_options': [],
            'layout_type': 'table'
        }
        
        try:
            # Get header row for response options
            header_row = await table.query_selector('tr:first-child')
            if header_row:
                headers = await header_row.query_selector_all('th, td')
                for header in headers[1:]:  # Skip first column
                    text = await header.text_content()
                    if text:
                        elements['response_options'].append(text.strip())
            
            # Get brand rows
            rows = await table.query_selector_all('tr')
            for row in rows[1:]:  # Skip header
                cells = await row.query_selector_all('td')
                if cells:
                    # First cell is usually brand name
                    brand_text = await cells[0].text_content()
                    if brand_text:
                        brand = brand_text.strip()
                        elements['brands'].append(brand)
                        
                        # Get radio buttons for this brand
                        radios = await row.query_selector_all('input[type="radio"]')
                        elements['radio_groups'][brand] = radios
            
            return elements
            
        except Exception as e:
            print(f"❌ Error extracting table matrix: {e}")
            return elements
    
    async def _extract_div_matrix(self, container) -> Dict[str, Any]:
        """Extract matrix data from div-based layout"""
        elements = {
            'brands': [],
            'radio_groups': {},
            'response_options': [],
            'layout_type': 'div'
        }
        
        try:
            # Find brand containers
            brand_sections = await container.query_selector_all(
                '.brand-row, .matrix-row, [class*="brand"]'
            )
            
            for section in brand_sections:
                # Extract brand name
                brand_label = await section.query_selector('label, .brand-name, strong')
                if brand_label:
                    brand = await brand_label.text_content()
                    if brand:
                        brand = brand.strip()
                        elements['brands'].append(brand)
                        
                        # Get radio buttons
                        radios = await section.query_selector_all('input[type="radio"]')
                        elements['radio_groups'][brand] = radios
            
            return elements
            
        except Exception as e:
            print(f"❌ Error extracting div matrix: {e}")
            return elements
    
    async def _detect_radio_groups(self) -> Dict[str, List]:
        """Detect radio button groups by name attribute"""
        groups = {}
        
        try:
            all_radios = await self.page.query_selector_all('input[type="radio"]')
            
            for radio in all_radios:
                name = await radio.get_attribute('name')
                if name:
                    if name not in groups:
                        groups[name] = []
                    groups[name].append(radio)
            
            return groups
            
        except:
            return {}
    
    async def _find_brand_element(self, brand: str) -> Optional[Any]:
        """Find element containing brand name"""
        # Try exact match first
        selectors = [
            f'text="{brand}"',
            f'*:has-text("{brand}")',
            f'label:has-text("{brand}")',
            f'td:has-text("{brand}")'
        ]
        
        for selector in selectors:
            element = await self.page.query_selector(selector)
            if element:
                return element
        
        # Try case-insensitive match
        all_elements = await self.page.query_selector_all('*')
        for element in all_elements:
            text = await element.text_content()
            if text and brand.lower() in text.lower():
                return element
        
        return None
    
    async def _get_brand_radio_buttons(self, brand_element) -> List[Any]:
        """Get radio buttons associated with a brand"""
        radios = []
        
        try:
            # Try parent container first
            parent = brand_element
            for _ in range(3):  # Check up to 3 levels up
                parent = await parent.query_selector('xpath=..')
                if parent:
                    radios = await parent.query_selector_all('input[type="radio"]')
                    if radios:
                        return radios
            
            # Try sibling elements
            siblings = await brand_element.query_selector_all('xpath=..//*')
            for sibling in siblings:
                radio = await sibling.query_selector('input[type="radio"]')
                if radio:
                    radios.append(radio)
            
        except:
            pass
        
        return radios
    
    async def _get_radio_label_text(self, radio) -> str:
        """Get label text for a radio button"""
        try:
            # Check for label with 'for' attribute
            radio_id = await radio.get_attribute('id')
            if radio_id:
                label = await self.page.query_selector(f'label[for="{radio_id}"]')
                if label:
                    return await label.text_content()
            
            # Check parent label
            parent = await radio.query_selector('xpath=..')
            if parent:
                tag = await parent.evaluate('el => el.tagName')
                if tag.lower() == 'label':
                    return await parent.text_content()
            
            # Check adjacent text
            following = await radio.query_selector('xpath=following-sibling::text()[1]')
            if following:
                return await following.text_content()
            
        except:
            pass
        
        return ""
    
    async def _human_like_click(self, element):
        """Click element with human-like behavior"""
        try:
            # Hover first
            await element.hover()
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Click
            await element.click()
            
        except Exception as e:
            # Fallback to force click
            await element.click(force=True)
    
    async def _thinking_delay(self):
        """Human-like thinking delay"""
        delay = random.uniform(0.5, 1.5) * self.thinking_speed
        await asyncio.sleep(delay)
    
    async def _inter_brand_delay(self):
        """Delay between processing brands"""
        delay = random.uniform(0.3, 0.8) * self.thinking_speed
        await asyncio.sleep(delay)
    
    async def take_screenshot(self, filename: str):
        """Take screenshot for debugging"""
        try:
            await self.page.screenshot(path=f"screenshots/{filename}")
            print(f"📸 Screenshot saved: {filename}")
        except:
            pass