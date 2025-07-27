#!/usr/bin/env python3
"""
🖱️ Multi Select UI Module v2.0 - Checkbox/Multi-Selection Specialist
Handles all UI interactions for multi-select questions.

This module manages:
- Checkbox detection and state management
- Multiple selection strategies
- Exclusive option handling (None of the above)
- Label extraction and matching
- Human-like selection patterns

ARCHITECTURE: Extends BaseUI with multi-select-specific functionality
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Set
from playwright.async_api import Page, ElementHandle
from handlers.shared.base_ui import BaseUI


class MultiSelectUI(BaseUI):
    """
    🖱️ UI Interaction Handler for Multi-Select Questions
    
    Extends BaseUI with checkbox-specific functionality:
    - Multiple checkbox selection
    - Exclusive option handling
    - State management (checked/unchecked)
    - Label association
    """
    
    def __init__(self, page: Page):
        """Initialize with base UI functionality"""
        super().__init__(page)
        self.last_checkbox_count = 0
        print("🖱️ MultiSelectUI initialized with BaseUI foundation")
    
    # ========================================
    # CHECKBOX DETECTION
    # ========================================
    
    async def detect_all_checkboxes(self) -> List[ElementHandle]:
        """
        Detect all checkbox elements on the page
        Returns list of checkbox elements
        """
        try:
            # Multiple selectors for different checkbox implementations
            selectors = [
                'input[type="checkbox"]',
                '[role="checkbox"]',
                '.checkbox-input',
                '.survey-checkbox'
            ]
            
            all_checkboxes = []
            
            for selector in selectors:
                checkboxes = await self.find_visible_elements(selector)
                all_checkboxes.extend(checkboxes)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_checkboxes = []
            for cb in all_checkboxes:
                if cb not in seen:
                    seen.add(cb)
                    unique_checkboxes.append(cb)
            
            self.last_checkbox_count = len(unique_checkboxes)
            print(f"☑️ Found {self.last_checkbox_count} visible checkboxes")
            
            return unique_checkboxes
            
        except Exception as e:
            print(f"❌ Error detecting checkboxes: {e}")
            return []
    
    async def get_checkbox_label(self, checkbox: ElementHandle) -> str:
        """
        Get the label text associated with a checkbox
        Tries multiple strategies to find the label
        """
        try:
            # Strategy 1: Check for associated label via 'for' attribute
            checkbox_id = await checkbox.get_attribute('id')
            if checkbox_id:
                label = await self.find_first_visible_element(f'label[for="{checkbox_id}"]')
                if label:
                    text = await self.get_element_text(label)
                    if text:
                        return text.strip()
            
            # Strategy 2: Check parent label
            try:
                parent_label = await checkbox.evaluate_handle('''
                    el => el.closest('label')
                ''')
                if parent_label:
                    text = await parent_label.evaluate('el => el.textContent')
                    if text:
                        return text.strip()
            except:
                pass
            
            # Strategy 3: Check next sibling
            try:
                next_text = await checkbox.evaluate('''
                    el => {
                        let next = el.nextSibling;
                        while (next && next.nodeType !== Node.TEXT_NODE) {
                            next = next.nextSibling;
                        }
                        return next ? next.textContent : null;
                    }
                ''')
                if next_text:
                    return next_text.strip()
            except:
                pass
            
            # Strategy 4: Check parent container text
            try:
                parent_text = await checkbox.evaluate('''
                    el => {
                        const parent = el.parentElement;
                        if (parent) {
                            // Clone parent and remove the checkbox to get just the text
                            const clone = parent.cloneNode(true);
                            const checkboxClone = clone.querySelector('input[type="checkbox"]');
                            if (checkboxClone) checkboxClone.remove();
                            return clone.textContent;
                        }
                        return null;
                    }
                ''')
                if parent_text:
                    return parent_text.strip()
            except:
                pass
            
            # Strategy 5: Look for nearby text elements
            try:
                nearby_text = await checkbox.evaluate('''
                    el => {
                        const parent = el.parentElement;
                        if (parent) {
                            const spans = parent.querySelectorAll('span, div, p');
                            for (let span of spans) {
                                if (span.textContent.trim()) {
                                    return span.textContent;
                                }
                            }
                        }
                        return null;
                    }
                ''')
                if nearby_text:
                    return nearby_text.strip()
            except:
                pass
            
            # Strategy 6: Use value attribute as fallback
            value = await checkbox.get_attribute('value')
            if value:
                return value
            
            return "Unknown option"
            
        except Exception as e:
            print(f"⚠️ Error getting checkbox label: {e}")
            return "Error getting label"
    
    # ========================================
    # CHECKBOX INTERACTION
    # ========================================
    
    async def select_checkbox(self, checkbox: ElementHandle) -> bool:
        """
        Select a checkbox if not already selected
        Uses multiple strategies for reliable selection
        """
        try:
            # Check current state
            is_checked = await checkbox.is_checked()
            
            if is_checked:
                print("☑️ Checkbox already selected")
                return True
            
            # Try multiple selection strategies
            strategies = [
                # Strategy 1: Standard click
                ("standard click", lambda: self.safe_click(checkbox)),
                
                # Strategy 2: Force click
                ("force click", lambda: self.safe_click(checkbox, force=True)),
                
                # Strategy 3: Check method
                ("check method", lambda: checkbox.check()),
                
                # Strategy 4: JavaScript click
                ("JS click", lambda: self.page.evaluate('el => el.click()', checkbox)),
                
                # Strategy 5: Dispatch event
                ("dispatch event", lambda: self.page.evaluate('''
                    el => {
                        el.checked = true;
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                ''', checkbox))
            ]
            
            for strategy_name, strategy_func in strategies:
                try:
                    await strategy_func()
                    await asyncio.sleep(0.2)  # Wait for state update
                    
                    # Verify selection
                    is_now_checked = await checkbox.is_checked()
                    if is_now_checked:
                        print(f"✅ Checkbox selected using {strategy_name}")
                        return True
                    
                except Exception as e:
                    print(f"⚠️ {strategy_name} failed: {e}")
                    continue
            
            print("❌ All checkbox selection strategies failed")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting checkbox: {e}")
            return False
    
    async def deselect_checkbox(self, checkbox: ElementHandle) -> bool:
        """Deselect a checkbox if currently selected"""
        try:
            is_checked = await checkbox.is_checked()
            
            if not is_checked:
                print("☐ Checkbox already deselected")
                return True
            
            # Try uncheck method first
            try:
                await checkbox.uncheck()
                await asyncio.sleep(0.2)
                
                if not await checkbox.is_checked():
                    print("✅ Checkbox deselected")
                    return True
            except:
                pass
            
            # Fallback to click
            await self.safe_click(checkbox)
            await asyncio.sleep(0.2)
            
            if not await checkbox.is_checked():
                print("✅ Checkbox deselected via click")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error deselecting checkbox: {e}")
            return False
    
    async def deselect_all_checkboxes(self) -> int:
        """
        Deselect all checkboxes on the page
        Used before selecting exclusive options like 'None of the above'
        """
        try:
            checkboxes = await self.detect_all_checkboxes()
            deselected_count = 0
            
            for checkbox in checkboxes:
                if await checkbox.is_checked():
                    if await self.deselect_checkbox(checkbox):
                        deselected_count += 1
            
            print(f"☐ Deselected {deselected_count} checkboxes")
            return deselected_count
            
        except Exception as e:
            print(f"❌ Error deselecting all checkboxes: {e}")
            return 0
    
    # ========================================
    # SELECTION PATTERNS
    # ========================================
    
    async def select_multiple_checkboxes(self, selections: List[str]) -> Dict[str, bool]:
        """
        Select multiple checkboxes based on label text
        Returns dict of selection_text -> success
        """
        results = {}
        
        try:
            checkboxes = await self.detect_all_checkboxes()
            
            for selection in selections:
                found = False
                selection_lower = selection.lower().strip()
                
                for checkbox in checkboxes:
                    label = await self.get_checkbox_label(checkbox)
                    label_lower = label.lower().strip()
                    
                    # Check for match
                    if (selection_lower == label_lower or
                        selection_lower in label_lower or
                        label_lower in selection_lower):
                        
                        success = await self.select_checkbox(checkbox)
                        results[selection] = success
                        found = True
                        break
                
                if not found:
                    results[selection] = False
                    print(f"⚠️ Could not find checkbox for: {selection}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error selecting multiple checkboxes: {e}")
            return {sel: False for sel in selections}
    
    async def handle_exclusive_option(self, exclusive_text: str) -> bool:
        """
        Handle exclusive options like 'None of the above'
        Deselects all others before selecting the exclusive option
        """
        try:
            # First, deselect all checkboxes
            await self.deselect_all_checkboxes()
            
            # Find and select the exclusive option
            checkboxes = await self.detect_all_checkboxes()
            exclusive_lower = exclusive_text.lower().strip()
            
            for checkbox in checkboxes:
                label = await self.get_checkbox_label(checkbox)
                
                if exclusive_lower in label.lower():
                    success = await self.select_checkbox(checkbox)
                    if success:
                        print(f"✅ Selected exclusive option: {label}")
                    return success
            
            print(f"⚠️ Could not find exclusive option: {exclusive_text}")
            return False
            
        except Exception as e:
            print(f"❌ Error handling exclusive option: {e}")
            return False
    
    # ========================================
    # STATE MANAGEMENT
    # ========================================
    
    async def get_checkbox_states(self) -> List[Dict[str, Any]]:
        """
        Get current state of all checkboxes
        Returns list of dicts with checkbox info
        """
        try:
            checkboxes = await self.detect_all_checkboxes()
            states = []
            
            for checkbox in checkboxes:
                state = {
                    'element': checkbox,
                    'label': await self.get_checkbox_label(checkbox),
                    'checked': await checkbox.is_checked(),
                    'enabled': await checkbox.is_enabled()
                }
                states.append(state)
            
            return states
            
        except Exception as e:
            print(f"❌ Error getting checkbox states: {e}")
            return []
    
    async def count_selected_checkboxes(self) -> int:
        """Count how many checkboxes are currently selected"""
        try:
            states = await self.get_checkbox_states()
            return sum(1 for state in states if state['checked'])
            
        except Exception:
            return 0
    
    # ========================================
    # NAVIGATION
    # ========================================
    
    async def try_navigation(self) -> bool:
        """Navigate to next page after completing multi-select"""
        # Add multi-select-specific navigation selectors
        custom_selectors = [
            ".multi-select-next", ".checkbox-submit", 
            "button[type='submit']", ".continue-button"
        ]
        
        return await self.click_navigation_button(custom_selectors=custom_selectors)
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    async def validate_minimum_selections(self, min_required: int = 1) -> bool:
        """
        Validate that minimum number of selections have been made
        Some surveys require at least X selections
        """
        try:
            selected_count = await self.count_selected_checkboxes()
            
            if selected_count >= min_required:
                print(f"✅ Validation passed: {selected_count} selections (min: {min_required})")
                return True
            else:
                print(f"⚠️ Validation failed: {selected_count} selections (min: {min_required})")
                return False
                
        except Exception:
            return False
    
    async def find_checkbox_by_partial_text(self, partial_text: str) -> Optional[ElementHandle]:
        """Find a checkbox by partial label text match"""
        try:
            checkboxes = await self.detect_all_checkboxes()
            partial_lower = partial_text.lower().strip()
            
            for checkbox in checkboxes:
                label = await self.get_checkbox_label(checkbox)
                if partial_lower in label.lower():
                    return checkbox
            
            return None
            
        except Exception:
            return None
    
    async def get_checkbox_group_name(self, checkbox: ElementHandle) -> Optional[str]:
        """
        Get the group name for a checkbox (useful for grouped questions)
        """
        try:
            # Check name attribute (often used for grouping)
            name = await checkbox.get_attribute('name')
            if name:
                return name
            
            # Check data attributes
            data_group = await checkbox.get_attribute('data-group')
            if data_group:
                return data_group
            
            # Check parent fieldset
            fieldset_name = await checkbox.evaluate('''
                el => {
                    const fieldset = el.closest('fieldset');
                    if (fieldset) {
                        const legend = fieldset.querySelector('legend');
                        return legend ? legend.textContent : null;
                    }
                    return null;
                }
            ''')
            
            return fieldset_name
            
        except Exception:
            return None