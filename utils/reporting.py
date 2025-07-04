"""
Reporting Module
Generates comprehensive reports for survey automation sessions.
"""

import os
import time
from typing import Dict, Any, List, Optional


class ReportGenerator:
    """
    Generates detailed reports for survey automation sessions with analytics.
    """
    
    def __init__(self):
        self.session_start_time = None
        self.session_end_time = None
    
    def start_session(self):
        """Mark the start of a survey session."""
        self.session_start_time = time.time()
    
    def end_session(self):
        """Mark the end of a survey session."""
        self.session_end_time = time.time()
    
    def generate_survey_report(self, survey_stats: Dict[str, Any], 
                             session_stats: Dict[str, Any],
                             handler_stats: Dict[str, Any],
                             intervention_stats: Dict[str, Any],
                             research_stats: Dict[str, Any]) -> str:
        """
        Generate comprehensive survey completion report.
        
        Args:
            survey_stats: Survey completion statistics
            session_stats: Browser session statistics  
            handler_stats: Handler usage statistics
            intervention_stats: Manual intervention statistics
            research_stats: Research operation statistics
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append("📊 ENHANCED SURVEY AUTOMATION REPORT")
        report.append("=" * 80)
        
        # Session timing summary
        if session_stats.get("session_mode") == "persistent":
            report.extend(self._generate_session_timing_section(session_stats))
        
        # Survey completion summary
        report.extend(self._generate_survey_summary_section(survey_stats))
        
        # Handler usage analysis
        report.extend(self._generate_handler_analysis_section(handler_stats))
        
        # Manual intervention analysis
        report.extend(self._generate_intervention_section(intervention_stats))
        
        # Research operations summary
        report.extend(self._generate_research_section(research_stats))
        
        # Performance metrics
        report.extend(self._generate_performance_section(survey_stats, intervention_stats))
        
        # Improvement recommendations
        report.extend(self._generate_recommendations_section(
            survey_stats, handler_stats, intervention_stats
        ))
        
        report.append("=" * 80)
        return "\n".join(report)
    
    def _generate_session_timing_section(self, session_stats: Dict[str, Any]) -> List[str]:
        """Generate session timing section."""
        section = []
        
        if session_stats.get("start_time") and session_stats.get("manual_navigation_time"):
            total_time = time.time() - session_stats["start_time"]
            manual_time = (session_stats["manual_navigation_time"] - 
                          session_stats["start_time"])
            auto_time = 0
            if session_stats.get("automation_start_time"):
                auto_time = time.time() - session_stats["automation_start_time"]
            
            section.extend([
                "⏱️ SESSION TIMING:",
                f"   • Total Session Time: {total_time/60:.1f} minutes",
                f"   • Manual Navigation: {manual_time/60:.1f} minutes",
                f"   • Automation Time: {auto_time/60:.1f} minutes",
                ""
            ])
        
        section.extend([
            "🌐 SESSION DETAILS:",
            f"   • Dashboard URL: {session_stats.get('dashboard_url', 'N/A')}",
            f"   • Survey URL: {session_stats.get('survey_url', 'N/A')}",
            f"   • Session Transfers: {session_stats.get('session_transfers', 0)}",
            f"   • Session Mode: {session_stats.get('session_mode', 'Unknown').title()}",
            ""
        ])
        
        return section
    
    def _generate_survey_summary_section(self, survey_stats: Dict[str, Any]) -> List[str]:
        """Generate survey completion summary."""
        # Calculate totals safely
        total_questions = survey_stats.get("total_questions", 0)
        automated_questions = survey_stats.get("automated_questions", 0)
        manual_interventions = survey_stats.get("manual_interventions", 0)
        research_performed = survey_stats.get("research_performed", 0)
        
        # Calculate automation rate
        automation_rate = 0
        if total_questions > 0:
            automation_rate = (automated_questions / total_questions) * 100
        
        # Calculate timing
        total_time = 0
        if survey_stats.get("start_time") and survey_stats.get("end_time"):
            total_time = survey_stats["end_time"] - survey_stats["start_time"]
        
        section = [
            "📈 SUMMARY STATISTICS:",
            f"   • Total Questions Processed: {total_questions}",
            f"   • Automated Successfully: {automated_questions}",
            f"   • Manual Interventions: {manual_interventions}",
            f"   • Automation Rate: {automation_rate:.1f}%",
            f"   • Research Operations: {research_performed}",
            f"   • Total Time: {total_time/60:.1f} minutes",
            ""
        ]
        
        return section
    
    def _generate_handler_analysis_section(self, handler_stats: Dict[str, Any]) -> List[str]:
        """Generate handler usage analysis."""
        section = ["🔧 HANDLER USAGE ANALYSIS:"]
        
        handler_usage = handler_stats.get("handler_usage", {})
        total_selections = handler_stats.get("total_selections", 0)
        
        if handler_usage and total_selections > 0:
            section.append("   Handler usage breakdown:")
            
            # Sort handlers by usage count
            sorted_handlers = sorted(handler_usage.items(), key=lambda x: x[1], reverse=True)
            
            for handler_name, count in sorted_handlers:
                percentage = (count / total_selections) * 100
                section.append(f"   • {handler_name}: {count} times ({percentage:.1f}%)")
            
            # Average confidence
            confidence_scores = handler_stats.get("confidence_scores", [])
            if confidence_scores:
                avg_confidence = sum(confidence_scores) / len(confidence_scores)
                section.append(f"   • Average Confidence: {avg_confidence:.2f}")
        else:
            section.append("   No handler usage data available")
        
        section.append("")
        return section
    
    def _generate_intervention_section(self, intervention_stats: Dict[str, Any]) -> List[str]:
        """Generate manual intervention analysis."""
        section = ["🚫 MANUAL INTERVENTION ANALYSIS:"]
        
        total_interventions = intervention_stats.get("total_interventions", 0)
        
        if total_interventions == 0:
            section.extend([
                "   🎉 NO MANUAL INTERVENTIONS REQUIRED!",
                "   ✅ Perfect automation achieved",
                ""
            ])
            return section
        
        # Intervention breakdown
        intervention_types = intervention_stats.get("intervention_types", {})
        if intervention_types:
            section.append("   Interventions by type:")
            for intervention_type, count in sorted(intervention_types.items(), 
                                                 key=lambda x: x[1], reverse=True):
                percentage = (count / total_interventions) * 100
                section.append(f"   • {intervention_type}: {count} times ({percentage:.1f}%)")
        
        # Average intervention time
        total_manual_time = intervention_stats.get("total_manual_time", 0)
        if total_manual_time > 0:
            avg_time = total_manual_time / total_interventions
            section.append(f"   • Average intervention time: {avg_time:.1f} seconds")
        
        section.append("")
        return section
    
    def _generate_research_section(self, research_stats: Dict[str, Any]) -> List[str]:
        """Generate research operations summary."""
        section = ["🔍 RESEARCH OPERATIONS:"]
        
        total_searches = research_stats.get("total_searches", 0)
        
        if total_searches == 0:
            section.extend([
                "   No research operations performed",
                ""
            ])
            return section
        
        cache_hits = research_stats.get("cache_hits", 0)
        cache_misses = research_stats.get("cache_misses", 0)
        failed_searches = research_stats.get("failed_searches", 0)
        
        # Calculate rates
        cache_hit_rate = 0
        success_rate = 0
        
        total_attempts = cache_hits + cache_misses
        if total_attempts > 0:
            cache_hit_rate = (cache_hits / total_attempts) * 100
        
        if total_searches > 0:
            successful_searches = total_searches - failed_searches
            success_rate = (successful_searches / total_searches) * 100
        
        section.extend([
            f"   • Total searches: {total_searches}",
            f"   • Cache hit rate: {cache_hit_rate:.1f}%",
            f"   • Success rate: {success_rate:.1f}%",
            f"   • Failed searches: {failed_searches}",
            ""
        ])
        
        return section
    
    def _generate_performance_section(self, survey_stats: Dict[str, Any], 
                                    intervention_stats: Dict[str, Any]) -> List[str]:
        """Generate performance metrics section."""
        section = ["⚡ PERFORMANCE METRICS:"]
        
        # Questions per minute
        total_questions = survey_stats.get("total_questions", 0)
        total_time = 0
        if survey_stats.get("start_time") and survey_stats.get("end_time"):
            total_time = survey_stats["end_time"] - survey_stats["start_time"]
        
        if total_time > 0 and total_questions > 0:
            questions_per_minute = (total_questions / total_time) * 60
            section.append(f"   • Questions per minute: {questions_per_minute:.1f}")
        
        # Efficiency score
        automated_questions = survey_stats.get("automated_questions", 0)
        if total_questions > 0:
            efficiency = (automated_questions / total_questions) * 100
            section.append(f"   • Automation efficiency: {efficiency:.1f}%")
        
        # Manual intervention impact
        total_interventions = intervention_stats.get("total_interventions", 0)
        if total_interventions > 0 and total_questions > 0:
            intervention_rate = (total_interventions / total_questions) * 100
            section.append(f"   • Intervention rate: {intervention_rate:.1f}%")
        
        section.append("")
        return section
    
    def _generate_recommendations_section(self, survey_stats: Dict[str, Any],
                                        handler_stats: Dict[str, Any],
                                        intervention_stats: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations."""
        section = ["💡 IMPROVEMENT RECOMMENDATIONS:"]
        
        recommendations = []
        
        # Automation rate recommendations
        total_questions = survey_stats.get("total_questions", 0)
        automated_questions = survey_stats.get("automated_questions", 0)
        
        if total_questions > 0:
            automation_rate = (automated_questions / total_questions) * 100
            
            if automation_rate < 70:
                recommendations.append("Priority: Improve handler confidence scoring")
                recommendations.append("Add more question patterns to knowledge base")
            elif automation_rate < 85:
                recommendations.append("Enhance existing handlers with better selectors")
                recommendations.append("Update question detection keywords")
            elif automation_rate < 95:
                recommendations.append("Fine-tune handler selection algorithms")
                recommendations.append("Add edge case handling")
            else:
                recommendations.append("Excellent automation rate achieved!")
        
        # Handler-specific recommendations
        handler_usage = handler_stats.get("handler_usage", {})
        if "Unknown" in handler_usage:
            unknown_count = handler_usage["Unknown"]
            if unknown_count > 2:
                recommendations.append("High unknown handler usage - create specific handlers")
        
        # Intervention-specific recommendations
        intervention_types = intervention_stats.get("intervention_types", {})
        for intervention_type, count in intervention_types.items():
            if count > 3:
                recommendations.append(f"Focus on improving {intervention_type} handler")
        
        # Add recommendations to section
        if recommendations:
            for rec in recommendations:
                section.append(f"   • {rec}")
        else:
            section.append("   • System is performing optimally!")
        
        section.append("")
        return section
    
    def generate_quick_summary(self, survey_stats: Dict[str, Any]) -> str:
        """Generate a quick one-line summary."""
        total_questions = survey_stats.get("total_questions", 0)
        automated_questions = survey_stats.get("automated_questions", 0)
        manual_interventions = survey_stats.get("manual_interventions", 0)
        
        automation_rate = 0
        if total_questions > 0:
            automation_rate = (automated_questions / total_questions) * 100
        
        return (f"📊 Survey completed: {total_questions} questions, "
                f"{automation_rate:.1f}% automated, {manual_interventions} manual interventions")
    
    def export_report(self, report_content: str, filepath: str) -> bool:
        """Export report to file with automatic directory creation."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📤 Report exported to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
            return False

    def get_report_filepath(self, filename: str = None) -> str:
        """
        Generate report filepath in the reporting directory.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            str: Full filepath for the report
        """
        import time
        
        # Create reporting directory path
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reporting_dir = os.path.join(script_dir, "reporting")
        
        # Generate filename if not provided
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"survey_report_{timestamp}.txt"
        
        return os.path.join(reporting_dir, filename)