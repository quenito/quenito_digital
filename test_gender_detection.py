#!/usr/bin/env python3
"""
Test gender question detection to diagnose the 0% success rate issue
"""

import asyncio
from handlers.demographics_handler_brain import DemographicsHandler
from utils.knowledge_base import KnowledgeBase

async def test_gender_detection():
    """Test gender detection confidence scoring"""
    
    print("🧪 TESTING GENDER QUESTION DETECTION")
    print("=" * 50)
    
    # Initialize components
    kb = KnowledgeBase()
    
    # Create a mock intervention manager (not needed for testing)
    class MockInterventionManager:
        def __init__(self):
            pass
    
    mock_intervention = MockInterventionManager()
    
    # Initialize handler with all required parameters
    handler = DemographicsHandler(None, kb, mock_intervention)  # No page needed for confidence testing
    
    # Test cases that might appear in surveys
    test_cases = [
        "What is your gender?",
        "Gender: Please select one",
        "Which of the following best describes your gender identity?",
        "Are you male or female?",
        "Select your gender from the options below:",
        "Gender selection: Male, Female, Other",
        "Please indicate your gender",
        "Demographics Survey - Gender Question",
    ]
    
    print("🎯 Testing gender detection confidence:")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: '{test_case}'")
        
        # Test the enhanced gender detection method
        content_lower = test_case.lower()
        
        # Check if the handler has the enhanced gender detection method
        if hasattr(handler, '_enhanced_gender_detection'):
            gender_confidence = handler._enhanced_gender_detection(content_lower)
        else:
            print("   ⚠️ Handler missing _enhanced_gender_detection method - needs implementation")
            gender_confidence = 0.0
        
        # Test overall page confidence  
        if hasattr(handler, 'get_confidence'):
            # Check if get_confidence is async
            import inspect
            if inspect.iscoroutinefunction(handler.get_confidence):
                overall_confidence = await handler.get_confidence(test_case)
            else:
                overall_confidence = handler.get_confidence(test_case)
        else:
            print("   ⚠️ Handler missing get_confidence method")
            overall_confidence = 0.0
        
        print(f"   Gender-specific confidence: {gender_confidence:.3f}")
        print(f"   Overall page confidence: {overall_confidence:.3f}")
        print(f"   Would trigger automation: {'✅ YES' if overall_confidence >= 0.4 else '❌ NO'}")
        print()
    
    print("🧠 Brain Learning Status:")
    learning_summary = kb.get_brain_learning_summary()
    print(f"   Gender success rate: {learning_summary}")
    
    print("\n🎯 RECOMMENDATION:")
    print("If all tests show low confidence, we need to:")
    print("1. Lower the confidence threshold for gender questions")
    print("2. Improve the gender detection patterns")
    print("3. Add more specific gender keywords")

if __name__ == "__main__":
    asyncio.run(test_gender_detection())