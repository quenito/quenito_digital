#!/usr/bin/env python3
"""
🧠 Multi Select Brain Module v2.0 - Learning & Intelligence Integration
Connects multi-select handling to Quenito's central knowledge base.

This module manages:
- Learning from successful checkbox selections
- Generating intelligent selection patterns
- Storing selection preferences
- Applying learned combinations
- Reporting successes/failures for continuous improvement

ARCHITECTURE: Bridge between multi-select handler and knowledge base
"""

import time
import random
from typing import Dict, Any, Optional, List, Set, Tuple


class MultiSelectBrain:
    """
    🧠 Brain Integration for Multi-Select Questions
    
    Manages all learning and intelligence for multi-select:
    - Learns optimal selection combinations
    - Remembers user preferences
    - Generates human-like selection patterns
    - Reports outcomes for continuous learning
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize brain integration with knowledge base
        
        Args:
            knowledge_base: Reference to Quenito's central knowledge base
        """
        self.brain = knowledge_base
        self.last_question_type = None
        self.last_selections = []
        self.selection_history = {}
        print("🧠 MultiSelectBrain initialized with knowledge base connection")
    
    # ========================================
    # LEARNED SELECTION RETRIEVAL
    # ========================================
    
    async def get_learned_selections(self, question_type: str, content: str) -> Optional[List[str]]:
        """
        Get previously learned selections for a question type
        
        Returns list of options to select, or None if no learning exists
        """
        try:
            if not self.brain:
                return None
            
            # Check learned selections in knowledge base
            learned_selections = self.brain.get("learned_multi_selections", {})
            
            # Try to find exact match first
            content_key = self._generate_content_key(content)
            if content_key in learned_selections:
                selection_data = learned_selections[content_key]
                print(f"🎯 Found exact match for selections: {selection_data['selections']}")
                return selection_data.get('selections', [])
            
            # Try question type patterns
            type_selections = self.brain.get(f"multi_select_{question_type}_defaults", {})
            if type_selections:
                default_selections = type_selections.get('common_selections', [])
                if default_selections:
                    print(f"🎯 Using default selections for {question_type}: {default_selections[:3]}...")
                    return default_selections
            
            # Check user preferences for this type
            user_prefs = self._get_user_preferences(question_type)
            if user_prefs:
                print(f"🎯 Using user preferences for {question_type}")
                return user_prefs
            
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving learned selections: {e}")
            return None
    
    # ========================================
    # SELECTION GENERATION
    # ========================================
    
    def generate_selections(self, question_type: str, options: List[str], 
                          content: str, min_selections: int = 1, 
                          max_selections: int = 5) -> List[str]:
        """
        Generate intelligent selections based on question type and options
        Uses patterns and randomization for human-like behavior
        """
        try:
            selections = []
            
            # Check for exclusive options first
            exclusive_options = [opt for opt in options if self._is_exclusive_option(opt)]
            
            # If selecting exclusive option, return only that
            if exclusive_options and random.random() < 0.15:  # 15% chance
                return [random.choice(exclusive_options)]
            
            # Filter out exclusive options for normal selection
            normal_options = [opt for opt in options if not self._is_exclusive_option(opt)]
            
            # Determine number of selections (human-like distribution)
            if len(normal_options) <= 3:
                num_selections = random.randint(1, min(2, len(normal_options)))
            else:
                # Bias toward 2-3 selections
                weights = [0.15, 0.35, 0.30, 0.15, 0.05]  # 1, 2, 3, 4, 5 selections
                num_selections = random.choices(
                    range(1, min(6, len(normal_options) + 1)),
                    weights=weights[:min(5, len(normal_options))]
                )[0]
            
            # Ensure within limits
            num_selections = max(min_selections, min(num_selections, max_selections))
            
            # Generate selections based on question type
            if question_type == 'activities':
                selections = self._select_activities(normal_options, num_selections)
            elif question_type == 'preferences':
                selections = self._select_preferences(normal_options, num_selections)
            elif question_type == 'features':
                selections = self._select_features(normal_options, num_selections)
            elif question_type == 'brands':
                selections = self._select_brands(normal_options, num_selections)
            else:
                # Generic selection with slight preference for earlier options
                weights = [1.0 / (i + 1) for i in range(len(normal_options))]
                selections = random.choices(normal_options, weights=weights, k=num_selections)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_selections = []
            for sel in selections:
                if sel not in seen:
                    seen.add(sel)
                    unique_selections.append(sel)
            
            print(f"🧠 Generated {len(unique_selections)} selections for {question_type}")
            return unique_selections
            
        except Exception as e:
            print(f"❌ Error generating selections: {e}")
            # Fallback to simple random selection
            return random.sample(options, min(max_selections, len(options)))
    
    def _select_activities(self, options: List[str], num: int) -> List[str]:
        """Select activities based on realistic patterns"""
        # Common activity preferences
        preferred_activities = ['watch', 'read', 'shop', 'browse', 'listen']
        selections = []
        
        # First, select preferred activities
        for option in options:
            option_lower = option.lower()
            if any(pref in option_lower for pref in preferred_activities):
                selections.append(option)
                if len(selections) >= num:
                    break
        
        # Fill remaining with random choices
        remaining = [opt for opt in options if opt not in selections]
        if remaining and len(selections) < num:
            additional = random.sample(remaining, min(num - len(selections), len(remaining)))
            selections.extend(additional)
        
        return selections[:num]
    
    def _select_preferences(self, options: List[str], num: int) -> List[str]:
        """Select preferences with consistency"""
        # Tend to select positive/agreeable options
        positive_indicators = ['yes', 'agree', 'like', 'prefer', 'enjoy', 'good']
        selections = []
        
        for option in options:
            option_lower = option.lower()
            if any(pos in option_lower for pos in positive_indicators):
                selections.append(option)
                if len(selections) >= num:
                    break
        
        # Random fill if needed
        if len(selections) < num:
            remaining = [opt for opt in options if opt not in selections]
            if remaining:
                additional = random.sample(remaining, min(num - len(selections), len(remaining)))
                selections.extend(additional)
        
        return selections[:num]
    
    def _select_features(self, options: List[str], num: int) -> List[str]:
        """Select features based on importance"""
        # Prioritize important-sounding features
        important_keywords = ['security', 'privacy', 'speed', 'quality', 'easy', 'free']
        selections = []
        
        # Select important features first
        for option in options:
            option_lower = option.lower()
            if any(keyword in option_lower for keyword in important_keywords):
                selections.append(option)
        
        # Random selection from remaining
        remaining = [opt for opt in options if opt not in selections]
        if remaining:
            additional_needed = num - len(selections)
            if additional_needed > 0:
                additional = random.sample(remaining, min(additional_needed, len(remaining)))
                selections.extend(additional)
        
        return selections[:num]
    
    def _select_brands(self, options: List[str], num: int) -> List[str]:
        """Select brands based on familiarity"""
        if self.brain:
            user_profile = self.brain.get("user_profile", {})
            preferred_brands = user_profile.get("preferred_brands", [])
            
            # Select preferred brands first
            selections = [opt for opt in options 
                         if any(pref.lower() in opt.lower() for pref in preferred_brands)]
        else:
            selections = []
        
        # Fill with well-known brands or random
        if len(selections) < num:
            remaining = [opt for opt in options if opt not in selections]
            additional = random.sample(remaining, min(num - len(selections), len(remaining)))
            selections.extend(additional)
        
        return selections[:num]
    
    # ========================================
    # SELECTION STORAGE
    # ========================================
    
    async def save_selections(self, question_type: str, selections: List[str], 
                            content: str) -> bool:
        """
        Save successful selections to knowledge base for future use
        """
        try:
            if not self.brain:
                return False
            
            # Get existing learned selections
            learned_selections = self.brain.get("learned_multi_selections", {})
            
            # Generate content key
            content_key = self._generate_content_key(content)
            
            # Update or create selection entry
            learned_selections[content_key] = {
                'question_type': question_type,
                'selections': selections,
                'content_snippet': content[:100],
                'first_used': learned_selections.get(content_key, {}).get('first_used', time.time()),
                'last_used': time.time(),
                'use_count': learned_selections.get(content_key, {}).get('use_count', 0) + 1
            }
            
            # Save back to knowledge base
            self.brain.set("learned_multi_selections", learned_selections)
            
            # Also update question type defaults
            self._update_question_type_defaults(question_type, selections)
            
            if hasattr(self.brain, 'save_data'):
                self.brain.save_data()
            
            print(f"🧠 Saved selections for {question_type}: {selections[:3]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error saving selections: {e}")
            return False
    
    # ========================================
    # SUCCESS/FAILURE REPORTING
    # ========================================
    
    async def report_success(self, strategy_used: str, execution_time: float,
                           question_type: str, selections_made: int,
                           success_rate: float, confidence_score: float = 0.0):
        """Report successful multi-select automation to brain for learning"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"multiselect_{int(time.time())}",
                "question_type": question_type,
                "strategy_used": strategy_used,
                "execution_time": execution_time,
                "selections_made": selections_made,
                "success_rate": success_rate,
                "confidence_score": confidence_score,
                "result": "SUCCESS",
                "automation_success": True
            }
            
            # Store for future reference
            self.last_question_type = question_type
            
            # Report to brain
            if self.brain and hasattr(self.brain, 'learn_successful_automation'):
                success = await self.brain.learn_successful_automation(learning_data)
                if success:
                    print(f"🧠 SUCCESS LEARNED: {strategy_used} for {question_type}")
                    print(f"☑️ Made {selections_made} selections with {success_rate:.1%} success")
                else:
                    print(f"⚠️ Failed to save learning data")
            else:
                print(f"⚠️ Brain connection not available for learning")
                
        except Exception as e:
            print(f"❌ Error reporting success to brain: {e}")
    
    async def report_failure(self, error_message: str, page_content: str,
                           question_type: str = None, confidence_score: float = 0.0):
        """Report automation failure to brain for learning"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"multiselect_{int(time.time())}",
                "question_type": question_type or self.last_question_type or "unknown",
                "error_message": error_message,
                "page_snippet": page_content[:200],
                "confidence_score": confidence_score,
                "result": "FAILURE",
                "automation_success": False
            }
            
            # Report failure for learning
            if self.brain and hasattr(self.brain, 'learn_from_failure'):
                await self.brain.learn_from_failure(learning_data)
                print(f"🧠 FAILURE LEARNED: {error_message}")
            else:
                print(f"⚠️ Brain connection not available for failure learning")
                
        except Exception as e:
            print(f"❌ Error reporting failure to brain: {e}")
    
    # ========================================
    # CONFIDENCE ADJUSTMENTS
    # ========================================
    
    def get_confidence_adjustment(self, question_type: str, base_confidence: float) -> float:
        """Get confidence adjustment based on learning history"""
        try:
            if self.brain and hasattr(self.brain, 'get_confidence_adjustment_suggestions'):
                adjustment = self.brain.get_confidence_adjustment_suggestions(
                    handler_name="multi_select_handler",
                    question_type=question_type
                )
                
                if adjustment:
                    # Apply conservative adjustments
                    return adjustment * 0.8
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error getting confidence adjustment: {e}")
            return 0.0
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    def _generate_content_key(self, content: str) -> str:
        """Generate a key from content for storage/retrieval"""
        # Extract key parts of the question
        content_lower = content.lower()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = content_lower.split()
        key_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Take first 5 key words
        key = '_'.join(key_words[:5])
        return key[:50]  # Limit length
    
    def _is_exclusive_option(self, option_text: str) -> bool:
        """Check if option is exclusive (like 'None of the above')"""
        exclusive_patterns = [
            'none of', 'none', 'n/a', 'not applicable',
            'do not', "don't", 'neither', 'nothing'
        ]
        option_lower = option_text.lower()
        return any(pattern in option_lower for pattern in exclusive_patterns)
    
    def _get_user_preferences(self, question_type: str) -> Optional[List[str]]:
        """Get user preferences for specific question types"""
        if not self.brain:
            return None
        
        user_profile = self.brain.get("user_profile", {})
        
        # Map question types to profile preferences
        preference_mappings = {
            'activities': user_profile.get('favorite_activities', []),
            'brands': user_profile.get('preferred_brands', []),
            'features': user_profile.get('important_features', []),
            'preferences': user_profile.get('general_preferences', [])
        }
        
        return preference_mappings.get(question_type)
    
    def _update_question_type_defaults(self, question_type: str, selections: List[str]):
        """Update default selections for a question type"""
        try:
            if not self.brain:
                return
            
            key = f"multi_select_{question_type}_defaults"
            defaults = self.brain.get(key, {
                'common_selections': [],
                'selection_frequency': {}
            })
            
            # Update frequency counts
            for selection in selections:
                freq = defaults['selection_frequency'].get(selection, 0)
                defaults['selection_frequency'][selection] = freq + 1
            
            # Update common selections (top 10 most frequent)
            sorted_selections = sorted(
                defaults['selection_frequency'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            defaults['common_selections'] = [s[0] for s in sorted_selections[:10]]
            
            self.brain.set(key, defaults)
            
        except Exception as e:
            print(f"❌ Error updating question type defaults: {e}")
    
    # ========================================
    # STATE TRACKING
    # ========================================
    
    def set_detected_question_type(self, question_type: str):
        """Set the currently detected question type"""
        self.last_question_type = question_type
    
    def get_last_question_type(self) -> Optional[str]:
        """Get the last detected question type"""
        return self.last_question_type
    
    def get_last_selections(self) -> List[str]:
        """Get the last selections made"""
        return self.last_selections
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def __str__(self) -> str:
        """String representation"""
        return f"MultiSelectBrain(connected={self.brain is not None})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"MultiSelectBrain(last_type={self.last_question_type})"