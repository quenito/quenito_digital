# services/carousel_handler.py - NEW FILE

class CarouselBrandHandler:
    """Handles carousel/slider style brand familiarity questions"""
    
    # Standard responses for brand familiarity
    FAMILIARITY_RESPONSES = {
        'very_well': ['I know them very well', 'Very familiar', 'Know very well'],
        'little': ['I know a little about them', 'Somewhat familiar', 'Know a little'],
        'name_only': ['I only know the name', 'Heard of them', 'Name only'],
        'never_heard': ['Never heard of them', "Don't know them", 'Not familiar']
    }
    
    # Top brands get "know a little", others get "name only"
    TOP_TIER_BRANDS = [
        'RACV', 'NRMA', 'AAMI', 'Budget Direct', 'Allianz',
        'Woolworths', 'Coles', 'Telstra', 'Optus', 'CommBank',
        'Origin', 'AGL', 'Energy Australia'
    ]
    
    async def detect_carousel_pattern(self, page) -> bool:
        """Detect if this is a carousel/slider question format"""
        
        # Look for navigation arrows
        arrow_selectors = [
            'button[class*="next"]',
            'button[class*="arrow"]',
            'div[class*="arrow"]',
            'span[class*="arrow"]',
            'i[class*="arrow"]',
            'button[aria-label*="next"]',
            '.carousel-control-next',
            'button:has(svg)',  # Arrow might be an SVG
            '[onclick*="next"]'
        ]
        
        # Check for arrows
        for selector in arrow_selectors:
            arrow = await page.query_selector(selector)
            if arrow:
                # Also check for brand display area
                brand_visible = await self.check_for_single_brand_display(page)
                if brand_visible:
                    print("🎠 Detected carousel/slider pattern!")
                    return True
        
        return False
    
    async def check_for_single_brand_display(self, page) -> bool:
        """Check if only one brand is displayed at a time"""
        
        # Look for single brand display patterns
        patterns = [
            'div[class*="brand-name"]',
            'h2:has-text("RACV")',  # Specific brand headers
            'img[alt]',  # Single brand logo
            'div[class*="current-brand"]'
        ]
        
        for pattern in patterns:
            elements = await page.query_selector_all(pattern)
            # If we find 1-2 brand elements (not a grid), likely carousel
            if 1 <= len(elements) <= 2:
                return True
        
        return False
    
    async def handle_carousel_brands(self, page, max_brands: int = 10):
        """Handle the full carousel of brands"""
        
        print("🎠 Starting carousel brand handling...")
        brands_processed = 0
        
        while brands_processed < max_brands:
            try:
                # Step 1: Identify current brand
                current_brand = await self.get_current_brand(page)
                if not current_brand:
                    print("❓ Could not identify current brand")
                    break
                
                print(f"📍 Processing brand {brands_processed + 1}: {current_brand}")
                
                # Step 2: Determine and select familiarity level
                familiarity = self.determine_familiarity(current_brand)
                selected = await self.select_familiarity_option(page, familiarity)
                
                if not selected:
                    print(f"⚠️ Could not select option for {current_brand}")
                
                # Step 3: Click next arrow to move to next brand
                has_next = await self.click_next_arrow(page)
                
                if not has_next:
                    print("✅ No more brands to process (no next button found)")
                    break
                
                # Step 4: Wait for transition
                await page.wait_for_timeout(500)  # Half second for animation
                
                # Step 5: Check if we've looped back or reached the end
                new_brand = await self.get_current_brand(page)
                if new_brand == current_brand:
                    print("🔄 Detected same brand - might be at the end")
                    # Check for continue button
                    if await self.check_for_continue_button(page):
                        print("✅ Continue button appeared - all brands processed!")
                        break
                
                brands_processed += 1
                
            except Exception as e:
                print(f"Error processing brand {brands_processed + 1}: {e}")
                break
        
        print(f"🎯 Processed {brands_processed} brands total")
        return brands_processed > 0
    
    async def get_current_brand(self, page) -> str:
        """Extract the currently displayed brand name"""
        
        # Try multiple methods to get brand name
        selectors = [
            'h1', 'h2', 'h3',  # Headers often contain brand name
            'div[class*="brand-name"]',
            'div[class*="brand-title"]',
            'span[class*="brand"]',
            'img[alt]',  # Alt text of brand logo
            '.question-brand',
            '[data-brand]'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    # Try to get text
                    text = await element.inner_text()
                    if text and len(text) > 1 and len(text) < 50:
                        # Clean up the text
                        brand = text.strip().replace('\n', ' ')
                        if brand and not any(skip in brand.lower() for skip in 
                                            ['how well', 'select', 'please', 'which']):
                            return brand
                    
                    # Try alt text if it's an image
                    alt = await element.get_attribute('alt')
                    if alt and len(alt) > 1 and len(alt) < 50:
                        return alt.strip()
            except:
                continue
        
        # Fallback: look for any prominent text that might be a brand
        all_text = await page.evaluate('''() => {
            const texts = [];
            document.querySelectorAll('h1, h2, h3, [class*="brand"]').forEach(el => {
                const text = el.innerText?.trim();
                if (text && text.length > 1 && text.length < 50) {
                    texts.push(text);
                }
            });
            return texts;
        }''')
        
        # Return first text that looks like a brand name
        for text in all_text:
            if not any(skip in text.lower() for skip in ['how well', 'select', 'please']):
                return text
        
        return None
    
    def determine_familiarity(self, brand_name: str) -> str:
        """Determine familiarity level based on brand"""
        
        if not brand_name:
            return 'name_only'
        
        # Check if it's a top-tier brand
        for top_brand in self.TOP_TIER_BRANDS:
            if top_brand.lower() in brand_name.lower() or brand_name.lower() in top_brand.lower():
                print(f"  → Top brand detected: selecting 'know a little'")
                return 'little'
        
        # Default for other brands
        print(f"  → Standard brand: selecting 'name only'")
        return 'name_only'
    
    async def select_familiarity_option(self, page, familiarity_level: str):
        """Select the appropriate familiarity option"""
        
        responses = self.FAMILIARITY_RESPONSES[familiarity_level]
        
        # Try to click the appropriate option
        for response_text in responses:
            selectors = [
                f'button:has-text("{response_text}")',
                f'label:has-text("{response_text}")',
                f'div[class*="option"]:has-text("{response_text}")',
                f'input[type="radio"][value*="{response_text.lower()}"]',
                f'span:has-text("{response_text}")'
            ]
            
            for selector in selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=1000)
                    if element:
                        # Check if it's a radio button or clickable element
                        is_input = await element.evaluate('el => el.tagName === "INPUT"')
                        
                        if is_input:
                            # For radio buttons, click the label or the input
                            await element.click()
                        else:
                            # For other elements, just click
                            await element.click()
                        
                        await page.wait_for_timeout(200)
                        print(f"  ✓ Selected: {response_text}")
                        return True
                except:
                    continue
        
        print(f"  ⚠️ Could not select {familiarity_level} option")
        return False
    
    async def click_next_arrow(self, page) -> bool:
        """Click the next/arrow button to move to next brand"""
        
        # Arrow selectors (ordered by likelihood)
        arrow_selectors = [
            'button[class*="next"]:visible',
            'button[class*="arrow"]:visible',
            'div[class*="arrow"]:visible',
            'i[class*="arrow-right"]',
            'i[class*="fa-arrow"]',
            'button[aria-label*="next"]',
            'button:has(svg):visible',
            '.carousel-control-next',
            '[onclick*="next"]',
            '>>',  # Text-based arrow
            '→',   # Unicode arrow
            '❯'    # Another unicode arrow
        ]
        
        for selector in arrow_selectors:
            try:
                # Special handling for text-based selectors
                if selector in ['>>', '→', '❯']:
                    element = await page.query_selector(f'button:has-text("{selector}")')
                else:
                    element = await page.query_selector(selector)
                
                if element:
                    is_visible = await element.is_visible()
                    is_enabled = await element.is_enabled()
                    
                    if is_visible and is_enabled:
                        await element.click()
                        print("  → Clicked next arrow")
                        return True
            except Exception as e:
                continue
        
        print("  ⚠️ No next arrow found or clickable")
        return False
    
    async def check_for_continue_button(self, page) -> bool:
        """Check if the main continue/next button has appeared"""
        
        continue_selectors = [
            'button:has-text("Continue")',
            'button:has-text("Next")',
            'input[type="submit"]',
            'button[type="submit"]',
            'button[class*="continue"]',
            'button[class*="submit"]'
        ]
        
        for selector in continue_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    is_visible = await element.is_visible()
                    if is_visible:
                        return True
            except:
                continue
        
        return False