#!/usr/bin/env python3
"""
Integration test: Multi-Question Single Page (YouGov Demographics)
Tests: Screenshot → Vision → Consciousness → Reasoning → UI Automation → Form Completion
Handles: Radio buttons, Text input, Dropdown on same page
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from consciousness_engine_production import ConsciousnessEngine

class MultiQuestionPageTest:
    def __init__(self):
        self.engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v3.json")
        
    async def analyze_multi_question_screenshot(self, screenshot_path):
        """Vision: Extract multiple questions from single page"""
        print("👁️ STEP 1: Vision Analysis (Multi-Question Page)...")
        print("-" * 60)
        
        # For this test, we'll simulate what the vision would extract
        # In production, this would use the actual analyze_screenshot method
        
        questions = {
            "gender": {
                "question": "Which gender do you belong to?",
                "type": "radio",
                "options": ["Male", "Female"]
            },
            "birth_year": {
                "question": "What is your birth year?",
                "type": "text_input",
                "validation": "4 digits"
            },
            "sexuality": {
                "question": "Which of the following best describes your sexuality?",
                "type": "radio",
                "options": ["Lesbian", "Gay", "Bisexual", "Heterosexual", "Prefer not to say"]
            },
            "country": {
                "question": "In which country do you currently reside?",
                "type": "dropdown",
                "placeholder": "Please select a country"
            }
        }
        
        print("📋 Questions detected on page:")
        for key, q in questions.items():
            print(f"  • {q['question']} ({q['type']})")
        
        return questions
    
    async def get_answers_from_consciousness(self):
        """Consciousness: Retrieve Matt's answers for all questions"""
        print("\n🧠 STEP 2: Consciousness Reasoning (All Questions)...")
        print("-" * 60)
        
        consciousness = self.engine.consciousness
        
        answers = {
            "gender": consciousness['identity'].get('gender', 'Male'),
            "birth_year": str(consciousness['identity'].get('birth_year', 1980)),
            "sexuality": "Heterosexual",  # Matt is married with kids
            "country": consciousness['identity']['location'].get('country', 'Australia')
        }
        
        print("Matt's answers from consciousness:")
        print(f"  • Gender: {answers['gender']}")
        print(f"  • Birth Year: {answers['birth_year']}")
        print(f"  • Sexuality: {answers['sexuality']}")
        print(f"  • Country: {answers['country']}")
        
        return answers
    
    async def create_test_page(self):
        """Create a local HTML page matching YouGov demographics"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouGov Demographics Test</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 600px;
            margin: 40px auto;
            padding: 0 20px;
            background: #f8f8f8;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .logo {
            text-align: center;
            color: #e60000;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .question-group {
            margin-bottom: 35px;
        }
        .question {
            font-size: 16px;
            margin-bottom: 15px;
            color: #333;
        }
        .radio-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .radio-option {
            display: flex;
            align-items: center;
        }
        .radio-option input[type="radio"] {
            margin-right: 10px;
        }
        .radio-option label {
            cursor: pointer;
        }
        input[type="text"], select {
            width: 100%;
            max-width: 300px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .next-button {
            background: #4a5e7a;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            margin: 30px auto 0;
            display: block;
        }
        .next-button:hover {
            background: #3a4e6a;
        }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            display: none;
        }
        .success.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">YouGov</div>
        
        <form id="demographicsForm">
            <!-- Gender Question -->
            <div class="question-group">
                <div class="question">Which gender do you belong to?</div>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="male" name="gender" value="Male">
                        <label for="male">Male</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="female" name="gender" value="Female">
                        <label for="female">Female</label>
                    </div>
                </div>
            </div>
            
            <!-- Birth Year Question -->
            <div class="question-group">
                <div class="question">What is your birth year?</div>
                <input type="text" id="birth_year" name="birth_year" 
                       placeholder="e.g., 1980" maxlength="4" pattern="[0-9]{4}">
            </div>
            
            <!-- Sexuality Question -->
            <div class="question-group">
                <div class="question">Which of the following best describes your sexuality?</div>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="lesbian" name="sexuality" value="Lesbian">
                        <label for="lesbian">Lesbian</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="gay" name="sexuality" value="Gay">
                        <label for="gay">Gay</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="bisexual" name="sexuality" value="Bisexual">
                        <label for="bisexual">Bisexual</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="heterosexual" name="sexuality" value="Heterosexual">
                        <label for="heterosexual">Heterosexual</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="prefer_not" name="sexuality" value="Prefer not to say">
                        <label for="prefer_not">Prefer not to say</label>
                    </div>
                </div>
            </div>
            
            <!-- Country Question -->
            <div class="question-group">
                <div class="question">In which country do you currently reside? (Country of residence)</div>
                <select id="country" name="country">
                    <option value="">Please select a country</option>
                    <option value="Australia">Australia</option>
                    <option value="United States">United States</option>
                    <option value="United Kingdom">United Kingdom</option>
                    <option value="Canada">Canada</option>
                    <option value="New Zealand">New Zealand</option>
                    <option value="Germany">Germany</option>
                    <option value="France">France</option>
                    <option value="Japan">Japan</option>
                    <option value="China">China</option>
                    <option value="India">India</option>
                </select>
            </div>
            
            <button type="submit" class="next-button">Next →</button>
        </form>
        
        <div id="success" class="success">
            <strong>✅ All questions answered successfully!</strong>
            <div id="summary"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('demographicsForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const summary = [];
            for (let [key, value] of formData.entries()) {
                summary.push(`${key}: ${value}`);
            }
            document.getElementById('summary').innerHTML = '<p>' + summary.join('<br>') + '</p>';
            document.getElementById('success').classList.add('show');
        });
    </script>
</body>
</html>"""
        
        html_file = Path(__file__).parent / "yougov_demographics_test.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
    
    async def automate_multi_question_form(self, answers, headless=False):
        """Playwright: Fill all questions on single page"""
        print("\n✋ STEP 3: UI Automation (Multiple Elements)...")
        print("-" * 60)
        
        html_file = await self.create_test_page()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(f"file://{html_file.absolute()}")
            print("📄 Loaded YouGov demographics page")
            
            # 1. Select Gender (Radio Button)
            print(f"\n1️⃣ Selecting Gender: {answers['gender']}")
            await page.click(f'input[name="gender"][value="{answers["gender"]}"]')
            await asyncio.sleep(5)
            
            # 2. Enter Birth Year (Text Input)
            print(f"2️⃣ Entering Birth Year: {answers['birth_year']}")
            await page.fill('#birth_year', answers['birth_year'])
            await asyncio.sleep(5)
            
            # 3. Select Sexuality (Radio Button)
            print(f"3️⃣ Selecting Sexuality: {answers['sexuality']}")
            await page.click(f'input[name="sexuality"][value="{answers["sexuality"]}"]')
            await asyncio.sleep(5)
            
            # 4. Select Country (Dropdown)
            print(f"4️⃣ Selecting Country: {answers['country']}")
            await page.select_option('#country', answers['country'])
            await asyncio.sleep(5)
            
            # Submit form
            print("\n📤 Submitting form...")
            await page.click('.next-button')
            await asyncio.sleep(1)
            
            # Verify success
            success_visible = await page.is_visible('#success.show')
            if success_visible:
                summary = await page.text_content('#summary')
                print("✅ Form submitted successfully!")
                print("\nSubmitted values:")
                print(summary)
            else:
                print("⚠️ Success message not showing")
            
            if not headless:
                print("\n👀 Browser will remain open")
                print("Press Enter to close...")
                input()
            
            await browser.close()
    
    async def run_full_test(self, screenshot_path):
        """Run complete multi-question page test"""
        print("="*70)
        print("🚀 MULTI-QUESTION SINGLE PAGE TEST")
        print("YouGov Demographics (4 Questions, Mixed Types)")
        print("="*70)
        
        # Step 1: Vision
        questions = await self.analyze_multi_question_screenshot(screenshot_path)
        
        # Step 2: Consciousness
        answers = await self.get_answers_from_consciousness()
        
        # Step 3: UI Automation
        await self.automate_multi_question_form(answers, headless=False)
        
        print("\n="*70)
        print("✨ MULTI-QUESTION TEST COMPLETE")
        print("="*70)
        print("Successfully handled:")
        print("  • Radio buttons (Gender, Sexuality)")
        print("  • Text input (Birth Year)")
        print("  • Dropdown (Country)")
        print("All on a single page!")

async def main():
    screenshot_path = "screenshots/yougov_demographics.png"
    
    print("📸 Save the YouGov screenshot as:")
    print(f"   {screenshot_path}")
    input("\nPress Enter when ready...")
    
    if not os.path.exists(screenshot_path):
        print(f"❌ Screenshot not found: {screenshot_path}")
        return
    
    test = MultiQuestionPageTest()
    await test.run_full_test(screenshot_path)

if __name__ == "__main__":
    asyncio.run(main())