# quenito_learning_with_automation.py
"""
Complete integrated learning system with enhanced capture AND automation
NOW WITH VISION! 👁️
ALL FIXES APPLIED - v2.0
"""

import asyncio
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from core.stealth_browser_manager import StealthBrowserManager
from data.knowledge_base import KnowledgeBase
from data.confidence_manager import ConfidenceManager
from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter
from vision_mvp import QuenitoVision 
from handlers.multi_question import MultiQuestionHandler, MultiQuestionUI, MultiQuestionBrain
from reporting.quenito_reporting import QuenitoReporting

# Import handlers and factory
from handler_adapter import create_simple_handlers  # Our simple adapter

class IntegratedLearningCapture:
    """Learning capture that integrates with existing confidence system"""
    
    def __init__(self, knowledge_base: KnowledgeBase, confidence_manager: ConfidenceManager):
        self.kb = knowledge_base
        self.cm = confidence_manager
        self.session_id = f"learning_session_{int(time.time())}"
        self.start_time = time.time()
        self.vision = QuenitoVision(platform="myopinions") # Initialize vision!
        
        # Ensure detailed_intervention_learning exists
        if 'detailed_intervention_learning' not in self.kb.data:
            self.kb.data['detailed_intervention_learning'] = {}
    
    async def capture_and_learn(self, page, question_number: int, vision_result: Dict = None) -> Dict[str, Any]:
        """Capture question details and create learning entry - NOW WITH VISION GUIDANCE!"""
        
        capture_start = time.time()
        
        # Extract comprehensive details
        question_data = await self._extract_comprehensive_details(page)
        
        # ENHANCE with vision data if available
        if vision_result:
            # Override/enhance with vision insights
            if vision_result.get('question_text'):
                question_data['question_text'] = vision_result['question_text']
            if vision_result.get('question_type'):
                # Map vision types to our types
                vision_type_map = {
                    'checkbox': 'multi_select',
                    'radio': question_data['question_type'],  # Keep our classification
                    'dropdown': 'select',
                    'text': 'text',
                    'matrix': 'rating_matrix'
                }
                mapped_type = vision_type_map.get(vision_result['question_type'], vision_result['question_type'])
                question_data['question_type'] = mapped_type
                question_data['vision_type'] = vision_result['question_type']
            
            # Store vision confidence
            question_data['vision_confidence'] = vision_result.get('confidence_rating', 0)
        
        # Determine strategy that would be used
        strategy = self._determine_strategy(question_data)
        
        # Get confidence for this question type
        handler_name = self._get_handler_name(question_data['question_type'])
        confidence = self.cm.get_dynamic_threshold(
            handler_name, 
            question_data['question_type']
        )
        
        # BOOST confidence if vision is confident!
        if vision_result and vision_result.get('confidence_rating', 0) > 85:
            confidence = min(confidence + 0.1, 0.95)  # Boost by 10%
        
        # Create detailed learning entry
        learning_key = f"learning_{int(time.time())}_{question_number}"
        learning_entry = {
            "timestamp": time.time(),
            "session_id": self.session_id,
            "question_number": question_number,
            "question_text": question_data['question_text'],
            "question_type": question_data['question_type'],
            "strategy_used": strategy,
            "execution_time": time.time() - capture_start,
            "confidence_score": confidence,
            "response_value": question_data['user_response'],
            "response_values": question_data.get('user_responses', []),
            "result": "MANUAL_LEARNING",
            "element_type": question_data['element_type'],
            "input_strategy": question_data['input_strategy'],
            "age_format": question_data.get('page_structure', {}).get('age_format'),
            "automation_success": False,
            "learned_at": time.time(),
            "url": page.url,
            "page_structure": question_data.get('page_structure', {}),
            # NEW VISION FIELDS
            "vision_confidence": question_data.get('vision_confidence', 0),
            "vision_type": question_data.get('vision_type', ''),
            "has_vision_analysis": vision_result is not None
        }
        
        # Store in detailed_intervention_learning
        self.kb.data['detailed_intervention_learning'][learning_key] = learning_entry
        
        # Update learning patterns
        self._update_learning_patterns(question_data, learning_entry)
        
        # Record in confidence manager
        self.cm.record_automation_result(
            handler_name,
            question_data['question_type'],
            confidence,
            True,  # Manual success
            {"element_type": question_data['element_type']}
        )
        
        # Save immediately
        self.kb.save()
        
        return learning_entry
    
    # ... [KEEP ALL YOUR EXISTING METHODS] ...
    
    async def _extract_comprehensive_details(self, page) -> Dict[str, Any]:
        """Extract all question details from the page"""
        
        details = {
            'question_text': '',
            'question_type': '',
            'element_type': '',
            'input_strategy': '',
            'user_response': '',
            'user_responses': [],
            'page_structure': {}
        }
        
        # Extract question text
        question_text = await self._find_question_text(page)
        details['question_text'] = question_text
        
        # Detect question type
        details['question_type'] = self._classify_question_type(question_text)
        
        # Analyze input elements with question context
        input_analysis = await self._analyze_inputs_for_question(page, question_text)
        details['element_type'] = input_analysis['primary_type']
        details['input_strategy'] = input_analysis['strategy']
        details['page_structure'] = input_analysis
        
        # Capture user selections with ENHANCED METHOD
        user_data = await self._capture_user_selections(page, input_analysis)
        details['user_response'] = user_data.get('primary_value', '')
        details['user_responses'] = user_data.get('all_values', [])
        
        return details
    
    async def _capture_user_selections(self, page, input_analysis: Dict) -> Dict[str, Any]:
        """Enhanced capture method for all form element types"""
        
        captured_data = {
            'primary_value': '',
            'all_values': []
        }
        
        try:
            # Radio buttons - check multiple attributes
            radio_elements = await page.query_selector_all('input[type="radio"]:checked')
            if radio_elements:
                for radio in radio_elements:
                    # Try multiple methods to get the value
                    value = await radio.get_attribute('value')
                    if not value:
                        # Try getting label text
                        label = await page.query_selector(f'label[for="{await radio.get_attribute("id")}"]')
                        if label:
                            value = await label.inner_text()
                        else:
                            # Try parent label
                            parent = await radio.evaluate('(el) => el.closest("label")')
                            if parent:
                                value = await page.evaluate('(el) => el.textContent.trim()', parent)
                    
                    if value:
                        captured_data['all_values'].append(value.strip())
                        print(f"  ✓ Captured radio selection: {value.strip()}")
            
            # Checkboxes - fix the capture issue
            checkbox_elements = await page.query_selector_all('input[type="checkbox"]')
            checked_count = 0
            for checkbox in checkbox_elements:
                is_checked = await checkbox.is_checked()
                if is_checked:
                    checked_count += 1
                    # Get value or label
                    value = await checkbox.get_attribute('value')
                    if not value or value == 'on':
                        # Try label
                        checkbox_id = await checkbox.get_attribute('id')
                        if checkbox_id:
                            label = await page.query_selector(f'label[for="{checkbox_id}"]')
                            if label:
                                value = await label.inner_text()
                        
                        # Try parent label
                        if not value:
                            value = await checkbox.evaluate('''(el) => {
                                const label = el.closest('label');
                                if (label) return label.textContent.trim();
                                // Try next sibling
                                const nextSib = el.nextElementSibling;
                                if (nextSib && nextSib.tagName === 'LABEL') return nextSib.textContent.trim();
                                return '';
                            }''')
                    
                    if value and value != 'on':
                        captured_data['all_values'].append(value.strip())
                        print(f"  ✓ Captured: {value.strip()}")
            
            if checkbox_elements:
                print(f"📦 Found {checked_count} checked boxes")
            
            # Text inputs - enhanced capture
            text_inputs = await page.query_selector_all('input[type="text"], input[type="number"], input:not([type]), textarea')
            for text_input in text_inputs:
                # Check if visible and has value
                is_visible = await text_input.is_visible()
                if is_visible:
                    # Try multiple ways to get value
                    value = await text_input.input_value()  # Better than get_attribute('value')
                    if not value:
                        value = await text_input.evaluate('(el) => el.value')
                    
                    if value:
                        captured_data['all_values'].append(value.strip())
                        print(f"  ✓ Captured text: {value.strip()}")
            
            # Dropdowns
            select_elements = await page.query_selector_all('select')
            for select in select_elements:
                selected_option = await select.evaluate('''(sel) => {
                    const option = sel.options[sel.selectedIndex];
                    return option ? option.text : '';
                }''')
                if selected_option:
                    captured_data['all_values'].append(selected_option.strip())
                    print(f"  ✓ Captured dropdown: {selected_option.strip()}")
            
            # Set primary value
            if captured_data['all_values']:
                captured_data['primary_value'] = captured_data['all_values'][0]
            
            # Summary
            print(f"📊 Total captured: {len(captured_data['all_values'])} values")
            
        except Exception as e:
            print(f"⚠️ Capture error: {str(e)}")
        
        return captured_data
    
    async def _analyze_inputs(self, page) -> Dict[str, Any]:
        """Enhanced input analysis with better type detection - FIXED FOR CHECKBOXES"""
        
        analysis = {
            'primary_type': 'unknown',
            'strategy': 'unknown_strategy',
            'elements': {
                'radio': 0,
                'checkbox': 0,
                'text': 0,
                'select': 0,
                'textarea': 0
            }
        }
        
        try:
            # Count each type
            analysis['elements']['radio'] = len(await page.query_selector_all('input[type="radio"]'))
            analysis['elements']['checkbox'] = len(await page.query_selector_all('input[type="checkbox"]'))
            analysis['elements']['text'] = len(await page.query_selector_all('input[type="text"], input[type="number"], input:not([type])'))
            analysis['elements']['select'] = len(await page.query_selector_all('select'))
            analysis['elements']['textarea'] = len(await page.query_selector_all('textarea'))
            
            # Determine primary type - FIXED to properly identify checkboxes
            max_count = max(analysis['elements'].values())
            if max_count > 0:
                # Prioritize checkbox if present and significant
                if analysis['elements']['checkbox'] > 0 and analysis['elements']['checkbox'] >= max_count - 1:
                    analysis['primary_type'] = 'checkbox'
                else:
                    for elem_type, count in analysis['elements'].items():
                        if count == max_count:
                            analysis['primary_type'] = elem_type
                            break
            
            # Set strategy based on type
            strategy_map = {
                'radio': 'radio_selection',
                'checkbox': 'checkbox_multi_select',
                'text': 'fill_strategy',
                'select': 'dropdown_selection',
                'textarea': 'fill_strategy'
            }
            
            analysis['strategy'] = strategy_map.get(analysis['primary_type'], 'unknown_strategy')
            
        except Exception as e:
            print(f"⚠️ Analysis error: {str(e)}")
        
        return analysis
    
    async def _analyze_inputs_for_question(self, page, question_text: str) -> Dict[str, Any]:
        """
        Enhanced input analysis that handles both text and radio age questions
        """
        
        analysis = {
            'primary_type': 'unknown',
            'strategy': 'unknown_strategy',
            'elements': {},
            'age_format': None  # 'text' or 'radio_range'
        }
        
        text_lower = question_text.lower()
        
        # AGE QUESTIONS - Check format - MORE SPECIFIC
        if any(phrase in text_lower for phrase in ['your age', 'how old are you', 'year were you born', 'your birth']):
            # First, check if there are age range radio buttons
            age_range_found = False
            
            # Age range patterns from universal detector
            age_ranges = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+', 
                          '18 to 24', '25 to 34', '35 to 44', '45 to 54', '55 to 64',
                          'under 18', 'over 65', '65 and over']
            
            # Check page content for age ranges
            try:
                page_text = await page.inner_text('body')
                for age_range in age_ranges:
                    if age_range in page_text:
                        age_range_found = True
                        break
            except:
                pass
            
            if age_range_found:
                # This is a radio button age question
                analysis['primary_type'] = 'radio'
                analysis['strategy'] = 'radio_selection'
                analysis['age_format'] = 'radio_range'
                print("🎯 Detected AGE RANGE radio buttons")
            else:
                # This is a text input age question
                analysis['primary_type'] = 'text'
                analysis['strategy'] = 'fill_strategy'
                analysis['age_format'] = 'text'
                print("🎯 Detected AGE text input")
            
            return analysis
        
        # GENDER QUESTIONS - Always radio - MORE SPECIFIC
        elif any(phrase in text_lower for phrase in ['your gender', 'are you male', 'are you female']):
            analysis['primary_type'] = 'radio'
            analysis['strategy'] = 'radio_selection'
            return analysis
        
        # POSTCODE - Always text
        elif any(word in text_lower for word in ['postcode', 'postal', 'zip']):
            analysis['primary_type'] = 'text'
            analysis['strategy'] = 'fill_strategy'
            return analysis
        
        # STATE/REGION - Usually dropdown
        elif any(word in text_lower for word in ['state', 'region', 'territory']):
            analysis['primary_type'] = 'select'
            analysis['strategy'] = 'dropdown_selection'
            return analysis
        
        # Fall back to counting method
        return await self._analyze_inputs(page)
    
    async def _find_question_text(self, page) -> str:
        """Extract the actual question text"""
        
        # Try multiple selectors
        selectors = [
            'h2:has-text("?")',
            'h3:has-text("?")',
            'label:has-text("?")',
            'p:has-text("?")',
            '.question-text',
            'legend',
            'fieldset > :first-child'
        ]
        
        for selector in selectors:
            try:
                elem = await page.query_selector(selector)
                if elem:
                    text = await elem.inner_text()
                    if len(text) > 10:
                        return text.strip()
            except:
                continue
        
        # Fallback: find text before inputs
        try:
            body_text = await page.inner_text('body')
            lines = [line.strip() for line in body_text.split('\n') if line.strip()]
            
            for line in lines:
                if '?' in line and len(line) > 10:
                    return line
        except:
            pass
        
        return "Question text not found"
    
    def _classify_question_type(self, question_text: str) -> str:
        """Classify question type based on text - FIXED TO BE MORE SPECIFIC"""
        
        text_lower = question_text.lower()
        
        # Brand/Product questions - CHECK THESE FIRST
        if 'brands' in text_lower or 'brand' in text_lower:
            if any(word in text_lower for word in ['committed', 'improving', 'safety', 'support', 'platforms']):
                return 'multi_select'  # Brand opinion questions
            else:
                return 'brand_awareness'
        
        # Multi-select patterns - CHECK BEFORE DEMOGRAPHICS
        elif any(phrase in text_lower for phrase in ['which of the following', 'select all', 'select as many']):
            return 'multi_select'
        
        # Demographics - MORE SPECIFIC, check for personal questions only
        elif any(phrase in text_lower for phrase in ['your age', 'how old are you', 'year were you born', 'your birth']):
            return 'age'
        elif any(phrase in text_lower for phrase in ['your gender', 'are you male', 'are you female']):
            return 'gender'
        elif any(word in text_lower for word in ['income', 'salary', 'earn', 'household income']) and 'your' in text_lower:
            return 'income'
        elif any(word in text_lower for word in ['postcode', 'postal', 'zip', 'post code']):
            return 'postcode'
        elif any(word in text_lower for word in ['occupation', 'work', 'employment', 'job']) and 'your' in text_lower:
            return 'occupation'
        
        # Rating questions
        elif any(word in text_lower for word in ['rate', 'rating', 'satisfaction', 'experience']):
            return 'rating_scale'
        
        return 'general'
    
    def _determine_strategy(self, question_data: Dict) -> str:
        """Determine the strategy based on element type"""
        return question_data.get('input_strategy', 'unknown_strategy')
    
    def _get_handler_name(self, question_type: str) -> str:
        """Map question type to handler name"""
        
        if question_type in ['age', 'gender', 'income', 'postcode', 'occupation']:
            return 'demographics'
        elif question_type in ['brand_awareness', 'brand_familiarity']:
            return 'brand_familiarity'
        elif question_type == 'rating_scale':
            return 'rating_matrix'
        elif question_type == 'multi_select':
            return 'multi_select'
        else:
            return 'general'
    
    def _update_learning_patterns(self, question_data: Dict, learning_entry: Dict):
        """Update learning patterns in knowledge base"""
        
        # Create pattern key
        pattern_key = f"{learning_entry['question_type']}_{question_data['element_type']}"
        
        # Update successful combinations
        if 'learning_patterns' not in self.kb.data['confidence_system']:
            self.kb.data['confidence_system']['learning_patterns'] = {
                'successful_combinations': {},
                'failure_patterns': {}
            }
        
        patterns = self.kb.data['confidence_system']['learning_patterns']['successful_combinations']
        
        if pattern_key not in patterns:
            patterns[pattern_key] = {
                'pattern': f"{learning_entry['question_type']} + {question_data['element_type']}",
                'confidence_boost': 0.05,
                'success_rate': 1.0,
                'sample_size': 1
            }
        else:
            # Update existing pattern
            pattern = patterns[pattern_key]
            pattern['sample_size'] += 1
            # Increase confidence boost with more samples
            if pattern['sample_size'] >= 5:
                pattern['confidence_boost'] = min(0.15, 0.05 + pattern['sample_size'] * 0.01)


