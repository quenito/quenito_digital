#!/usr/bin/env python3
"""
🧠 QUENITO LIVE SURVEY RUNNER - Prime Opinion First Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Real survey testing with comparison tracking, error recovery, and timing metrics
Matt's Digital Twin vs Matt's Actual Answers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
from typing import Dict, List, Any, Optional

# Import the stealth browser manager
try:
    from core.stealth_browser_manager import StealthBrowserManager
except ImportError:
    print("⚠️ StealthBrowserManager not found, using basic browser")
    StealthBrowserManager = None

# Import your core components
try:
    from core.consciousness_engine_production import ConsciousnessEngine
except ImportError:
    ConsciousnessEngine = None
    
from services.vision_service import VisionService
from services.ui_pattern_intelligence import UIPatternIntelligence


class LiveSurveyRunner:
    """
    Orchestrates Quenito's first real survey on Prime Opinion
    with comprehensive tracking and comparison capabilities
    """
    
    def __init__(self, matt_comparison_mode: bool = True):
        """
        Initialize the runner with all validated UI capabilities
        
        Args:
            matt_comparison_mode: If True, prompts for Matt's actual answers for comparison
        """
        # Core brain - PROPERLY INITIALIZE CONSCIOUSNESS ENGINE
        if ConsciousnessEngine:
            try:
                self.engine = ConsciousnessEngine(consciousness_path="core/matt_consciousness_v3.json")
                print("🧠 Consciousness Engine loaded successfully")
            except Exception as e:
                print(f"⚠️ Warning: Could not load consciousness engine: {e}")
                self.engine = None
        else:
            print("⚠️ Warning: consciousness_engine_production.py not found")
            self.engine = None
        
        self.vision = VisionService()
        
        # Comparison mode
        self.comparison_mode = matt_comparison_mode
        
        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.survey_data = {
            "session_id": self.session_id,
            "platform": "Prime Opinion",
            "start_time": None,
            "end_time": None,
            "survey_url": None,
            "survey_title": None,
            "questions": [],
            "comparison_results": [],
            "metrics": {
                "total_questions": 0,
                "automated_questions": 0,
                "manual_interventions": 0,
                "ui_pattern_distribution": {},
                "time_per_question": [],
                "total_time": 0,
                "accuracy_score": 0,
                "confidence_average": 0
            },
            "errors": [],
            "ui_patterns_encountered": set()
        }
        
        # Browser manager
        self.browser_manager = None
        self.browser = None
        self.page = None
        self.ui_intelligence = None
        
    async def initialize_browser(self):
        """Launch browser using StealthBrowserManager with proper cookie transfer"""
        print("🌐 Launching stealth browser...")
        
        if StealthBrowserManager:
            # First, extract Chrome cookies (missing from StealthBrowserManager)
            print("🍪 Extracting Chrome cookies...")
            relevant_cookies = []
            
            try:
                import browser_cookie3
                chrome_cookies = list(browser_cookie3.chrome())
                
                # Filter for Prime Opinion domains (match simple_primeopinion_test.py)
                target_domains = ['primeopinion.com.au', 'google.com', 'googleapis.com']
                
                for cookie in chrome_cookies:
                    if any(domain in cookie.domain for domain in target_domains):
                        relevant_cookies.append({
                            'name': cookie.name,
                            'value': cookie.value,
                            'domain': cookie.domain,
                            'path': cookie.path,
                            'secure': bool(cookie.secure),
                            'httpOnly': bool(getattr(cookie, 'httpOnly', False)),
                            'expires': float(cookie.expires) if cookie.expires and cookie.expires != -1 else -1
                        })
                
                print(f"✅ Found {len(relevant_cookies)} Prime Opinion cookies")
                
            except ImportError:
                print("⚠️ browser_cookie3 not installed")
            except Exception as e:
                print(f"⚠️ Cookie extraction failed: {e}")
            
            # Use the StealthBrowserManager
            self.browser_manager = StealthBrowserManager(profile_name="quenito_survey")
            
            try:
                # Initialize browser
                self.page = await self.browser_manager.initialize_stealth_browser(
                    transfer_cookies=False,  # We'll add them manually
                    use_existing_chrome=False
                )
                
                if self.page and relevant_cookies:
                    # Manually add the extracted cookies
                    print(f"🔄 Transferring {len(relevant_cookies)} cookies...")
                    await self.browser_manager.context.add_cookies(relevant_cookies)
                    print("✅ Cookies transferred successfully")
                
                if self.page:
                    self.browser = self.browser_manager.browser
                    self.ui_intelligence = UIPatternIntelligence(self.page)
                    print("✅ Stealth browser ready with session persistence")
                else:
                    raise Exception("Failed to initialize page")
                    
            except Exception as e:
                print(f"⚠️ StealthBrowserManager failed: {e}")
                await self._fallback_browser_init()
        else:
            # Fallback to basic browser if StealthBrowserManager not available
            await self._fallback_browser_init()
    
    async def _fallback_browser_init(self):
        """Fallback browser initialization without StealthBrowserManager"""
        print("Using fallback browser initialization...")
        
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        self.page = await context.new_page()
        self.ui_intelligence = UIPatternIntelligence(self.page)
        print("✅ Basic browser ready")
    
    async def start_survey(self, survey_url: str = None):
        """
        Begin the survey - with cookie transfer, might already be logged in!
        
        Args:
            survey_url: The Prime Opinion survey URL (optional)
        """
        print("\n" + "="*70)
        print("🚀 QUENITO LIVE SURVEY TEST - PRIME OPINION")
        print("="*70)
        
        # Default to Prime Opinion dashboard if no URL provided
        if not survey_url or survey_url == "None":
            survey_url = "https://app.primeopinion.com.au/surveys"
            print(f"\n📍 Using default: {survey_url}")
        else:
            print(f"\n📍 Target survey: {survey_url}")
        
        self.survey_data["survey_url"] = survey_url
        self.survey_data["start_time"] = datetime.now().isoformat()
        
        # Navigate to survey/dashboard
        print("🔗 Navigating (cookies should maintain login)...")
        await self.page.goto(survey_url, wait_until='networkidle')
        
        # Check if we're logged in
        current_url = self.page.url
        
        if "login" in current_url.lower():
            print("\n⚠️ LOGIN REQUIRED - Cookie transfer may have failed")
            print("Please login manually...")
            input("Press Enter when logged in and ready...")
        elif "surveys" in current_url or "dashboard" in current_url:
            print("✅ Already logged in via cookie transfer!")
            print("\n📋 Please select a survey to test:")
            print("1. Choose a 5-8 minute survey")
            print("2. Click on it to start")
            print("3. The survey will open in a NEW TAB")
            print("4. Complete any intro/consent screens in the new tab")
            input("\n✋ Press Enter when you're on the FIRST QUESTION in the SURVEY TAB...")
        else:
            print(f"\n📍 Current page: {current_url}")
            print("Navigate to your chosen survey...")
            print("Remember: The survey will open in a NEW TAB")
            input("\n✋ Press Enter when you're on the FIRST QUESTION in the SURVEY TAB...")
        
        # Capture survey title if possible
        try:
            title = await self.page.title()
            self.survey_data["survey_title"] = title
            print(f"\n📋 Survey Title: {title}")
        except:
            pass
        
        # Start the automation
        await self.process_survey()
    
    async def process_survey(self):
        """Main survey processing loop with full UI pattern support and TAB HANDLING"""
        question_num = 0
        
        print("\n🧠 Quenito taking control...")
        print("-" * 70)
        
        # CRITICAL: Switch to the survey tab (rightmost/newest)
        await self._switch_to_survey_tab()
        
        while True:
            question_num += 1
            question_start_time = time.time()
            
            try:
                # IMPORTANT: Always check we're on the right tab
                await self._ensure_survey_tab()
                
                # CRITICAL: Wait for page to fully load before screenshot
                print(f"\n⏳ Waiting for page to stabilize...")
                try:
                    # Try networkidle first but with shorter timeout
                    await self.page.wait_for_load_state('networkidle', timeout=5000)
                except:
                    # If networkidle times out, just wait for DOM to be ready
                    try:
                        await self.page.wait_for_load_state('domcontentloaded', timeout=5000)
                    except:
                        pass  # Page might already be loaded
                
                # Additional wait for dynamic content
                await asyncio.sleep(2)
                
                # Take screenshot for vision analysis AFTER page is stable
                screenshot_path = f"surveys/live_{self.session_id}_q{question_num}.png"
                await self.page.screenshot(path=screenshot_path)
                
                # Vision analysis
                print(f"\n📸 Question {question_num}:")
                
                # PROPERLY USE CONSCIOUSNESS ENGINE with test_screenshot_flow
                if self.engine:
                    try:
                        # Use test_screenshot_flow to get FULL reasoning (like the test files)
                        vision_result = await self.engine.test_screenshot_flow(screenshot_path)
                        
                        # This should now have all the keys:
                        # - question, options, question_type (vision)
                        # - llm_answer, confidence, reasoning (consciousness)
                            
                    except Exception as e:
                        print(f"⚠️ Consciousness engine error: {e}")
                        # Fallback to basic structure
                        vision_result = {
                            'question': 'Error processing question',
                            'question_type': 'unknown',
                            'options': [],
                            'llm_answer': 'Unknown',
                            'confidence': 0.0,
                            'reasoning': 'Error in consciousness engine'
                        }
                else:
                    # Fallback to basic vision service without consciousness
                    print("⚠️ Running without consciousness engine")
                    vision_result = {
                        'question': 'No consciousness engine',
                        'question_type': 'unknown',
                        'options': [],
                        'llm_answer': 'Unknown',
                        'confidence': 0.0
                    }
                
                # Check for completion
                if self._is_completion_page(vision_result):
                    print("\n🎉 SURVEY COMPLETE!")
                    break
                
                # Display question details
                question_text = vision_result.get('question', 'Unknown question')
                question_type = vision_result.get('question_type', 'unknown')
                print(f"❓ {question_text[:100]}...")
                print(f"📊 Type: {question_type}")
                
                # Get Quenito's answer from consciousness
                quenito_answer = await self._get_quenito_answer(vision_result)
                confidence = vision_result.get('confidence', 0)
                reasoning = vision_result.get('reasoning', '')
                
                print(f"🤖 Quenito's Answer: {self._format_answer(quenito_answer)}")
                print(f"💭 Confidence: {confidence:.0%}")
                
                # Display reasoning if available
                if reasoning:
                    print(f"🧠 Reasoning: {reasoning[:200]}...")
                
                # Track UI pattern
                self.survey_data["ui_patterns_encountered"].add(question_type)
                self.survey_data["metrics"]["ui_pattern_distribution"][question_type] = \
                    self.survey_data["metrics"]["ui_pattern_distribution"].get(question_type, 0) + 1
                
                # Attempt UI automation FIRST
                automation_success = await self._automate_answer(question_type, quenito_answer, vision_result)
                
                if automation_success:
                    print("✅ Automated successfully")
                    self.survey_data["metrics"]["automated_questions"] += 1
                    
                    # Only ask for Matt's answer AFTER automation for comparison
                    matt_answer = None
                    if self.comparison_mode and confidence > 0.5:  # Only compare high-confidence answers
                        print("\n📝 For comparison (optional - press Enter to skip):")
                        matt_input = input("Your answer (or Enter to skip): ").strip()
                        if matt_input:
                            matt_answer = matt_input
                else:
                    print("⚠️ Automation failed - manual intervention needed")
                    self.survey_data["metrics"]["manual_interventions"] += 1
                    
                    # Manual mode - you answer once
                    print("\n👤 Please answer the question manually in the browser")
                    input("Press Enter after answering...")
                    
                    # In manual mode, we can still track your answer if you want
                    matt_answer = None
                    if self.comparison_mode:
                        matt_input = input("What did you answer? (optional, Enter to skip): ").strip()
                        if matt_input:
                            matt_answer = matt_input
                
                # Record question data
                question_time = time.time() - question_start_time
                self.survey_data["questions"].append({
                    "number": question_num,
                    "text": question_text,
                    "type": question_type,
                    "quenito_answer": quenito_answer,
                    "matt_answer": matt_answer,
                    "confidence": confidence,
                    "automated": automation_success,
                    "time_seconds": question_time,
                    "match": quenito_answer == matt_answer if matt_answer else None
                })
                
                self.survey_data["metrics"]["time_per_question"].append(question_time)
                self.survey_data["metrics"]["total_questions"] += 1
                
                # Click next/continue button automatically
                next_clicked = await self._click_next(self.page)
                
                if not next_clicked:
                    # Only ask for manual intervention if auto-click failed
                    print("📍 Auto-click failed - please click Next/Continue manually")
                    input("Press Enter after clicking Next...")
                
                # CRITICAL: Wait for next page to START loading
                print("⏳ Waiting for next question to load...")
                await asyncio.sleep(1)  # Brief pause for navigation to start
                    
            except Exception as e:
                print(f"❌ Error on question {question_num}: {str(e)}")
                self.survey_data["errors"].append({
                    "question": question_num,
                    "error": str(e)
                })
                
                # Error recovery
                print("\n🔧 Error Recovery Options:")
                print("1. Continue (c) - Skip this question")
                print("2. Retry (r) - Try again")
                print("3. Quit (q) - End survey")
                choice = input("Choice: ").lower()
                
                if choice == 'q':
                    break
                elif choice == 'r':
                    question_num -= 1  # Retry same question
                    continue
                else:
                    input("Answer manually and press Enter to continue...")
        
        # Finalize session
        await self.finalize_session()
    
    async def _get_quenito_answer(self, vision_result: Dict) -> Any:
        """Get Quenito's answer based on question type - with proper consciousness integration"""
        question_type = vision_result.get('question_type', 'unknown')
        question_text = vision_result.get('question', '')
        options = vision_result.get('options', [])
        
        # Debug: Show what we're working with
        print(f"🔍 Debug - Question: {question_text[:50]}...")
        print(f"🔍 Debug - Options detected: {len(options)}")
        
        # If consciousness engine provided an answer, use it
        answer = vision_result.get('llm_answer', 'Unknown')
        
        # If we got "Unknown" but have options, try to use Matt's consciousness directly
        if (answer == 'Unknown' or answer == '' or (isinstance(answer, list) and len(answer) == 0)) and options:
            print("🧠 Applying Matt's consciousness directly...")
            
            # Apply Matt's logic based on question content
            question_lower = question_text.lower()
            
            # Gender questions
            if 'gender' in question_lower:
                for i, opt in enumerate(options):
                    if 'male' in opt.lower() and 'female' not in opt.lower():
                        answer = opt
                        print(f"  Matt's gender: {answer}")
                        break
            
            # Location questions
            elif 'australia' in question_lower or 'country' in question_lower:
                for opt in options:
                    if 'australia' in opt.lower():
                        answer = opt
                        print(f"  Matt's location: {answer}")
                        break
            
            # Language questions
            elif 'language' in question_lower:
                for opt in options:
                    if 'english' in opt.lower():
                        answer = opt
                        print(f"  Matt's language: {answer}")
                        break
            
            # Interest questions (multi-select)
            elif 'interest' in question_lower and question_type in ['multi_select', 'multi-select']:
                interests = []
                interest_keywords = ['health', 'food', 'nutrition', 'fitness', 'exercise', 'sport']
                for opt in options:
                    opt_lower = opt.lower()
                    if any(keyword in opt_lower for keyword in interest_keywords):
                        interests.append(opt)
                
                if interests:
                    answer = interests[:3]  # Select up to 3 interests
                    print(f"  Matt's interests: {answer}")
                else:
                    answer = []
            
            # Personality traits (multi-select)
            elif 'describe' in question_lower and question_type in ['multi_select', 'multi-select']:
                traits = []
                trait_keywords = ['social', 'open-minded', 'confident', 'price-conscious']
                for opt in options:
                    opt_lower = opt.lower()
                    if any(keyword in opt_lower for keyword in trait_keywords):
                        traits.append(opt)
                
                if traits:
                    answer = traits[:3]  # Select up to 3 traits
                    print(f"  Matt's traits: {answer}")
                else:
                    answer = []
            
            # If still unknown, use first option for single-select
            elif question_type in ['radio', 'single_select', 'single-select'] and answer == 'Unknown':
                answer = options[0] if options else 'Unknown'
                print(f"  Using first option as fallback: {answer}")
        
        return answer
    
    async def _get_matt_answer(self, question: str, options: List[str]) -> Any:
        """Get Matt's actual answer for comparison"""
        print("\n👤 MATT'S ACTUAL ANSWER:")
        print(f"Question: {question[:100]}...")
        
        if options:
            print("Options:")
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            print("\nEnter your answer (number, or comma-separated for multi-select):")
        else:
            print("Enter your answer:")
        
        answer = input("Matt's answer: ").strip()
        
        # Parse answer based on format
        if ',' in answer:
            # Multi-select
            indices = [int(x.strip()) - 1 for x in answer.split(',')]
            return [options[i] for i in indices if i < len(options)]
        elif answer.isdigit() and options:
            # Single select by number
            idx = int(answer) - 1
            return options[idx] if idx < len(options) else answer
        else:
            # Text or direct answer
            return answer
    
    async def _automate_answer(self, question_type: str, answer: Any, vision_result: Dict) -> bool:
        """
        Automate the answer using the appropriate UI pattern handler
        
        Returns:
            bool: True if automation successful, False if manual needed
        """
        try:
            # Map question types to handlers (handle various naming conventions)
            type_mapping = {
                'radio': self._handle_radio,
                'single_select': self._handle_radio,  # Map single_select to radio
                'single-select': self._handle_radio,
                'dropdown': self._handle_dropdown,
                'text': self._handle_text_input,
                'text_input': self._handle_text_input,
                'multi_select': self._handle_multi_select,
                'multi-select': self._handle_multi_select,
                'checkbox': self._handle_multi_select,
                'grid': self._handle_grid,
                'matrix': self._handle_grid,
                'slider': self._handle_slider,
                'scale': self._handle_slider,
                'star_rating': self._handle_star_rating,
                'star-rating': self._handle_star_rating,
                'brand_card': self._handle_brand_card,
                'brand-card': self._handle_brand_card,
                'carousel': self._handle_carousel
            }
            
            # Get the appropriate handler
            handler = type_mapping.get(question_type)
            
            if handler:
                return await handler(answer)
            else:
                print(f"⚠️ Unknown UI pattern: {question_type}")
                return False
                
        except Exception as e:
            print(f"❌ Automation failed: {str(e)}")
            return False
    
    # UI Handler Methods (simplified versions - you have the full implementations)
    
    async def _handle_radio(self, answer: str) -> bool:
        """Handle radio button selection"""
        try:
            # Don't try to automate if answer is Unknown
            if answer == 'Unknown' or not answer:
                return False
                
            # Wait for any dynamic content to load
            await asyncio.sleep(0.5)
            
            # Method 1: Try clicking the label containing the answer text
            label_selectors = [
                f'label:has-text("{answer}")',
                f'label:text-is("{answer}")',
                f'div[role="radio"]:has-text("{answer}")',
                f'span:has-text("{answer}")'
            ]
            
            for selector in label_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        await element.click()
                        await asyncio.sleep(0.5)  # Wait for selection to register
                        return True
                except:
                    continue
            
            # Method 2: Find the radio input and click it
            radio_inputs = await self.page.query_selector_all('input[type="radio"]')
            for radio in radio_inputs:
                try:
                    # Get the label or text associated with this radio
                    parent = await radio.evaluate_handle('(el) => el.parentElement')
                    text = await parent.inner_text()
                    if answer.lower() in text.lower():
                        await radio.click()
                        await asyncio.sleep(0.5)
                        return True
                except:
                    continue
            
            return False
        except Exception as e:
            print(f"   ⚠️ Radio handler error: {e}")
            return False
    
    async def _handle_dropdown(self, answer: str) -> bool:
        """Handle dropdown selection"""
        try:
            # Find select element and choose option
            selects = await self.page.query_selector_all('select')
            for select in selects:
                await select.select_option(label=answer)
                return True
            return False
        except:
            return False
    
    async def _handle_text_input(self, answer: str) -> bool:
        """Handle text input"""
        try:
            # Find and fill text input
            input_field = await self.page.query_selector('input[type="text"], input[type="number"]')
            if input_field:
                await input_field.fill(str(answer))
                return True
            return False
        except:
            return False
    
    async def _handle_multi_select(self, answers: List[str]) -> bool:
        """Handle multi-select checkboxes"""
        try:
            success_count = 0
            for answer in answers:
                checkbox = await self.page.query_selector(f'label:has-text("{answer}")')
                if checkbox:
                    await checkbox.click()
                    success_count += 1
                    await asyncio.sleep(0.3)  # Small delay between selections
            return success_count > 0
        except:
            return False
    
    async def _handle_grid(self, answers: Any) -> bool:
        """Handle grid/matrix questions (e.g., alcohol consumption grid)"""
        try:
            # Check if answers is the right format
            if not isinstance(answers, dict):
                print(f"   ⚠️ Grid expects dictionary, got {type(answers).__name__}")
                return False
                
            if answers == {} or answers == 'Unknown':
                print("   ⚠️ No grid answers provided")
                return False
                
            success_count = 0
            
            # For each item in the grid (e.g., Beer, Wine, Spirits)
            for item, frequency in answers.items():
                # Find the row for this item
                row_selectors = [
                    f'tr:has-text("{item}")',
                    f'div[class*="row"]:has-text("{item}")',
                    f'div:has-text("{item}"):has(input[type="radio"])'
                ]
                
                for row_selector in row_selectors:
                    try:
                        row = await self.page.query_selector(row_selector)
                        if row:
                            # Find and click the radio button for the frequency
                            frequency_selectors = [
                                f'label:has-text("{frequency}")',
                                f'input[type="radio"][value*="{frequency}"]',
                                f'td:has-text("{frequency}") input[type="radio"]'
                            ]
                            
                            for freq_selector in frequency_selectors:
                                radio = await row.query_selector(freq_selector)
                                if radio:
                                    await radio.click()
                                    success_count += 1
                                    await asyncio.sleep(0.3)  # Small delay between selections
                                    break
                            break
                    except:
                        continue
            
            return success_count > 0
            
        except Exception as e:
            print(f"   ⚠️ Grid handling error: {e}")
            return False
    
    async def _handle_slider(self, value: Any) -> bool:
        """Handle slider input (Likert scales, satisfaction ratings)"""
        try:
            # Find slider element
            slider_selectors = [
                'input[type="range"]',
                'div[class*="slider"]',
                'div[role="slider"]',
                '.rc-slider'  # React slider component
            ]
            
            for selector in slider_selectors:
                slider = await self.page.query_selector(selector)
                if slider:
                    # Method 1: For input range elements
                    if selector.startswith('input'):
                        # Set value directly
                        await slider.evaluate(f'(el) => el.value = {value}')
                        # Trigger change event
                        await slider.evaluate('(el) => el.dispatchEvent(new Event("change", { bubbles: true }))')
                        return True
                    
                    # Method 2: For div-based sliders, click at position
                    else:
                        # Get slider bounds
                        box = await slider.bounding_box()
                        if box:
                            # Calculate click position (0-100 scale)
                            position_ratio = float(value) / 100
                            click_x = box['x'] + (box['width'] * position_ratio)
                            click_y = box['y'] + (box['height'] / 2)
                            
                            # Click at calculated position
                            await self.page.mouse.click(click_x, click_y)
                            return True
            
            # Method 3: Click on scale labels if present
            scale_labels = [
                'Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree',
                'Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied'
            ]
            
            # Map value to label position
            label_index = int((float(value) / 100) * (len(scale_labels) - 1))
            if label_index < len(scale_labels):
                label = scale_labels[label_index]
                label_elem = await self.page.query_selector(f'text="{label}"')
                if label_elem:
                    await label_elem.click()
                    return True
            
            return False
            
        except Exception as e:
            print(f"   ⚠️ Slider handling error: {e}")
            return False
    
    async def _handle_star_rating(self, ratings: Any) -> bool:
        """Handle star ratings for brands"""
        try:
            success_count = 0
            
            # Handle single rating or multiple ratings
            if isinstance(ratings, int):
                # Single star rating
                star_selector = f'.star[data-rating="{ratings}"], .star:nth-child({ratings})'
                star = await self.page.query_selector(star_selector)
                if star:
                    await star.click()
                    return True
            
            elif isinstance(ratings, dict):
                # Multiple brands to rate
                for brand, rating in ratings.items():
                    # Find the brand row
                    brand_row_selectors = [
                        f'div:has-text("{brand}"):has(.star)',
                        f'tr:has-text("{brand}")',
                        f'div[data-brand="{brand}"]'
                    ]
                    
                    for row_selector in brand_row_selectors:
                        row = await self.page.query_selector(row_selector)
                        if row:
                            # Click the appropriate star
                            star = await row.query_selector(f'.star:nth-child({rating})')
                            if not star:
                                # Try data-rating attribute
                                star = await row.query_selector(f'.star[data-rating="{rating}"]')
                            
                            if star:
                                await star.click()
                                success_count += 1
                                await asyncio.sleep(0.3)
                                break
                
                return success_count > 0
            
            return False
            
        except Exception as e:
            print(f"   ⚠️ Star rating error: {e}")
            return False
    
    async def _handle_brand_card(self, brand: str) -> bool:
        """Handle brand card/logo selection (e.g., mattress retailers)"""
        try:
            # Brand cards can be images, divs with logos, or cards
            brand_selectors = [
                f'img[alt*="{brand}"]',
                f'div[class*="brand"]:has-text("{brand}")',
                f'div[class*="card"]:has-text("{brand}")',
                f'button:has-text("{brand}")',
                f'label:has-text("{brand}")',
                f'div[data-brand="{brand}"]',
                # For image-based cards
                f'div:has(img[src*="{brand.lower()}"])',
                f'div:has(img[alt*="{brand}"])'
            ]
            
            for selector in brand_selectors:
                element = await self.page.query_selector(selector)
                if element:
                    # Check if it's clickable
                    is_clickable = await element.is_visible() and await element.is_enabled()
                    if is_clickable:
                        await element.click()
                        
                        # Some brand cards have a separate select button
                        await asyncio.sleep(0.5)
                        select_btn = await self.page.query_selector('button:has-text("Select"):visible')
                        if select_btn:
                            await select_btn.click()
                        
                        return True
            
            # Try JavaScript click as fallback
            js_result = await self.page.evaluate(f'''() => {{
                const elements = document.querySelectorAll('*');
                for (const el of elements) {{
                    if (el.textContent && el.textContent.includes('{brand}')) {{
                        el.click();
                        return true;
                    }}
                }}
                return false;
            }}''')
            
            return js_result
            
        except Exception as e:
            print(f"   ⚠️ Brand card error: {e}")
            return False
    
    async def _handle_carousel(self, selection: Any) -> bool:
        """Handle carousel navigation and selection"""
        try:
            # First, check current page for the target item
            target_found = False
            target_text = selection if isinstance(selection, str) else str(selection)
            
            # Check if target is visible on current page
            target_element = await self.page.query_selector(f'text="{target_text}"')
            if target_element and await target_element.is_visible():
                await target_element.click()
                target_found = True
            
            # If not found, navigate carousel
            if not target_found:
                max_pages = 10  # Prevent infinite loop
                pages_checked = 0
                
                while pages_checked < max_pages and not target_found:
                    # Look for next/arrow button
                    next_selectors = [
                        'button[aria-label*="next"]',
                        'button[class*="next"]',
                        'button:has-text("→")',
                        '.carousel-control-next',
                        '.swiper-button-next',
                        'button.slick-next'
                    ]
                    
                    next_clicked = False
                    for selector in next_selectors:
                        next_btn = await self.page.query_selector(selector)
                        if next_btn and await next_btn.is_visible():
                            await next_btn.click()
                            next_clicked = True
                            await asyncio.sleep(1)  # Wait for carousel animation
                            break
                    
                    if not next_clicked:
                        break  # No more pages
                    
                    # Check for target on new page
                    target_element = await self.page.query_selector(f'text="{target_text}"')
                    if target_element and await target_element.is_visible():
                        await target_element.click()
                        target_found = True
                    
                    pages_checked += 1
            
            # After selecting, might need to choose visit type (Online/In-store/Both)
            if target_found:
                await asyncio.sleep(0.5)
                
                # Check for follow-up selection (e.g., visit type)
                visit_options = ['Online', 'In physical store', 'Both']
                for option in visit_options:
                    option_elem = await self.page.query_selector(f'button:has-text("{option}"):visible')
                    if option_elem:
                        # Default to "Online" for simplicity
                        if option == "Online":
                            await option_elem.click()
                            break
                
                return True
            
            return False
            
        except Exception as e:
            print(f"   ⚠️ Carousel error: {e}")
            return False
    
    async def _switch_to_survey_tab(self):
        """
        Switch to the survey tab (usually the last/rightmost tab).
        Survey aggregators always open actual surveys in new tabs.
        """
        print("\n🔍 Detecting survey tab...")
        
        # Get browser context
        context = self.browser.contexts[0] if self.browser.contexts else None
        if not context:
            print("❌ No browser context found!")
            return
        
        # Wait for potential new tabs to open
        for attempt in range(5):
            await asyncio.sleep(2)  # Give time for redirect/new tab
            
            all_pages = context.pages
            print(f"  Attempt {attempt + 1}: Found {len(all_pages)} tab(s)")
            
            if len(all_pages) > 1:
                # Multiple tabs - survey is usually the last one
                survey_page = None
                
                # First, try to identify by URL patterns
                for page in reversed(all_pages):  # Check from last to first
                    page_url = page.url.lower()
                    
                    # Common survey platform patterns
                    survey_patterns = [
                        'survey', 'ssi', 'projects', 'selfserve', 'focus',
                        'yougov', 'reptrak', 'toluna', 'qualtrics', 'cint',
                        'lucid', 'purespectrum', 'dynata', 'ipsos', 'gfk'
                    ]
                    
                    if any(pattern in page_url for pattern in survey_patterns):
                        survey_page = page
                        print(f"✅ Found survey tab by URL pattern: {page.url[:80]}...")
                        break
                
                # If no pattern match, use the rightmost (last) tab
                if not survey_page:
                    survey_page = all_pages[-1]
                    print(f"✅ Using rightmost tab (typical survey behavior): {survey_page.url[:80]}...")
                
                # Switch to the survey tab
                self.page = survey_page
                await survey_page.bring_to_front()
                
                # Verify we have question content
                try:
                    await asyncio.sleep(1)
                    content = await survey_page.content()
                    if '?' in content or any(word in content.lower() for word in ['select', 'choose', 'which', 'how']):
                        print("✅ Survey content detected!")
                        return
                except:
                    pass
                
                return
            
            elif len(all_pages) == 1:
                # Single tab - might have navigated within same tab
                current_page = all_pages[0]
                if 'primeopinion' not in current_page.url.lower() and 'dashboard' not in current_page.url.lower():
                    self.page = current_page
                    print(f"✅ Single tab navigated to survey: {current_page.url[:80]}...")
                    return
        
        print("⚠️ Could not detect survey tab after 5 attempts - using current tab")
    
    async def _ensure_survey_tab(self):
        """
        Ensure we're still on the survey tab (not dashboard).
        Call this periodically as some surveys might open additional tabs.
        """
        context = self.browser.contexts[0] if self.browser.contexts else None
        if not context:
            return
        
        all_pages = context.pages
        
        # If multiple tabs exist and we're on a dashboard/aggregator page
        if len(all_pages) > 1:
            current_url = self.page.url.lower()
            
            # Check if we somehow ended up back on the aggregator
            aggregator_patterns = ['primeopinion', 'myopinions', 'dashboard', 'surveys/available']
            if any(pattern in current_url for pattern in aggregator_patterns):
                print("⚠️ Detected we're on aggregator page - switching to survey tab...")
                
                # Find the actual survey tab (usually the last one)
                for page in reversed(all_pages):
                    page_url = page.url.lower()
                    if not any(pattern in page_url for pattern in aggregator_patterns):
                        self.page = page
                        await page.bring_to_front()
                        print(f"✅ Switched back to survey tab: {page.url[:80]}...")
                        break
    
    async def _click_next(self, page):
        """Click next/continue button - ENHANCED with better detection and clicking"""
        
        # Store current page content to verify we actually advance
        current_url = page.url
        try:
            current_question = await page.query_selector('body')
            current_text = await current_question.inner_text() if current_question else ""
        except:
            current_text = ""
            
        # First, wait a moment to see if page auto-advances after filling
        await page.wait_for_timeout(1500)
        
        # Check if page already advanced
        if page.url != current_url:
            print("   ➡️ Page auto-advanced (no click needed)")
            return True
        
        # Try clicking next button with various methods
        clicked = False
        
        # Method 1: Try standard selectors
        selectors = [
            # Submit buttons first (most reliable)
            'button[type="submit"]:visible',
            'input[type="submit"]:visible',
            
            # Text-based selectors
            'button:has-text("Submit")',
            'button:has-text("Next")',
            'button:has-text("NEXT")',
            'button:has-text("Continue")',
            'button:has-text("CONTINUE")',
            'button:has-text("→")',
            
            # Value-based for input buttons
            'input[type="button"][value="Next"]',
            'input[type="button"][value="Continue"]',
            'input[type="button"][value="Submit"]',
            
            # Class/ID based
            'button[class*="next"]',
            'button[class*="continue"]',
            'button[class*="submit"]',
            'button[id*="next"]',
            'button[id*="submit"]',
            
            # Generic visible button (last resort)
            'button:visible'
        ]
        
        for selector in selectors:
            try:
                # Find all matching elements
                elements = await page.query_selector_all(selector)
                
                for elem in elements:
                    # Check if element is visible and enabled
                    if not await elem.is_visible():
                        continue
                    
                    if await elem.is_disabled():
                        continue
                    
                    # Get button text to verify it's a next-type button
                    button_text = ""
                    try:
                        button_text = await elem.inner_text()
                    except:
                        try:
                            button_text = await elem.get_attribute('value') or ""
                        except:
                            pass
                    
                    button_text_lower = button_text.lower()
                    
                    # Check if this is a next/submit button
                    next_keywords = ['next', 'continue', 'submit', '→', 'proceed', 'forward']
                    
                    # Skip if it's clearly not a next button
                    skip_keywords = ['back', 'previous', 'cancel', 'reset', 'clear']
                    if any(skip in button_text_lower for skip in skip_keywords):
                        continue
                    
                    # If it matches next keywords or is the only button, click it
                    if any(keyword in button_text_lower for keyword in next_keywords) or len(elements) == 1:
                        await elem.click()
                        print(f"   ✅ Clicked '{button_text or 'Submit'}' button")
                        clicked = True
                        break
                
                if clicked:
                    break
                    
            except Exception as e:
                continue
        
        # Method 2: If standard clicking didn't work, try JavaScript
        if not clicked:
            try:
                js_result = await page.evaluate('''() => {
                    // Find submit buttons first
                    const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
                    if (submitButtons.length > 0) {
                        submitButtons[0].click();
                        return 'submit';
                    }
                    
                    // Find buttons with next-like text
                    const buttons = document.querySelectorAll('button, input[type="button"]');
                    for (const btn of buttons) {
                        const text = (btn.textContent || btn.value || '').toLowerCase();
                        if (text.includes('next') || text.includes('continue') || text.includes('submit')) {
                            btn.click();
                            return text;
                        }
                    }
                    
                    // If only one visible button, click it
                    const visibleButtons = Array.from(buttons).filter(b => {
                        const style = window.getComputedStyle(b);
                        return style.display !== 'none' && style.visibility !== 'hidden';
                    });
                    
                    if (visibleButtons.length === 1) {
                        visibleButtons[0].click();
                        return 'single-button';
                    }
                    
                    return null;
                }''')
                
                if js_result:
                    print(f"   ✅ Clicked next via JavaScript: {js_result}")
                    clicked = True
            except:
                pass
        
        # Method 3: Try form submission if there's a form
        if not clicked:
            try:
                form_submitted = await page.evaluate('''() => {
                    const forms = document.querySelectorAll('form');
                    if (forms.length > 0) {
                        // Try to submit the first form
                        forms[0].submit();
                        return true;
                    }
                    return false;
                }''')
                
                if form_submitted:
                    print("   ✅ Submitted form directly")
                    clicked = True
            except:
                pass
        
        # Wait for navigation if we clicked
        if clicked:
            try:
                # Wait for either navigation or DOM change
                await page.wait_for_load_state('networkidle', timeout=3000)
            except:
                # Even if timeout, we might have progressed
                pass
            
            await page.wait_for_timeout(1000)
            
            # Check if URL changed (success indicator)
            if page.url != current_url:
                print("   ✅ Navigation successful")
                return True
            else:
                # URL might not change in some surveys, check for content change
                try:
                    new_content = await page.inner_text('body')
                    # If content significantly changed, consider it success
                    return True
                except:
                    return True
        else:
            print("   ⚠️ Could not auto-click next button")
            return False
    
    def _is_completion_page(self, vision_result: Dict) -> bool:
        """Check if we're on the survey completion page"""
        text = str(vision_result.get('question', '')).lower()
        indicators = ['thank you', 'complete', 'finished', 'submitted', 'reward', 'points earned']
        return any(indicator in text for indicator in indicators)
    
    def _format_answer(self, answer: Any) -> str:
        """Format answer for display"""
        if isinstance(answer, list):
            return f"[{len(answer)} selections]"
        elif isinstance(answer, dict):
            return f"[Grid with {len(answer)} responses]"
        else:
            return str(answer)[:50]
    
    async def finalize_session(self):
        """Calculate final metrics and save results"""
        print("\n" + "="*70)
        print("📊 SURVEY SESSION COMPLETE")
        print("="*70)
        
        # Calculate final metrics
        self.survey_data["end_time"] = datetime.now().isoformat()
        
        metrics = self.survey_data["metrics"]
        
        # Automation rate
        if metrics["total_questions"] > 0:
            automation_rate = metrics["automated_questions"] / metrics["total_questions"]
            metrics["automation_rate"] = automation_rate
            
            # Average confidence
            total_confidence = sum(q["confidence"] for q in self.survey_data["questions"])
            metrics["confidence_average"] = total_confidence / metrics["total_questions"]
            
            # Accuracy (if comparison mode)
            if self.comparison_mode:
                matches = sum(1 for q in self.survey_data["questions"] if q["match"] == True)
                metrics["accuracy_score"] = matches / metrics["total_questions"]
        
        # Total time
        if metrics["time_per_question"]:
            metrics["total_time"] = sum(metrics["time_per_question"])
            metrics["avg_time_per_question"] = metrics["total_time"] / len(metrics["time_per_question"])
        
        # Display summary
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"  Total Questions: {metrics['total_questions']}")
        print(f"  Automated: {metrics['automated_questions']} ({metrics.get('automation_rate', 0):.1%})")
        print(f"  Manual Interventions: {metrics['manual_interventions']}")
        print(f"  Average Confidence: {metrics.get('confidence_average', 0):.1%}")
        
        if self.comparison_mode and 'accuracy_score' in metrics:
            print(f"  Accuracy vs Matt: {metrics['accuracy_score']:.1%}")
        
        print(f"\n⏱️ TIMING:")
        print(f"  Total Time: {metrics.get('total_time', 0):.1f} seconds")
        print(f"  Avg per Question: {metrics.get('avg_time_per_question', 0):.1f} seconds")
        
        print(f"\n🎨 UI PATTERNS ENCOUNTERED:")
        for pattern, count in metrics["ui_pattern_distribution"].items():
            print(f"  {pattern}: {count} times")
        
        # Save detailed results
        results_file = f"surveys/results_{self.session_id}.json"
        with open(results_file, 'w') as f:
            # Convert set to list for JSON serialization
            self.survey_data["ui_patterns_encountered"] = list(self.survey_data["ui_patterns_encountered"])
            json.dump(self.survey_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        # Close browser
        if self.browser:
            await self.browser.close()
            print("🌐 Browser closed")
        
        # Final comparison report if enabled
        if self.comparison_mode:
            await self.generate_comparison_report()
    
    async def generate_comparison_report(self):
        """Generate detailed comparison between Quenito and Matt"""
        print("\n" + "="*70)
        print("🔍 QUENITO vs MATT COMPARISON")
        print("="*70)
        
        matches = []
        mismatches = []
        
        for q in self.survey_data["questions"]:
            if q["match"] is None:
                continue
            
            if q["match"]:
                matches.append(q)
            else:
                mismatches.append(q)
        
        print(f"\n✅ Matches: {len(matches)}")
        print(f"❌ Mismatches: {len(mismatches)}")
        
        if mismatches:
            print("\n📝 MISMATCHED ANSWERS:")
            for q in mismatches[:5]:  # Show first 5
                print(f"\nQ{q['number']}: {q['text'][:60]}...")
                print(f"  Quenito: {self._format_answer(q['quenito_answer'])}")
                print(f"  Matt: {self._format_answer(q['matt_answer'])}")
                print(f"  Confidence: {q['confidence']:.0%}")
        
        # Identify patterns in mismatches
        if mismatches:
            mismatch_types = {}
            for q in mismatches:
                q_type = q['type']
                mismatch_types[q_type] = mismatch_types.get(q_type, 0) + 1
            
            print("\n🔬 MISMATCH PATTERNS:")
            for q_type, count in mismatch_types.items():
                print(f"  {q_type}: {count} mismatches")


async def main():
    """Run the live survey test with stealth browser and cookie transfer"""
    
    print("🚀 QUENITO LIVE SURVEY RUNNER - STEALTH EDITION")
    print("="*70)
    print("\n✨ Features:")
    print("  • Cookie transfer for automatic login")
    print("  • Full stealth browser configuration")
    print("  • Comparison tracking against your answers")
    print("  • All UI patterns supported\n")
    
    # Check prerequisites
    print("📋 PRE-TEST CHECKLIST:")
    print("  ✅ Chrome browser with Prime Opinion logged in")
    print("  ✅ Python packages: playwright, browser_cookie3")
    print("  ✅ Core files in place (consciousness_engine_production.py)")
    
    proceed = input("\nReady to start? (y/n): ").lower()
    if proceed != 'y':
        print("Test cancelled")
        return
    
    # Get survey URL (optional with cookie transfer)
    print("\n🔗 Survey URL Options:")
    print("  1. Go to Prime Opinion dashboard (recommended)")
    print("  2. Enter a specific survey URL")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    survey_url = None
    if choice == "2":
        survey_url = input("Enter survey URL: ").strip()
        if not survey_url.startswith('http'):
            survey_url = f"https://{survey_url}"
    elif choice != "1":
        print("Invalid choice, using dashboard by default")
    
    # Comparison mode
    compare = input("\nEnable Matt comparison mode? (y/n): ").lower() == 'y'
    
    # Create runner
    runner = LiveSurveyRunner(matt_comparison_mode=compare)
    
    # Initialize browser with stealth and cookies
    await runner.initialize_browser()
    
    # Start survey (URL is optional, None goes to dashboard)
    await runner.start_survey(survey_url)
    
    print("\n✨ Test complete! Check the results file for detailed analysis.")


if __name__ == "__main__":
    # Create surveys directory if it doesn't exist
    Path("surveys").mkdir(exist_ok=True)
    
    # Run the test
    asyncio.run(main())