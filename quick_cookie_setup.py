"""
🍪 Quick Manual Cookie Setup for MyOpinions
Get logged in and save cookies in 2 minutes!
"""

import asyncio
import json
import os
from playwright.async_api import async_playwright

async def quick_cookie_setup():
    """One-time setup to save MyOpinions cookies"""
    
    print("🚀 MyOpinions Cookie Setup")
    print("=" * 50)
    
    # Launch browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,  # Show browser
        args=['--start-maximized']
    )
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        locale='en-AU',
        timezone_id='Australia/Sydney'
    )
    
    page = await context.new_page()
    
    # Go to MyOpinions
    print("\n🌐 Opening MyOpinions login page...")
    await page.goto("https://www.myopinions.com.au/auth/login")
    
    print("\n📝 MANUAL STEPS:")
    print("1. Log into MyOpinions in the browser window")
    print("2. Make sure you can see your dashboard")
    print("3. Press Enter here when you're logged in...")
    
    input("\n⏸️  Press Enter when logged in: ")
    
    # Get current URL
    current_url = page.url
    print(f"\n📍 Current URL: {current_url}")
    
    if "dashboard" in current_url:
        print("✅ Successfully on dashboard!")
    else:
        print("⚠️  Not on dashboard, but continuing anyway...")
    
    # Save cookies
    cookies = await context.cookies()
    
    # Create directory if needed
    os.makedirs("personas/quenito", exist_ok=True)
    
    # Save cookies
    cookie_file = "personas/quenito/myopinions_cookies.json"
    with open(cookie_file, 'w') as f:
        json.dump(cookies, f, indent=2)
    
    print(f"\n✅ Saved {len(cookies)} cookies to {cookie_file}")
    
    # Show some cookie info
    session_cookies = [c for c in cookies if 'session' in c['name'].lower()]
    print(f"🔐 Found {len(session_cookies)} session cookies")
    
    # Take a screenshot
    await page.screenshot(path="myopinions_logged_in.png")
    print("📸 Saved screenshot: myopinions_logged_in.png")
    
    # Close browser
    await browser.close()
    await playwright.stop()
    
    print("\n✅ Setup complete! Your cookies are saved.")
    print("🚀 You can now run the automation with saved cookies")


async def test_saved_cookies():
    """Test if saved cookies work"""
    
    cookie_file = "personas/quenito/myopinions_cookies.json"
    
    if not os.path.exists(cookie_file):
        print("❌ No saved cookies found! Run the setup first.")
        return
    
    # Load cookies
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    
    print(f"📥 Loading {len(cookies)} saved cookies...")
    
    # Launch browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        locale='en-AU',
        timezone_id='Australia/Sydney'
    )
    
    # Add cookies BEFORE navigating
    await context.add_cookies(cookies)
    
    page = await context.new_page()
    
    # Go directly to dashboard
    print("🌐 Navigating to dashboard with cookies...")
    await page.goto("https://www.myopinions.com.au/auth/dashboard")
    
    # Check if we're logged in
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    
    if "dashboard" in current_url and "login" not in current_url:
        print("✅ Successfully logged in with saved cookies!")
        
        # Take screenshot
        await page.screenshot(path="test_cookies_success.png")
        print("📸 Screenshot saved: test_cookies_success.png")
        
        # Look for surveys
        surveys = await page.query_selector_all("div[class*='survey']")
        print(f"📊 Found {len(surveys)} survey elements")
        
    else:
        print(f"❌ Not logged in. Current URL: {current_url}")
        await page.screenshot(path="test_cookies_failed.png")
    
    await browser.close()
    await playwright.stop()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test saved cookies
        asyncio.run(test_saved_cookies())
    else:
        # Setup cookies
        asyncio.run(quick_cookie_setup())
