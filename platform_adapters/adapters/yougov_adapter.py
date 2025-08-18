# yougov_adapter.py
"""
YouGov Platform Adapter for Quenito Survey Assistant
Handles YouGov AU survey automation with vision support
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from platform_adapters.base_adapter import BasePlatformAdapter

logger = logging.getLogger(__name__)

class YouGovAdapter(BasePlatformAdapter):
    """
    YouGov platform adapter for Australian surveys
    Points system: 5,000 points = $20 AUD
    """
    
    def __init__(self, browser_manager, persona: str = "quenito"):
        super().__init__(browser_manager, persona)
        self.platform_name = "yougov"
        self.base_url = "https://account.yougov.com/au-en/account"
        
        # YouGov specific selectors
        self.selectors = {
            # Dashboard elements
            'points_display': 'span:has-text("points")',
            'hi_greeting': 'text=/Hi\\s+Matt/',
            
            # Survey cards
            'survey_card': 'div:has-text("Research survey")',
            'start_button': 'button:has-text("Start now")',
            'survey_link': 'a[href*="/surveys/"]',
            
            # Survey elements  
            'question_text': '[data-testid="question-text"], .question-text, h2.question',
            'radio_button': 'input[type="radio"]',
            'checkbox': 'input[type="checkbox"]',
            'text_input': 'input[type="text"], textarea',
            'select_dropdown': 'select',
            'continue_button': 'button:has-text("Continue"), button:has-text("Next")',
            'submit_button': 'button:has-text("Submit"), button:has-text("Done")',
            
            # Navigation
            'progress_bar': '.progress-bar, [role="progressbar"]',
            'back_button': 'button:has-text("Back"), button:has-text("Previous")',
            
            # Completion
            'completion_text': 'text=/thank you|survey complete|points added/i',
            'error_message': '.error-message, .alert-danger'
        }
        
        # YouGov specific patterns
        self.yougov_patterns = {
            "grid_questions": [
                "How much do you agree",
                "Rate the following",
                "Please indicate"
            ],
            "screening_questions": [
                "Are you the primary",
                "Do you make decisions",
                "Which of these applies"
            ],
            "completion_urls": [
                "/surveys/success",
                "/surveys/complete",
                "account.yougov.com/au-en/account"
            ]
        }
        
    async def login(self, email: str = None, password: str = None) -> bool:
        """
        Login to YouGov account
        """
        try:
            logger.info("Navigating to YouGov login page...")
            await self.browser.page.goto(self.base_url)
            await asyncio.sleep(2)
            
            # Check if already logged in
            if await self.browser.page.locator(self.selectors['hi_greeting']).count() > 0:
                logger.info("Already logged in to YouGov!")
                return True
            
            # Manual login prompt for now
            logger.info("Please login to YouGov manually")
            input("Press Enter when logged in >>> ")
            
            # Verify login success
            await self.browser.page.wait_for_selector(self.selectors['points_display'], timeout=10000)
            logger.info("Successfully logged in to YouGov!")
            
            # Save cookies
            await self.save_cookies()
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    async def detect_available_surveys(self) -> List[Dict]:
        """
        Find available surveys on YouGov dashboard
        """
        surveys = []
        try:
            logger.info("Detecting available YouGov surveys...")
            
            # Wait for page to load
            await asyncio.sleep(2)
            
            # Look for survey cards
            survey_cards = await self.browser.page.locator(self.selectors['survey_card']).all()
            
            for idx, card in enumerate(survey_cards):
                try:
                    # Get survey details
                    survey_info = {
                        'index': idx,
                        'platform': 'yougov',
                        'card_element': card,
                        'detected_at': datetime.now().isoformat()
                    }
                    
                    # Try to get points value if visible
                    points_text = await card.locator('text=/[0-9]+ points/').text_content()
                    if points_text:
                        survey_info['points'] = int(''.join(filter(str.isdigit, points_text)))
                    
                    # Check for start button
                    start_btn = card.locator(self.selectors['start_button'])
                    if await start_btn.count() > 0:
                        survey_info['has_start_button'] = True
                        survey_info['start_element'] = start_btn
                    
                    surveys.append(survey_info)
                    logger.info(f"Found survey #{idx}: {survey_info.get('points', 'Unknown')} points")
                    
                except Exception as e:
                    logger.warning(f"Error processing survey card {idx}: {e}")
                    continue
            
            logger.info(f"Total surveys found: {len(surveys)}")
            return surveys
            
        except Exception as e:
            logger.error(f"Error detecting surveys: {e}")
            return []
    
    async def start_survey(self, survey: Dict) -> bool:
        """
        Start a specific YouGov survey
        """
        try:
            logger.info(f"Starting YouGov survey: {survey.get('points', 'Unknown')} points")
            
            # Click start button
            if 'start_element' in survey:
                await survey['start_element'].click()
            elif 'card_element' in survey:
                start_btn = survey['card_element'].locator(self.selectors['start_button'])
                await start_btn.click()
            else:
                logger.error("No start element found for survey")
                return False
            
            # Wait for survey to load
            await asyncio.sleep(3)
            
            # Check if new tab opened
            all_pages = self.browser.context.pages
            if len(all_pages) > 1:
                # Switch to survey tab
                self.browser.page = all_pages[-1]
                await self.browser.page.bring_to_front()
                logger.info("Switched to survey tab")
            
            # Wait for first question
            await self.browser.page.wait_for_selector(
                self.selectors['question_text'],
                timeout=10000
            )
            
            logger.info("Survey started successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start survey: {e}")
            return False
    
    async def handle_survey_question(self, question_data: Dict) -> Dict:
        """
        Handle a YouGov survey question using Quenito's knowledge
        """
        result = {
            'success': False,
            'question': question_data.get('text', ''),
            'action_taken': None,
            'confidence': 0
        }
        
        try:
            # Get question text
            question_text = question_data.get('text', '')
            
            # Determine question type
            element_type = await self.detect_element_type()
            
            # Use vision if available
            if self.browser.vision_enabled:
                vision_result = await self.use_vision_for_question(question_text)
                if vision_result['success']:
                    result.update(vision_result)
                    return result
            
            # Handle based on element type
            if element_type == 'radio':
                result = await self.handle_radio_question(question_text)
            elif element_type == 'checkbox':
                result = await self.handle_checkbox_question(question_text)
            elif element_type == 'text':
                result = await self.handle_text_question(question_text)
            elif element_type == 'select':
                result = await self.handle_select_question(question_text)
            elif element_type == 'grid':
                result = await self.handle_grid_question(question_text)
            else:
                logger.warning(f"Unknown element type: {element_type}")
                result['requires_manual'] = True
            
            return result
            
        except Exception as e:
            logger.error(f"Error handling question: {e}")
            result['error'] = str(e)
            return result
    
    async def detect_element_type(self) -> str:
        """
        Detect the type of survey element on current page
        """
        try:
            # Check for different element types
            if await self.browser.page.locator('input[type="radio"]').count() > 0:
                return 'radio'
            elif await self.browser.page.locator('input[type="checkbox"]').count() > 0:
                return 'checkbox'
            elif await self.browser.page.locator('textarea, input[type="text"]').count() > 0:
                return 'text'
            elif await self.browser.page.locator('select').count() > 0:
                return 'select'
            elif await self.browser.page.locator('table input, .grid-question').count() > 0:
                return 'grid'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    async def check_survey_completion(self) -> bool:
        """
        Check if YouGov survey is complete
        """
        try:
            # Check URL
            current_url = self.browser.page.url
            for completion_url in self.yougov_patterns['completion_urls']:
                if completion_url in current_url:
                    logger.info("Survey completed - URL match!")
                    return True
            
            # Check for completion text
            completion_element = await self.browser.page.locator(
                self.selectors['completion_text']
            ).count()
            
            if completion_element > 0:
                logger.info("Survey completed - completion message found!")
                return True
            
            # Check if back on dashboard
            if self.base_url in current_url:
                logger.info("Back on dashboard - survey likely complete")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking completion: {e}")
            return False
    
    async def save_cookies(self):
        """
        Save YouGov cookies for session persistence
        """
        try:
            cookies = await self.browser.context.cookies()
            cookies_path = Path(f"personas/{self.persona}/yougov_cookies.json")
            cookies_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(cookies_path, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            logger.info(f"Saved YouGov cookies to {cookies_path}")
            
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    async def load_cookies(self):
        """
        Load saved YouGov cookies
        """
        try:
            cookies_path = Path(f"personas/{self.persona}/yougov_cookies.json")
            if cookies_path.exists():
                with open(cookies_path, 'r') as f:
                    cookies = json.load(f)
                
                await self.browser.context.add_cookies(cookies)
                logger.info("Loaded saved YouGov cookies")
                return True
                
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
        
        return False
    
    async def run_survey_session(self, max_surveys: int = 5) -> Dict:
        """
        Run a complete YouGov survey session
        """
        session_results = {
            'platform': 'yougov',
            'persona': self.persona,
            'start_time': datetime.now().isoformat(),
            'surveys_completed': 0,
            'total_points': 0,
            'automation_rate': 0,
            'errors': []
        }
        
        try:
            # Login if needed
            if not await self.login():
                session_results['errors'].append("Login failed")
                return session_results
            
            for survey_num in range(max_surveys):
                logger.info(f"\n{'='*50}")
                logger.info(f"Survey attempt #{survey_num + 1}")
                
                # Detect available surveys
                surveys = await self.detect_available_surveys()
                if not surveys:
                    logger.info("No surveys available")
                    break
                
                # Start first available survey
                survey = surveys[0]
                if not await self.start_survey(survey):
                    logger.error("Failed to start survey")
                    continue
                
                # Run survey automation
                survey_result = await self.automate_survey()
                
                # Update session results
                if survey_result['completed']:
                    session_results['surveys_completed'] += 1
                    session_results['total_points'] += survey.get('points', 0)
                
                # Check if back on dashboard
                await asyncio.sleep(3)
                if not await self.check_survey_completion():
                    logger.warning("Survey may not have completed properly")
                
                # Return to dashboard
                await self.browser.page.goto(self.base_url)
                await asyncio.sleep(2)
            
            # Calculate final automation rate
            if session_results['surveys_completed'] > 0:
                # This would come from actual tracking
                session_results['automation_rate'] = 70  # Placeholder
            
        except Exception as e:
            logger.error(f"Session error: {e}")
            session_results['errors'].append(str(e))
        
        finally:
            session_results['end_time'] = datetime.now().isoformat()
            
            # Save session report
            self.save_session_report(session_results)
        
        return session_results
    
    def save_session_report(self, results: Dict):
        """
        Save YouGov session report
        """
        try:
            reports_dir = Path(f"personas/{self.persona}/reporting/yougov")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = reports_dir / f"session_{timestamp}.json"
            
            with open(report_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Session report saved to {report_path}")
            
            # Print summary
            print("\n" + "="*50)
            print("YOUGOV SESSION COMPLETE!")
            print("="*50)
            print(f"Surveys Completed: {results['surveys_completed']}")
            print(f"Total Points Earned: {results['total_points']}")
            print(f"Automation Rate: {results['automation_rate']}%")
            print("="*50)
            
        except Exception as e:
            logger.error(f"Failed to save report: {e}")

# Usage example
if __name__ == "__main__":
    async def test_yougov():
        from core.stealth_browser_manager import StealthBrowserManager
        
        # Initialize browser
        browser = StealthBrowserManager("quenito_yougov")
        await browser.initialize_stealth_browser()
        
        # Create adapter
        adapter = YouGovAdapter(browser, "quenito")
        
        # Run session
        results = await adapter.run_survey_session(max_surveys=3)
        
        print(f"Session complete: {results}")
    
    # Run test
    asyncio.run(test_yougov())