# services/brand_selection_handler.py - NEW FILE

import asyncio
from typing import List, Dict, Any

class BrandSelectionHandler:
    """Handles both checkbox and clickable image brand selections"""
    
    # Extended brand database for Australian market
    BRAND_DATABASE = {
        'insurance_comparison': [
            'iSelect', 'Compare the Market', 'Canstar', 'CHOICE', 
            'Finder', 'Compareclub', 'Health.com.au', 'Choosi'
        ],
        'health_insurance': [
            'Medibank', 'Bupa', 'HCF', 'NIB', 'HBF', 
            'Australian Unity', 'GMHBA', 'AHM', 'Frank Health'
        ],
        'energy': [
            'Origin', 'Origin Energy', 'AGL', 'Energy Australia', 
            'Simply Energy', 'Red Energy', 'Alinta Energy', 'Dodo Power',
            'Powershop', 'Momentum Energy', 'Click Energy', 'Ausgrid',
            'Jemena', 'Solgen', 'Arise Solar', 'Sunpower', 'Zinfra',
            'Ovida', 'Renewable Gas'
        ],
        'general_insurance': [
            'AAMI', 'GIO', 'NRMA', 'RACV', 'RACQ', 'Budget Direct',
            'Youi', 'Woolworths Insurance', 'Coles Insurance', 'Allianz'
        ]
    }
    
    async def detect_and_handle_brand_selection(self, page, question_text: str):
        """Main entry point - detects type and handles accordingly"""
        
        print(f"🔍 Analyzing brand selection question: {question_text[:50]}...")
        
        # Detect selection type
        selection_type = await self.detect_selection_type(page)
        
        # Get brands to select
        brands_to_select = await self.determine_brands_to_select(page, question_text)
        
        print(f"📋 Selection type: {selection_type}")
        print(f"🎯 Will select: {brands_to_select[:5]}")  # Show first 5
        
        # Handle based on type
        if selection_type == 'checkbox_overlay':
            return await self.handle_checkbox_overlay(page, brands_to_select)
        elif selection_type == 'clickable_image':
            return await self.handle_clickable_image(page, brands_to_select)
        else:
            return await self.handle_hybrid_approach(page, brands_to_select)
    
    async def detect_selection_type(self, page) -> str:
        """Detect if we have checkbox overlays or clickable images"""
        
        # Check for visible checkboxes
        checkboxes = await page.query_selector_all('input[type="checkbox"]:visible')
        
        # Check for clickable image containers
        clickable_indicators = [
            'div[onclick]',
            'div[class*="clickable"]',
            'div[class*="selectable"]',
            'label:has(img)',
            'div[class*="option"]:has(img)'
        ]
        
        clickable_count = 0
        for selector in clickable_indicators:
            elements = await page.query_selector_all(selector)
            clickable_count += len(elements)
        
        # Determine type
        if len(checkboxes) > 3:
            # Check if checkboxes are near images
            first_checkbox = checkboxes[0]
            parent = await first_checkbox.evaluate_handle('el => el.parentElement')
            has_image = await parent.evaluate('el => el.querySelector("img") !== null')
            
            if has_image:
                return 'checkbox_overlay'
            else:
                return 'standard_checkbox'
        elif clickable_count > 3:
            return 'clickable_image'
        else:
            return 'hybrid'
    
    async def determine_brands_to_select(self, page, question_text: str) -> List[str]:
        """Determine which brands to select based on context"""
        
        # Extract visible brands from page
        visible_brands = await self.extract_visible_brands(page)
        
        # Determine category
        category = self.detect_category(question_text, visible_brands)
        
        # Get known brands for this category
        known_brands = self.BRAND_DATABASE.get(category, [])
        
        # Select top 3-5 brands that are visible
        brands_to_select = []
        
        # First pass: exact matches
        for known in known_brands:
            for visible in visible_brands:
                if known.lower() == visible.lower():
                    brands_to_select.append(visible)
                    if len(brands_to_select) >= 5:
                        break
            if len(brands_to_select) >= 5:
                break
        
        # Second pass: partial matches
        if len(brands_to_select) < 3:
            for known in known_brands:
                for visible in visible_brands:
                    if (known.lower() in visible.lower() or 
                        visible.lower() in known.lower()) and \
                       visible not in brands_to_select:
                        brands_to_select.append(visible)
                        if len(brands_to_select) >= 5:
                            break
                if len(brands_to_select) >= 5:
                    break
        
        # Fallback: select first few if we don't have enough
        if len(brands_to_select) < 3:
            for visible in visible_brands:
                if visible not in brands_to_select:
                    brands_to_select.append(visible)
                    if len(brands_to_select) >= 3:
                        break
        
        return brands_to_select
    
    async def handle_checkbox_overlay(self, page, brands_to_select: List[str]):
        """Handle checkboxes overlaid on brand images"""
        
        print("📦 Handling checkbox overlay selection...")
        success_count = 0
        
        # Strategy 1: Find checkbox by adjacent text/image
        for brand in brands_to_select:
            selectors = [
                f'input[type="checkbox"][value*="{brand}"]',
                f'input[type="checkbox"][id*="{brand.replace(" ", "")}"]',
                f'label:has-text("{brand}") input[type="checkbox"]',
                f'div:has-text("{brand}") input[type="checkbox"]',
                # For image-based selections
                f'img[alt*="{brand}"] ~ input[type="checkbox"]',
                f'img[alt*="{brand}"] + input[type="checkbox"]',
                f'div:has(img[alt*="{brand}"]) input[type="checkbox"]'
            ]
            
            for selector in selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=1000)
                    if element:
                        is_checked = await element.is_checked()
                        if not is_checked:
                            await element.click()
                            await page.wait_for_timeout(300)
                            success_count += 1
                            print(f"✅ Selected {brand} via checkbox")
                        break
                except:
                    continue
        
        # Strategy 2: Find by position if text matching fails
        if success_count < len(brands_to_select):
            containers = await page.query_selector_all('div[class*="option"], div[class*="brand"], label')
            
            for container in containers:
                try:
                    # Check for brand text or image alt
                    text_content = await container.evaluate('''el => {
                        const text = el.innerText || '';
                        const img = el.querySelector('img');
                        const alt = img ? img.alt : '';
                        return text + ' ' + alt;
                    }''')
                    
                    for brand in brands_to_select:
                        if brand.lower() in text_content.lower():
                            # Find checkbox within container
                            checkbox = await container.query_selector('input[type="checkbox"]')
                            if checkbox:
                                is_checked = await checkbox.is_checked()
                                if not is_checked:
                                    await checkbox.click()
                                    await page.wait_for_timeout(300)
                                    success_count += 1
                                    print(f"✅ Selected {brand} via container")
                            break
                except:
                    continue
        
        return success_count
    
    async def handle_clickable_image(self, page, brands_to_select: List[str]):
        """Handle clickable image selections (like insurance comparison sites)"""
        
        print("🖱️ Handling clickable image selection...")
        success_count = 0
        
        # Find all clickable brand containers
        selectors = [
            'div[class*="brand"][onclick]',
            'div[class*="option"]:has(img)',
            'label:has(img)',
            'div[class*="select"]:has(img)',
            'td:has(img)'  # For table-based layouts
        ]
        
        for brand in brands_to_select:
            for selector in selectors:
                try:
                    # Find container with this brand
                    containers = await page.query_selector_all(selector)
                    
                    for container in containers:
                        text_content = await container.evaluate('''el => {
                            const text = el.innerText || '';
                            const img = el.querySelector('img');
                            const alt = img ? img.alt : '';
                            return text + ' ' + alt;
                        }''')
                        
                        if brand.lower() in text_content.lower():
                            # Check if already selected
                            is_selected = await container.evaluate('''el => {
                                const checkbox = el.querySelector('input[type="checkbox"]');
                                if (checkbox) return checkbox.checked;
                                
                                // Check for selected class
                                return el.classList.contains('selected') || 
                                       el.classList.contains('active') ||
                                       el.classList.contains('checked');
                            }''')
                            
                            if not is_selected:
                                # Click the container or image
                                await container.click()
                                await page.wait_for_timeout(300)
                                success_count += 1
                                print(f"✅ Selected {brand} via image click")
                            break
                except Exception as e:
                    print(f"Error clicking {brand}: {e}")
                    continue
        
        return success_count
    
    async def handle_hybrid_approach(self, page, brands_to_select: List[str]):
        """Try both methods when unsure"""
        
        print("🔄 Using hybrid approach...")
        
        # Try checkbox first
        checkbox_success = await self.handle_checkbox_overlay(page, brands_to_select)
        
        # If that didn't work well, try clickable
        if checkbox_success < len(brands_to_select) / 2:
            clickable_success = await self.handle_clickable_image(page, brands_to_select)
            return max(checkbox_success, clickable_success)
        
        return checkbox_success
    
    async def extract_visible_brands(self, page) -> List[str]:
        """Extract all visible brand names from the page"""
        
        brands = []
        
        # JavaScript to extract all potential brand names
        extracted = await page.evaluate('''() => {
            const brands = new Set();
            
            // Get text from labels
            document.querySelectorAll('label').forEach(el => {
                const text = el.innerText?.trim();
                if (text && text.length > 1 && text.length < 50) {
                    brands.add(text);
                }
            });
            
            // Get alt text from images
            document.querySelectorAll('img[alt]').forEach(el => {
                const alt = el.alt?.trim();
                if (alt && alt.length > 1 && alt.length < 50) {
                    brands.add(alt);
                }
            });
            
            // Get text from brand containers
            const selectors = [
                '[class*="brand-name"]',
                '[class*="option-text"]',
                '[class*="company"]',
                '[class*="provider"]'
            ];
            
            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => {
                    const text = el.innerText?.trim();
                    if (text && text.length > 1 && text.length < 50) {
                        brands.add(text);
                    }
                });
            });
            
            return Array.from(brands);
        }''')
        
        print(f"👁️ Extracted {len(extracted)} potential brands")
        return extracted
    
    def detect_category(self, question_text: str, visible_brands: List[str]) -> str:
        """Detect the category based on question and visible brands"""
        
        q_lower = question_text.lower()
        brands_lower = ' '.join(visible_brands).lower()
        
        if 'comparison' in q_lower and ('insurance' in q_lower or 'health' in q_lower):
            return 'insurance_comparison'
        elif 'health insurance' in q_lower or 'health cover' in q_lower:
            return 'health_insurance'
        elif 'energy' in q_lower or 'electricity' in q_lower or 'gas' in q_lower:
            return 'energy'
        elif 'insurance' in q_lower:
            return 'general_insurance'
        
        # Check visible brands
        if any(brand in brands_lower for brand in ['iselect', 'canstar', 'finder']):
            return 'insurance_comparison'
        elif any(brand in brands_lower for brand in ['origin', 'agl', 'energy australia']):
            return 'energy'
        
        return 'general'  # Fallback