# Save as debug_selectors_v4.py
"""
Enhanced debug script with proper modal-based login detection
"""

import asyncio
from core.stealth_browser_manager import StealthBrowserManager

async def wait_for_login_modal_to_close(page):
    """Wait for login modal to disappear"""
    print("\n🔐 Login modal detected!")
    print("👤 Please login in the browser window...")
    print("⏸️  I'll wait for you to complete login...")
    print("\n📍 Waiting for login modal to close...")
    
    # Keep checking until login modal is gone
    while True:
        await page.wait_for_timeout(2000)  # Check every 2 seconds
        
        try:
            # Check for login modal by looking for the welcome back text or sign in button
            login_modal = await page.query_selector("text='welcome back'")
            sign_in_button = await page.query_selector("button:has-text('Sign in')")
            password_field = await page.query_selector("input[type='password']")
            
            if not login_modal and not sign_in_button and not password_field:
                # Double check by looking for survey content
                has_surveys = await page.query_selector("button:has-text('START SURVEY')") is not None
                has_points = await page.query_selector("*:has-text(' points')") is not None
                
                if has_surveys or has_points:
                    print("✅ Login successful! Surveys detected.")
                    return True
                else:
                    print("⏳ Login modal closed but waiting for surveys to load...")
            else:
                print("⏳ Still waiting for login... (modal still visible)")
        except Exception as e:
            print(f"⏳ Checking login status...")

