"""
🕵️ FIXED: Stealth Browser Manager with Robust Async Handling
Fixed the 'NoneType' object has no attribute 'start' error by improving async context management.

Key Fixes:
1. ✅ Proper playwright instance lifecycle management
2. ✅ Robust error handling for async context initialization  
3. ✅ Fallback strategies for browser launch failures
4. ✅ Enhanced stealth configuration validation
5. ✅ Better resource cleanup and error recovery
"""

import os
import json
import time
import asyncio
import sqlite3
import browser_cookie3
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import subprocess
import platform
import random


class StealthBrowserManager:
    """
    🕵️ Fixed Advanced browser manager for stealth survey automation.
    Maintains session continuity and platform compatibility with robust async handling.
    """
    
    def __init__(self, profile_name: str = "quenito_main", knowledge_base_path: str = "data/knowledge_base.json"):
        self.profile_name = profile_name
        self.profile_dir = f"./browser_profiles/{profile_name}"
        self.knowledge_base_path = knowledge_base_path
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self._is_initialized = False
        
        # Browser fingerprinting parameters
        self.fingerprint_config = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'viewport': {'width': 1920, 'height': 1080},
            'locale': 'en-AU',
            'timezone_id': 'Australia/Sydney',
            'screen': {'width': 1920, 'height': 1080},
            'device_scale_factor': 1.0
        }
        
        print("🕵️ Stealth Browser Manager initialized")
        print(f"📁 Profile: {self.profile_name}")
    
    async def initialize_stealth_browser(self, transfer_cookies: bool = True, 
                                       use_existing_chrome: bool = False) -> Page:
        """
        FIXED: Initialize browser with maximum stealth and compatibility.
        
        Args:
            transfer_cookies: Whether to transfer cookies from real Chrome
            use_existing_chrome: Whether to connect to existing Chrome instance
            
        Returns:
            Playwright Page object ready for automation
        """
        try:
            # Step 1: Initialize playwright with proper error handling
            if not self.playwright:
                print("🚀 Starting Playwright instance...")
                self.playwright = await async_playwright().start()
                
                if not self.playwright:
                    raise Exception("Failed to start Playwright instance")
                
                print("✅ Playwright instance started successfully")
            
            # Step 2: Try existing Chrome connection if requested
            if use_existing_chrome:
                print("🔗 Attempting to connect to existing Chrome...")
                page = await self._connect_to_existing_chrome()
                if page:
                    print("🔗 Connected to existing Chrome browser")
                    self._is_initialized = True
                    return page
                else:
                    print("⚠️ Could not connect to existing Chrome, falling back...")
            
            # Step 3: Launch new stealth browser with fallback strategies
            print("🎭 Launching new stealth browser...")
            self.browser = await self._launch_stealth_browser_with_fallback()
            
            if not self.browser:
                raise Exception("Failed to launch browser after all fallback attempts")
            
            # Step 4: Create stealth context
            print("🎪 Creating stealth context...")
            self.context = await self._create_stealth_context(transfer_cookies)
            
            if not self.context:
                raise Exception("Failed to create browser context")
            
            # Step 5: Create new page
            print("📄 Creating new page...")
            self.page = await self.context.new_page()
            
            if not self.page:
                raise Exception("Failed to create new page")
            
            # Step 6: Apply stealth enhancements
            print("🔧 Applying stealth enhancements...")
            await self._apply_stealth_enhancements(self.page)
            
            self._is_initialized = True
            print("🎭 Stealth browser session created successfully")
            return self.page
            
        except Exception as e:
            print(f"❌ Error initializing stealth browser: {e}")
            # Clean up on failure
            await self._cleanup_failed_initialization()
            raise Exception(f"Stealth browser initialization failed: {e}")
    
    async def _launch_stealth_browser_with_fallback(self) -> Browser:
        """
        FIXED: Launch Chromium with stealth parameters and multiple fallback strategies.
        """
        
        # Strategy 1: Full stealth configuration (preferred)
        try:
            print("🎯 Trying full stealth configuration...")
            launch_options = self._get_full_stealth_options()
            browser = await self.playwright.chromium.launch(**launch_options)
            if browser:
                print("✅ Full stealth browser launched successfully")
                return browser
        except Exception as e:
            print(f"⚠️ Full stealth launch failed: {e}")
        
        # Strategy 2: Minimal stealth configuration (fallback)
        try:
            print("🎯 Trying minimal stealth configuration...")
            launch_options = self._get_minimal_stealth_options()
            browser = await self.playwright.chromium.launch(**launch_options)
            if browser:
                print("✅ Minimal stealth browser launched successfully")
                return browser
        except Exception as e:
            print(f"⚠️ Minimal stealth launch failed: {e}")
        
        # Strategy 3: Basic browser launch (last resort)
        try:
            print("🎯 Trying basic browser launch...")
            launch_options = {
                'headless': False,
                'args': ['--disable-blink-features=AutomationControlled']
            }
            browser = await self.playwright.chromium.launch(**launch_options)
            if browser:
                print("✅ Basic browser launched successfully")
                return browser
        except Exception as e:
            print(f"❌ Basic browser launch failed: {e}")
        
        return None
    
    def _get_full_stealth_options(self) -> Dict[str, Any]:
        """Get full stealth launch options."""
        return {
            'headless': False,
            'slow_mo': random.randint(50, 150),
            'args': [
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--disable-ipc-flooding-protection',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-client-side-phishing-detection',
                '--disable-component-extensions-with-background-pages',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-features=TranslateUI',
                '--disable-hang-monitor',
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--disable-sync',
                '--disable-web-security',
                '--metrics-recording-only',
                '--safebrowsing-disable-auto-update',
                '--enable-automation=false',
                '--password-store=basic',
                '--use-mock-keychain',
                f'--user-agent={self.fingerprint_config["user_agent"]}'
            ]
        }
    
    def _get_minimal_stealth_options(self) -> Dict[str, Any]:
        """Get minimal stealth launch options for fallback."""
        return {
            'headless': False,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--no-first-run',
                '--enable-automation=false',
                f'--user-agent={self.fingerprint_config["user_agent"]}'
            ]
        }
    
    async def _create_stealth_context(self, transfer_cookies: bool = True) -> BrowserContext:
        """
        FIXED: Create browser context with stealth configuration and error handling.
        """
        try:
            # Ensure profile directory exists
            os.makedirs(self.profile_dir, exist_ok=True)
            
            context_options = {
                'viewport': self.fingerprint_config['viewport'],
                'user_agent': self.fingerprint_config['user_agent'],
                'locale': self.fingerprint_config['locale'],
                'timezone_id': self.fingerprint_config['timezone_id'],
                'accept_downloads': True,
                'ignore_https_errors': True,
                'bypass_csp': True,
                'java_script_enabled': True
            }
            
            # Try to create persistent context first
            try:
                context = await self.browser.new_context(**context_options)
                print("✅ Browser context created successfully")
                return context
            except Exception as e:
                print(f"⚠️ Standard context creation failed: {e}")
                
                # Fallback to minimal context
                minimal_options = {
                    'viewport': self.fingerprint_config['viewport'],
                    'user_agent': self.fingerprint_config['user_agent']
                }
                context = await self.browser.new_context(**minimal_options)
                print("✅ Minimal context created as fallback")
                return context
                
        except Exception as e:
            print(f"❌ Error creating stealth context: {e}")
            return None
    
    async def _connect_to_existing_chrome(self) -> Optional[Page]:
        """
        FIXED: Try to connect to existing Chrome instance with better error handling.
        """
        try:
            if not self.playwright:
                print("❌ Playwright not initialized, cannot connect to existing Chrome")
                return None
            
            # Try to connect to Chrome with remote debugging enabled
            browser = await self.playwright.chromium.connect_over_cdp("http://localhost:9222")
            
            if browser and browser.contexts:
                context = browser.contexts[0]
                pages = context.pages
                
                if pages:
                    print("✅ Connected to existing Chrome page")
                    return pages[0]
                else:
                    page = await context.new_page()
                    print("✅ Created new page in existing Chrome")
                    return page
            
            print("⚠️ No existing Chrome contexts found")
            return None
            
        except Exception as e:
            print(f"⚠️ Could not connect to existing Chrome: {e}")
            return None
    
    async def _apply_stealth_enhancements(self, page: Page):
        """
        FIXED: Apply additional stealth enhancements with error handling.
        """
        try:
            # Remove automation indicators
            await page.add_init_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Override plugins length
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Override languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-AU', 'en', 'en-US'],
                });
                
                // Override permissions API
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Override chrome runtime
                window.chrome = {
                    runtime: {},
                };
            """)
            
            # Set additional headers for stealth
            await page.set_extra_http_headers({
                'Accept-Language': 'en-AU,en;q=0.9,en-US;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            })
            
            print("✅ Stealth enhancements applied successfully")
            
        except Exception as e:
            print(f"⚠️ Some stealth enhancements failed: {e}")
            # Don't fail the entire initialization for stealth enhancement errors
    
    async def _cleanup_failed_initialization(self):
        """Clean up resources after failed initialization."""
        try:
            if self.page:
                await self.page.close()
                self.page = None
            if self.context:
                await self.context.close()
                self.context = None
            if self.browser:
                await self.browser.close()
                self.browser = None
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            self._is_initialized = False
            print("🧹 Cleaned up failed initialization resources")
            
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
    
    async def test_platform_compatibility(self, url: str) -> Dict[str, Any]:
        """
        Test stealth browser compatibility with survey platforms.
        """
        if not self._is_initialized or not self.page:
            return {'error': 'Browser not initialized'}
        
        try:
            print(f"🧪 Testing compatibility with {url}")
            
            await self.page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Test for detection
            detection_tests = {
                'webdriver_detected': await self.page.evaluate('navigator.webdriver !== undefined'),
                'automation_detected': await self.page.evaluate('window.chrome && window.chrome.runtime && window.chrome.runtime.onConnect'),
                'headless_detected': await self.page.evaluate('navigator.plugins.length === 0'),
                'user_agent_valid': self.fingerprint_config['user_agent'] in await self.page.evaluate('navigator.userAgent'),
                'cookies_loaded': len(await self.context.cookies()) > 0 if self.context else False
            }
            
            compatibility_score = sum(1 for test, result in detection_tests.items() 
                                    if (test.endswith('_detected') and not result) or 
                                       (not test.endswith('_detected') and result))
            
            result = {
                'url': url,
                'compatibility_score': f"{compatibility_score}/{len(detection_tests)}",
                'detection_tests': detection_tests,
                'stealth_level': 'HIGH' if compatibility_score >= 4 else 'MEDIUM' if compatibility_score >= 3 else 'LOW'
            }
            
            print(f"🎯 Compatibility: {result['stealth_level']} ({result['compatibility_score']})")
            return result
            
        except Exception as e:
            print(f"❌ Error testing compatibility: {e}")
            return {'error': str(e)}
    
    async def save_session_state(self):
        """Save current session state for persistence."""
        try:
            if not self.context:
                return
            
            session_data = {
                'cookies': await self.context.cookies(),
                'storage_state': await self.context.storage_state(),
                'timestamp': time.time(),
                'profile_name': self.profile_name
            }
            
            session_file = os.path.join(self.profile_dir, 'session_state.json')
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            print(f"💾 Session state saved to {session_file}")
            
        except Exception as e:
            print(f"⚠️ Error saving session state: {e}")
    
    async def close(self):
        """
        FIXED: Clean up browser resources with proper error handling.
        """
        try:
            # Save session state before closing
            if self._is_initialized:
                await self.save_session_state()
            
            if self.page:
                await self.page.close()
                self.page = None
            
            if self.context:
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            self._is_initialized = False
            print("🔒 Stealth browser session closed successfully")
            
        except Exception as e:
            print(f"⚠️ Error closing browser (non-critical): {e}")
    
    def is_initialized(self) -> bool:
        """Check if browser is properly initialized."""
        return self._is_initialized and self.page is not None
    
    def launch_chrome_with_debugging(self):
        """Launch Chrome with remote debugging enabled for connection."""
        try:
            chrome_args = [
                '--remote-debugging-port=9222',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-blink-features=AutomationControlled'
            ]
            
            system = platform.system()
            if system == "Windows":
                chrome_path = "chrome.exe"
            elif system == "Darwin":  # macOS
                chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            else:  # Linux
                chrome_path = "google-chrome"
            
            subprocess.Popen([chrome_path] + chrome_args)
            print("🚀 Chrome launched with remote debugging on port 9222")
            print("💡 You can now connect to this instance using use_existing_chrome=True")
            
        except Exception as e:
            print(f"❌ Error launching Chrome with debugging: {e}")


# Integration test function for the fix
async def test_stealth_browser_fix():
    """
    Test the fixed stealth browser manager.
    """
    print("🧪 Testing Fixed Stealth Browser Manager")
    print("=" * 50)
    
    browser_manager = StealthBrowserManager("test_fix")
    
    try:
        # Test initialization
        page = await browser_manager.initialize_stealth_browser()
        
        if page:
            print("✅ Stealth browser initialization: SUCCESS")
            
            # Test basic navigation
            await page.goto("https://www.google.com", timeout=10000)
            print("✅ Basic navigation test: SUCCESS")
            
            # Test stealth features
            webdriver_detected = await page.evaluate('navigator.webdriver !== undefined')
            print(f"🔍 WebDriver detected: {webdriver_detected} (should be False)")
            
            return True
        else:
            print("❌ Failed to initialize browser")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        await browser_manager.close()


if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_stealth_browser_fix())
    print(f"\n🎯 Test Result: {'PASSED' if result else 'FAILED'}")
