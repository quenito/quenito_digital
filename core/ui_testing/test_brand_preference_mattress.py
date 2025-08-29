#!/usr/bin/env python3
"""
Integration test: Brand Preference - Mattress Retailers
Tests: Screenshot → Vision → Consciousness → Reasoning → UI Selection
Single-select brand preference from grid of logos
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from consciousness_engine_production import ConsciousnessEngine

class MattressRetailerTest:
    def __init__(self):
        self.engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v3.json")
        
    async def analyze_mattress_screenshot(self, screenshot_path):
        """Vision: Extract brand preference question"""
        print("👁️ STEP 1: Vision Analysis...")
        print("-" * 60)
        
        # In production, this would use actual vision analysis
        # For testing, we'll simulate the detected brands
        detected = {
            "question": "If you had to award one of these as your most preferred mattress retailer, who would win?",
            "question_type": "single_select",
            "brands": [
                "David Jones", "Sleeping Duck", "Harvey Norman",
                "Domayne", "Temple & Webster", "Freedom",
                "A-Mart", "Koala", "IKEA",
                "Forty Winks", "Beds R Us", "Myer",
                "Snooze"
            ],
            "instruction": "Don't know / Can't say"
        }
        
        print(f"Question: {detected['question']}")
        print(f"Brands detected: {len(detected['brands'])} retailers")
        print(f"Type: {detected['question_type']}")
        
        return detected
    
    async def select_preferred_retailer(self):
        """Consciousness: Determine Matt's preferred mattress retailer"""
        print("\n🧠 STEP 2: Consciousness Reasoning...")
        print("-" * 60)
        
        # Look up Matt's mattress retailer preferences
        mattress_prefs = self.engine.consciousness['brand_awareness']['mattress_retailers']
        
        # Matt purchased from Forty Winks
        preferred = mattress_prefs['purchased_from']
        
        print("Matt's mattress retailer knowledge:")
        print(f"  Know very well: {', '.join(mattress_prefs['know_very_well'])}")
        print(f"  Purchased from: {preferred}")
        print(f"  Last purchase: {mattress_prefs['last_purchase']}")
        print(f"\n✅ Selected: {preferred}")
        print(f"Reasoning: Bought from them in 2019, know them very well")
        
        return preferred
    
    async def create_test_page_with_brands(self):
        """Create HTML page with brand grid matching screenshot"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mattress Retailer Preference Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
        }
        h2 {
            text-align: center;
            font-size: 18px;
            margin-bottom: 30px;
            color: #333;
        }
        .brand-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .brand-card {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: white;
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .brand-card:hover {
            border-color: #666;
            background: #f9f9f9;
        }
        .brand-card.selected {
            border-color: #4CAF50;
            background: #e8f5e9;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
        }
        .brand-name {
            font-size: 16px;
            font-weight: 500;
            color: #333;
        }
        .brand-subtitle {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .submit-container {
            text-align: center;
            margin-top: 30px;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        .result {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            display: none;
        }
        .result.show {
            display: block;
        }
        .dont-know {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>If you had to award one of these as your most preferred mattress retailer, who would win?</h2>
        
        <div class="brand-grid">
            <div class="brand-card" data-brand="David Jones">
                <div>
                    <div class="brand-name">David Jones</div>
                    <div class="brand-subtitle">David Jones</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Sleeping Duck">
                <div>
                    <div class="brand-name">Sleeping Duck</div>
                    <div class="brand-subtitle">Sleeping Duck</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Harvey Norman">
                <div>
                    <div class="brand-name">Harvey Norman</div>
                    <div class="brand-subtitle">Harvey Norman</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Domayne">
                <div>
                    <div class="brand-name">Domayne</div>
                    <div class="brand-subtitle">Domayne</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Temple & Webster">
                <div>
                    <div class="brand-name">Temple & Webster</div>
                    <div class="brand-subtitle">Temple & Webster</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Freedom">
                <div>
                    <div class="brand-name">Freedom</div>
                    <div class="brand-subtitle">Freedom</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="A-Mart">
                <div>
                    <div class="brand-name">A-Mart</div>
                    <div class="brand-subtitle">A-Mart Furniture</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Koala">
                <div>
                    <div class="brand-name">Koala</div>
                    <div class="brand-subtitle">Koala</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="IKEA">
                <div>
                    <div class="brand-name">IKEA</div>
                    <div class="brand-subtitle">Ikea</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Forty Winks">
                <div>
                    <div class="brand-name">Forty Winks</div>
                    <div class="brand-subtitle">Forty Winks</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Beds R Us">
                <div>
                    <div class="brand-name">Beds R Us</div>
                    <div class="brand-subtitle">Beds R Us</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Myer">
                <div>
                    <div class="brand-name">Myer</div>
                    <div class="brand-subtitle">Myer</div>
                </div>
            </div>
            
            <div class="brand-card" data-brand="Snooze">
                <div>
                    <div class="brand-name">Snooze</div>
                    <div class="brand-subtitle">Snooze</div>
                </div>
            </div>
        </div>
        
        <div class="dont-know">Don't know / Can't say</div>
        
        <div class="submit-container">
            <button id="submitBtn" onclick="submitSelection()">Submit Selection</button>
        </div>
        
        <div id="result" class="result">
            <strong>✅ Selection Submitted!</strong>
            <p id="selectedBrand"></p>
        </div>
    </div>
    
    <script>
        let selectedBrand = null;
        
        document.querySelectorAll('.brand-card').forEach(card => {
            card.addEventListener('click', function() {
                // Remove previous selection
                document.querySelectorAll('.brand-card').forEach(c => {
                    c.classList.remove('selected');
                });
                
                // Add selection to clicked card
                this.classList.add('selected');
                selectedBrand = this.getAttribute('data-brand');
            });
        });
        
        function submitSelection() {
            if (selectedBrand) {
                document.getElementById('selectedBrand').textContent = 
                    'Selected: ' + selectedBrand;
                document.getElementById('result').classList.add('show');
            } else {
                alert('Please select a mattress retailer');
            }
        }
    </script>
</body>
</html>"""
        
        html_file = Path(__file__).parent / "mattress_retailer_test.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
    
    async def automate_brand_selection(self, preferred_brand, headless=False):
        """Playwright: Click on the preferred brand"""
        print("\n✋ STEP 3: UI Automation (Brand Selection)...")
        print("-" * 60)
        
        html_file = await self.create_test_page_with_brands()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(f"file://{html_file.absolute()}")
            print("📄 Loaded mattress retailer preference page")
            
            # Click on the preferred brand
            print(f"\n🎯 Clicking on: {preferred_brand}")
            await page.click(f'.brand-card[data-brand="{preferred_brand}"]')
            await asyncio.sleep(3)  # Pause to see selection
            
            # Submit selection
            print("📤 Submitting selection...")
            await page.click('#submitBtn')
            await asyncio.sleep(2)
            
            # Verify result
            result_visible = await page.is_visible('#result.show')
            if result_visible:
                result_text = await page.text_content('#selectedBrand')
                print(f"✅ Success! {result_text}")
            
            if not headless:
                print("\n👀 Browser will remain open")
                print("Press Enter to close...")
                input()
            
            await browser.close()
    
    async def run_full_test(self, screenshot_path):
        """Run complete brand preference test"""
        print("="*70)
        print("🚀 BRAND PREFERENCE TEST - MATTRESS RETAILERS")
        print("="*70)
        
        # Step 1: Vision
        detected = await self.analyze_mattress_screenshot(screenshot_path)
        
        # Step 2: Consciousness
        preferred = await self.select_preferred_retailer()
        
        # Step 3: UI Automation
        await self.automate_brand_selection(preferred, headless=False)
        
        print("\n="*70)
        print("✨ BRAND PREFERENCE TEST COMPLETE")
        print("="*70)

async def main():
    screenshot_path = "screenshots/mattress_retailer_preference.png"
    
    print("📸 Save the mattress retailer screenshot as:")
    print(f"   {screenshot_path}")
    input("\nPress Enter to test...")
    
    if not os.path.exists(screenshot_path):
        print(f"❌ Screenshot not found: {screenshot_path}")
        return
    
    test = MattressRetailerTest()
    await test.run_full_test(screenshot_path)

if __name__ == "__main__":
    asyncio.run(main())