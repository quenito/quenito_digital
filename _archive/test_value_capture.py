# test_value_capture.py
"""Quick test to verify we're capturing actual values, not indices"""

import asyncio
from playwright.async_api import async_playwright

async def test_radio_capture():
    """Test capturing radio button text values"""
    
    # Create a simple test page
    test_html = """
    <html>
    <body>
        <h3>Test Question</h3>
        <label><input type="radio" name="test" value="0"> Full-time worker</label><br>
        <label><input type="radio" name="test" value="1" checked> Part-time worker</label><br>
        <label><input type="radio" name="test" value="2"> Self-employed</label>
    </body>
    </html>
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.set_content(test_html)
        
        # Test the capture logic
        radio_elements = await page.query_selector_all('input[type="radio"]:checked')
        
        for radio in radio_elements:
            # Old way (gets value)
            value = await radio.get_attribute('value')
            print(f"❌ Old capture: {value}")
            
            # New way (gets label text)
            label_text = await radio.evaluate('''(el) => {
                const label = el.closest('label');
                return label ? label.textContent.trim() : null;
            }''')
            print(f"✅ New capture: {label_text}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_radio_capture())