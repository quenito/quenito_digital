#!/usr/bin/env python3
"""
Enhanced Learning System Integration Script
Integrates the new learning components with your existing survey automation system.
"""

import os
import sys
import shutil
from pathlib import Path


def integrate_enhanced_learning_system():
    """
    Step-by-step integration of enhanced learning components.
    """
    print("🚀 Enhanced Learning System Integration")
    print("=" * 50)
    
    # Step 1: Create enhanced intervention manager
    print("\n📁 Step 1: Creating enhanced intervention manager...")
    
    enhanced_intervention_code = '''# Save the Enhanced Learning Intervention Manager code to:
# utils/enhanced_intervention_manager.py
    
# Then update your main.py to use it like this:

# At the top of main.py, replace the import:
from utils.enhanced_intervention_manager import EnhancedLearningInterventionManager

# In the EnhancedSurveyAutomationTool.__init__ method, replace:
self.intervention_manager = EnhancedLearningInterventionManager()

# In the _handle_manual_intervention method, replace:
def _handle_manual_intervention(self, question_type, page_content, reason):
    """Enhanced manual intervention with comprehensive learning."""
    
    # Use the enhanced flow
    result = self.intervention_manager.enhanced_manual_intervention_flow(
        question_type=question_type,
        reason=reason,
        page_content=page_content,
        page=self.browser_manager.page
    )
    
    if result == "SURVEY_COMPLETE":
        self._survey_completed = True
        return False
    
    return True
'''
    
    print(enhanced_intervention_code)
    
    # Step 2: Create human timing manager
    print("\n📁 Step 2: Creating human timing manager...")
    
    timing_integration_code = '''# Save the Human-Like Timing Manager code to:
# utils/human_timing_manager.py

# Then update your handlers to use it like this:

# In handlers/base_handler.py, add at the top:
from utils.human_timing_manager import HumanLikeTimingManager

# In BaseQuestionHandler.__init__, add:
self.timing_manager = HumanLikeTimingManager()

# Replace all human_like_delay calls with:
def human_like_delay(self, min_ms=None, max_ms=None, action_type="general", question_content=""):
    """Enhanced human-like delay with realistic timing patterns."""
    if self.timing_manager:
        # Use enhanced timing
        self.timing_manager.apply_human_delay(
            action_type=action_type,
            question_content=question_content
        )
    else:
        # Fallback to original method
        import random, time
        delay = random.randint(min_ms or 1500, max_ms or 4000) / 1000
        time.sleep(delay)
'''
    
    print(timing_integration_code)
    
    # Step 3: Update confidence thresholds
    print("\n📁 Step 3: Updating confidence thresholds...")
    
    confidence_update_code = '''# Update handlers/handler_factory.py:

# In HandlerFactory.__init__, add the ultra-conservative thresholds:
self.confidence_thresholds = {
    "demographics": 0.98,        # 98% - highest confidence needed
    "brand_familiarity": 0.98,   # 98% - matrix questions need precision
    "rating_matrix": 0.99,       # 99% - complex interactions
    "multi_select": 0.97,        # 97% - multiple selections
    "trust_rating": 0.96,        # 96% - scaling questions
    "research_required": 0.95,   # 95% - research complexity
    "unknown": 0.99              # 99% - unknown patterns
}

# In get_best_handler method, update the threshold check:
if handler_confidences and handler_confidences[0][2] > self.confidence_thresholds.get(handler_name, 0.95):
    # Use the handler
else:
    # Fall back to manual intervention
'''
    
    print(confidence_update_code)
    
    # Step 4: Create learning data directory
    print("\n📁 Step 4: Creating learning data directory...")
    
    try:
        os.makedirs("learning_data", exist_ok=True)
        print("✅ Created learning_data directory")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
    
    # Step 5: Test integration
    print("\n📁 Step 5: Testing integration...")
    
    test_script = '''# Create test_enhanced_learning.py to test the new system:

#!/usr/bin/env python3
"""Test Enhanced Learning System"""

def test_enhanced_intervention_manager():
    """Test the enhanced intervention manager"""
    try:
        from utils.enhanced_intervention_manager import EnhancedLearningInterventionManager
        
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
        print("\\n🎉 All enhanced learning components working!")
        print("✅ Ready for Week 1 implementation")
    else:
        print("\\n❌ Some components need fixes")
'''
    
    with open("test_enhanced_learning.py", "w") as f:
        f.write(test_script)
    
    print("✅ Created test_enhanced_learning.py")
    
    # Step 6: Integration summary
    print("\n📋 INTEGRATION SUMMARY")
    print("=" * 30)
    print("📁 Files to create:")
    print("   • utils/enhanced_intervention_manager.py")
    print("   • utils/human_timing_manager.py")
    print("   • test_enhanced_learning.py")
    print("   • learning_data/ directory")
    print()
    print("🔧 Files to update:")
    print("   • main.py (import and use enhanced intervention manager)")
    print("   • handlers/base_handler.py (add timing manager)")
    print("   • handlers/handler_factory.py (update confidence thresholds)")
    print()
    print("🧪 Testing:")
    print("   • Run: python test_enhanced_learning.py")
    print("   • Test with a real MyOpinions social survey")
    print()
    print("📊 Expected Results:")
    print("   • 98-99% confidence thresholds active")
    print("   • Comprehensive learning data capture")
    print("   • Human-like timing patterns")
    print("   • 100% survey completion maintained")


