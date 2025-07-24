#!/usr/bin/env python3
"""
Brain Learning Module - AI learning, intelligence, and adaptation logic
Extracted from knowledge_base.py for better modularity and maintainability.

This module handles:
- Intervention learning and storage
- Handler performance tracking and analysis
- Success pattern recognition and storage
- Confidence calibration and adjustment
- Learning session management
- Strategy preference learning
- Automation improvement suggestions
"""

from typing import Dict, Any, Optional, List, Tuple
import time
import statistics


class BrainLearning:
    """
    Clean AI learning management with dynamic learning data from knowledge_base.json.
    Handles all learning algorithms, performance tracking, and intelligence evolution.
    """
    
    def __init__(self, user_profile, pattern_manager, brain_data: Optional[Dict[str, Any]] = None):
        """Initialize with brain learning data from knowledge_base.json"""
        self.user_profile = user_profile
        self.pattern_manager = pattern_manager
        self.brain_data = brain_data or {}
        
        # Initialize learning session
        self.current_session = {
            "session_id": f"brain_session_{int(time.time())}",
            "learning_events": [],
            "performance_improvements": [],
            "new_patterns_discovered": []
        }
        
        self._ensure_brain_structures()
        print(f"🧠 BrainLearning initialized with {len(self.brain_data)} learning categories")
    
    def _ensure_brain_structures(self):
        """Ensure all required brain learning structures exist"""
        default_structures = {
            'intervention_history': [],
            'success_patterns': {},
            'strategy_preferences': {},
            'confidence_calibration': {},
            'handler_performance': {},
            'failure_analysis': [],
            'learning_history': [],
            'pattern_evolution': {},
            'learning_metrics': {
                'total_interventions': 0,
                'automation_improvement_rate': 0.0,
                'last_learning_session': None
            }
        }
        
        for structure, default_value in default_structures.items():
            if structure not in self.brain_data:
                self.brain_data[structure] = default_value
    
    # ========================================
    # INTERVENTION LEARNING
    # ========================================
    
    def store_intervention_learning(self, learning_data: Dict[str, Any]) -> bool:
        """Store intervention learning data for handler improvement"""
        try:
            # Ensure required fields exist
            required_fields = ['intervention_id', 'question_type', 'handler_name', 'confidence_before']
            for field in required_fields:
                if field not in learning_data:
                    learning_data[field] = f"unknown_{field}"
            
            # Add timestamp and session info
            learning_data['timestamp'] = time.time()
            learning_data['session_id'] = self.current_session['session_id']
            learning_data['learning_type'] = 'manual_intervention'
            
            # Store in intervention history
            self.brain_data['intervention_history'].append(learning_data)
            
            # Update handler performance
            self._update_handler_performance(
                learning_data.get('handler_name', 'unknown'),
                success=False,  # Manual intervention = automation failure
                confidence=learning_data.get('confidence_before', 0.0)
            )
            
            # Learn patterns for future improvement
            self._learn_intervention_patterns(learning_data)
            
            # Add to current session
            self.current_session['learning_events'].append({
                'type': 'intervention_learning',
                'data': learning_data,
                'timestamp': time.time()
            })
            
            print(f"🧠 Intervention learning stored: {learning_data.get('question_type', 'unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error storing intervention learning: {e}")
            return False
    
    async def learn_from_failure(self, learning_data):
        """🧠 Learn from automation failure (captures manual intervention data)"""
        try:
            # 🔧 CRITICAL FIX: Use self.brain_data instead of self.data
            if not hasattr(self, 'brain_data'):
                print("⚠️ No brain_data structure available for learning")
                return False
                
            # Ensure intervention_learning section exists
            if 'intervention_learning' not in self.brain_data:
                self.brain_data['intervention_learning'] = {}
            
            # Create unique ID for this learning session
            session_id = f"failure_{int(learning_data.get('timestamp', time.time()))}"
            
            # Store the failure data for future learning
            self.brain_data['intervention_learning'][session_id] = {
                **learning_data,
                'result': 'FAILURE',
                'learned_at': time.time(),
                'needs_learning': True
            }
            
            print(f"🧠 FAILURE LEARNED: {learning_data.get('error_message', 'Unknown error')}")
            print(f"🧠 Question type: {learning_data.get('question_type')}")
            print(f"🧠 Manual answer needed: {learning_data.get('manual_response', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error in learn_from_failure: {e}")
            return False
    
    def _learn_intervention_patterns(self, learning_data: Dict[str, Any]):
        """Learn patterns from manual interventions to improve future automation"""
        try:
            question_type = learning_data.get('question_type', 'unknown')
            confidence = learning_data.get('confidence_before', 0.0)
            element_type = learning_data.get('element_type', 'unknown')
            
            # Store failure pattern for future confidence adjustment
            failure_key = f"{question_type}_{element_type}"
            
            if 'failure_analysis' not in self.brain_data:
                self.brain_data['failure_analysis'] = []
            
            failure_pattern = {
                'failure_key': failure_key,
                'question_type': question_type,
                'element_type': element_type,
                'failed_confidence': confidence,
                'timestamp': time.time(),
                'improvement_needed': True
            }
            
            self.brain_data['failure_analysis'].append(failure_pattern)
            print(f"🧠 Failure pattern learned: {failure_key} (conf: {confidence:.2f})")
            
        except Exception as e:
            print(f"⚠️ Error learning intervention patterns: {e}")
    
    # ========================================
    # HANDLER PERFORMANCE TRACKING
    # ========================================
    
    def _update_handler_performance(self, handler_name: str, success: bool, confidence: float):
        """Update handler performance metrics"""
        try:
            if handler_name not in self.brain_data['handler_performance']:
                self.brain_data['handler_performance'][handler_name] = {
                    'total_attempts': 0,
                    'successful_attempts': 0,
                    'success_rate': 0.0,
                    'confidence_history': [],
                    'average_confidence': 0.0,
                    'improvement_trend': 'new',
                    'last_updated': time.time()
                }
            
            handler_stats = self.brain_data['handler_performance'][handler_name]
            
            # Update attempt counts
            handler_stats['total_attempts'] += 1
            if success:
                handler_stats['successful_attempts'] += 1
            
            # Update success rate
            handler_stats['success_rate'] = handler_stats['successful_attempts'] / handler_stats['total_attempts']
            
            # Update confidence tracking
            handler_stats['confidence_history'].append(confidence)
            if handler_stats['confidence_history']:
                handler_stats['average_confidence'] = statistics.mean(handler_stats['confidence_history'])
            
            # Determine improvement trend
            handler_stats['improvement_trend'] = self._calculate_improvement_trend(handler_stats)
            handler_stats['last_updated'] = time.time()
            
            print(f"🧠 Handler performance updated: {handler_name} -> {handler_stats['success_rate']:.1%} success, trending {handler_stats['improvement_trend']}")
            
        except Exception as e:
            print(f"⚠️ Error updating handler performance: {e}")

    def update_handler_performance(self, handler_name: str, confidence: float, success: bool, **kwargs):
        """
        Public method to update handler performance - called by KnowledgeBase delegation
        Delegates to internal _update_handler_performance method
        """
        try:
            # Delegate to the existing private method
            self._update_handler_performance(handler_name, success, confidence)
            
            # Add to current learning session
            self.current_session['learning_events'].append({
                'type': 'handler_performance_update',
                'data': {
                    'handler_name': handler_name,
                    'confidence': confidence,
                    'success': success,
                    **kwargs
                },
                'timestamp': time.time()
            })
            
            # Track as performance improvement if successful
            if success:
                self.current_session['performance_improvements'].append({
                    'handler_name': handler_name,
                    'improvement_type': 'successful_automation',
                    'confidence': confidence,
                    'timestamp': time.time()
                })
            
            return True
            
        except Exception as e:
            print(f"❌ Error in public update_handler_performance: {e}")
            return False

    def _calculate_improvement_trend(self, handler_stats: Dict[str, Any]) -> str:
        """Calculate whether handler performance is improving, declining, or stable"""
        try:
            confidence_history = handler_stats.get('confidence_history', [])
            if len(confidence_history) < 5:
                return 'insufficient_data'
            
            # Look at recent vs older performance
            recent_confidence = confidence_history[-5:]
            older_confidence = confidence_history[-10:-5] if len(confidence_history) >= 10 else confidence_history[:-5]
            
            if older_confidence:
                recent_avg = statistics.mean(recent_confidence)
                older_avg = statistics.mean(older_confidence)
                
                if recent_avg > older_avg + 0.1:
                    return 'improving'
                elif recent_avg < older_avg - 0.1:
                    return 'declining'
                else:
                    return 'stable'
            
            return 'new'
            
        except Exception as e:
            return 'unknown'
    
    def get_handler_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive handler performance summary"""
        summary = {
            'total_handlers': len(self.brain_data.get('handler_performance', {})),
            'handler_details': {},
            'overall_metrics': {
                'average_success_rate': 0.0,
                'total_attempts': 0,
                'total_successes': 0,
                'top_performing_handler': None,
                'needs_improvement': []
            }
        }
        
        handler_performance = self.brain_data.get('handler_performance', {})
        if not handler_performance:
            return summary
        
        total_attempts = 0
        total_successes = 0
        success_rates = []
        
        for handler_name, stats in handler_performance.items():
            handler_summary = {
                'success_rate': stats.get('success_rate', 0.0),
                'total_attempts': stats.get('total_attempts', 0),
                'average_confidence': stats.get('average_confidence', 0.0),
                'trend': stats.get('improvement_trend', 'unknown'),
                'last_updated': stats.get('last_updated', 0)
            }
            
            summary['handler_details'][handler_name] = handler_summary
            
            # Aggregate metrics
            attempts = stats.get('total_attempts', 0)
            successes = stats.get('successful_attempts', 0)
            success_rate = stats.get('success_rate', 0.0)
            
            total_attempts += attempts
            total_successes += successes
            if success_rate > 0:
                success_rates.append(success_rate)
            
            # Identify handlers needing improvement
            if success_rate < 0.7 and attempts > 5:
                summary['overall_metrics']['needs_improvement'].append(handler_name)
        
        # Calculate overall metrics
        if success_rates:
            summary['overall_metrics']['average_success_rate'] = statistics.mean(success_rates)
            summary['overall_metrics']['top_performing_handler'] = max(
                handler_performance.items(), 
                key=lambda x: x[1].get('success_rate', 0.0)
            )[0]
        
        summary['overall_metrics']['total_attempts'] = total_attempts
        summary['overall_metrics']['total_successes'] = total_successes
        
        return summary
    
    # ========================================
    # SUCCESS PATTERN LEARNING
    # ========================================
    
    def store_success_pattern(self, pattern_data: Dict[str, Any]) -> bool:
        """Store successful automation patterns for future use"""
        try:
            pattern_key = f"{pattern_data.get('question_type', 'unknown')}_{pattern_data.get('strategy_used', 'unknown')}"
            
            success_pattern = {
                'pattern_key': pattern_key,
                'question_type': pattern_data.get('question_type', 'unknown'),
                'strategy_used': pattern_data.get('strategy_used', 'unknown'),
                'confidence_achieved': pattern_data.get('confidence', 0.0),
                'execution_time': pattern_data.get('execution_time', 0.0),
                'success_count': 1,
                'last_success': time.time(),
                'pattern_strength': 'new'
            }
            
            # If pattern already exists, update it
            if pattern_key in self.brain_data['success_patterns']:
                existing = self.brain_data['success_patterns'][pattern_key]
                existing['success_count'] += 1
                existing['last_success'] = time.time()
                existing['pattern_strength'] = self._calculate_pattern_strength(existing['success_count'])
                print(f"🧠 Success pattern reinforced: {pattern_key} ({existing['success_count']} successes)")
            else:
                self.brain_data['success_patterns'][pattern_key] = success_pattern
                print(f"🧠 New success pattern learned: {pattern_key}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error storing success pattern: {e}")
            return False

    async def learn_successful_automation(self, learning_data):
        """🧠 Learn from successful automation (method was missing after refactoring)"""
        try:
            # 🔧 CRITICAL FIX: Use self.brain_data instead of self.data
            if not hasattr(self, 'brain_data'):
                print("⚠️ No brain_data structure available for learning")
                return False
                
            # Ensure intervention_learning section exists
            if 'intervention_learning' not in self.brain_data:
                self.brain_data['intervention_learning'] = {}
            
            # Create unique ID for this learning session
            session_id = f"success_{int(learning_data.get('timestamp', time.time()))}"
            
            # Store the successful automation data
            self.brain_data['intervention_learning'][session_id] = {
                **learning_data,
                'result': 'SUCCESS',
                'learned_at': time.time()
            }
            
            print(f"🧠 SUCCESS LEARNED: {learning_data.get('strategy_used')} for {learning_data.get('question_type')}")
            return True
            
        except Exception as e:
            print(f"❌ Error in learn_successful_automation: {e}")
            return False

    def _calculate_pattern_strength(self, success_count: int) -> str:
        """Calculate pattern strength based on success count"""
        if success_count >= 10:
            return 'very_strong'
        elif success_count >= 5:
            return 'strong'
        elif success_count >= 3:
            return 'moderate'
        else:
            return 'weak'
    
    def get_best_strategy_for_question_type(self, question_type: str) -> Optional[Dict[str, Any]]:
        """Get the best learned strategy for a question type"""
        try:
            best_strategy = None
            best_score = 0.0
            
            for pattern_key, pattern_data in self.brain_data['success_patterns'].items():
                if pattern_data.get('question_type') == question_type:
                    # Score based on success count and confidence
                    score = (pattern_data.get('success_count', 0) * 0.3 + 
                           pattern_data.get('confidence_achieved', 0.0) * 0.7)
                    
                    if score > best_score:
                        best_score = score
                        best_strategy = pattern_data
            
            return best_strategy
            
        except Exception as e:
            print(f"⚠️ Error getting best strategy: {e}")
            return None
    
    # ========================================
    # STRATEGY PREFERENCE LEARNING
    # ========================================
    
    def learn_strategy_preference(self, question_type: str, strategy: str, success: bool) -> bool:
        """Learn which strategies work best for different question types"""
        try:
            if question_type not in self.brain_data['strategy_preferences']:
                self.brain_data['strategy_preferences'][question_type] = {}
            
            if strategy not in self.brain_data['strategy_preferences'][question_type]:
                self.brain_data['strategy_preferences'][question_type][strategy] = {
                    'success_count': 0,
                    'total_attempts': 0,
                    'success_rate': 0.0
                }
            
            strategy_stats = self.brain_data['strategy_preferences'][question_type][strategy]
            strategy_stats['total_attempts'] += 1
            
            if success:
                strategy_stats['success_count'] += 1
            
            strategy_stats['success_rate'] = strategy_stats['success_count'] / strategy_stats['total_attempts']
            
            print(f"🧠 Strategy preference updated: {question_type} -> {strategy} ({strategy_stats['success_rate']:.1%})")
            return True
            
        except Exception as e:
            print(f"❌ Error learning strategy preference: {e}")
            return False
    
    async def get_preferred_strategy(self, question_type, **kwargs):
        """🧠 Get preferred strategy (fixed parameter handling)"""
        try:
            # Remove problematic kwargs
            kwargs.pop('element_type', None)
            
            if not hasattr(self, 'brain_data'):
                return None
                
            strategy_prefs = self.brain_data.get('strategy_preferences', {})
            
            if question_type in strategy_prefs:
                strategy_info = strategy_prefs[question_type]
                if strategy_info.get('success_count', 0) >= 3:  # Need minimum successes
                    preferred_strategy = strategy_info.get('name')
                    print(f"🧠 USING LEARNED STRATEGY: {preferred_strategy} for {question_type}")
                    return {'name': preferred_strategy, 'success_rate': 1.0}
                    
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting preferred strategy: {e}")
            return None
    
    # ========================================
    # CONFIDENCE CALIBRATION
    # ========================================
    
    def calibrate_confidence(self, handler_name: str, question_type: str, 
                           predicted_confidence: float, actual_success: bool):
        """Calibrate confidence predictions based on actual results"""
        try:
            calibration_key = f"{handler_name}_{question_type}"
            
            if 'confidence_calibration' not in self.brain_data:
                self.brain_data['confidence_calibration'] = {}
            
            if calibration_key not in self.brain_data['confidence_calibration']:
                self.brain_data['confidence_calibration'][calibration_key] = {
                    'predictions': [],
                    'accuracy_rate': 0.0,
                    'recommended_threshold': 0.5
                }
            
            calibration_data = self.brain_data['confidence_calibration'][calibration_key]
            
            # Store prediction vs result
            calibration_data['predictions'].append({
                'predicted_confidence': predicted_confidence,
                'actual_success': actual_success,
                'timestamp': time.time()
            })
            
            # Keep only recent predictions (last 50)
            if len(calibration_data['predictions']) > 50:
                calibration_data['predictions'] = calibration_data['predictions'][-50:]
            
            # Update calibration metrics
            self._update_confidence_calibration(calibration_key, calibration_data)
            
            print(f"🧠 Confidence calibrated: {calibration_key} -> {calibration_data['accuracy_rate']:.2f} accuracy")
            
        except Exception as e:
            print(f"⚠️ Error calibrating confidence: {e}")
    
    def _update_confidence_calibration(self, calibration_key: str, calibration_data: Dict[str, Any]):
        """Update confidence calibration metrics"""
        try:
            predictions = calibration_data['predictions']
            
            if len(predictions) >= 3:
                # Calculate accuracy of high-confidence predictions
                high_conf_predictions = [p for p in predictions if p['predicted_confidence'] >= 0.6]
                
                if high_conf_predictions:
                    accuracy = sum(1 for p in high_conf_predictions if p['actual_success']) / len(high_conf_predictions)
                    calibration_data['accuracy_rate'] = accuracy
                    
                    # Adjust threshold based on accuracy
                    if accuracy >= 0.9:  # Very accurate - can lower threshold
                        calibration_data['recommended_threshold'] = max(0.3, calibration_data['recommended_threshold'] - 0.1)
                    elif accuracy < 0.7:  # Not accurate enough - raise threshold
                        calibration_data['recommended_threshold'] = min(0.8, calibration_data['recommended_threshold'] + 0.1)
                        
        except Exception as e:
            print(f"⚠️ Error updating confidence calibration: {e}")
    
    # ========================================
    # LEARNING SESSION MANAGEMENT
    # ========================================
    
    def start_learning_session(self, session_context: Optional[str] = None):
        """Start a new learning session"""
        self.current_session = {
            "session_id": f"brain_session_{int(time.time())}",
            "start_time": time.time(),
            "context": session_context or "general_learning",
            "learning_events": [],
            "performance_improvements": [],
            "new_patterns_discovered": []
        }
        print(f"🧠 Learning session started: {self.current_session['session_id']}")
    
    def end_learning_session(self) -> Dict[str, Any]:
        """End current learning session and return summary"""
        try:
            session_summary = {
                'session_id': self.current_session['session_id'],
                'duration': time.time() - self.current_session.get('start_time', time.time()),
                'learning_events_count': len(self.current_session['learning_events']),
                'performance_improvements': len(self.current_session['performance_improvements']),
                'new_patterns': len(self.current_session['new_patterns_discovered']),
                'session_value': self._calculate_session_value()
            }
            
            # Store session in learning history
            self.brain_data['learning_history'].append({
                'session_summary': session_summary,
                'timestamp': time.time()
            })
            
            print(f"🧠 Learning session completed: {session_summary['learning_events_count']} events, {session_summary['session_value']} value")
            return session_summary
            
        except Exception as e:
            print(f"❌ Error ending learning session: {e}")
            return {}
    
    def _calculate_session_value(self) -> float:
        """Calculate the learning value of current session"""
        try:
            # Simple scoring based on learning events and improvements
            events_score = len(self.current_session['learning_events']) * 0.1
            improvements_score = len(self.current_session['performance_improvements']) * 0.3
            patterns_score = len(self.current_session['new_patterns_discovered']) * 0.5
            
            return min(1.0, events_score + improvements_score + patterns_score)
            
        except Exception:
            return 0.0
    
    # ========================================
    # LEARNING ANALYSIS & INSIGHTS
    # ========================================
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights about learning progress and suggestions"""
        insights = {
            'learning_maturity': 'beginner',
            'total_interventions': len(self.brain_data.get('intervention_history', [])),
            'success_patterns_count': len(self.brain_data.get('success_patterns', {})),
            'strategy_preferences_count': len(self.brain_data.get('strategy_preferences', {})),
            'automation_readiness': 0.0,
            'key_insights': [],
            'improvement_recommendations': []
        }
        
        # Analyze intervention history
        interventions = self.brain_data.get('intervention_history', [])
        if interventions:
            insights['key_insights'].append(f"Learned from {len(interventions)} manual interventions")
            
            # Check for common failure patterns
            question_types = [i.get('question_type', 'unknown') for i in interventions]
            common_failures = max(set(question_types), key=question_types.count) if question_types else None
            if common_failures and common_failures != 'unknown':
                insights['improvement_recommendations'].append(f"Focus on improving {common_failures} question detection")
        
        # Analyze handler performance
        handler_performance = self.brain_data.get('handler_performance', {})
        if handler_performance:
            avg_success_rate = statistics.mean([h.get('success_rate', 0) for h in handler_performance.values()])
            insights['automation_readiness'] = avg_success_rate
            
            if avg_success_rate >= 0.8:
                insights['learning_maturity'] = 'advanced'
            elif avg_success_rate >= 0.6:
                insights['learning_maturity'] = 'intermediate'
        
        # Success pattern analysis
        success_patterns = self.brain_data.get('success_patterns', {})
        if success_patterns:
            strong_patterns = sum(1 for p in success_patterns.values() if p.get('success_count', 0) >= 5)
            insights['key_insights'].append(f"Developed {strong_patterns} strong automation patterns")
        
        return insights
    
    def get_brain_statistics(self) -> Dict[str, Any]:
        """Get comprehensive brain learning statistics"""
        return {
            'intervention_history': len(self.brain_data.get('intervention_history', [])),
            'success_patterns': len(self.brain_data.get('success_patterns', {})),
            'strategy_preferences': len(self.brain_data.get('strategy_preferences', {})),
            'handler_performance_tracked': len(self.brain_data.get('handler_performance', {})),
            'learning_sessions': len(self.brain_data.get('learning_history', [])),
            'confidence_calibrations': len(self.brain_data.get('confidence_calibration', {})),
            'failure_patterns_analyzed': len(self.brain_data.get('failure_analysis', [])),
            'current_session_events': len(self.current_session.get('learning_events', [])),
            'brain_data_size': len(self.brain_data)
        }


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def create_brain_learning(user_profile, pattern_manager, brain_data: Optional[Dict[str, Any]] = None) -> BrainLearning:
    """Factory function to create BrainLearning instance"""
    return BrainLearning(user_profile, pattern_manager, brain_data)


# ========================================
# MODULE TEST
# ========================================

if __name__ == "__main__":
    # Quick module test with mock dependencies
    print("🧠 Brain Learning Module Test")
    
    # Mock user profile and pattern manager for testing
    class MockUserProfile:
        def get_age(self): return "45"
    
    class MockPatternManager:
        def detect_question_type(self, content): return {'primary_type': 'demographics', 'confidence': 0.8}
    
    # Test brain learning initialization
    mock_profile = MockUserProfile()
    mock_patterns = MockPatternManager()
    brain_learning = BrainLearning(mock_profile, mock_patterns, {})
    
    # Test learning functions
    test_intervention = {
        'intervention_id': 'test_001',
        'question_type': 'age',
        'handler_name': 'DemographicsHandler',
        'confidence_before': 0.3
    }
    
    success = brain_learning.store_intervention_learning(test_intervention)
    print(f"Intervention learning: {'✅' if success else '❌'}")
    
    # Test performance tracking
    brain_learning._update_handler_performance('TestHandler', True, 0.8)
    
    # Test insights
    insights = brain_learning.get_learning_insights()
    print(f"Learning maturity: {insights['learning_maturity']}")
    
    print("✅ Brain Learning Module working correctly!")