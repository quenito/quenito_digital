#!/usr/bin/env python3
"""
🧠 Recency Activities Brain Module
Integrates with knowledge base for learning and intelligence
"""

from typing import Dict, List, Any, Optional
import random
from datetime import datetime

class RecencyActivitiesBrain:
    """Brain integration for recency activities learning"""
    
    def __init__(self, knowledge_base):
        """Initialize with knowledge base connection"""
        self.brain = knowledge_base
        self.learned_activities = {}
        self.user_activity_history = []
        print("🧠 Recency Activities Brain module initialized")
    
    def learn_from_manual_selection(self, question_text: str, selected_activities: List[str], 
                                  time_frame: str, user_profile: Dict[str, Any]) -> None:
        """Learn from manual activity selections"""
        try:
            learning_data = {
                'question_text': question_text,
                'selected_activities': selected_activities,
                'time_frame': time_frame,
                'user_profile': user_profile,
                'timestamp': datetime.now().isoformat(),
                'activity_count': len(selected_activities)
            }
            
            # Store in brain
            if hasattr(self.brain, 'store_handler_improvement_pattern'):
                self.brain.store_handler_improvement_pattern(
                    handler_type='recency_activities',
                    pattern_type='activity_selection',
                    pattern_data=learning_data,
                    success_indicator='manual_selection'
                )
                print(f"🧠 Learned activity selection pattern: {len(selected_activities)} activities for {time_frame}")
            
            # Update local history
            self.user_activity_history.append(learning_data)
            
        except Exception as e:
            print(f"❌ Error learning from selection: {e}")
    
    def get_intelligent_activity_selection(self, available_activities: List[str], 
                                         time_frame: str, user_profile: Dict[str, Any],
                                         strategy: Dict[str, Any]) -> List[str]:
        """Generate intelligent activity selection based on learning"""
        selected = []
        
        try:
            # Get learned patterns
            learned_patterns = self._get_learned_patterns(time_frame, user_profile)
            
            # Start with frequently selected activities from learning
            if learned_patterns:
                frequent_activities = self._get_frequent_activities(learned_patterns, available_activities)
                selected.extend(frequent_activities[:strategy.get('max', 7) // 2])
            
            # Add activities based on user profile
            profile_activities = self._get_profile_based_activities(available_activities, user_profile)
            for activity in profile_activities:
                if activity not in selected and len(selected) < strategy.get('max', 7):
                    selected.append(activity)
            
            # Fill remaining with realistic common activities
            common_activities = self._get_common_activities(available_activities)
            for activity in common_activities:
                if activity not in selected and len(selected) < strategy.get('max', 7):
                    selected.append(activity)
            
            # Ensure minimum selection
            if len(selected) < strategy.get('min', 4):
                remaining = [a for a in available_activities if a not in selected and 'none' not in a.lower()]
                random.shuffle(remaining)
                selected.extend(remaining[:strategy.get('min', 4) - len(selected)])
            
            print(f"🧠 Intelligently selected {len(selected)} activities based on learning and profile")
            
        except Exception as e:
            print(f"❌ Error in intelligent selection: {e}")
            # Fallback to random selection
            selected = self._fallback_selection(available_activities, strategy)
        
        return selected[:strategy.get('max', 7)]
    
    def _get_learned_patterns(self, time_frame: str, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve relevant learned patterns"""
        patterns = []
        
        try:
            # Get patterns from brain
            if hasattr(self.brain, 'get_intervention_insights'):
                insights = self.brain.get_intervention_insights('recency_activities')
                if insights and 'patterns' in insights:
                    # Filter by similar time frame and profile
                    for pattern in insights['patterns']:
                        if pattern.get('time_frame') == time_frame:
                            patterns.append(pattern)
            
            # Add local history
            for entry in self.user_activity_history:
                if entry.get('time_frame') == time_frame:
                    patterns.append(entry)
        
        except Exception as e:
            print(f"⚠️ Error retrieving patterns: {e}")
        
        return patterns
    
    def _get_frequent_activities(self, patterns: List[Dict[str, Any]], available: List[str]) -> List[str]:
        """Extract frequently selected activities from patterns"""
        activity_counts = {}
        
        for pattern in patterns:
            for activity in pattern.get('selected_activities', []):
                activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        # Sort by frequency
        sorted_activities = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Match with available activities
        frequent = []
        for activity, _ in sorted_activities:
            for available_activity in available:
                if activity.lower() in available_activity.lower() or available_activity.lower() in activity.lower():
                    if available_activity not in frequent:
                        frequent.append(available_activity)
                        break
        
        return frequent
    
    def _get_profile_based_activities(self, available: List[str], profile: Dict[str, Any]) -> List[str]:
        """Select activities based on user profile"""
        selected = []
        
        age = profile.get('age', 35)
        occupation = profile.get('occupation', '').lower()
        income = profile.get('income', '')
        
        for activity in available:
            activity_lower = activity.lower()
            
            # Age-based selection
            if age < 30 and any(word in activity_lower for word in ['online', 'app', 'streaming', 'gaming']):
                selected.append(activity)
            elif age > 50 and any(word in activity_lower for word in ['doctor', 'medical', 'health']):
                selected.append(activity)
            
            # Occupation-based selection
            if 'business' in occupation and any(word in activity_lower for word in ['travel', 'flight', 'hotel']):
                selected.append(activity)
            elif 'tech' in occupation and any(word in activity_lower for word in ['device', 'software', 'online']):
                selected.append(activity)
            
            # Income-based selection
            if income and 'over' in income.lower() and '$100' in income:
                if any(word in activity_lower for word in ['premium', 'luxury', 'high-end']):
                    selected.append(activity)
        
        return selected
    
    def _get_common_activities(self, available: List[str]) -> List[str]:
        """Get universally common activities"""
        common_keywords = [
            'online purchase', 'restaurant', 'movie', 'haircut',
            'doctor', 'shopping', 'delivery', 'subscription'
        ]
        
        selected = []
        for activity in available:
            activity_lower = activity.lower()
            if any(keyword in activity_lower for keyword in common_keywords):
                selected.append(activity)
        
        return selected
    
    def _fallback_selection(self, available: List[str], strategy: Dict[str, Any]) -> List[str]:
        """Fallback random selection when intelligent selection fails"""
        # Filter out 'none' options
        valid_activities = [a for a in available if 'none' not in a.lower()]
        
        # Random selection within strategy limits
        num_to_select = random.randint(strategy.get('min', 4), strategy.get('max', 7))
        num_to_select = min(num_to_select, len(valid_activities))
        
        return random.sample(valid_activities, num_to_select)
    
    def analyze_activity_patterns(self) -> Dict[str, Any]:
        """Analyze learned activity patterns for reporting"""
        analysis = {
            'total_interactions': len(self.user_activity_history),
            'average_activities_selected': 0,
            'most_common_activities': [],
            'time_frame_distribution': {},
            'learning_effectiveness': 0
        }
        
        if not self.user_activity_history:
            return analysis
        
        # Calculate averages
        total_activities = sum(entry.get('activity_count', 0) for entry in self.user_activity_history)
        analysis['average_activities_selected'] = total_activities / len(self.user_activity_history)
        
        # Time frame distribution
        for entry in self.user_activity_history:
            time_frame = entry.get('time_frame', 'unknown')
            analysis['time_frame_distribution'][time_frame] = \
                analysis['time_frame_distribution'].get(time_frame, 0) + 1
        
        # Most common activities
        activity_counts = {}
        for entry in self.user_activity_history:
            for activity in entry.get('selected_activities', []):
                activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        analysis['most_common_activities'] = sorted(
            activity_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Learning effectiveness (placeholder - would need success metrics)
        analysis['learning_effectiveness'] = min(len(self.user_activity_history) * 10, 85)
        
        return analysis