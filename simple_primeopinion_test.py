#!/usr/bin/env python3
"""
🧪 Simple Prime Opinion Stealth Test
Tests ONLY cookie transfer and dashboard access - no file conflicts.
Uses standalone stealth functionality for validation.
"""

import asyncio
import os
import time
import json
import browser_cookie3
from playwright.async_api import async_playwright


async def test_primeopinion_cookie_transfer():
    """
    Simple test to validate cookie transfer to Prime Opinion.
    Standalone - doesn't interfere with existing browser_manager.py
    """
    
    print("🧪 PRIME OPINION COOKIE TRANSFER TEST")
    print("=" * 45)
    print("🎯 Testing stealth cookie transfer capability")
    print("🚫 No integration - standalone validation only")
    print()
    
    # Step 1: Extract Chrome cookies
    print("🍪 STEP 1: Extract Chrome Cookies")
    print("-" * 30)
    
    try:
        print("🔍 Scanning Chrome browser cookies...")
        chrome_cookies = list(browser_cookie3.chrome())
        
        # Filter for relevant domains
        relevant_cookies = []
        target_domains = ['primeopinion.com.au', 'google.com', 'googleapis.com']
        
        for cookie in chrome_cookies:
            if any(domain in cookie.domain for domain in target_domains):
                relevant_cookies.append({
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'secure': bool(cookie.secure),  # Convert to boolean
                    'httpOnly': bool(getattr(cookie, 'httpOnly', False)),  # Convert to boolean
                    'expires': float(cookie.expires) if cookie.expires and cookie.expires != -1 else -1
                })
        
        print(f"✅ Found {len(chrome_cookies)} total Chrome cookies")
        print(f"🎯 Found {len(relevant_cookies)} relevant cookies for Prime Opinion")
        
        if len(relevant_cookies) == 0:
            print("⚠️ No relevant cookies found - you may need to login to Prime Opinion in Chrome first")
            return False
            
    except Exception as e:
        print(f"❌ Cookie extraction failed: {e}")
        print("💡 Try: pip install browser_cookie3")
        return False
    
    # Step 2: Create stealth browser
    print(f"\n🕵️ STEP 2: Create Stealth Browser")
    print("-" * 30)
    
    playwright = await async_playwright().start()
    
    try:
        # Launch with stealth settings
        browser = await playwright.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--no-first-run',
                '--no-default-browser-check'
            ]
        )
        
        # Create stealth context
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='en-AU',
            timezone_id='Australia/Sydney'
        )
        
        # Add stealth script
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        print("✅ Stealth browser created")
        
        # Step 3: Transfer cookies
        print(f"\n🔄 STEP 3: Transfer Cookies")
        print("-" * 30)
        
        if relevant_cookies:
            await context.add_cookies(relevant_cookies)
            print(f"✅ Transferred {len(relevant_cookies)} cookies to stealth browser")
        
        # Step 4: Test Prime Opinion access
        print(f"\n🌐 STEP 4: Test Prime Opinion Access")
        print("-" * 30)
        
        page = await context.new_page()
        
        print("🔗 Navigating to https://app.primeopinion.com.au/surveys...")
        await page.goto("https://app.primeopinion.com.au/surveys", wait_until='networkidle')
        
        # Analyze result
        current_url = page.url
        page_title = await page.title()
        
        print(f"📄 Page Title: {page_title}")
        print(f"🔗 Final URL: {current_url}")
        
        # Check success
        if "login" in current_url.lower():
            print("❌ RESULT: Login page detected")
            print("💡 Cookie transfer may have failed")
            print("🔧 Try refreshing your Prime Opinion login in Chrome")
            success = False
        elif "app.primeopinion.com.au/surveys" in current_url or "surveys" in current_url:
            print("✅ RESULT: Prime Opinion surveys dashboard accessed!")
            print("🎯 Cookie transfer successful")
            print("🕵️ Stealth access working")
            success = True
        else:
            print("🤔 RESULT: Unexpected page")
            print(f"🔍 Manual check needed: {current_url}")
            success = False
        
        # Step 5: Manual verification
        print(f"\n👁️ STEP 5: Manual Verification")
        print("-" * 30)
        print("Please visually inspect the Prime Opinion page...")
        print("✅ Can you see your dashboard/surveys?")
        print("✅ Are you logged in?")
        
        manual_input = input("Does the page look correct? (y/n): ").lower().strip()
        manual_success = manual_input == 'y'
        
        # Final summary
        print(f"\n📊 TEST SUMMARY")
        print("=" * 20)
        print(f"🍪 Cookie Extraction: ✅ SUCCESS")
        print(f"🕵️ Stealth Browser: ✅ SUCCESS")
        print(f"🔄 Cookie Transfer: ✅ SUCCESS")
        print(f"🌐 Dashboard Access: {'✅ SUCCESS' if success else '❌ FAILED'}")
        print(f"👁️ Manual Verification: {'✅ SUCCESS' if manual_success else '❌ FAILED'}")
        
        overall_success = success and manual_success
        
        if overall_success:
            print(f"\n🎉 PRIME OPINION STEALTH TEST: PASSED!")
            print("✅ Cookie transfer system working")
            print("✅ Stealth browser functional")
            print("✅ Prime Opinion access confirmed")
            print("🚀 Ready for integration with main system!")
        else:
            print(f"\n⚠️ PRIME OPINION STEALTH TEST: NEEDS WORK")
            print("🔧 Check Chrome login and retry")
        
        # Keep browser open for inspection
        if overall_success:
            input("\n⏸️ Press Enter to close browser...")
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False
    
    finally:
        await browser.close()
        await playwright.stop()


