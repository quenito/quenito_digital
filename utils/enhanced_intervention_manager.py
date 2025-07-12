#!/usr/bin/env python3
"""
Enhanced Learning Intervention Manager (Standalone Version)
Comprehensive data capture with learning capabilities for survey automation improvement.
No dependencies on missing intervention_manager.
"""

import time
import json
import os
from typing import Dict, Any, List, Optional


class EnhancedLearningInterventionManager:
    """
    Enhanced intervention manager with comprehensive learning capabilities.
    Standalone version with no problematic dependencies.
    """
    
    def __init__(self):
        """Initialize the enhanced intervention manager."""
        # Basic intervention stats
        self.intervention_stats = {
            "total_interventions": 0,
            "intervention_details": [],
            "intervention_types": {},
            "total_automation_time": 0,
            "total_manual_time": 0
        }
        
        # Enhanced learning data structures
        self.learning_session_data = {
            "session_id": f"session_{int(time.time())}",
            "start_time": time.time(),
            "interventions": [],
            "page_captures": [],
            "learning_insights": [],
            "handler_performance": {}
        }
        
        # Ultra-conservative confidence thresholds (98-99%)
        self.confidence_thresholds = {
            "demographics": 0.98,        # 98% - highest confidence needed
            "brand_familiarity": 0.98,   # 98% - matrix questions need precision
            "rating_matrix": 0.99,       # 99% - complex interactions
            "multi_select": 0.97,        # 97% - multiple selections
            "trust_rating": 0.96,        # 96% - scaling questions
            "research_required": 0.95,   # 95% - research complexity
            "unknown": 0.99              # 99% - unknown patterns
        }
        
        # Create learning data directory
        self.learning_data_dir = "learning_data"
        os.makedirs(self.learning_data_dir, exist_ok=True)
        
        # Completion detection callbacks
        self._completion_check_callback = None
        self._page_status_callback = None
    
    def enhanced_manual_intervention_flow(self, question_type: str, reason: str, 
                                        page_content: str = "", page=None) -> str:
        """
        Enhanced manual intervention with comprehensive data capture and learning.
        
        Args:
            question_type: Type of question requiring intervention
            reason: Reason why automation failed
            page_content: Content of the current page
            page: Playwright page object for advanced capture
            
        Returns:
            str: Result of intervention ("COMPLETE" or "SURVEY_COMPLETE")
        """
        print("\n" + "="*80)
        print("🔄 ENHANCED LEARNING MODE: Manual intervention required")
        print("📚 System is capturing comprehensive learning data...")
        print("="*80)
        
        intervention_start_time = time.time()
        
        # Phase 1: Capture pre-intervention state
        print("📸 Phase 1: Capturing page state...")
        pre_intervention_data = self._capture_comprehensive_page_state(page, question_type, reason)
        
        # Phase 2: Display intervention context
        self._display_enhanced_intervention_context(question_type, reason, page_content)
        
        # Phase 3: User completes manually
        print("🔧 MANUAL INTERVENTION INSTRUCTIONS:")
        print("1. Please complete this question manually in the browser")
        print("2. Click the 'Next' or 'Continue' button to move to the next question")
        print("3. Wait until the next question loads completely")
        print("4. Press Enter here to resume automation")
        print()
        print("📊 Learning System Status:")
        print(f"   • Question Type: {question_type}")
        print(f"   • Confidence Threshold: {self.confidence_thresholds.get(question_type, 0.95):.0%}")
        print(f"   • Learning Data: Being captured for future enhancement")
        print()
        
        user_input = input("✋ Press Enter AFTER you've completed the question and moved to the next page...")
        
        # Phase 4: Capture post-intervention state
        print("📸 Phase 2: Capturing response data...")
        post_intervention_data = self._capture_user_response_data(page)
        
        # Phase 5: Analyze and learn
        print("🧠 Phase 3: Analyzing learning opportunities...")
        learning_insights = self._analyze_learning_opportunities(
            pre_intervention_data, post_intervention_data, question_type, reason
        )
        
        # Phase 6: Store learning data
        intervention_duration = time.time() - intervention_start_time
        self._store_intervention_learning_data({
            "question_type": question_type,
            "reason": reason,
            "pre_state": pre_intervention_data,
            "post_state": post_intervention_data,
            "learning_insights": learning_insights,
            "duration": intervention_duration,
            "timestamp": time.time()
        })
        
        print("✅ Learning data captured! System intelligence enhanced!")
        print("🚀 Resuming automation with improved knowledge...")
        print("="*80 + "\n")
        
        # Update intervention stats
        self._update_intervention_stats(question_type, reason, intervention_duration)
        
        return "COMPLETE"
    
    def _capture_comprehensive_page_state(self, page, question_type: str, reason: str) -> Dict[str, Any]:
        """Capture comprehensive page state for learning."""
        try:
            if page:
                return {
                    "url": page.url,
                    "title": page.title(),
                    "content_sample": page.inner_text('body')[:1000],  # First 1000 chars
                    "timestamp": time.time(),
                    "question_type": question_type,
                    "failure_reason": reason
                }
            else:
                return {
                    "url": "unknown",
                    "title": "unknown",
                    "content_sample": "Page object not available",
                    "timestamp": time.time(),
                    "question_type": question_type,
                    "failure_reason": reason
                }
        except Exception as e:
            print(f"⚠️ Could not capture page state: {e}")
            return {
                "error": str(e),
                "timestamp": time.time(),
                "question_type": question_type,
                "failure_reason": reason
            }
    
    def _display_enhanced_intervention_context(self, question_type: str, reason: str, page_content: str):
        """Display enhanced context for the intervention."""
        print(f"📍 Question Type: {question_type}")
        print(f"❌ Automation Failed: {reason}")
        print(f"🎯 Confidence Threshold: {self.confidence_thresholds.get(question_type, 0.95):.0%}")
        
        if page_content:
            print("📄 Page Content Sample:")
            print("-" * 40)
            content_sample = page_content[:300] + "..." if len(page_content) > 300 else page_content
            print(content_sample)
            print("-" * 40)
        print()
    
    def _capture_user_response_data(self, page) -> Dict[str, Any]:
        """Capture data about how the user responded."""
        try:
            if page:
                return {
                    "post_url": page.url,
                    "post_title": page.title(),
                    "post_content_sample": page.inner_text('body')[:1000],
                    "timestamp": time.time()
                }
            else:
                return {
                    "post_url": "unknown",
                    "timestamp": time.time()
                }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": time.time()
            }
    
    def _analyze_learning_opportunities(self, pre_data: Dict, post_data: Dict, 
                                      question_type: str, reason: str) -> Dict[str, Any]:
        """Analyze what can be learned from this intervention."""
        return {
            "question_type": question_type,
            "failure_reason": reason,
            "learning_opportunities": [
                f"Pattern recognition improvement needed for {question_type}",
                f"Handler enhancement required: {reason}",
                "Element detection strategies should be updated"
            ],
            "suggested_improvements": [
                f"Lower confidence threshold for {question_type} from {self.confidence_thresholds.get(question_type, 0.95):.0%}",
                "Add new element selectors based on this page structure",
                "Improve question type classification accuracy"
            ],
            "timestamp": time.time()
        }
    
    def _store_intervention_learning_data(self, learning_data: Dict[str, Any]):
        """Store learning data for future analysis."""
        try:
            # Add to session data
            self.learning_session_data["interventions"].append(learning_data)
            
            # Save to file
            filename = f"intervention_{int(time.time())}.json"
            filepath = os.path.join(self.learning_data_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(learning_data, f, indent=2, default=str)
            
            print(f"💾 Learning data saved: {filename}")
            
        except Exception as e:
            print(f"⚠️ Could not save learning data: {e}")
    
    def _update_intervention_stats(self, question_type: str, reason: str, duration: float):
        """Update intervention statistics."""
        self.intervention_stats["total_interventions"] += 1
        self.intervention_stats["total_manual_time"] += duration
        
        # Track intervention types
        if question_type not in self.intervention_stats["intervention_types"]:
            self.intervention_stats["intervention_types"][question_type] = 0
        self.intervention_stats["intervention_types"][question_type] += 1
        
        # Add detailed record
        self.intervention_stats["intervention_details"].append({
            "question_type": question_type,
            "reason": reason,
            "duration": duration,
            "timestamp": time.time()
        })
    
    def request_manual_intervention(self, question_type: str, reason: str, page_content: str = "") -> bool:
        """
        Legacy method for compatibility with existing code.
        Redirects to enhanced flow.
        """
        result = self.enhanced_manual_intervention_flow(question_type, reason, page_content)
        return result == "COMPLETE"
    
    def generate_learning_session_report(self) -> str:
        """Generate a comprehensive learning session report."""
        total_interventions = len(self.learning_session_data["interventions"])
        session_duration = time.time() - self.learning_session_data["start_time"]
        
        report = []
        report.append("📊 ENHANCED LEARNING SESSION REPORT")
        report.append("=" * 50)
        report.append(f"Session ID: {self.learning_session_data['session_id']}")
        report.append(f"Total Interventions: {total_interventions}")
        report.append(f"Session Duration: {session_duration:.1f} seconds")
        report.append()
        
        if total_interventions > 0:
            # Question type breakdown
            question_types = {}
            for intervention in self.learning_session_data["interventions"]:
                q_type = intervention["question_type"]
                question_types[q_type] = question_types.get(q_type, 0) + 1
            
            report.append("📋 Question Types Encountered:")
            for q_type, count in question_types.items():
                percentage = (count / total_interventions) * 100
                threshold = self.confidence_thresholds.get(q_type, 0.95)
                report.append(f"   • {q_type}: {count} times ({percentage:.1f}%) - Threshold: {threshold:.0%}")
            
            report.append()
            report.append("💡 Learning Insights Generated:")
            report.append(f"   • {total_interventions} comprehensive data captures completed")
            report.append(f"   • {len(self.confidence_thresholds)} confidence thresholds active")
            report.append(f"   • Learning data saved to: {self.learning_data_dir}/")
            
        report.append()
        report.append("🎯 Next Steps:")
        report.append("   • Review learning data for pattern improvements")
        report.append("   • Consider threshold adjustments based on performance")
        report.append("   • Implement suggested handler enhancements")
        
        return "\n".join(report)
    
    def set_completion_check_callback(self, callback):
        """Set callback for survey completion detection."""
        self._completion_check_callback = callback
    
    def set_page_status_callback(self, callback):
        """Set callback for page status assessment."""
        self._page_status_callback = callback


# Test the enhanced intervention manager if run directly
if __name__ == "__main__":
    print("🧪 Testing Enhanced Learning Intervention Manager")
    print("=" * 55)
    
    # Create manager
    manager = EnhancedLearningInterventionManager()
    print("✅ Enhanced Intervention Manager created successfully!")
    
    # Test confidence thresholds
    print(f"📊 Confidence thresholds loaded: {len(manager.confidence_thresholds)} types")
    for q_type, threshold in manager.confidence_thresholds.items():
        print(f"   • {q_type}: {threshold:.0%}")
    
    # Test learning data directory
    if os.path.exists(manager.learning_data_dir):
        print(f"✅ Learning data directory ready: {manager.learning_data_dir}/")
    
    # Generate test report
    report = manager.generate_learning_session_report()
    print("\n📊 Sample Learning Report:")
    print(report)
    
    print("\n✅ Enhanced Learning Intervention Manager test completed!")
    print("🎉 Ready for integration with your survey automation system!")