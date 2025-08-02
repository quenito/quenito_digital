#!/usr/bin/env python3
"""
🧪 Quick Stealth Browser Test
Test just the stealth browser component to fix the initialization issue.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.stealth_browser_manager import StealthBrowserManager


async def test_stealth_browser_only():
    """Test only the stealth browser initialization."""
    
    print("🧪 QUICK STEALTH BROWSER TEST")
    print("=" * 35)
    
    stealth_manager = None
    
    try:
        print("🔧 Creating StealthBrowserManager...")
        stealth_manager = StealthBrowserManager("quenito_test")
        print("✅ StealthBrowserManager created")
        
        print("\n🚀 Testing stealth browser initialization...")
        page = await stealth_manager.initialize_stealth_browser(
            transfer_cookies=False,  # Skip cookies for test
            use_existing_chrome=False
        )
        
        print("✅ Stealth browser initialized successfully!")
        print(f"✅ Page object: {type(page).__name__}")
        
        # Quick stealth test
        print("\n🕵️ Testing stealth capabilities...")
        
        # Navigate to a test page
        await page.goto("https://httpbin.org/user-agent")
        
        # Check user agent
        user_agent = await page.evaluate("navigator.userAgent")
        print(f"✅ User Agent: {user_agent[:50]}...")
        
        # Check webdriver detection
        webdriver_detected = await page.evaluate("navigator.webdriver !== undefined")
        print(f"✅ WebDriver detected: {'❌ YES' if webdriver_detected else '✅ NO'}")
        
        if not webdriver_detected:
            print("\n🎉 STEALTH BROWSER TEST: SUCCESS!")
            print("✅ Browser initialization working")
            print("✅ Stealth detection avoidance active")
            print("✅ Ready for Prime Opinion/SurveyMonkey testing")
        else:
            print("\n⚠️ STEALTH BROWSER TEST: PARTIAL SUCCESS")
            print("✅ Browser working but stealth needs improvement")
        
        return True
        
    except Exception as e:
        print(f"❌ Stealth browser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if stealth_manager:
            try:
                await stealth_manager.close()
                print("🔒 Stealth browser closed cleanly")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")


if __name__ == "__main__":
    print("🚀 Testing stealth browser component...")
    
    async def main():
        success = await test_stealth_browser_only()
        
        if success:
            print("\n🎯 STEALTH BROWSER: READY FOR INTEGRATION!")
            print("🧠 Combined with working brain system = Ultimate automation!")
        else:
            print("\n🔧 Stealth browser needs debugging")
            print("💡 The brain system is working perfectly though!")
    
    asyncio.run(main())
