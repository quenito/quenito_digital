# services/brand_association_handler.py - NEW FILE

class BrandAssociationHandler:
    """Handles free text brand association questions"""
    
    # Realistic, human-like associations for different brands
    BRAND_ASSOCIATIONS = {
        # Insurance comparison sites
        'finder': [
            'helpful reviews',
            'good comparison tool',
            'easy to use',
            'lots of options',
            'detailed information'
        ],
        'canstar': [
            'star ratings',
            'trusted reviews',
            'award winners',
            'reliable ratings',
            'good research'
        ],
        'iselect': [
            'TV ads',
            'phone service',
            'personal help',
            'lots of advertising',
            'call center'
        ],
        'compare the market': [
            'meerkat ads',
            'Sergei and Aleksandr',
            'funny commercials',
            'price comparison',
            'meerkats'
        ],
        'choice': [
            'independent reviews',
            'consumer advocacy',
            'unbiased',
            'subscription service',
            'product testing'
        ],
        
        # Energy companies
        'origin': [
            'big energy company',
            'electricity and gas',
            'major supplier',
            'solar options',
            'been around long time'
        ],
        'agl': [
            'large energy provider',
            'renewable energy',
            'electricity supplier',
            'competitive rates',
            'green energy options'
        ],
        'energy australia': [
            'power company',
            'electricity provider',
            'good customer service',
            'reliable supply',
            'various plans'
        ],
        
        # Banks
        'commonwealth bank': [
            'biggest bank',
            'yellow and black',
            'CBA',
            'everywhere',
            'good app'
        ],
        'westpac': [
            'red bank',
            'one of big four',
            'mortgages',
            'long history',
            'branches everywhere'
        ],
        
        # Telcos
        'telstra': [
            'biggest telco',
            'expensive but reliable',
            'best coverage',
            'mobile network',
            'NBN provider'
        ],
        'optus': [
            'second biggest',
            'cheaper than Telstra',
            'sports streaming',
            'yes brand',
            'mobile plans'
        ],
        
        # Retailers
        'woolworths': [
            'supermarket',
            'fresh food people',
            'groceries',
            'rewards program',
            'green logo'
        ],
        'coles': [
            'red hand logo',
            'supermarket',
            'flybuys',
            'down down prices',
            'groceries'
        ],
        
        # Default associations for unknown brands
        'default': [
            'familiar brand',
            'well known',
            'seen advertising',
            'heard of them',
            'recognizable name'
        ]
    }
    
    # Alternative phrases to add variety
    MODIFIERS = [
        '',  # No modifier
        'quite ',
        'pretty ',
        'fairly ',
        'seems '
    ]
    
    async def detect_brand_association_question(self, page) -> bool:
        """Detect if this is a brand association text input question"""
        
        # Check for the telltale signs
        indicators = [
            'what comes to mind',
            'thinking about',
            'describe',
            'tell us about',
            'your thoughts on',
            'what do you think'
        ]
        
        # Get question text
        question_text = await page.evaluate('''() => {
            const headings = document.querySelectorAll('h1, h2, h3, p');
            for (let h of headings) {
                if (h.innerText.length > 20) {
                    return h.innerText.toLowerCase();
                }
            }
            return '';
        }''')
        
        has_indicator = any(ind in question_text for ind in indicators)
        
        # Check for multiple text inputs
        text_inputs = await page.query_selector_all('input[type="text"], textarea')
        
        # Check for brand labels near inputs
        brand_labels = await self.detect_brand_labels(page)
        
        if has_indicator and len(text_inputs) >= 3 and len(brand_labels) >= 3:
            print(f"💭 Detected brand association question with {len(text_inputs)} brands")
            return True
        
        return False
    
    async def detect_brand_labels(self, page) -> list:
        """Extract brand names associated with text inputs"""
        
        brands = []
        
        # Method 1: Look for labels or text near inputs
        rows = await page.query_selector_all('tr, div[class*="row"], div[class*="brand"]')
        
        for row in rows:
            try:
                # Get text content
                text = await row.evaluate('el => el.innerText')
                
                # Check if there's an input field in this row
                has_input = await row.evaluate('''el => {
                    return el.querySelector('input[type="text"], textarea') !== null;
                }''')
                
                if has_input and text:
                    # Extract brand name (usually first part before input)
                    lines = text.strip().split('\n')
                    if lines and len(lines[0]) < 50:  # Reasonable brand name length
                        brand = lines[0].strip()
                        if brand and not any(skip in brand.lower() for skip in 
                                            ['please', 'answer', 'type', 'enter']):
                            brands.append(brand)
            except:
                continue
        
        # Method 2: Look for text immediately before inputs
        if not brands:
            inputs = await page.query_selector_all('input[type="text"], textarea')
            for input_elem in inputs:
                try:
                    # Get previous sibling or parent text
                    brand = await input_elem.evaluate('''el => {
                        // Check previous sibling
                        let prev = el.previousElementSibling;
                        if (prev && prev.innerText) {
                            return prev.innerText.trim();
                        }
                        
                        // Check parent's first text node
                        let parent = el.parentElement;
                        if (parent) {
                            let text = parent.innerText.split('\\n')[0];
                            return text.trim();
                        }
                        
                        return '';
                    }''')
                    
                    if brand and len(brand) < 50:
                        brands.append(brand)
                except:
                    continue
        
        print(f"📋 Detected brands: {brands}")
        return brands
    
    def get_association_for_brand(self, brand_name: str) -> str:
        """Get an appropriate association text for a brand"""
        
        brand_lower = brand_name.lower().strip()
        
        # Direct match
        if brand_lower in self.BRAND_ASSOCIATIONS:
            associations = self.BRAND_ASSOCIATIONS[brand_lower]
        # Partial match
        else:
            found = False
            for key, values in self.BRAND_ASSOCIATIONS.items():
                if key in brand_lower or brand_lower in key:
                    associations = values
                    found = True
                    break
            
            if not found:
                # Check for common words
                if 'compare' in brand_lower or 'comparison' in brand_lower:
                    associations = ['comparison site', 'price comparison', 'helpful tool']
                elif 'insurance' in brand_lower:
                    associations = ['insurance company', 'coverage options', 'insurance provider']
                elif 'energy' in brand_lower or 'power' in brand_lower:
                    associations = ['energy provider', 'electricity company', 'power supplier']
                else:
                    associations = self.BRAND_ASSOCIATIONS['default']
        
        # Pick a random association
        import random
        base_association = random.choice(associations)
        
        # Sometimes add a modifier (30% chance)
        if random.random() < 0.3:
            modifier = random.choice(self.MODIFIERS)
            association = modifier + base_association
        else:
            association = base_association
        
        # Occasionally make it slightly personal (20% chance)
        if random.random() < 0.2:
            personal_prefix = random.choice([
                'I think ',
                'seems like ',
                'looks like ',
                ''
            ])
            association = personal_prefix + association
        
        return association
    
    async def fill_brand_associations(self, page, brands: list = None) -> int:
        """Fill in text associations for all brands"""
        
        print("💭 Filling brand associations...")
        
        # If brands not provided, detect them
        if not brands:
            brands = await self.detect_brand_labels(page)
        
        if not brands:
            print("❌ No brands detected")
            return 0
        
        success_count = 0
        
        # Method 1: Find inputs by adjacent brand text
        for brand in brands:
            association = self.get_association_for_brand(brand)
            
            # Try different selectors to find the right input
            selectors = [
                # Input in same row as brand text
                f'tr:has-text("{brand}") input[type="text"]',
                f'tr:has-text("{brand}") textarea',
                f'div:has-text("{brand}") input[type="text"]',
                f'div:has-text("{brand}") textarea',
                
                # Input after brand text
                f'text="{brand}" >> xpath=following::input[1]',
                f'text="{brand}" >> xpath=following::textarea[1]',
                
                # Using partial match
                f'*:has-text("{brand}") >> input[type="text"]',
                f'*:has-text("{brand}") >> textarea'
            ]
            
            filled = False
            for selector in selectors:
                try:
                    input_elem = await page.wait_for_selector(selector, timeout=1000)
                    if input_elem:
                        # Clear and fill
                        await input_elem.click()
                        await input_elem.fill('')  # Clear first
                        await input_elem.type(association, delay=50)  # Type with human-like delay
                        
                        await page.wait_for_timeout(200)  # Small pause between brands
                        
                        print(f"✅ {brand}: '{association}'")
                        success_count += 1
                        filled = True
                        break
                except:
                    continue
            
            if not filled:
                print(f"⚠️ Could not fill association for: {brand}")
        
        # Method 2: If method 1 didn't work, try filling by position
        if success_count == 0:
            inputs = await page.query_selector_all('input[type="text"]:visible, textarea:visible')
            
            for i, input_elem in enumerate(inputs[:len(brands)]):  # Don't overfill
                try:
                    brand = brands[i] if i < len(brands) else f"Brand {i+1}"
                    association = self.get_association_for_brand(brand)
                    
                    await input_elem.click()
                    await input_elem.fill('')
                    await input_elem.type(association, delay=50)
                    
                    print(f"✅ Input {i+1}: '{association}'")
                    success_count += 1
                    
                    await page.wait_for_timeout(200)
                except Exception as e:
                    print(f"Error filling input {i+1}: {e}")
        
        print(f"📊 Filled {success_count}/{len(brands)} brand associations")
        return success_count
    
    async def handle_brand_association_question(self, page) -> bool:
        """Main handler for brand association questions"""
        
        # Detect if this is the right question type
        if not await self.detect_brand_association_question(page):
            return False
        
        # Fill in all associations
        success_count = await self.fill_brand_associations(page)
        
        return success_count > 0