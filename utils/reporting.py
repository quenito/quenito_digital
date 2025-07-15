"""
🧠 Brain-Enhanced Reporting Module v2.0
Generates comprehensive reports with DIGITAL BRAIN INTELLIGENCE ANALYSIS.

NEW FEATURES:
- ✅ Brain evolution tracking and analysis
- ✅ Intelligence progression reporting  
- ✅ Learning correlation insights
- ✅ Confidence calibration analysis
- ✅ Pattern discovery reporting
- ✅ Handler intelligence evolution
- ✅ Automation readiness progression
"""

import os
import time
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class BrainEnhancedReportGenerator:
    """
    🧠 Enhanced report generator with digital brain intelligence analysis.
    Creates comprehensive reports showing not just automation performance,
    but how Quenito's brain learns and evolves during each session.
    """
    
    def __init__(self, knowledge_base=None):
        """Initialize brain-enhanced report generator."""
        self.knowledge_base = knowledge_base
        self.session_start_time = None
        self.session_end_time = None
        
        print("🧠 Brain-Enhanced Report Generator initialized!")
        if self.knowledge_base:
            print("🔗 Connected to Quenito's Digital Brain for intelligence analysis")
        else:
            print("⚠️ No brain connection - intelligence analysis will be limited")
    
    def start_session(self):
        """Mark the start of a survey session."""
        self.session_start_time = time.time()
        print("⏰ Brain-enhanced reporting session started")

    def end_session(self):
        """Mark the end of a survey session."""
        self.session_end_time = time.time()
        print("📊 Brain-enhanced reporting session completed")
    
    def generate_brain_intelligence_report(self, brain_enhanced_stats, 
                                         session_stats: Dict[str, Any] = None,
                                         handler_stats: Dict[str, Any] = None) -> str:
        """
        Generate comprehensive brain intelligence report.
        
        Args:
            brain_enhanced_stats: BrainEnhancedSurveyStats instance
            session_stats: Session-level statistics
            handler_stats: Handler performance statistics
            
        Returns:
            Formatted brain intelligence report string
        """
        try:
            report = []
            report.append("🧠" + "=" * 79)
            report.append("🧠 QUENITO'S DIGITAL BRAIN INTELLIGENCE REPORT")
            report.append("🧠" + "=" * 79)
            
            # Brain baseline and evolution
            report.extend(self._generate_brain_evolution_section(brain_enhanced_stats))
            
            # Core automation performance with brain correlation
            report.extend(self._generate_brain_correlated_performance_section(brain_enhanced_stats))
            
            # Handler intelligence analysis
            report.extend(self._generate_handler_intelligence_section(brain_enhanced_stats))
            
            # Learning events and pattern discoveries
            report.extend(self._generate_learning_events_section(brain_enhanced_stats))
            
            # Confidence evolution analysis
            report.extend(self._generate_confidence_evolution_section(brain_enhanced_stats))
            
            # Brain improvement recommendations
            report.extend(self._generate_brain_recommendations_section(brain_enhanced_stats))
            
            # Traditional survey metrics (for compatibility)
            report.extend(self._generate_traditional_survey_section(brain_enhanced_stats))
            
            # Future brain development roadmap
            report.extend(self._generate_brain_roadmap_section(brain_enhanced_stats))
            
            report.append("🧠" + "=" * 79)
            report.append("🧠 END OF BRAIN INTELLIGENCE REPORT")
            report.append("🧠" + "=" * 79)
            
            return "\n".join(report)
            
        except Exception as e:
            print(f"❌ Error generating brain intelligence report: {e}")
            return self._generate_fallback_report(brain_enhanced_stats, str(e))
    
    def _generate_brain_evolution_section(self, stats) -> List[str]:
        """Generate brain evolution and intelligence progression analysis."""
        section = [
            "",
            "🧠 BRAIN EVOLUTION ANALYSIS:",
            "=" * 50
        ]
        
        try:
            evolution_metrics = stats.get_brain_evolution_metrics()
            session_data = stats.session_data
            
            # Brain intelligence progression
            brain_start = session_data.get("brain_intelligence_start", {})
            brain_end = session_data.get("brain_intelligence_end", {})
            
            if brain_start and brain_end:
                start_level = brain_start.get('brain_intelligence_level', 'Unknown')
                end_level = brain_end.get('brain_intelligence_level', 'Unknown')
                start_readiness = brain_start.get('automation_readiness', 0)
                end_readiness = brain_end.get('automation_readiness', 0)
                readiness_improvement = end_readiness - start_readiness
                
                section.extend([
                    f"📊 Intelligence Level: {start_level} → {end_level}",
                    f"🎯 Automation Readiness: {start_readiness:.1f}% → {end_readiness:.1f}% (+{readiness_improvement:.1f}%)",
                    f"🧠 Total Interventions Learned: {brain_end.get('total_interventions', 0)}",
                    f"🎯 Success Patterns Stored: {brain_end.get('success_patterns_count', 0)}",
                    f"⚙️ Calibrated Handlers: {brain_end.get('calibrated_handlers', 0)}",
                    ""
                ])
            else:
                section.extend([
                    "⚠️ Brain baseline data not available",
                    "🔧 Recommendation: Ensure brain connection during survey initialization",
                    ""
                ])
            
            # Session learning summary
            learning_improvement = session_data.get("automation_improvement", 0)
            new_patterns = session_data.get("new_patterns_learned", 0)
            calibrations = session_data.get("confidence_calibrations", 0)
            
            section.extend([
                "📈 SESSION LEARNING SUMMARY:",
                f"   • Automation Improvement: +{learning_improvement:.1f}%",
                f"   • New Patterns Learned: {new_patterns}",
                f"   • Confidence Calibrations: {calibrations}",
                f"   • Learning Events: {len(evolution_metrics.get('learning_events', []))}",
                f"   • Pattern Discoveries: {len(evolution_metrics.get('pattern_discoveries', []))}",
                ""
            ])
            
        except Exception as e:
            section.extend([
                f"⚠️ Error analyzing brain evolution: {e}",
                "🔧 Check brain connection and data integrity",
                ""
            ])
        
        return section
    
    def _generate_brain_correlated_performance_section(self, stats) -> List[str]:
        """Generate performance analysis correlated with brain learning."""
        section = [
            "📊 BRAIN-CORRELATED PERFORMANCE ANALYSIS:",
            "=" * 50
        ]
        
        try:
            # Core metrics
            total_questions = stats.get_total_questions()
            automated_questions = stats.get_automated_questions()
            manual_interventions = stats.get_manual_interventions()
            automation_rate = stats.get_automation_rate()
            learning_rate = stats.get_brain_learning_rate()
            
            section.extend([
                f"🎯 CORE AUTOMATION METRICS:",
                f"   • Total Questions Processed: {total_questions}",
                f"   • Successfully Automated: {automated_questions}",
                f"   • Manual Interventions: {manual_interventions}",
                f"   • Automation Rate: {automation_rate:.1f}%",
                f"   • Brain Learning Rate: {learning_rate:.2f} events/question",
                ""
            ])
            
            # Timing analysis
            total_time = stats.get_total_time()
            if total_time > 0:
                questions_per_minute = stats.get_questions_per_minute()
                section.extend([
                    f"⏱️ TIMING ANALYSIS:",
                    f"   • Total Session Time: {total_time/60:.1f} minutes",
                    f"   • Questions per Minute: {questions_per_minute:.1f}",
                    f"   • Average Time per Question: {total_time/total_questions:.1f} seconds" if total_questions > 0 else "   • Average Time per Question: N/A",
                    ""
                ])
            
            # Learning correlation analysis
            if automation_rate > 0 and learning_rate > 0:
                learning_efficiency = automation_rate / (learning_rate * 100)  # Automation per learning event
                section.extend([
                    f"🧠 LEARNING CORRELATION:",
                    f"   • Learning Efficiency: {learning_efficiency:.2f} automation/learning_event",
                    f"   • Brain Growth Velocity: {learning_rate * questions_per_minute:.2f} learning_events/minute" if total_time > 0 else "   • Brain Growth Velocity: N/A",
                    ""
                ])
            
        except Exception as e:
            section.extend([
                f"⚠️ Error analyzing brain-correlated performance: {e}",
                ""
            ])
        
        return section
    
    def _generate_handler_intelligence_section(self, stats) -> List[str]:
        """Generate handler intelligence and performance evolution analysis."""
        section = [
            "🎯 HANDLER INTELLIGENCE ANALYSIS:",
            "=" * 50
        ]
        
        try:
            handler_summary = stats.get_handler_performance_summary()
            
            if handler_summary:
                section.append("📊 HANDLER PERFORMANCE MATRIX:")
                
                # Sort handlers by success rate
                sorted_handlers = sorted(handler_summary.items(), 
                                       key=lambda x: x[1]['success_rate'], reverse=True)
                
                for handler_name, metrics in sorted_handlers:
                    success_rate = metrics['success_rate']
                    avg_confidence = metrics['average_confidence']
                    total_attempts = metrics['total_attempts']
                    trend = metrics['trend']
                    
                    # Determine trend emoji
                    trend_emoji = {
                        'improving': '📈',
                        'declining': '📉', 
                        'stable': '➡️',
                        'insufficient_data': '❓'
                    }.get(trend, '❓')
                    
                    section.append(f"   • {handler_name}:")
                    section.append(f"     - Success Rate: {success_rate:.1f}% ({total_attempts} attempts)")
                    section.append(f"     - Avg Confidence: {avg_confidence:.2f}")
                    section.append(f"     - Intelligence Trend: {trend} {trend_emoji}")
                
                section.append("")
                
                # Handler intelligence insights
                best_handler = sorted_handlers[0] if sorted_handlers else None
                if best_handler:
                    best_name, best_metrics = best_handler
                    section.extend([
                        "🏆 TOP PERFORMING HANDLER:",
                        f"   • {best_name}: {best_metrics['success_rate']:.1f}% success rate",
                        f"   • This handler shows the strongest brain integration",
                        ""
                    ])
                
                # Identify handlers needing improvement
                struggling_handlers = [name for name, metrics in handler_summary.items() 
                                     if metrics['success_rate'] < 50 and metrics['total_attempts'] > 2]
                
                if struggling_handlers:
                    section.extend([
                        "⚠️ HANDLERS NEEDING BRAIN ENHANCEMENT:",
                        *[f"   • {handler}: Consider additional pattern training" for handler in struggling_handlers],
                        ""
                    ])
            else:
                section.extend([
                    "⚠️ No handler performance data available",
                    "🔧 Handlers may not be reporting performance metrics correctly",
                    ""
                ])
                
        except Exception as e:
            section.extend([
                f"⚠️ Error analyzing handler intelligence: {e}",
                ""
            ])
        
        return section
    
    def _generate_learning_events_section(self, stats) -> List[str]:
        """Generate learning events and pattern discovery analysis."""
        section = [
            "📚 LEARNING EVENTS & PATTERN DISCOVERIES:",
            "=" * 50
        ]
        
        try:
            learning_events = getattr(stats, 'learning_events', [])
            pattern_discoveries = getattr(stats, 'pattern_discoveries', [])
            brain_improvements = getattr(stats, 'brain_improvements', [])
            
            # Learning events summary
            if learning_events:
                successful_automations = [e for e in learning_events if e.get('event_type') == 'successful_automation']
                manual_interventions = [e for e in learning_events if e.get('event_type') == 'manual_intervention']
                
                section.extend([
                    f"📊 LEARNING EVENTS SUMMARY:",
                    f"   • Total Learning Events: {len(learning_events)}",
                    f"   • Successful Automations: {len(successful_automations)}",
                    f"   • Manual Interventions: {len(manual_interventions)}",
                    ""
                ])
                
                # Recent learning events (last 5)
                recent_events = learning_events[-5:] if len(learning_events) > 5 else learning_events
                if recent_events:
                    section.append("🔍 RECENT LEARNING EVENTS:")
                    for event in recent_events:
                        event_type = event.get('event_type', 'unknown')
                        handler = event.get('handler', 'unknown')
                        confidence = event.get('confidence', 0)
                        timestamp = event.get('timestamp', 0)
                        
                        time_str = time.strftime('%H:%M:%S', time.localtime(timestamp))
                        emoji = '✅' if event_type == 'successful_automation' else '📝'
                        section.append(f"   {emoji} {time_str}: {handler} - {event_type} (conf: {confidence:.2f})")
                    section.append("")
            
            # Pattern discoveries
            if pattern_discoveries:
                section.extend([
                    f"🔍 PATTERN DISCOVERIES:",
                    f"   • New Patterns Discovered: {len(pattern_discoveries)}",
                    ""
                ])
                
                for discovery in pattern_discoveries:
                    pattern_type = discovery.get('pattern_type', 'unknown')
                    timestamp = discovery.get('timestamp', 0)
                    time_str = time.strftime('%H:%M:%S', time.localtime(timestamp))
                    section.append(f"   🆕 {time_str}: {pattern_type} pattern discovered")
                section.append("")
            
            # Brain improvements
            if brain_improvements:
                section.extend([
                    f"🧠 BRAIN IMPROVEMENTS:",
                    f"   • Brain Enhancement Events: {len(brain_improvements)}",
                    ""
                ])
                
                for improvement in brain_improvements:
                    improvement_type = improvement.get('improvement_type', 'unknown')
                    timestamp = improvement.get('timestamp', 0)
                    time_str = time.strftime('%H:%M:%S', time.localtime(timestamp))
                    section.append(f"   🚀 {time_str}: {improvement_type}")
                section.append("")
            
            if not learning_events and not pattern_discoveries and not brain_improvements:
                section.extend([
                    "⚠️ No learning events recorded this session",
                    "🔧 Verify brain learning integration is active",
                    ""
                ])
                
        except Exception as e:
            section.extend([
                f"⚠️ Error analyzing learning events: {e}",
                ""
            ])
        
        return section
    
    def _generate_confidence_evolution_section(self, stats) -> List[str]:
        """Generate confidence evolution and calibration analysis."""
        section = [
            "🎯 CONFIDENCE EVOLUTION ANALYSIS:",
            "=" * 50
        ]
        
        try:
            confidence_evolution = getattr(stats, 'confidence_evolution', [])
            
            if confidence_evolution:
                # Calculate confidence trends by handler
                handler_confidence = {}
                for point in confidence_evolution:
                    handler = point.get('handler', 'unknown')
                    confidence = point.get('confidence', 0)
                    
                    if handler not in handler_confidence:
                        handler_confidence[handler] = []
                    handler_confidence[handler].append(confidence)
                
                # Analyze trends
                section.append("📈 CONFIDENCE TRENDS BY HANDLER:")
                for handler, confidences in handler_confidence.items():
                    if len(confidences) >= 2:
                        avg_confidence = sum(confidences) / len(confidences)
                        first_half = confidences[:len(confidences)//2]
                        second_half = confidences[len(confidences)//2:]
                        
                        first_avg = sum(first_half) / len(first_half) if first_half else 0
                        second_avg = sum(second_half) / len(second_half) if second_half else 0
                        
                        trend = "improving" if second_avg > first_avg + 0.05 else "declining" if second_avg < first_avg - 0.05 else "stable"
                        trend_emoji = {'improving': '📈', 'declining': '📉', 'stable': '➡️'}[trend]
                        
                        section.append(f"   • {handler}: {avg_confidence:.2f} avg, {trend} {trend_emoji}")
                    else:
                        section.append(f"   • {handler}: {confidences[0]:.2f} (single measurement)")
                
                section.extend([
                    "",
                    f"🔢 CONFIDENCE STATISTICS:",
                    f"   • Total Confidence Measurements: {len(confidence_evolution)}",
                    f"   • Handlers Tracked: {len(handler_confidence)}",
                    ""
                ])
            else:
                section.extend([
                    "⚠️ No confidence evolution data available",
                    "🔧 Ensure handlers are reporting confidence scores",
                    ""
                ])
                
        except Exception as e:
            section.extend([
                f"⚠️ Error analyzing confidence evolution: {e}",
                ""
            ])
        
        return section
    
    def _generate_brain_recommendations_section(self, stats) -> List[str]:
        """Generate brain intelligence improvement recommendations."""
        section = [
            "💡 BRAIN ENHANCEMENT RECOMMENDATIONS:",
            "=" * 50
        ]
        
        try:
            recommendations = []
            
            # Analyze automation rate and brain learning correlation
            automation_rate = stats.get_automation_rate()
            learning_rate = stats.get_brain_learning_rate()
            
            # Automation rate recommendations
            if automation_rate < 50:
                recommendations.extend([
                    "🚨 CRITICAL: Low automation rate detected",
                    "   → Increase brain learning data through more manual interventions",
                    "   → Review and enhance question pattern recognition",
                    "   → Consider lowering confidence thresholds for learning mode"
                ])
            elif automation_rate < 75:
                recommendations.extend([
                    "⚠️ MODERATE: Automation rate needs improvement",
                    "   → Focus on handler-specific brain training",
                    "   → Expand question pattern libraries",
                    "   → Optimize confidence calibration algorithms"
                ])
            elif automation_rate < 90:
                recommendations.extend([
                    "✅ GOOD: Solid automation performance",
                    "   → Fine-tune edge case handling",
                    "   → Enhance cross-handler knowledge sharing",
                    "   → Implement predictive question sequencing"
                ])
            else:
                recommendations.extend([
                    "🏆 EXCELLENT: Outstanding automation performance!",
                    "   → Focus on intelligence optimization",
                    "   → Explore advanced AI integration",
                    "   → Consider commercial deployment readiness"
                ])
            
            # Learning rate analysis
            if learning_rate < 0.1:
                recommendations.extend([
                    "📚 Brain learning opportunities:",
                    "   → Increase manual intervention capture",
                    "   → Implement active learning strategies",
                    "   → Enhance pattern discovery algorithms"
                ])
            elif learning_rate > 1.0:
                recommendations.extend([
                    "🧠 High learning activity detected:",
                    "   → Validate learning quality vs quantity",
                    "   → Optimize learning event filtering",
                    "   → Focus on pattern consolidation"
                ])
            
            # Handler-specific recommendations
            handler_summary = stats.get_handler_performance_summary()
            for handler_name, metrics in handler_summary.items():
                if metrics['success_rate'] < 30 and metrics['total_attempts'] > 3:
                    recommendations.append(f"   → {handler_name}: Requires immediate brain enhancement")
                elif metrics['trend'] == 'declining':
                    recommendations.append(f"   → {handler_name}: Monitor for confidence calibration issues")
            
            # Brain evolution recommendations
            evolution_metrics = stats.get_brain_evolution_metrics()
            if evolution_metrics.get('automation_improvement', 0) < 5:
                recommendations.extend([
                    "🧠 Brain evolution enhancement:",
                    "   → Implement more sophisticated learning algorithms",
                    "   → Increase pattern recognition sensitivity",
                    "   → Enhance success pattern storage mechanisms"
                ])
            
            # Knowledge base recommendations
            if self.knowledge_base:
                try:
                    brain_summary = self.knowledge_base.get_brain_learning_summary()
                    intelligence_level = brain_summary.get('brain_intelligence_level', 'Unknown')
                    
                    if intelligence_level == 'Beginner':
                        recommendations.extend([
                            "🎓 Brain development focus:",
                            "   → Complete Phase 1A demographics mastery",
                            "   → Accumulate at least 10 successful interventions",
                            "   → Establish baseline confidence calibration"
                        ])
                    elif intelligence_level == 'Learning':
                        recommendations.extend([
                            "📈 Intelligence advancement:",
                            "   → Expand to Phase 1B multi-format testing",
                            "   → Develop specialized handler expertise",
                            "   → Implement cross-survey learning"
                        ])
                    elif intelligence_level == 'Intermediate':
                        recommendations.extend([
                            "🚀 Advanced capabilities:",
                            "   → Begin Phase 2 brand intelligence development",
                            "   → Implement predictive automation",
                            "   → Enhance multi-platform compatibility"
                        ])
                except Exception:
                    pass
            
            # Add recommendations to section
            if recommendations:
                for rec in recommendations:
                    section.append(rec)
            else:
                section.extend([
                    "🎯 System operating optimally!",
                    "   → Continue monitoring brain evolution",
                    "   → Focus on intelligence maintenance",
                    "   → Prepare for advanced feature development"
                ])
            
            section.append("")
            
        except Exception as e:
            section.extend([
                f"⚠️ Error generating brain recommendations: {e}",
                ""
            ])
        
        return section
    
    def _generate_traditional_survey_section(self, stats) -> List[str]:
        """Generate traditional survey metrics for compatibility."""
        section = [
            "📊 TRADITIONAL SURVEY METRICS:",
            "=" * 50
        ]
        
        try:
            # Get traditional stats for compatibility
            traditional_stats = stats.get_stats()
            
            section.extend([
                f"📈 LEGACY COMPATIBILITY METRICS:",
                f"   • Questions Encountered: {traditional_stats.get('total_questions', 0)}",
                f"   • Automation Successes: {traditional_stats.get('automated_questions', 0)}",
                f"   • Manual Interventions: {traditional_stats.get('manual_interventions', 0)}",
                f"   • Research Operations: {traditional_stats.get('research_performed', 0)}",
                ""
            ])
            
            # Question type breakdown
            question_types = traditional_stats.get('question_types_encountered', {})
            if question_types:
                section.append("🔍 QUESTION TYPE BREAKDOWN:")
                for q_type, count in sorted(question_types.items(), key=lambda x: x[1], reverse=True):
                    section.append(f"   • {q_type}: {count} occurrences")
                section.append("")
            
        except Exception as e:
            section.extend([
                f"⚠️ Error generating traditional metrics: {e}",
                ""
            ])
        
        return section
    
    def _generate_brain_roadmap_section(self, stats) -> List[str]:
        """Generate future brain development roadmap."""
        section = [
            "🗺️ BRAIN DEVELOPMENT ROADMAP:",
            "=" * 50
        ]
        
        try:
            automation_rate = stats.get_automation_rate()
            evolution_metrics = stats.get_brain_evolution_metrics()
            
            # Determine current phase and next steps
            if automation_rate < 60:
                phase = "Phase 1A: Demographics Foundation"
                next_milestone = "Achieve 100% demographics automation"
                timeline = "Current focus - complete within 1-2 weeks"
            elif automation_rate < 80:
                phase = "Phase 1B: Format Expansion"
                next_milestone = "Master all demographic question formats"
                timeline = "Next 2-3 weeks"
            elif automation_rate < 90:
                phase = "Phase 1C: Complex Demographics"
                next_milestone = "Handle multi-question demographic pages"
                timeline = "Next 3-4 weeks"
            else:
                phase = "Phase 2: Brand Intelligence"
                next_milestone = "Develop brand familiarity automation"
                timeline = "Ready for advanced development"
            
            section.extend([
                f"🎯 CURRENT DEVELOPMENT PHASE:",
                f"   • Phase: {phase}",
                f"   • Next Milestone: {next_milestone}",
                f"   • Timeline: {timeline}",
                "",
                f"🚀 BRAIN EVOLUTION PATHWAY:",
                f"   • Current Automation Rate: {automation_rate:.1f}%",
                f"   • Learning Events This Session: {len(evolution_metrics.get('learning_events', []))}",
                f"   • Pattern Discoveries: {len(evolution_metrics.get('pattern_discoveries', []))}",
                ""
            ])
            
            # Future capabilities roadmap
            section.extend([
                "🔮 FUTURE BRAIN CAPABILITIES:",
                "   🎯 Phase 2: Brand Familiarity Mastery (60-70% automation)",
                "   🎯 Phase 3: Survey Prediction (80-85% automation)",
                "   🎯 Phase 4: True AI Assistant (99% automation)",
                "",
                "💫 ULTIMATE VISION:",
                "   • Human-indistinguishable survey responses",
                "   • Cross-platform universal compatibility",
                "   • Commercial scalability and deployment",
                "   • Self-improving artificial intelligence",
                ""
            ])
            
        except Exception as e:
            section.extend([
                f"⚠️ Error generating brain roadmap: {e}",
                ""
            ])
        
        return section
    
    def _generate_fallback_report(self, stats, error_msg: str) -> str:
        """Generate a basic fallback report when full analysis fails."""
        try:
            fallback = [
                "🧠" + "=" * 79,
                "🧠 BRAIN INTELLIGENCE REPORT (FALLBACK MODE)",
                "🧠" + "=" * 79,
                "",
                f"⚠️ REPORT GENERATION ERROR: {error_msg}",
                "",
                "📊 BASIC METRICS:",
                f"   • Questions Processed: {getattr(stats, 'total_questions', 0)}",
                f"   • Automated: {getattr(stats, 'automated_questions', 0)}",
                f"   • Manual Interventions: {getattr(stats, 'manual_interventions', 0)}",
                f"   • Automation Rate: {stats.get_automation_rate() if hasattr(stats, 'get_automation_rate') else 0:.1f}%",
                "",
                "🔧 TROUBLESHOOTING:",
                "   • Check brain connection during survey initialization",
                "   • Verify BrainEnhancedSurveyStats integration",
                "   • Review error logs for detailed diagnostics",
                "",
                "🧠" + "=" * 79
            ]
            
            return "\n".join(fallback)
            
        except Exception as e:
            return f"🧠 CRITICAL ERROR: Unable to generate even fallback report: {e}"
    
    def export_brain_report(self, report_content: str, filename: str = None) -> bool:
        """Export brain intelligence report to file with brain-specific naming."""
        try:
            # Create brain-specific filename if not provided
            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"brain_intelligence_report_{timestamp}.txt"
            
            # Get report filepath
            filepath = self.get_report_filepath(filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Write report
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"🧠 Brain intelligence report exported to: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting brain report: {e}")
            return False
    
    def get_report_filepath(self, filename: str) -> str:
        """Generate brain report filepath in the reporting directory."""
        # Create reporting directory path
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reporting_dir = os.path.join(script_dir, "reporting", "brain_intelligence")
        
        # Ensure brain intelligence subdirectory exists
        os.makedirs(reporting_dir, exist_ok=True)
        
        return os.path.join(reporting_dir, filename)
    
    def generate_brain_summary_json(self, brain_enhanced_stats) -> Dict[str, Any]:
        """Generate brain intelligence summary in JSON format for API consumption."""
        try:
            evolution_metrics = brain_enhanced_stats.get_brain_evolution_metrics()
            session_data = brain_enhanced_stats.session_data
            
            summary = {
                "timestamp": time.time(),
                "report_type": "brain_intelligence_summary",
                "session_id": session_data.get("session_id", "unknown"),
                "brain_evolution": {
                    "intelligence_level_start": session_data.get("brain_intelligence_start", {}).get("brain_intelligence_level", "Unknown"),
                    "intelligence_level_end": session_data.get("brain_intelligence_end", {}).get("brain_intelligence_level", "Unknown"),
                    "automation_readiness_improvement": session_data.get("automation_improvement", 0),
                    "new_patterns_learned": session_data.get("new_patterns_learned", 0),
                    "confidence_calibrations": session_data.get("confidence_calibrations", 0)
                },
                "performance_metrics": {
                    "total_questions": brain_enhanced_stats.get_total_questions(),
                    "automated_questions": brain_enhanced_stats.get_automated_questions(),
                    "manual_interventions": brain_enhanced_stats.get_manual_interventions(),
                    "automation_rate": brain_enhanced_stats.get_automation_rate(),
                    "brain_learning_rate": brain_enhanced_stats.get_brain_learning_rate()
                },
                "learning_analytics": {
                    "total_learning_events": len(evolution_metrics.get("learning_events", [])),
                    "pattern_discoveries": len(evolution_metrics.get("pattern_discoveries", [])),
                    "brain_improvements": len(evolution_metrics.get("brain_improvements", [])),
                    "confidence_evolution_points": len(evolution_metrics.get("confidence_evolution", []))
                },
                "handler_intelligence": brain_enhanced_stats.get_handler_performance_summary(),
                "recommendations": self._generate_json_recommendations(brain_enhanced_stats),
                "next_development_phase": self._determine_next_phase(brain_enhanced_stats.get_automation_rate())
            }
            
            return summary
            
        except Exception as e:
            return {
                "timestamp": time.time(),
                "report_type": "brain_intelligence_summary",
                "error": str(e),
                "status": "failed"
            }
    
    def _generate_json_recommendations(self, stats) -> List[str]:
        """Generate recommendations in JSON-friendly format."""
        recommendations = []
        automation_rate = stats.get_automation_rate()
        
        if automation_rate < 50:
            recommendations.extend([
                "Increase brain learning data through manual interventions",
                "Review and enhance question pattern recognition",
                "Consider lowering confidence thresholds for learning mode"
            ])
        elif automation_rate < 75:
            recommendations.extend([
                "Focus on handler-specific brain training", 
                "Expand question pattern libraries",
                "Optimize confidence calibration algorithms"
            ])
        elif automation_rate < 90:
            recommendations.extend([
                "Fine-tune edge case handling",
                "Enhance cross-handler knowledge sharing",
                "Implement predictive question sequencing"
            ])
        else:
            recommendations.extend([
                "Focus on intelligence optimization",
                "Explore advanced AI integration", 
                "Consider commercial deployment readiness"
            ])
        
        return recommendations
    
    def _determine_next_phase(self, automation_rate: float) -> Dict[str, str]:
        """Determine next development phase based on automation rate."""
        if automation_rate < 60:
            return {
                "phase": "Phase 1A: Demographics Foundation",
                "milestone": "Achieve 100% demographics automation",
                "timeline": "1-2 weeks"
            }
        elif automation_rate < 80:
            return {
                "phase": "Phase 1B: Format Expansion", 
                "milestone": "Master all demographic question formats",
                "timeline": "2-3 weeks"
            }
        elif automation_rate < 90:
            return {
                "phase": "Phase 1C: Complex Demographics",
                "milestone": "Handle multi-question demographic pages",
                "timeline": "3-4 weeks"
            }
        else:
            return {
                "phase": "Phase 2: Brand Intelligence",
                "milestone": "Develop brand familiarity automation",
                "timeline": "Ready for advanced development"
            }


# Legacy compatibility class
class ReportGenerator(BrainEnhancedReportGenerator):
    """
    Legacy compatibility wrapper for existing code.
    Provides traditional reporting functionality while supporting brain enhancement.
    """
    
    def __init__(self):
        super().__init__(knowledge_base=None)
        print("📊 Legacy ReportGenerator initialized")
        print("🧠 Consider upgrading to BrainEnhancedReportGenerator for full intelligence analysis")
    
    def generate_survey_report(self, survey_stats: Dict[str, Any], 
                             session_stats: Dict[str, Any] = None,
                             handler_stats: Dict[str, Any] = None,
                             intervention_stats: Dict[str, Any] = None,
                             research_stats: Dict[str, Any] = None) -> str:
        """
        Generate traditional survey report for backward compatibility.
        """
        try:
            report = []
            report.append("=" * 80)
            report.append("📊 ENHANCED SURVEY AUTOMATION REPORT")
            report.append("=" * 80)
            
            # Basic survey metrics
            total_questions = survey_stats.get("total_questions", 0)
            automated_questions = survey_stats.get("automated_questions", 0)
            manual_interventions = survey_stats.get("manual_interventions", 0)
            automation_rate = (automated_questions / total_questions * 100) if total_questions > 0 else 0
            
            report.extend([
                "",
                "📈 SURVEY COMPLETION SUMMARY:",
                f"   • Total Questions Processed: {total_questions}",
                f"   • Automated Successfully: {automated_questions}",
                f"   • Manual Interventions: {manual_interventions}",
                f"   • Automation Rate: {automation_rate:.1f}%",
                ""
            ])
            
            # Timing analysis
            if survey_stats.get("start_time") and survey_stats.get("end_time"):
                total_time = survey_stats["end_time"] - survey_stats["start_time"]
                questions_per_minute = (total_questions / total_time * 60) if total_time > 0 else 0
                
                report.extend([
                    "⏱️ TIMING ANALYSIS:",
                    f"   • Total Time: {total_time/60:.1f} minutes",
                    f"   • Questions per Minute: {questions_per_minute:.1f}",
                    ""
                ])
            
            # Handler stats if available
            if handler_stats:
                report.extend([
                    "🎯 HANDLER USAGE:",
                    *[f"   • {handler}: {stats.get('attempts', 0)} attempts" 
                      for handler, stats in handler_stats.items()],
                    ""
                ])
            
            # Basic recommendations
            report.extend([
                "💡 RECOMMENDATIONS:",
                f"   • {'Continue current strategy' if automation_rate >= 80 else 'Improve handler confidence scoring'}",
                f"   • {'Excellent performance!' if automation_rate >= 90 else 'Focus on pattern recognition enhancement'}",
                ""
            ])
            
            report.append("=" * 80)
            return "\n".join(report)
            
        except Exception as e:
            return f"❌ Error generating legacy report: {e}"
    
    def generate_quick_summary(self, survey_stats: Dict[str, Any]) -> str:
        """Generate a quick one-line summary for legacy compatibility."""
        total_questions = survey_stats.get("total_questions", 0)
        automated_questions = survey_stats.get("automated_questions", 0)
        manual_interventions = survey_stats.get("manual_interventions", 0)
        
        automation_rate = 0
        if total_questions > 0:
            automation_rate = (automated_questions / total_questions) * 100
        
        return (f"📊 Survey completed: {total_questions} questions, "
                f"{automation_rate:.1f}% automated, {manual_interventions} manual interventions")
    
    def export_report(self, report_content: str, filepath: str) -> bool:
        """Export report to file with automatic directory creation (legacy method)."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📤 Legacy report exported to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error exporting legacy report: {e}")
            return False
    
    def get_report_filepath(self, filename: str = None) -> str:
        """Generate report filepath in the reporting directory (legacy method)."""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"survey_report_{timestamp}.txt"
        
        # Create reporting directory path
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reporting_dir = os.path.join(script_dir, "reporting")
        
        return os.path.join(reporting_dir, filename)