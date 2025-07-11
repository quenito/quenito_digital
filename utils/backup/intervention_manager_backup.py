"""
Intervention Manager Module
Handles manual intervention requests and logging for continuous improvement.
Enhanced with completion detection during manual intervention.
"""

import time
from typing import List, Dict, Any, Optional


class InterventionManager:
    """
    Manages manual intervention requests with comprehensive logging and analysis.
    Enhanced with survey completion detection during manual interventions.
    """
    
    def __init__(self):
        self.intervention_stats = {
            "total_interventions": 0,
            "intervention_details": [],
            "intervention_types": {},
            "total_automation_time": 0,
            "total_manual_time": 0
        }
        
        # Completion detection callbacks
        self._completion_check_callback = None
        self._page_status_callback = None
    
    def request_manual_intervention(self, question_type: str, reason: str, page_content: str = "") -> bool:
        """
        Enhanced manual intervention with completion detection.
        
        Args:
            question_type: Type of question requiring intervention
            reason: Reason why automation failed
            page_content: Content of the current page
            
        Returns:
            bool: True after user completes manual intervention, "SURVEY_COMPLETE" if survey completed
        """
        print("\n" + "="*80)
        print("🚫 AUTOMATION PAUSED - MANUAL INTERVENTION REQUIRED")
        print("="*80)
        print(f"📍 Question Type: {question_type}")
        print(f"❌ Reason: {reason}")
        print()
        
        # Record intervention start time
        intervention_start = time.time()
        
        # Log intervention details
        intervention_record = self._create_intervention_record(
            question_type, reason, page_content, intervention_start
        )
        
        # Show page content sample for context
        if page_content:
            print("📄 Page Content Sample:")
            print("-" * 40)
            content_sample = page_content[:300] + "..." if len(page_content) > 300 else page_content
            print(content_sample)
            print("-" * 40)
            print()
        
        # Provide specific guidance based on question type
        self._provide_intervention_guidance(question_type)
        
        print("🔧 MANUAL INTERVENTION INSTRUCTIONS:")
        print("1. Please complete this question manually in the browser")
        print("2. Click the 'Next' or 'Continue' button to move to the next question")
        print("3. Wait until the next question loads completely")
        print("4. Press Enter here to resume automation")
        print()
        print("💡 Your interaction will be logged for system improvement!")
        print("🎯 The system will automatically detect if the survey completes!")
        print()
        
        # Enhanced intervention loop with completion checking
        max_intervention_attempts = 10  # Prevent infinite loops
        attempt = 0
        
        while attempt < max_intervention_attempts:
            attempt += 1
            
            # Wait for user confirmation
            user_input = input("✋ Press Enter AFTER you've completed the question and moved to the next page...")
            
            # Check for survey completion after user action
            if self._check_completion_after_intervention():
                print("🎉 Survey completion detected during manual intervention!")
                
                # Record successful completion
                intervention_end = time.time()
                intervention_duration = intervention_end - intervention_start
                intervention_record["end_time"] = intervention_end
                intervention_record["duration"] = intervention_duration
                intervention_record["completion_detected"] = True
                intervention_record["suggestions"] = ["Survey completed during manual intervention"]
                
                self._update_intervention_stats(intervention_record)
                
                print("🏆 Manual intervention resulted in survey completion!")
                print("="*80 + "\n")
                
                return "SURVEY_COMPLETE"  # Special return value
            
            # Check if we're still on a survey question or moved to next page
            current_status = self._assess_current_page_status()
            
            if current_status == "COMPLETED":
                print("🎉 Survey completion confirmed!")
                break
            elif current_status == "NEXT_QUESTION":
                print("✅ Successfully moved to next question")
                break
            elif current_status == "SAME_PAGE":
                if attempt < max_intervention_attempts:
                    print(f"⚠️ Still on same page - attempt {attempt}/{max_intervention_attempts}")
                    print("Please ensure you clicked 'Next' or 'Continue' and the page loaded")
                    continue
                else:
                    print("⚠️ Maximum intervention attempts reached")
                    break
        
        # Record intervention completion
        intervention_end = time.time()
        intervention_duration = intervention_end - intervention_start
        
        intervention_record["end_time"] = intervention_end
        intervention_record["duration"] = intervention_duration
        intervention_record["completion_detected"] = False
        intervention_record["suggestions"] = self._get_improvement_suggestions(question_type, reason)
        
        # Update statistics
        self._update_intervention_stats(intervention_record)
        
        print("🚀 Resuming automation...")
        print("="*80 + "\n")
        
        return True
    
    def _check_completion_after_intervention(self):
        """
        Check for survey completion after manual intervention.
        """
        try:
            # Brief delay to allow page to load
            time.sleep(2)
            
            # Use the completion check callback if available
            if self._completion_check_callback:
                return self._completion_check_callback()
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking completion after intervention: {e}")
            return False
    
    def _assess_current_page_status(self):
        """
        Assess the current page status after manual intervention.
        """
        try:
            # Use the page status callback if available
            if self._page_status_callback:
                return self._page_status_callback()
            
            # Default assessment - assume progression
            return "NEXT_QUESTION"
            
        except Exception as e:
            print(f"⚠️ Error assessing page status: {e}")
            return "UNKNOWN"
    
    def set_completion_check_callback(self, callback):
        """
        Set the callback function for checking survey completion.
        This should be called from the main automation tool.
        """
        self._completion_check_callback = callback
    
    def set_page_status_callback(self, callback):
        """
        Set the callback function for checking page status.
        This should be called from the main automation tool.
        """
    
    def _create_intervention_record(self, question_type: str, reason: str, 
                                   page_content: str, start_time: float) -> Dict[str, Any]:
        """Create detailed intervention record for analysis."""
        return {
            "intervention_id": len(self.intervention_stats["intervention_details"]) + 1,
            "question_type": question_type,
            "reason": reason,
            "page_content_sample": page_content[:500] + "..." if len(page_content) > 500 else page_content,
            "start_time": start_time,
            "end_time": None,
            "duration": None,
            "completion_detected": False,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "suggestions": []
        }
    
    def _provide_intervention_guidance(self, question_type: str):
        """Provide specific guidance based on question type."""
        guidance_map = {
            "demographics": [
                "💡 Demographics Tip: Fill in your actual demographic information",
                "💡 For location, look for your state/region in dropdowns"
            ],
            "brand_familiarity": [
                "💡 Brand Familiarity Tip: Rate based on your actual knowledge",
                "💡 Use 'Never heard of' for unknown brands"
            ],
            "rating_matrix": [
                "💡 Rating Matrix Tip: Read each statement carefully",
                "💡 Use 'Neither agree nor disagree' when unsure"
            ],
            "multi_select": [
                "💡 Multi-Select Tip: Select all relevant options",
                "💡 Usually 3-5 selections are appropriate"
            ],
            "research_required": [
                "💡 Research Required: This question needs specific knowledge",
                "💡 It's okay to select 'Don't know' for unfamiliar topics"
            ],
            "unknown": [
                "💡 Unknown Question: This is a new pattern we haven't seen",
                "💡 Your response will help improve the automation system"
            ]
        }
        
        guidance = guidance_map.get(question_type, [
            "💡 General Tip: Answer naturally and honestly",
            "💡 Your response pattern will help improve automation"
        ])
        
        for tip in guidance:
            print(tip)
        print()
    
    def _get_improvement_suggestions(self, question_type: str, reason: str) -> List[str]:
        """Generate improvement suggestions based on intervention."""
        suggestions = []
        
        # Question-type specific suggestions
        if question_type == "demographics":
            suggestions.extend([
                "Add new demographic field detection patterns",
                "Update location mapping for new regional formats",
                "Enhance form element selector patterns"
            ])
        elif question_type == "brand_familiarity":
            suggestions.extend([
                "Add new brand familiarity response patterns", 
                "Update brand recognition database",
                "Enhance matrix navigation logic"
            ])
        elif question_type == "rating_matrix":
            suggestions.extend([
                "Add new rating scale patterns",
                "Update agreement/disagreement detection",
                "Enhance matrix row processing"
            ])
        elif question_type == "unknown":
            suggestions.extend([
                "Analyze question content for new patterns",
                "Create new handler for this question type",
                "Update question type detection keywords"
            ])
        
        # Reason-specific suggestions
        if "element not found" in reason.lower():
            suggestions.append("Update CSS selectors for this survey platform")
        elif "not recognized" in reason.lower():
            suggestions.append("Add new question pattern recognition")
        elif "complex" in reason.lower():
            suggestions.append("Break down into simpler interaction steps")
        
        # General suggestions
        suggestions.extend([
            "Update knowledge base with new patterns",
            "Enhance handler confidence scoring",
            "Add platform-specific optimizations"
        ])
        
        return suggestions
    
    def _update_intervention_stats(self, intervention_record: Dict[str, Any]):
        """Update intervention statistics."""
        self.intervention_stats["total_interventions"] += 1
        self.intervention_stats["intervention_details"].append(intervention_record)
        
        # Update intervention type counts
        question_type = intervention_record["question_type"]
        if question_type in self.intervention_stats["intervention_types"]:
            self.intervention_stats["intervention_types"][question_type] += 1
        else:
            self.intervention_stats["intervention_types"][question_type] = 1
        
        # Update timing statistics
        if intervention_record["duration"]:
            self.intervention_stats["total_manual_time"] += intervention_record["duration"]
    
    def get_intervention_stats(self) -> Dict[str, Any]:
        """Get intervention statistics."""
        return self.intervention_stats.copy()
    
    def get_intervention_details(self) -> List[Dict[str, Any]]:
        """Get detailed intervention records."""
        return self.intervention_stats["intervention_details"].copy()
    
    def get_most_common_interventions(self, limit: int = 5) -> List[tuple]:
        """Get most common intervention types."""
        intervention_types = self.intervention_stats["intervention_types"]
        sorted_types = sorted(intervention_types.items(), key=lambda x: x[1], reverse=True)
        return sorted_types[:limit]
    
    def get_average_intervention_time(self) -> float:
        """Get average time per manual intervention."""
        total_interventions = self.intervention_stats["total_interventions"]
        total_time = self.intervention_stats["total_manual_time"]
        
        if total_interventions > 0:
            return total_time / total_interventions
        return 0.0
    
    def generate_improvement_report(self) -> str:
        """Generate a report with improvement recommendations."""
        if self.intervention_stats["total_interventions"] == 0:
            return "📊 No interventions recorded - excellent automation performance!"
        
        report = []
        report.append("📊 INTERVENTION ANALYSIS REPORT")
        report.append("=" * 40)
        
        # Summary statistics
        total = self.intervention_stats["total_interventions"]
        avg_time = self.get_average_intervention_time()
        report.append(f"Total Interventions: {total}")
        report.append(f"Average Time per Intervention: {avg_time:.1f} seconds")
        report.append("")
        
        # Most common intervention types
        common_types = self.get_most_common_interventions()
        if common_types:
            report.append("🔍 Most Common Intervention Types:")
            for question_type, count in common_types:
                percentage = (count / total) * 100
                report.append(f"   • {question_type}: {count} times ({percentage:.1f}%)")
            report.append("")
        
        # Improvement suggestions
        all_suggestions = set()
        for intervention in self.intervention_stats["intervention_details"]:
            all_suggestions.update(intervention.get("suggestions", []))
        
        if all_suggestions:
            report.append("💡 IMPROVEMENT RECOMMENDATIONS:")
            for suggestion in sorted(all_suggestions):
                report.append(f"   • {suggestion}")
            report.append("")
        
        # Recent interventions analysis
        recent_interventions = self.intervention_stats["intervention_details"][-3:]
        if recent_interventions:
            report.append("🕒 Recent Interventions:")
            for intervention in recent_interventions:
                report.append(f"   • {intervention['question_type']}: {intervention['reason']}")
            report.append("")
        
        return "\n".join(report)
    
    def reset_stats(self):
        """Reset intervention statistics for a new session."""
        self.intervention_stats = {
            "total_interventions": 0,
            "intervention_details": [],
            "intervention_types": {},
            "total_automation_time": 0,
            "total_manual_time": 0
        }
        print("🔄 Intervention statistics reset")
    
    def export_intervention_data(self, filepath: str) -> bool:
        """Export intervention data to JSON file for analysis."""
        try:
            import json
            with open(filepath, 'w') as f:
                json.dump(self.intervention_stats, f, indent=2)
            print(f"📤 Intervention data exported to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error exporting intervention data: {e}")
            return False
    
    def print_intervention_summary(self):
        """Print a summary of intervention statistics."""
        stats = self.intervention_stats
        
        if stats["total_interventions"] == 0:
            print("📊 No manual interventions required - perfect automation! 🎉")
            return
        
        print(f"\n🚫 MANUAL INTERVENTION SUMMARY:")
        print(f"   Total interventions: {stats['total_interventions']}")
        print(f"   Average duration: {self.get_average_intervention_time():.1f} seconds")
        
        # Show breakdown by type
        if stats["intervention_types"]:
            print(f"\n📊 Breakdown by question type:")
            for question_type, count in sorted(stats["intervention_types"].items(), 
                                             key=lambda x: x[1], reverse=True):
                percentage = (count / stats["total_interventions"]) * 100
                print(f"   • {question_type}: {count} times ({percentage:.1f}%)")
        
        print(f"\n💡 See improvement report for enhancement suggestions")