"""
🧠 Enhanced Knowledge Base with Digital Brain Integration v2.1
Handles loading, saving, and accessing the survey automation knowledge base.
NOW WITH BRAIN LEARNING CAPABILITIES - Quenito gets smarter with every interaction!

New Digital Brain Features:
- ✅ Auto-Learning from interventions  
- ✅ Pattern recognition improvement
- ✅ Confidence calibration evolution
- ✅ Handler performance tracking
- ✅ Question mapping expansion
- ✅ Success pattern storage
- ✅ AUTOMATION SUCCESS LEARNING - NEW!
- ✅ STRATEGY PREFERENCE LEARNING - NEW!
"""

import json
import os
import time
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path


class KnowledgeBase:
    """
    🧠 Enhanced Knowledge Base with Digital Brain Integration
    Manages the survey automation knowledge base with user preferences,
    question patterns, response strategies, AND LEARNING CAPABILITIES.
    
    The brain gets smarter with every interaction!
    """
    
    def __init__(self, knowledge_base_path="data/knowledge_base.json"):
        self.path = knowledge_base_path
        self.data = {}
        
        # 🧠 Brain learning tracking
        self.learning_session = {
            "session_id": f"brain_session_{int(time.time())}",
            "learning_events": [],
            "performance_improvements": [],
            "new_patterns_discovered": []
        }
        
        self.load()
        
        # Initialize brain learning structures if missing
        self._ensure_brain_structures()
    
    def load(self):
        """Load the knowledge base from JSON file."""
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                print("✅ Knowledge base loaded successfully")
                print(f"📊 Loaded patterns for: {list(self.data.get('question_patterns', {}).keys())}")
                
                # 🧠 Brain status report
                brain_data = self.data.get('brain_learning', {})
                total_interventions = len(brain_data.get('intervention_history', []))
                success_patterns = len(brain_data.get('success_patterns', {}))
                strategy_preferences = len(brain_data.get('strategy_preferences', {}))
                handler_performance = len(brain_data.get('handler_performance', {}))
                print(f"🧠 Brain Status: {total_interventions} interventions, {success_patterns} success patterns, {strategy_preferences} strategy preferences, {handler_performance} handler metrics")
                
            else:
                print(f"⚠️ Knowledge base file not found: {self.path}")
                print("🔧 Creating minimal fallback knowledge base")
                self._create_fallback_knowledge_base()
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            print("🔧 Creating minimal fallback knowledge base")
            self._create_fallback_knowledge_base()
    
    def save(self):
        """Save the knowledge base back to the JSON file with brain learning data."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            
            # 🧠 Add current learning session data before saving
            if 'brain_learning' not in self.data:
                self.data['brain_learning'] = {}
            
            # Store learning session data
            self.data['brain_learning']['last_session'] = self.learning_session
            self.data['brain_learning']['last_updated'] = time.time()
            
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            print("💾 Knowledge base updated and saved")
            print(f"🧠 Brain learning data updated with {len(self.learning_session['learning_events'])} new events")
            
            # 🧠 Report brain learning status after save
            brain_data = self.data.get('brain_learning', {})
            success_patterns = len(brain_data.get('success_patterns', {}))
            handler_performance = len(brain_data.get('handler_performance', {}))

            # 🔧 FIXED: Check both locations for strategy preferences
            strategy_preferences_brain = len(brain_data.get('strategy_preferences', {}))
            strategy_preferences_root = len(self.data.get('strategy_preferences', {}))
            strategy_preferences = max(strategy_preferences_brain, strategy_preferences_root)

            print(f"🧠 Brain Status After Save: {success_patterns} patterns, {handler_performance} handlers, {strategy_preferences} strategy preferences")
            
            return True
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
            return False

    async def save_knowledge_base(self) -> bool:
        """💾 FIXED: Async wrapper for existing save method"""
        try:
            return self.save()  # FIXED: Removed 'await' since save() is not async
        except Exception as e:
            print(f"❌ Error in async save wrapper: {e}")
            return False

    # ========================================
    # 🧠 NEW: AUTOMATION SUCCESS LEARNING METHODS
    # ========================================
    
    async def learn_successful_automation(self, learning_data: dict) -> bool:
        """🧠 FIXED: Learn from successful automation with proper data structure"""
        try:
            # Create learning session entry
            if 'brain_learning' not in self.data:
                self.data['brain_learning'] = {}
            
            if 'last_session' not in self.data['brain_learning']:
                self.data['brain_learning']['last_session'] = {
                    'learning_events': [],
                    'session_id': f'session_{int(time.time())}',
                    'start_time': time.time()
                }
            
            # Add learning event to current session
            learning_event = {
                'timestamp': learning_data.get('timestamp', time.time()),
                'session_id': learning_data.get('session_id', 'unknown'),
                'question_type': learning_data.get('question_type', 'unknown'),
                'question_text': learning_data.get('question_text', ''),
                'strategy_used': learning_data.get('strategy_used', ''),
                'execution_time': learning_data.get('execution_time', 0.0),
                'confidence_score': learning_data.get('confidence_score', 0.0),  # FIXED: Use confidence_score
                'response_value': learning_data.get('response_value', ''),
                'result': learning_data.get('result', 'SUCCESS'),
                'element_type': learning_data.get('element_type', 'unknown'),
                'automation_success': learning_data.get('automation_success', True)
            }
            
            # Add to session events
            self.data['brain_learning']['last_session']['learning_events'].append(learning_event)
            
            # Store successful strategy
            question_type = learning_data.get('question_type', 'unknown')
            strategy = learning_data.get('strategy_used', '')
            
            if strategy and question_type != 'unknown':
                if 'strategy_preferences' not in self.data:
                    self.data['strategy_preferences'] = {}
                
                if question_type not in self.data['strategy_preferences']:
                    self.data['strategy_preferences'][question_type] = {
                        'name': strategy,
                        'success_count': 0,
                        'total_attempts': 0
                    }
                
                # Update strategy stats
                self.data['strategy_preferences'][question_type]['success_count'] += 1
                self.data['strategy_preferences'][question_type]['total_attempts'] += 1
                
                success_rate = self.data['strategy_preferences'][question_type]['success_count'] / \
                            self.data['strategy_preferences'][question_type]['total_attempts']
                
                print(f"🧠 STRATEGY LEARNED: {question_type} → {strategy} ({success_rate:.1%} success)")
            
            # Save to knowledge base
            await self.save_knowledge_base()
            
            return True
            
        except Exception as e:
            print(f"❌ Error in learn_successful_automation: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def learn_from_failure(self, learning_data: dict) -> bool:
        """🧠 FIXED: Learn from automation failure"""
        try:
            # Add failure event to brain learning
            if 'brain_learning' not in self.data:
                self.data['brain_learning'] = {}
            
            if 'last_session' not in self.data['brain_learning']:
                self.data['brain_learning']['last_session'] = {
                    'learning_events': [],
                    'session_id': f'session_{int(time.time())}',
                    'start_time': time.time()
                }
            
            # Add failure event
            failure_event = {
                'timestamp': learning_data.get('timestamp', time.time()),
                'question_type': learning_data.get('question_type', 'unknown'),
                'error_message': learning_data.get('error_message', ''),
                'confidence_score': learning_data.get('confidence_score', 0.0),
                'result': 'FAILURE',
                'automation_success': False
            }
            
            self.data['brain_learning']['last_session']['learning_events'].append(failure_event)
            
            print(f"🧠 FAILURE LEARNED: {learning_data.get('question_type')} - {learning_data.get('error_message')}")
            
            # Save to knowledge base
            await self.save_knowledge_base()
            
            return True
            
        except Exception as e:
            print(f"❌ Error learning from failure: {e}")
            return False

    async def get_preferred_strategy(self, question_type: str, element_type: str = None) -> Optional[Dict[str, Any]]:
        """🧠 FIXED: Get learned preferred strategy for question type"""
        try:
            # 🔧 FIXED: Check BOTH locations for strategy preferences
            strategy_prefs_brain = self.data.get('brain_learning', {}).get('strategy_preferences', {})
            strategy_prefs_root = self.data.get('strategy_preferences', {})
            
            # Use root level preferences first (where current strategies are stored)
            if question_type in strategy_prefs_root:
                pref = strategy_prefs_root[question_type]
                strategy_info = {
                    'name': pref['name'],
                    'success_rate': (pref.get('success_count', 0) / max(pref.get('total_attempts', 1), 1)),
                    'success_count': pref.get('success_count', 0),
                    'total_attempts': pref.get('total_attempts', 0)
                }
                
                print(f"🧠 STRATEGY RECALLED: {question_type} → {strategy_info['name']} (success rate: {strategy_info['success_rate']:.1%})")
                return strategy_info
            
            # Fallback to brain_learning location
            elif question_type in strategy_prefs_brain:
                pref = strategy_prefs_brain[question_type]
                strategy_info = {
                    'name': pref['preferred_strategy'],
                    'success_rate': pref.get('success_rate', 0.0),
                    'success_count': pref.get('success_count', 0),
                    'avg_execution_time': pref.get('avg_execution_time', 0.0),
                    'last_used': pref.get('last_used')
                }
                
                print(f"🧠 STRATEGY RECALLED: {question_type} → {strategy_info['name']} (success rate: {strategy_info['success_rate']:.1%})")
                return strategy_info
            
            print(f"🧠 No learned strategy for: {question_type}")
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting preferred strategy: {e}")
            return None

    async def _update_handler_performance_detailed(self, learning_data: Dict[str, Any]):
        """Update detailed handler performance metrics"""
        handler_type = "demographics_handler"  # Can be dynamic later
        question_type = learning_data.get('question_type', 'unknown')
        
        if 'handler_performance' not in self.data['brain_learning']:
            self.data['brain_learning']['handler_performance'] = {}
        
        if handler_type not in self.data['brain_learning']['handler_performance']:
            self.data['brain_learning']['handler_performance'][handler_type] = {}
        
        if question_type not in self.data['brain_learning']['handler_performance'][handler_type]:
            self.data['brain_learning']['handler_performance'][handler_type][question_type] = {
                'total_attempts': 0,
                'successful_automations': 0,
                'success_rate': 0.0,
                'avg_confidence': 0.0,
                'confidence_scores': [],
                'execution_times': [],
                'avg_execution_time': 0.0,
                'last_success': None,
                'strategies_used': {}
            }
        
        # Update metrics
        perf = self.data['brain_learning']['handler_performance'][handler_type][question_type]
        perf['total_attempts'] += 1
        perf['successful_automations'] += 1
        perf['success_rate'] = perf['successful_automations'] / perf['total_attempts']
        
        # Update confidence tracking
        confidence = learning_data.get('confidence_score', 0.0)
        perf['confidence_scores'].append(confidence)
        perf['avg_confidence'] = sum(perf['confidence_scores']) / len(perf['confidence_scores'])
        
        # Update execution time tracking
        execution_time = learning_data.get('execution_time', 0.0)
        if execution_time > 0:
            perf['execution_times'].append(execution_time)
            perf['avg_execution_time'] = sum(perf['execution_times']) / len(perf['execution_times'])
        
        perf['last_success'] = learning_data.get('timestamp')
        
        # Track strategy usage
        strategy_used = learning_data.get('strategy_used')
        if strategy_used:
            if strategy_used not in perf['strategies_used']:
                perf['strategies_used'][strategy_used] = 0
            perf['strategies_used'][strategy_used] += 1
        
        print(f"📊 HANDLER PERFORMANCE UPDATED: {handler_type}.{question_type} → {perf['success_rate']:.1%} success rate")

    async def _update_handler_performance_failure(self, learning_data: Dict[str, Any]):
        """Update handler performance metrics for failure case"""
        handler_type = "demographics_handler"
        question_type = learning_data.get('question_type', 'unknown')
        
        if 'handler_performance' not in self.data['brain_learning']:
            self.data['brain_learning']['handler_performance'] = {}
        
        if handler_type not in self.data['brain_learning']['handler_performance']:
            self.data['brain_learning']['handler_performance'][handler_type] = {}
        
        if question_type not in self.data['brain_learning']['handler_performance'][handler_type]:
            self.data['brain_learning']['handler_performance'][handler_type][question_type] = {
                'total_attempts': 0,
                'successful_automations': 0,
                'success_rate': 0.0,
                'failure_count': 0
            }
        
        # Update failure metrics
        perf = self.data['brain_learning']['handler_performance'][handler_type][question_type]
        perf['total_attempts'] += 1
        perf['failure_count'] = perf.get('failure_count', 0) + 1
        perf['success_rate'] = perf.get('successful_automations', 0) / perf['total_attempts']
        
        print(f"📊 FAILURE RECORDED: {handler_type}.{question_type} → {perf['success_rate']:.1%} success rate")

    async def _store_success_pattern_detailed(self, learning_data: Dict[str, Any]):
        """Store detailed successful automation pattern"""
        question_text = learning_data.get('question_text', '').lower()
        pattern_key = self._generate_pattern_key(question_text)
        
        if 'success_patterns' not in self.data['brain_learning']:
            self.data['brain_learning']['success_patterns'] = {}
        
        self.data['brain_learning']['success_patterns'][pattern_key] = {
            "timestamp": learning_data.get('timestamp'),
            "question_text": question_text,
            "question_type": learning_data.get('question_type'),
            "strategy": learning_data.get('strategy_used'),
            "execution_time": learning_data.get('execution_time'),
            "confidence": learning_data.get('confidence_score'),
            "response_value": learning_data.get('response_value'),
            "element_type": learning_data.get('element_type'),
            "usage_count": self.data['brain_learning']['success_patterns'].get(pattern_key, {}).get('usage_count', 0) + 1,
            "success_rate": 1.0  # Will be updated with more data
        }
        
        print(f"🧠 SUCCESS PATTERN STORED: {pattern_key} → {learning_data.get('strategy_used')}")

    async def _update_strategy_preferences_detailed(self, learning_data: Dict[str, Any]):
        """Update detailed strategy preferences based on successful automation"""
        question_type = learning_data.get('question_type')
        strategy_used = learning_data.get('strategy_used')
        execution_time = learning_data.get('execution_time', 0.0)
        
        if not question_type or not strategy_used:
            return
        
        if 'strategy_preferences' not in self.data['brain_learning']:
            self.data['brain_learning']['strategy_preferences'] = {}
        
        if question_type not in self.data['brain_learning']['strategy_preferences']:
            self.data['brain_learning']['strategy_preferences'][question_type] = {
                'preferred_strategy': strategy_used,
                'success_count': 1,
                'total_attempts': 1,
                'success_rate': 1.0,
                'avg_execution_time': execution_time,
                'execution_times': [execution_time] if execution_time > 0 else [],
                'first_success': learning_data.get('timestamp'),
                'last_used': learning_data.get('timestamp'),
                'strategy_history': [strategy_used]
            }
        else:
            pref = self.data['brain_learning']['strategy_preferences'][question_type]
            pref['success_count'] += 1
            pref['total_attempts'] += 1
            pref['success_rate'] = pref['success_count'] / pref['total_attempts']
            pref['preferred_strategy'] = strategy_used  # Update to most recent successful strategy
            pref['last_used'] = learning_data.get('timestamp')
            pref['strategy_history'].append(strategy_used)
            
            # Update average execution time
            if execution_time > 0:
                pref['execution_times'].append(execution_time)
                pref['avg_execution_time'] = sum(pref['execution_times']) / len(pref['execution_times'])
        
        print(f"🎯 STRATEGY PREFERENCE UPDATED: {question_type} → {strategy_used} ({self.data['brain_learning']['strategy_preferences'][question_type]['success_rate']:.1%} success)")

    async def _update_confidence_calibration_detailed(self, learning_data: Dict[str, Any]):
        """Update detailed confidence calibration based on automation success"""
        question_type = learning_data.get('question_type')
        confidence = learning_data.get('confidence_score', 0.0)
        
        if not question_type:
            return
        
        if 'confidence_calibration' not in self.data['brain_learning']:
            self.data['brain_learning']['confidence_calibration'] = {}
        
        if question_type not in self.data['brain_learning']['confidence_calibration']:
            self.data['brain_learning']['confidence_calibration'][question_type] = {
                'predictions': [],
                'success_rate_by_confidence': {},
                'optimal_threshold': 0.3,
                'total_predictions': 0,
                'successful_predictions': 0
            }
        
        # Add new prediction result
        cal_data = self.data['brain_learning']['confidence_calibration'][question_type]
        cal_data['predictions'].append({
            'predicted_confidence': confidence,
            'actual_success': True,  # This is a success case
            'timestamp': learning_data.get('timestamp')
        })
        
        cal_data['total_predictions'] += 1
        cal_data['successful_predictions'] += 1
        
        # Calculate confidence-based success rates
        confidence_bucket = int(confidence * 10) / 10  # Round to nearest 0.1
        if confidence_bucket not in cal_data['success_rate_by_confidence']:
            cal_data['success_rate_by_confidence'][confidence_bucket] = {'successes': 0, 'total': 0}
        
        cal_data['success_rate_by_confidence'][confidence_bucket]['successes'] += 1
        cal_data['success_rate_by_confidence'][confidence_bucket]['total'] += 1
        
        # Update optimal threshold based on performance
        await self._recalibrate_optimal_threshold(question_type)
        
        print(f"🎯 CONFIDENCE CALIBRATED: {question_type} → {confidence:.2f} confidence resulted in SUCCESS")

    async def _recalibrate_optimal_threshold(self, question_type: str):
        """Recalibrate optimal confidence threshold for question type"""
        try:
            cal_data = self.data['brain_learning']['confidence_calibration'][question_type]
            
            if len(cal_data['predictions']) >= 3:  # Need minimum data points
                # Find the lowest confidence that still achieves high success rate
                confidence_buckets = cal_data['success_rate_by_confidence']
                
                # ✅ FIX: Convert all keys to floats before sorting to handle mixed types
                try:
                    sorted_confidence_levels = sorted([float(k) for k in confidence_buckets.keys()])
                except (ValueError, TypeError):
                    # Fallback: use original keys but handle mixed types safely
                    sorted_confidence_levels = []
                    for k in confidence_buckets.keys():
                        try:
                            sorted_confidence_levels.append(float(k))
                        except (ValueError, TypeError):
                            continue
                    sorted_confidence_levels.sort()
                
                # ✅ COMPLETE the for loop with proper logic
                for confidence_level in sorted_confidence_levels:
                    bucket = confidence_buckets[confidence_level]
                    
                    # Calculate success rate for this confidence level
                    if bucket['total'] > 0:
                        success_rate = bucket['successes'] / bucket['total']
                        
                        # If this confidence level has good success rate, it could be our threshold
                        if success_rate >= 0.8 and bucket['total'] >= 2:  # At least 80% success with 2+ attempts
                            # Set threshold slightly below the working level
                            cal_data['optimal_threshold'] = max(0.2, confidence_level - 0.1)
                            print(f"🎯 THRESHOLD UPDATED: {question_type} → {cal_data['optimal_threshold']:.2f} (based on {confidence_level:.1f} success)")
                            break
                else:
                    # If no good threshold found, use conservative default
                    cal_data['optimal_threshold'] = 0.3
                    print(f"🎯 THRESHOLD DEFAULT: {question_type} → 0.3 (insufficient data)")
                    
            print(f"🧠 CONFIDENCE RECALIBRATED: {question_type}")
            
        except Exception as e:
            print(f"❌ Error in _recalibrate_optimal_threshold: {e}")
            # Set safe default on error
            if 'brain_learning' in self.data and 'confidence_calibration' in self.data['brain_learning']:
                if question_type in self.data['brain_learning']['confidence_calibration']:
                    self.data['brain_learning']['confidence_calibration'][question_type]['optimal_threshold'] = 0.3

    def _generate_pattern_key(self, question_text: str) -> str:
        """Generate a key for storing question patterns"""
        # Extract key words for pattern matching
        key_words = []
        question_lower = question_text.lower()
        
        # Age patterns
        if any(word in question_lower for word in ['age', 'old', 'born', 'years']):
            key_words.append('age')
        
        # Gender patterns  
        if any(word in question_lower for word in ['gender', 'male', 'female', 'man', 'woman']):
            key_words.append('gender')
        
        # Location patterns
        if any(word in question_lower for word in ['location', 'state', 'live', 'where', 'region']):
            key_words.append('location')
        
        # Question type patterns
        if any(word in question_lower for word in ['how', 'what', 'which', 'where']):
            if 'how' in question_lower:
                key_words.append('how')
            elif 'what' in question_lower:
                key_words.append('what')
            elif 'which' in question_lower:
                key_words.append('which')
        
        # Create pattern key
        if key_words:
            pattern_key = '_'.join(sorted(key_words))
        else:
            # Fallback to length-based categorization
            if len(question_text) < 30:
                pattern_key = "short_question"
            elif len(question_text) < 60:
                pattern_key = "medium_question"
            else:
                pattern_key = "long_question"
        
        return pattern_key

    # ========================================
    # 🧠 ENHANCED EXISTING LEARNING METHODS
    # ========================================
    
    def learn_from_intervention(self, question_text: str, answer_provided: str, 
                              question_type: str, selector_used: str, success: bool,
                              confidence_before: float, context: Dict[str, Any] = None):
        """
        🧠 BRAIN LEARNING: Learn from manual interventions
        This is how Quenito gets smarter!
        """
        intervention_data = {
            "timestamp": time.time(),
            "question_text": question_text.lower(),
            "answer_provided": answer_provided,
            "question_type": question_type,
            "selector_used": selector_used,
            "success": success,
            "confidence_before": confidence_before,
            "context": context or {}
        }
        
        # Store in brain learning
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'intervention_history' not in self.data['brain_learning']:
            self.data['brain_learning']['intervention_history'] = []
        
        self.data['brain_learning']['intervention_history'].append(intervention_data)
        
        # Add to current session
        self.learning_session['learning_events'].append(intervention_data)
        
        # 🧠 Extract learning patterns
        self._extract_learning_patterns(intervention_data)
        
        # 🔧 CRITICAL: Save after learning
        self.save()
        
        print(f"🧠 BRAIN LEARNED: '{question_text[:50]}...' -> '{answer_provided}' (Success: {success})")
        
    def learn_successful_pattern(self, question_text: str, successful_strategy: Dict[str, Any]):
        """
        🧠 BRAIN LEARNING: Store successful automation strategies
        """
        pattern_key = self._generate_pattern_key(question_text)
        
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'success_patterns' not in self.data['brain_learning']:
            self.data['brain_learning']['success_patterns'] = {}
        
        self.data['brain_learning']['success_patterns'][pattern_key] = {
            "timestamp": time.time(),
            "question_text": question_text,
            "strategy": successful_strategy,
            "usage_count": self.data['brain_learning']['success_patterns'].get(pattern_key, {}).get('usage_count', 0) + 1
        }
        
        # 🔧 CRITICAL: Save after learning
        self.save()
        
        print(f"🧠 SUCCESS PATTERN STORED: {pattern_key}")
    
    def get_learned_strategy(self, question_text: str) -> Optional[Dict[str, Any]]:
        """
        🧠 BRAIN RETRIEVAL: Get previously learned successful strategy
        """
        pattern_key = self._generate_pattern_key(question_text)
        success_patterns = self.data.get('brain_learning', {}).get('success_patterns', {})
        
        if pattern_key in success_patterns:
            strategy = success_patterns[pattern_key]
            print(f"🧠 BRAIN RECALL: Found learned strategy for '{question_text[:30]}...'")
            return strategy['strategy']
        
        return None
    
    def update_confidence_calibration(self, handler_type: str, question_pattern: str, 
                                    predicted_confidence: float, actual_success: bool):
        """
        🧠 BRAIN LEARNING: Calibrate confidence predictions based on actual results
        """
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'confidence_calibration' not in self.data['brain_learning']:
            self.data['brain_learning']['confidence_calibration'] = {}
        
        calibration_key = f"{handler_type}_{question_pattern}"
        
        if calibration_key not in self.data['brain_learning']['confidence_calibration']:
            self.data['brain_learning']['confidence_calibration'][calibration_key] = {
                "predictions": [],
                "accuracy_rate": 0.0,
                "recommended_threshold": 0.3
            }
        
        # Add new prediction result
        self.data['brain_learning']['confidence_calibration'][calibration_key]['predictions'].append({
            "predicted_confidence": predicted_confidence,
            "actual_success": actual_success,
            "timestamp": time.time()
        })
        
        # Recalculate accuracy and adjust threshold
        self._recalibrate_confidence_threshold(calibration_key)
        
        # 🔧 CRITICAL: Save after learning
        self.save()
        
        print(f"🧠 CONFIDENCE CALIBRATED: {calibration_key} -> Predicted: {predicted_confidence:.2f}, Success: {actual_success}")
    
    def get_recommended_confidence_threshold(self, handler_type: str, question_pattern: str = "general") -> float:
        """
        🧠 BRAIN INTELLIGENCE: Get learned confidence threshold for handler/pattern combination
        """
        calibration_key = f"{handler_type}_{question_pattern}"
        calibration_data = self.data.get('brain_learning', {}).get('confidence_calibration', {})
        
        if calibration_key in calibration_data:
            threshold = calibration_data[calibration_key]['recommended_threshold']
            print(f"🧠 BRAIN THRESHOLD: {calibration_key} -> {threshold:.2f}")
            return threshold
        
        # Fallback to default thresholds
        defaults = {
            "demographics": 0.3,
            "brand_familiarity": 0.5,
            "rating_matrix": 0.6,
            "multi_select": 0.3,
            "research": 0.3
        }
        
        return defaults.get(handler_type, 0.3)
    
    def add_discovered_question_pattern(self, question_text: str, question_type: str, 
                                      keywords_found: List[str], successful_response: str):
        """
        🧠 BRAIN EXPANSION: Add newly discovered question patterns
        """
        pattern_data = {
            "question_text": question_text,
            "question_type": question_type,
            "keywords": keywords_found,
            "successful_response": successful_response,
            "discovery_timestamp": time.time(),
            "usage_count": 1
        }
        
        # Determine pattern category
        category = self._categorize_question(question_text, keywords_found)
        
        if 'question_patterns' not in self.data:
            self.data['question_patterns'] = {}
        if category not in self.data['question_patterns']:
            self.data['question_patterns'][category] = {'discovered_patterns': []}
        if 'discovered_patterns' not in self.data['question_patterns'][category]:
            self.data['question_patterns'][category]['discovered_patterns'] = []
        
        self.data['question_patterns'][category]['discovered_patterns'].append(pattern_data)
        
        # Add to current session discoveries
        self.learning_session['new_patterns_discovered'].append(pattern_data)
        
        # 🔧 CRITICAL: Save after discovery
        self.save()
        
        print(f"🧠 NEW PATTERN DISCOVERED: {category} -> '{question_text[:40]}...'")
    
    def get_handler_performance_history(self, handler_type: str) -> Dict[str, Any]:
        """
        🧠 BRAIN ANALYTICS: Get performance history for a handler
        """
        performance_data = self.data.get('brain_learning', {}).get('handler_performance', {})
        return performance_data.get(handler_type, {
            "total_attempts": 0,
            "successful_attempts": 0,
            "success_rate": 0.0,
            "average_confidence": 0.0,
            "improvement_trend": "stable"
        })
    
    def update_handler_performance(self, handler_type: str, confidence: float, success: bool):
        """
        🧠 BRAIN TRACKING: Update handler performance metrics
        """
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        if 'handler_performance' not in self.data['brain_learning']:
            self.data['brain_learning']['handler_performance'] = {}
        
        if handler_type not in self.data['brain_learning']['handler_performance']:
            self.data['brain_learning']['handler_performance'][handler_type] = {
                "total_attempts": 0,
                "successful_attempts": 0,
                "success_rate": 0.0,
                "confidence_history": [],
                "average_confidence": 0.0,
                "improvement_trend": "stable",
                "last_updated": time.time()
            }
        
        perf = self.data['brain_learning']['handler_performance'][handler_type]
        
        # Update metrics
        perf['total_attempts'] += 1
        if success:
            perf['successful_attempts'] += 1
        
        perf['success_rate'] = perf['successful_attempts'] / perf['total_attempts']
        perf['confidence_history'].append(confidence)
        perf['average_confidence'] = sum(perf['confidence_history']) / len(perf['confidence_history'])
        perf['last_updated'] = time.time()
        
        # Calculate improvement trend
        if len(perf['confidence_history']) >= 5:
            recent = perf['confidence_history'][-5:]
            older = perf['confidence_history'][-10:-5] if len(perf['confidence_history']) >= 10 else perf['confidence_history'][:-5]
            
            if older:
                recent_avg = sum(recent) / len(recent)
                older_avg = sum(older) / len(older)
                
                if recent_avg > older_avg + 0.05:
                    perf['improvement_trend'] = "improving"
                elif recent_avg < older_avg - 0.05:
                    perf['improvement_trend'] = "declining"
                else:
                    perf['improvement_trend'] = "stable"
        
        # 🔧 CRITICAL: Save after performance update
        self.save()
        
        print(f"🧠 PERFORMANCE UPDATED: {handler_type} -> {perf['success_rate']:.1%} success, trending {perf['improvement_trend']}")

    # ========================================
    # 🧠 NEW: PHASE 1 INTERVENTION LEARNING METHODS
    # ========================================
    #!/usr/bin/env python3
    """
    Enhanced Knowledge Base - Learning Data Integration
    Adds comprehensive learning data storage and handler improvement capabilities.
    🧠 Stores intervention learning data
    🎯 Tracks handler improvement patterns  
    📊 Updates confidence calibration
    🔄 Enables pattern-based learning
    """

    def store_intervention_learning(self, learning_data: Dict[str, Any]):
        """🧠 Store intervention learning data for handler improvement"""
        try:
            # Ensure intervention_learning section exists
            if "intervention_learning" not in self.data:
                self.data["intervention_learning"] = {
                    "sessions": [],
                    "question_patterns": {},
                    "element_type_patterns": {},
                    "confidence_failures": {},
                    "improvement_suggestions": []
                }
            
            # Store the intervention session
            session_summary = {
                "intervention_id": learning_data["intervention_id"],
                "timestamp": learning_data["timestamp"],
                "question_type": learning_data["question_analysis"]["question_type"],
                "element_type": learning_data["question_analysis"]["element_type"],
                "failed_confidence": learning_data["question_analysis"]["confidence_attempted"],
                "user_answer": learning_data["user_response"]["answer_provided"],
                "duration": learning_data["duration_seconds"]
            }
            
            self.data["intervention_learning"]["sessions"].append(session_summary)
            
            # Update question patterns for improved detection
            question_type = learning_data["question_analysis"]["question_type"]
            if question_type not in self.data["intervention_learning"]["question_patterns"]:
                self.data["intervention_learning"]["question_patterns"][question_type] = {
                    "failed_attempts": [],
                    "element_types_seen": {},
                    "common_answers": [],
                    "confidence_thresholds": []
                }
            
            pattern_data = self.data["intervention_learning"]["question_patterns"][question_type]
            pattern_data["failed_attempts"].append({
                "confidence": learning_data["question_analysis"]["confidence_attempted"],
                "reason": learning_data["question_analysis"]["failure_reason"],
                "timestamp": learning_data["timestamp"]
            })
            
            # Track element types for this question type
            element_type = learning_data["question_analysis"]["element_type"]
            if element_type not in pattern_data["element_types_seen"]:
                pattern_data["element_types_seen"][element_type] = 0
            pattern_data["element_types_seen"][element_type] += 1
            
            # Store user answer for pattern recognition
            user_answer = learning_data["user_response"]["answer_provided"]
            if user_answer not in pattern_data["common_answers"]:
                pattern_data["common_answers"].append(user_answer)
            
            # Update confidence failure tracking
            confidence = learning_data["question_analysis"]["confidence_attempted"]
            if question_type not in self.data["intervention_learning"]["confidence_failures"]:
                self.data["intervention_learning"]["confidence_failures"][question_type] = []
            
            self.data["intervention_learning"]["confidence_failures"][question_type].append(confidence)
            
            print(f"🧠 Intervention learning stored for {question_type}")
            
            # Auto-save after storing learning data
            self.save()
            
        except Exception as e:
            print(f"❌ Error storing intervention learning: {e}")

    def store_handler_improvement_pattern(self, handler_name: str, improvement_pattern: Dict[str, Any]):
        """🎯 Store handler improvement patterns for future automation enhancement"""
        try:
            # Ensure handler_improvements section exists
            if "handler_improvements" not in self.data:
                self.data["handler_improvements"] = {}
            
            if handler_name not in self.data["handler_improvements"]:
                self.data["handler_improvements"][handler_name] = {
                    "improvement_patterns": [],
                    "confidence_adjustments": {},
                    "suggested_enhancements": [],
                    "learning_priority": "medium"
                }
            
            # Store the improvement pattern
            self.data["handler_improvements"][handler_name]["improvement_patterns"].append(improvement_pattern)
            
            # Analyze confidence adjustments needed
            failed_confidence = improvement_pattern["failed_confidence"]
            element_type = improvement_pattern["element_type"]
            
            # Suggest confidence adjustment
            adjustment_key = f"{improvement_pattern['question_type']}_{element_type}"
            if adjustment_key not in self.data["handler_improvements"][handler_name]["confidence_adjustments"]:
                self.data["handler_improvements"][handler_name]["confidence_adjustments"][adjustment_key] = []
            
            self.data["handler_improvements"][handler_name]["confidence_adjustments"][adjustment_key].append({
                "failed_at": failed_confidence,
                "suggested_threshold": max(0.1, failed_confidence - 0.1),  # Lower threshold
                "timestamp": improvement_pattern["learning_timestamp"]
            })
            
            print(f"🎯 Handler improvement pattern stored for {handler_name}")
            
            # Auto-save
            self.save()
            
        except Exception as e:
            print(f"❌ Error storing handler improvement pattern: {e}")

    def get_confidence_adjustment_suggestions(self, handler_name: str, question_type: str, element_type: str = "unknown") -> float:
        """🧠 FIXED: Get confidence adjustment suggestions from intervention learning data"""
        try:
            interventions = self.data.get('intervention_learning', {})
            
            # Look for similar question types and handlers
            adjustment = 0.0
            matches = 0
            
            for intervention_id, intervention_data in interventions.items():
                if (intervention_data.get('handler_name') == handler_name and 
                    intervention_data.get('question_type') == question_type):
                    
                    # If this combination has been successful before, boost confidence
                    if intervention_data.get('result') == 'SUCCESS':
                        adjustment += 0.2
                    else:
                        adjustment -= 0.1
                    matches += 1
            
            # Average the adjustment
            if matches > 0:
                adjustment = adjustment / matches
            
            # Cap adjustments to reasonable range
            adjustment = max(-0.3, min(0.3, adjustment))
            
            if adjustment != 0:
                print(f"🧠 Confidence adjustment for {handler_name}.{question_type}: {adjustment:+.2f}")
            
            return adjustment
            
        except Exception as e:
            print(f"❌ Error getting confidence adjustment: {e}")
            return 0.0

    def get_intervention_insights(self, question_type: str = None) -> Dict[str, Any]:
        """📊 Get insights from intervention learning data"""
        try:
            if "intervention_learning" not in self.data:
                return {"insights": "No intervention data available"}
            
            insights = {
                "total_interventions": len(self.data["intervention_learning"]["sessions"]),
                "question_types_needing_help": {},
                "common_element_types": {},
                "confidence_failure_patterns": {}
            }
            
            # Analyze sessions
            for session in self.data["intervention_learning"]["sessions"]:
                q_type = session["question_type"]
                if q_type not in insights["question_types_needing_help"]:
                    insights["question_types_needing_help"][q_type] = 0
                insights["question_types_needing_help"][q_type] += 1
                
                # Track element types
                element_type = session["element_type"]
                if element_type not in insights["common_element_types"]:
                    insights["common_element_types"][element_type] = 0
                insights["common_element_types"][element_type] += 1
            
            # Confidence failure analysis
            if "confidence_failures" in self.data["intervention_learning"]:
                for q_type, failures in self.data["intervention_learning"]["confidence_failures"].items():
                    if failures:
                        insights["confidence_failure_patterns"][q_type] = {
                            "average_failed_confidence": sum(failures) / len(failures),
                            "lowest_failed_confidence": min(failures),
                            "failure_count": len(failures)
                        }
            
            return insights
            
        except Exception as e:
            print(f"❌ Error getting intervention insights: {e}")
            return {"error": str(e)}

    def suggest_handler_improvements(self, handler_name: str) -> List[str]:
        """💡 Generate improvement suggestions based on learning data"""
        try:
            suggestions = []
            
            if "handler_improvements" not in self.data or handler_name not in self.data["handler_improvements"]:
                return ["No improvement data available for this handler"]
            
            improvements = self.data["handler_improvements"][handler_name]
            
            # Analyze confidence adjustments
            if "confidence_adjustments" in improvements:
                for pattern, adjustments in improvements["confidence_adjustments"].items():
                    if adjustments:
                        avg_failed = sum(adj["failed_at"] for adj in adjustments) / len(adjustments)
                        suggestions.append(f"Lower confidence threshold for {pattern} - currently failing at {avg_failed:.2f}")
            
            # Analyze improvement patterns
            if "improvement_patterns" in improvements:
                element_types = {}
                for pattern in improvements["improvement_patterns"]:
                    et = pattern.get("element_type", "unknown")
                    if et not in element_types:
                        element_types[et] = 0
                    element_types[et] += 1
                
                for element_type, count in element_types.items():
                    if count > 1:
                        suggestions.append(f"Improve {element_type} detection - failed {count} times")
            
            if not suggestions:
                suggestions.append("Handler performing well - no specific improvements needed")
            
            return suggestions
            
        except Exception as e:
            return [f"Error generating suggestions: {e}"]


    # ========================================
    # 🧠 USER DATA ACCESS METHODS
    # ========================================
    
    async def get_user_age(self) -> Optional[str]:
        """🧠 Get user age from demographics"""
        try:
            demographics = self.get_demographics()
            age = demographics.get('age')
            if age:
                print(f"🧠 Retrieved user age: {age}")
                return str(age)
            else:
                print(f"⚠️ No age found in user profile")
                return None
        except Exception as e:
            print(f"❌ Error getting user age: {e}")
            return None
    
    async def get_user_gender(self) -> Optional[str]:
        """🧠 Get user gender from demographics"""
        try:
            demographics = self.get_demographics()
            gender = demographics.get('gender')
            if gender:
                print(f"🧠 Retrieved user gender: {gender}")
                return str(gender)
            else:
                print(f"⚠️ No gender found in user profile")
                return None
        except Exception as e:
            print(f"❌ Error getting user gender: {e}")
            return None
    
    async def get_user_location(self) -> Optional[str]:
        """🧠 Get user location from demographics"""
        try:
            demographics = self.get_demographics()
            location = demographics.get('location')
            if location:
                print(f"🧠 Retrieved user location: {location}")
                return str(location)
            else:
                print(f"⚠️ No location found in user profile")
                return None
        except Exception as e:
            print(f"❌ Error getting user location: {e}")
            return None

    # ========================================
    # 🧠 BRAIN INTELLIGENCE HELPERS
    # ========================================
    
    def _ensure_brain_structures(self):
        """Ensure all brain learning structures exist"""
        if 'brain_learning' not in self.data:
            self.data['brain_learning'] = {}
        
        brain_defaults = {
            'intervention_history': [],
            'success_patterns': {},
            'strategy_preferences': {},  # NEW!
            'confidence_calibration': {},
            'handler_performance': {},
            'failure_analysis': [],  # NEW!
            'learning_history': [],  # NEW!
            'pattern_evolution': {},
            'learning_metrics': {
                'total_interventions': 0,
                'automation_improvement_rate': 0.0,
                'last_learning_session': None
            }
        }
        
        for key, default in brain_defaults.items():
            if key not in self.data['brain_learning']:
                self.data['brain_learning'][key] = default
    
    def _extract_learning_patterns(self, intervention_data: Dict[str, Any]):
        """Extract patterns from intervention data for future learning"""
        question_text = intervention_data['question_text']
        answer = intervention_data['answer_provided']
        
        # Extract keywords that might be useful for future pattern matching
        important_keywords = []
        keywords_to_check = ['age', 'gender', 'male', 'female', 'location', 'state', 'income', 'employment']
        
        for keyword in keywords_to_check:
            if keyword in question_text:
                important_keywords.append(keyword)
        
        # Store pattern insights
        if important_keywords:
            pattern_insight = {
                "keywords": important_keywords,
                "successful_answer": answer,
                "question_length": len(question_text),
                "extraction_timestamp": time.time()
            }
            
            if 'pattern_insights' not in self.data['brain_learning']:
                self.data['brain_learning']['pattern_insights'] = []
            
            self.data['brain_learning']['pattern_insights'].append(pattern_insight)
    
    def _categorize_question(self, question_text: str, keywords: List[str]) -> str:
        """Categorize discovered questions"""
        question_lower = question_text.lower()
        
        # Demographics patterns
        if any(word in question_lower for word in ['age', 'gender', 'male', 'female', 'location', 'state']):
            return "demographics_questions"
        
        # Brand patterns  
        if any(word in question_lower for word in ['brand', 'familiar', 'use', 'purchase', 'buy']):
            return "brand_familiarity_questions"
        
        # Rating patterns
        if any(word in question_lower for word in ['rate', 'rating', 'scale', 'agree', 'disagree']):
            return "rating_questions"
        
        # Default category
        return "general_questions"
    
    def _recalibrate_confidence_threshold(self, calibration_key: str):
        """Recalibrate confidence threshold based on prediction accuracy"""
        calibration_data = self.data['brain_learning']['confidence_calibration'][calibration_key]
        predictions = calibration_data['predictions']
        
        if len(predictions) >= 3:  # Need minimum data points
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
    
    # ========================================
    # EXISTING METHODS (Enhanced)
    # ========================================
    
    def get(self, key: str, default=None):
        """Get a value from the knowledge base."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a value in the knowledge base."""
        self.data[key] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple values in the knowledge base."""
        self.data.update(updates)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get the complete user profile."""
        return self.data.get("user_profile", {})
    
    def get_demographics(self) -> Dict[str, Any]:
        """Get user demographics."""
        return self.get_user_profile().get("demographics", {})
    
    def get_brand_preferences(self) -> Dict[str, Any]:
        """Get user brand preferences."""
        return self.get_user_profile().get("existing_brands", {})
    
    def get_interests(self) -> Dict[str, Any]:
        """Get user interests and preferences."""
        return self.get_user_profile().get("interests_and_preferences", {})
    
    def get_question_patterns(self) -> Dict[str, Any]:
        """Get question detection patterns."""
        return self.data.get("question_patterns", {})
    
    def get_question_pattern(self, pattern_name: str) -> Dict[str, Any]:
        """Get a specific question pattern."""
        patterns = self.get_question_patterns()
        return patterns.get(pattern_name, {})
    
    def get_automation_settings(self) -> Dict[str, Any]:
        """Get automation configuration settings."""
        return self.data.get("automation_settings", {})
    
    def get_research_patterns(self) -> Dict[str, Any]:
        """Get research configuration patterns."""
        return self.data.get("research_patterns", {})
    
    def add_research_result(self, query: str, results: List[Dict[str, Any]]):
        """Add research results to the cache."""
        if 'research_cache' not in self.data:
            self.data['research_cache'] = {}
        
        self.data['research_cache'][query] = {
            'results': results,
            'timestamp': time.time()
        }
    
    def get_research_result(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached research results."""
        cache = self.data.get('research_cache', {})
        result = cache.get(query)
        
        if result:
            # Check if result is less than 24 hours old
            if time.time() - result['timestamp'] < 86400:  # 24 hours
                return result['results']
        
        return None
    
    def get_known_brands(self, category: str = "currently_use") -> List[str]:
        """Get list of known brands for a category."""
        brands = self.get_brand_preferences()
        return brands.get(category, [])
    
    def get_user_interests_by_level(self, level: str) -> List[str]:
        """Get user interests by level (high, medium, low)."""
        interests = self.get_interests()
        return interests.get(f"{level}_interest", [])
    
    def get_location_mappings(self) -> Dict[str, List[str]]:
        """Get location format mappings for different survey platforms."""
        demographics_patterns = self.get_question_pattern("demographics_questions")
        location_questions = demographics_patterns.get("location_questions", {})
        return location_questions.get("location_mappings", {})
    
    def get_activity_patterns(self) -> Dict[str, Any]:
        """Get activity likelihood patterns for recency questions."""
        recency_patterns = self.get_question_pattern("recency_activities_questions")
        return recency_patterns.get("activity_patterns", {})
    
    def get_brand_familiarity_levels(self) -> Dict[str, List[str]]:
        """Get brand familiarity response mappings."""
        brand_patterns = self.get_question_pattern("brand_familiarity_questions")
        return brand_patterns.get("response_levels", {})
    
    def add_used_brand(self, brand: str):
        """Track used brands to avoid repetition."""
        if 'used_brands' not in self.data:
            self.data['used_brands'] = []
        
        if brand not in self.data['used_brands']:
            self.data['used_brands'].append(brand)
    
    def get_used_brands(self) -> List[str]:
        """Get list of brands already used in current session."""
        return self.data.get('used_brands', [])
    
    def clear_used_brands(self):
        """Clear the used brands list (for new survey sessions)."""
        self.data['used_brands'] = []
    
    def update_user_profile(self, updates: Dict[str, Any]):
        """Update user profile with new information."""
        if 'user_profile' not in self.data:
            self.data['user_profile'] = {}
        
        self.data['user_profile'].update(updates)
    
    def add_question_pattern(self, pattern_name: str, pattern_data: Dict[str, Any]):
        """Add a new question pattern to the knowledge base."""
        if 'question_patterns' not in self.data:
            self.data['question_patterns'] = {}
        
        self.data['question_patterns'][pattern_name] = pattern_data
    
    def get_fallback_brands(self, category: str) -> List[str]:
        """Get fallback brand lists for research failures."""
        brand_patterns = self.get_question_pattern("brand_naming_questions")
        product_categories = brand_patterns.get("product_categories", {})
        category_data = product_categories.get(category, {})
        return category_data.get("fallback_brands", [])
    
    def get_research_query_for_category(self, category: str) -> str:
        """Get research query template for a product category."""
        brand_patterns = self.get_question_pattern("brand_naming_questions")
        product_categories = brand_patterns.get("product_categories", {})
        category_data = product_categories.get(category, {})
        return category_data.get("research_query", "")
    
    def get_confirmed_survey_domains(self) -> List[str]:
        """Get list of confirmed survey domains."""
        automation_settings = self.get_automation_settings()
        return automation_settings.get("confirmed_survey_domains", [
            "yoursurveynow.com",
            "qualtrics.com", 
            "decipherinc.com",
            "surveycmix.com"
        ])
    
    def get_selection_limits(self) -> Dict[str, int]:
        """Get selection limits for various question types."""
        automation_settings = self.get_automation_settings()
        return automation_settings.get("selection_limits", {
            "multi_select_max": 5,
            "brand_personality_max": 3,
            "interests_max": 8
        })
    
    def get_delay_settings(self) -> Dict[str, str]:
        """Get human-like delay settings."""
        automation_settings = self.get_automation_settings()
        return automation_settings.get("delays", {
            "between_actions": "1500-4000ms",
            "after_research": "2000-3000ms",
            "page_load": "2000-3000ms",
            "checkbox_selection": "300-700ms",
            "matrix_navigation": "200-500ms"
        })
    
    def _create_fallback_knowledge_base(self):
        """Create a minimal fallback knowledge base with brain structures."""
        self.data = {
            "user_profile": {
                "demographics": {
                    "age": "45",
                    "birth_year": "1980",
                    "gender": "Male",
                    "location": "New South Wales",
                    "postcode": "2217",
                    "household_size": "4",
                    "marital_status": "Married",
                    "employment_status": "Full-time",
                    "education": "High school"
                },
                "existing_brands": {
                    "currently_use": [
                        "Netflix", "Spotify", "Commonwealth Bank", "Toyota", "Telstra"
                    ],
                    "familiar_with": [
                        "Samsung", "LG", "Sony", "Westpac", "ANZ"
                    ]
                },
                "interests_and_preferences": {
                    "high_interest": ["technology", "news", "finance"],
                    "medium_interest": ["sports", "music", "travel"],
                    "low_interest": ["fashion", "celebrities"]
                }
            },
            "question_patterns": {},
            "automation_settings": {
                "confirmed_survey_domains": [
                    "yoursurveynow.com",
                    "qualtrics.com",
                    "decipherinc.com", 
                    "surveycmix.com"
                ]
            },
            # 🧠 Brain learning structures
            "brain_learning": {
                "intervention_history": [],
                "success_patterns": {},
                "strategy_preferences": {},  # NEW!
                "confidence_calibration": {},
                "handler_performance": {},
                "failure_analysis": [],  # NEW!
                "learning_history": [],  # NEW!
                "pattern_evolution": {},
                "learning_metrics": {
                    "total_interventions": 0,
                    "automation_improvement_rate": 0.0,
                    "last_learning_session": None
                }
            }
        }
        print("🔧 Fallback knowledge base created with brain learning structures")
    
    def print_summary(self):
        """Print a comprehensive summary of the knowledge base including brain learning."""
        print(f"\n📊 KNOWLEDGE BASE SUMMARY:")
        print(f"   File: {self.path}")
        print(f"   User Profile: {'✅' if 'user_profile' in self.data else '❌'}")
        print(f"   Question Patterns: {len(self.data.get('question_patterns', {}))}")
        print(f"   Research Cache: {len(self.data.get('research_cache', {}))}")
        print(f"   Used Brands: {len(self.data.get('used_brands', []))}")
        
        demographics = self.get_demographics()
        if demographics:
            print(f"   Demographics: Age {demographics.get('age', 'N/A')}, "
                  f"Gender {demographics.get('gender', 'N/A')}, "
                  f"Location {demographics.get('location', 'N/A')}")
        
        brands = self.get_brand_preferences()
        if brands:
            currently_use = len(brands.get('currently_use', []))
            familiar_with = len(brands.get('familiar_with', []))
            print(f"   Brands: {currently_use} currently use, {familiar_with} familiar with")
        
        # 🧠 Brain learning summary
        brain_data = self.data.get('brain_learning', {})
        if brain_data:
            print(f"\n🧠 BRAIN LEARNING SUMMARY:")
            print(f"   Total Interventions: {len(brain_data.get('intervention_history', []))}")
            print(f"   Success Patterns: {len(brain_data.get('success_patterns', {}))}")
            print(f"   Strategy Preferences: {len(brain_data.get('strategy_preferences', {}))}")  # NEW!
            print(f"   Confidence Calibrations: {len(brain_data.get('confidence_calibration', {}))}")
            print(f"   Handler Performance Tracking: {len(brain_data.get('handler_performance', {}))}")
            print(f"   Automation Learning History: {len(brain_data.get('learning_history', []))}")  # NEW!
            
            # Performance insights
            handler_perf = brain_data.get('handler_performance', {})
            if handler_perf:
                print(f"   🎯 Handler Success Rates:")
                for handler, perf in handler_perf.items():
                    success_rate = perf.get('success_rate', 0) * 100
                    trend = perf.get('improvement_trend', 'unknown')
                    print(f"      {handler}: {success_rate:.1f}% (trending {trend})")
            
            # Strategy preferences insights
            strategy_prefs = brain_data.get('strategy_preferences', {})
            if strategy_prefs:
                print(f"   🎯 Strategy Preferences:")
                for question_type, pref in strategy_prefs.items():
                    strategy = pref.get('preferred_strategy', 'none')
                    success_rate = pref.get('success_rate', 0) * 100
                    print(f"      {question_type}: {strategy} ({success_rate:.1f}% success)")
            
            # Learning session info
            current_session = self.learning_session
            print(f"   📈 Current Session: {len(current_session['learning_events'])} events, "
                  f"{len(current_session['new_patterns_discovered'])} new patterns")
    
    def print_brain_intelligence_report(self):
        """
        🧠 Print detailed brain intelligence and learning report
        """
        print(f"\n🧠 ===============================================")
        print(f"🧠 QUENITO'S DIGITAL BRAIN INTELLIGENCE REPORT")
        print(f"🧠 ===============================================")
        
        brain_data = self.data.get('brain_learning', {})
        
        # Automation Learning Analysis (NEW!)
        learning_history = brain_data.get('learning_history', [])
        if learning_history:
            print(f"\n🤖 AUTOMATION LEARNING ANALYSIS:")
            print(f"   Total Automation Events: {len(learning_history)}")
            
            # Success rate analysis
            successful_automations = [event for event in learning_history if event.get('result') == 'SUCCESS']
            if learning_history:
                automation_success_rate = len(successful_automations) / len(learning_history) * 100
                print(f"   Automation Success Rate: {automation_success_rate:.1f}%")
            
            # Question type analysis
            question_types = {}
            for event in learning_history:
                q_type = event.get('question_type', 'unknown')
                question_types[q_type] = question_types.get(q_type, 0) + 1
            
            if question_types:
                print(f"   Automated Question Types:")
                for q_type, count in sorted(question_types.items(), key=lambda x: x[1], reverse=True):
                    print(f"      {q_type}: {count} successful automations")
        
        # Strategy Preferences Analysis (NEW!)
        strategy_prefs = brain_data.get('strategy_preferences', {})
        if strategy_prefs:
            print(f"\n🎯 STRATEGY LEARNING ANALYSIS:")
            print(f"   Learned Strategy Preferences: {len(strategy_prefs)}")
            
            for question_type, pref in strategy_prefs.items():
                strategy = pref.get('preferred_strategy', 'none')
                success_rate = pref.get('success_rate', 0) * 100
                success_count = pref.get('success_count', 0)
                avg_time = pref.get('avg_execution_time', 0)
                
                print(f"   {question_type}:")
                print(f"      Preferred Strategy: {strategy}")
                print(f"      Success Rate: {success_rate:.1f}% ({success_count} successes)")
                if avg_time > 0:
                    print(f"      Avg Execution Time: {avg_time:.1f}s")
        
        # Learning History Analysis
        interventions = brain_data.get('intervention_history', [])
        if interventions:
            print(f"\n📚 MANUAL INTERVENTION LEARNING:")
            print(f"   Total Interventions: {len(interventions)}")
            
            # Success rate over time
            recent_interventions = interventions[-10:] if len(interventions) >= 10 else interventions
            success_rate = sum(1 for i in recent_interventions if i.get('success', False)) / len(recent_interventions) * 100
            print(f"   Recent Success Rate: {success_rate:.1f}%")
            
            # Most common question types
            question_types = {}
            for intervention in interventions:
                q_type = intervention.get('question_type', 'unknown')
                question_types[q_type] = question_types.get(q_type, 0) + 1
            
            if question_types:
                print(f"   Most Common Question Types:")
                for q_type, count in sorted(question_types.items(), key=lambda x: x[1], reverse=True)[:3]:
                    print(f"      {q_type}: {count} interventions")
        
        # Success Patterns Analysis
        success_patterns = brain_data.get('success_patterns', {})
        if success_patterns:
            print(f"\n🎯 SUCCESS PATTERNS STORED:")
            print(f"   Total Patterns: {len(success_patterns)}")
            
            # Most used patterns
            sorted_patterns = sorted(success_patterns.items(), 
                                   key=lambda x: x[1].get('usage_count', 0), reverse=True)
            
            print(f"   Most Used Patterns:")
            for pattern_key, pattern_data in sorted_patterns[:3]:
                usage = pattern_data.get('usage_count', 0)
                question = pattern_data.get('question_text', '')[:40]
                strategy = pattern_data.get('strategy', 'unknown')
                print(f"      {pattern_key}: {usage} uses, strategy: {strategy}")
                print(f"         Question: '{question}...'")
        
        # Confidence Calibration Analysis
        calibrations = brain_data.get('confidence_calibration', {})
        if calibrations:
            print(f"\n🎯 CONFIDENCE CALIBRATION:")
            for handler_pattern, cal_data in calibrations.items():
                if isinstance(cal_data, dict):
                    accuracy = cal_data.get('accuracy_rate', 0) * 100
                    threshold = cal_data.get('recommended_threshold', 0.3)
                    predictions = len(cal_data.get('predictions', []))
                    print(f"   {handler_pattern}: {accuracy:.1f}% accuracy, "
                          f"threshold: {threshold:.2f}, {predictions} predictions")
        
        # Handler Performance Analysis
        handler_perf = brain_data.get('handler_performance', {})
        if handler_perf:
            print(f"\n📊 HANDLER PERFORMANCE INTELLIGENCE:")
            for handler, perf in handler_perf.items():
                if isinstance(perf, dict):
                    # Check if this is detailed handler performance or simple
                    if 'total_attempts' in perf:
                        attempts = perf.get('total_attempts', 0)
                        success_rate = perf.get('success_rate', 0) * 100
                        avg_confidence = perf.get('average_confidence', 0)
                        trend = perf.get('improvement_trend', 'unknown')
                        
                        print(f"   {handler}:")
                        print(f"      Attempts: {attempts}, Success Rate: {success_rate:.1f}%")
                        print(f"      Avg Confidence: {avg_confidence:.2f}, Trend: {trend}")
                    else:
                        # Detailed question-type breakdown
                        print(f"   {handler}:")
                        for question_type, q_perf in perf.items():
                            if isinstance(q_perf, dict):
                                attempts = q_perf.get('total_attempts', 0)
                                success_rate = q_perf.get('success_rate', 0) * 100
                                avg_confidence = q_perf.get('avg_confidence', 0)
                                print(f"      {question_type}: {attempts} attempts, {success_rate:.1f}% success, {avg_confidence:.2f} confidence")
        
        # Learning Session Summary
        session = self.learning_session
        print(f"\n📈 CURRENT LEARNING SESSION:")
        print(f"   Session ID: {session['session_id']}")
        print(f"   Learning Events: {len(session['learning_events'])}")
        print(f"   New Patterns Discovered: {len(session['new_patterns_discovered'])}")
        print(f"   Performance Improvements: {len(session['performance_improvements'])}")
        
        # Brain Growth Potential
        print(f"\n🚀 BRAIN GROWTH POTENTIAL:")
        total_learning_events = len(learning_history) + len(interventions)
        if total_learning_events > 0:
            automation_potential = (len(success_patterns) / total_learning_events) * 100
            print(f"   Automation Potential: {automation_potential:.1f}%")
            print(f"   Total Learning Events: {total_learning_events}")
            print(f"   Strategy Preferences Learned: {len(strategy_prefs)}")
            
            # Growth recommendations
            if total_learning_events < 5:
                print(f"   🎯 Recommendation: Need more automation attempts (current: {total_learning_events})")
            elif len(success_patterns) < 3:
                print(f"   🎯 Recommendation: Focus on identifying success patterns")
            elif len(strategy_prefs) < 2:
                print(f"   🎯 Recommendation: Test more question types to build strategy preferences")
            else:
                print(f"   🎯 Recommendation: Ready for advanced automation testing")
        
        print(f"\n🧠 ===============================================")
        print(f"🧠 END OF BRAIN INTELLIGENCE REPORT")
        print(f"🧠 ===============================================\n")
    
    def get_brain_learning_summary(self) -> Dict[str, Any]:
        """
        🧠 Get a structured summary of brain learning data for other components
        """
        brain_data = self.data.get('brain_learning', {})
        
        return {
            "total_interventions": len(brain_data.get('intervention_history', [])),
            "automation_learning_events": len(brain_data.get('learning_history', [])),  # NEW!
            "success_patterns_count": len(brain_data.get('success_patterns', {})),
            "strategy_preferences_count": len(brain_data.get('strategy_preferences', {})),  # NEW!
            "calibrated_handlers": len(brain_data.get('confidence_calibration', {})),
            "tracked_handlers": len(brain_data.get('handler_performance', {})),
            "current_session_events": len(self.learning_session['learning_events']),
            "current_session_discoveries": len(self.learning_session['new_patterns_discovered']),
            "brain_intelligence_level": self._calculate_intelligence_level(),
            "automation_readiness": self._calculate_automation_readiness()
        }
    
    def _calculate_intelligence_level(self) -> str:
        """Calculate current brain intelligence level"""
        brain_data = self.data.get('brain_learning', {})
        
        interventions = len(brain_data.get('intervention_history', []))
        automation_events = len(brain_data.get('learning_history', []))  # NEW!
        success_patterns = len(brain_data.get('success_patterns', {}))
        strategy_preferences = len(brain_data.get('strategy_preferences', {}))  # NEW!
        calibrations = len(brain_data.get('confidence_calibration', {}))
        
        # Calculate intelligence score
        score = 0
        total_learning_events = interventions + automation_events
        
        if total_learning_events >= 5:
            score += 20
        if total_learning_events >= 15:
            score += 20
        if success_patterns >= 3:
            score += 20
        if strategy_preferences >= 2:  # NEW!
            score += 20
        if calibrations >= 2:
            score += 20
        
        if score >= 80:
            return "Advanced"
        elif score >= 60:
            return "Intermediate"
        elif score >= 40:
            return "Learning"
        else:
            return "Beginner"
    
    def _calculate_automation_readiness(self) -> float:
        """Calculate automation readiness percentage"""
        brain_data = self.data.get('brain_learning', {})
        
        # Factors contributing to automation readiness
        interventions = len(brain_data.get('intervention_history', []))
        automation_events = len(brain_data.get('learning_history', []))  # NEW!
        success_patterns = len(brain_data.get('success_patterns', {}))
        strategy_preferences = len(brain_data.get('strategy_preferences', {}))  # NEW!
        handler_performance = brain_data.get('handler_performance', {})
        
        readiness_score = 0.0
        
        # Learning data availability (30% weight)
        total_learning = interventions + automation_events
        if total_learning >= 10:
            readiness_score += 0.3
        elif total_learning >= 5:
            readiness_score += 0.15
        
        # Success pattern coverage (25% weight)
        if success_patterns >= 5:
            readiness_score += 0.25
        elif success_patterns >= 2:
            readiness_score += 0.125
        
        # Strategy preferences (25% weight) - NEW!
        if strategy_preferences >= 3:
            readiness_score += 0.25
        elif strategy_preferences >= 1:
            readiness_score += 0.125
        
        # Handler performance (20% weight)
        if handler_performance:
            total_success_rate = 0
            handler_count = 0
            
            for handler, perf in handler_performance.items():
                if isinstance(perf, dict):
                    if 'success_rate' in perf:
                        total_success_rate += perf.get('success_rate', 0)
                        handler_count += 1
                    else:
                        # Handle detailed performance data
                        for question_type, q_perf in perf.items():
                            if isinstance(q_perf, dict) and 'success_rate' in q_perf:
                                total_success_rate += q_perf.get('success_rate', 0)
                                handler_count += 1
            
            if handler_count > 0:
                avg_success_rate = total_success_rate / handler_count
                readiness_score += avg_success_rate * 0.2
        
        return min(readiness_score * 100, 100.0)  # Cap at 100%