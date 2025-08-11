# quenito_mvp_learning.py
"""
MVP Script focused on LEARNING - picks shortest survey and captures everything
"""

import asyncio
import json
from datetime import datetime
from core.stealth_browser_manager import StealthBrowserManager
from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter
from data.knowledge_base import KnowledgeBase
from utils.intervention_manager import EnhancedLearningInterventionManager

async def run_learning_mvp():
    """MVP focused on learning capture - shortest survey first"""
    
    print("🧠 QUENITO LEARNING MVP - SHORTEST SURVEY FIRST")
    print("="*50)
    
    # Initialize knowledge base and intervention manager
    print("\n🧠 Initializing learning systems...")
    knowledge_base = KnowledgeBase()
    intervention_manager = EnhancedLearningInterventionManager(
        signal_handler=None,
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
    print("2️⃣  Close any popups")
    print("3️⃣  Wait for surveys to load")
    print("="*50)
    input("\n✅ Press Enter when ready >>> ")
    
    # Create adapter
    adapter = MyOpinionsAdapter(browser, "quenito")
    
    # SURVEY DETECTION
    print("\n🔍 Detecting available surveys...")
    surveys = await adapter.detect_available_surveys()
    
    if not surveys:
        print("❌ No surveys found!")
        return
    
    # SORT BY SHORTEST TIME (not points!)
    print("\n⏱️ Sorting by SHORTEST duration for learning test...")
    
    # Parse time estimates
    for survey in surveys:
        time_text = survey['time'].lower()
        if 'min' in time_text:
            # Extract minutes
            minutes = int(''.join(filter(str.isdigit, time_text.split('min')[0])))
            survey['minutes'] = minutes
        else:
            survey['minutes'] = 999  # Unknown duration
    
    # Sort by shortest time
    surveys.sort(key=lambda x: x['minutes'])
    
    print(f"\n✅ Found {len(surveys)} surveys (sorted by duration):")
    for i, survey in enumerate(surveys[:5], 1):
        print(f"   {i}. {survey['time']} - {survey['points']} points - {survey['topic']}")
    
    # Select SHORTEST survey
    shortest_survey = surveys[0]
    print(f"\n🎯 SELECTED SHORTEST SURVEY: {shortest_survey['time']}")
    print(f"   Points: {shortest_survey['points']} (${shortest_survey['points']/100:.2f})")
    print(f"   Topic: {shortest_survey['topic']}")
    print(f"   Perfect for learning test!")
    
    # Start survey
    print(f"\n🚀 Starting survey flow...")
    
    # Direct approach - bypass the adapter's flow handler
    initial_pages = browser.context.pages
    
    # Click the survey
    await shortest_survey['element'].click()
    print("✅ Clicked survey button")
    
    # Wait for page change
    await asyncio.sleep(3)
    
    # Get all pages
    all_pages = browser.context.pages
    survey_page = None
    
    if len(all_pages) > len(initial_pages):
        # New tab opened
        survey_page = all_pages[-1]
        await survey_page.bring_to_front()
        print(f"✅ New tab opened (total: {len(all_pages)})")
    else:
        # Same tab
        survey_page = browser.page
        print("✅ Survey loaded in same tab")
    
    # Wait for page to load
    await survey_page.wait_for_load_state('networkidle')
    
    # Check what type of page we're on
    page_content = await survey_page.inner_text('body')
    page_lower = page_content.lower()
    
    print("\n🔍 Detecting page type...")
    
    if 'start survey now' in page_lower or 'your survey offer' in page_lower:
        print("📄 Intermediate page detected")
        print("🔘 Looking for Start Survey Now button...")
        
        # Try to click start button
        start_clicked = False
        for selector in ['button:has-text("Start Survey Now")', 
                        'button:has-text("START SURVEY NOW")',
                        'a:has-text("Start Survey Now")',
                        'a.btn-primary']:
            try:
                await survey_page.click(selector)
                print("✅ Clicked Start Survey Now")
                start_clicked = True
                await asyncio.sleep(3)
                
                # Check for another new tab
                final_pages = browser.context.pages
                if len(final_pages) > len(all_pages):
                    survey_page = final_pages[-1]
                    await survey_page.bring_to_front()
                    print("✅ Switched to final survey tab")
                break
            except:
                continue
        
        if not start_clicked:
            print("⚠️ Could not find start button - continue anyway")
    
    elif any(q in page_lower for q in ['what is your', 'please select', 'which of', 
                                       'how often', 'your age', 'your gender']):
        print("❓ Survey question detected - no intermediate page!")
        print("✅ Ready to start capturing responses")
    
    elif 'captcha' in page_lower:
        print("🔐 Captcha detected!")
        input("Please solve the captcha and press Enter >>> ")
    
    else:
        print("❓ Unknown page type")
        print(f"Preview: {page_content[:200]}...")
    
    print("\n✅ SURVEY PAGE LOADED!")
    print("="*50)
    print("🧠 ACTIVE LEARNING MODE - MONITORING ALL RESPONSES")
    print("="*50)
    
    # ACTIVE MONITORING LOOP
    question_count = 0
    learning_data = []
    
    print("\n📝 Starting question-by-question learning capture...")
    print("Instructions:")
    print("  1. Answer each question in the browser")
    print("  2. Click Next/Continue in the survey")
    print("  3. Come back here and press Enter")
    print("  4. Quenito will capture and show what was learned")
    print("\n" + "="*50)
    
    while True:
        question_count += 1
        
        # Get current page content
        try:
            page_content = await survey_page.inner_text('body')
            page_url = survey_page.url
        except:
            print("❌ Lost connection to survey page")
            break
        
        # Check for completion indicators
        if any(indicator in page_content.lower() for indicator in 
               ['thank you', 'survey complete', 'points earned', 'redirecting']):
            print("\n🎉 SURVEY COMPLETE!")
            break
        
        print(f"\n❓ QUESTION {question_count}")
        print("-"*50)
        
        # Show preview of current question
        preview = page_content[:200] + "..." if len(page_content) > 200 else page_content
        print(f"Preview: {preview}")
        
        # Manual intervention prompt
        print("\n🎯 Learning Capture Active:")
        print("  1. Complete the question in the browser")
        print("  2. Click Next/Continue")
        print("  3. Press Enter here to capture")
        
        input("\n✋ Press Enter AFTER answering and clicking Next >>> ")
        
        # Capture what changed
        try:
            new_content = await survey_page.inner_text('body')
            
            # Analyze what was on the page
            question_data = {
                'question_number': question_count,
                'timestamp': datetime.now().isoformat(),
                'url': page_url,
                'question_preview': preview,
                'page_length': len(page_content)
            }
            
            # Detect question type
            content_lower = page_content.lower()
            if 'your age' in content_lower or 'how old' in content_lower:
                question_data['detected_type'] = 'age'
            elif 'gender' in content_lower:
                question_data['detected_type'] = 'gender'
            elif 'industry' in content_lower or 'work' in content_lower:
                question_data['detected_type'] = 'occupation/industry'
            elif any(word in content_lower for word in ['select all', 'check all']):
                question_data['detected_type'] = 'multi-select'
            elif any(word in content_lower for word in ['rate', 'scale', 'satisfied']):
                question_data['detected_type'] = 'rating scale'
            else:
                question_data['detected_type'] = 'unknown'
            
            # Show what was captured
            print("\n📊 CAPTURED LEARNING DATA:")
            print(f"  ✅ Question Type: {question_data['detected_type']}")
            print(f"  ✅ Question #: {question_count}")
            print(f"  ✅ Timestamp: {question_data['timestamp']}")
            print(f"  ✅ Page URL: {page_url}")
            
            # Store in knowledge base
            if 'learning_sessions' not in knowledge_base.data:
                knowledge_base.data['learning_sessions'] = []
            
            session_id = f"learning_mvp_{int(datetime.now().timestamp())}"
            if not any(s['id'] == session_id for s in knowledge_base.data['learning_sessions']):
                knowledge_base.data['learning_sessions'].append({
                    'id': session_id,
                    'started': datetime.now().isoformat(),
                    'survey': shortest_survey,
                    'questions': []
                })
            
            # Add question to session
            for session in knowledge_base.data['learning_sessions']:
                if session['id'] == session_id:
                    session['questions'].append(question_data)
            
            # Save immediately
            knowledge_base.save()
            
            print("\n💾 STORAGE CONFIRMATION:")
            print(f"  ✅ Saved to: personas/quenito/knowledge_base.json")
            print(f"  ✅ Total questions captured: {question_count}")
            print(f"  ✅ Learning system: ACTIVE")
            
            learning_data.append(question_data)
            
        except Exception as e:
            print(f"❌ Capture error: {e}")
    
    # Final summary
    print("\n" + "="*50)
    print("📊 LEARNING SESSION COMPLETE!")
    print("="*50)
    print(f"✅ Total questions captured: {len(learning_data)}")
    print(f"✅ Survey duration: {shortest_survey['time']}")
    print(f"✅ Points earned: {shortest_survey['points']}")
    
    print("\n🧠 Question types detected:")
    types = {}
    for q in learning_data:
        q_type = q.get('detected_type', 'unknown')
        types[q_type] = types.get(q_type, 0) + 1
    
    for q_type, count in types.items():
        print(f"  - {q_type}: {count} questions")
    
    print("\n💾 All data saved to knowledge base!")
    print("🚀 Run again to test automation with learned patterns!")
    
    # Keep browser open
    input("\n🏁 Press Enter to close browser >>> ")
    await browser.close()

if __name__ == "__main__":
    asyncio.run(run_learning_mvp())