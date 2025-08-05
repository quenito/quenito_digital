# confidence_monitor.py
"""
Real-time confidence monitoring to see when Quenito will automate
Shows progress towards automation thresholds
"""

import json
from typing import Dict, List
from datetime import datetime
from data.knowledge_base import KnowledgeBase
from data.confidence_manager import ConfidenceManager

class ConfidenceMonitor:
    """Monitor confidence levels and predict automation readiness"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.cm = ConfidenceManager(self.kb.data.get('confidence_system', {}))
        
    def show_automation_readiness(self):
        """Display current automation readiness for all handlers"""
        
        print("\n🎯 QUENITO AUTOMATION READINESS DASHBOARD")
        print("="*60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Get all handlers
        handlers = self.cm.handler_thresholds
        
        for handler_name, config in handlers.items():
            print(f"\n📊 {handler_name.upper()} HANDLER")
            print("-"*40)
            
            base = config.get('base_threshold', 0.5)
            adjustment = config.get('dynamic_adjustment', 0.0)
            current = base + adjustment
            success_rate = config.get('success_rate', 0.0)
            
            # Visual progress bar
            progress = int(success_rate * 20)
            bar = "█" * progress + "░" * (20 - progress)
            
            print(f"  Success Rate: [{bar}] {success_rate:.1%}")
            print(f"  Threshold:    {current:.3f} (base: {base:.3f}, adj: {adjustment:+.3f})")
            print(f"  Trending:     {config.get('trending', 'unknown')}")
            
            # Check recent learning entries
            recent_questions = self._get_recent_questions(handler_name)
            if recent_questions:
                print(f"\n  Recent Questions:")
                for q in recent_questions[-3:]:  # Last 3
                    conf = q['confidence_score']
                    threshold = self.cm.get_dynamic_threshold(handler_name, q['question_type'])
                    ready = "🟢 READY!" if conf >= threshold else f"🟡 {(conf/threshold)*100:.0f}%"
                    print(f"    • {q['question_type']}: {conf:.3f} {ready}")
    
    def _get_recent_questions(self, handler_name: str) -> List[Dict]:
        """Get recent questions for a handler"""
        questions = []
        
        # Check detailed intervention learning
        if 'detailed_intervention_learning' in self.kb.data:
            for key, entry in self.kb.data['detailed_intervention_learning'].items():
                if self._get_handler_for_question(entry.get('question_type', '')) == handler_name:
                    questions.append(entry)
        
        # Sort by timestamp
        questions.sort(key=lambda x: x.get('timestamp', 0))
        return questions
    
    def _get_handler_for_question(self, question_type: str) -> str:
        """Map question type to handler"""
        mapping = {
            'age': 'demographics',
            'gender': 'demographics',
            'income': 'demographics',
            'postcode': 'demographics',
            'occupation': 'demographics',
            'rating_scale': 'rating_matrix',
            'brand_awareness': 'brand_familiarity',
            'brand_familiarity': 'brand_familiarity',
            'multi_select': 'multi_select'
        }
        return mapping.get(question_type, 'general')
    
    def predict_automation_timeline(self):
        """Predict when each handler might be ready for automation"""
        
        print("\n🔮 AUTOMATION PREDICTIONS")
        print("="*60)
        
        for handler_name, config in self.cm.handler_thresholds.items():
            current_adjustment = config.get('dynamic_adjustment', 0.0)
            success_rate = config.get('success_rate', 0.0)
            
            # Calculate how many more successes needed
            if success_rate > 0.8:
                print(f"\n✅ {handler_name}: Ready for automation!")
            else:
                # Estimate based on current trend
                learning_rate = 0.1
                success_boost = 0.05
                adjustment_per_success = -success_boost * learning_rate
                
                # How much adjustment needed to be confident
                needed_adjustment = -0.1 - current_adjustment
                successes_needed = int(abs(needed_adjustment / adjustment_per_success))
                
                print(f"\n📈 {handler_name}:")
                print(f"   Current: {current_adjustment:+.3f}")
                print(f"   Estimated successes needed: ~{successes_needed}")
                print(f"   At current rate: ~{successes_needed} more surveys")

# Enhanced learning capture with automation attempt
async def capture_with_automation_check(learner, page, question_num):
    """Capture that checks if automation should be attempted"""
    
    # First, analyze the question
    question_data = await learner._extract_comprehensive_details(page)
    handler_name = learner._get_handler_name(question_data['question_type'])
    
    # Get confidence for this exact question
    confidence = learner.cm.get_dynamic_threshold(
        handler_name, 
        question_data['question_type']
    )
    
    # Check if we should attempt automation
    should_automate, reason = learner.cm.should_attempt_automation(
        handler_name,
        confidence,
        question_data['question_type']
    )
    
    print(f"\n🤖 AUTOMATION CHECK:")
    print(f"   Handler: {handler_name}")
    print(f"   Question Type: {question_data['question_type']}")
    print(f"   Confidence: {confidence:.3f}")
    print(f"   Should Automate: {'YES! 🎉' if should_automate else 'Not yet'}")
    print(f"   Reason: {reason}")
    
    if should_automate:
        print("\n🚀 ATTEMPTING AUTOMATION...")
        # Here you would call the actual automation logic
        # For now, we'll still do manual but track it differently
        print("⚠️ Automation logic not yet implemented - continuing manually")
    
    # Continue with normal capture
    return await learner.capture_and_learn(page, question_num)

# Quick status check function
def check_automation_status():
    """Quick check of automation readiness"""
    monitor = ConfidenceMonitor()
    monitor.show_automation_readiness()
    monitor.predict_automation_timeline()

if __name__ == "__main__":
    check_automation_status()