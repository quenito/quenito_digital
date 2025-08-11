"""
🤖 Test Hybrid Survey Completion
Demonstrates the full hybrid automation flow
"""

import asyncio
import os
from datetime import datetime
from core.stealth_browser_manager import StealthBrowserManager
from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_hybrid_survey_completion():
    """Test the complete hybrid survey flow"""
    
    print("🚀 MyOpinions Hybrid Survey Test")
    print("="*60)
    
    # Initialize browser
    print("\n1️⃣ Initializing stealth browser...")
    browser = StealthBrowserManager("quenito_myopinions")
    
    # Create adapter
    adapter = MyOpinionsAdapter(browser, "quenito")
    
    try:
        # Initialize session
        if not await adapter.initialize_session():
            print("❌ Failed to initialize session")
            return
        
        print("✅ Session initialized")
        
        # Load saved cookies if they exist
        cookie_file = "personas/quenito/myopinions_cookies.json"
        if os.path.exists(cookie_file):
            print("\n2️⃣ Loading saved cookies...")
            await browser.load_saved_cookies(cookie_file)
            print("✅ Cookies loaded")
        else:
            print("⚠️  No saved cookies found - you may need to login manually")
        
        # Navigate to surveys
        print("\n3️⃣ Navigating to survey dashboard...")
        if not await adapter.navigate_to_surveys():
            print("❌ Failed to navigate to surveys")
            return
        
        print("✅ Successfully loaded dashboard")
        
        # Get available surveys
        print("\n4️⃣ Scanning for available surveys...")
        surveys = await adapter.get_available_surveys()
        
        if not surveys:
            print("😕 No surveys available right now")
            return
        
        print(f"📊 Found {len(surveys)} available surveys:")
        
        # Display survey options
        for i, survey in enumerate(surveys[:5], 1):  # Show top 5
            print(f"\n   {i}. {survey.title[:50]}...")
            print(f"      💰 ${survey.dollar_value:.2f} ({survey.points} points)")
            print(f"      ⏱️  {survey.time_minutes} minutes")
            print(f"      💵 ${survey.hourly_rate:.2f}/hour")
        
        # Select best survey
        print("\n5️⃣ Selecting optimal survey...")
        best_survey = await adapter.select_best_survey(surveys)
        
        if not best_survey:
            print("❌ No suitable survey found")
            return
        
        print(f"\n🎯 Selected: {best_survey.title}")
        print(f"   Expected value: ${best_survey.dollar_value:.2f}")
        print(f"   Expected time: {best_survey.time_minutes} minutes")
        
        # Confirm before starting
        response = input("\n🤔 Start this survey? (y/n): ")
        if response.lower() != 'y':
            print("Survey cancelled")
            return
        
        # Start survey
        print("\n6️⃣ Starting survey...")
        if not await adapter.start_survey(best_survey):
            print("❌ Failed to start survey")
            return
        
        # Run hybrid completion
        print("\n7️⃣ Running hybrid completion...")
        print("   - Automated: Navigation, consent forms, survey questions")
        print("   - Manual: CAPTCHA solving")
        print("\n" + "="*60)
        
        result = await adapter.complete_survey_hybrid(best_survey)
        
        # Display results
        print("\n" + "="*60)
        print("📊 SURVEY COMPLETION RESULTS")
        print("="*60)
        
        if result.get("success"):
            print("✅ Survey completed successfully!")
            print(f"\n📈 Statistics:")
            print(f"   - Total time: {result['total_seconds']:.1f} seconds")
            print(f"   - Questions automated: {result['questions_automated']}")
            print(f"   - Manual interventions: {result['manual_interventions']}")
            
            if result['questions_automated'] > 0:
                automation_rate = (
                    result['questions_automated'] / 
                    (result['questions_automated'] + result['manual_interventions']) * 100
                )
                print(f"   - Automation rate: {automation_rate:.1f}%")
            
            print(f"\n💰 Earned: {best_survey.points} points (${best_survey.dollar_value:.2f})")
            
            # Track earnings
            adapter.surveys_completed += 1
            adapter.total_points_earned += best_survey.points
            
        else:
            print("❌ Survey completion failed")
            if "error" in result:
                print(f"   Error: {result['error']}")
        
        # Save session state
        await adapter.save_session_state()
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Close browser
        print("\n🧹 Cleaning up...")
        await browser.close()
        print("✅ Test complete!")


async def quick_survey_scan():
    """Quick scan to see available surveys without completing"""
    
    print("🔍 Quick Survey Scan")
    print("="*40)
    
    browser = StealthBrowserManager("quenito_myopinions")
    adapter = MyOpinionsAdapter(browser, "quenito")
    
    try:
        if await adapter.initialize_session():
            # Load cookies
            cookie_file = "personas/quenito/myopinions_cookies.json"
            if os.path.exists(cookie_file):
                await browser.load_saved_cookies(cookie_file)
            
            # Navigate and scan
            if await adapter.navigate_to_surveys():
                surveys = await adapter.get_available_surveys()
                
                if surveys:
                    print(f"\n📊 {len(surveys)} surveys available:")
                    
                    total_value = sum(s.dollar_value for s in surveys)
                    total_time = sum(s.time_minutes for s in surveys)
                    
                    for survey in surveys:
                        print(f"\n• {survey.title[:60]}...")
                        print(f"  ${survey.dollar_value:.2f} | {survey.time_minutes} min | ${survey.hourly_rate:.2f}/hr")
                    
                    print(f"\n💰 Total available: ${total_value:.2f}")
                    print(f"⏱️  Total time: {total_time} minutes")
                    
                    if total_time > 0:
                        avg_rate = (total_value / total_time) * 60
                        print(f"💵 Average rate: ${avg_rate:.2f}/hour")
                else:
                    print("No surveys available right now")
                    
    finally:
        await browser.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        # Just scan available surveys
        asyncio.run(quick_survey_scan())
    else:
        # Run full hybrid test
        asyncio.run(test_hybrid_survey_completion())