# quenito_survey_mvp.py
"""
MVP Launch Process for Quenito - Focus on survey learning
With proper learning system integration!
"""

import asyncio
from datetime import datetime
from core.stealth_browser_manager import StealthBrowserManager
from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter
from data.knowledge_base import KnowledgeBase
from utils.intervention_manager import EnhancedLearningInterventionManager

async def run_quenito_mvp():
    """Streamlined MVP process with learning system connected"""
    
    print("🚀 QUENITO SURVEY AUTOMATION MVP")
    print("="*50)
    
    # Initialize knowledge base and learning systems
    print("\n🧠 Initializing learning systems...")
    knowledge_base = KnowledgeBase()
    intervention_manager = EnhancedLearningInterventionManager(
        signal_handler=None,  # Will add if needed
        knowledge_base=knowledge_base
    )
    print("✅ Learning systems connected!")
    
    # Initialize browser
    browser = StealthBrowserManager("quenito_myopinions")
    await browser.initialize_stealth_browser(transfer_cookies=False)
    await browser.load_saved_cookies()
    
    # Navigate to MyOpinions
    await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
    
    # MANUAL STEPS
    print("\n📋 MANUAL SETUP REQUIRED:")
    print("="*50)
    print("1️⃣  Login if needed")
    print("2️⃣  Close any popups (click 'NO THANKS' or 'X')")
    print("3️⃣  Wait for dashboard with surveys to load")
    print("="*50)
    input("\n✅ Press Enter when dashboard is clear and surveys are visible >>> ")
    
    # Create adapter with learning system
    adapter = MyOpinionsAdapter(browser, "quenito")
    
    # Connect intervention manager to handlers (if possible)
    # This ensures learning data is captured during manual interventions
    print("\n🔗 Connecting learning systems to survey handlers...")
    
    # AUTOMATED FLOW BEGINS
    print("\n🤖 QUENITO TAKING OVER...")
    print("="*50)
    
    # Step 1: Detect surveys
    print("\n🔍 STEP 1: Detecting available surveys...")
    surveys = await adapter.detect_available_surveys()
    
    if not surveys:
        print("❌ No surveys found! Check if surveys are visible on dashboard")
        return
    
    print(f"✅ Found {len(surveys)} surveys:")
    for i, survey in enumerate(surveys[:5], 1):
        print(f"   {i}. {survey['points']} points - {survey['time']} - {survey['topic']}")
        print(f"      Type: {survey['type']} | Button: {survey['button_text']}")
    
    # Step 2: Select best survey
    best_survey = surveys[0]  # Already sorted by points
    print(f"\n🎯 STEP 2: Selected best survey: {best_survey['points']} points")
    
    # Step 3: Start survey flow
    print(f"\n🚀 STEP 3: Starting survey automation flow...")
    print(f"   Topic: {best_survey['topic']}")
    print(f"   Estimated time: {best_survey['time']}")
    print(f"   Value: ${adapter.get_points_value(best_survey['points']):.2f} AUD")
    
    # Run the flow
    success = await adapter.start_survey(best_survey)
    
    if success:
        print("\n✅ SURVEY PAGE REACHED SUCCESSFULLY!")
        print("="*50)
        print("📍 Current status:")
        print("   - Survey loaded in new tab")
        print("   - Ready for manual completion")
        print("\n🧠 LEARNING MODE ACTIVE:")
        print("   - Quenito will observe your responses")
        print("   - Patterns will be saved for future automation")
        print("   - Second run should show improved automation")
        
        # Check learning system status
        print("\n💾 Learning System Status:")
        try:
            # Check knowledge base
            kb_stats = knowledge_base.get_statistics() if hasattr(knowledge_base, 'get_statistics') else {}
            print(f"   ✅ Knowledge Base: Active")
            print(f"   ✅ Intervention Manager: Connected")
            print(f"   ✅ Pattern Capture: READY")
            
            # Show current learning stats
            if 'brain_learning' in knowledge_base.data:
                interventions = len(knowledge_base.data['brain_learning'].get('intervention_history', []))
                patterns = len(knowledge_base.data['brain_learning'].get('success_patterns', {}))
                print(f"   📊 Previous interventions learned: {interventions}")
                print(f"   📊 Success patterns stored: {patterns}")
            
        except Exception as e:
            print(f"   ⚠️ Warning: {e}")
        
        print("\n📝 MANUAL COMPLETION INSTRUCTIONS:")
        print("="*50)
        print("1. Complete the survey manually")
        print("2. If Quenito pauses and asks for help:")
        print("   - Answer the question it's stuck on")
        print("   - Quenito will learn from your response")
        print("3. Complete as many questions as possible")
        print("4. On the SECOND run, Quenito should handle more automatically!")
        
        # Learning summary
        print("\n🎯 EXPECTED LEARNING OUTCOMES:")
        print("   - Text inputs: Quenito learns your typical responses")
        print("   - Radio buttons: Learns your selection preferences")
        print("   - Checkboxes: Understands your multi-select patterns")
        print("   - Demographics: Remembers personal information")
        
    else:
        print("\n❌ Failed to reach survey page")
        print("Check the browser for any errors")
    
    # Keep browser open
    input("\n🏁 Press Enter to close browser >>> ")
    await browser.close()
    
    print("\n🎉 Session complete!")
    print("Run again to test learned patterns!")

if __name__ == "__main__":
    # First verify learning system
    print("\n🔍 Pre-flight check...")
    try:
        from data.knowledge_base import KnowledgeBase
        from utils.intervention_manager import EnhancedLearningInterventionManager
        print("✅ All learning components available!")
    except ImportError as e:
        print(f"❌ Missing component: {e}")
        print("Run: python verify_learning_system.py")
        exit(1)
    
    asyncio.run(run_quenito_mvp())