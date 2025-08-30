# Create a test file: test_engine.py
from core.consciousness_engine_production import ConsciousnessEngine
import asyncio

async def test():
    engine = ConsciousnessEngine(consciousness_path="core/matt_consciousness_v3.json")
    result = await engine.analyze_screenshot("surveys/live_20250829_221143_q2.png")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")

asyncio.run(test())