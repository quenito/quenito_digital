# services/multi_question_handler.py - NEW FILE

class MultiQuestionHandler:
    """Handles pages with multiple questions that need sequential answering"""
    
    # Smart response patterns for different question types
    RESPONSE_PATTERNS = {
        'past_purchase': {
            'vehicle_insurance': 'no',  # Most people haven't bought caravan insurance
            'home_insurance': 'yes',    # Common
            'health_insurance': 'yes',  # Common
            'life_insurance': 'no',     # Less common
            'pet_insurance': 'no',      # Less common
            'default': 'no'             # Conservative default
        },
        'future_intent': {
            'likely': 'maybe',          # "open or likely in near future"
            'default': 'maybe'
        },
        'past_behavior': {
            'in_home_care': 'no',       # Specific, uncommon
            'medical': 'yes',           # Common
            'travel': 'yes',            # Common
            'default': 'no'
        },
        'yes_no_simple': {
            'default': 'no'             # Conservative for unknowns
        }
    }
    
    async def detect_multi_question_page(self, page) -> bool:
        """Detect if this page has multiple questions to answer"""
        
        # Count question indicators
        question_indicators = await page.query_selector_all('''
            h2:has-text("?"),
            h3:has-text("?"),
            p:has-text("?"),
            div[class*="question"]:has-text("?")
        ''')
        
        # Count sets of radio buttons
        radio_groups = await self.count_radio_groups(page)
        
        # Count "Please select" text
        select_prompts = await page.query_selector_all('text=/Please select/')
        
        # If we have multiple questions with radio groups
        if len(question_indicators) >= 2 or radio_groups >= 2 or len(select_prompts) >= 2:
            print(f"📋 Detected multi-question page with {max(len(question_indicators), radio_groups)} questions")
            return True
        
        return False
    
    async def count_radio_groups(self, page) -> int:
        """Count distinct radio button groups"""
        
        radio_names = await page.evaluate('''() => {
            const radios = document.querySelectorAll('input[type="radio"]');
            const names = new Set();
            radios.forEach(r => {
                if (r.name) names.add(r.name);
            });
            return names.size;
        }''')
        
        return radio_names
    
    async def extract_questions(self, page) -> list:
        """Extract all questions from the page"""
        
        questions = []
        
        # Method 1: Look for question text patterns
        question_elements = await page.query_selector_all('''
            *:has-text("In the past"),
            *:has-text("Have you"),
            *:has-text("Do you"),
            *:has-text("Will you"),
            *:has-text("Are you")
        ''')
        
        for element in question_elements:
            try:
                text = await element.inner_text()
                # Filter to actual questions
                if '?' in text and len(text) > 20 and len(text) < 500:
                    # Get the radio group associated with this question
                    radio_group = await self.find_radio_group_for_question(page, text)
                    if radio_group:
                        questions.append({
                            'text': text.strip(),
                            'element': element,
                            'radio_group': radio_group
                        })
            except:
                continue
        
        # Method 2: Find by structure (question text followed by radio options)
        if not questions:
            containers = await page.query_selector_all('div[class*="question"], tr, div[class*="row"]')
            
            for container in containers:
                try:
                    text = await container.evaluate('''el => {
                        const text = el.innerText;
                        return text && text.includes('?') ? text.split('\\n')[0] : null;
                    }''')
                    
                    if text and len(text) > 20:
                        # Check for radio buttons in this container
                        has_radios = await container.evaluate('''el => {
                            return el.querySelectorAll('input[type="radio"]').length > 0;
                        }''')
                        
                        if has_radios:
                            questions.append({
                                'text': text.strip(),
                                'container': container
                            })
                except:
                    continue
        
        print(f"📝 Extracted {len(questions)} questions")
        for i, q in enumerate(questions):
            print(f"  Q{i+1}: {q['text'][:60]}...")
        
        return questions
    
    async def find_radio_group_for_question(self, page, question_text: str) -> str:
        """Find the radio button group name for a question"""
        
        # Find radio buttons near this question text
        try:
            # Look for the container with this question
            container = await page.query_selector(f'*:has-text("{question_text[:30]}")')
            if container:
                # Find radio buttons within or after this container
                radio = await container.query_selector('input[type="radio"]')
                if not radio:
                    # Try next sibling
                    radio = await container.evaluate_handle('''el => {
                        let next = el.nextElementSibling;
                        while (next && !next.querySelector('input[type="radio"]')) {
                            next = next.nextElementSibling;
                        }
                        return next ? next.querySelector('input[type="radio"]') : null;
                    }''')
                
                if radio:
                    name = await radio.get_attribute('name')
                    return name
        except:
            pass
        
        return None
    
    def determine_response(self, question_text: str) -> str:
        """Determine the appropriate response based on question content"""
        
        q_lower = question_text.lower()
        
        # Check for past purchase questions
        if 'in the past' in q_lower and ('purchased' in q_lower or 'paid' in q_lower):
            if 'caravan' in q_lower or 'camper' in q_lower or 'four-wheel' in q_lower:
                return 'no'  # Specific vehicles - less common
            elif 'home' in q_lower or 'house' in q_lower:
                return 'yes'  # Home insurance - common
            elif 'health' in q_lower:
                return 'yes'  # Health insurance - common
            else:
                return 'no'  # Conservative default
        
        # Check for future intent
        if 'near future' in q_lower or 'likely' in q_lower or 'open to' in q_lower:
            return 'maybe'  # "No, but I am open or likely to in the near future"
        
        # Check for care/medical questions
        if 'care' in q_lower or 'medical' in q_lower:
            if 'in-home care' in q_lower or 'organised' in q_lower:
                return 'no'  # In-home care - less common
            else:
                return 'yes'  # General medical - common
        
        # Check for usage questions
        if 'do you use' in q_lower or 'have you used' in q_lower:
            return 'yes' if 'regularly' not in q_lower else 'sometimes'
        
        # Default conservative response
        return 'no'
    
    async def select_radio_option(self, page, question: dict, response: str) -> bool:
        """Select the appropriate radio button for a question"""
        
        print(f"  → Answering: {response}")
        
        # Map response to actual option text
        option_map = {
            'yes': ['Yes', 'yes'],
            'no': ['No', 'no'],
            'maybe': [
                'No, but I am open or likely to in the near future',
                'Maybe', 
                'Not sure',
                'Possibly'
            ],
            'sometimes': ['Sometimes', 'Occasionally']
        }
        
        option_texts = option_map.get(response, [response])
        
        # Try to click the right option
        for option_text in option_texts:
            selectors = [
                f'label:has-text("{option_text}")',
                f'text="{option_text}"',
                f'input[type="radio"][value*="{option_text.lower()}"]'
            ]
            
            # If we have a radio group name, be more specific
            if 'radio_group' in question and question['radio_group']:
                selectors.insert(0, 
                    f'input[type="radio"][name="{question["radio_group"]}"] + label:has-text("{option_text}")'
                )
            
            for selector in selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=1000)
                    if element:
                        # Check if it's the input or label
                        tag_name = await element.evaluate('el => el.tagName')
                        
                        if tag_name == 'INPUT':
                            await element.click()
                        else:
                            # It's probably a label, click it
                            await element.click()
                        
                        await page.wait_for_timeout(300)  # Small delay
                        print(f"    ✅ Selected: {option_text}")
                        return True
                except:
                    continue
        
        print(f"    ⚠️ Could not select {response}")
        return False
    
    async def handle_multi_question_page(self, page) -> bool:
        """Main handler for multi-question pages"""
        
        print("📋 Handling multi-question page...")
        
        # Extract all questions
        questions = await self.extract_questions(page)
        
        if not questions:
            print("❌ No questions found")
            return False
        
        success_count = 0
        
        # Answer each question
        for i, question in enumerate(questions):
            print(f"\n🔹 Question {i+1}/{len(questions)}: {question['text'][:60]}...")
            
            # Determine response
            response = self.determine_response(question['text'])
            
            # Select the option
            success = await self.select_radio_option(page, question, response)
            
            if success:
                success_count += 1
            
            # Small delay between questions
            await page.wait_for_timeout(200)
        
        print(f"\n📊 Successfully answered {success_count}/{len(questions)} questions")
        
        # After answering all, look for continue button
        if success_count > 0:
            await self.click_continue_if_present(page)
        
        return success_count > 0
    
    async def click_continue_if_present(self, page):
        """Click continue/next button if all questions are answered"""
        
        await page.wait_for_timeout(500)  # Wait for any validation
        
        continue_selectors = [
            'button:has-text("Continue")',
            'button:has-text("Next")',
            'input[type="submit"]',
            'button[type="submit"]'
        ]
        
        for selector in continue_selectors:
            try:
                button = await page.query_selector(selector)
                if button:
                    is_enabled = await button.is_enabled()
                    if is_enabled:
                        await button.click()
                        print("✅ Clicked continue button")
                        return True
            except:
                continue
        
        return False