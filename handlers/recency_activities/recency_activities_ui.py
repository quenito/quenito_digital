#!/usr/bin/env python3
"""
⏰ Recency Activities UI Module
Handles all UI interactions for activity selection
"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio
import random

class RecencyActivitiesUI:
    """UI interaction methods for recency activities questions"""
    
    def __init__(self, page):
        """Initialize with page object"""
        self.page = page
        print("🖥️ Recency Activities UI module initialized")
    
    async def detect_ui_elements(self) -> Dict[str, Any]:
        """Detect available UI elements for activity selection"""
        elements = {
            'checkboxes': [],
            'multi_select': None,
            'dropdown': None,
            'buttons': [],
            'submit': None
        }
        
        try:
            # Check for checkboxes (most common for multi-select activities)
            checkboxes = await self.page.query_selector_all('input[type="checkbox"]')
            if checkboxes:
                elements['checkboxes'] = checkboxes
                print(f"☑️ Found {len(checkboxes)} checkboxes")
            
            # Check for multi-select dropdown
            multi_select = await self.page.query_selector('select[multiple]')
            if multi_select:
                elements['multi_select'] = multi_select
                print("📋 Found multi-select dropdown")
            
            # Check for regular dropdown (less common for activities)
            dropdown = await self.page.query_selector('select:not([multiple])')
            if dropdown:
                elements['dropdown'] = dropdown
                print("📑 Found single-select dropdown")
            
            # Check for clickable buttons/divs
            buttons = await self.page.query_selector_all('button:not([type="submit"]), div[role="button"]')
            if buttons:
                elements['buttons'] = buttons
                print(f"🔘 Found {len(buttons)} clickable buttons")
            
            # Find submit button
            submit = await self.page.query_selector('button[type="submit"], input[type="submit"], button:has-text("Next"), button:has-text("Continue")')
            if submit:
                elements['submit'] = submit
                print("✅ Found submit button")
            
        except Exception as e:
            print(f"❌ Error detecting UI elements: {e}")
        
        return elements
    
    async def get_available_activities(self, elements: Dict[str, Any]) -> List[Tuple[Any, str]]:
        """Extract available activities from UI elements"""
        activities = []
        
        try:
            # Extract from checkboxes
            if elements['checkboxes']:
                for checkbox in elements['checkboxes']:
                    # Get label text
                    label_text = await self._get_checkbox_label(checkbox)
                    if label_text and label_text.strip():
                        activities.append((checkbox, label_text.strip()))
            
            # Extract from multi-select
            elif elements['multi_select']:
                options = await elements['multi_select'].query_selector_all('option')
                for option in options:
                    text = await option.inner_text()
                    if text and text.strip():
                        activities.append((option, text.strip()))
            
            # Extract from buttons
            elif elements['buttons']:
                for button in elements['buttons']:
                    text = await button.inner_text()
                    if text and text.strip():
                        activities.append((button, text.strip()))
            
            print(f"📊 Found {len(activities)} available activities")
            
        except Exception as e:
            print(f"❌ Error extracting activities: {e}")
        
        return activities
    
    async def _get_checkbox_label(self, checkbox) -> Optional[str]:
        """Get label text for a checkbox"""
        try:
            # Try parent label
            parent = await checkbox.evaluate_handle('el => el.parentElement')
            tag_name = await parent.evaluate('el => el.tagName')
            
            if tag_name == 'LABEL':
                return await parent.inner_text()
            
            # Try associated label
            checkbox_id = await checkbox.get_attribute('id')
            if checkbox_id:
                label = await self.page.query_selector(f'label[for="{checkbox_id}"]')
                if label:
                    return await label.inner_text()
            
            # Try next sibling
            next_sibling = await checkbox.evaluate_handle('el => el.nextSibling')
            if next_sibling:
                text = await next_sibling.evaluate('el => el.textContent')
                if text and text.strip():
                    return text.strip()
            
            # Try parent's text content
            parent_text = await parent.inner_text()
            if parent_text and parent_text.strip():
                return parent_text.strip()
            
        except Exception as e:
            print(f"⚠️ Error getting checkbox label: {e}")
        
        return None
    
    async def select_activities(self, activities_to_select: List[str], available_activities: List[Tuple[Any, str]], elements: Dict[str, Any]) -> bool:
        """Select the specified activities in the UI"""
        try:
            selected_count = 0
            
            # Match and select activities
            for activity in activities_to_select:
                activity_lower = activity.lower()
                
                for element, text in available_activities:
                    if activity_lower in text.lower() or text.lower() in activity_lower:
                        # Select based on element type
                        if elements['checkboxes'] and element in elements['checkboxes']:
                            await self._select_checkbox(element)
                            selected_count += 1
                            print(f"☑️ Selected: {text}")
                            break
                        
                        elif elements['multi_select'] and element.tag_name == 'option':
                            await element.click()
                            selected_count += 1
                            print(f"📋 Selected: {text}")
                            break
                        
                        elif elements['buttons'] and element in elements['buttons']:
                            await element.click()
                            selected_count += 1
                            print(f"🔘 Clicked: {text}")
                            await asyncio.sleep(0.3)  # Brief pause between button clicks
                            break
            
            print(f"✅ Selected {selected_count}/{len(activities_to_select)} activities")
            
            # Submit if button available
            if elements['submit'] and selected_count > 0:
                await asyncio.sleep(0.5)  # Brief pause before submit
                await elements['submit'].click()
                print("📤 Submitted activity selection")
                return True
            
            return selected_count > 0
            
        except Exception as e:
            print(f"❌ Error selecting activities: {e}")
            return False
    
    async def _select_checkbox(self, checkbox) -> None:
        """Select a checkbox if not already selected"""
        try:
            is_checked = await checkbox.is_checked()
            if not is_checked:
                await checkbox.click()
                await asyncio.sleep(0.1)  # Brief pause
        except Exception as e:
            print(f"⚠️ Error selecting checkbox: {e}")
    
    async def handle_none_option(self, available_activities: List[Tuple[Any, str]], elements: Dict[str, Any]) -> bool:
        """Handle 'None of the above' option if no activities to select"""
        try:
            none_options = ['none of the above', 'none', 'n/a', 'not applicable']
            
            for element, text in available_activities:
                if any(opt in text.lower() for opt in none_options):
                    # Select based on element type
                    if elements['checkboxes'] and element in elements['checkboxes']:
                        await self._select_checkbox(element)
                        print(f"☑️ Selected: {text}")
                    
                    elif elements['buttons'] and element in elements['buttons']:
                        await element.click()
                        print(f"🔘 Clicked: {text}")
                    
                    # Submit
                    if elements['submit']:
                        await asyncio.sleep(0.5)
                        await elements['submit'].click()
                        print("📤 Submitted 'None' selection")
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling none option: {e}")
            return False
    
    async def get_question_text(self) -> str:
        """Extract the question text from the page"""
        try:
            # Common question selectors
            selectors = [
                'h1', 'h2', 'h3', 'h4',
                '.question-text', '.question',
                'div[role="heading"]',
                'label:has(input[type="checkbox"])'
            ]
            
            for selector in selectors:
                element = await self.page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and len(text) > 20 and 'activities' in text.lower():
                        return text.strip()
            
            # Fallback: get all text and find question
            all_text = await self.page.inner_text('body')
            lines = all_text.split('\n')
            
            for line in lines:
                if len(line) > 20 and any(keyword in line.lower() for keyword in ['last 12 months', 'past year', 'activities']):
                    return line.strip()
            
            return ""
            
        except Exception as e:
            print(f"❌ Error getting question text: {e}")
            return ""