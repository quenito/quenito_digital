"""
🕵️ Stealth Browser Manager for Survey Platform Compatibility
Handles browser automation with maximum stealth and compatibility across platforms.

Features:
- ✅ Cookie transfer from real Chrome browser
- ✅ Persistent browser profiles  
- ✅ Human-like browser fingerprinting
- ✅ Session continuity management
- ✅ Multi-platform compatibility
- ✅ Detection avoidance strategies
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
    🕵️ Advanced browser manager for stealth survey automation.
    Maintains session continuity and platform compatibility.
    """
    
    def __init__(self, profile_name: str = "quenito_main", knowledge_base_path: str = "data/knowledge_base.json"):
        self.profile_name = profile_name
        self.profile_dir = f"./browser_profiles/{profile_name}"
        self.knowledge_base_path = knowledge_base_path
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        
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
        Initialize browser with maximum stealth and compatibility.
        
        Args:
            transfer_cookies: Whether to transfer cookies from real Chrome
            use_existing_chrome: Whether to connect to existing Chrome instance
            
        Returns:
            Playwright Page object ready for automation
        """
        try:
            # Import and start playwright
            from playwright.async_api import async_playwright
            
            self.playwright = await async_playwright().start()
            
            if use_existing_chrome:
                # Strategy 1: Connect to existing Chrome (highest stealth)
                page = await self._connect_to_existing_chrome()
                if page:
                    print("🔗 Connected to existing Chrome browser")
                    return page
                else:
                    print("⚠️ Could not connect to existing Chrome, falling back...")
            
            # Strategy 2: Persistent context with cookie transfer
            self.browser = await self._launch_stealth_browser()
            self.context = await self._create_stealth_context(transfer_cookies)
            self.page = await self.context.new_page()
            
            # Apply stealth enhancements
            await self._apply_stealth_enhancements(self.page)
            
            print("🎭 Stealth browser session created successfully")
            return self.page
            
        except Exception as e:
            print(f"❌ Error initializing stealth browser: {e}")
            raise
    
    async def _launch_stealth_browser(self) -> Browser:
        """Launch Chromium with stealth parameters."""
        launch_options = {
            'headless': False,  # Headless can be detected
            'slow_mo': random.randint(50, 150),  # Human-like delays
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
                '--no-first-run',
                '--safebrowsing-disable-auto-update',
                '--enable-automation=false',
                '--password-store=basic',
                '--use-mock-keychain',
                f'--user-agent={self.fingerprint_config["user_agent"]}'
            ]
        }
        
        return await self.playwright.chromium.launch(**launch_options)
    
    async def _create_stealth_context(self, transfer_cookies: bool = True) -> BrowserContext:
        """Create browser context with stealth configuration."""
        
        # Ensure profile directory exists
        os.makedirs(self.profile_dir, exist_ok=True)
        
        # For persistent context, we need to use launch_persistent_context
        # For now, create a regular context and handle persistence differently
        context_options = {
            'viewport': self.fingerprint_config['viewport'],
            'user_agent': self.fingerprint_config['user_agent'],
            'locale': self.fingerprint_config['locale'],
            'timezone_id': self.fingerprint_config['timezone_id'],
            'device_scale_factor': self.fingerprint_config['device_scale_factor'],
            'permissions': ['geolocation', 'notifications'],
            'java_script_enabled': True,
            'accept_downloads': True,
            'ignore_https_errors': False,
            'extra_http_headers': {
                'Accept-Language': 'en-AU,en;q=0.9,en-US;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document'
            }
        }
        
        context = await self.browser.new_context(**context_options)
        
        # Transfer cookies from real Chrome browser
        if transfer_cookies:
            await self._transfer_chrome_cookies(context)
        
        return context
    
    async def _transfer_chrome_cookies(self, context: BrowserContext):
        """Transfer cookies from real Chrome browser to Playwright context."""
        try:
            print("🍪 Transferring cookies from Chrome browser...")
            
            # Get cookies from actual Chrome installation
            chrome_cookies = self._get_chrome_cookies()
            
            if chrome_cookies:
                # Add cookies to Playwright context
                await context.add_cookies(chrome_cookies)
                print(f"✅ Transferred {len(chrome_cookies)} cookies from Chrome")
            else:
                print("⚠️ No Chrome cookies found to transfer")
                
        except Exception as e:
            print(f"⚠️ Could not transfer Chrome cookies: {e}")
            print("🔧 Continuing without cookie transfer...")
    
    def _get_chrome_cookies(self) -> List[Dict[str, Any]]:
        """Extract cookies from Chrome browser."""
        try:
            # Try multiple methods to get Chrome cookies
            playwright_cookies = []
            
            # Method 1: browser_cookie3 library
            try:
                chrome_cookies = browser_cookie3.chrome()
                for cookie in chrome_cookies:
                    # Focus on survey platform domains
                    relevant_domains = [
                        'myopinions.com.au', 'qualtrics.com', 'surveymonkey.com',
                        'google.com', 'googleapis.com', 'gstatic.com'
                    ]
                    
                    if any(domain in cookie.domain for domain in relevant_domains):
                        playwright_cookies.append({
                            'name': cookie.name,
                            'value': cookie.value,
                            'domain': cookie.domain,
                            'path': cookie.path,
                            'secure': cookie.secure,
                            'httpOnly': getattr(cookie, 'httpOnly', False),
                            'expires': cookie.expires if cookie.expires else -1
                        })
            except Exception as e:
                print(f"⚠️ browser_cookie3 method failed: {e}")
            
            # Method 2: Direct Chrome cookie database access
            if not playwright_cookies:
                playwright_cookies = self._extract_chrome_cookies_direct()
            
            return playwright_cookies
            
        except Exception as e:
            print(f"❌ Error extracting Chrome cookies: {e}")
            return []
    
    def _extract_chrome_cookies_direct(self) -> List[Dict[str, Any]]:
        """Directly extract cookies from Chrome's SQLite database."""
        try:
            # Locate Chrome user data directory
            if platform.system() == "Windows":
                chrome_user_data = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
            elif platform.system() == "Darwin":  # macOS
                chrome_user_data = os.path.expanduser("~/Library/Application Support/Google/Chrome")
            else:  # Linux
                chrome_user_data = os.path.expanduser("~/.config/google-chrome")
            
            cookies_db = os.path.join(chrome_user_data, "Default", "Cookies")
            
            if not os.path.exists(cookies_db):
                return []
            
            # Copy database to avoid locking issues
            temp_db = "./temp_cookies.db"
            subprocess.run(["copy" if platform.system() == "Windows" else "cp", cookies_db, temp_db], 
                         capture_output=True)
            
            # Extract cookies from database
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, value, host_key, path, secure, httponly, expires_utc 
                FROM cookies 
                WHERE host_key LIKE '%myopinions%' 
                   OR host_key LIKE '%google%'
                   OR host_key LIKE '%qualtrics%'
                   OR host_key LIKE '%surveymonkey%'
            """)
            
            cookies = []
            for row in cursor.fetchall():
                cookies.append({
                    'name': row[0],
                    'value': row[1],
                    'domain': row[2],
                    'path': row[3],
                    'secure': bool(row[4]),
                    'httpOnly': bool(row[5]),
                    'expires': row[6] / 1000000 - 11644473600 if row[6] else -1  # Convert Chrome time
                })
            
            conn.close()
            os.remove(temp_db)
            
            return cookies
            
        except Exception as e:
            print(f"⚠️ Direct cookie extraction failed: {e}")
            return []
    
    async def _connect_to_existing_chrome(self) -> Optional[Page]:
        """Connect to existing Chrome browser instance."""
        try:
            # Try to connect to Chrome with remote debugging enabled
            browser = await self.playwright.chromium.connect_over_cdp("http://localhost:9222")
            
            if browser.contexts:
                context = browser.contexts[0]
                pages = context.pages
                
                if pages:
                    return pages[0]
                else:
                    return await context.new_page()
            
            return None
            
        except Exception as e:
            print(f"⚠️ Could not connect to existing Chrome: {e}")
            return None
    
    async def _apply_stealth_enhancements(self, page: Page):
        """Apply additional stealth enhancements to the page."""
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
                
                // Add realistic screen properties
                Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
                Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
                Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
                Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
            """)
            
            # Set realistic timezone and geolocation
            await page.emulate_timezone(self.fingerprint_config['timezone_id'])
            
            # Add human-like mouse movements
            await page.evaluate("""
                // Add slight mouse movement jitter
                let originalMouse = {
                    move: window.MouseEvent.prototype.initMouseEvent
                };
                
                // Inject realistic timing delays
                const originalClick = window.HTMLElement.prototype.click;
                window.HTMLElement.prototype.click = function() {
                    setTimeout(() => originalClick.call(this), Math.random() * 10);
                };
            """)
            
            print("🎭 Stealth enhancements applied successfully")
            
        except Exception as e:
            print(f"⚠️ Could not apply stealth enhancements: {e}")
    
    async def save_session_state(self):
        """Save current browser session state for future use."""
        try:
            if self.context:
                # Save storage state (cookies, localStorage, sessionStorage)
                storage_state = await self.context.storage_state()
                
                state_file = os.path.join(self.profile_dir, "session_state.json")
                with open(state_file, 'w') as f:
                    json.dump(storage_state, f, indent=2)
                
                print(f"💾 Session state saved to {state_file}")
                
        except Exception as e:
            print(f"❌ Error saving session state: {e}")
    
    async def load_session_state(self):
        """Load previously saved session state."""
        try:
            state_file = os.path.join(self.profile_dir, "session_state.json")
            
            if os.path.exists(state_file):
                with open(state_file, 'r') as f:
                    storage_state = json.load(f)
                
                # Apply storage state to context
                if self.context:
                    await self.context.add_cookies(storage_state.get('cookies', []))
                    
                    # Set localStorage and sessionStorage
                    for origin in storage_state.get('origins', []):
                        if origin.get('localStorage'):
                            await self.page.evaluate(f"""
                                Object.entries({json.dumps(origin['localStorage'])}).forEach(([key, value]) => {{
                                    localStorage.setItem(key, value);
                                }});
                            """)
                
                print("📁 Previous session state loaded")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error loading session state: {e}")
            return False
    
    async def test_platform_compatibility(self, url: str) -> Dict[str, Any]:
        """Test browser compatibility with a survey platform."""
        try:
            print(f"🧪 Testing compatibility with {url}")
            
            await self.page.goto(url, wait_until='networkidle')
            
            # Test for detection
            detection_tests = {
                'webdriver_detected': await self.page.evaluate('navigator.webdriver !== undefined'),
                'automation_detected': await self.page.evaluate('window.chrome && window.chrome.runtime && window.chrome.runtime.onConnect'),
                'headless_detected': await self.page.evaluate('navigator.plugins.length === 0'),
                'user_agent_valid': self.fingerprint_config['user_agent'] in await self.page.evaluate('navigator.userAgent'),
                'cookies_loaded': len(await self.context.cookies()) > 0
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
    
    async def close(self):
        """Clean up browser resources."""
        try:
            # Save session state before closing
            await self.save_session_state()
            
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            print("🔒 Stealth browser session closed")
            
        except Exception as e:
            print(f"❌ Error closing browser: {e}")
    
    def launch_chrome_with_debugging(self):
        """Launch Chrome with remote debugging enabled for connection."""
        try:
            chrome_path = self._get_chrome_path()
            
            if chrome_path:
                debug_port = 9222
                user_data_dir = os.path.join(self.profile_dir, "chrome_debug")
                
                cmd = [
                    chrome_path,
                    f"--remote-debugging-port={debug_port}",
                    f"--user-data-dir={user_data_dir}",
                    "--no-first-run",
                    "--no-default-browser-check"
                ]
                
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"🚀 Chrome launched with debugging on port {debug_port}")
                print("🔗 You can now connect to this instance with connect_to_existing_chrome()")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error launching Chrome with debugging: {e}")
            return False
    
    def _get_chrome_path(self) -> Optional[str]:
        """Get the path to Chrome executable."""
        paths = []
        
        if platform.system() == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]
        elif platform.system() == "Darwin":  # macOS
            paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
        else:  # Linux
            paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        return None


# Usage example and testing
async def main():
    """Example usage of StealthBrowserManager."""
    
    # Initialize stealth browser manager
    stealth_manager = StealthBrowserManager("quenito_myopinions")
    
    try:
        # Option 1: Full stealth with cookie transfer
        page = await stealth_manager.initialize_stealth_browser(
            transfer_cookies=True,
            use_existing_chrome=False
        )
        
        # Test compatibility with MyOpinions
        compatibility = await stealth_manager.test_platform_compatibility("https://myopinions.com.au")
        print(f"📊 Platform compatibility: {compatibility}")
        
        # Navigate to MyOpinions dashboard
        await page.goto("https://myopinions.com.au/dashboard", wait_until='networkidle')
        
        # Check if already logged in
        if "login" in page.url.lower():
            print("🔐 Login required - cookies may not have transferred")
        else:
            print("✅ Successfully accessed dashboard - cookies working!")
        
        # Save session state for next time
        await stealth_manager.save_session_state()
        
    except Exception as e:
        print(f"❌ Error in main: {e}")
    
    finally:
        await stealth_manager.close()


if __name__ == "__main__":
    asyncio.run(main())