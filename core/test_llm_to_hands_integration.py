#!/usr/bin/env python3
"""
Integration test: LLM Consciousness → Playwright Hands → Form Completion
Tests the full flow from reasoning to UI interaction
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from consciousness_engine_production import ConsciousnessEngine

class LLMToHandsIntegration:
    def __init__(self):
        self.engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v3.json")
        # Map LLM response text to form values
        self.timeframe_mapping = {
            "Within the last week": "week",
            "Within the past week": "week",
            "Within the past month": "month",
            "Within the past month (but not in the last week)": "month",
            "Within the past six months": "six_months",
            "Within the past year": "year",
            "Not within the past year": "never",
            "Not within the past year, or never": "never",
            "Never": "never"
        }
        
        # Map item names to form field names
        self.field_mapping = {
            "Beer": "beer",
            "Spirits": "spirits",
            "Red wine (incl. Rose)": "red_wine",
            "White wine (incl. Dessert Wine)": "white_wine",
            "Sparkling wine": "sparkling_wine",
            "Other wine": "other_wine",
            "Cider": "cider",
            "Other alcohol type (incl. Alcoholic Ginger Beer & Seltzer)": "other_alcohol"
        }
    
    async def get_llm_answers(self, screenshot_path):
        """Get Matt's consciousness-based answers for the alcohol grid"""
        print("🧠 STEP 1: Consciousness Engine Processing...")
        print("-" * 60)
        
        result = await self.engine.test_screenshot_flow(screenshot_path)
        
        print(f"Question detected: {result['question'][:100]}...")
        print(f"Question type: {result.get('question_type', 'unknown')}")
        print(f"Confidence: {result['confidence']:.0%}")
        
        if isinstance(result['llm_answer'], dict):
            print("\n📊 Matt's Answers:")
            for item, timeframe in result['llm_answer'].items():
                print(f"  • {item}: {timeframe}")
        
        return result['llm_answer']
    
    async def fill_form_with_playwright(self, llm_answers, headless=False):
        """Use Playwright to fill the form based on LLM answers"""
        print("\n✋ STEP 2: Playwright Hands Executing...")
        print("-" * 60)
        
        # Get the absolute path to the HTML file
        html_file = Path(__file__).parent / "alcohol_grid_test.html"
        if not html_file.exists():
            raise FileNotFoundError(f"HTML test file not found. Please save the HTML as: {html_file}")
        
        async with async_playwright() as p:
            # Launch browser (visible by default for testing)
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            # Navigate to local HTML file
            await page.goto(f"file://{html_file.absolute()}")
            print(f"📄 Loaded test page: {html_file.name}")
            
            # Fill each item based on LLM answers
            selections_made = []
            
            for item_name, timeframe in llm_answers.items():
                # Get the form field name
                field_name = self.field_mapping.get(item_name)
                if not field_name:
                    print(f"⚠️  No field mapping for: {item_name}")
                    continue
                
                # Get the value to select
                value = self.timeframe_mapping.get(timeframe)
                if not value:
                    print(f"⚠️  No value mapping for timeframe: {timeframe}")
                    continue
                
                # Select the radio button
                selector = f'input[name="{field_name}"][value="{value}"]'
                try:
                    await page.click(selector)
                    selections_made.append(f"{item_name} → {timeframe}")
                    print(f"✅ Selected: {item_name} → {timeframe}")
                    await asyncio.sleep(5)  # 5 second delay to watch each selection
                except Exception as e:
                    print(f"❌ Failed to select {item_name}: {e}")
            
            # Submit the form
            print("\n📤 Submitting form...")
            await page.click('button.submit-btn')
            await asyncio.sleep(1)  # Wait for results to show
            
            # Check if results appeared
            results_visible = await page.is_visible('#results.show')
            if results_visible:
                print("✅ Form submitted successfully!")
                results_text = await page.text_content('#resultsContent')
                print("\n📋 Submitted values:")
                print(results_text)
            else:
                print("⚠️  Results div not visible after submission")
            
            # Keep browser open for manual inspection
            if not headless:
                print("\n👀 Browser will remain open for inspection")
                print("Press Enter in the terminal when you're ready to close it...")
                input()  # Wait for user input before closing
            
            await browser.close()
            
            return selections_made
    
    async def run_full_integration(self, screenshot_path):
        """Run the complete integration test"""
        print("="*70)
        print("🚀 LLM → HANDS → FORM INTEGRATION TEST")
        print("="*70)
        
        # Step 1: Get LLM answers
        llm_answers = await self.get_llm_answers(screenshot_path)
        
        if not isinstance(llm_answers, dict):
            print("❌ LLM did not return grid answers. Got:", llm_answers)
            return False
        
        # Step 2: Fill form with Playwright
        selections = await self.fill_form_with_playwright(llm_answers, headless=False)
        
        # Step 3: Validate
        print("\n="*70)
        print("✨ INTEGRATION TEST COMPLETE")
        print("="*70)
        print(f"Total selections made: {len(selections)}")
        print(f"Expected selections: {len(llm_answers)}")
        
        success = len(selections) == len(llm_answers)
        if success:
            print("✅ SUCCESS: All LLM answers were successfully entered into the form!")
        else:
            print("⚠️  PARTIAL SUCCESS: Some selections may have failed")
        
        return success

async def main():
    # First, save the HTML file
    print("📝 Please ensure you've saved the HTML file as: alcohol_grid_test.html")
    print("   (Save the HTML artifact content to this file in the same directory)")
    
    input("\nPress Enter when ready to run the test...")
    
    # Run the integration test
    integration = LLMToHandsIntegration()
    
    # Use your existing screenshot
    screenshot_path = "screenshots/alcohol_consumption_survey.png"
    
    if not os.path.exists(screenshot_path):
        print(f"❌ Screenshot not found: {screenshot_path}")
        print("Please ensure the alcohol survey screenshot exists")
        return
    
    success = await integration.run_full_integration(screenshot_path)
    
    if success:
        print("\n🎉 Integration validated! The consciousness engine successfully")
        print("   guided Playwright to complete the form as Matt would.")

if __name__ == "__main__":
    asyncio.run(main())