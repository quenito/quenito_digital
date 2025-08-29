# Test both questions
import asyncio
from consciousness_engine_production import ConsciousnessEngine

async def test_milieu_questions():
    engine = ConsciousnessEngine()
    
    # Test values question (where it already works)
    print("Testing VALUES question:")
    result1 = await engine.test_screenshot_flow("screenshots/milieu_values.png")
    print(f"Selected {len(result1['llm_answer']) if isinstance(result1['llm_answer'], list) else 1} values")
    
    # Test friend description (should now select up to 6)
    print("\nTesting FRIEND DESCRIPTION question:")
    result2 = await engine.test_screenshot_flow("screenshots/milieu_friend.png")
    print(f"Selected {len(result2['llm_answer']) if isinstance(result2['llm_answer'], list) else 1} traits")
    if isinstance(result2['llm_answer'], list):
        print(f"Traits: {', '.join(result2['llm_answer'])}")

asyncio.run(test_milieu_questions())