async def debug_myopinions_selectors():
    """Debug script to find correct selectors with modal-based login detection"""
    
    print("🔍 MyOpinions Selector Debug V4 - Modal Detection")
    print("="*50)
    
    browser = StealthBrowserManager("quenito_myopinions")
    
    try:
        # Initialize and load cookies
        await browser.initialize_stealth_browser(transfer_cookies=False)
        await browser.load_saved_cookies()
        
        # Navigate to site
        print("\n📍 Navigating to MyOpinions...")
        await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
        await browser.page.wait_for_timeout(3000)  # Give page time to load
        
        # Check if login modal is present
        login_modal = await browser.page.query_selector("text='welcome back'")
        sign_in_button = await browser.page.query_selector("button:has-text('Sign in')")
        password_field = await browser.page.query_selector("input[type='password']")
        
        if login_modal or sign_in_button or password_field:
            # Wait for manual login
            await wait_for_login_modal_to_close(browser.page)
            
            # Give page extra time to fully load after login
            print("\n⏳ Waiting for dashboard to fully load...")
            await browser.page.wait_for_timeout(5000)
        else:
            # Check if we have surveys visible
            has_surveys = await browser.page.query_selector("button:has-text('START SURVEY')") is not None
            if has_surveys:
                print("✅ Already logged in and surveys visible!")
            else:
                print("⚠️  No login modal but also no surveys. Waiting a bit...")
                await browser.page.wait_for_timeout(5000)
        
        # Double-check we have surveys before proceeding
        start_buttons = await browser.page.query_selector_all("button:has-text('START SURVEY')")
        if not start_buttons:
            print("\n⚠️  No START SURVEY buttons found. Let me wait for manual action...")
            print("Please ensure you're logged in and on the surveys page.")
            print("Press Enter when ready to continue...")
            input()
            await browser.page.wait_for_timeout(2000)
        
        # NOW we can capture the dashboard
        print("\n📸 Capturing dashboard...")
        await browser.page.screenshot(path="debug_dashboard.png", full_page=True)
        print("✅ Screenshot saved: debug_dashboard.png")
        
        # Save current cookies for future use
        print("\n🍪 Saving fresh cookies...")
        cookies = await browser.page.context.cookies()
        import json
        with open("fresh_myopinions_cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Saved {len(cookies)} cookies")
        
        # Now do all the selector detection
        print("\n🔍 Analyzing page structure...")
        
        # Save the entire page HTML
        page_html = await browser.page.content()
        with open("dashboard_page.html", "w", encoding='utf-8') as f:
            f.write(page_html)
        print("✅ Dashboard HTML saved to dashboard_page.html")
        
        # Look for START SURVEY buttons again
        start_buttons = await browser.page.query_selector_all("button:has-text('START SURVEY')")
        print(f"\n📊 Found {len(start_buttons)} START SURVEY buttons")
        
        if start_buttons and len(start_buttons) > 0:
            # Get detailed info about survey cards
            print("\n🔍 Analyzing survey card structure...")
            
            # Method 1: Find survey cards by working up from buttons
            survey_cards_data = await browser.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button')).filter(
                        btn => btn.textContent.includes('START SURVEY')
                    );
                    
                    const cards = [];
                    buttons.forEach((button, index) => {
                        // Traverse up to find the card container
                        let element = button;
                        let cardElement = null;
                        
                        // Go up max 10 levels to find the card
                        for (let i = 0; i < 10; i++) {
                            element = element.parentElement;
                            if (!element) break;
                            
                            // Check if this element contains both points and button
                            const text = element.textContent;
                            if (text.includes('points') && element.contains(button)) {
                                // Check if this is likely the card (not too big)
                                const childButtons = element.querySelectorAll('button');
                                if (childButtons.length <= 2) {
                                    cardElement = element;
                                    break;
                                }
                            }
                        }
                        
                        if (cardElement) {
                            // Extract points value
                            const pointsMatch = cardElement.textContent.match(/(\\d+)\\s*points/i);
                            const points = pointsMatch ? pointsMatch[1] : 'Unknown';
                            
                            // Get classes at each level
                            const classes = [];
                            let el = button;
                            for (let i = 0; i < 5; i++) {
                                el = el.parentElement;
                                if (!el) break;
                                classes.push({
                                    level: i + 1,
                                    tag: el.tagName,
                                    className: el.className || 'no-class',
                                    id: el.id || 'no-id'
                                });
                            }
                            
                            cards.push({
                                index: index,
                                points: points,
                                cardTag: cardElement.tagName,
                                cardClass: cardElement.className,
                                cardId: cardElement.id,
                                hasImage: !!cardElement.querySelector('img'),
                                buttonClass: button.className,
                                hierarchy: classes,
                                innerHTML: index === 0 ? cardElement.innerHTML : null
                            });
                        }
                    });
                    
                    return cards;
                }
            """)
            
            print(f"\n📋 Found {len(survey_cards_data)} survey cards:")
            for card in survey_cards_data[:3]:  # Show first 3
                print(f"\n  Card {card['index'] + 1}:")
                print(f"    Points: {card['points']}")
                print(f"    Card tag: {card['cardTag']}")
                print(f"    Card class: {card['cardClass']}")
                print(f"    Button class: {card['buttonClass']}")
                
            # Save first card structure
            if survey_cards_data and survey_cards_data[0].get('innerHTML'):
                with open("first_survey_card.html", "w", encoding='utf-8') as f:
                    f.write(survey_cards_data[0]['innerHTML'])
                print("\n✅ First survey card HTML saved to first_survey_card.html")
        
        # Method 2: Find all elements with points
        points_analysis = await browser.page.evaluate("""
            () => {
                const pointsElements = [];
                const allElements = document.querySelectorAll('*');
                
                allElements.forEach(el => {
                    if (el.textContent.match(/\\d+\\s*points/i) && 
                        el.children.length < 10) {  // Not too many children
                        const pointsMatch = el.textContent.match(/(\\d+)\\s*points/i);
                        if (pointsMatch) {
                            pointsElements.push({
                                tag: el.tagName,
                                className: el.className,
                                points: pointsMatch[1],
                                hasButton: !!el.querySelector('button'),
                                text: el.textContent.substring(0, 100)
                            });
                        }
                    }
                });
                
                return pointsElements;
            }
        """)
        
        print(f"\n💰 Found {len(points_analysis)} elements with points:")
        for i, elem in enumerate(points_analysis[:5]):
            if elem['hasButton']:
                print(f"  {elem['tag']}.{elem['className']} - {elem['points']} points (HAS BUTTON ✓)")
        
        # Try to find common patterns
        print("\n🎯 Looking for selector patterns...")
        
        # Check various possible selectors
        selectors_to_test = [
            "div.survey-card",
            "div[class*='survey']",
            "div[class*='card']",
            "article",
            "section[class*='survey']",
            "[data-testid*='survey']",
            ".list-item",
            "div.item",
            "div[class*='MuiCard']",
            "div[class*='MuiPaper']"
        ]
        
        for selector in selectors_to_test:
            elements = await browser.page.query_selector_all(selector)
            if elements:
                print(f"  ✓ Found {len(elements)} elements matching: {selector}")
        
        print("\n✅ Analysis complete! Check generated files:")
        print("  - debug_dashboard.png (screenshot)")
        print("  - dashboard_page.html (full HTML)")
        print("  - first_survey_card.html (card structure)")
        print("  - fresh_myopinions_cookies.json (updated cookies)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Keep browser open for inspection
        print("\n⏸️  Browser will stay open for inspection.")
        print("Press Enter to close browser and exit...")
        input()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_myopinions_selectors())