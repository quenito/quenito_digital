#!/usr/bin/env python3
"""
Demographics Handler Debug Test - Updated for Latest Handler
Let's see exactly what happens when the handler encounters your survey questions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.knowledge_base import KnowledgeBase
from handlers.demographics_handler_brain import DemographicsHandler
from utils.intervention_manager import EnhancedLearningInterventionManager


def test_demographics_handler():
    """Test the demographics handler with your actual survey content."""
    
    print("🔍 DEMOGRAPHICS HANDLER DEBUG TEST")
    print("=" * 50)
    
    # Initialize components
    brain = KnowledgeBase()
    intervention_manager = EnhancedLearningInterventionManager()
    handler = DemographicsHandler(None, brain, intervention_manager)
    
    print("✅ Components initialized")
    
    # Test the exact content from your SurveyMonkey survey
    test_content = "How old are you?"
    
    print(f"\n🧪 TESTING: '{test_content}'")
    print("-" * 30)
    
    try:
        # Test confidence calculation
        print("🔍 Testing can_handle() method...")
        confidence = handler.can_handle(test_content)
        print(f"📊 Confidence Score: {confidence:.3f}")
        
        if confidence > 0.4:
            print("✅ WOULD AUTOMATE (confidence > 0.4)")
        else:
            print("❌ WOULD NOT AUTOMATE (confidence ≤ 0.4)")
            print("💡 Need to investigate why confidence is low")
        
        # Test brain connection
        print(f"\n🧠 TESTING BRAIN CONNECTION")
        print("-" * 30)
        
        demographics = brain.get_demographics()
        print("📋 Demographics from brain:")
        if demographics:
            for key, value in demographics.items():
                print(f"   • {key}: {value}")
            print("✅ Knowledge base connection working")
            
            # Specifically check age
            age_value = demographics.get('age', 'NOT FOUND')
            print(f"🎯 Age value: '{age_value}'")
        else:
            print("❌ No demographics found in knowledge base")
            print("💡 This is likely the problem!")
        
        # Test question type identification
        print(f"\n🔍 TESTING QUESTION TYPE IDENTIFICATION")
        print("-" * 40)
        
        question_type = handler._identify_question_type(test_content)
        print(f"📊 Identified question type: {question_type}")
        
        if question_type == 'age':
            print("✅ Correctly identified as age question")
        else:
            print("❌ Failed to identify as age question")
            print("💡 Check keyword patterns")
        
        # Test keyword detection
        print(f"\n🔍 TESTING KEYWORD DETECTION")
        print("-" * 30)
        
        content_lower = test_content.lower()
        age_keywords = handler.question_patterns['age']['keywords']
        
        found_keywords = [kw for kw in age_keywords if kw in content_lower]
        print(f"🔍 Age keywords found: {found_keywords}")
        
        if found_keywords:
            print("✅ Keywords detected correctly")
        else:
            print("❌ No keywords detected")
            print("💡 Check keyword list")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


def test_handler_factory_threshold():
    """Test what threshold the HandlerFactory is using."""
    
    print(f"\n⚙️ TESTING HANDLER FACTORY THRESHOLD")
    print("=" * 40)
    
    try:
        brain = KnowledgeBase()
        intervention_manager = EnhancedLearningInterventionManager()
        
        from handlers.handler_factory import HandlerFactory
        factory = HandlerFactory(brain, intervention_manager)
        
        threshold = factory.confidence_thresholds.get('demographics', 'NOT FOUND')
        print(f"📊 Demographics threshold: {threshold}")
        
        if threshold == 'NOT FOUND':
            print("❌ Threshold not found in HandlerFactory")
        elif threshold > 0.5:
            print(f"⚠️ Threshold might be too high: {threshold}")
            print("💡 Consider lowering to 0.4 for testing")
        else:
            print(f"✅ Threshold looks reasonable: {threshold}")
            
    except Exception as e:
        print(f"❌ Error checking threshold: {e}")


def test_comprehensive():
    """Test all three survey questions."""
    
    print(f"\n🧪 COMPREHENSIVE TEST - ALL 3 QUESTIONS")
    print("=" * 45)
    
    brain = KnowledgeBase()
    intervention_manager = EnhancedLearningInterventionManager()
    handler = DemographicsHandler(None, brain, intervention_manager)
    
    questions = [
        "How old are you?",
        "What is your gender? Male Female Other",
        "What is your occupation?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 20)
        
        try:
            confidence = handler.can_handle(question)
            question_type = handler._identify_question_type(question)
            
            print(f"   Confidence: {confidence:.3f}")
            print(f"   Type: {question_type}")
            print(f"   Result: {'✅ AUTOMATE' if confidence > 0.4 else '❌ MANUAL'}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    try:
        test_demographics_handler()
        test_handler_factory_threshold()
        test_comprehensive()
        
        print(f"\n🎯 SUMMARY & NEXT STEPS")
        print("=" * 30)
        print("If any tests failed:")
        print("1. Check knowledge base data loading")
        print("2. Lower HandlerFactory threshold if needed")
        print("3. Verify keyword detection")
        print("4. Test page element detection")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
