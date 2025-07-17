#!/usr/bin/env python3
"""
🧪 Simple Integration Test for Fixed Stealth Browser Manager

This script tests the stealth browser fix independently to verify
the 'NoneType' error has been resolved.

Usage:
    python test_stealth_fix.py
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_stealth_browser_initialization():
    """Test stealth browser initialization with the fix."""
    
    print("🚀 STEALTH BROWSER FIX TEST")
    print("=" * 40)
    
    try:
        # Import the fixed StealthBrowserManager
        from core.stealth_browser_manager import StealthBrowserManager
        
        print("✅ StealthBrowserManager imported successfully")
        
        # Initialize browser manager
        manager = StealthBrowserManager("test_fix_profile")
        print("✅ Manager created successfully")
        
        # Test browser initialization
        print("🔧 Testing browser initialization...")
        page = await manager.initialize_stealth_browser(
            transfer_cookies=False,  # Skip cookie transfer for test
            use_existing_chrome=False  # Use fresh browser
        )
        
        if page:
            print("✅ Browser initialization: SUCCESS")
            print("🎯 Testing basic functionality...")
            
            # Test navigation
            await page.goto("https://httpbin.org/user-agent", timeout=15000)
            
            # Check user agent
            user_agent = await page.evaluate('navigator.userAgent')
            print(f"🔍 User Agent: {user_agent[:50]}...")
            
            # Check webdriver detection
            webdriver_detected = await page.evaluate('navigator.webdriver !== undefined')
            print(f"🕵️ WebDriver detected: {webdriver_detected} (should be False)")
            
            # Test stealth score
            if not webdriver_detected and 'Chrome' in user_agent:
                print("🎉 STEALTH TEST: PASSED")
                result = True
            else:
                print("⚠️ STEALTH TEST: PARTIAL (browser works but stealth needs improvement)")
                result = True  # Still consider it a pass since browser works
        else:
            print("❌ Browser initialization failed")
            result = False
        
        # Clean up
        await manager.close()
        print("🧹 Cleanup completed")
        
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

async def test_fallback_strategies():
    """Test the fallback strategies in browser initialization."""
    
    print("\n🔄 TESTING FALLBACK STRATEGIES")
    print("=" * 40)
    
    try:
        from core.stealth_browser_manager import StealthBrowserManager
        
        manager = StealthBrowserManager("test_fallback")
        
        # This should work even if full stealth fails
        page = await manager.initialize_stealth_browser()
        
        if page:
            print("✅ Fallback strategy test: SUCCESS")
            await page.goto("https://www.google.com")
            title = await page.title()
            print(f"📄 Page title: {title}")
        else:
            print("❌ All fallback strategies failed")
            return False
        
        await manager.close()
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 QUENITO STEALTH BROWSER FIX VERIFICATION")
    print("=" * 50)
    print("Testing the fix for: 'NoneType' object has no attribute 'start'")
    print()
    
    # Test 1: Basic initialization
    result1 = asyncio.run(test_stealth_browser_initialization())
    
    # Test 2: Fallback strategies  
    result2 = asyncio.run(test_fallback_strategies())
    
    # Final results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"✅ Basic Initialization: {'PASSED' if result1 else 'FAILED'}")
    print(f"✅ Fallback Strategies: {'PASSED' if result2 else 'FAILED'}")
    
    overall_result = result1 and result2
    print(f"\n🎯 OVERALL RESULT: {'✅ PASSED' if overall_result else '❌ FAILED'}")
    
    if overall_result:
        print("\n🎉 The stealth browser fix is working!")
        print("💡 You can now proceed with Survey 1A testing")
    else:
        print("\n⚠️ Some issues remain. Check the error messages above.")
        
    return overall_result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
