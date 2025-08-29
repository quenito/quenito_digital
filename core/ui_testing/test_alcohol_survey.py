#!/usr/bin/env python3
"""
Quick test to verify consciousness engine ignores pre-selected options
and returns Matt's authentic alcohol consumption patterns
"""

import asyncio
from consciousness_engine_production import ConsciousnessEngine

async def test_alcohol_screenshot():
    # Initialize engine with Matt's consciousness
    engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v2.json")
    
    # Test the alcohol consumption screenshot
    screenshot_path = "screenshots/alcohol_consumption_survey.png"  # Save the screenshot with this name
    
    print("="*70)
    print("🍺 ALCOHOL CONSUMPTION TEST")
    print("="*70)
    print("\nTesting if consciousness engine ignores pre-selected options...")
    print("\nMatt's actual drinking patterns from consciousness:")
    print("- Beer: Pale ales, 1-2 weekdays, 3-4 weekends")
    print("- Sparkling cider: Every few months")
    print("- Wine: 1-2 times per year")
    print("- Spirits: Rarely, sometimes not even once a year")
    print("\n" + "="*70)
    
    # Run the test
    result = await engine.test_screenshot_flow(screenshot_path)
    
    print(f"\n📋 Extracted Question: {result['question']}")
    print(f"❓ Question Type: {result.get('question_type', 'unknown')}")
    
    if result.get('grid_items'):
        print(f"\n📊 Grid Items Detected: {', '.join(result['grid_items'])}")
    
    print(f"\n🎯 LLM Answer Based on Matt's Consciousness:")
    
    if isinstance(result['llm_answer'], dict):
        # Grid question - display each beverage and its frequency
        print("\n   Grid Responses:")
        for beverage, frequency in result['llm_answer'].items():
            checkmark = "✓" if frequency != "Never" else " "
            print(f"   [{checkmark}] {beverage:30s} → {frequency}")
    elif isinstance(result['llm_answer'], list):
        # Multi-select question
        print(f"   Selected {len(result['llm_answer'])} options:")
        for answer in result['llm_answer']:
            print(f"   • {answer}")
    else:
        # Single answer
        print(f"   {result['llm_answer']}")
    
    print(f"\n💭 Confidence: {result['confidence']:.0%}")
    print(f"\n🧠 Reasoning: {result['reasoning'][:300]}...")
    
    # Check if the answer matches Matt's actual patterns
    print("\n" + "="*70)
    print("✅ VALIDATION:")
    print("The LLM should select:")
    print("- Beer: Within the past week (or past month)")
    print("- Spirits: Not within the past year (or never)")
    print("- Wine: Within the past six months (or past year)")
    print("- Cider: Within the past six months")
    print("- Other categories: Never or Not within past year")
    
    return result

if __name__ == "__main__":
    asyncio.run(test_alcohol_screenshot())