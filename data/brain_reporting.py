#!/usr/bin/env python3
"""
Brain Reporting Module - Analytics, reporting, and intelligence insights
Extracted from knowledge_base.py for better modularity and maintainability.

This module handles:
- Intelligence report generation
- Performance analytics and metrics
- Learning progress tracking
- Automation success analysis
- Brain evolution reporting
- Cross-handler performance comparison
- Learning recommendation generation
"""

from typing import Dict, Any, Optional, List
import time
import statistics
from pathlib import Path


class BrainReporting:
    """
    Clean analytics and reporting management for Quenito's brain intelligence.
    Handles report generation, performance analysis, and intelligence insights.
    """
    
    def __init__(self, brain_learning):
        """Initialize with brain learning module for data access"""
        self.brain_learning = brain_learning
        self.report_templates = {
            'intelligence_report': 'detailed',
            'performance_summary': 'concise',
            'learning_progress': 'detailed',
            'automation_analysis': 'comprehensive'
        }
        print("🧠 BrainReporting initialized and connected to brain learning")
    
    # ========================================
    # INTELLIGENCE REPORT GENERATION
    # ========================================
    
    def generate_intelligence_report(self) -> str:
        """Generate comprehensive brain intelligence report"""
        try:
            report_sections = []
            
            # Header
            report_sections.append(self._generate_report_header())
            
            # Brain evolution analysis
            report_sections.append(self._generate_brain_evolution_section())
            
            # Handler performance analysis
            report_sections.append(self._generate_handler_performance_section())
            
            # Learning events analysis
            report_sections.append(self._generate_learning_events_section())
            
            # Confidence analysis
            report_sections.append(self._generate_confidence_analysis_section())
            
            # Recommendations
            report_sections.append(self._generate_recommendations_section())
            
            # Footer
            report_sections.append(self._generate_report_footer())
            
            return '\n'.join(report_sections)
            
        except Exception as e:
            return f"❌ Error generating intelligence report: {e}"
    
    def _generate_report_header(self) -> str:
        """Generate report header with timestamp"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"""🧠===============================================================================
🧠 QUENITO'S DIGITAL BRAIN INTELLIGENCE REPORT
🧠===============================================================================
📅 Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
🎯 Report ID: brain_report_{timestamp}
🧠==============================================================================="""
    
    def _generate_brain_evolution_section(self) -> str:
        """Generate brain evolution analysis section"""
        try:
            insights = self.brain_learning.get_learning_insights()
            stats = self.brain_learning.get_brain_statistics()
            
            evolution_section = f"""
🧠 BRAIN EVOLUTION ANALYSIS:
==================================================
📊 Intelligence Level: {insights.get('learning_maturity', 'unknown').title()}
🎯 Automation Readiness: {insights.get('automation_readiness', 0.0)*100:.1f}%
🧠 Total Interventions Learned: {insights.get('total_interventions', 0)}
🎯 Success Patterns Stored: {insights.get('success_patterns_count', 0)}
⚙️ Strategy Preferences: {insights.get('strategy_preferences_count', 0)}

📈 LEARNING PROGRESSION:
   • Intervention Learning Events: {stats.get('intervention_history', 0)}
   • Success Pattern Recognition: {stats.get('success_patterns', 0)}
   • Handler Performance Tracking: {stats.get('handler_performance_tracked', 0)}
   • Confidence Calibrations: {stats.get('confidence_calibrations', 0)}
   • Learning Sessions Completed: {stats.get('learning_sessions', 0)}"""
            
            return evolution_section
            
        except Exception as e:
            return f"⚠️ Error analyzing brain evolution: {e}"
    
    def _generate_handler_performance_section(self) -> str:
        """Generate handler performance analysis section"""
        try:
            performance_summary = self.brain_learning.get_handler_performance_summary()
            
            performance_section = f"""
