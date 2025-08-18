# services/demographics_handler.py - CLEAN VERSION (Logic Only, No Data)

class DemographicsHandler:
    """Handles all demographic questions using persona knowledge base"""
    
    def __init__(self, knowledge_base):
        """Initialize with reference to knowledge base"""
        self.kb = knowledge_base
        
    def get_demographic(self, field_name: str):
        """Helper method to get demographic data from knowledge base"""
        # Access the actual data structure in knowledge base
        if hasattr(self.kb, 'data') and 'user_profile' in self.kb.data:
            user_profile = self.kb.data['user_profile']
            
            # Map field names to their locations in the data structure
            field_mapping = {
                # Personal fields
                'age': user_profile.get('personal', {}).get('age'),
                'age_range': user_profile.get('personal', {}).get('age_range'),
                'gender': user_profile.get('personal', {}).get('gender'),
                'birth_month': user_profile.get('personal', {}).get('birth_month', 'June'),
                'birth_year': user_profile.get('personal', {}).get('birth_year', 1980),  # Calculated from age
                
                # Location fields
                'postcode': user_profile.get('location', {}).get('postcode'),
                'state': user_profile.get('location', {}).get('state'),
                'state_code': user_profile.get('location', {}).get('state_code'),
                
                # Household fields
                'marital_status': user_profile.get('household', {}).get('marital_status'),
                'children': user_profile.get('household', {}).get('children'),
                'children_count': user_profile.get('household', {}).get('children_count'),
                'household': user_profile.get('household', {}),
                'home_ownership': user_profile.get('household', {}).get('home_ownership'),
                
                # Employment fields
                'employment_status': user_profile.get('employment', {}).get('employment_status'),
                'industry': user_profile.get('employment', {}).get('industry'),
                'sub_industry': user_profile.get('employment', {}).get('sub_industry'),
                
                # Financial fields
                'personal_income': user_profile.get('financial', {}).get('personal_income'),
                'household_income': user_profile.get('financial', {}).get('household_income'),
                
                # Education fields
                'highest_level': user_profile.get('education', {}).get('highest_level'),
            }
            
            return field_mapping.get(field_name)
        
        # Fallback: try direct access if kb has different structure
        if hasattr(self.kb, 'get_demographic'):
            return self.kb.get_demographic(field_name)
        
        return None
    
    async def detect_household_question(self, page) -> bool:
        """Detect if this is a household composition question"""
        
        indicators = [
            'describe your household',
            'who lives in your household',
            'household composition',
            'living situation',
            'who do you live with'
        ]
        
        question_text = await self.get_question_text(page)
        
        # Check for indicators
        if any(ind in question_text.lower() for ind in indicators):
            # Verify we have checkboxes with household options
            household_options = [
                'Living by myself',
                'Living with my partner',
                'Living with others',
                'Family with children'
            ]
            
            for option in household_options:
                element = await page.query_selector(f'text=/{option}/i')
                if element:
                    print("👨‍👩‍👧‍👦 Detected household composition question")
                    return True
        
        return False
    
    async def handle_household_question(self, page) -> bool:
        """Handle household composition multi-select"""
        
        print("👨‍👩‍👧‍👦 Handling household composition...")
        
        # Get household composition from knowledge base
        household_data = self.get_demographic('household')
        if isinstance(household_data, dict):
            selections = household_data.get('composition', [])
        else:
            selections = []
        
        # Map knowledge base values to survey options if needed
        selection_mappings = {
            "Family with children under 5": ["Family with children under 5", "Family with young children"],
            "Family with children primary school aged": ["Family with children primary school aged", "Family with school age children"],
            "Couple with young children": ["Living with my partner only", "Family with children"]
        }
        
        success_count = 0
        
        for selection in selections:
            # Try mapped values and original
            options_to_try = selection_mappings.get(selection, [selection]) + [selection]
            
            for option in options_to_try:
                selectors = [
                    f'label:has-text("{option}")',
                    f'text="{option}" >> xpath=preceding-sibling::input[@type="checkbox"]',
                    f'text="{option}" >> xpath=following-sibling::input[@type="checkbox"]',
                    f'input[type="checkbox"] + label:has-text("{option}")',
                    f'label:has-text("{option}") input[type="checkbox"]'
                ]
                
                for selector in selectors:
                    try:
                        element = await page.wait_for_selector(selector, timeout=1000)
                        if element:
                            # Check if it's already selected
                            if selector.startswith('label'):
                                checkbox = await element.query_selector('input[type="checkbox"]')
                                if checkbox:
                                    is_checked = await checkbox.is_checked()
                                    if not is_checked:
                                        await element.click()
                                        success_count += 1
                                        print(f"  ✅ Selected: {option}")
                                    else:
                                        print(f"  ✔ Already selected: {option}")
                                        success_count += 1
                                else:
                                    await element.click()
                                    success_count += 1
                                    print(f"  ✅ Selected: {option}")
                            else:
                                is_checked = await element.is_checked()
                                if not is_checked:
                                    await element.click()
                                    success_count += 1
                                    print(f"  ✅ Selected: {option}")
                            
                            await page.wait_for_timeout(200)
                            break
                    except:
                        continue
                
                if success_count > 0:
                    break
        
        print(f"📊 Selected {success_count}/{len(selections)} household options")
        return success_count > 0
    
    async def detect_demographics_question(self, page) -> dict:
        """Detect any type of demographics question"""
        
        question_info = {
            'type': None,
            'detected': False
        }
        
        question_text = await self.get_question_text(page)
        q_lower = question_text.lower()
        
        # Check for different demographic types
        if 'household' in q_lower or 'live with' in q_lower or 'living situation' in q_lower:
            question_info['type'] = 'household'
            question_info['detected'] = True
        
        elif 'age' in q_lower or 'how old' in q_lower or 'birth' in q_lower:
            question_info['type'] = 'age'
            question_info['detected'] = True
        
        elif 'gender' in q_lower or 'sex' in q_lower:
            question_info['type'] = 'gender'
            question_info['detected'] = True
        
        elif 'postcode' in q_lower or 'post code' in q_lower or 'zip' in q_lower:
            question_info['type'] = 'postcode'
            question_info['detected'] = True
        
        elif 'income' in q_lower or 'earn' in q_lower or 'salary' in q_lower:
            question_info['type'] = 'income'
            question_info['detected'] = True
        
        elif 'employ' in q_lower or 'work' in q_lower or 'occupation' in q_lower:
            question_info['type'] = 'employment'
            question_info['detected'] = True
        
        elif 'education' in q_lower or 'qualification' in q_lower or 'degree' in q_lower:
            question_info['type'] = 'education'
            question_info['detected'] = True
        
        elif 'marital' in q_lower or 'married' in q_lower or 'relationship' in q_lower:
            question_info['type'] = 'marital_status'
            question_info['detected'] = True
        
        elif 'children' in q_lower or 'kids' in q_lower or 'dependents' in q_lower:
            question_info['type'] = 'children'
            question_info['detected'] = True
        
        elif 'state' in q_lower or 'territory' in q_lower or 'location' in q_lower:
            question_info['type'] = 'state'
            question_info['detected'] = True
        
        elif 'home' in q_lower and ('own' in q_lower or 'rent' in q_lower):
            question_info['type'] = 'home_ownership'
            question_info['detected'] = True
        
        elif 'industry' in q_lower or 'sector' in q_lower:
            question_info['type'] = 'industry'
            question_info['detected'] = True
        
        return question_info
    
    async def handle_demographics_question(self, page, question_type: str) -> bool:
        """Route to appropriate handler based on demographic type"""
        
        handlers = {
            'household': self.handle_household_question,
            'age': self.handle_age_question,
            'date_of_birth': self.handle_date_of_birth_question,
            'gender': self.handle_gender_question,
            'postcode': self.handle_postcode_question,
            'income': self.handle_income_question,
            'employment': self.handle_employment_question,
            'education': self.handle_education_question,
            'marital_status': self.handle_marital_question,
            'children': self.handle_children_question,
            'state': self.handle_state_question,
            'home_ownership': self.handle_home_ownership_question,
            'industry': self.handle_industry_question
        }
        
        handler = handlers.get(question_type)
        if handler:
            return await handler(page)
        
        return False
    
    async def handle_age_question(self, page) -> bool:
        """Handle age input or selection - SMART RANGE DETECTION"""
        
        # Get age from knowledge base
        age = self.get_demographic('age')  # Gets 45
        
        # Check if it's a text input or dropdown/radio
        text_input = await page.query_selector('input[type="text"], input[type="number"]')
        
        if text_input:
            await text_input.fill(str(age))
            print(f"✅ Entered age: {age}")
            return True
        
        # SMART AGE RANGE SELECTION - Find any range containing our age
        print(f"🔍 Looking for age range containing {age}...")
        
        # Try to find all options/labels that look like age ranges
        potential_selectors = [
            'option',  # Dropdown options
            'label',   # Radio/checkbox labels
            'input[type="radio"]',  # Radio buttons
            'div[class*="option"]',  # Div-based options
            'span[class*="option"]'  # Span-based options
        ]
        
        for selector_type in potential_selectors:
            try:
                elements = await page.query_selector_all(selector_type)
                
                for element in elements:
                    # Get the text content
                    try:
                        if selector_type.startswith('input'):
                            # For input elements, check the value attribute
                            text = await element.get_attribute('value') or ''
                            # Also check associated label
                            label_for = await element.get_attribute('id')
                            if label_for:
                                label = await page.query_selector(f'label[for="{label_for}"]')
                                if label:
                                    text = await label.inner_text()
                        else:
                            # For other elements, get inner text
                            text = await element.inner_text()
                    except:
                        continue
                    
                    if not text:
                        continue
                    
                    # Check if this text represents an age range containing our age
                    if self._age_in_range(age, text):
                        # Found a matching range!
                        await element.click()
                        print(f"✅ Selected age range: {text.strip()}")
                        return True
                        
            except Exception as e:
                continue
        
        # Fallback: Try common age range patterns
        print(f"🔄 Trying common patterns for age {age}...")
        
        # Common age ranges that would include 45
        possible_ranges = [
            "45-49", "45-50", "45-54", "45-55",  # Ranges starting with 45
            "40-45", "40-49", "40-50",           # Ranges ending with or including 45
            "41-50", "35-44", "35-45",           # Other ranges containing 45
            "35-54", "35-55", "40-54", "40-55"   # Wider ranges
        ]
        
        for range_text in possible_ranges:
            # Check if this range actually contains our age
            if not self._age_in_range(age, range_text):
                continue
                
            # Try various selector patterns
            selectors = [
                f'option:has-text("{range_text}")',
                f'label:has-text("{range_text}")',
                f'input[type="radio"][value*="{range_text}"]',
                f'text="{range_text}"'
            ]
            
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.click()
                        print(f"✅ Selected age range: {range_text}")
                        return True
                except:
                    continue
        
        print(f"⚠️ Could not find age range for {age}")
        return False
    
    def _age_in_range(self, age: int, text: str) -> bool:
        """
        Check if an age falls within a range described in text.
        Handles formats like: "45-54", "45 to 54", "45 - 54", "45-49 years", etc.
        """
        import re
        
        # Clean the text
        text = text.strip()
        
        # Pattern to match age ranges: "45-54", "45 to 54", "45 - 54", etc.
        patterns = [
            r'(\d+)\s*[-–—]\s*(\d+)',  # Various dash types
            r'(\d+)\s*to\s*(\d+)',      # "to" separator
            r'(\d+)\s*thru\s*(\d+)',    # "thru" separator
            r'(\d+)\s*through\s*(\d+)',  # "through" separator
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    start_age = int(match.group(1))
                    end_age = int(match.group(2))
                    
                    # Check if our age falls within this range (inclusive)
                    if start_age <= age <= end_age:
                        return True
                except:
                    continue
        
        # Also check for exact age match (like "45 years old")
        if str(age) in text:
            # Make sure it's not part of a range we already checked
            if not any(sep in text for sep in ['-', '–', '—', 'to', 'thru', 'through']):
                return True
        
        return False
    
    async def handle_date_of_birth_question(self, page) -> bool:
        """Handle date of birth with month/year dropdowns or date picker"""
        
        print("📅 Handling date of birth question...")
        
        # Get age from knowledge base and calculate birth year
        age = self.get_demographic('age')  # Gets 45
        if not age:
            print("⚠️ No age found in knowledge base")
            return False
            
        # Calculate birth year (current year is 2025)
        import datetime
        current_year = datetime.datetime.now().year
        birth_year = current_year - int(age)
        
        # Use June as default birth month (middle of year)
        birth_month = "June"
        birth_month_num = "6"
        
        print(f"📅 Calculated birth date: {birth_month} {birth_year} (age {age})")
        
        # Look for month and year dropdowns
        month_dropdown = None
        year_dropdown = None
        
        # Try to find month dropdown
        month_selectors = [
            'select[name*="month"]',
            'select[id*="month"]',
            'select[aria-label*="month"]',
            'select:has(option:has-text("January"))',
            'select:has(option:has-text("June"))'
        ]
        
        for selector in month_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    month_dropdown = element
                    print("✅ Found month dropdown")
                    break
            except:
                continue
        
        # Try to find year dropdown
        year_selectors = [
            'select[name*="year"]',
            'select[id*="year"]',
            'select[aria-label*="year"]',
            f'select:has(option:has-text("{birth_year}"))',
            f'select:has(option:has-text("{birth_year - 1}"))'
        ]
        
        for selector in year_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    year_dropdown = element
                    print("✅ Found year dropdown")
                    break
            except:
                continue
        
        # If we don't have specific selectors, try to find all visible selects
        if not month_dropdown or not year_dropdown:
            all_selects = await page.query_selector_all('select:visible')
            
            for select in all_selects:
                try:
                    # Get first option to check what type of dropdown it is
                    options = await select.query_selector_all('option')
                    if len(options) > 1:
                        first_option_text = await options[1].inner_text()  # Skip placeholder
                        
                        # Check if it's a month dropdown
                        if not month_dropdown and any(month in first_option_text for month in ['January', 'Jan', 'February', 'Feb']):
                            month_dropdown = select
                            print("✅ Found month dropdown by content")
                        
                        # Check if it's a year dropdown
                        elif not year_dropdown and first_option_text.isdigit() and len(first_option_text) == 4:
                            year_dropdown = select
                            print("✅ Found year dropdown by content")
                except:
                    continue
        
        success = False
        
        # Select month
        if month_dropdown:
            try:
                # Try selecting by month name
                await month_dropdown.select_option(label=birth_month)
                print(f"✅ Selected month: {birth_month}")
                success = True
            except:
                try:
                    # Try selecting by month number
                    await month_dropdown.select_option(value=birth_month_num)
                    print(f"✅ Selected month: {birth_month_num}")
                    success = True
                except:
                    try:
                        # Try selecting June by index (6th month = index 6 usually)
                        await month_dropdown.select_option(index=6)
                        print(f"✅ Selected month by index: 6")
                        success = True
                    except:
                        print("⚠️ Could not select month")
        
        # Select year
        if year_dropdown:
            try:
                # Try selecting by year text
                await year_dropdown.select_option(label=str(birth_year))
                print(f"✅ Selected year: {birth_year}")
                success = True
            except:
                try:
                    # Try with value attribute
                    await year_dropdown.select_option(value=str(birth_year))
                    print(f"✅ Selected year by value: {birth_year}")
                    success = True
                except:
                    # Try to find the year in options and click it
                    try:
                        year_option = await year_dropdown.query_selector(f'option:has-text("{birth_year}")')
                        if year_option:
                            await year_option.click()
                            print(f"✅ Selected year by clicking option: {birth_year}")
                            success = True
                    except:
                        print(f"⚠️ Could not select year {birth_year}")
        
        # Alternative: Look for date input field (HTML5 date picker)
        if not success:
            date_input = await page.query_selector('input[type="date"]')
            if date_input:
                # Format: YYYY-MM-DD
                date_value = f"{birth_year}-06-15"  # June 15th as default
                await date_input.fill(date_value)
                print(f"✅ Filled date input: {date_value}")
                success = True
        
        return success
    
    async def handle_gender_question(self, page) -> bool:
        """Handle gender selection"""
        
        gender = self.get_demographic('gender')  # Gets 'Male'
        
        selectors = [
            f'label:has-text("{gender}")',
            f'input[type="radio"][value="{gender}"]',
            f'option:has-text("{gender}")'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected gender: {gender}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_postcode_question(self, page) -> bool:
        """Handle postcode input"""
        
        postcode = self.get_demographic('postcode')  # Gets '2217'
        
        input_field = await page.query_selector('input[type="text"], input[type="number"], input[name*="postcode"], input[name*="zip"]')
        
        if input_field:
            await input_field.fill(postcode)
            print(f"✅ Entered postcode: {postcode}")
            return True
        
        return False
    
    async def handle_income_question(self, page) -> bool:
        """Handle income selection"""
        
        # Get income from knowledge base
        personal_income = self.get_demographic('personal_income')  # '$100,000 to $149,999'
        household_income = self.get_demographic('household_income')  # '$200,000 to $499,999'
        
        # Determine which income to use based on question text
        question_text = await self.get_question_text(page)
        
        if 'household' in question_text.lower():
            income = household_income
            income_keywords = ["200", "499", "200k", "500k", "200,000", "499,999"]
        else:
            income = personal_income
            income_keywords = ["100", "149", "100k", "150k", "100,000", "149,999"]
        
        # Try to find the income range
        selectors = []
        for keyword1 in income_keywords[:3]:
            for keyword2 in income_keywords[3:]:
                selectors.extend([
                    f'option:has-text("{keyword1}"):has-text("{keyword2}")',
                    f'label:has-text("{keyword1}"):has-text("{keyword2}")'
                ])
        
        selectors.extend([
            f'option:has-text("{income}")',
            f'label:has-text("{income}")'
        ])
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected income: {income}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_employment_question(self, page) -> bool:
        """Handle employment status selection"""
        
        employment_status = self.get_demographic('employment_status')  # 'Full-time'
        
        # Try various selectors for employment options
        selectors = [
            f'label:has-text("{employment_status}")',
            f'label:has-text("Full-time")',
            f'label:has-text("Full time")',
            f'input[type="radio"][value="{employment_status}"]',
            f'input[type="radio"][value="Full-time"]',
            f'option:has-text("{employment_status}")',
            f'option:has-text("Full-time")',
            f'text="Full-time employed"',
            f'text="Employed full-time"'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected employment: {employment_status}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_education_question(self, page) -> bool:
        """Handle education level selection"""
        
        education = self.get_demographic('highest_level')  # 'High school education'
        
        # Try various selectors for education options
        selectors = [
            f'label:has-text("{education}")',
            f'label:has-text("High school")',
            f'label:has-text("Secondary")',
            f'input[type="radio"][value*="High school"]',
            f'input[type="radio"][value*="Secondary"]',
            f'option:has-text("{education}")',
            f'option:has-text("High school")',
            f'text="High school"',
            f'text="Secondary education"',
            f'text="Year 12"'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected education: {education}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_marital_question(self, page) -> bool:
        """Handle marital status selection"""
        
        marital = self.get_demographic('marital_status')  # 'Married/civil partnership'
        
        # Try various selectors for marital status
        selectors = [
            f'label:has-text("Married")',
            f'label:has-text("Civil partnership")',
            f'label:has-text("{marital}")',
            f'input[type="radio"][value*="Married"]',
            f'input[type="radio"][value*="partnership"]',
            f'option:has-text("Married")',
            f'option:has-text("partnership")',
            f'text="Married"',
            f'text="Living with partner"',
            f'text="In a relationship"'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected marital status: {marital}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_children_question(self, page) -> bool:
        """Handle children/dependents question - SMART AGE DETECTION FOR KIDS"""
        
        has_children = self.get_demographic('children')  # 'Yes'
        children_count = self.get_demographic('children_count')  # 2
        
        # Get children details from knowledge base
        household_data = self.get_demographic('household')
        children_details = []
        if isinstance(household_data, dict):
            children_details = household_data.get('children_details', [])
        
        question_text = await self.get_question_text(page)
        q_lower = question_text.lower()
        
        # If asking yes/no about having children
        if 'do you have' in q_lower or 'any children' in q_lower:
            if has_children == 'Yes':
                selectors = [
                    f'label:has-text("Yes")',
                    f'input[type="radio"][value="Yes"]',
                    f'option:has-text("Yes")'
                ]
            else:
                selectors = [
                    f'label:has-text("No")',
                    f'input[type="radio"][value="No"]',
                    f'option:has-text("No")'
                ]
            
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.click()
                        print(f"✅ Selected children: {has_children}")
                        return True
                except:
                    continue
        
        # If asking for number of children
        if 'how many' in q_lower or 'number of' in q_lower:
            # Check if it's a number input
            number_input = await page.query_selector('input[type="number"], input[type="text"][name*="children"]')
            if number_input:
                await number_input.fill(str(children_count))
                print(f"✅ Entered children: {children_count}")
                return True
            
            # Or select from options
            selectors = [
                f'label:has-text("{children_count}")',
                f'option:has-text("{children_count}")',
                f'input[type="radio"][value="{children_count}"]'
            ]
            
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.click()
                        print(f"✅ Selected number of children: {children_count}")
                        return True
                except:
                    continue
        
        # SMART AGE RANGE DETECTION FOR CHILDREN'S AGES
        if 'age' in q_lower and ('child' in q_lower or 'kid' in q_lower or 'dependent' in q_lower):
            print("🔍 Detecting children's age selection...")
            
            # Get actual ages of children (3 and 6)
            children_ages = []
            for child in children_details:
                if 'age' in child:
                    children_ages.append(child['age'])
            
            if not children_ages:
                # Fallback to default if no specific ages found
                children_ages = [3, 6]  # Your daughters' ages
            
            print(f"👧 Looking for age ranges for children aged: {children_ages}")
            
            # Check if it's a multi-select (checkboxes) or single-select
            checkboxes = await page.query_selector_all('input[type="checkbox"]')
            
            if checkboxes:
                # Multi-select for multiple children
                selected_count = 0
                
                for age in children_ages:
                    # Find checkbox for each child's age range
                    found = await self._select_age_range_for_child(page, age, 'checkbox')
                    if found:
                        selected_count += 1
                
                if selected_count > 0:
                    print(f"✅ Selected {selected_count} age ranges for {len(children_ages)} children")
                    return True
            else:
                # Single select or dropdown - might need to select multiple times
                for i, age in enumerate(children_ages):
                    # Some surveys ask "Age of child 1:", "Age of child 2:", etc.
                    child_selectors = [
                        f'select[name*="child{i+1}"]',
                        f'select[name*="child_{i+1}"]',
                        f'select[name*="kid{i+1}"]',
                        f'div:has-text("Child {i+1}") >> select',
                        f'label:has-text("Child {i+1}") >> select'
                    ]
                    
                    dropdown_found = False
                    for selector in child_selectors:
                        dropdown = await page.query_selector(selector)
                        if dropdown:
                            # Find and select appropriate age range
                            options = await dropdown.query_selector_all('option')
                            for option in options:
                                option_text = await option.inner_text()
                                if self._age_in_range(age, option_text):
                                    await dropdown.select_option(label=option_text)
                                    print(f"✅ Selected age range '{option_text}' for child {i+1} (age {age})")
                                    dropdown_found = True
                                    break
                            
                            if dropdown_found:
                                break
                    
                    # If no specific dropdown, try general selection
                    if not dropdown_found:
                        found = await self._select_age_range_for_child(page, age, 'radio')
                        if found:
                            print(f"✅ Selected age range for child {i+1} (age {age})")
                
                return True
        
        return False
    
    async def _select_age_range_for_child(self, page, age: int, input_type: str = 'checkbox') -> bool:
        """
        Select the appropriate age range for a child.
        
        Args:
            page: The page object
            age: The child's age (e.g., 3 or 6)
            input_type: 'checkbox' or 'radio'
        """
        # Find all potential elements
        if input_type == 'checkbox':
            elements = await page.query_selector_all('input[type="checkbox"]')
        else:
            elements = await page.query_selector_all('input[type="radio"]')
        
        for element in elements:
            try:
                # Get associated label text
                element_id = await element.get_attribute('id')
                label_text = ''
                
                if element_id:
                    label = await page.query_selector(f'label[for="{element_id}"]')
                    if label:
                        label_text = await label.inner_text()
                
                # Also check value attribute
                value_text = await element.get_attribute('value') or ''
                
                # Check both label and value for age range
                combined_text = f"{label_text} {value_text}"
                
                if self._age_in_range(age, combined_text):
                    # Check if already selected (for checkboxes)
                    is_checked = await element.is_checked()
                    if not is_checked:
                        # Click the element or its label
                        if label:
                            await label.click()
                        else:
                            await element.click()
                        
                        print(f"   ✅ Selected range '{label_text or value_text}' for age {age}")
                        await page.wait_for_timeout(200)
                    return True
                    
            except Exception as e:
                continue
        
        # Fallback: Try common children's age ranges
        print(f"   🔄 Trying common patterns for child age {age}...")
        
        # Define common age ranges for children
        if age == 3:
            possible_ranges = ["0-4", "0-5", "2-4", "3-4", "3-5", "Under 5", "Toddler", "Preschool"]
        elif age == 6:
            possible_ranges = ["5-7", "5-8", "5-9", "5-10", "6-8", "6-10", "5-11", "5-12", "Primary school", "Elementary"]
        else:
            # Generic ranges based on age
            possible_ranges = [
                f"{age-2}-{age+2}",
                f"{age-1}-{age+3}",
                f"{age}-{age+4}"
            ]
        
        for range_text in possible_ranges:
            selectors = [
                f'label:has-text("{range_text}")',
                f'option:has-text("{range_text}")',
                f'text="{range_text}"'
            ]
            
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.click()
                        print(f"   ✅ Selected '{range_text}' for age {age}")
                        return True
                except:
                    continue
        
        return False
    
    async def handle_state_question(self, page) -> bool:
        """Handle state selection"""
        
        state = self.get_demographic('state')  # 'New South Wales'
        state_code = self.get_demographic('state_code')  # 'NSW'
        
        # Handle dropdown
        dropdown = await page.query_selector('select')
        if dropdown:
            # Try full name first, then code
            try:
                await dropdown.select_option(label=state)
                print(f"✅ Selected state: {state}")
                return True
            except:
                try:
                    await dropdown.select_option(label=state_code)
                    print(f"✅ Selected state: {state_code}")
                    return True
                except:
                    pass
        
        # Handle radio buttons - try both full name and code
        selectors = [
            f'label:has-text("{state}")',
            f'label:has-text("{state_code}")',
            f'input[type="radio"][value="{state}"]',
            f'input[type="radio"][value="{state_code}"]'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected state: {state}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_home_ownership_question(self, page) -> bool:
        """Handle home ownership status"""
        
        home_ownership = self.get_demographic('home_ownership')  # 'Own with mortgage'
        
        selectors = [
            f'label:has-text("Own with mortgage")',
            f'label:has-text("Mortgage")',
            f'label:has-text("Own"):has-text("mortgage")',
            f'input[type="radio"][value*="mortgage"]',
            f'option:has-text("mortgage")'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected home ownership: {home_ownership}")
                    return True
            except:
                continue
        
        return False
    
    async def handle_industry_question(self, page) -> bool:
        """Handle industry selection"""
        
        industry = self.get_demographic('industry')  # 'Retail'
        sub_industry = self.get_demographic('sub_industry')  # 'Supermarkets'
        
        # Try sub-industry first, then main industry
        selectors = [
            f'label:has-text("{sub_industry}")',
            f'option:has-text("{sub_industry}")',
            f'label:has-text("{industry}")',
            f'option:has-text("{industry}")',
            f'input[type="radio"][value*="{industry}"]'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click()
                    print(f"✅ Selected industry: {industry}/{sub_industry}")
                    return True
            except:
                continue
        
        return False
    
    async def get_question_text(self, page) -> str:
        """Extract the main question text from the page"""
        
        selectors = [
            'h1', 'h2', 'h3',
            'p:has-text("?")',
            'div[class*="question"]'
        ]
        
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and '?' in text:
                        return text
            except:
                continue
        
        return ""