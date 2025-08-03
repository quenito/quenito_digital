# quenito_integrated_learning.py
"""
Integrated learning system that captures detailed data and updates confidence dynamically
Matches the existing knowledge base structure and confidence management system
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from core.stealth_browser_manager import StealthBrowserManager
from data.knowledge_base import KnowledgeBase
from data.confidence_manager import ConfidenceManager
from utils.intervention_manager import EnhancedLearningInterventionManager

class IntegratedLearningCapture:
    """Learning capture that integrates with existing confidence system"""
    
    def __init__(self, knowledge_base: KnowledgeBase, confidence_manager: ConfidenceManager):
        self.kb = knowledge_base
        self.cm = confidence_manager
        self.session_id = f"learning_session_{int(time.time())}"
        self.start_time = time.time()
        
        # Ensure detailed_intervention_learning exists
        if 'detailed_intervention_learning' not in self.kb.data:
            self.kb.data['detailed_intervention_learning'] = {}
    
    async def capture_and_learn(self, page, question_number: int) -> Dict[str, Any]:
        """Capture question details and create learning entry"""
        
        capture_start = time.time()
        
        # Extract comprehensive details
        question_data = await self._extract_comprehensive_details(page)
        
        # Determine strategy that would be used
        strategy = self._determine_strategy(question_data)
        
        # Get confidence for this question type
        handler_name = self._get_handler_name(question_data['question_type'])
        confidence = self.cm.get_dynamic_threshold(
            handler_name, 
            question_data['question_type']
        )
        
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
            "automation_success": False,  # Manual for now
            "learned_at": time.time(),
            "url": page.url,
            "page_structure": question_data.get('page_structure', {})
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
        
        # Analyze input elements
        input_analysis = await self._analyze_inputs(page)
        details['element_type'] = input_analysis['primary_type']
        details['input_strategy'] = input_analysis['strategy']
        details['page_structure'] = input_analysis
        
        # Capture user selections
        user_data = await self._capture_user_selections(page, input_analysis)
        details['user_response'] = user_data.get('primary_value', '')
        details['user_responses'] = user_data.get('all_values', [])
        
        return details
    
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
                if '?' in line and 10 < len(line) < 200:
                    return line
        except:
            pass
        
        return "Question text not captured"
    
    def _classify_question_type(self, question_text: str) -> str:
        """Classify question type based on text"""
        
        q_lower = question_text.lower()
        
        # Demographics
        if any(word in q_lower for word in ['age', 'old are you', 'year of birth']):
            return 'age'
        elif 'gender' in q_lower:
            return 'gender'
        elif any(word in q_lower for word in ['occupation', 'job', 'work', 'employed']):
            return 'occupation'
        elif any(word in q_lower for word in ['income', 'earn', 'salary']):
            return 'income'
        elif any(word in q_lower for word in ['education', 'degree', 'school']):
            return 'education'
        elif any(word in q_lower for word in ['postcode', 'zip', 'postal']):
            return 'postcode'
        
        # Survey types
        elif 'tv channels' in q_lower or 'television' in q_lower:
            return 'media_channels'
        elif any(word in q_lower for word in ['brand', 'product']):
            return 'brand_awareness'
        elif any(word in q_lower for word in ['how often', 'frequency']):
            return 'frequency'
        elif any(word in q_lower for word in ['rate', 'rating', 'satisfied']):
            return 'rating_scale'
        elif any(word in q_lower for word in ['select all', 'check all']):
            return 'multi_select'
        
        return 'general'
    
    async def _analyze_inputs(self, page) -> Dict[str, Any]:
        """Analyze input elements on the page"""
        
        analysis = {
            'checkboxes': 0,
            'radios': 0,
            'text_inputs': 0,
            'selects': 0,
            'textareas': 0,
            'buttons': 0,
            'primary_type': '',
            'strategy': ''
        }
        
        # Count input types
        analysis['checkboxes'] = len(await page.query_selector_all('input[type="checkbox"]'))
        analysis['radios'] = len(await page.query_selector_all('input[type="radio"]'))
        analysis['text_inputs'] = len(await page.query_selector_all('input[type="text"]'))
        analysis['selects'] = len(await page.query_selector_all('select'))
        analysis['textareas'] = len(await page.query_selector_all('textarea'))
        analysis['buttons'] = len(await page.query_selector_all('button.option, div.option'))
        
        # Determine primary type and strategy
        if analysis['checkboxes'] > 0:
            analysis['primary_type'] = 'checkbox'
            analysis['strategy'] = 'checkbox_multi_select'
        elif analysis['radios'] > 0:
            analysis['primary_type'] = 'radio'
            analysis['strategy'] = 'radio_selection'
        elif analysis['text_inputs'] > 0:
            analysis['primary_type'] = 'text_input'
            analysis['strategy'] = 'fill_strategy'
        elif analysis['selects'] > 0:
            analysis['primary_type'] = 'dropdown'
            analysis['strategy'] = 'dropdown_selection'
        else:
            analysis['primary_type'] = 'unknown'
            analysis['strategy'] = 'unknown'
        
        return analysis
    
    async def _capture_user_selections(self, page, input_analysis: Dict) -> Dict[str, Any]:
        """Capture what the user selected/entered"""
        
        user_data = {
            'primary_value': '',
            'all_values': []
        }
        
        try:
            if input_analysis['primary_type'] == 'checkbox':
                # Get checked checkboxes
                checkboxes = await page.query_selector_all('input[type="checkbox"]:checked')
                for cb in checkboxes:
                    # Get label text
                    cb_id = await cb.get_attribute('id')
                    if cb_id:
                        label = await page.query_selector(f'label[for="{cb_id}"]')
                        if label:
                            text = await label.inner_text()
                            user_data['all_values'].append(text.strip())
                
            elif input_analysis['primary_type'] == 'radio':
                # Get selected radio
                radio = await page.query_selector('input[type="radio"]:checked')
                if radio:
                    radio_id = await radio.get_attribute('id')
                    if radio_id:
                        label = await page.query_selector(f'label[for="{radio_id}"]')
                        if label:
                            text = await label.inner_text()
                            user_data['all_values'].append(text.strip())
            
            elif input_analysis['primary_type'] == 'text_input':
                # Get text input values
                inputs = await page.query_selector_all('input[type="text"]')
                for inp in inputs:
                    value = await inp.get_attribute('value')
                    if value:
                        user_data['all_values'].append(value)
            
            elif input_analysis['primary_type'] == 'dropdown':
                # Get selected dropdown values
                selects = await page.query_selector_all('select')
                for sel in selects:
                    selected_text = await sel.evaluate('''el => {
                        const opt = el.options[el.selectedIndex];
                        return opt ? opt.text : '';
                    }''')
                    if selected_text:
                        user_data['all_values'].append(selected_text)
            
            # Set primary value
            if user_data['all_values']:
                user_data['primary_value'] = user_data['all_values'][0]
        
        except Exception as e:
            print(f"Error capturing selections: {e}")
        
        return user_data
    
    def _determine_strategy(self, question_data: Dict) -> str:
        """Determine which strategy would be used"""
        
        strategies_map = {
            'text_input': 'fill_strategy',
            'radio': 'radio_selection',
            'checkbox': 'checkbox_multi_select',
            'dropdown': 'dropdown_selection',
            'button': 'button_click'
        }
        
        return strategies_map.get(question_data['element_type'], 'unknown_strategy')
    
    def _get_handler_name(self, question_type: str) -> str:
        """Get handler name for question type"""
        
        if question_type in ['age', 'gender', 'occupation', 'income', 'education', 'postcode']:
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
    """Main learning session with integrated capture"""
    
    print("🧠 QUENITO INTEGRATED LEARNING SYSTEM")
    print("="*50)
    
    # Initialize systems
    kb = KnowledgeBase()
    cm = ConfidenceManager(kb.data.get('confidence_system', {}))
    learner = IntegratedLearningCapture(kb, cm)
    
    # Initialize browser
    browser = StealthBrowserManager("quenito_myopinions")
    await browser.initialize_stealth_browser(transfer_cookies=False)
    await browser.load_saved_cookies()
    
    # Navigate to MyOpinions
    await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
    
    print("\n📋 SETUP:")
    print("1. Login if needed")
    print("2. Close popups")
    input("\n✅ Press Enter when ready >>> ")
    
    # Detect and select shortest survey
    print("\n🔍 Finding shortest survey...")
    
    await browser.page.wait_for_selector('.card', timeout=10000)
    cards = await browser.page.query_selector_all('.card')
    
    surveys = []
    for card in cards:
        try:
            points_elem = await card.query_selector('.card-body-points')
            time_elem = await card.query_selector('.card-body-loi')
            button_elem = await card.query_selector('a.btn.btn-primary')
            
            if button_elem and time_elem:
                time_text = await time_elem.inner_text()
                points_text = await points_elem.inner_text() if points_elem else "0"
                
                # Parse time
                if 'min' in time_text.lower():
                    minutes = int(''.join(filter(str.isdigit, time_text.split('min')[0])))
                else:
                    minutes = 999
                
                surveys.append({
                    'time': time_text,
                    'minutes': minutes,
                    'points': points_text,
                    'element': button_elem
                })
        except:
            continue
    
    # Sort by time
    surveys.sort(key=lambda x: x['minutes'])
    
    if not surveys:
        print("❌ No surveys found!")
        return
    
    print(f"\n✅ Selected: {surveys[0]['time']} survey")
    
    # Click survey
    await surveys[0]['element'].click()
    await asyncio.sleep(3)
    
    # Handle page transitions
    all_pages = browser.context.pages
    survey_page = all_pages[-1]
    await survey_page.bring_to_front()
    
    # Check page type
    page_content = await survey_page.inner_text('body')
    
    # Handle intermediate page if present
    if 'start survey now' in page_content.lower():
        print("📄 Intermediate page detected")
        for selector in ['button:has-text("Start Survey Now")', 'a:has-text("Start Survey Now")']:
            try:
                await survey_page.click(selector)
                print("✅ Clicked Start Survey Now")
                await asyncio.sleep(3)
                break
            except:
                continue
    
    print("\n🧠 ACTIVE LEARNING MODE")
    print("="*50)
    print("Instructions:")
    print("1. Answer question in browser")
    print("2. Press Enter HERE (before clicking Next)")
    print("3. See detailed capture")
    print("4. Click Next in browser")
    print("="*50)
    
    question_num = 0
    
    while True:
        question_num += 1
        
        print(f"\n❓ QUESTION {question_num}")
        print("-"*50)
        
        input("\n✋ Press Enter AFTER answering but BEFORE clicking Next >>> ")
        
        # Capture and learn
        learning_entry = await learner.capture_and_learn(survey_page, question_num)
        
        # Display results
        print("\n📊 CAPTURED LEARNING DATA:")
        print(f"  📝 Question: {learning_entry['question_text'][:80]}...")
        print(f"  🏷️ Type: {learning_entry['question_type']}")
        print(f"  🎯 Element: {learning_entry['element_type']}")
        print(f"  💡 Strategy: {learning_entry['strategy_used']}")
        print(f"  ✅ Your Response: {learning_entry['response_value']}")
        if learning_entry.get('response_values') and len(learning_entry['response_values']) > 1:
            print(f"     All values: {', '.join(learning_entry['response_values'])}")
        print(f"  📊 Confidence: {learning_entry['confidence_score']:.3f}")
        print(f"  ⏱️ Capture Time: {learning_entry['execution_time']:.2f}s")
        print(f"  🔑 Learning Key: learning_{int(learning_entry['timestamp'])}_{question_num}")
        
        print("\n💾 SAVED TO:")
        print(f"  📁 personas/quenito/knowledge_base.json")
        print(f"  📍 Section: detailed_intervention_learning")
        
        # Show confidence update
        handler = learner._get_handler_name(learning_entry['question_type'])
        print(f"\n🎯 Confidence Update:")
        print(f"  Handler: {handler}")
        print(f"  Question Type: {learning_entry['question_type']}")
        print(f"  New Pattern: {learning_entry['question_type']}_{learning_entry['element_type']}")
        
        input("\n👉 Now click Next/Continue in browser, then press Enter >>> ")
        
        # Check for completion
        try:
            new_content = await survey_page.inner_text('body')
            if any(word in new_content.lower() for word in ['thank you', 'complete', 'points earned']):
                print("\n🎉 SURVEY COMPLETE!")
                break
        except:
            pass
    
    # Summary
    print("\n" + "="*50)
    print("📊 LEARNING SESSION COMPLETE")
    print(f"✅ Questions captured: {question_num}")
    print(f"📁 All data saved to: personas/quenito/knowledge_base.json")
    print("\n🧠 Next survey will use these learned patterns!")
    
    input("\n🏁 Press Enter to close >>> ")
    await browser.close()

if __name__ == "__main__":
    asyncio.run(run_integrated_learning())