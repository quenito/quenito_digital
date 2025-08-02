"""
Quick debug script to find the right selectors
Run this to see what's on the page
"""

import asyncio
from core.stealth_browser_manager import StealthBrowserManager
from playwright.async_api import Page

async def debug_myopinions_selectors():
    """Debug script to find correct selectors"""
    
    print("🔍 MyOpinions Selector Debug")
    print("="*40)
    
    browser = StealthBrowserManager("quenito_myopinions")
    
    try:
        # Initialize and load cookies
        await browser.initialize_stealth_browser(transfer_cookies=False)
        
        # Load saved cookies
        await browser.load_saved_cookies()
        
        # Navigate to dashboard
        print("\n📍 Navigating to dashboard...")
        await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
        await browser.page.wait_for_timeout(5000)  # Wait 5 seconds
        
        # Take screenshot
        await browser.page.screenshot(path="debug_dashboard.png")
        print("📸 Screenshot saved: debug_dashboard.png")
        
        # Try different selectors
        print("\n🔍 Testing selectors...")
        
        selectors_to_try = [
            # Button-based
            "button:has-text('START SURVEY')",
            "button.start-survey",
            "a.start-survey",
            
            # Container-based
            "div:has(button:has-text('START SURVEY'))",
            "[class*='survey-item']",
            "[class*='survey-card']",
            
            # Points-based
            "div:has-text('points')",
            "*:has-text('220 points')",
            
            # Generic
            "div.card",
            "article",
            "section:has(button)",
            
            # By parent structure
            "#root div div div div:has(button)",
            "main div:has(button:has-text('START'))"
        ]
        
        for selector in selectors_to_try:
            try:
                elements = await browser.page.query_selector_all(selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with: {selector}")
                    
                    # Get sample text from first element
                    if elements:
                        try:
                            text = await elements[0].inner_text()
                            print(f"   Sample text: {text[:100]}...")
                        except:
                            pass
            except Exception as e:
                print(f"❌ Error with selector {selector}: {e}")
        
        # Get page structure
        print("\n📄 Getting page HTML structure...")
        
        # Find survey container area
        survey_area = await browser.page.query_selector("div:has(h2:has-text('SURVEYS'))")
        if survey_area:
            html = await survey_area.inner_html()
            # Save for analysis
            with open("survey_area.html", "w") as f:
                f.write(html)
            print("💾 Saved survey area HTML to survey_area.html")
        
        # Try to get all text with "points"
        points_elements = await browser.page.query_selector_all("*:has-text(' points')")
        print(f"\n🎯 Found {len(points_elements)} elements containing 'points'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await browser.close()
        print("\n✅ Debug complete - check debug_dashboard.png and survey_area.html")

if __name__ == "__main__":
    asyncio.run(debug_myopinions_selectors())