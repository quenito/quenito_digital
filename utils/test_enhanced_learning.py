# Create test_enhanced_learning.py to test the new system:

#!/usr/bin/env python3
"""Test Enhanced Learning System"""

def test_enhanced_intervention_manager():
    """Test the enhanced intervention manager"""
    try:
        from survey_automation.utils.intervention_manager import EnhancedLearningInterventionManager
        
        manager = EnhancedLearningInterventionManager()
        print("✅ Enhanced Intervention Manager loads successfully")
        
        # Test confidence thresholds
        print(f"📊 Confidence thresholds: {manager.confidence_thresholds}")
        
        return True
    except Exception as e:
        print(f"❌ Enhanced Intervention Manager error: {e}")
        return False

def test_human_timing_manager():
    """Test the human timing manager"""
    try:
        from utils.human_timing_manager import HumanLikeTimingManager
        
        timing = HumanLikeTimingManager()
        print("✅ Human Timing Manager loads successfully")
        
        # Test timing calculation
        delay = timing.calculate_human_delay("demographics", "simple", 50, "What is your age?")
        print(f"⏱️ Sample timing: {delay:.1f}s for demographics question")
        
        return True
    except Exception as e:
        print(f"❌ Human Timing Manager error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Enhanced Learning System")
    print("=" * 40)
    
    success = True
    success &= test_enhanced_intervention_manager()
    success &= test_human_timing_manager()
    
    if success:
        print("\n🎉 All enhanced learning components working!")
        print("✅ Ready for Week 1 implementation")
    else:
        print("\n❌ Some components need fixes")
