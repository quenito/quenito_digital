# Quick test script using your existing system
import asyncio
from core.stealth_browser_manager import StealthBrowserManager

async def quick_myopinions_test():
    browser = StealthBrowserManager("quenito_myopinions")
    
    try:
        page = await browser.initialize_stealth_browser(transfer_cookies=True)
        await page.goto("https://www.myopinions.com.au/auth/dashboard")
        
        # Check if logged in
        current_url = page.url
        if "dashboard" in current_url:
            print("✅ MyOpinions access successful!")
        else:
            print(f"❌ Not on dashboard: {current_url}")
            
    finally:
        await browser.close()

asyncio.run(quick_myopinions_test())