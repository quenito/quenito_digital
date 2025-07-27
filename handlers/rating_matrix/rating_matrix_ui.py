#!/usr/bin/env python3
"""
🖱️ Rating Matrix UI Module v2.0 - Grid/Matrix Interaction Specialist
Handles all UI interactions for rating matrices and grids.

This module manages:
- Matrix/grid detection and structure analysis
- Cell navigation and clicking
- Scale selection (1-5, 1-10, etc.)
- Brand row identification
- Multi-column rating automation

ARCHITECTURE: Extends BaseUI with matrix-specific functionality
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple
from playwright.async_api import Page, ElementHandle
from handlers.shared.base_ui import BaseUI


class RatingMatrixUI(BaseUI):
    """
    🖱️ UI Interaction Handler for Rating Matrices
    
    Extends BaseUI with matrix-specific functionality:
    - Grid structure detection
    - Cell-by-cell navigation
    - Scale clicking strategies
    - Row/column identification
    """
    
    def __init__(self, page: Page):
        """Initialize with base UI functionality"""
        super().__init__(page)
        self.last_matrix_info = None
        print("🖱️ RatingMatrixUI initialized with BaseUI foundation")
    
    # ========================================
    # MATRIX STRUCTURE DETECTION
    # ========================================
    
    async def detect_matrix_structure(self) -> Optional[Dict[str, Any]]:
        """
        Detect and analyze matrix/grid structure on the page
        Returns matrix info with rows, columns, and element references
        """
        try:
            matrix_info = {
                'type': None,
                'rows': 0,
                'cols': 0,
                'container': None,
                'row_elements': [],
                'scale_type': None,
                'clickable_elements': []
            }
            
            # Method 1: Look for HTML table
            tables = await self.find_visible_elements('table')
            if tables:
                table = tables[0]
                matrix_info['type'] = 'table'
                matrix_info['container'] = table
                
                # Count rows and columns
                rows = await table.query_selector_all('tr')
                matrix_info['rows'] = len(rows)
                
                if rows:
                    # Check first data row for columns
                    first_row = rows[1] if len(rows) > 1 else rows[0]
                    cols = await first_row.query_selector_all('td, th')
                    matrix_info['cols'] = len(cols)
                
                matrix_info['row_elements'] = rows
                print(f"📊 Found table matrix: {matrix_info['rows']}x{matrix_info['cols']}")
                
            # Method 2: Look for grid/matrix divs
            else:
                grid_selectors = [
                    '.matrix-container', '.rating-grid', '.survey-matrix',
                    '[role="grid"]', '.question-matrix', '.brand-matrix'
                ]
                
                for selector in grid_selectors:
                    grids = await self.find_visible_elements(selector)
                    if grids:
                        grid = grids[0]
                        matrix_info['type'] = 'div_grid'
                        matrix_info['container'] = grid
                        
                        # Find rows
                        row_selectors = ['.matrix-row', '.grid-row', '[role="row"]', '.brand-row']
                        for row_sel in row_selectors:
                            rows = await grid.query_selector_all(row_sel)
                            if rows:
                                matrix_info['row_elements'] = rows
                                matrix_info['rows'] = len(rows)
                                break
                        
                        print(f"📊 Found div grid matrix with {matrix_info['rows']} rows")
                        break
            
            # Detect scale type
            matrix_info['scale_type'] = await self._detect_scale_type()
            
            # Find clickable elements (radio buttons, scale buttons, etc.)
            if matrix_info['container']:
                clickables = await matrix_info['container'].query_selector_all(
                    'input[type="radio"], button.scale-button, .rating-option, .clickable-cell'
                )
                matrix_info['clickable_elements'] = clickables
            
            self.last_matrix_info = matrix_info
            return matrix_info if matrix_info['rows'] > 0 else None
            
        except Exception as e:
            print(f"❌ Error detecting matrix structure: {e}")
            return None
    
    async def _detect_scale_type(self) -> str:
        """Detect the rating scale type (1-5, 1-10, etc.)"""
        try:
            page_text = await self.get_page_text()
            page_lower = page_text.lower()
            
            # Check for scale indicators
            if '1-10' in page_lower or '1 to 10' in page_lower:
                return '1-10'
            elif '1-7' in page_lower or '1 to 7' in page_lower:
                return '1-7'
            elif '1-5' in page_lower or '1 to 5' in page_lower:
                return '1-5'
            elif 'strongly' in page_lower and 'agree' in page_lower:
                return 'likert'
            else:
                # Check for numbered options
                numbers_found = []
                for i in range(1, 11):
                    if str(i) in page_text:
                        numbers_found.append(i)
                
                if numbers_found:
                    return f'1-{max(numbers_found)}'
                
                return '1-5'  # Default
                
        except Exception:
            return '1-5'
    
    # ========================================
    # BRAND FAMILIARITY RATING
    # ========================================
    
    async def rate_brand_familiarity(self, brand_row_index: int, rating: int, 
                                    matrix_info: Dict[str, Any]) -> bool:
        """
        Rate a single brand's familiarity in the matrix
        
        Args:
            brand_row_index: Row index of the brand (0-based)
            rating: Familiarity rating to select (1-5, 1-10, etc.)
            matrix_info: Matrix structure information
        """
        try:
            print(f"🎯 Rating row {brand_row_index + 1} with familiarity: {rating}")
            
            # Get the specific row
            if brand_row_index >= len(matrix_info['row_elements']):
                print(f"❌ Row index {brand_row_index} out of range")
                return False
            
            row = matrix_info['row_elements'][brand_row_index]
            
            # Find rating options in this row
            success = await self._click_rating_in_row(row, rating, matrix_info['scale_type'])
            
            if success:
                print(f"✅ Successfully rated row {brand_row_index + 1}")
                # Small delay for realism
                await asyncio.sleep(0.3)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error rating brand familiarity: {e}")
            return False
    
    async def _click_rating_in_row(self, row: ElementHandle, rating: int, scale_type: str) -> bool:
        """Click the appropriate rating option in a matrix row"""
        try:
            # Method 1: Radio buttons
            radios = await row.query_selector_all('input[type="radio"]')
            if radios:
                # Determine which radio to click based on rating and scale
                if scale_type == '1-5' and 1 <= rating <= 5:
                    index = rating - 1
                elif scale_type == '1-10' and 1 <= rating <= 10:
                    index = rating - 1
                else:
                    # Try to match by value or label
                    for i, radio in enumerate(radios):
                        value = await radio.get_attribute('value')
                        if value and str(rating) in value:
                            index = i
                            break
                    else:
                        index = min(rating - 1, len(radios) - 1)
                
                if 0 <= index < len(radios):
                    await self.safe_click(radios[index], force=True)
                    return True
            
            # Method 2: Clickable cells/buttons
            cells = await row.query_selector_all('td')
            if cells and len(cells) > 1:  # Skip first cell (usually brand name)
                # Find the cell corresponding to the rating
                rating_cell_index = rating  # Assuming first cell is brand name
                if rating_cell_index < len(cells):
                    cell = cells[rating_cell_index]
                    
                    # Try to click any clickable element in the cell
                    clickable = await cell.query_selector(
                        'input, button, .clickable, [role="radio"], [role="button"]'
                    )
                    if clickable:
                        await self.safe_click(clickable, force=True)
                        return True
                    else:
                        # Click the cell itself
                        await self.safe_click(cell, force=True)
                        return True
            
            # Method 3: Scale buttons
            buttons = await row.query_selector_all('button, .scale-button, .rating-button')
            for button in buttons:
                button_text = await self.get_element_text(button)
                if str(rating) in button_text:
                    await self.safe_click(button, force=True)
                    return True
            
            print(f"⚠️ Could not find rating option {rating} in row")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking rating in row: {e}")
            return False
    
    # ========================================
    # SATISFACTION MATRIX RATING
    # ========================================
    
    async def rate_satisfaction_cell(self, brand_row_index: int, attribute_col_index: int,
                                   rating: int, matrix_info: Dict[str, Any]) -> bool:
        """
        Rate a specific cell in a satisfaction matrix (brand x attribute)
        
        Args:
            brand_row_index: Row index of the brand
            attribute_col_index: Column index of the attribute
            rating: Satisfaction rating to select
            matrix_info: Matrix structure information
        """
        try:
            print(f"🎯 Rating cell [{brand_row_index + 1}, {attribute_col_index + 1}] = {rating}")
            
            # Get the specific row
            if brand_row_index >= len(matrix_info['row_elements']):
                return False
            
            row = matrix_info['row_elements'][brand_row_index]
            
            # Get cells in this row
            cells = await row.query_selector_all('td')
            
            # Calculate actual cell index (accounting for brand name column)
            cell_index = attribute_col_index + 1  # +1 to skip brand name column
            
            if cell_index < len(cells):
                cell = cells[cell_index]
                
                # Find and click rating option in this cell
                success = await self._click_rating_in_cell(cell, rating)
                
                if success:
                    print(f"✅ Successfully rated cell [{brand_row_index + 1}, {attribute_col_index + 1}]")
                    await asyncio.sleep(0.2)  # Small delay
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error rating satisfaction cell: {e}")
            return False
    
    async def _click_rating_in_cell(self, cell: ElementHandle, rating: int) -> bool:
        """Click rating option within a specific cell"""
        try:
            # Look for radio buttons in cell
            radios = await cell.query_selector_all('input[type="radio"]')
            if radios:
                # Find radio with matching value
                for radio in radios:
                    value = await radio.get_attribute('value')
                    if value and str(rating) == value:
                        await self.safe_click(radio, force=True)
                        return True
            
            # Look for dropdown in cell
            select = await cell.query_selector('select')
            if select:
                await select.select_option(value=str(rating))
                return True
            
            # Look for clickable rating elements
            rating_elements = await cell.query_selector_all(
                f'[data-rating="{rating}"], [data-value="{rating}"], .rating-{rating}'
            )
            if rating_elements:
                await self.safe_click(rating_elements[0], force=True)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error clicking rating in cell: {e}")
            return False
    
    # ========================================
    # NAVIGATION
    # ========================================
    
    async def try_navigation(self) -> bool:
        """Navigate to next page after completing matrix"""
        # Add matrix-specific navigation selectors
        custom_selectors = [
            ".matrix-next", ".grid-submit", "[data-action='next']",
            "button[type='submit']", ".continue-after-matrix"
        ]
        
        return await self.click_navigation_button(custom_selectors=custom_selectors)
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    async def get_brand_from_row(self, row: ElementHandle) -> str:
        """Extract brand name from a matrix row"""
        try:
            # Usually the first cell contains the brand name
            cells = await row.query_selector_all('td, th')
            if cells:
                brand_text = await self.get_element_text(cells[0])
                return brand_text.strip()
            
            # Try other methods
            brand_element = await row.query_selector('.brand-name, .item-name, strong')
            if brand_element:
                return await self.get_element_text(brand_element)
            
            # Get all text and take first part
            row_text = await self.get_element_text(row)
            if row_text:
                # Take first word/phrase before any numbers
                parts = row_text.split()
                brand_parts = []
                for part in parts:
                    if part.isdigit():
                        break
                    brand_parts.append(part)
                return ' '.join(brand_parts)
            
            return "Unknown"
            
        except Exception:
            return "Unknown"
    
    async def get_scale_labels(self) -> List[str]:
        """Get the scale labels (e.g., 'Not at all familiar', 'Very familiar')"""
        try:
            labels = []
            
            # Look for scale headers
            scale_headers = await self.find_visible_elements('.scale-label, .rating-label, th.scale')
            for header in scale_headers:
                label = await self.get_element_text(header)
                if label:
                    labels.append(label)
            
            # Look for legend
            legends = await self.find_visible_elements('legend, .scale-legend')
            for legend in legends:
                text = await self.get_element_text(legend)
                if text and '=' in text:  # e.g., "1 = Not familiar"
                    parts = text.split(',')
                    for part in parts:
                        if '=' in part:
                            label = part.split('=')[1].strip()
                            labels.append(label)
            
            return labels
            
        except Exception:
            return []
    
    async def highlight_current_cell(self, row_index: int, col_index: int) -> None:
        """Visually highlight the current cell being processed (for debugging)"""
        try:
            if self.last_matrix_info and self.last_matrix_info['row_elements']:
                row = self.last_matrix_info['row_elements'][row_index]
                cells = await row.query_selector_all('td')
                if col_index < len(cells):
                    cell = cells[col_index]
                    # Add temporary highlight
                    await self.page.evaluate(
                        '''(element) => {
                            element.style.border = "3px solid red";
                            setTimeout(() => {
                                element.style.border = "";
                            }, 1000);
                        }''',
                        cell
                    )
        except Exception:
            pass  # Non-critical, just for visual feedback