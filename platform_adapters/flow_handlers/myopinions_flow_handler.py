# myopinions_flow_handler.py
"""
Complete flow handler for MyOpinions survey automation
Handles: popups, tabs, intermediate pages, consent forms, and captchas
"""

import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import Page

class MyOpinionsFlowHandler:
    """Manages the complete MyOpinions survey flow"""
    
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.context = None
        self.dashboard_page = None
        self.intermediate_page = None
        self.survey_page = None
        
    async def handle_dashboard_popups(self, page: Page) -> bool:
        """
        Handle any popups/overlays on the dashboard
        Returns True if successfully handled all popups
        """
        try:
            print("\n🎯 Checking for popups/overlays...")
            
            # Method 1: Handle promo banner with X close button
            close_buttons = await page.query_selector_all('[class*="close"], [aria-label*="close"], .close-btn, button:has-text("×")')
            
            for button in close_buttons:
                try:
                    if await button.is_visible():
                        print("  📍 Found close button, clicking...")
                        await button.click()
                        await page.wait_for_timeout(1000)
                        print("  ✅ Closed popup/banner")
                except:
                    continue
            
            # Method 2: Handle "No Thanks" style popups
            no_thanks_selectors = [
                'button:has-text("No Thanks")',
                'button:has-text("NO THANKS")',
                'button:has-text("Maybe Later")',
                'button:has-text("Skip")',
                'a:has-text("No Thanks")'
            ]
            
            for selector in no_thanks_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button and await button.is_visible():
                        print(f"  📍 Found '{selector}' button, clicking...")
                        await button.click()
                        await page.wait_for_timeout(1000)
                        print("  ✅ Dismissed popup")
                except:
                    continue
            
            # Method 3: Check for overlay divs and try to close them
            overlays = await page.query_selector_all('[class*="overlay"], [class*="modal"], [class*="popup"]')
            
            for overlay in overlays:
                try:
                    if await overlay.is_visible():
                        # Look for close button within the overlay
                        close_btn = await overlay.query_selector('button, [role="button"], a')
                        if close_btn and ('close' in (await close_btn.get_attribute('class') or '').lower() or
                                         'no' in (await close_btn.inner_text()).lower()):
                            await close_btn.click()
                            await page.wait_for_timeout(1000)
                            print("  ✅ Closed overlay")
                except:
                    continue
                    
            print("✅ Popup handling complete")
            return True
            
        except Exception as e:
            print(f"❌ Error handling popups: {e}")
            return False
    
    async def click_survey_and_handle_tabs(self, survey_info: Dict[str, Any]) -> Page:
        """
        Click survey button and handle tab switching
        Returns the final survey page
        """
        try:
            print(f"\n🎯 Starting survey: {survey_info['points']} points - {survey_info['topic']}")
            
            # Store current page count
            initial_pages = self.context.pages
            
            # Click the survey button
            button = survey_info['element']
            await button.click()
            print("  ✅ Clicked START SURVEY button")
            
            # Wait for new tab to open
            await asyncio.sleep(3)
            
            # Get all pages/tabs
            all_pages = self.context.pages
            
            if len(all_pages) > len(initial_pages):
                # New tab opened - it's the last one
                self.intermediate_page = all_pages[-1]
                print(f"  ✅ New tab opened - total tabs: {len(all_pages)}")
                
                # Switch to intermediate page
                await self.intermediate_page.bring_to_front()
                print("  📍 Switched to intermediate survey page")
                
                # Handle intermediate page
                await self.handle_intermediate_page(self.intermediate_page)
                
                # Now wait for the actual survey tab
                await asyncio.sleep(3)
                all_pages = self.context.pages
                
                if len(all_pages) > 2:
                    # Survey page is the newest tab
                    self.survey_page = all_pages[-1]
                    await self.survey_page.bring_to_front()
                    print("  ✅ Switched to survey page (3rd tab)")
                    return self.survey_page
                    
            else:
                print("  ⚠️ No new tab detected, checking for navigation...")
                return self.dashboard_page
                
        except Exception as e:
            print(f"❌ Error handling tabs: {e}")
            return None
    
    async def handle_intermediate_page(self, page: Page) -> bool:
        """
        Handle the intermediate survey details page
        Click 'START SURVEY NOW' button
        """
        try:
            print("\n📋 Handling intermediate survey page...")
            
            # Wait for page to load
            await page.wait_for_load_state('networkidle')
            
            # Look for START SURVEY NOW button
            start_survey_selectors = [
                'button:has-text("START SURVEY NOW")',
                'button:has-text("Start Survey Now")',
                'a:has-text("START SURVEY NOW")',
                '.btn:has-text("START")',
                'button.btn-primary'
            ]
            
            for selector in start_survey_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button and await button.is_visible():
                        print(f"  ✅ Found START SURVEY NOW button")
                        await button.click()
                        print("  ✅ Clicked - loading actual survey...")
                        return True
                except:
                    continue
                    
            print("  ❌ Could not find START SURVEY NOW button")
            return False
            
        except Exception as e:
            print(f"❌ Error on intermediate page: {e}")
            return False
    
    async def handle_consent_form(self, page: Page) -> bool:
        """
        Handle consent forms with scroll and accept
        """
        try:
            # Check if this is a consent form
            content = await page.inner_text('body')
            content_lower = content.lower()
            
            consent_indicators = [
                'terms and conditions',
                'privacy policy', 
                'consent form',
                'participant information',
                'agreement'
            ]
            
            if not any(indicator in content_lower for indicator in consent_indicators):
                return False
                
            print("\n📜 Consent form detected...")
            
            # Try to find scrollable consent area
            consent_areas = await page.query_selector_all('[class*="consent"], [class*="terms"], #terms, .agreement')
            
            for area in consent_areas:
                try:
                    # Scroll to bottom
                    await area.evaluate('element => element.scrollTop = element.scrollHeight')
                    await page.wait_for_timeout(1000)
                    print("  ✅ Scrolled consent text")
                except:
                    continue
            
            # Look for checkboxes to check
            checkboxes = await page.query_selector_all('input[type="checkbox"]:not(:checked)')
            for checkbox in checkboxes:
                if await checkbox.is_visible():
                    await checkbox.click()
                    print("  ✅ Checked consent checkbox")
            
            # Click accept/continue
            accept_selectors = [
                'button:has-text("I Agree")',
                'button:has-text("Accept")',
                'button:has-text("Continue")',
                'button:has-text("Agree")',
                'button.btn-primary'
            ]
            
            for selector in accept_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button and await button.is_visible():
                        await button.click()
                        print("  ✅ Accepted consent form")
                        return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"❌ Error handling consent: {e}")
            return False
    
    async def detect_captcha(self, page: Page) -> Optional[str]:
        """
        Detect if there's a captcha on the page
        Returns captcha type or None
        """
        try:
            # Common captcha indicators
            captcha_selectors = {
                'recaptcha': '[class*="recaptcha"], #recaptcha, .g-recaptcha',
                'hcaptcha': '[class*="h-captcha"], .h-captcha',
                'text_captcha': 'img[alt*="captcha"], img[src*="captcha"], .captcha-image',
                'funcaptcha': '[id*="funcaptcha"], .funcaptcha'
            }
            
            for captcha_type, selector in captcha_selectors.items():
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"\n🔐 Detected {captcha_type} captcha")
                    return captcha_type
                    
            # Check page content for captcha text
            content = await page.inner_text('body')
            if any(word in content.lower() for word in ['captcha', 'verify you are human', 'security check']):
                print("\n🔐 Detected captcha by text content")
                return 'unknown'
                
            return None
            
        except:
            return None
    
    async def handle_pre_screening(self, page: Page) -> bool:
        """
        Placeholder for pre-screening questions
        Will be expanded based on learning
        """
        print("\n📝 Pre-screening questions detected")
        print("  ⚠️ Manual intervention required for learning phase")
        
        # In future, this will use patterns from knowledge_base.json
        # For now, return False to indicate manual handling needed
        return False
    
    async def run_complete_flow(self, survey_info: Dict[str, Any]) -> bool:
        """
        Execute the complete survey flow from dashboard to completion
        """
        try:
            # Set context from browser manager
            self.context = self.browser.context
            self.dashboard_page = self.browser.page
            
            # Step 1: Handle dashboard popups
            await self.handle_dashboard_popups(self.dashboard_page)
            
            # Step 2: Click survey and handle tabs
            survey_page = await self.click_survey_and_handle_tabs(survey_info)
            
            if not survey_page:
                print("❌ Failed to reach survey page")
                return False
            
            # Step 3: Wait for survey page to load
            await survey_page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # Step 4: Check for consent form
            if await self.handle_consent_form(survey_page):
                await asyncio.sleep(2)
            
            # Step 5: Check for captcha
            captcha_type = await self.detect_captcha(survey_page)
            if captcha_type:
                print(f"  ⚠️ Captcha detected: {captcha_type}")
                print("  ⚠️ Manual captcha solving required (vision integration pending)")
                # Future: Integrate vision system here
                return False
            
            # Step 6: Handle pre-screening
            # For now, this returns False for manual handling
            if not await self.handle_pre_screening(survey_page):
                print("\n✅ Survey page loaded and ready for manual pre-screening")
                print(f"📍 Active tab: {survey_page.url}")
                
            return True
            
        except Exception as e:
            print(f"❌ Flow error: {e}")
            import traceback
            traceback.print_exc()
            return False


# Integration with MyOpinions adapter
async def complete_myopinions_survey(browser_manager, survey_info: Dict[str, Any]) -> bool:
    """
    Complete entry point for MyOpinions survey automation
    """
    flow_handler = MyOpinionsFlowHandler(browser_manager)
    return await flow_handler.run_complete_flow(survey_info)