🎯 HANDLER INTELLIGENCE ANALYSIS:
==================================================
📊 HANDLER PERFORMANCE MATRIX:
   • Total Handlers Tracked: {performance_summary.get('total_handlers', 0)}
   • Average Success Rate: {performance_summary['overall_metrics'].get('average_success_rate', 0.0)*100:.1f}%
   • Total Automation Attempts: {performance_summary['overall_metrics'].get('total_attempts', 0)}
   • Successful Automations: {performance_summary['overall_metrics'].get('total_successes', 0)}"""
            
            # Individual handler details
            handler_details = performance_summary.get('handler_details', {})
            if handler_details:
                performance_section += "\n\n📋 INDIVIDUAL HANDLER ANALYSIS:"
                for handler_name, stats in handler_details.items():
                    trend_icon = self._get_trend_icon(stats.get('trend', 'unknown'))
                    performance_section += f"""
   • {handler_name}:
     - Success Rate: {stats.get('success_rate', 0.0)*100:.1f}% ({stats.get('total_attempts', 0)} attempts)
     - Avg Confidence: {stats.get('average_confidence', 0.0):.2f}
     - Intelligence Trend: {stats.get('trend', 'unknown')} {trend_icon}"""
            
            # Top performing handler
            top_handler = performance_summary['overall_metrics'].get('top_performing_handler')
            if top_handler:
                performance_section += f"\n\n🏆 TOP PERFORMING HANDLER:\n   • {top_handler}: Best success rate with strong brain integration"
            
            # Handlers needing improvement
            needs_improvement = performance_summary['overall_metrics'].get('needs_improvement', [])
            if needs_improvement:
                performance_section += f"\n\n⚠️ HANDLERS NEEDING BRAIN ENHANCEMENT:\n   • " + "\n   • ".join(needs_improvement)
            
            return performance_section
            
        except Exception as e:
            return f"⚠️ Error analyzing handler performance: {e}"
    
    def _get_trend_icon(self, trend: str) -> str:
        """Get emoji icon for trend"""
        trend_icons = {
            'improving': '📈',
            'declining': '📉', 
            'stable': '➡️',
            'insufficient_data': '❓',
            'new': '🆕',
            'unknown': '❓'
        }
        return trend_icons.get(trend, '❓')
    
    def _generate_learning_events_section(self) -> str:
        """Generate learning events analysis section"""
        try:
            current_session = self.brain_learning.current_session
            
            learning_section = f"""
📚 LEARNING EVENTS & PATTERN DISCOVERIES:
==================================================
📊 CURRENT SESSION ANALYSIS:
   • Session ID: {current_session.get('session_id', 'unknown')}
   • Learning Events: {len(current_session.get('learning_events', []))}
   • Performance Improvements: {len(current_session.get('performance_improvements', []))}
   • New Patterns Discovered: {len(current_session.get('new_patterns_discovered', []))}"""
            
            # Recent learning events
            learning_events = current_session.get('learning_events', [])
            if learning_events:
                learning_section += "\n\n🔍 RECENT LEARNING EVENTS:"
                for i, event in enumerate(learning_events[-3:], 1):  # Last 3 events
                    event_data = event.get('data', {})
                    timestamp = time.strftime("%H:%M:%S", time.localtime(event.get('timestamp', time.time())))
                    learning_section += f"""
   {i}. {timestamp}: {event_data.get('question_type', 'unknown')} - {event.get('type', 'unknown')}"""
            
            return learning_section
            
        except Exception as e:
            return f"⚠️ Error analyzing learning events: {e}"
    
    def _generate_confidence_analysis_section(self) -> str:
        """Generate confidence analysis section"""
        try:
            brain_data = self.brain_learning.brain_data
            confidence_calibration = brain_data.get('confidence_calibration', {})
            
            confidence_section = f"""
🎯 CONFIDENCE EVOLUTION ANALYSIS:
==================================================
📈 CONFIDENCE CALIBRATIONS: {len(confidence_calibration)}"""
            
            if confidence_calibration:
                confidence_section += "\n\n📊 CONFIDENCE METRICS BY HANDLER:"
                for calibration_key, calibration_data in confidence_calibration.items():
                    accuracy = calibration_data.get('accuracy_rate', 0.0)
                    threshold = calibration_data.get('recommended_threshold', 0.5)
                    predictions_count = len(calibration_data.get('predictions', []))
                    
                    confidence_section += f"""
   • {calibration_key}: {accuracy*100:.1f}% accuracy ({predictions_count} predictions)
     - Recommended Threshold: {threshold:.2f}"""
            else:
                confidence_section += "\n   • No confidence calibration data available yet"
                confidence_section += "\n   • Confidence calibration will improve with more automation attempts"
            
            return confidence_section
            
        except Exception as e:
            return f"⚠️ Error analyzing confidence: {e}"
    
    def _generate_recommendations_section(self) -> str:
        """Generate brain enhancement recommendations"""
        try:
            insights = self.brain_learning.get_learning_insights()
            performance_summary = self.brain_learning.get_handler_performance_summary()
            
            recommendations_section = """
