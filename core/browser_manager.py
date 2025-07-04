"""
Browser Management Module
Handles browser creation, session management, and stealth configuration.
"""

from playwright.sync_api import sync_playwright
import time
import random


class BrowserManager:
    """
    Manages browser sessions with support for both persistent and legacy modes.
    """
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright_instance = None
        
        # Session tracking
        self.session_stats = {
            "start_time": None,
            "manual_navigation_time": None,
            "automation_start_time": None,
            "dashboard_url": None,
            "survey_url": None,
            "tabs_tracked": [],
            "session_transfers": 0,
            "session_mode": None  # "persistent" or "legacy"
        }
    
    def create_persistent_browser_session(self):
        """
        Create a persistent browser session for same-browser automation.
        Eliminates cross-domain authentication issues.
        """
        print("🚀 Creating persistent browser session...")
        
        self.playwright_instance = sync_playwright().start()
        
        # Option 1: Try persistent context (recommended)
        try:
            # Use launch_persistent_context for true session persistence
            self.context = self.playwright_instance.chromium.launch_persistent_context(
                user_data_dir="/tmp/myopinions_session",  # Persistent session directory
                headless=False,  # Must be visible for manual navigation
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                accept_downloads=True,
                ignore_https_errors=True,
                args=self._get_stealth_args()
            )
            
            # Get the browser instance from the context
            self.browser = self.context.browser
            print("✅ Persistent context created successfully")
            
        except Exception as e:
            print(f"⚠️ Persistent context failed: {e}")
            print("🔄 Falling back to regular browser with enhanced session handling...")
            
            # Fallback: Regular browser launch
            self.browser = self.playwright_instance.chromium.launch(
                headless=False,
                args=self._get_stealth_args()
            )
            
            # Create enhanced context
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                accept_downloads=True,
                ignore_https_errors=True
            )
        
        # Enhanced stealth setup for both methods
        self._setup_stealth_scripts()
        
        print("✅ Persistent browser session created")
        self.session_stats["session_mode"] = "persistent"
        return True

    def create_stealth_browser(self, use_existing_session=False):
        """
        Create a browser optimized for survey platforms (legacy method).
        """
        print("🚀 Creating stealth browser session...")
        
        self.playwright_instance = sync_playwright().start()
        
        if use_existing_session:
            # Try to use existing browser session
            try:
                self.browser = self.playwright_instance.chromium.connect_over_cdp("http://localhost:9222")
                # Get existing page
                contexts = self.browser.contexts
                if contexts:
                    self.context = contexts[0]
                    self.page = contexts[0].pages[0] if contexts[0].pages else contexts[0].new_page()
                else:
                    # Fallback to new context
                    self.context = self.browser.new_context()
                    self.page = self.context.new_page()
            except Exception as e:
                print(f"⚠️ Could not connect to existing session: {e}")
                use_existing_session = False
        
        if not use_existing_session:
            self.browser = self.playwright_instance.chromium.launch(
                headless=False,  # Keep visible for research workflows
                args=self._get_stealth_args()
            )
            
            # Survey-optimized context
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},  # Full HD for best compatibility
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            self.page = self.context.new_page()
        
        # Setup stealth scripts
        self._setup_stealth_scripts()
        
        print("✅ Stealth browser session created")
        self.session_stats["session_mode"] = "legacy"
        return True

    def start_manual_navigation_phase(self):
        """
        Phase 1: User manually navigates to survey question.
        Creates dashboard tab and provides instructions.
        """
        print("\n" + "="*80)
        print("📋 PHASE 1: MANUAL NAVIGATION")
        print("="*80)
        
        # Record start time
        self.session_stats["start_time"] = time.time()
        
        # Create dashboard tab
        dashboard_tab = self.context.new_page()
        
        print("🌐 Opening MyOpinions dashboard...")
        dashboard_tab.goto("https://www.myopinions.com.au/auth/dashboard")
        self.session_stats["dashboard_url"] = dashboard_tab.url
        
        print("\n📋 MANUAL NAVIGATION INSTRUCTIONS:")
        print("=" * 60)
        print("1. 🔐 Login to your MyOpinions account (if needed)")
        print("2. 📋 Browse and select the survey you want to complete")
        print("3. 🚀 Click 'START SURVEY' button")
        print("   → This will open the survey in a NEW TAB")
        print("4. 🎯 In the NEW survey tab:")
        print("   • Click 'Start Survey Now' or similar button")
        print("   • Complete any CAPTCHA if required")
        print("   • Complete any consent/agreement forms")
        print("   • Answer any qualifying questions if needed")
        print("   • ⏹️ STOP when you reach the FIRST MAIN survey question")
        print("5. ✅ Return here and press Enter to start automation")
        print("=" * 60)
        print("\n💡 TIP: The automation will take over the survey tab automatically")
        print("💡 TIP: Keep both tabs open - don't close anything!")
        
        # Wait for user to complete manual navigation
        input("\n✋ Press Enter when you've reached the first survey question...")
        
        self.session_stats["manual_navigation_time"] = time.time()
        return dashboard_tab

    def get_all_pages(self):
        """Get all open pages/tabs in the current context."""
        if not self.context:
            return []
        return self.context.pages

    def bring_page_to_front(self, page):
        """Bring a specific page to the front."""
        try:
            page.bring_to_front()
            return True
        except Exception as e:
            print(f"⚠️ Could not bring page to front: {e}")
            return False

    def close_browser(self):
        """Clean up browser resources."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright_instance:
                self.playwright_instance.stop()
            print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")

    def human_like_delay(self, min_ms=1500, max_ms=4000):
        """Generate human-like delays with variation."""
        delay = random.randint(min_ms, max_ms) / 1000
        time.sleep(delay)

    def get_session_stats(self):
        """Get current session statistics."""
        return self.session_stats.copy()

    def update_session_stats(self, **kwargs):
        """Update session statistics."""
        self.session_stats.update(kwargs)

    def _get_stealth_args(self):
        """Get browser arguments for stealth mode."""
        return [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--remote-debugging-port=9222',
            '--enable-features=NetworkService',
            '--disable-site-isolation-trials',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding'
        ]

    def _setup_stealth_scripts(self):
        """Setup stealth scripts to avoid detection."""
        stealth_script = """
            // Remove automation detection
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Prevent automation detection through timing
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: 'granted' }) :
                    originalQuery(parameters)
            );
        """
        
        if self.context:
            self.context.add_init_script(stealth_script)
        
        # Also add to individual page if it exists
        if self.page:
            self.page.add_init_script(stealth_script)

    def set_active_page(self, page):
        """Set the active page for automation."""
        self.page = page
        # Ensure stealth scripts are applied to this page
        self._setup_stealth_scripts()

    def is_browser_ready(self):
        """Check if browser is ready for automation."""
        return (self.browser is not None and 
                self.context is not None and 
                not self.browser.is_connected() == False)

    def get_current_url(self):
        """Get the current page URL."""
        if self.page:
            return self.page.url
        return None

    def navigate_to(self, url):
        """Navigate to a specific URL."""
        if not self.page:
            self.page = self.context.new_page()
        
        try:
            self.page.goto(url)
            self.human_like_delay(2000, 3000)
            return True
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False

    def wait_for_page_load(self, timeout=30000):
        """Wait for page to load completely."""
        if self.page:
            try:
                self.page.wait_for_load_state('networkidle', timeout=timeout)
                return True
            except Exception as e:
                print(f"⚠️ Page load timeout: {e}")
                return False
        return False

    def get_page_content(self):
        """Get the current page content."""
        if self.page:
            try:
                return self.page.inner_text('body')
            except Exception as e:
                print(f"❌ Could not get page content: {e}")
                return ""
        return ""

    def get_page_title(self):
        """Get the current page title."""
        if self.page:
            try:
                return self.page.title()
            except Exception as e:
                print(f"❌ Could not get page title: {e}")
                return ""
        return ""