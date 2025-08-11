# run_myopinions_survey.py
"""
Simple example showing how to use the integrated MyOpinions system
"""

import asyncio
from core.stealth_browser_manager import StealthBrowserManager
from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter

async def run_survey():
    """Run a complete MyOpinions survey session"""
    
    # Initialize browser
    browser = StealthBrowserManager("quenito_myopinions")
    await browser.initialize_stealth_browser(transfer_cookies=False)
    await browser.load_saved_cookies()
    
    # Create adapter (which now includes the flow handler)
    adapter = MyOpinionsAdapter(browser, "quenito")
    
    # Navigate to MyOpinions
    await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
    
    # Manual login if needed
    print("Login if needed, then press Enter...")
    input("Press Enter when ready >>> ")
    
    # Run a complete survey session
    # This single method now handles EVERYTHING:
    # - Closes popups
    # - Detects surveys  
    # - Selects best one
    # - Handles all tabs
    # - Manages consent forms
    # - Gets to survey page
    results = await adapter.run_survey_session()
    
    # Display results
    print("\n📊 Session Results:")
    print(f"Started: {results['started']}")
    print(f"Ended: {results['ended']}")
    
    if results.get('current_survey'):
        survey = results['current_survey']
        print(f"\n✅ Survey loaded:")
        print(f"  Points: {survey['points']} (${adapter.get_points_value(survey['points']):.2f})")
        print(f"  Topic: {survey['topic']}")
        print(f"  Time: {survey['time']}")
    
    if results['errors']:
        print(f"\n❌ Errors: {results['errors']}")
    
    # Keep browser open
    input("\nPress Enter to close browser >>> ")
    await browser.close()

if __name__ == "__main__":
    asyncio.run(run_survey())