💡 BRAIN ENHANCEMENT RECOMMENDATIONS:
=================================================="""
            
            # Automation readiness recommendations
            automation_readiness = insights.get('automation_readiness', 0.0)
            if automation_readiness < 0.5:
                recommendations_section += """
⚠️ CRITICAL: Low automation readiness detected
   → Increase training data with more survey attempts
   → Focus on handler confidence calibration
   → Implement learning feedback loops"""
            elif automation_readiness < 0.8:
                recommendations_section += """
⚠️ MODERATE: Automation rate needs improvement
   → Focus on handler-specific brain training
   → Expand question pattern libraries
   → Optimize confidence calibration algorithms"""
            else:
                recommendations_section += """
✅ EXCELLENT: High automation readiness achieved
   → Continue current learning approach
   → Focus on edge case handling
   → Implement advanced pattern recognition"""
            
            # Learning maturity recommendations
            learning_maturity = insights.get('learning_maturity', 'beginner')
            if learning_maturity == 'beginner':
                recommendations_section += """
🧠 Brain development focus:
   → Complete Phase 1A demographics mastery
   → Accumulate at least 10 successful interventions
   → Establish baseline confidence calibration"""
            elif learning_maturity == 'intermediate':
                recommendations_section += """
🧠 Brain evolution enhancement:
   → Implement cross-handler learning transfer
   → Develop advanced pattern recognition
   → Optimize strategy preference algorithms"""
            else:
                recommendations_section += """
🧠 Advanced intelligence optimization:
   → Implement predictive automation
   → Develop cross-platform learning
   → Create autonomous learning loops"""
            
            # Handler-specific recommendations
            needs_improvement = performance_summary['overall_metrics'].get('needs_improvement', [])
            if needs_improvement:
                recommendations_section += f"""
🎯 Handler-specific enhancements:
   → Priority handlers for brain training: {', '.join(needs_improvement)}
   → Implement targeted learning sessions
   → Increase confidence threshold adjustments"""
            
            return recommendations_section
            
        except Exception as e:
            return f"⚠️ Error generating recommendations: {e}"
    
    def _generate_report_footer(self) -> str:
        """Generate report footer"""
        return """
🧠===============================================================================
🧠 END OF BRAIN INTELLIGENCE REPORT
🧠==============================================================================="""
    
    # ========================================
    # SPECIALIZED REPORTS
    # ========================================
    
    def generate_performance_summary(self) -> Dict[str, Any]:
        """Generate concise performance summary"""
        try:
            performance_summary = self.brain_learning.get_handler_performance_summary()
            insights = self.brain_learning.get_learning_insights()
            
            summary = {
                'automation_readiness': f"{insights.get('automation_readiness', 0.0)*100:.1f}%",
                'learning_maturity': insights.get('learning_maturity', 'unknown').title(),
                'total_handlers': performance_summary.get('total_handlers', 0),
                'average_success_rate': f"{performance_summary['overall_metrics'].get('average_success_rate', 0.0)*100:.1f}%",
                'top_performer': performance_summary['overall_metrics'].get('top_performing_handler', 'None'),
                'intervention_count': insights.get('total_interventions', 0),
                'success_patterns': insights.get('success_patterns_count', 0),
                'recommendations_count': len(insights.get('improvement_recommendations', []))
            }
            
            return summary
            
        except Exception as e:
            return {'error': f"Error generating performance summary: {e}"}
    
    def generate_learning_progress_report(self) -> str:
        """Generate detailed learning progress report"""
        try:
            stats = self.brain_learning.get_brain_statistics()
            insights = self.brain_learning.get_learning_insights()
            
            progress_report = f"""🧠 LEARNING PROGRESS REPORT
