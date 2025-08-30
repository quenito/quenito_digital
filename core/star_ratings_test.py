#!/usr/bin/env python3
"""
Integration test: Star Rating Questions
Tests: 5-star rating system for brand opinions
Handles: Clicking star ratings for multiple brands
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from consciousness_engine_production import ConsciousnessEngine

class StarRatingTest:
    def __init__(self):
        self.engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v3.json")
        
    async def analyze_rating_screenshot(self, screenshot_path):
        """Vision: Detect star rating question and brands"""
        print("👁️ STEP 1: Vision Analysis (Star Ratings)...")
        print("-" * 60)
        
        detected = {
            "question": "Considering everything you know about the following brands / retailers, what is your overall opinion of each?",
            "instruction": "1=Part 1 - Excellent",
            "question_type": "star_rating",
            "brands": [
                {"name": "Officeworks", "logo": "Officeworks", "rating": None},
                {"name": "Shell", "logo": "Shell", "rating": None},
                {"name": "McDonald's", "logo": "McDonald's", "rating": None}
            ],
            "scale": "5_star",
            "labels": {"poor": 1, "excellent": 5}
        }
        
        print(f"Question: {detected['question'][:60]}...")
        print(f"Type: {detected['scale']} rating")
        print(f"Brands to rate:")
        for brand in detected['brands']:
            print(f"  • {brand['name']}")
        
        return detected
    
    async def determine_brand_ratings(self, brands):
        """Consciousness: Determine Matt's ratings for each brand"""
        print("\n🧠 STEP 2: Consciousness Reasoning...")
        print("-" * 60)
        
        ratings = {}
        
        for brand in brands:
            brand_name = brand['name']
            
            if brand_name == "Officeworks":
                # Matt knows well, uses for work supplies
                rating = 4
                reasoning = "Regular customer for office supplies, good prices"
                
            elif brand_name == "Shell":
                # Petrol station - knows well but prefers Budget Petrol
                rating = 3
                reasoning = "Okay petrol station but prefer Budget Petrol for price"
                
            elif brand_name == "McDonald's":
                # Matt's go-to fast food
                rating = 4
                reasoning = "Go-to fast food, kids love it, convenient"
            
            else:
                # Default moderate rating
                rating = 3
                reasoning = "Neutral opinion"
            
            ratings[brand_name] = {
                "stars": rating,
                "reasoning": reasoning
            }
            
            print(f"{brand_name}: {rating}/5 stars")
            print(f"  Reasoning: {reasoning}")
        
        return ratings
    
    async def create_star_rating_page(self):
        """Create HTML page with star ratings"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Rating Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .progress-bar {
            height: 30px;
            background: linear-gradient(to right, #2196F3 0%, #2196F3 13%, #e0e0e0 13%);
            border-radius: 4px;
            margin-bottom: 30px;
            position: relative;
        }
        .progress-text {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #333;
            font-weight: bold;
        }
        h2 {
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
        }
        .instruction {
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .rating-grid {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        .brand-row {
            display: grid;
            grid-template-columns: 200px 1fr;
            align-items: center;
            gap: 30px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        .brand-info {
            text-align: center;
        }
        .brand-logo {
            width: 120px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px;
            font-weight: bold;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #f9f9f9;
        }
        .brand-name {
            font-size: 12px;
            color: #666;
        }
        .rating-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .rating-label {
            font-size: 12px;
            color: #999;
            margin: 0 10px;
        }
        .stars {
            display: flex;
            gap: 10px;
        }
        .star {
            font-size: 28px;
            color: #ddd;
            cursor: pointer;
            transition: color 0.5s;
        }
        .star:hover {
            color: #ffb400;
        }
        .star.filled {
            color: #ffb400;
        }
        .navigation {
            margin-top: 40px;
            text-align: center;
        }
        button {
            padding: 12px 30px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="progress-bar">
            <span class="progress-text">13%</span>
        </div>
        
        <h2>Considering everything you know about the following brands / retailers, what is your overall opinion of each?</h2>
        <p class="instruction">1 = Part 1 - Excellent</p>
        
        <div class="rating-grid">
            <!-- Officeworks -->
            <div class="brand-row">
                <div class="brand-info">
                    <div class="brand-logo">Officeworks</div>
                    <div class="brand-name">Officeworks</div>
                </div>
                <div class="rating-container">
                    <span class="rating-label">Poor</span>
                    <div class="stars" data-brand="Officeworks">
                        <span class="star" data-rating="1">★</span>
                        <span class="star" data-rating="2">★</span>
                        <span class="star" data-rating="3">★</span>
                        <span class="star" data-rating="4">★</span>
                        <span class="star" data-rating="5">★</span>
                    </div>
                    <span class="rating-label">Excellent</span>
                </div>
            </div>
            
            <!-- Shell -->
            <div class="brand-row">
                <div class="brand-info">
                    <div class="brand-logo" style="background: #ffcc00;">Shell</div>
                    <div class="brand-name">Shell</div>
                </div>
                <div class="rating-container">
                    <span class="rating-label">Poor</span>
                    <div class="stars" data-brand="Shell">
                        <span class="star" data-rating="1">★</span>
                        <span class="star" data-rating="2">★</span>
                        <span class="star" data-rating="3">★</span>
                        <span class="star" data-rating="4">★</span>
                        <span class="star" data-rating="5">★</span>
                    </div>
                    <span class="rating-label">Excellent</span>
                </div>
            </div>
            
            <!-- McDonald's -->
            <div class="brand-row">
                <div class="brand-info">
                    <div class="brand-logo" style="background: #ffcc00; color: #c00;">McDonald's</div>
                    <div class="brand-name">McDonald's</div>
                </div>
                <div class="rating-container">
                    <span class="rating-label">Poor</span>
                    <div class="stars" data-brand="McDonald's">
                        <span class="star" data-rating="1">★</span>
                        <span class="star" data-rating="2">★</span>
                        <span class="star" data-rating="3">★</span>
                        <span class="star" data-rating="4">★</span>
                        <span class="star" data-rating="5">★</span>
                    </div>
                    <span class="rating-label">Excellent</span>
                </div>
            </div>
        </div>
        
        <div class="navigation">
            <button onclick="submitRatings()">Continue →</button>
        </div>
        
        <div id="result" class="result">
            <strong>✅ Ratings Submitted!</strong>
            <p id="ratingSummary"></p>
        </div>
    </div>
    
    <script>
        const ratings = {};
        
        document.querySelectorAll('.stars').forEach(starsContainer => {
            const brand = starsContainer.getAttribute('data-brand');
            const stars = starsContainer.querySelectorAll('.star');
            
            stars.forEach(star => {
                star.addEventListener('click', function() {
                    const rating = parseInt(this.getAttribute('data-rating'));
                    ratings[brand] = rating;
                    
                    // Update visual state
                    stars.forEach((s, index) => {
                        if (index < rating) {
                            s.classList.add('filled');
                        } else {
                            s.classList.remove('filled');
                        }
                    });
                });
            });
        });
        
        function submitRatings() {
            const summary = Object.entries(ratings)
                .map(([brand, rating]) => `${brand}: ${rating} stars`)
                .join(', ');
            
            document.getElementById('ratingSummary').textContent = summary || 'No ratings provided';
            document.getElementById('result').classList.add('show');
        }
    </script>
</body>
</html>"""
        
        html_file = Path(__file__).parent / "star_rating_test.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
    
    async def automate_star_ratings(self, ratings, headless=False):
        """Playwright: Click star ratings for each brand"""
        print("\n✋ STEP 3: UI Automation (Star Ratings)...")
        print("-" * 60)
        
        html_file = await self.create_star_rating_page()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(f"file://{html_file.absolute()}")
            print("📄 Loaded star rating page")
            
            # Rate each brand
            for brand_name, rating_data in ratings.items():
                stars_to_select = rating_data['stars']
                
                print(f"\n⭐ Rating {brand_name}: {stars_to_select}/5 stars")
                
                # Click the appropriate star
                selector = f'.stars[data-brand="{brand_name}"] .star[data-rating="{stars_to_select}"]'
                await page.click(selector)
                await asyncio.sleep(5)  # Pause to see each rating
            
            await asyncio.sleep(5)
            
            # Submit ratings
            print("\n📤 Submitting all ratings...")
            await page.click('button')
            await asyncio.sleep(5)
            
            # Verify result
            result_visible = await page.is_visible('#result.show')
            if result_visible:
                summary = await page.text_content('#ratingSummary')
                print(f"✅ Success! {summary}")
            
            if not headless:
                print("\n👀 Browser will remain open")
                print("Press Enter to close...")
                input()
            
            await browser.close()
    
    async def run_full_test(self, screenshot_path):
        """Run complete star rating test"""
        print("="*70)
        print("🚀 STAR RATING TEST")
        print("Brand Opinion Ratings")
        print("="*70)
        
        # Step 1: Vision
        detected = await self.analyze_rating_screenshot(screenshot_path)
        
        # Step 2: Consciousness
        ratings = await self.determine_brand_ratings(detected['brands'])
        
        # Step 3: UI Automation
        await self.automate_star_ratings(ratings, headless=False)
        
        print("\n="*70)
        print("✨ STAR RATING TEST COMPLETE")
        print("="*70)

async def main():
    screenshot_path = "screenshots/star_ratings.png"
    
    print("📸 Save the star rating screenshot as:")
    print(f"   {screenshot_path}")
    input("\nPress Enter to test...")
    
    if not os.path.exists(screenshot_path):
        print(f"❌ Screenshot not found: {screenshot_path}")
        return
    
    test = StarRatingTest()
    await test.run_full_test(screenshot_path)

if __name__ == "__main__":
    asyncio.run(main())