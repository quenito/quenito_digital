#!/usr/bin/env python3
"""
🧠 Multi-Select Brain Module
Integrates with knowledge base for learning and intelligence
Following the same pattern as brand_familiarity_brain.py
"""

from typing import Dict, List, Any, Optional

class MultiSelectBrain:
    """Brain integration for multi-select learning"""
    
    def __init__(self, knowledge_base):
        """Initialize with knowledge base connection"""
        self.brain = knowledge_base
        self.learned_selections = {}
        self.topic_patterns = {}
        self.success_history = {}
        print("🧠 Multi-Select Brain module initialized")
    
    def get_learned_selections(self, topic: str, options: List[str]) -> Optional[List[str]]:
        """
        Get previously successful selections for a topic
        
        Args:
            topic: The topic/context of the question
            options: Available options to choose from
            
        Returns:
            List of options to select, or None if no learning available
        """
        if not self.brain:
            return None
        
        # Check user preferences for this topic
        user_prefs = self.brain.get('user_profile', {}).get('multi_select_preferences', {})
        if topic in user_prefs:
            preferred = user_prefs[topic]
            # Return options that match user preferences
            return [opt for opt in options if any(pref in opt.lower() for pref in preferred)]
        
        # Check learned patterns
        learned_key = f'multi_select_{topic.lower().replace(" ", "_")}'
        learned = self.brain.get('learned_automations', {}).get(learned_key, {})
        
        if learned and 'selections' in learned:
            # Return previously successful selections that are in current options
            prev_selections = learned['selections']
            return [opt for opt in options if opt in prev_selections]
        
        return None
    
    def calculate_selection_confidence(self, topic: str, base_confidence: float) -> float:
        """Apply learning-based confidence adjustments"""
        confidence = base_confidence
        
        # Boost if we've successfully handled this topic before
        if self.get_learned_selections(topic, []):
            confidence += 0.2
        
        # Check success rate for multi-select questions
        handler_stats = self.brain.get('handler_performance', {}).get('multi_select', {})
        if handler_stats.get('success_rate', 0) > 0.8:
            confidence += 0.1
        
        return min(confidence, 0.98)
    
    def store_successful_selection(self, topic: str, selections: List[str], options: List[str], success: bool):
        """
        Store successful multi-select choices for learning
        
        Args:
            topic: The topic/context of the question
            selections: Options that were selected
            options: All available options
            success: Whether the selection was successful
        """
        if not self.brain:
            return
        
        learning_data = {
            'question_type': f'multi_select_{topic.lower().replace(" ", "_")}',
            'strategy_used': 'checkbox_selection',
            'selections': selections,
            'selection_count': len(selections),
            'total_options': len(options),
            'selection_ratio': len(selections) / len(options) if options else 0,
            'has_exclusive': any('none' in sel.lower() for sel in selections),
            'success': success,
            'execution_time': 2.0,  # Typical time for multi-select
            'confidence_score': 0.9
        }
        
        # Store in learned automations
        self.brain.learn_successful_automation(learning_data)
        
        print(f"🧠 Learned: {topic} → {len(selections)} selections from {len(options)} options")
    
    def get_selection_strategy(self, topic: str, options: List[str]) -> Dict[str, Any]:
        """
        Determine selection strategy based on topic and options
        
        Returns:
            Strategy dict with min/max selections and approach
        """
        # Check if any exclusive options present
        has_exclusive = any(
            any(excl in opt.lower() for excl in ['none', 'n/a', 'not applicable'])
            for opt in options
        )
        
        # If user typically selects "none", use none_strategy
        if has_exclusive and self._user_prefers_none(topic):
            return {
                'name': 'none_strategy',
                'min': 1,
                'max': 1,
                'prefer_exclusive': True
            }
        
        # Otherwise use learned patterns or default to moderate
        learned = self.get_learned_selections(topic, options)
        if learned:
            count = len(learned)
            if count <= 2:
                return {'name': 'conservative', 'min': 1, 'max': 2}
            elif count <= 4:
                return {'name': 'moderate', 'min': 2, 'max': 4}
            else:
                return {'name': 'comprehensive', 'min': 3, 'max': 6}
        
        # Default to moderate strategy
        return {'name': 'moderate', 'min': 2, 'max': 4}
    
    def _user_prefers_none(self, topic: str) -> bool:
        """Check if user typically selects 'none' options for this topic"""
        learned_key = f'multi_select_{topic.lower().replace(" ", "_")}'
        learned = self.brain.get('learned_automations', {}).get(learned_key, {})
        
        if learned and learned.get('has_exclusive'):
            return True
        
        return False
    
    def analyze_topic_patterns(self, topic: str, options: List[str]) -> Dict[str, Any]:
        """Analyze patterns for a specific topic"""
        return {
            'learned_selections': self.get_learned_selections(topic, options),
            'strategy': self.get_selection_strategy(topic, options),
            'confidence_boost': 0.1 if topic in self.topic_patterns else 0.0,
            'has_history': topic in self.learned_selections
        }
    
    def get_option_relevance_scores(self, options: List[str], context: str) -> Dict[str, float]:
        """
        Calculate relevance scores for each option based on context and learning
        
        Returns:
            Dict mapping option to relevance score (0.0 to 1.0)
        """
        scores = {}
        context_lower = context.lower()
        
        for option in options:
            option_lower = option.lower()
            
            # Base score from keyword matching
            score = 0.5
            
            # Boost if option appears in context
            if any(word in context_lower for word in option_lower.split()):
                score += 0.2
            
            # Check if this option was previously selected successfully
            if self._was_previously_selected(option):
                score += 0.3
            
            scores[option] = min(score, 1.0)
        
        return scores
    
    def _was_previously_selected(self, option: str) -> bool:
        """Check if an option was previously selected successfully"""
        if not self.brain:
            return False
        
        # Check all learned multi-select automations
        learned = self.brain.get('learned_automations', {})
        
        for key, data in learned.items():
            if key.startswith('multi_select_') and data.get('success'):
                if option in data.get('selections', []):
                    return True
        
        return False