# test_all_screenshots.py
import asyncio
import os
import json
from vision_mvp import QuenitoVision

async def test_all():
    vision = QuenitoVision()
    
    test_dir = "screenshots/test"
    screenshots = [f for f in os.listdir(test_dir) if f.endswith('.png')]
    
    print(f"🔍 Testing {len(screenshots)} screenshots...\n")
    
    results = {}
    
    for screenshot in screenshots:
        print(f"\n{'='*60}")
        print(f"📸 {screenshot}")
        print('='*60)
        
        path = os.path.join(test_dir, screenshot)
        
        try:
            result = await vision.analyze_screenshot(path)
            
            # Extract key info
            if 'raw_response' in result:
                print("📝 Raw response received")
            else:
                q_type = result.get('question_type', 'unknown')
                q_text = result.get('question_text', 'not found')[:80] + "..."
                confidence = result.get('confidence_rating', 0)
                
                print(f"✅ Type: {q_type}")
                print(f"📝 Text: {q_text}")
                print(f"🎯 Confidence: {confidence}%")
                
                results[screenshot] = {
                    'type': q_type,
                    'confidence': confidence
                }
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Summary
    print(f"\n\n📊 SUMMARY")
    print("="*60)
    for name, data in results.items():
        print(f"{name}: {data['type']} ({data['confidence']}%)")

if __name__ == "__main__":
    asyncio.run(test_all())