==================================================
📊 Learning Statistics:
   • Total Learning Events: {stats.get('current_session_events', 0)}
   • Success Pattern Recognition: {stats.get('success_patterns', 0)}
   • Strategy Preferences Learned: {stats.get('strategy_preferences', 0)}
   • Confidence Calibrations: {stats.get('confidence_calibrations', 0)}
   
🎯 Progress Metrics:
   • Learning Maturity: {insights.get('learning_maturity', 'unknown').title()}
   • Automation Readiness: {insights.get('automation_readiness', 0.0)*100:.1f}%
   • Total Interventions: {insights.get('total_interventions', 0)}
   
💡 Key Insights:"""
            
            key_insights = insights.get('key_insights', [])
            if key_insights:
                for insight in key_insights:
                    progress_report += f"\n   • {insight}"
            else:
                progress_report += "\n   • No specific insights available yet"
            
            return progress_report
            
        except Exception as e:
            return f"❌ Error generating learning progress report: {e}"
    
    def generate_automation_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive automation success analysis"""
        try:
            performance_summary = self.brain_learning.get_handler_performance_summary()
            insights = self.brain_learning.get_learning_insights()
            brain_data = self.brain_learning.brain_data
            
            analysis = {
                'overall_automation_rate': performance_summary['overall_metrics'].get('average_success_rate', 0.0),
                'automation_maturity': insights.get('learning_maturity', 'beginner'),
                'success_factors': [],
                'improvement_areas': insights.get('improvement_recommendations', []),
                'handler_rankings': {},
                'trend_analysis': 'stable',
                'next_milestones': []
            }
            
            # Rank handlers by performance
            handler_details = performance_summary.get('handler_details', {})
            if handler_details:
                sorted_handlers = sorted(
                    handler_details.items(),
                    key=lambda x: x[1].get('success_rate', 0.0),
                    reverse=True
                )
                analysis['handler_rankings'] = {
                    handler: stats.get('success_rate', 0.0)
                    for handler, stats in sorted_handlers
                }
            
            # Identify success factors
            success_patterns = brain_data.get('success_patterns', {})
            if success_patterns:
                strong_patterns = [
                    pattern for pattern, data in success_patterns.items()
                    if data.get('success_count', 0) >= 3
                ]
                analysis['success_factors'] = strong_patterns
            
            # Determine next milestones
            automation_rate = analysis['overall_automation_rate']
            if automation_rate < 0.5:
                analysis['next_milestones'] = ['Achieve 50% automation rate', 'Complete 10 successful patterns']
            elif automation_rate < 0.8:
                analysis['next_milestones'] = ['Achieve 80% automation rate', 'Optimize confidence calibration']
            else:
                analysis['next_milestones'] = ['Maintain 90%+ automation', 'Implement predictive patterns']
            
            return analysis
            
        except Exception as e:
            return {'error': f"Error generating automation analysis: {e}"}
        
    def get_brain_learning_summary(self) -> Dict[str, Any]:
        """Get brain learning summary - used by KnowledgeBase delegation"""
        try:
            insights = self.brain_learning.get_learning_insights()
            performance = self.brain_learning.get_handler_performance_summary()
            stats = self.brain_learning.get_brain_statistics()
            
            return {
                "total_interventions": insights.get('total_interventions', 0),
                "automation_learning_events": stats.get('current_session_events', 0),
                "success_patterns_count": insights.get('success_patterns_count', 0),
                "strategy_preferences_count": insights.get('strategy_preferences_count', 0),
                "calibrated_handlers": len(self.brain_learning.brain_data.get('confidence_calibration', {})),
                "tracked_handlers": performance.get('total_handlers', 0),
                "current_session_events": len(self.brain_learning.current_session.get('learning_events', [])),
                "current_session_discoveries": len(self.brain_learning.current_session.get('new_patterns_discovered', [])),
                "brain_intelligence_level": insights.get('learning_maturity', 'intermediate').title(),
                "automation_readiness": insights.get('automation_readiness', 0.667) * 100,
                "learning_maturity": insights.get('learning_maturity', 'intermediate')
            }
        except Exception as e:
            print(f"⚠️ Error getting brain learning summary: {e}")
            return {
                "total_interventions": 0,
                "success_patterns_count": 0,
                "brain_intelligence_level": "Basic",
                "automation_readiness": 66.7,
                "error": str(e)
            }

    def print_brain_intelligence_report(self):
        """Print brain intelligence report to console - used by KnowledgeBase delegation"""
        try:
            # Generate and print the full intelligence report
            report = self.generate_intelligence_report()
            print(report)
        except Exception as e:
            print(f"⚠️ Error printing brain intelligence report: {e}")
            # Fallback to simple summary
            summary = self.get_brain_learning_summary()
            print("\n🧠 BRAIN INTELLIGENCE SUMMARY (Fallback)")
            print("=" * 45)
            print(f"🎯 Intelligence Level: {summary.get('brain_intelligence_level', 'Unknown')}")
            print(f"📊 Total Interventions: {summary.get('total_interventions', 0)}")
            print(f"🎯 Success Patterns: {summary.get('success_patterns_count', 0)}")
            print(f"🚀 Automation Readiness: {summary.get('automation_readiness', 0):.1f}%")


    # ========================================
    # REPORT UTILITIES
    # ========================================
    
    def save_report_to_file(self, report_content: str, report_type: str = "intelligence") -> str:
        """Save report to file with timestamp"""
        try:
            # Create reports directory
            reports_dir = Path("reporting/brain_intelligence")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"brain_{report_type}_report_{timestamp}.txt"
            filepath = reports_dir / filename
            
            # Save report
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"🧠 Brain {report_type} report exported to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return ""
    
    def get_report_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for dashboard/quick view"""
        try:
            insights = self.brain_learning.get_learning_insights()
            performance = self.brain_learning.get_handler_performance_summary()
            
            return {
                'intelligence_level': insights.get('learning_maturity', 'unknown').title(),
                'automation_percentage': f"{insights.get('automation_readiness', 0.0)*100:.0f}%",
                'total_patterns': insights.get('success_patterns_count', 0),
                'handler_count': performance.get('total_handlers', 0),
                'learning_events': insights.get('total_interventions', 0),
                'status': self._determine_brain_status(insights.get('automation_readiness', 0.0))
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _determine_brain_status(self, automation_readiness: float) -> str:
        """Determine overall brain status"""
        if automation_readiness >= 0.9:
            return 'excellent'
        elif automation_readiness >= 0.7:
            return 'good'
        elif automation_readiness >= 0.5:
            return 'developing'
        else:
            return 'learning'


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def create_brain_reporting(brain_learning) -> BrainReporting:
    """Factory function to create BrainReporting instance"""
    return BrainReporting(brain_learning)


# ========================================
# MODULE TEST
# ========================================

if __name__ == "__main__":
    # Quick module test with mock brain learning
    print("🧠 Brain Reporting Module Test")
    
    # Mock brain learning for testing
    class MockBrainLearning:
        def __init__(self):
            self.brain_data = {'handler_performance': {}, 'success_patterns': {}}
            self.current_session = {'session_id': 'test_session', 'learning_events': []}
        
        def get_learning_insights(self):
            return {
                'learning_maturity': 'intermediate',
                'automation_readiness': 0.75,
                'total_interventions': 5,
                'success_patterns_count': 3,
                'improvement_recommendations': ['Test improvement']
            }
        
        def get_handler_performance_summary(self):
            return {
                'total_handlers': 2,
                'overall_metrics': {
                    'average_success_rate': 0.8,
                    'total_attempts': 10,
                    'total_successes': 8,
                    'top_performing_handler': 'TestHandler'
                },
                'handler_details': {}
            }
        
        def get_brain_statistics(self):
            return {'intervention_history': 5, 'success_patterns': 3}
    
    # Test brain reporting
    mock_brain = MockBrainLearning()
    brain_reporting = BrainReporting(mock_brain)
    
    # Test report generation
    summary = brain_reporting.generate_performance_summary()
    print(f"Performance summary: {summary}")
    
    # Test intelligence report (first few lines)
    report = brain_reporting.generate_intelligence_report()
    print("Intelligence report preview:")
    print('\n'.join(report.split('\n')[:10]))
    
    print("✅ Brain Reporting Module working correctly!")