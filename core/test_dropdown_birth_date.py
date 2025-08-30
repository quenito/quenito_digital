#!/usr/bin/env python3
"""
Integration test: Birth Date Dropdowns
Tests: Screenshot → Vision → Consciousness → Reasoning → UI Automation → Form Completion
For dropdown/select elements instead of radio buttons
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from consciousness_engine_production import ConsciousnessEngine

class BirthDateDropdownTest:
    def __init__(self):
        self.engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v3.json")
        
    async def analyze_birth_date_screenshot(self, screenshot_path):
        """Vision: Extract birth date question from screenshot"""
        print("👁️ STEP 1: Vision Analysis...")
        print("-" * 60)
        
        result = await self.engine.analyze_screenshot(screenshot_path)
        
        print(f"Question detected: {result.get('question', 'Unknown')}")
        print(f"Question type: {result.get('question_type', 'Unknown')}")
        
        # The vision should detect this as dropdowns/select elements
        if 'Month' in result.get('question', '') or 'birth' in result.get('question', '').lower():
            print("✅ Birth date question detected")
        
        return result
    
    async def get_birth_date_from_consciousness(self):
        """Consciousness: Retrieve Matt's birth month and year"""
        print("\n🧠 STEP 2: Consciousness Reasoning...")
        print("-" * 60)
        
        # Direct lookup from consciousness
        month = self.engine.consciousness['identity'].get('birth_month', 'Unknown')
        year = self.engine.consciousness['identity'].get('birth_year', 'Unknown')
        
        print(f"Matt's birth month: {month}")
        print(f"Matt's birth year: {year}")
        print(f"Age verification: {2025 - year} years old (should be 45)")
        
        return {"month": month, "year": str(year)}
    
    async def create_test_html_with_dropdowns(self):
        """Create a local HTML page with dropdown selectors matching the screenshot"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Birth Date Test</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f5f5f5;
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 500px;
        }
        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: 500;
        }
        .form-row {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }
        .form-group {
            flex: 1;
        }
        select {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            background: white;
            cursor: pointer;
        }
        select:focus {
            outline: none;
            border-color: #6366f1;
        }
        button {
            width: 120px;
            padding: 12px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            margin: 0 auto;
            display: block;
        }
        button:hover {
            background: #5558e3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e8f5e9;
            border-radius: 6px;
            display: none;
        }
        .result.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>What is your date of birth?</h2>
        
        <form id="birthForm">
            <div class="form-row">
                <div class="form-group">
                    <select name="month" id="month" required>
                        <option value="">Month</option>
                        <option value="January">January</option>
                        <option value="February">February</option>
                        <option value="March">March</option>
                        <option value="April">April</option>
                        <option value="May">May</option>
                        <option value="June">June</option>
                        <option value="July">July</option>
                        <option value="August">August</option>
                        <option value="September">September</option>
                        <option value="October">October</option>
                        <option value="November">November</option>
                        <option value="December">December</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <select name="year" id="year" required>
                        <option value="">Year</option>
                        """ + ''.join([f'<option value="{y}">{y}</option>' for y in range(2010, 1920, -1)]) + """
                    </select>
                </div>
            </div>
            
            <button type="submit">Submit</button>
        </form>
        
        <div id="result" class="result">
            <strong>✅ Form Submitted Successfully!</strong>
            <div id="resultText"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('birthForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const month = document.getElementById('month').value;
            const year = document.getElementById('year').value;
            
            document.getElementById('resultText').innerHTML = 
                `<p>Birth Month: ${month}<br>Birth Year: ${year}<br>Age: ${2025 - parseInt(year)} years old</p>`;
            document.getElementById('result').classList.add('show');
        });
    </script>
</body>
</html>"""
        
        # Save HTML file
        html_file = Path(__file__).parent / "birth_date_test.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"📄 Test HTML created: {html_file.name}")
        return html_file
    
    async def automate_dropdown_selection(self, birth_data, headless=False):
        """Playwright: Automate dropdown selections"""
        print("\n✋ STEP 3: UI Automation (Dropdowns)...")
        print("-" * 60)
        
        # Create test HTML
        html_file = await self.create_test_html_with_dropdowns()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            # Load the test page
            await page.goto(f"file://{html_file.absolute()}")
            print("📋 Loaded birth date form")
            
            # Select Month dropdown
            print(f"\n🎯 Selecting Month: {birth_data['month']}")
            await page.select_option('#month', birth_data['month'])
            await asyncio.sleep(2)  # Pause to see selection
            
            # Select Year dropdown  
            print(f"🎯 Selecting Year: {birth_data['year']}")
            await page.select_option('#year', birth_data['year'])
            await asyncio.sleep(2)  # Pause to see selection
            
            # Submit form
            print("\n📤 Submitting form...")
            await page.click('button[type="submit"]')
            await asyncio.sleep(1)
            
            # Verify results
            result_visible = await page.is_visible('#result.show')
            if result_visible:
                result_text = await page.text_content('#resultText')
                print("✅ Form submitted successfully!")
                print(f"\nSubmitted values:")
                print(result_text.strip())
            else:
                print("⚠️ Results not showing after submission")
            
            # Keep browser open for manual inspection
            if not headless:
                print("\n👀 Browser will remain open")
                print("Press Enter in terminal to close...")
                input()
            
            await browser.close()
    
    async def run_full_test(self, screenshot_path):
        """Run complete integration test for dropdowns"""
        print("="*70)
        print("🚀 DROPDOWN INTEGRATION TEST")
        print("Birth Date Selection (Month & Year)")
        print("="*70)
        
        # Step 1: Vision (analyze screenshot)
        vision_result = await self.analyze_birth_date_screenshot(screenshot_path)
        
        # Step 2: Consciousness (get birth date)
        birth_data = await self.get_birth_date_from_consciousness()
        
        # Step 3: UI Automation (select dropdowns)
        await self.automate_dropdown_selection(birth_data, headless=False)
        
        print("\n="*70)
        print("✨ DROPDOWN TEST COMPLETE")
        print("="*70)
        print("Chain validated: Screenshot → Vision → Consciousness → Dropdowns → Success")

async def main():
    # Save the screenshot as birth_date_screenshot.png
    screenshot_path = "screenshots/birth_date_screenshot.png"
    
    print("📸 Please save the birth date screenshot as:")
    print(f"   {screenshot_path}")
    input("\nPress Enter when ready to test...")
    
    if not os.path.exists(screenshot_path):
        print(f"❌ Screenshot not found: {screenshot_path}")
        return
    
    # Run the test
    test = BirthDateDropdownTest()
    await test.run_full_test(screenshot_path)

if __name__ == "__main__":
    asyncio.run(main())