def create_week1_implementation_checklist():
    """Create implementation checklist for Week 1."""
    
    checklist = '''# 📋 Week 1 Implementation Checklist

## Day 1-2: Enhanced Intervention Manager Setup
- [ ] Create utils/enhanced_intervention_manager.py
- [ ] Update main.py imports and initialization
- [ ] Update _handle_manual_intervention method
- [ ] Test basic functionality
- [ ] Verify learning_data directory creation

## Day 3: Confidence Threshold Implementation  
- [ ] Update handlers/handler_factory.py with 98-99% thresholds
- [ ] Test threshold enforcement
- [ ] Verify manual intervention triggers correctly
- [ ] Test with known working handlers (demographics)

## Day 4-5: Human Timing Manager Integration
- [ ] Create utils/human_timing_manager.py
- [ ] Update handlers/base_handler.py
- [ ] Replace human_like_delay calls
- [ ] Test timing patterns
- [ ] Verify realistic behavior

## Day 6-7: First Social Topics Test
- [ ] Run complete test with MyOpinions social survey
- [ ] Verify comprehensive data capture
- [ ] Check learning session report generation
- [ ] Confirm 100% survey completion
- [ ] Review captured learning data

## Week 1 Success Criteria:
✅ Enhanced Intervention Manager capturing comprehensive data
✅ Human-like timing integration working seamlessly  
✅ 98-99% confidence thresholds enforced
✅ 100% survey completion maintained
✅ First social topics learning data collected
✅ Learning session reports generated

## Troubleshooting:
- If imports fail: Check file paths and Python path
- If thresholds not working: Verify handler_factory updates
- If timing seems off: Check HumanLikeTimingManager initialization
- If learning data not saving: Check learning_data directory permissions
'''
    
    with open("week1_implementation_checklist.md", "w") as f:
        f.write(checklist)
    
    print("✅ Created week1_implementation_checklist.md")


if __name__ == "__main__":
    integrate_enhanced_learning_system()
    create_week1_implementation_checklist()
    
    print("\n🚀 READY TO START WEEK 1!")
    print("=" * 30)
    print("1. Save the Enhanced Learning components to your utils/ directory")
    print("2. Follow the integration instructions above")
    print("3. Run test_enhanced_learning.py to verify setup")
    print("4. Use week1_implementation_checklist.md to track progress")
    print("5. Test with a MyOpinions social survey!")
    print()
    print("💡 Remember: 98-99% confidence thresholds ensure 100% survey completion")
    print("📚 Every intervention will now capture comprehensive learning data!")