async def run_integrated_learning():
    """Main learning session with integrated capture AND automation"""
    
    print("🧠 QUENITO INTEGRATED LEARNING SYSTEM - WITH VISION! 👁️")
    print("="*50)
    
    # Initialize systems
    kb = KnowledgeBase()
    cm = ConfidenceManager(kb.data.get('confidence_system', {}))
    learner = IntegratedLearningCapture(kb, cm)
    
    # 📊 INITIALIZE REPORTING SYSTEM
    reporter = QuenitoReporting()
    reporter.start_session(f"myopinions_{datetime.now().strftime('%H%M')}")
    
    # 📊 TRACKING VARIABLES
    survey_start_time = time.time()
    vision_calls_count = 0
    pattern_matches_count = 0
    survey_topic = "General"  # Will try to detect
    survey_points = 0  # Will extract at the end
    question_num = 0
    automated_count = 0

    # Create simple handlers for automation
    handlers = create_simple_handlers(kb)
    
    # Initialize browser
    browser = StealthBrowserManager("quenito_myopinions")
    await browser.initialize_stealth_browser(transfer_cookies=False)
    await browser.load_saved_cookies()
    
    # Get browser context for tab management
    context = browser.browser.contexts[0]  # Get first context
    
    # Navigate to MyOpinions
    await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
    
    print("\n📋 SETUP:")
    print("1. Login if needed")
    print("2. Close popups")
    
    input("\n✅ Press Enter when ready >>> ")
    
    # Handle popups manually
    print("\n🎯 Checking for popups/overlays...")
    
    popup_selectors = [
        'button:has-text("No Thanks")',
        'button:has-text("Close")',
        '[class*="modal-close"]',
        'button[class*="close"]',
        'a[class*="close"]',
        'button:has-text("X")'
    ]
    
    for selector in popup_selectors:
        try:
            elements = await browser.page.query_selector_all(selector)
            for element in elements:
                if await element.is_visible():
                    await element.click()
                    await browser.page.wait_for_timeout(500)
        except:
            continue
    
    print("✅ Popup handling complete")
    await browser.page.wait_for_timeout(2000)
    
    # Find surveys
    print("\n🔍 Finding shortest survey...")
    adapter = MyOpinionsAdapter(browser)
    surveys = await adapter.detect_available_surveys()
    
    if not surveys:
        print("❌ No surveys found!")
        return
    
    # Select shortest survey
    def parse_time_to_minutes(time_str):
        """Parse survey time string to minutes"""
        time_str = time_str.lower()
        if 'min' in time_str:
            # Extract number before 'min'
            import re
            match = re.search(r'(\d+)\s*min', time_str)
            if match:
                return int(match.group(1))
        return 99  # Default high value
    
    shortest = min(surveys, key=lambda s: parse_time_to_minutes(s['time']))
    print(f"\n✅ Selected: {shortest['time']} survey")
    
    # Click survey and wait for new tab
    await browser.page.click(f'a[href="{shortest["url"]}"]')
    print("⏳ Waiting for survey to load...")
    
    # Wait for new tab to open
    print("\n📑 Waiting for survey tab to open...")
    for attempt in range(5):
        await asyncio.sleep(3)
        all_pages = context.pages
        print(f"\n📑 Attempt {attempt + 1}: Found {len(all_pages)} tabs open")
        
        for i, page in enumerate(all_pages, 1):
            print(f"  📄 Tab {i}: {page.url[:80]}...")
        
        if len(all_pages) >= 2:
            # Survey tab is usually the last one
            survey_page = all_pages[-1]
            if 'survey' in survey_page.url or 'ssisurveys' in survey_page.url:
                print(f"✅ Switched to survey tab: {survey_page.url[:80]}...")
                break
        
        if attempt == 4:
            print("⏳ No survey tab found yet, waiting...")
    else:
        print("❌ Survey tab didn't open!")
        return
    
    # Handle survey flow
    print("\n🔄 Detecting survey flow...")
    
    # Check for intermediate page with start button
    for flow_attempt in range(5):
        print(f"\n🔍 Flow attempt {flow_attempt + 1} - Current URL: {survey_page.url[:80]}...")
        
        # Look for start button on intermediate page
        start_buttons = [
            'button:has-text("START SURVEY NOW")',
            'button:has-text("Start Survey Now")', 
            'button:has-text("Start Survey")',
            'a:has-text("START")',
            'button.btn-primary'
        ]
        
        clicked = False
        for selector in start_buttons:
            try:
                if await survey_page.query_selector(selector):
                    await survey_page.click(selector)
                    print("✅ Clicked survey start button")
                    clicked = True
                    break
            except:
                continue
        
        if clicked:
            await survey_page.wait_for_timeout(3000)
        
        # Check if we're at main survey questions
        page_text = await survey_page.inner_text('body')
        if any(indicator in page_text.lower() for indicator in ['question', 'please select', 'which of', 'how do you']):
            print("✅ Main survey questions detected!")
            break
            
        await survey_page.wait_for_timeout(2000)
    else:
        print("⚠️ Could not detect survey questions, continuing anyway...")
    
    print("\n🧠 ACTIVE LEARNING MODE WITH AUTOMATION + VISION!")
    print("="*50)
    print("🚀 Quenito will attempt automation when confident!")
    print("👁️ Vision system will guide detection and capture!")
    print("="*50)
    
    # MAIN LOOP WITH EXCEPTION HANDLING
    try:
        while True:
            question_num += 1
            
            print(f"\n❓ QUESTION {question_num}")
            print("-"*50)
            
            # 👁️ VISION ANALYSIS FIRST!
            screenshot_path = f"vision_data/question_{question_num}_{int(time.time())}.png"
            await survey_page.screenshot(path=screenshot_path)
            
            print("\n👁️ VISION ANALYSIS...")
            vision_result = await learner.vision.analyze_screenshot(screenshot_path)
            vision_calls_count += 1 
            
            # Parse vision result
            if isinstance(vision_result, dict):
                if 'raw_response' in vision_result:
                    print("📝 Parsing vision response...")
                    # Try to extract key info from raw response
                    raw = vision_result.get('raw_response', '')
                    vision_confidence = 70  # Default moderate confidence
                else:
                    vision_confidence = vision_result.get('confidence_rating', vision_result.get('confidence', 0))
                
                print(f"👁️ Vision Type: {vision_result.get('question_type', 'unknown')}")
                print(f"👁️ Vision Confidence: {vision_confidence}%")
                if vision_result.get('question_text'):
                    print(f"👁️ Question: {vision_result['question_text'][:80]}...")
            else:
                vision_result = {}
                vision_confidence = 0
            
            # Check for multi-question page FIRST
            if MultiQuestionBrain.is_multi_question(vision_result):
                print("🔍 MULTI-QUESTION PAGE DETECTED!")
                
                mq_handler = MultiQuestionHandler(kb)
                confidence = mq_handler.calculate_confidence(vision_result)
                
                print(f"📊 Multi-Question Confidence: {confidence:.3f}")
                
                if confidence >= 0.60:  # Lower threshold for multi-question
                    print("🚀 ATTEMPTING MULTI-QUESTION AUTOMATION...")
                    
                    response = mq_handler.handle(vision_result)
                    
                    if response.success and response.responses:
                        print(f"📝 Generated {len(response.responses)} responses")
                        
                        # Apply all responses
                        success = await MultiQuestionUI.apply_responses(
                            survey_page, 
                            response.responses
                        )
                        
                        if success:
                            automated_count += 1
                            print(f"✅ MULTI-QUESTION AUTOMATED! (Total: {automated_count}) 🎉")
                            
                            # Store pattern
                            if vision_confidence > 80:
                                pattern_id = await learner.vision.store_pattern(
                                    screenshot_path,
                                    vision_result,
                                    {
                                        'responses': response.responses,
                                        'success': True,
                                        'type': 'multi_question'
                                    }
                                )
                                print(f"💾 Stored multi-question pattern: {pattern_id}")
                            
                            # Click next and continue to next iteration
                            await survey_page.wait_for_timeout(1000)
                            await survey_page.click('button:has-text("Next"), button:has-text("Continue")')
                            await survey_page.wait_for_timeout(1000)
                            
                            # Check for completion - ENHANCED
                            try:
                                new_content = await survey_page.inner_text('body')
                                completion_indicators = [
                                    'thank you', 'thanks for completing', 'survey complete',
                                    'points have been added', 'points earned', 'congratulations',
                                    'survey has been completed', 'successfully completed',
                                    'reward', 'credited to your account'
                                ]
                                
                                if any(indicator in new_content.lower() for indicator in completion_indicators):
                                    print("\n🎉 SURVEY COMPLETE!")
                                    
                                    # Extract points
                                    try:
                                        points_match = re.search(r'(\d+)\s*points?', new_content.lower())
                                        if points_match:
                                            survey_points = int(points_match.group(1))
                                            print(f"💰 Points earned: {survey_points}")
                                    except:
                                        survey_points = 100
                                    
                                    # 📊 LOG THE COMPLETED SURVEY
                                    survey_duration = int(time.time() - survey_start_time)
                                    
                                    reporter.log_survey_completion(
                                        platform="MyOpinions",
                                        survey_id=f"survey_{int(time.time())}",
                                        topic=survey_topic,
                                        points=survey_points,
                                        duration_seconds=survey_duration,
                                        questions_total=question_num,
                                        questions_automated=automated_count,
                                        vision_api_calls=vision_calls_count,
                                        pattern_matches=pattern_matches_count
                                    )
                                    
                                    reporter.print_session_report()
                                    break
                            except:
                                pass
                            
                            continue  # Skip to next question (important!)
                        else:
                            print("⚠️ Some fields couldn't be automated, falling back to single-question logic")
                else:
                    print("📝 Multi-question confidence too low, falling back to single-question logic")

            # Analyze question with DOM methods
            question_data = await learner._extract_comprehensive_details(survey_page)
            handler_name = learner._get_handler_name(question_data['question_type'])
            
            # ENHANCE with vision insights
            if vision_confidence > 70:
                print("✨ Enhancing with vision insights...")
                if vision_result.get('question_text') and len(vision_result['question_text']) > len(question_data['question_text']):
                    question_data['question_text'] = vision_result['question_text']
            
            # Check automation possibility
            handler = handlers.get(handler_name)
            if handler:
                confidence = handler.calculate_confidence(
                    question_data['question_type'],
                    question_data['question_text']
                )
                
                # BOOST confidence if vision agrees!
                if vision_confidence > 80:
                    confidence = min(confidence + 0.15, 0.95)
                    print(f"🚀 Vision boost: +15% confidence!")
                
                threshold = learner.cm.get_dynamic_threshold(handler_name, question_data['question_type'])
                should_automate, reason = learner.cm.should_attempt_automation(
                    handler_name, confidence, question_data['question_type']
                )
                
                print(f"\n🤖 AUTOMATION CHECK:")
                print(f"   Handler: {handler_name}")
                print(f"   Type: {question_data['question_type']}")
                print(f"   Element: {question_data['element_type']}")
                print(f"   Vision says: {vision_result.get('question_type', 'unknown')} ({vision_confidence}%)")
                if question_data['question_type'] == 'age' and 'age_format' in question_data.get('page_structure', {}):
                    print(f"   Age Format: {question_data['page_structure']['age_format']}")
                print(f"   Confidence: {confidence:.3f} vs Threshold: {threshold:.3f}")
                print(f"   Decision: {'✅ AUTOMATE!' if should_automate else '❌ Manual'}")
                print(f"   Reason: {reason}")
                
                if should_automate and confidence >= threshold:
                    print("\n🚀 ATTEMPTING AUTOMATION...")
                    
                    try:
                        # Get automated response with element type awareness
                        response = handler.handle(question_data['question_text'], question_data['element_type'])
                        
                        if response and response.response_value:
                            print(f"🎯 AUTO-RESPONSE: {response.response_value}")
                            print("⏳ Applying response to form...")
                            
                            # Apply based on element type
                            success = False
                            
                            if question_data['element_type'] == 'radio':
                                # Handle different types of radio questions
                                if 'age' in question_data['question_text'].lower():
                                    # Age range radio buttons
                                    print(f"🎯 Selecting age range: {response.response_value}")
                                    
                                    # Try multiple selectors for age ranges
                                    selectors = [
                                        f'label:has-text("{response.response_value}")',
                                        f'input[type="radio"][value="{response.response_value}"]',
                                        f'label:has-text("{response.response_value.replace("-", " to ")}")',  # "45-54" → "45 to 54"
                                        f'span:has-text("{response.response_value}") input[type="radio"]',
                                        f'label:has-text("{response.response_value.replace("-", " - ")}")'  # "45-54" → "45 - 54"
                                    ]
                                    
                                    for selector in selectors:
                                        try:
                                            await survey_page.click(selector)
                                            print(f"✅ Selected age range using: {selector}")
                                            success = True
                                            break
                                        except:
                                            continue
                                            
                                    if not success:
                                        print("⚠️ Could not find age range radio button")
                                else:
                                    # Regular radio buttons (gender, etc.)
                                    try:
                                        await survey_page.click(f'input[type="radio"][value="{response.response_value}"]')
                                        success = True
                                    except:
                                        try:
                                            # Try clicking by label text
                                            await survey_page.click(f'label:has-text("{response.response_value}")')
                                            success = True
                                        except:
                                            print("⚠️ Could not find radio button to click")
                                        
                            elif question_data['element_type'] in ['text_input', 'text']:
                                # Fill visible text input - enhanced for age fields
                                try:
                                    # Try specific selectors for age inputs
                                    if 'age' in question_data['question_text'].lower():
                                        filled = False
                                        age_selectors = [
                                            'input[placeholder="Number"]',
                                            'input[placeholder*="Number"]',
                                            'input[type="number"]:visible',
                                            'fieldset:has-text("age") input[type="text"]'
                                        ]
                                        for selector in age_selectors:
                                            try:
                                                await survey_page.fill(selector, str(response.response_value))
                                                filled = True
                                                success = True
                                                break
                                            except:
                                                continue
                                        
                                        if not filled:
                                            # Fallback to general input
                                            await survey_page.fill('input[type="text"]:visible, input[type="number"]:visible', str(response.response_value))
                                            success = True
                                    else:
                                        # General text input
                                        await survey_page.fill('input[type="text"]:visible, input[type="number"]:visible, input:not([type]):visible', str(response.response_value))
                                        success = True
                                except:
                                    print("⚠️ Could not find text input to fill")
                                    
                            elif question_data['element_type'] == 'checkbox':
                                # FIXED - Check if response is a number
                                if response.response_value.isdigit():
                                    print(f"⚠️ Got index ({response.response_value}) instead of text, skipping automation")
                                    success = False
                                else:
                                    try:
                                        await survey_page.click(f'label:has-text("{response.response_value}")')
                                        success = True
                                    except:
                                        print("⚠️ Could not find checkbox to click")
                                        success = False
                            
                            elif question_data['element_type'] == 'select' or 'state' in question_data['question_text'].lower():
                                # Dropdown/select handling
                                print(f"🎯 Selecting dropdown option: {response.response_value}")
                                
                                try:
                                    # Select the option
                                    await survey_page.select_option('select:visible', value=response.response_value)
                                    success = True
                                    print(f"✅ Selected dropdown option: {response.response_value}")
                                except:
                                    try:
                                        # Try by label (for full state names)
                                        state_mappings = {
                                            'NSW': 'New South Wales',
                                            'VIC': 'Victoria', 
                                            'QLD': 'Queensland',
                                            'WA': 'Western Australia',
                                            'SA': 'South Australia',
                                            'TAS': 'Tasmania',
                                            'ACT': 'Australian Capital Territory',
                                            'NT': 'Northern Territory'
                                        }
                                        
                                        full_name = state_mappings.get(response.response_value, response.response_value)
                                        await survey_page.select_option('select:visible', label=full_name)
                                        success = True
                                        print(f"✅ Selected dropdown option: {full_name}")
                                    except:
                                        print("⚠️ Could not select dropdown option")
                                
                            if success:
                                automated_count += 1
                                print(f"✅ AUTOMATED SUCCESSFULLY! (Total: {automated_count}) 🎉")
                                
                                # STORE VISUAL PATTERN!
                                if vision_confidence > 80:
                                    pattern_id = await learner.vision.store_pattern(
                                        screenshot_path,
                                        vision_result,
                                        {
                                            'response_value': response.response_value,
                                            'success': True,
                                            'element_type': question_data['element_type']
                                        }
                                    )
                                    print(f"💾 Stored visual pattern: {pattern_id}")
                                
                                # Record success
                                learner.cm.record_automation_result(
                                    handler_name, question_data['question_type'],
                                    confidence, True
                                )
                                
                                # Save immediately
                                learner.kb.save()
                                
                                # Wait and click next
                                await survey_page.wait_for_timeout(1000)
                                print("📍 Clicking Next...")
                                await survey_page.click('button:has-text("Next"), button:has-text("Continue"), input[type="submit"]:visible')
                                await survey_page.wait_for_timeout(1000)
                                
                                # Check for completion - ENHANCED
                                try:
                                    new_content = await survey_page.inner_text('body')
                                    completion_indicators = [
                                        'thank you', 'thanks for completing', 'survey complete',
                                        'points have been added', 'points earned', 'congratulations',
                                        'survey has been completed', 'successfully completed',
                                        'reward', 'credited to your account'
                                    ]
                                    
                                    if any(indicator in new_content.lower() for indicator in completion_indicators):
                                        print("\n🎉 SURVEY COMPLETE!")
                                        
                                        # Extract points
                                        try:
                                            points_match = re.search(r'(\d+)\s*points?', new_content.lower())
                                            if points_match:
                                                survey_points = int(points_match.group(1))
                                                print(f"💰 Points earned: {survey_points}")
                                        except:
                                            survey_points = 100
                                        
                                        # 📊 LOG THE COMPLETED SURVEY
                                        survey_duration = int(time.time() - survey_start_time)
                                        
                                        reporter.log_survey_completion(
                                            platform="MyOpinions",
                                            survey_id=f"survey_{int(time.time())}",
                                            topic=survey_topic,
                                            points=survey_points,
                                            duration_seconds=survey_duration,
                                            questions_total=question_num,
                                            questions_automated=automated_count,
                                            vision_api_calls=vision_calls_count,
                                            pattern_matches=pattern_matches_count
                                        )
                                        
                                        reporter.print_session_report()
                                        break
                                except:
                                    pass
                                
                                continue  # Skip manual input
                                
                    except Exception as e:
                        print(f"❌ Automation failed: {str(e)}")
                        print("📝 Falling back to manual...")
            
            # Manual capture flow
            input("\n✋ Press Enter AFTER answering but BEFORE clicking Next >>> ")
            
            # Capture and learn WITH VISION GUIDANCE
            learning_entry = await learner.capture_and_learn(survey_page, question_num, vision_result)
            
            # Display results
            print("\n📊 CAPTURED LEARNING DATA:")
            print(f"  📝 Question: {learning_entry['question_text'][:80]}...")
            print(f"  🏷️ Type: {learning_entry['question_type']}")
            print(f"  🎯 Element: {learning_entry['element_type']}")
            print(f"  👁️ Vision Type: {learning_entry.get('vision_type', 'N/A')}")
            print(f"  👁️ Vision Confidence: {learning_entry.get('vision_confidence', 0)}%")
            if learning_entry.get('age_format'):
                print(f"  📍 Age Format: {learning_entry['age_format']}")
            print(f"  💡 Strategy: {learning_entry['strategy_used']}")
            print(f"  ✅ Your Response: {learning_entry['response_value']}")
            if learning_entry.get('response_values') and len(learning_entry['response_values']) > 1:
                print(f"     All values: {', '.join(learning_entry['response_values'])}")
            print(f"  📊 Confidence: {learning_entry['confidence_score']:.3f}")
            print(f"  ⏱️ Capture Time: {learning_entry['execution_time']:.2f}s")
            print(f"  🔑 Learning Key: learning_{int(learning_entry['timestamp'])}_{question_num}")
            
            # STORE VISUAL PATTERN for manual captures too!
            if vision_confidence > 70 and learning_entry.get('response_value'):
                pattern_id = await learner.vision.store_pattern(
                    screenshot_path,
                    vision_result,
                    {
                        'response_value': learning_entry['response_value'],
                        'response_values': learning_entry.get('response_values', []),
                        'success': True,
                        'element_type': learning_entry['element_type'],
                        'capture_type': 'manual_learning'
                    }
                )
                print(f"\n💾 Stored visual pattern from manual capture: {pattern_id}")
            
            print("\n💾 SAVED TO:")
            print(f"  📁 personas/quenito/knowledge_base.json")
            print(f"  📍 Section: detailed_intervention_learning")
            print(f"  👁️ Visual patterns: personas/quenito/visual_patterns/")
            
            # Show confidence update
            handler = learner._get_handler_name(learning_entry['question_type'])
            print(f"\n🎯 Confidence Update:")
            print(f"  Handler: {handler}")
            print(f"  Question Type: {learning_entry['question_type']}")
            print(f"  New Pattern: {learning_entry['question_type']}_{learning_entry['element_type']}")
            
            # AUTO-SAVE PROGRESS EVERY 5 QUESTIONS
            if question_num % 5 == 0:
                print("\n💾 Auto-saving progress...")
                reporter.save_session()
            
            input("\n👉 Now click Next/Continue in browser, then press Enter >>> ")
            
            # Check for completion - ENHANCED
            try:
                new_content = await survey_page.inner_text('body')
                completion_indicators = [
                    'thank you', 'thanks for completing', 'survey complete',
                    'points have been added', 'points earned', 'congratulations',
                    'survey has been completed', 'successfully completed',
                    'reward', 'credited to your account'
                ]
                
                if any(indicator in new_content.lower() for indicator in completion_indicators):
                    print("\n🎉 SURVEY COMPLETE!")
                    
                    # Extract points
                    try:
                        points_match = re.search(r'(\d+)\s*points?', new_content.lower())
                        if points_match:
                            survey_points = int(points_match.group(1))
                            print(f"💰 Points earned: {survey_points}")
                    except:
                        survey_points = 100
                    
                    # 📊 LOG THE COMPLETED SURVEY
                    survey_duration = int(time.time() - survey_start_time)
                    
                    reporter.log_survey_completion(
                        platform="MyOpinions",
                        survey_id=f"survey_{int(time.time())}",
                        topic=survey_topic,
                        points=survey_points,
                        duration_seconds=survey_duration,
                        questions_total=question_num,
                        questions_automated=automated_count,
                        vision_api_calls=vision_calls_count,
                        pattern_matches=pattern_matches_count
                    )
                    
                    reporter.print_session_report()
                    break
            except:
                pass
                
    except KeyboardInterrupt:
        print("\n\n⚠️ Survey interrupted by user")
        print("📊 Saving final reports...")
        
        # SAVE REPORTS EVEN ON INTERRUPT!
        if question_num > 0:
            # Log partial survey
            survey_duration = int(time.time() - survey_start_time)
            
            reporter.log_survey_completion(
                platform="MyOpinions",
                survey_id=f"survey_{int(time.time())}_partial",
                topic=survey_topic,
                points=survey_points or 0,
                duration_seconds=survey_duration,
                questions_total=question_num,
                questions_automated=automated_count,
                vision_api_calls=vision_calls_count,
                pattern_matches=pattern_matches_count
            )
            
            # Print reports
            reporter.print_session_report()
            reporter.print_weekly_summary()
            
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("📊 Saving reports before exit...")
        
        # Save what we can
        if 'reporter' in locals() and question_num > 0:
            reporter.print_session_report()
            
    finally:
        # ALWAYS run final summary
        print("\n" + "="*50)
        print("📊 LEARNING SESSION COMPLETE WITH VISION!")
        print(f"✅ Questions captured: {question_num}")
        print(f"🤖 Questions automated: {automated_count}")
        if question_num > 0:
            print(f"📈 Automation rate: {(automated_count/question_num)*100:.1f}%")
        print(f"👁️ Vision API Calls: {vision_calls_count} (${vision_calls_count * 0.001:.3f})")
        print(f"🎯 Pattern Matches: {pattern_matches_count}")
        print(f"👁️ Visual patterns stored: Check personas/quenito/visual_patterns/")
        print(f"📁 All data saved to: personas/quenito/knowledge_base.json")
        print("\n🧠 Next survey will use these learned patterns + visual recognition!")
        
        # 📊 PRINT FINAL REPORTS
        if 'reporter' in locals():
            reporter.print_session_report()
            reporter.print_weekly_summary()
            
            # 📊 Show lifetime stats if available
            lifetime = reporter.get_lifetime_stats()
            if lifetime.get('total_earnings'):
                print(f"""
╔══════════════════════════════════════════════════════╗
║               💰 LIFETIME STATS                       ║
╚══════════════════════════════════════════════════════╝
Total Earnings: ${lifetime['total_earnings']:.2f}
Total Surveys:  {lifetime['total_surveys']}
Days Active:    {lifetime['days_active']}
Best Day Ever:  {lifetime.get('best_day', 'N/A')} (${lifetime.get('best_day_earnings', 0):.2f})
""")
        
        input("\n🏁 Press Enter to close >>> ")
        
        # Close browser
        if 'browser' in locals():
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_integrated_learning())