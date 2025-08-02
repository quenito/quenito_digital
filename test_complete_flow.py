# test_complete_flow.py
"""
Test the complete MyOpinions survey flow
From dashboard through to survey page
"""

import asyncio
from core.stealth_browser_manager import StealthBrowserManager
from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter
from platform_adapters.flow_handlers.myopinions_flow_handler import MyOpinionsFlowHandler

async def test_complete_flow():
    """Test the full survey automation flow"""
    
    print("🚀 MyOpinions Complete Flow Test")
    print("="*50)
    
    browser = StealthBrowserManager("quenito_myopinions")
    
    try:
        # Initialize browser
        await browser.initialize_stealth_browser(transfer_cookies=False)
        await browser.load_saved_cookies()
        
        # Create adapter
        adapter = MyOpinionsAdapter(browser)
        
        # Navigate to dashboard
        print("\n📍 Navigating to MyOpinions dashboard...")
        await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
        
        # Manual login step
        print("\n" + "="*50)
        print("🛑 MANUAL STEP REQUIRED")
        print("="*50)
        print("\n1️⃣  Login if needed")
        print("2️⃣  Press Enter when dashboard loads")
        print("   (Don't close any popups - Quenito will handle them!)")
        input("\nPress Enter when ready >>> ")
        
        # Create flow handler
        flow_handler = MyOpinionsFlowHandler(browser)
        
        # Step 1: Handle popups automatically
        print("\n🎯 Step 1: Handling dashboard popups...")
        await flow_handler.handle_dashboard_popups(browser.page)
        
        # Wait a moment for page to settle
        await browser.page.wait_for_timeout(2000)
        
        # Step 2: Detect available surveys
        print("\n🎯 Step 2: Detecting available surveys...")
        surveys = await adapter.detect_available_surveys()
        
        if not surveys:
            print("❌ No surveys found!")
            return
            
        print(f"\n✅ Found {len(surveys)} surveys:")
        for i, survey in enumerate(surveys[:3], 1):
            print(f"  {i}. {survey['points']} points - {survey['time']} - {survey['topic']}")
        
        # Step 3: Select best survey (highest points)
        best_survey = surveys[0]  # Already sorted by points
        print(f"\n🎯 Step 3: Selected best survey: {best_survey['points']} points")
        
        # Step 4: Run complete flow
        print("\n🎯 Step 4: Starting complete survey flow...")
        print("-"*50)
        
        success = await flow_handler.run_complete_flow(best_survey)
        
        if success:
            print("\n✅ Successfully navigated to survey!")
            print("📍 Survey is now loaded and ready")
            print("\n⚠️ Next steps require manual intervention:")
            print("  1. Solve any captcha if present")
            print("  2. Complete pre-screening questions")
            print("  3. Then Quenito can handle the main survey")
        else:
            print("\n⚠️ Flow stopped - manual intervention required")
        
        # Keep browser open for inspection
        print("\n" + "="*50)
        print("💡 CURRENT STATUS:")
        all_pages = browser.context.pages
        print(f"  Total tabs open: {len(all_pages)}")
        for i, page in enumerate(all_pages, 1):
            print(f"  Tab {i}: {page.url[:80]}...")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n⏸️  Browser stays open for inspection")
        input("Press Enter to close browser >>> ")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_complete_flow())