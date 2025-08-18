# services/rating_handler.py - NEW FILE

import random
from typing import Optional, Tuple

class RatingScaleHandler:
    """Handles all types of rating scales and sliders in surveys"""
    
    # Smart rating strategies to appear human-like
    RATING_STRATEGIES = {
        'satisfaction': {
            'range': (6, 8),      # Generally satisfied
            'variance': 1,        # Can vary by ±1
            'description': 'Generally positive but not extreme'
        },
        'likelihood': {
            'range': (7, 8),      # Likely to recommend
            'variance': 1,
            'description': 'Positive likelihood'
        },
        'nps': {  # Net Promoter Score
            'range': (7, 8),      # Passive to Promoter
            'variance': 1,
            'description': 'NPS Passive/Promoter range'
        },
        'importance': {
            'range': (6, 8),      # Moderately to very important
            'variance': 1,
            'description': 'Important but not critical'
        },
        'frequency': {
            'range': (3, 4),      # Sometimes to often (on 1-5 scale)
            'variance': 0,
            'description': 'Regular usage'
        },
        'agreement': {
            'range': (4, 4),      # Agree (on 1-5 scale)
            'variance': 0,
            'description': 'Generally agree'
        },
        'quality': {
            'range': (7, 8),      # Good quality
            'variance': 1,
            'description': 'Good quality rating'
        },
        'default': {
            'range': (6, 8),      # Safe middle-high range
            'variance': 1,
            'description': 'Default positive rating'
        }
    }
    
    async def detect_rating_scale(self, page) -> dict:
        """Detect the type and range of rating scale"""
        
        scale_info = {
            'type': None,
            'min': 0,
            'max': 10,
            'format': None,  # 'buttons', 'slider', 'radio', 'stars'
            'detected': False
        }
        
        # Method 1: Check for number buttons (most common)
        number_buttons = await self.detect_number_buttons(page)
        if number_buttons:
            scale_info.update(number_buttons)
            scale_info['detected'] = True
            return scale_info
        
        # Method 2: Check for slider
        slider = await self.detect_slider(page)
        if slider:
            scale_info.update(slider)
            scale_info['detected'] = True
            return scale_info
        
        # Method 3: Check for radio buttons with numbers
        radio_scale = await self.detect_radio_scale(page)
        if radio_scale:
            scale_info.update(radio_scale)
            scale_info['detected'] = True
            return scale_info
        
        # Method 4: Check for star rating
        stars = await self.detect_star_rating(page)
        if stars:
            scale_info.update(stars)
            scale_info['detected'] = True
            return scale_info
        
        return scale_info
    
    async def detect_number_buttons(self, page) -> Optional[dict]:
        """Detect clickable number buttons (0-10, 1-5, etc.)"""
        
        # Look for button patterns
        button_selectors = [
            'button[class*="scale"]',
            'button[class*="rating"]',
            'div[class*="scale"] button',
            'label[class*="scale"]',
            'span[class*="rating-option"]',
            'div[role="button"]'
        ]
        
        all_numbers = []
        
        for selector in button_selectors:
            elements = await page.query_selector_all(selector)
            
            for element in elements:
                try:
                    text = await element.inner_text()
                    # Check if it's a number
                    if text.strip().isdigit():
                        all_numbers.append(int(text.strip()))
                except:
                    continue
        
        if all_numbers:
            all_numbers.sort()
            print(f"📊 Detected number scale: {min(all_numbers)} to {max(all_numbers)}")
            
            return {
                'type': 'number_scale',
                'min': min(all_numbers),
                'max': max(all_numbers),
                'format': 'buttons',
                'available_values': all_numbers
            }
        
        return None
    
    async def detect_slider(self, page) -> Optional[dict]:
        """Detect slider input elements"""
        
        slider_selectors = [
            'input[type="range"]',
            'div[class*="slider"]',
            'div[role="slider"]',
            '.ui-slider',
            'div[class*="rc-slider"]'
        ]
        
        for selector in slider_selectors:
            element = await page.query_selector(selector)
            if element:
                # Get slider attributes
                if selector == 'input[type="range"]':
                    min_val = await element.get_attribute('min') or '0'
                    max_val = await element.get_attribute('max') or '100'
                    
                    print(f"🎚️ Detected slider: {min_val} to {max_val}")
                    
                    return {
                        'type': 'slider',
                        'min': int(min_val),
                        'max': int(max_val),
                        'format': 'slider',
                        'element': element
                    }
                else:
                    # For custom sliders, try to extract range from aria attributes
                    min_val = await element.get_attribute('aria-valuemin') or '0'
                    max_val = await element.get_attribute('aria-valuemax') or '10'
                    
                    return {
                        'type': 'slider',
                        'min': int(min_val),
                        'max': int(max_val),
                        'format': 'slider',
                        'element': element
                    }
        
        return None
    
    async def detect_radio_scale(self, page) -> Optional[dict]:
        """Detect radio button scales"""
        
        radio_buttons = await page.query_selector_all('input[type="radio"]')
        
        if len(radio_buttons) >= 3:  # At least 3 options for a scale
            values = []
            
            for radio in radio_buttons:
                # Get the value or label
                value = await radio.get_attribute('value')
                if value and value.isdigit():
                    values.append(int(value))
                else:
                    # Check label
                    label_for = await radio.get_attribute('id')
                    if label_for:
                        label = await page.query_selector(f'label[for="{label_for}"]')
                        if label:
                            text = await label.inner_text()
                            if text.strip().isdigit():
                                values.append(int(text.strip()))
            
            if values:
                values.sort()
                print(f"📻 Detected radio scale: {min(values)} to {max(values)}")
                
                return {
                    'type': 'radio_scale',
                    'min': min(values),
                    'max': max(values),
                    'format': 'radio',
                    'available_values': values
                }
        
        return None
    
    async def detect_star_rating(self, page) -> Optional[dict]:
        """Detect star rating systems"""
        
        star_selectors = [
            'i[class*="star"]',
            'span[class*="star"]',
            'svg[class*="star"]',
            '.rating-star',
            '[role="radio"][aria-label*="star"]'
        ]
        
        for selector in star_selectors:
            stars = await page.query_selector_all(selector)
            if len(stars) >= 3:  # At least 3 stars
                print(f"⭐ Detected {len(stars)} star rating")
                
                return {
                    'type': 'star_rating',
                    'min': 1,
                    'max': len(stars),
                    'format': 'stars',
                    'star_count': len(stars)
                }
        
        return None
    
    def determine_rating_strategy(self, question_text: str) -> str:
        """Determine which rating strategy to use based on question"""
        
        q_lower = question_text.lower()
        
        # Map keywords to strategies
        strategy_keywords = {
            'satisfaction': ['satisfied', 'satisfaction', 'happy'],
            'likelihood': ['likely', 'likelihood', 'recommend', 'chance'],
            'nps': ['recommend to a friend', 'recommend to a colleague', 'net promoter'],
            'importance': ['important', 'importance', 'matter'],
            'frequency': ['often', 'frequently', 'frequency', 'how many times'],
            'agreement': ['agree', 'agreement', 'disagree'],
            'quality': ['quality', 'good', 'excellent', 'poor']
        }
        
        for strategy, keywords in strategy_keywords.items():
            if any(keyword in q_lower for keyword in keywords):
                print(f"📋 Using {strategy} rating strategy")
                return strategy
        
        return 'default'
    
    def calculate_rating(self, strategy: str, scale_min: int, scale_max: int) -> int:
        """Calculate appropriate rating based on strategy and scale"""
        
        config = self.RATING_STRATEGIES[strategy]
        base_range = config['range']
        variance = config['variance']
        
        # Adjust for scale (e.g., 0-10, 1-5, 1-7)
        scale_size = scale_max - scale_min
        
        if scale_size <= 5:  # 1-5 or 0-5 scale
            if scale_max == 5:
                # For 1-5 scale
                if strategy in ['satisfaction', 'likelihood', 'quality']:
                    rating = 4  # "Satisfied/Likely"
                elif strategy == 'agreement':
                    rating = 4  # "Agree"
                elif strategy == 'frequency':
                    rating = 3  # "Sometimes"
                else:
                    rating = 4
            else:
                # For 0-5 scale
                rating = 4
        
        elif scale_size <= 7:  # 1-7 scale
            # Map to 1-7 scale
            rating = random.randint(5, 6)
        
        else:  # 0-10 or 1-10 scale
            # Use the base range with variance
            min_rating = base_range[0]
            max_rating = base_range[1]
            
            # Add some randomness
            rating = random.randint(min_rating, max_rating)
            
            # Apply variance occasionally (30% chance)
            if random.random() < 0.3 and variance > 0:
                rating += random.choice([-variance, variance])
                rating = max(scale_min, min(rating, scale_max))
        
        print(f"🎯 Calculated rating: {rating} (scale: {scale_min}-{scale_max})")
        return rating
    
    async def apply_rating(self, page, scale_info: dict, rating: int) -> bool:
        """Apply the calculated rating to the page"""
        
        format_type = scale_info['format']
        
        if format_type == 'buttons':
            return await self.click_number_button(page, rating)
        
        elif format_type == 'slider':
            return await self.set_slider_value(page, scale_info, rating)
        
        elif format_type == 'radio':
            return await self.select_radio_value(page, rating)
        
        elif format_type == 'stars':
            return await self.click_star_rating(page, rating)
        
        return False
    
    async def click_number_button(self, page, number: int) -> bool:
        """Click a number button"""
        
        selectors = [
            f'button:has-text("{number}")',
            f'div[role="button"]:has-text("{number}")',
            f'label:has-text("{number}")',
            f'span[class*="rating"]:has-text("{number}")',
            f'[data-value="{number}"]',
            f'[value="{number}"]'
        ]
        
        for selector in selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=2000)
                if element:
                    await element.click()
                    await page.wait_for_timeout(200)
                    print(f"✅ Clicked rating: {number}")
                    return True
            except:
                continue
        
        print(f"⚠️ Could not click rating: {number}")
        return False
    
    async def set_slider_value(self, page, scale_info: dict, value: int) -> bool:
        """Set a slider to a specific value"""
        
        try:
            # For HTML5 range input
            slider = await page.query_selector('input[type="range"]')
            if slider:
                await slider.evaluate(f'(el) => el.value = {value}')
                
                # Trigger change event
                await slider.evaluate('(el) => el.dispatchEvent(new Event("change", {bubbles: true}))')
                await slider.evaluate('(el) => el.dispatchEvent(new Event("input", {bubbles: true}))')
                
                print(f"✅ Set slider to: {value}")
                return True
            
            # For custom sliders, try clicking at position
            custom_slider = await page.query_selector('div[class*="slider"], div[role="slider"]')
            if custom_slider:
                # Calculate position
                box = await custom_slider.bounding_box()
                if box:
                    # Calculate click position
                    scale_range = scale_info['max'] - scale_info['min']
                    position_ratio = (value - scale_info['min']) / scale_range
                    click_x = box['x'] + (box['width'] * position_ratio)
                    click_y = box['y'] + (box['height'] / 2)
                    
                    await page.mouse.click(click_x, click_y)
                    print(f"✅ Clicked slider at position for value: {value}")
                    return True
        
        except Exception as e:
            print(f"Error setting slider: {e}")
        
        return False
    
    async def select_radio_value(self, page, value: int) -> bool:
        """Select a radio button with a specific value"""
        
        selectors = [
            f'input[type="radio"][value="{value}"]',
            f'input[type="radio"][id*="{value}"]'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected radio value: {value}")
                    return True
                    
                # Try clicking the label
                radio_id = await element.get_attribute('id')
                if radio_id:
                    label = await page.query_selector(f'label[for="{radio_id}"]')
                    if label:
                        await label.click()
                        print(f"✅ Clicked label for radio value: {value}")
                        return True
            except:
                continue
        
        return False
    
    async def click_star_rating(self, page, stars: int) -> bool:
        """Click on star rating"""
        
        star_selectors = [
            'i[class*="star"]',
            'span[class*="star"]',
            'svg[class*="star"]',
            '.rating-star'
        ]
        
        for selector in star_selectors:
            elements = await page.query_selector_all(selector)
            if len(elements) >= stars:
                # Click the nth star (0-indexed)
                await elements[stars - 1].click()
                print(f"✅ Clicked {stars} stars")
                return True
        
        return False
    
    async def handle_rating_question(self, page, question_text: str) -> bool:
        """Main handler for rating questions"""
        
        print("📊 Handling rating scale question...")
        
        # Step 1: Detect the scale
        scale_info = await self.detect_rating_scale(page)
        
        if not scale_info['detected']:
            print("❌ No rating scale detected")
            return False
        
        # Step 2: Determine strategy
        strategy = self.determine_rating_strategy(question_text)
        
        # Step 3: Calculate rating
        rating = self.calculate_rating(
            strategy, 
            scale_info['min'], 
            scale_info['max']
        )
        
        # Step 4: Apply rating
        success = await self.apply_rating(page, scale_info, rating)
        
        return success