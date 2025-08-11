# Save as test_myopinions_fix.py
"""
Test script to verify MyOpinions button detection is working
Now with manual control for login and popup handling
"""

import asyncio
from core.stealth_browser_manager import StealthBrowserManager

async def test_button_detection():
    """Test the fixed button detection with manual control"""
    
    print("🧪 Testing MyOpinions Button Detection Fix")
    print("="*50)
    
    browser = StealthBrowserManager("quenito_myopinions")
    
    try:
        # Initialize browser
        await browser.initialize_stealth_browser(transfer_cookies=False)
        await browser.load_saved_cookies()
        
        # Navigate to dashboard
        print("\n📍 Navigating to MyOpinions dashboard...")
        await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
        
        # Manual login step
        print("\n" + "="*50)
        print("🛑 MANUAL STEP REQUIRED")
        print("="*50)
        print("\n1️⃣  Login if needed")
        print("2️⃣  Close any banner pop-ups")
        print("3️⃣  Wait for survey tiles to fully load")
        print("4️⃣  Press Enter when you see all the survey cards")
        input("\nPress Enter when ready >>> ")
        
        # Extra wait to ensure everything is loaded
        await browser.page.wait_for_timeout(3000)
        
        print("\n🔍 Testing button detection with fixed selectors...")
        
        # Test 1: Count all anchor tags with btn btn-primary
        anchor_buttons = await browser.page.query_selector_all('a.btn.btn-primary')
        print(f"\n✅ Found {len(anchor_buttons)} anchor buttons (a.btn.btn-primary)")
        
        # Test 2: Get button details
        if anchor_buttons:
            print("\n📋 Button details:")
            for i, button in enumerate(anchor_buttons[:5]):  # First 5 buttons
                try:
                    text = await button.inner_text()
                    href = await button.get_attribute('href')
                    print(f"\n  Button {i+1}:")
                    print(f"    Text: {text}")
                    print(f"    URL: {href[:80]}...")  # First 80 chars of URL
                except Exception as e:
                    print(f"    Error reading button {i+1}: {e}")
                    continue
        else:
            print("\n❌ No anchor buttons found! Checking why...")
            
            # Debug: Look for any buttons
            all_buttons = await browser.page.query_selector_all('button')
            print(f"  Found {len(all_buttons)} <button> elements")
            
            # Debug: Look for any anchors
            all_anchors = await browser.page.query_selector_all('a')
            print(f"  Found {len(all_anchors)} <a> elements")
            
            # Debug: Look for elements with btn class
            btn_elements = await browser.page.query_selector_all('.btn')
            print(f"  Found {len(btn_elements)} elements with .btn class")
        
        # Test 3: Find survey cards and their buttons
        print("\n\n🎯 Testing full survey card detection:")
        
        cards = await browser.page.query_selector_all('.card')
        print(f"\n✅ Found {len(cards)} survey cards")
        
        surveys_found = 0
        survey_details = []
        
        for card in cards:
            try:
                # Look for button within card
                button = await card.query_selector('a.btn.btn-primary')
                if button:
                    button_text = await button.inner_text()
                    button_href = await button.get_attribute('href')
                    
                    # Get points if available
                    points_elem = await card.query_selector('.card-body-points')
                    points_text = await points_elem.inner_text() if points_elem else "No points"
                    
                    # Get time estimate
                    time_elem = await card.query_selector('.card-body-loi')
                    time_text = await time_elem.inner_text() if time_elem else "No time"
                    
                    # Get topic
                    topic_elem = await card.query_selector('.card-body-topic')
                    topic_text = await topic_elem.inner_text() if topic_elem else "No topic"
                    
                    surveys_found += 1
                    survey_details.append({
                        'button': button_text,
                        'points': points_text,
                        'time': time_text,
                        'topic': topic_text,
                        'url': button_href
                    })
                    
                    print(f"\n  Survey {surveys_found}:")
                    print(f"    Button: {button_text}")
                    print(f"    Points: {points_text}")
                    print(f"    Time: {time_text}")
                    print(f"    Topic: {topic_text}")
            except Exception as e:
                print(f"  Error parsing card: {e}")
                continue
        
        if surveys_found > 0:
            print(f"\n\n🎉 SUCCESS! Found {surveys_found} surveys with clickable buttons")
            
            # Test clicking the first survey (optional)
            print("\n🖱️  Testing button click functionality...")
            print("Would you like to test clicking the first survey button?")
            test_click = input("This will open the survey in a new tab (y/n): ").strip().lower()
            
            if test_click == 'y' and survey_details:
                first_card = await browser.page.query_selector('.card')
                first_button = await first_card.query_selector('a.btn.btn-primary')
                if first_button:
                    print("\n📍 Clicking first survey button...")
                    await first_button.click()
                    await browser.page.wait_for_timeout(3000)
                    print("✅ Button clicked! Check if a new tab opened.")
        else:
            print("\n❌ No surveys found with the new selector!")
            print("Trying alternative selectors...")
            
            # Try some alternative selectors
            alt_selectors = [
                "a.btn",
                "a[class*='btn']",
                "*:has-text('START SURVEY')",
                "a:has-text('START')"
            ]
            
            for selector in alt_selectors:
                try:
                    elements = await browser.page.query_selector_all(selector)
                    if elements:
                        print(f"  Found {len(elements)} elements with selector: {selector}")
                except:
                    pass
        
        # Test 4: Visual verification
        print("\n📸 Taking screenshot for visual verification...")
        await browser.page.screenshot(path="myopinions_buttons_test.png", full_page=True)
        print("✅ Screenshot saved as myopinions_buttons_test.png")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n⏸️  Test complete. Browser stays open for inspection.")
        input("Press Enter to close browser >>> ")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_button_detection())