async def quick_stealth_detection_test():
    """Quick test to validate stealth capabilities."""
    
    print("🔍 QUICK STEALTH DETECTION TEST")
    print("=" * 35)
    
    playwright = await async_playwright().start()
    
    try:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # Add stealth script
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        page = await context.new_page()
        
        # Test detection
        print("🧪 Testing automation detection...")
        webdriver_detected = await page.evaluate("navigator.webdriver !== undefined")
        
        print(f"   WebDriver detected: {'❌ YES' if webdriver_detected else '✅ NO'}")
        
        if not webdriver_detected:
            print("✅ Basic stealth: WORKING")
            return True
        else:
            print("⚠️ Basic stealth: NEEDS IMPROVEMENT")
            return False
            
    except Exception as e:
        print(f"❌ Stealth test error: {e}")
        return False
    
    finally:
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    print("🚀 PRIME OPINION STEALTH VALIDATION")
    print("🎯 Standalone test - no file conflicts")
    print("=" * 50)
    print()
    
    print("📋 PRE-TEST CHECKLIST:")
    print("✅ Chrome browser open")
    print("✅ Prime Opinion logged in: https://app.primeopinion.com.au/surveys")
    print("✅ Surveys dashboard visible in Chrome tab")
    print()
    
    proceed = input("Ready to test? (y/N): ").lower().strip()
    if proceed != 'y':
        print("❌ Test cancelled")
        exit()
    
    async def run_tests():
        # Quick stealth test
        print("\nPHASE 1: Basic stealth detection test")
        stealth_ok = await quick_stealth_detection_test()
        
        if not stealth_ok:
            print("❌ Basic stealth failed - deployment issue")
            return
        
        print("\n" + "="*50)
        
        # Prime Opinion test
        print("PHASE 2: Prime Opinion cookie transfer test")
        primeopinion_ok = await test_primeopinion_cookie_transfer()
        
        print("\n" + "="*50)
        print("🏁 FINAL RESULT:")
        
        if primeopinion_ok:
            print("🎉 ALL TESTS PASSED!")
            print("✅ Prime Opinion stealth access validated")
            print("🚀 Ready to integrate with main Quenito system")
            print("🎯 Confident to scale beyond MyOpinions")
        else:
            print("⚠️ TESTS INCOMPLETE")
            print("🔧 Address issues and retry")
            print("💡 Most common fix: refresh Prime Opinion login in Chrome")
    
    asyncio.run(run_tests())
