# Save as debug_button_detection.py
"""
Debug script to find out why START SURVEY buttons aren't being detected
"""

import asyncio
from core.stealth_browser_manager import StealthBrowserManager

async def debug_button_detection():
    """Debug why START SURVEY buttons aren't found"""
    
    print("🔍 MyOpinions Button Detection Debug")
    print("="*50)
    
    browser = StealthBrowserManager("quenito_myopinions")
    
    try:
        # Initialize and load cookies
        await browser.initialize_stealth_browser(transfer_cookies=False)
        await browser.load_saved_cookies()
        
        # Navigate to site
        print("\n📍 Navigating to MyOpinions...")
        await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
        
        # Manual login step
        print("\n" + "="*50)
        print("🛑 MANUAL STEP REQUIRED")
        print("="*50)
        print("\n1️⃣  Login if needed")
        print("2️⃣  Wait for surveys to load")
        print("3️⃣  Press Enter when you see the survey cards")
        input("\nPress Enter when ready >>> ")
        
        await browser.page.wait_for_timeout(3000)
        
        print("\n🔍 Debugging button detection...")
        
        # Method 1: Try different text selectors
        print("\n📊 Method 1: Text-based selectors")
        selectors = [
            "button:has-text('START SURVEY')",
            "button:has-text('Start Survey')",
            "button:has-text('START')",
            "button:has-text('SURVEY')",
            "*:has-text('START SURVEY')",
            "text='START SURVEY'",
            "text=/START.*SURVEY/i"
        ]
        
        for selector in selectors:
            try:
                elements = await browser.page.query_selector_all(selector)
                if elements:
                    print(f"  ✓ Found {len(elements)} elements with selector: {selector}")
            except:
                print(f"  ✗ Error with selector: {selector}")
        
        # Method 2: Find ALL buttons and analyze
        print("\n📊 Method 2: Analyzing ALL buttons")
        all_buttons = await browser.page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                return buttons.map(btn => ({
                    text: btn.textContent.trim(),
                    className: btn.className,
                    innerHTML: btn.innerHTML.substring(0, 100),
                    hasStartText: btn.textContent.toUpperCase().includes('START'),
                    hasSurveyText: btn.textContent.toUpperCase().includes('SURVEY')
                }));
            }
        """)
        
        print(f"\n  Total buttons found: {len(all_buttons)}")
        
        # Show buttons containing START or SURVEY
        start_buttons = [b for b in all_buttons if b['hasStartText'] or b['hasSurveyText']]
        print(f"  Buttons with START or SURVEY text: {len(start_buttons)}")
        
        if start_buttons:
            print("\n  First few matching buttons:")
            for i, btn in enumerate(start_buttons[:3]):
                print(f"\n  Button {i+1}:")
                print(f"    Text: '{btn['text']}'")
                print(f"    Class: {btn['className']}")
                print(f"    HTML preview: {btn['innerHTML'][:50]}...")
        
        # Method 3: Look for links or other clickable elements
        print("\n📊 Method 3: Checking for links or other clickable elements")
        clickables = await browser.page.evaluate("""
            () => {
                // Find all elements with START SURVEY text
                const allElements = Array.from(document.querySelectorAll('*'));
                const startElements = allElements.filter(el => 
                    el.textContent.includes('START SURVEY') && 
                    el.children.length <= 3
                );
                
                return startElements.map(el => ({
                    tag: el.tagName,
                    className: el.className,
                    text: el.textContent.trim(),
                    isClickable: el.tagName === 'BUTTON' || el.tagName === 'A' || 
                                 el.onclick !== null || el.style.cursor === 'pointer',
                    innerHTML: el.innerHTML.substring(0, 100)
                }));
            }
        """)
        
        print(f"\n  Elements containing 'START SURVEY': {len(clickables)}")
        for i, elem in enumerate(clickables[:5]):
            print(f"\n  Element {i+1}:")
            print(f"    Tag: <{elem['tag']}>")
            print(f"    Class: {elem['className']}")
            print(f"    Clickable: {elem['isClickable']}")
        
        # Method 4: Save a survey card for manual inspection
        print("\n📊 Method 4: Extracting survey card HTML")
        
        # Try to find survey cards by looking for elements with points
        card_html = await browser.page.evaluate("""
            () => {
                // Find elements with points that might be survey cards
                const pointsElements = Array.from(document.querySelectorAll('*')).filter(
                    el => el.textContent.match(/\d+\s*points/i) && el.children.length < 20
                );
                
                // Find the most likely survey card
                for (let el of pointsElements) {
                    // Check if this element or its children contain START
                    if (el.textContent.includes('START') || el.textContent.includes('Start')) {
                        return el.outerHTML;
                    }
                }
                
                // If no START found, return first points element
                return pointsElements[0] ? pointsElements[0].outerHTML : null;
            }
        """)
        
        if card_html:
            with open("debug_survey_card.html", "w", encoding='utf-8') as f:
                f.write(card_html)
            print("\n✅ Survey card HTML saved to debug_survey_card.html")
        
        # Method 5: Screenshot just the survey area
        print("\n📸 Taking focused screenshot of survey area...")
        
        # Find survey section
        survey_section = await browser.page.query_selector(".surveys") or \
                        await browser.page.query_selector("[class*='survey']") or \
                        await browser.page.query_selector("main")
        
        if survey_section:
            await survey_section.screenshot(path="survey_section.png")
            print("✅ Survey section screenshot saved")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n⏸️  Browser stays open for inspection.")
        input("Press Enter to close >>> ")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_button_detection())