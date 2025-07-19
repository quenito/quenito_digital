"""
🧠 Brain-Enhanced Survey Statistics Module v2.1 - STEP 3 COMPLETE
Tracks survey completion statistics and performance metrics WITH BRAIN INTEGRATION.

NEW FEATURES FOR STEP 3:
- ✅ Brain learning correlation tracking with automation success
- ✅ Pattern discovery correlation with handler performance  
- ✅ Strategy effectiveness tracking
- ✅ Learning session data with brain feedback loop
- ✅ Complete brain learning integration methods

EXISTING FEATURES:
- ✅ Digital brain learning correlation
- ✅ Handler performance tracking
- ✅ Confidence evolution metrics  
- ✅ Intelligence progression analytics
- ✅ Pattern discovery statistics
"""

import time
from typing import Dict, Any, List, Optional


class BrainEnhancedSurveyStats:
    """
    🧠 Enhanced survey statistics with digital brain integration.
    Tracks not just automation rates, but brain learning and evolution.
    """
    
    def __init__(self, knowledge_base=None):
        """Initialize brain-enhanced survey statistics tracking."""
        self.knowledge_base = knowledge_base
        
        # Core survey metrics
        self.survey_started = False
        self.survey_ended = False
        self.start_time = None
        self.end_time = None
        self.total_questions = 0
        self.automated_questions = 0
        self.manual_interventions = 0
        
        # 🧠 Brain-enhanced metrics
        self.handler_performance = {}
        self.confidence_evolution = []
        self.learning_events = []
        self.pattern_discoveries = []
        self.brain_improvements = []
        
        # Session data for brain correlation
        self.session_data = {
            "session_id": f"stats_session_{int(time.time())}",
            "brain_intelligence_start": None,
            "brain_intelligence_end": None,
            "automation_improvement": 0.0,
            "new_patterns_learned": 0,
            "confidence_calibrations": 0
        }
        
        # Legacy compatibility
        self.stats = {
            "total_questions": 0,
            "automated_questions": 0,
            "manual_interventions": 0,
            "research_performed": 0,
            "start_time": None,
            "end_time": None,
            "question_types_encountered": {},
            # 🧠 New brain metrics
            "brain_learning_events": 0,
            "handler_improvements": {},
            "confidence_evolution": [],
            "intelligence_progression": []
        }
        
        print("🧠 Brain-Enhanced Survey Statistics initialized!")
        if self.knowledge_base:
            print("🔗 Connected to Quenito's Digital Brain")
        else:
            print("⚠️ No brain connection - limited intelligence tracking")
    
    def start_survey(self):
        """Mark the start of survey processing with brain baseline."""
        self.survey_started = True
        self.start_time = time.time()
        self.stats["start_time"] = self.start_time
        
        # 🧠 Capture initial brain intelligence
        if self.knowledge_base:
            brain_summary = self.knowledge_base.get_brain_learning_summary()
            self.session_data["brain_intelligence_start"] = brain_summary
            print(f"🧠 Brain baseline captured: {brain_summary.get('brain_intelligence_level', 'Unknown')} level")
        
        print("⏰ Brain-enhanced survey timing started")
    
    def end_survey(self):
        """Mark the end of survey processing with brain evolution analysis."""
        if not self.survey_ended:
            self.survey_ended = True
            self.end_time = time.time()
            self.stats["end_time"] = self.end_time
            
            # 🧠 Capture final brain intelligence and calculate growth
            if self.knowledge_base:
                brain_summary = self.knowledge_base.get_brain_learning_summary()
                self.session_data["brain_intelligence_end"] = brain_summary
                
                # Calculate brain improvements
                start_brain = self.session_data.get("brain_intelligence_start", {})
                end_brain = brain_summary
                
                if start_brain:
                    self.session_data["automation_improvement"] = (
                        end_brain.get("automation_readiness", 0) - 
                        start_brain.get("automation_readiness", 0)
                    )
                    self.session_data["new_patterns_learned"] = (
                        end_brain.get("success_patterns_count", 0) - 
                        start_brain.get("success_patterns_count", 0)
                    )
                    self.session_data["confidence_calibrations"] = (
                        end_brain.get("calibrated_handlers", 0) - 
                        start_brain.get("calibrated_handlers", 0)
                    )
                
                print(f"🧠 Brain evolution: +{self.session_data['automation_improvement']:.1f}% automation readiness")
                print(f"🧠 New patterns learned: {self.session_data['new_patterns_learned']}")
            
            print("📊 Brain-enhanced survey statistics finalized")
            print("⏰ Survey timing completed")
    
    def increment_question_count(self, handler_type: str = None, confidence: float = None):
        """Increment question count with brain metrics."""
        self.total_questions += 1
        self.stats["total_questions"] += 1
        
        # 🧠 Track handler-specific performance
        if handler_type:
            if handler_type not in self.handler_performance:
                self.handler_performance[handler_type] = {
                    "attempts": 0,
                    "successes": 0,
                    "confidence_scores": [],
                    "evolution_trend": "stable"
                }
            
            self.handler_performance[handler_type]["attempts"] += 1
            
            if confidence is not None:
                self.handler_performance[handler_type]["confidence_scores"].append(confidence)
                self.confidence_evolution.append({
                    "timestamp": time.time(),
                    "handler": handler_type,
                    "confidence": confidence
                })
    
    def increment_automated_count(self, handler_type: str = None, confidence: float = None):
        """Increment automated count with brain learning correlation."""
        self.automated_questions += 1
        self.stats["automated_questions"] += 1
        
        # 🧠 Track successful automation
        if handler_type and handler_type in self.handler_performance:
            self.handler_performance[handler_type]["successes"] += 1
            
            # Update brain learning stats
            if self.knowledge_base:
                self.knowledge_base.update_handler_performance(handler_type, confidence or 0.0, True)
        
        # Record learning event
        self.learning_events.append({
            "timestamp": time.time(),
            "event_type": "successful_automation",
            "handler": handler_type,
            "confidence": confidence
        })
    
    def increment_intervention_count(self, handler_type: str = None, reason: str = None):
        """Increment intervention count with brain learning opportunity."""
        self.manual_interventions += 1
        self.stats["manual_interventions"] += 1
        
        # 🧠 Track learning opportunity
        learning_event = {
            "timestamp": time.time(),
            "event_type": "manual_intervention",
            "handler": handler_type,
            "reason": reason,
            "learning_opportunity": True
        }
        
        self.learning_events.append(learning_event)
        
        # Update brain learning stats
        if self.knowledge_base and handler_type:
            self.knowledge_base.update_handler_performance(handler_type, 0.0, False)
        
        print(f"🧠 Learning opportunity recorded: {handler_type} - {reason}")

    # 🚀 NEW STEP 3 METHODS - Brain Learning Correlation Tracking
    def record_automation_success(self, handler_type: str, confidence: float,
                                 question_type: str, strategy_used: str):
        """Record successful automation with brain learning correlation"""
        
        # Update base stats
        self.increment_automated_count(handler_type, confidence)
        
        # 🧠 Record brain learning correlation
        learning_event = {
            "timestamp": time.time(),
            "event_type": "successful_automation",
            "handler": handler_type,
            "question_type": question_type,
            "strategy_used": strategy_used,
            "confidence": confidence,
            "brain_learning_triggered": True
        }
        
        self.learning_events.append(learning_event)
        
        # Track pattern discovery
        if question_type not in [event.get('question_type') for event in self.learning_events[:-1]]:
            self.pattern_discoveries.append({
                "timestamp": time.time(),
                "pattern_type": question_type,
                "confidence": confidence,
                "first_success": True
            })
            print(f"🧠 NEW PATTERN DISCOVERED: {question_type}")
        
        print(f"📊 Automation success recorded: {handler_type} → {question_type} using {strategy_used}")

    def record_strategy_effectiveness(self, strategy_name: str, success: bool, 
                                    execution_time: float, question_type: str):
        """Record strategy effectiveness for brain learning optimization"""
        
        strategy_event = {
            "timestamp": time.time(),
            "strategy_name": strategy_name,
            "success": success,
            "execution_time": execution_time,
            "question_type": question_type,
            "brain_optimization_data": True
        }
        
        self.learning_events.append(strategy_event)
        
        # Track brain improvement based on strategy success
        if success:
            self.brain_improvements.append({
                "timestamp": time.time(),
                "improvement_type": "strategy_optimization",
                "strategy": strategy_name,
                "question_type": question_type,
                "performance_gain": f"Successful in {execution_time:.1f}s"
            })
            
        print(f"🎯 Strategy effectiveness: {strategy_name} {'✅' if success else '❌'} ({execution_time:.1f}s)")

    def record_confidence_calibration(self, handler_type: str, old_confidence: float, 
                                    new_confidence: float, calibration_reason: str):
        """Record confidence calibration events for brain learning tracking"""
        
        calibration_event = {
            "timestamp": time.time(),
            "event_type": "confidence_calibration",
            "handler": handler_type,
            "old_confidence": old_confidence,
            "new_confidence": new_confidence,
            "confidence_change": new_confidence - old_confidence,
            "calibration_reason": calibration_reason,
            "brain_learning_impact": True
        }
        
        self.learning_events.append(calibration_event)
        self.session_data["confidence_calibrations"] += 1
        
        # Track as brain improvement
        self.brain_improvements.append({
            "timestamp": time.time(),
            "improvement_type": "confidence_calibration",
            "handler": handler_type,
            "improvement_details": f"{old_confidence:.2f} → {new_confidence:.2f}",
            "reason": calibration_reason
        })
        
        print(f"🧠 Confidence calibrated: {handler_type} {old_confidence:.2f} → {new_confidence:.2f} ({calibration_reason})")

    def record_learning_session_data(self, session_type: str, learning_data: Dict[str, Any]):
        """Record comprehensive learning session data for brain evolution tracking"""
        
        session_event = {
            "timestamp": time.time(),
            "session_type": session_type,
            "learning_data": learning_data,
            "session_id": self.session_data["session_id"],
            "brain_evolution_marker": True
        }
        
        self.learning_events.append(session_event)
        
        # Update session metrics
        if session_type == "pattern_learning":
            self.session_data["new_patterns_learned"] += learning_data.get("patterns_count", 0)
        elif session_type == "strategy_optimization":
            # Track strategy improvements
            self.brain_improvements.append({
                "timestamp": time.time(),
                "improvement_type": "strategy_learning",
                "optimization_data": learning_data
            })
        elif session_type == "handler_evolution":
            # Track handler performance evolution
            handler = learning_data.get("handler_type")
            if handler:
                if handler not in self.stats["handler_improvements"]:
                    self.stats["handler_improvements"][handler] = []
                self.stats["handler_improvements"][handler].append(learning_data)
        
        print(f"🧠 Learning session recorded: {session_type} with {len(learning_data)} data points")

    def correlate_brain_learning_with_performance(self) -> Dict[str, Any]:
        """Analyze correlation between brain learning events and automation performance"""
        
        correlation_analysis = {
            "learning_to_automation_ratio": 0.0,
            "pattern_discovery_effectiveness": 0.0,
            "strategy_optimization_impact": 0.0,
            "confidence_calibration_benefit": 0.0,
            "overall_brain_learning_effectiveness": 0.0
        }
        
        total_learning_events = len(self.learning_events)
        if total_learning_events == 0:
            return correlation_analysis
        
        # Calculate learning to automation ratio
        automation_events = [e for e in self.learning_events if e.get("event_type") == "successful_automation"]
        if total_learning_events > 0:
            correlation_analysis["learning_to_automation_ratio"] = len(automation_events) / total_learning_events
        
        # Calculate pattern discovery effectiveness
        pattern_events = len(self.pattern_discoveries)
        if pattern_events > 0 and self.total_questions > 0:
            correlation_analysis["pattern_discovery_effectiveness"] = pattern_events / self.total_questions
        
        # Calculate strategy optimization impact
        strategy_events = [e for e in self.learning_events if e.get("strategy_name")]
        successful_strategies = [e for e in strategy_events if e.get("success", False)]
        if len(strategy_events) > 0:
            correlation_analysis["strategy_optimization_impact"] = len(successful_strategies) / len(strategy_events)
        
        # Calculate confidence calibration benefit
        calibration_events = [e for e in self.learning_events if e.get("event_type") == "confidence_calibration"]
        positive_calibrations = [e for e in calibration_events if e.get("confidence_change", 0) > 0]
        if len(calibration_events) > 0:
            correlation_analysis["confidence_calibration_benefit"] = len(positive_calibrations) / len(calibration_events)
        
        # Calculate overall effectiveness
        metrics = [
            correlation_analysis["learning_to_automation_ratio"],
            correlation_analysis["pattern_discovery_effectiveness"], 
            correlation_analysis["strategy_optimization_impact"],
            correlation_analysis["confidence_calibration_benefit"]
        ]
        non_zero_metrics = [m for m in metrics if m > 0]
        if non_zero_metrics:
            correlation_analysis["overall_brain_learning_effectiveness"] = sum(non_zero_metrics) / len(non_zero_metrics)
        
        return correlation_analysis
    
    def record_pattern_discovery(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """Record when Quenito's brain discovers new patterns."""
        discovery = {
            "timestamp": time.time(),
            "pattern_type": pattern_type,
            "pattern_data": pattern_data,
            "discovery_method": "brain_analysis"
        }
        
        self.pattern_discoveries.append(discovery)
        self.stats["question_types_encountered"][pattern_type] = (
            self.stats["question_types_encountered"].get(pattern_type, 0) + 1
        )
        
        print(f"🧠 NEW PATTERN DISCOVERED: {pattern_type}")
    
    def record_brain_improvement(self, improvement_type: str, improvement_data: Dict[str, Any]):
        """Record when Quenito's brain improves its capabilities."""
        improvement = {
            "timestamp": time.time(),
            "improvement_type": improvement_type,
            "improvement_data": improvement_data
        }
        
        self.brain_improvements.append(improvement)
        print(f"🧠 BRAIN IMPROVEMENT: {improvement_type}")
    
    def get_automation_rate(self) -> float:
        """Calculate automation rate as percentage."""
        if self.total_questions > 0:
            return (self.automated_questions / self.total_questions) * 100
        return 0.0
    
    def get_brain_learning_rate(self) -> float:
        """Calculate brain learning rate (learning events per question)."""
        if self.total_questions > 0:
            return len(self.learning_events) / self.total_questions
        return 0.0
    
    def get_handler_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive handler performance analysis."""
        summary = {}
        
        for handler_type, perf_data in self.handler_performance.items():
            attempts = perf_data["attempts"]
            successes = perf_data["successes"]
            success_rate = (successes / attempts * 100) if attempts > 0 else 0.0
            
            confidence_scores = perf_data["confidence_scores"]
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            # Calculate trend
            if len(confidence_scores) >= 5:
                recent_avg = sum(confidence_scores[-5:]) / 5
                older_avg = sum(confidence_scores[-10:-5]) / 5 if len(confidence_scores) >= 10 else avg_confidence
                
                if recent_avg > older_avg + 0.05:
                    trend = "improving"
                elif recent_avg < older_avg - 0.05:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            summary[handler_type] = {
                "success_rate": success_rate,
                "average_confidence": avg_confidence,
                "total_attempts": attempts,
                "trend": trend
            }
        
        return summary
    
    def get_brain_evolution_metrics(self) -> Dict[str, Any]:
        """Get brain evolution and learning metrics including Step 3 correlations."""
        
        # Get correlation analysis
        correlation_data = self.correlate_brain_learning_with_performance()
        
        return {
            "total_learning_events": len(self.learning_events),
            "pattern_discoveries": len(self.pattern_discoveries),
            "brain_improvements": len(self.brain_improvements),
            "confidence_evolution_points": len(self.confidence_evolution),
            "automation_improvement": self.session_data.get("automation_improvement", 0.0),
            "new_patterns_learned": self.session_data.get("new_patterns_learned", 0),
            "brain_intelligence_progression": {
                "start": self.session_data.get("brain_intelligence_start", {}),
                "end": self.session_data.get("brain_intelligence_end", {})
            },
            # 🚀 NEW Step 3 correlation metrics
            "brain_learning_correlations": correlation_data,
            "learning_effectiveness_score": correlation_data.get("overall_brain_learning_effectiveness", 0.0),
            "strategy_optimization_events": len([e for e in self.learning_events if e.get("strategy_name")]),
            "confidence_calibration_events": len([e for e in self.learning_events if e.get("event_type") == "confidence_calibration"]),
            "pattern_learning_sessions": len([e for e in self.learning_events if e.get("session_type") == "pattern_learning"])
        }
    
    def print_brain_enhanced_summary(self):
        """Print comprehensive brain-enhanced statistics summary with Step 3 metrics."""
        print(f"\n🧠 ===============================================")
        print(f"🧠 BRAIN-ENHANCED SURVEY STATISTICS SUMMARY v2.1")
        print(f"🧠 ===============================================")
        
        # Core metrics
        print(f"\n📊 CORE SURVEY METRICS:")
        print(f"   Questions processed: {self.total_questions}")
        print(f"   Automated: {self.automated_questions}")
        print(f"   Manual interventions: {self.manual_interventions}")
        print(f"   Automation rate: {self.get_automation_rate():.1f}%")
        
        if self.get_total_time() > 0:
            print(f"   Total time: {self.get_total_time()/60:.1f} minutes")
            print(f"   Questions/minute: {self.get_questions_per_minute():.1f}")
        
        # 🧠 Brain learning metrics
        print(f"\n🧠 BRAIN LEARNING METRICS:")
        print(f"   Learning events: {len(self.learning_events)}")
        print(f"   Pattern discoveries: {len(self.pattern_discoveries)}")
        print(f"   Brain improvements: {len(self.brain_improvements)}")
        print(f"   Learning rate: {self.get_brain_learning_rate():.2f} events/question")
        
        # 🚀 NEW Step 3 correlation metrics
        correlation_data = self.correlate_brain_learning_with_performance()
        print(f"\n🚀 BRAIN LEARNING CORRELATIONS (Step 3):")
        print(f"   Learning effectiveness: {correlation_data['overall_brain_learning_effectiveness']:.1%}")
        print(f"   Learning → Automation ratio: {correlation_data['learning_to_automation_ratio']:.2f}")
        print(f"   Pattern discovery rate: {correlation_data['pattern_discovery_effectiveness']:.2f}")
        print(f"   Strategy optimization success: {correlation_data['strategy_optimization_impact']:.1%}")
        print(f"   Confidence calibration benefit: {correlation_data['confidence_calibration_benefit']:.1%}")
        
        # Handler performance
        handler_summary = self.get_handler_performance_summary()
        if handler_summary:
            print(f"\n🎯 HANDLER PERFORMANCE:")
            for handler, metrics in handler_summary.items():
                print(f"   {handler}: {metrics['success_rate']:.1f}% success, "
                      f"{metrics['average_confidence']:.2f} avg confidence, "
                      f"trending {metrics['trend']}")
        
        # Brain evolution
        evolution = self.get_brain_evolution_metrics()
        print(f"\n🚀 BRAIN EVOLUTION:")
        print(f"   Automation improvement: +{evolution['automation_improvement']:.1f}%")
        print(f"   New patterns learned: {evolution['new_patterns_learned']}")
        print(f"   Strategy optimization events: {evolution['strategy_optimization_events']}")
        print(f"   Confidence calibration events: {evolution['confidence_calibration_events']}")
        
        brain_start = evolution['brain_intelligence_progression']['start']
        brain_end = evolution['brain_intelligence_progression']['end']
        
        if brain_start and brain_end:
            start_level = brain_start.get('brain_intelligence_level', 'Unknown')
            end_level = brain_end.get('brain_intelligence_level', 'Unknown')
            print(f"   Intelligence evolution: {start_level} → {end_level}")
        
        print(f"\n🧠 ===============================================")
    
    # Legacy compatibility methods
    def get_total_questions(self) -> int:
        return self.total_questions
    
    def get_automated_questions(self) -> int:
        return self.automated_questions
    
    def get_manual_interventions(self) -> int:
        return self.manual_interventions
    
    def get_total_time(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def get_questions_per_minute(self) -> float:
        total_time = self.get_total_time()
        if total_time > 0 and self.total_questions > 0:
            return (self.total_questions / total_time) * 60
        return 0.0
    
    def get_stats(self) -> dict:
        """Get all statistics including brain metrics."""
        brain_stats = self.get_brain_evolution_metrics()
        self.stats.update(brain_stats)
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset all statistics including brain metrics."""
        self.survey_started = False
        self.survey_ended = False
        self.start_time = None
        self.end_time = None
        self.total_questions = 0
        self.automated_questions = 0
        self.manual_interventions = 0
        
        # Reset brain metrics
        self.handler_performance = {}
        self.confidence_evolution = []
        self.learning_events = []
        self.pattern_discoveries = []
        self.brain_improvements = []
        
        self.session_data = {
            "session_id": f"stats_session_{int(time.time())}",
            "brain_intelligence_start": None,
            "brain_intelligence_end": None,
            "automation_improvement": 0.0,
            "new_patterns_learned": 0,
            "confidence_calibrations": 0
        }
        
        self.stats = {
            "total_questions": 0,
            "automated_questions": 0,
            "manual_interventions": 0,
            "research_performed": 0,
            "start_time": None,
            "end_time": None,
            "question_types_encountered": {},
            "brain_learning_events": 0,
            "handler_improvements": {},
            "confidence_evolution": [],
            "intelligence_progression": []
        }
        
        print("🔄 Brain-enhanced survey statistics reset")
        print("🧠 Ready for new brain learning session")


# Legacy compatibility class
class SurveyStats(BrainEnhancedSurveyStats):
    """Legacy compatibility wrapper for existing code."""
    
    def __init__(self):
        super().__init__(knowledge_base=None)
        print("📊 Legacy SurveyStats initialized (consider upgrading to BrainEnhancedSurveyStats)")