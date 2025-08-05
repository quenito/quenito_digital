# test_simple_automation.py
"""
Minimal test to verify automation works
"""

import asyncio
from data.knowledge_base import KnowledgeBase
from data.confidence_manager import ConfidenceManager
from handler_adapter import create_simple_handlers

async def test_automation():
    """Test basic automation logic without browser"""
    
    print("🧪 TESTING AUTOMATION LOGIC")
    print("="*50)
    
    # Initialize systems
    kb = KnowledgeBase()
    cm = ConfidenceManager(kb.data.get('confidence_system', {}))
    handlers = create_simple_handlers(kb)
    
    # Test questions
    test_questions = [
        ("How old are you?", "age", "demographics"),
        ("What is your postcode?", "postcode", "demographics"),
        ("Select your gender", "gender", "demographics"),
        ("Which brands do you know?", "brand_awareness", "brand_familiarity")
    ]
    
    for question_text, question_type, handler_name in test_questions:
        print(f"\n❓ Question: {question_text}")
        
        handler = handlers.get(handler_name)
        if handler:
            # Calculate confidence
            confidence = handler.calculate_confidence(question_type, question_text)
            threshold = cm.get_dynamic_threshold(handler_name, question_type)
            should_automate, reason = cm.should_attempt_automation(
                handler_name, confidence, question_type
            )
            
            print(f"   Handler: {handler_name}")
            print(f"   Confidence: {confidence:.3f} vs Threshold: {threshold:.3f}")
            print(f"   Should Automate: {'✅ YES' if should_automate else '❌ NO'}")
            print(f"   Reason: {reason}")
            
            if should_automate:
                response = handler.handle(question_text)
                if response:
                    print(f"   🎯 Would respond with: {response.response_value}")
                else:
                    print(f"   ⚠️ No response available")
    
    print("\n✅ Automation logic test complete!")

if __name__ == "__main__":
    asyncio.run(test_automation())