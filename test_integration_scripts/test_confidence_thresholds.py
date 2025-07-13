#!/usr/bin/env python3
"""Test that confidence thresholds are working"""

def test_thresholds():
    try:
        from handlers.handler_factory import HandlerFactory
        from utils.knowledge_base import KnowledgeBase
        from survey_automation.utils.intervention_manager import EnhancedLearningInterventionManager
        
        kb = KnowledgeBase()
        intervention = EnhancedLearningInterventionManager()
        factory = HandlerFactory(kb, intervention)
        
        print("✅ Handler Factory created successfully!")
        print(f"✅ Confidence thresholds: {factory.confidence_thresholds}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_thresholds()