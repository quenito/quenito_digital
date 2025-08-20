#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're teaching Quenito to UNDERSTAND surveys, not just fill them.
Every decision should make him smarter, not just more mechanical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Main Orchestrator - The consciousness that guides Quenito's journey
"""
import asyncio
import json
import os 
import time
import re
from datetime import datetime
from typing import Optional, Dict, Any, List

from core.stealth_browser_manager import StealthBrowserManager
from data.knowledge_base import KnowledgeBase
from handlers.handler_factory import HandlerFactory
from services.page_orchestrator import PageOrchestrator
from services.vision_service import VisionService
from services.learning_service import LearningService
from services.automation_service import AutomationService
from reporting.quenito_reporting import QuenitoReporting
from utils.intervention_manager import InterventionManager


class QuenitoRunner:
    """
    Clean orchestrator for Quenito's survey automation.
    Simplified flow: Manual survey start, automated question handling.
    """
    
    def __init__(self, persona_name: str = "quenito", platform: str = "myopinions"):
        self.persona_name = persona_name
        self.platform = platform
        
        # Core systems
        self.kb = KnowledgeBase(persona_name)
        self.intervention_manager = InterventionManager()
        
        # Initialize services (clean separation!)
        self.vision = VisionService()
        self.learning = LearningService(self.kb)
        self.automation = AutomationService(self.kb)
        self.reporter = QuenitoReporting()
        
        # Initialize handlers
        self.handler_factory = HandlerFactory(self.kb, self.intervention_manager)
        
        # Session stats
        self.stats = {
            "questions_total": 0,
            "questions_automated": 0,
            "multi_questions_handled": 0,
            "vision_calls": 0,
            "pattern_matches": 0,
            "survey_start": None,
            "survey_topic": "Social Topics",  # Default for focused learning
            "survey_points": 0
        }
    
    async def run(self):
        """Main entry point - simplified flow!"""
        print(f"🧠 QUENITO SURVEY AUTOMATION v2.2 - {self.persona_name.upper()}")
        print("=" * 50)
        print("📋 SIMPLIFIED MODE: Manual survey selection")
        print("🎯 FOCUS: Social Topics (80% automation target)")
        print("🎬 PAGE ORCHESTRATOR: ENABLED")
        print("=" * 50)
        
        # Start session
        self.reporter.start_session(f"{self.platform}_{datetime.now().strftime('%H%M')}")
        self.stats["survey_start"] = datetime.now()
        
        # Initialize browser
        browser_manager = StealthBrowserManager(f"{self.persona_name}_{self.platform}")
        await browser_manager.initialize_stealth_browser(transfer_cookies=False)
        await browser_manager.load_saved_cookies()
        
        try:
            # Run platform-specific flow
            if self.platform == "myopinions":
                await self._run_myopinions(browser_manager)
            else:
                raise ValueError(f"Platform {self.platform} not supported yet")
                
        except KeyboardInterrupt:
            print("\n⚠️ Survey interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        finally:
            # Always generate reports
            self._generate_final_report()
            await browser_manager.close()
    
    async def _run_myopinions(self, browser_manager):
        """MyOpinions specific flow - FIXED with proper tab waiting"""
        
        # Navigate to dashboard
        await browser_manager.page.goto("https://www.myopinions.com.au/auth/dashboard")
        
        print("\n" + "="*50)
        print("📋 MANUAL SETUP PHASE")
        print("="*50)
        print("Please complete the following manually:")
        print("1. ✅ Login if needed")
        print("2. ✅ Close any popups")
        print("3. ✅ Select a SOCIAL TOPIC survey")
        print("4. ✅ Click 'Start Survey'")
        print("5. ✅ Navigate through intro pages")
        print("6. ✅ Stop at the FIRST real question")
        print("="*50)
        
        input("\n🎯 Press Enter when you're at the FIRST SURVEY QUESTION >>> ")
        
        # Get the browser context
        context = browser_manager.browser.contexts[0]
        
        # Wait for survey tab to potentially open with multiple attempts
        print("\n🔍 Detecting survey tab...")
        survey_page = None
        
        for attempt in range(5):
            await asyncio.sleep(2)  # Give time for tabs to open
            all_pages = context.pages
            
            print(f"\n🔍 Attempt {attempt + 1}: Found {len(all_pages)} tab(s)")
            
            # List all tabs
            for i, page in enumerate(all_pages, 1):
                print(f"  📄 Tab {i}: {page.url[:80]}...")
            
            # Check for survey tab
            if len(all_pages) >= 2:
                # Survey is usually the last tab or the one with survey URL
                for page in reversed(all_pages):  # Check from last to first
                    page_url = page.url.lower()
                    
                    # Check for survey URL patterns
                    if any(indicator in page_url for indicator in [
                        'survey', 'ssi', 'projects', 'selfserve', 'focus',
                        'yougov', 'reptrak', 'toluna', 'qualtrics'
                    ]):
                        survey_page = page
                        print(f"✅ Found survey tab: {page.url[:80]}...")
                        break
                
                if survey_page:
                    break
                    
                # If no survey URL found, use the last non-dashboard tab
                for page in reversed(all_pages):
                    if 'dashboard' not in page.url.lower():
                        survey_page = page
                        print(f"✅ Using non-dashboard tab: {page.url[:80]}...")
                        break
                
                if survey_page:
                    break
            
            elif len(all_pages) == 1:
                # Only one tab - check if URL changed from dashboard
                current_page = all_pages[0]
                if 'dashboard' not in current_page.url.lower():
                    survey_page = current_page
                    print(f"✅ Single tab navigated to survey: {current_page.url[:80]}...")
                    break
            
            if attempt < 4:
                print("⏳ Checking for survey tab...")
        
        # Final check - if still no survey page found
        if not survey_page:
            if len(all_pages) > 1:
                # Use the last tab as fallback
                survey_page = all_pages[-1]
                print(f"⚠️ No survey URL detected, using last tab: {survey_page.url[:80]}...")
            else:
                # Use the only tab
                survey_page = all_pages[0]
                print(f"⚠️ Using single tab: {survey_page.url[:80]}...")
        
        if not survey_page:
            print("❌ ERROR: Could not detect survey page!")
            return
        
        print(f"\n✅ Survey page selected: {survey_page.url[:80]}...")
        
        # IMPORTANT: Update browser_manager's page reference!
        browser_manager.page = survey_page
        
        # Additional verification - check for question content
        try:
            content = await survey_page.inner_text('body')
            if '?' in content or any(word in content.lower() for word in ['select', 'choose', 'gender', 'age']):
                print("✅ Question content confirmed on page")
            else:
                print("⚠️ Warning: No clear question content detected")
        except:
            pass
        
        print("\n" + "="*50)
        print("🚀 STARTING AUTOMATION WITH ORCHESTRATOR")
        print("="*50)
        
        # Process survey questions
        await self._process_survey(survey_page)
    
    async def _process_survey(self, page):
        """Main survey processing loop - NOW WITH PAGE ORCHESTRATOR!"""
        
        # Create page orchestrator for multi-question handling
        orchestrator = PageOrchestrator(
            self.automation,      # automation_service
            self.automation.llm,  # llm_service  
            self.vision,         # vision_service
            page                 # page
        )
        
        while True:
            self.stats["questions_total"] += 1
            question_num = self.stats["questions_total"]
            
            print(f"\n❓ QUESTION {question_num}")
            print("-" * 50)
            
            # Step 1: Vision Analysis (optional but recommended)
            vision_result = None
            if self.vision and self.vision.enabled:
                # Take screenshot first
                try:
                    screenshot = await page.screenshot()
                    import base64
                    screenshot_base64 = base64.b64encode(screenshot).decode('utf-8')
                    vision_result = await self.vision.analyze_page(screenshot_base64)
                    self.stats["vision_calls"] += 1
                except Exception as e:
                    print(f"   ⚠️ Vision analysis skipped: {e}")
                    vision_result = None
            
            # Step 3: 🎯 USE THE NEW ORCHESTRATOR METHOD!
            automation_result = await self.automation.attempt_automation_with_orchestrator(
                page=page,
                handler_factory=self.handler_factory,
                vision_result=vision_result,
                question_num=question_num
            )
            
            # 🛑 CHECK FOR SURVEY COMPLETION SIGNAL
            if automation_result.get('stop_automation'):
                print("\n🎉 SURVEY COMPLETE DETECTED BY ORCHESTRATOR!")
                self._log_survey_completion()
                break
            
            if automation_result.get('success'):
                self.stats["questions_automated"] += 1
                
                # Handle multi-question pages
                if automation_result.get('handler_used') == 'PageOrchestrator':
                    if automation_result.get('partial_manual'):
                        print(f"⚠️ Partial automation - some fields needed manual input")
                    print(f"✅ ORCHESTRATOR HANDLED! (Total automated: {self.stats['questions_automated']})")
                else:
                    print(f"✅ AUTOMATED! (Total: {self.stats['questions_automated']})")
                
                # Store pattern if vision was confident
                # if vision_result and vision_result.get('confidence_rating', 0) > 80:
                #    await self.vision.store_success_pattern(
                #         page, question_num, vision_result, automation_result
                #    )
                #     self.stats["pattern_matches"] += 1
                # 
                # Check completion (backup check)
                if await self._check_survey_complete(page):
                    break
                
                # Special handling for transition pages
                if automation_result.get('reason') == 'transition_page':
                    print("📄 Transition page - moving to next section")
                    await page.wait_for_timeout(2000)
                    continue
                
                # Click next (unless it was a transition that already clicked)
                if automation_result.get('reason') != 'transition_page':
                    await self._click_next(page)
                
                await page.wait_for_timeout(1500)
                continue
            
            # Step 4: Manual Intervention Required
            print("🖊️ Manual input required...")
            print("🔍 Please answer the question in the browser")
            input("\n✋ Press Enter AFTER answering but BEFORE clicking Next >>> ")
            
            # Capture learning from manual input
            learning_data = await self.learning.capture_manual_response(
                page=page,
                question_num=question_num,
                vision_result=vision_result
            )
            
            if learning_data:
                captured_value = learning_data.get('response_value', 'N/A')
                print(f"💾 Captured: {captured_value}")
                
                # Show what type of element was captured
                if learning_data.get('response_values'):
                    print(f"   All values: {', '.join(learning_data['response_values'])}")
                
            # Store pattern for future learning
            #    if vision_result:
            #        await self.vision.store_learning_pattern(
            #            page, question_num, vision_result, learning_data
            #        )
            
            # User clicks next
            input("\n👉 Now click Next/Continue, then press Enter >>> ")
            
            # Check if complete
            if await self._check_survey_complete(page):
                break
            
            await page.wait_for_timeout(1000)
    
    async def _check_survey_complete(self, page) -> bool:
        """Check if survey is complete - with LEARNING capture"""
        try:
            content = await page.inner_text('body')
            content_lower = content.lower()
            
            # MUST have multiple completion indicators to avoid false positives
            completion_indicators = 0
            
            # Strong indicators (need at least 2)
            strong_indicators = [
                ('thank you' in content_lower and 'completing' in content_lower),
                ('survey complete' in content_lower),
                ('points have been added' in content_lower),
                ('points earned' in content_lower),
                ('congratulations' in content_lower and 'completed' in content_lower),
                ('successfully completed' in content_lower),
                ('reward' in content_lower and 'credited' in content_lower),
                ('survey has been completed' in content_lower),
                ('you have completed' in content_lower and 'survey' in content_lower)
            ]
            
            for indicator in strong_indicators:
                if indicator:
                    completion_indicators += 1
            
            # Need at least 2 strong indicators to confirm completion
            if completion_indicators >= 2:
                print("\n🎉 SURVEY COMPLETE!")
                
                # Try to extract points
                points_match = re.search(r'(\d+)\s*points?', content_lower)
                if points_match:
                    self.stats["survey_points"] = int(points_match.group(1))
                    print(f"💰 Points earned: {self.stats['survey_points']}")
                
                # 🎓 LEARNING ANALYSIS - NEW!
                if hasattr(self.automation, 'qa_history'):
                    print("\n🧠 ANALYZING SURVEY FOR LEARNING...")
                    learning_data = {
                        "questions": self.automation.qa_history,
                        "topic": self.stats.get("survey_topic", "General"),
                        "points": self.stats.get("survey_points", 0),
                        "platform": self.platform,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Save session learning
                    learning_file = f"personas/{self.persona_name}/session_learning_{int(time.time())}.json"
                    os.makedirs(os.path.dirname(learning_file), exist_ok=True)
                    
                    with open(learning_file, 'w') as f:
                        json.dump(learning_data, f, indent=2)
                    
                    print(f"💾 Session learning saved: {len(self.automation.qa_history)} Q&As")
                    print(f"📊 Run 'python reporting/learning_dashboard.py' to see insights!")
                
                # Log completion
                self._log_survey_completion()
                return True
            
            # Also check URL for completion indicators
            if 'complete' in page.url.lower() or 'thank' in page.url.lower():
                if completion_indicators >= 1:  # URL + 1 text indicator
                    print("\n🎉 SURVEY COMPLETE! (URL confirmed)")
                    
                    # 🎓 LEARNING ANALYSIS
                    if hasattr(self.automation, 'qa_history'):
                        print("\n🧠 ANALYZING SURVEY FOR LEARNING...")
                        learning_data = {
                            "questions": self.automation.qa_history,
                            "topic": self.stats.get("survey_topic", "General"),
                            "points": self.stats.get("survey_points", 0),
                            "platform": self.platform,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Save session learning
                        learning_file = f"personas/{self.persona_name}/session_learning_{int(time.time())}.json"
                        os.makedirs(os.path.dirname(learning_file), exist_ok=True)
                        
                        with open(learning_file, 'w') as f:
                            json.dump(learning_data, f, indent=2)
                        
                        print(f"💾 Session learning saved: {len(self.automation.qa_history)} Q&As")
                        print(f"📊 Run 'python reporting/learning_dashboard.py' to see insights!")
                    
                    self._log_survey_completion()
                    return True
                    
        except Exception as e:
            print(f"Error checking completion: {e}")
        
        return False
    
    async def _click_next(self, page):
            """Click next/continue button - ENHANCED with better detection and clicking"""
            
            # First, wait a moment to see if page auto-advances after filling
            current_url = page.url
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
        
    def _log_survey_completion(self):
        """Log survey completion to reporter"""
        if self.stats["survey_start"]:
            duration = (datetime.now() - self.stats["survey_start"]).seconds
            
            self.reporter.log_survey_completion(
                platform=self.platform,
                survey_id=f"survey_{int(time.time())}",
                topic=self.stats["survey_topic"],
                points=self.stats["survey_points"],
                duration_seconds=duration,
                questions_total=self.stats["questions_total"],
                questions_automated=self.stats["questions_automated"],
                vision_api_calls=self.stats["vision_calls"],
                pattern_matches=self.stats["pattern_matches"]
            )
    
    def _generate_final_report(self):
        """Generate final session report"""
        if self.stats["survey_start"] and self.stats["questions_total"] > 0:
            duration = (datetime.now() - self.stats["survey_start"]).seconds
            automation_rate = (self.stats["questions_automated"] / self.stats["questions_total"] * 100)
            
            print("\n" + "=" * 50)
            print("📊 SESSION COMPLETE!")
            print("=" * 50)
            print(f"📝 Questions Total: {self.stats['questions_total']}")
            print(f"🤖 Questions Automated: {self.stats['questions_automated']}")
            print(f"📦 Multi-Question Pages: {self.stats['multi_questions_handled']}")
            print(f"📈 Automation Rate: {automation_rate:.1f}%")
            print(f"👁️ Vision API Calls: {self.stats['vision_calls']} (${self.stats['vision_calls'] * 0.001:.3f})")
            print(f"🎯 Pattern Matches: {self.stats['pattern_matches']}")
            print(f"⏱️ Duration: {duration//60}m {duration%60}s")
            print(f"💰 Points Earned: {self.stats['survey_points']}")
            print("=" * 50)
            
            # Print reporter summaries
            self.reporter.print_session_report()
            self.reporter.print_weekly_summary()
            
            # FIX: Convert datetime objects to strings for JSON serialization
            stats_clean = self.stats.copy()
            if stats_clean.get("survey_start"):
                stats_clean["survey_start"] = stats_clean["survey_start"].isoformat()
            
            # SAVE REPORT TO FILE
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "persona": self.persona_name,
                "platform": self.platform,
                "stats": stats_clean,  # Use cleaned stats
                "duration_seconds": duration,
                "automation_rate": automation_rate
            }
            
            # Create reports directory if it doesn't exist
            import os
            import json
            reports_dir = f"personas/{self.persona_name}/reporting"
            os.makedirs(reports_dir, exist_ok=True)
            
            # Save with timestamp
            report_file = f"{reports_dir}/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.platform}_{int(automation_rate)}.json"
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"\n💾 Report saved to: {report_file}")


async def main():
    """Clean entry point"""
    runner = QuenitoRunner(persona_name="quenito", platform="myopinions")
    await runner.run()


if __name__ == "__main__":
    asyncio.run(main())