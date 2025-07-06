"""
Enhanced Demographics Handler with Multi-Question Page Support
Updated with YOUR correct demographic values from knowledge base.
Enhanced with new radio button clicking methods.
FIXED: Critical null reference bug that prevented all automation.
"""

from handlers.base_handler import BaseQuestionHandler
import random
import time


class MultiQuestionPageHandler:
    """
    Handles pages with multiple questions of different types.
    Intelligently separates demographics from other question types.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        self.page = page
        self.knowledge_base = knowledge_base
        self.intervention_manager = intervention_manager
        
    def analyze_page_questions(self):
        """
        Analyze the page to identify all questions and their types.
        
        Returns:
            dict: {
                'demographics': [...],
                'multi_select': [...],
                'brand_questions': [...],
                'unknown': [...],
                'total_questions': int
            }
        """
        try:
            if not self.page:
                print("⚠️ No page available for multi-question analysis")
                return self._empty_analysis()
            
            page_content = self.page.inner_text('body')
            
            # Find all question blocks
            question_blocks = self._identify_question_blocks(page_content)
            
            # Classify each question
            classified_questions = {
                'demographics': [],
                'multi_select': [],
                'brand_questions': [],
                'rating_questions': [],
                'unknown': [],
                'total_questions': len(question_blocks)
            }
            
            for i, question_block in enumerate(question_blocks):
                question_type = self._classify_question(question_block, i + 1)
                question_info = {
                    'question_number': i + 1,
                    'text': question_block['text'],
                    'elements': question_block['elements'],
                    'type': question_type
                }
                
                classified_questions[question_type].append(question_info)
            
            return classified_questions
            
        except Exception as e:
            print(f"⚠️ Error in multi-question analysis: {e}")
            return self._empty_analysis()
    
    def _empty_analysis(self):
        """Return empty analysis structure."""
        return {
            'demographics': [],
            'multi_select': [],
            'brand_questions': [],
            'rating_questions': [],
            'unknown': [],
            'total_questions': 0
        }
    
    def _identify_question_blocks(self, page_content):
        """
        Identify individual question blocks on the page.
        """
        question_blocks = []
        
        # Look for required question indicators
        required_indicators = [
            '*', 'required', 'this question is required'
        ]
        
        # Split content into potential question areas
        lines = page_content.split('\n')
        current_block = []
        block_text = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line indicates a new question
            if any(indicator in line.lower() for indicator in required_indicators):
                if current_block:
                    # Save previous question block
                    question_blocks.append({
                        'text': block_text.strip(),
                        'elements': self._find_elements_for_question(block_text)
                    })
                    current_block = []
                    block_text = ""
                
                current_block.append(line)
                block_text += line + " "
            elif current_block:  # Continue building current question
                current_block.append(line)
                block_text += line + " "
            else:  # Standalone text that might be a question
                if '?' in line or any(word in line.lower() for word in ['select', 'choose', 'enter']):
                    current_block.append(line)
                    block_text += line + " "
        
        # Don't forget the last block
        if current_block:
            question_blocks.append({
                'text': block_text.strip(),
                'elements': self._find_elements_for_question(block_text)
            })
        
        print(f"🔍 Identified {len(question_blocks)} question blocks on page")
        for i, block in enumerate(question_blocks):
            print(f"   Question {i+1}: {block['text'][:60]}...")
        
        return question_blocks
    
    def _classify_question(self, question_block, question_number):
        """
        Classify a single question block by type.
        """
        text = question_block['text'].lower()
        
        # Demographics patterns
        demographics_patterns = [
            'age', 'gender', 'male', 'female', 'employment', 'income', 
            'education', 'location', 'postcode', 'state', 'territory', 
            'country', 'occupation', 'living situation', 'household', 
            'marital status', 'place of residence', 'current residence',
            'born', 'birth year', 'how old'
        ]
        
        # Product/Brand/Purchase patterns
        product_patterns = [
            'purchased', 'bought', 'buy', 'product', 'brand', 'chocolate',
            'consumption', 'gift', 'consume', 'shopping', 'store'
        ]
        
        # Rating/Opinion patterns
        rating_patterns = [
            'likely', 'recommend', 'satisfaction', 'agree', 'disagree',
            'rate', 'scale', 'opinion', 'think about', 'feel about'
        ]
        
        # Multi-select patterns
        multiselect_patterns = [
            'which of the following', 'select all', 'check all',
            'multiple', 'all that apply'
        ]
        
        # Count pattern matches
        demo_matches = sum(1 for pattern in demographics_patterns if pattern in text)
        product_matches = sum(1 for pattern in product_patterns if pattern in text)
        rating_matches = sum(1 for pattern in rating_patterns if pattern in text)
        multiselect_matches = sum(1 for pattern in multiselect_patterns if pattern in text)
        
        print(f"   Q{question_number} classification: demo={demo_matches}, product={product_matches}, rating={rating_matches}, multi={multiselect_matches}")
        
        # Classification logic with confidence thresholds
        if demo_matches >= 1 and product_matches == 0:
            return 'demographics'
        elif product_matches >= 1 and demo_matches <= 1:
            return 'brand_questions'
        elif rating_matches >= 1:
            return 'rating_questions'
        elif multiselect_matches >= 1:
            return 'multi_select'
        else:
            return 'unknown'
    
    def _find_elements_for_question(self, question_text):
        """
        Find form elements associated with a question.
        """
        elements = {
            'radio_buttons': [],
            'checkboxes': [],
            'dropdowns': [],
            'text_inputs': []
        }
        
        try:
            if not self.page:
                return elements
                
            # Find radio buttons
            radios = self.page.query_selector_all('input[type="radio"]')
            for radio in radios:
                elements['radio_buttons'].append(radio)
            
            # Find checkboxes
            checkboxes = self.page.query_selector_all('input[type="checkbox"]')
            for checkbox in checkboxes:
                elements['checkboxes'].append(checkbox)
            
            # Find dropdowns
            selects = self.page.query_selector_all('select')
            for select in selects:
                elements['dropdowns'].append(select)
            
            # Find text inputs
            text_inputs = self.page.query_selector_all('input[type="text"], input[type="number"]')
            for text_input in text_inputs:
                elements['text_inputs'].append(text_input)
                
        except Exception as e:
            print(f"⚠️ Error finding elements: {e}")
        
        return elements


class DemographicsHandler(BaseQuestionHandler):
    """
    Enhanced demographics handler that works with multi-question pages.
    Only handles actual demographic questions.
    Uses YOUR correct demographic values from knowledge base.
    FIXED: Critical null reference bugs.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        super().__init__(page, knowledge_base, intervention_manager)
        self.multi_question_handler = MultiQuestionPageHandler(page, knowledge_base, intervention_manager)
        
        # YOUR ACTUAL DEMOGRAPHIC VALUES from knowledge base
        self.user_demographics = {
            "age": "45",
            "birth_year": "1980", 
            "gender": "Male",
            "location": "New South Wales",
            "postcode": "2217",
            "city_suburb": "Kogarah",
            "location_type": "In a large metropolitan city",
            "urban_rural": "Urban",
            "marital_status": "Married/civil partnership",
            "household_size": "4",
            "children": "Yes",
            "pets": "Yes",
            "employment_status": "Full-time",
            "work_arrangement": "Mix of on-site and home-based",
            "education": "High school",
            "occupation_level": "Academic/Professional",
            "personal_income": "$100,000 to $149,999",
            "household_income": "$200,000 to $499,999"
        }
        
        # Location mappings for different survey formats
        self.location_mappings = {
            "New South Wales": [
                "NSW/ACT", "NSW", "New South Wales", "NSW / ACT",
                "New South Wales - Sydney", "New South Wales - regional",
                "nsw", "new south wales", "sydney"
            ],
            "Victoria": ["Victoria", "VIC", "Victoria - Melbourne", "Victoria - regional"],
            "Queensland": ["Queensland", "QLD"],
            "South Australia": ["South Australia", "SA"],
            "Western Australia": ["Western Australia", "WA"],
            "Tasmania": ["Tasmania", "TAS"],
            "Northern Territory": ["Northern Territory", "NT"],
            "ACT": ["ACT", "Australian Capital Territory", "Canberra"]
        }
    
    def can_handle(self, page_content: str) -> float:
        """
        Enhanced confidence calculation for multi-question pages.
        FIXED: Added comprehensive null safety checks and fallback logic.
        """
        try:
            # SAFETY CHECK: Ensure we have valid page content
            if not page_content:
                print("⚠️ No page content provided to demographics handler")
                return 0.0
            
            # SAFETY CHECK: Ensure page object exists
            if not hasattr(self, 'page') or self.page is None:
                print("⚠️ Page object not available in demographics handler")
                return self._fallback_confidence_calculation(page_content)
            
            # SAFETY CHECK: Ensure multi_question_handler is properly initialized
            if not hasattr(self, 'multi_question_handler') or self.multi_question_handler is None:
                print("⚠️ Multi-question handler not initialized, using fallback")
                return self._fallback_confidence_calculation(page_content)
            
            # Now safely analyze the page
            try:
                page_analysis = self.multi_question_handler.analyze_page_questions()
                
                if not page_analysis or page_analysis.get('total_questions', 0) == 0:
                    print("⚠️ No questions found in multi-question analysis, using fallback")
                    return self._fallback_confidence_calculation(page_content)
                
            except Exception as e:
                print(f"⚠️ Error in multi-question analysis: {e}")
                # FALLBACK: Use simple content analysis
                return self._fallback_confidence_calculation(page_content)
            
            demographics_count = len(page_analysis.get('demographics', []))
            total_questions = page_analysis.get('total_questions', 0)
            
            if total_questions == 0:
                return self._fallback_confidence_calculation(page_content)
            
            # Calculate confidence based on demographics ratio
            demographics_ratio = demographics_count / total_questions
            
            print(f"🔍 Multi-question analysis: {demographics_count}/{total_questions} demographics questions")
            
            # High confidence if mostly demographics
            if demographics_ratio >= 0.7:
                return 0.9
            # Medium confidence if some demographics
            elif demographics_ratio >= 0.4:
                return 0.7
            # Low confidence if few demographics
            elif demographics_ratio > 0:
                return 0.5
            else:
                # Even if no demographics found in multi-question analysis, try fallback
                return self._fallback_confidence_calculation(page_content)
                
        except Exception as e:
            print(f"❌ Critical error in demographics handler can_handle: {e}")
            # FALLBACK: Try simple pattern matching
            return self._fallback_confidence_calculation(page_content)
    
    def _fallback_confidence_calculation(self, page_content: str) -> float:
        """
        Fallback confidence calculation when multi-question analysis fails.
        This handles simple single-question demographics pages.
        """
        try:
            if not page_content:
                return 0.0
                
            content_lower = page_content.lower()
            
            # Enhanced demographics keyword matching
            demographic_keywords = [
                'age', 'gender', 'employment', 'income', 'education', 'location',
                'postcode', 'state', 'territory', 'country', 'occupation',
                'living situation', 'household', 'marital status', 'employment status',
                'place of residence', 'current residence', 'please enter your age',
                'which gender', 'what is your age', 'enter your age', 'your age',
                'male', 'female', 'which of the following regions',
                'in which country', 'enter a number'
            ]
            
            keyword_matches = sum(1 for keyword in demographic_keywords if keyword in content_lower)
            
            # Specific age question patterns (high confidence)
            age_patterns = [
                'please enter your age', 'what is your age', 'enter your age',
                'your age:', 'enter a number in the box', 'please enter a number'
            ]
            
            age_match = any(pattern in content_lower for pattern in age_patterns)
            
            # Gender question patterns
            gender_patterns = [
                'which gender', 'male', 'female', 'gender do you identify'
            ]
            
            gender_match = any(pattern in content_lower for pattern in gender_patterns)
            
            # Location question patterns  
            location_patterns = [
                'which country', 'in which of the following regions',
                'new south wales', 'victoria', 'queensland'
            ]
            
            location_match = any(pattern in content_lower for pattern in location_patterns)
            
            # Calculate confidence
            confidence = 0.0
            
            if age_match:
                confidence = 0.9  # Very high confidence for age questions
                print(f"🎯 Age question detected - high confidence")
            elif gender_match:
                confidence = 0.9  # Very high confidence for gender questions
                print(f"🎯 Gender question detected - high confidence")
            elif location_match:
                confidence = 0.9  # Very high confidence for location questions
                print(f"🎯 Location question detected - high confidence")
            elif keyword_matches >= 3:
                confidence = 0.8
                print(f"🔍 Multiple demographic keywords found: {keyword_matches}")
            elif keyword_matches >= 2:
                confidence = 0.6
                print(f"🔍 Some demographic keywords found: {keyword_matches}")
            elif keyword_matches >= 1:
                confidence = 0.4
                print(f"🔍 Few demographic keywords found: {keyword_matches}")
            else:
                confidence = 0.0
                print(f"🔍 No demographic keywords found")
            
            return confidence
            
        except Exception as e:
            print(f"❌ Error in fallback confidence calculation: {e}")
            return 0.0
    
    def handle(self) -> bool:
        """
        Handle only the demographic questions on a multi-question page.
        ENHANCED: Better handling of single-question pages and null safety.
        """
        try:
            print("🔧 Enhanced Demographics handler processing...")
            
            # SAFETY CHECK: Ensure page exists
            if not self.page:
                print("❌ No page available for demographics processing")
                return False
            
            # Try multi-question analysis first
            try:
                page_analysis = self.multi_question_handler.analyze_page_questions()
                demographics_questions = page_analysis.get('demographics', [])
                total_questions = page_analysis.get('total_questions', 0)
                
                if demographics_questions:
                    print(f"🎯 Processing {len(demographics_questions)} demographic questions out of {total_questions} total")
                    return self._handle_multi_question_demographics(demographics_questions)
                else:
                    print("🔍 No demographics found in multi-question analysis, trying single-question approach")
                    
            except Exception as e:
                print(f"⚠️ Multi-question analysis failed: {e}, trying single-question approach")
            
            # Fallback: Handle as single question
            return self._handle_single_question_demographics()
            
        except Exception as e:
            print(f"❌ Critical error in demographics handler: {e}")
            return False
    
    def _handle_multi_question_demographics(self, demographics_questions):
        """Handle multiple demographic questions on a page."""
        completed_demographics = 0
        
        for demo_question in demographics_questions:
            print(f"\n📝 Processing demographic question {demo_question['question_number']}: {demo_question['text'][:50]}...")
            
            if self._process_single_demographic_question(demo_question):
                completed_demographics += 1
                self.human_like_delay(500, 1000)
            else:
                print(f"❌ Failed to complete demographic question {demo_question['question_number']}")
        
        # Summary
        print(f"\n📊 Demographics Summary: {completed_demographics}/{len(demographics_questions)} completed")
        
        if completed_demographics > 0:
            print(f"✅ Successfully completed {completed_demographics} demographic questions")
            return True
        else:
            print(f"❌ Could not complete any demographic questions")
            return False
    
    def _handle_single_question_demographics(self):
        """Handle single demographic question on a page."""
        try:
            page_content = self.page.inner_text('body').lower()
            
            # Detect question type and handle accordingly
            if any(term in page_content for term in ['age', 'old', 'birth', 'enter your age', 'enter a number']):
                return self._handle_single_age_question()
            elif any(term in page_content for term in ['gender', 'male', 'female']):
                return self._handle_single_gender_question()
            elif any(term in page_content for term in ['country', 'regions', 'state', 'territory']):
                return self._handle_single_location_question()
            elif any(term in page_content for term in ['employment', 'work', 'job']):
                return self._handle_single_employment_question()
            elif any(term in page_content for term in ['income', 'salary', 'earn']):
                return self._handle_single_income_question()
            else:
                print(f"⚠️ Unknown single demographic question type")
                return False
                
        except Exception as e:
            print(f"❌ Error handling single question demographics: {e}")
            return False
    
    def _handle_single_age_question(self):
        """Handle single age question using direct page elements."""
        user_age = self.user_demographics["age"]  # "45"
        
        try:
            # Find text inputs for age
            text_inputs = self.page.query_selector_all('input[type="text"], input[type="number"]')
            for text_input in text_inputs:
                if self.fill_input_safely(text_input, user_age, "age"):
                    print(f"✅ Successfully filled age question with: {user_age}")
                    return True
            
            print(f"❌ Could not find age input field")
            return False
            
        except Exception as e:
            print(f"❌ Error handling single age question: {e}")
            return False
    
    def _handle_single_gender_question(self):
        """Handle single gender question using direct page elements."""
        user_gender = self.user_demographics["gender"]  # "Male"
        
        try:
            # Find radio buttons for gender
            radio_buttons = self.page.query_selector_all('input[type="radio"]')
            for radio in radio_buttons:
                label_text = self._get_radio_label_text(radio)
                if label_text and user_gender.lower() in label_text.lower():
                    if self.click_radio_button_safely(radio, f"gender: {label_text}"):
                        print(f"✅ Successfully selected gender: {user_gender}")
                        return True
            
            print(f"❌ Could not find gender radio button for: {user_gender}")
            return False
            
        except Exception as e:
            print(f"❌ Error handling single gender question: {e}")
            return False
    
    def _handle_single_location_question(self):
        """Handle single location question using direct page elements."""
        user_location = self.user_demographics["location"]  # "New South Wales"
        
        try:
            # Try radio buttons first
            radio_buttons = self.page.query_selector_all('input[type="radio"]')
            possible_matches = self.location_mappings.get(user_location, [user_location.lower()])
            
            for radio in radio_buttons:
                label_text = self._get_radio_label_text(radio)
                if label_text:
                    label_lower = label_text.lower()
                    if any(match.lower() in label_lower for match in possible_matches):
                        if self.click_radio_button_safely(radio, f"location: {label_text}"):
                            print(f"✅ Successfully selected location: {label_text}")
                            return True
            
            # Try dropdowns
            dropdowns = self.page.query_selector_all('select')
            for dropdown in dropdowns:
                for location_variant in possible_matches:
                    if self.select_dropdown_safely(dropdown, location_variant, f"location ({location_variant})"):
                        print(f"✅ Successfully selected location: {location_variant}")
                        return True
            
            print(f"❌ Could not find location option for: {user_location}")
            return False
            
        except Exception as e:
            print(f"❌ Error handling single location question: {e}")
            return False
    
    def _handle_single_employment_question(self):
        """Handle single employment question."""
        employment_status = self.user_demographics["employment_status"]  # "Full-time"
        
        try:
            radio_buttons = self.page.query_selector_all('input[type="radio"]')
            for radio in radio_buttons:
                label_text = self._get_radio_label_text(radio)
                if label_text:
                    label_lower = label_text.lower()
                    if ('full-time' in employment_status.lower() and 'full' in label_lower):
                        if self.click_radio_button_safely(radio, f"employment: {label_text}"):
                            print(f"✅ Successfully selected employment: {label_text}")
                            return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling employment question: {e}")
            return False
    
    def _handle_single_income_question(self):
        """Handle single income question."""
        personal_income = self.user_demographics["personal_income"]
        
        try:
            radio_buttons = self.page.query_selector_all('input[type="radio"]')
            for radio in radio_buttons:
                label_text = self._get_radio_label_text(radio)
                if label_text and '$100,000' in label_text and '$149,999' in label_text:
                    if self.click_radio_button_safely(radio, f"personal income: {label_text}"):
                        print(f"✅ Successfully selected income: {label_text}")
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling income question: {e}")
            return False
    
    def _process_single_demographic_question(self, question_info):
        """
        Process a single demographic question using YOUR values.
        """
        question_text = question_info['text'].lower()
        elements = question_info['elements']
        
        # Determine question type and use YOUR values
        if any(term in question_text for term in ['age', 'old', 'birth']):
            return self._handle_age_question(elements, question_text)
        elif any(term in question_text for term in ['gender', 'male', 'female']):
            return self._handle_gender_question(elements)
        elif any(term in question_text for term in ['residence', 'location', 'state', 'territory']):
            return self._handle_location_question(elements)
        elif any(term in question_text for term in ['employment', 'work', 'job']):
            return self._handle_employment_question(elements)
        elif any(term in question_text for term in ['income', 'salary', 'earn']):
            return self._handle_income_question(elements)
        elif any(term in question_text for term in ['household', 'people live', 'family']):
            return self._handle_household_question(elements)
        elif any(term in question_text for term in ['marital', 'married', 'relationship']):
            return self._handle_marital_question(elements)
        elif any(term in question_text for term in ['education', 'school', 'qualification']):
            return self._handle_education_question(elements)
        else:
            print(f"⚠️ Unknown demographic question type: {question_text[:50]}")
            return False
    
    def _handle_age_question(self, elements, question_text):
        """Handle age-related questions using YOUR age (45)."""
        user_age = self.user_demographics["age"]  # "45"
        
        # Check if it's asking for birth year
        if 'birth' in question_text or 'born' in question_text:
            birth_year = self.user_demographics["birth_year"]  # "1980"
            
            # Try text input for birth year
            if elements['text_inputs']:
                for text_input in elements['text_inputs']:
                    if self.fill_input_safely(text_input, birth_year, "birth year"):
                        return True
        
        # Try text input for age
        if elements['text_inputs']:
            for text_input in elements['text_inputs']:
                if self.fill_input_safely(text_input, user_age, "age"):
                    return True
        
        # Try dropdown for age range
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                age_range = self._get_age_range(int(user_age))  # "45-54"
                if self.select_dropdown_safely(dropdown, age_range, "age range"):
                    return True
        
        # Try radio buttons for age range
        if elements['radio_buttons']:
            return self._select_age_radio(elements['radio_buttons'], int(user_age))
        
        return False
    
    def _handle_gender_question(self, elements):
        """Handle gender selection using YOUR gender (Male)."""
        user_gender = self.user_demographics["gender"]  # "Male"
        
        # Try radio buttons
        if elements['radio_buttons']:
            return self._select_gender_radio(elements['radio_buttons'], user_gender)
        
        # Try dropdown
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                if self.select_dropdown_safely(dropdown, user_gender, "gender"):
                    return True
        
        return False
    
    def _handle_location_question(self, elements):
        """Handle location/residence questions using YOUR location (New South Wales)."""
        user_location = self.user_demographics["location"]  # "New South Wales"
        
        # Try radio buttons first (common for state selection)
        if elements['radio_buttons']:
            return self._select_location_radio(elements['radio_buttons'], user_location)
        
        # Try dropdown
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                # Try main location first
                if self.select_dropdown_safely(dropdown, user_location, "location"):
                    return True
                
                # Try mapped variations
                possible_matches = self.location_mappings.get(user_location, [])
                for location_variant in possible_matches:
                    if self.select_dropdown_safely(dropdown, location_variant, f"location ({location_variant})"):
                        return True
        
        return False
    
    def _handle_employment_question(self, elements):
        """Handle employment status using YOUR status (Full-time)."""
        employment_status = self.user_demographics["employment_status"]  # "Full-time"
        
        if elements['radio_buttons']:
            return self._select_employment_radio(elements['radio_buttons'], employment_status)
        
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                if self.select_dropdown_safely(dropdown, employment_status, "employment"):
                    return True
        
        return False
    
    def _handle_income_question(self, elements):
        """Handle income questions using YOUR income ranges."""
        personal_income = self.user_demographics["personal_income"]  # "$100,000 to $149,999"
        household_income = self.user_demographics["household_income"]  # "$200,000 to $499,999"
        
        # Try radio buttons for income ranges
        if elements['radio_buttons']:
            return self._select_income_radio(elements['radio_buttons'], personal_income, household_income)
        
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                # Try personal income first
                if self.select_dropdown_safely(dropdown, personal_income, "personal income"):
                    return True
                # Try household income
                if self.select_dropdown_safely(dropdown, household_income, "household income"):
                    return True
        
        return False
    
    def _handle_household_question(self, elements):
        """Handle household questions using YOUR household info."""
        household_size = self.user_demographics["household_size"]  # "4"
        
        if elements['text_inputs']:
            for text_input in elements['text_inputs']:
                if self.fill_input_safely(text_input, household_size, "household size"):
                    return True
        
        if elements['radio_buttons']:
            return self._select_household_radio(elements['radio_buttons'], household_size)
        
        return False
    
    def _handle_marital_question(self, elements):
        """Handle marital status using YOUR status."""
        marital_status = self.user_demographics["marital_status"]  # "Married/civil partnership"
        
        if elements['radio_buttons']:
            return self._select_marital_radio(elements['radio_buttons'], marital_status)
        
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                if self.select_dropdown_safely(dropdown, marital_status, "marital status"):
                    return True
        
        return False
    
    def _handle_education_question(self, elements):
        """Handle education questions using YOUR education level."""
        education = self.user_demographics["education"]  # "High school"
        
        if elements['radio_buttons']:
            return self._select_education_radio(elements['radio_buttons'], education)
        
        if elements['dropdowns']:
            for dropdown in elements['dropdowns']:
                if self.select_dropdown_safely(dropdown, education, "education"):
                    return True
        
        return False
    
    # Enhanced radio button selection methods with YOUR values - UPDATED TO USE NEW METHOD
    
    def _select_gender_radio(self, radio_buttons, target_gender):
        """Select appropriate gender radio button using enhanced method."""
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text and target_gender.lower() in label_text.lower():
                    return self.click_radio_button_safely(radio, f"gender: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_location_radio(self, radio_buttons, target_location):
        """Select appropriate location radio button using YOUR location mappings."""
        possible_matches = self.location_mappings.get(target_location, [target_location.lower()])
        
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text:
                    label_lower = label_text.lower()
                    if any(match.lower() in label_lower for match in possible_matches):
                        return self.click_radio_button_safely(radio, f"location: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_employment_radio(self, radio_buttons, employment_status):
        """Select employment radio using YOUR status."""
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text:
                    label_lower = label_text.lower()
                    # Match "Full-time" with various formats
                    if ('full-time' in employment_status.lower() and 'full' in label_lower) or \
                       ('30 or more hours' in label_lower) or \
                       ('full time' in label_lower):
                        return self.click_radio_button_safely(radio, f"employment: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_income_radio(self, radio_buttons, personal_income, household_income):
        """Select income radio using YOUR income ranges."""
        # Try personal income first
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text and '$100,000' in label_text and '$149,999' in label_text:
                    return self.click_radio_button_safely(radio, f"personal income: {label_text}")  # UPDATED METHOD
                elif label_text and '$200,000' in label_text and '$499,999' in label_text:
                    return self.click_radio_button_safely(radio, f"household income: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_household_radio(self, radio_buttons, household_size):
        """Select household size radio."""
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text and household_size in label_text:
                    return self.click_radio_button_safely(radio, f"household size: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_marital_radio(self, radio_buttons, marital_status):
        """Select marital status radio."""
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text:
                    label_lower = label_text.lower()
                    if 'married' in marital_status.lower() and 'married' in label_lower:
                        return self.click_radio_button_safely(radio, f"marital status: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_education_radio(self, radio_buttons, education):
        """Select education radio."""
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text:
                    label_lower = label_text.lower()
                    if 'high school' in education.lower() and 'high school' in label_lower:
                        return self.click_radio_button_safely(radio, f"education: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    def _select_age_radio(self, radio_buttons, age):
        """Select age range radio button using enhanced method."""
        age_range = self._get_age_range(age)
        
        for radio in radio_buttons:
            try:
                label_text = self._get_radio_label_text(radio)
                if label_text and age_range in label_text:
                    return self.click_radio_button_safely(radio, f"age range: {label_text}")  # UPDATED METHOD
            except:
                continue
        return False
    
    # Helper methods remain the same
    def _get_radio_label_text(self, radio_element):
        """Get the label text for a radio button."""
        try:
            # Try associated label first
            radio_id = radio_element.get_attribute('id')
            if radio_id:
                label = self.page.query_selector(f"label[for='{radio_id}']")
                if label:
                    return label.inner_text().strip()
            
            # Try parent element text
            parent = radio_element.locator('..')
            if parent:
                text = parent.inner_text().strip()
                return text
            
            return ""
        except:
            return ""
    
    def _get_age_range(self, age):
        """Convert YOUR age (45) to appropriate range."""
        if age < 25:
            return "18-24"
        elif age < 35:
            return "25-34"
        elif age < 45:
            return "35-44"
        elif age < 55:
            return "45-54"  # YOUR age range
        elif age < 65:
            return "55-64"
        else:
            return "65+"