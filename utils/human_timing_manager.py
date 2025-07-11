#!/usr/bin/env python3
"""
Human-Like Timing Manager
Realistic timing patterns for enhanced stealth and human-like behavior.
"""

import random
import time
import statistics
from typing import Dict, Tuple, List


class HumanLikeTimingManager:
    """
    Advanced timing manager that simulates realistic human behavior patterns.
    Includes question complexity analysis, typing simulation, and personal variation.
    """
    
    def __init__(self):
        # Simulated user characteristics
        self.user_typing_speed = random.uniform(40, 80)  # WPM (words per minute)
        self.user_reading_speed = random.uniform(200, 300)  # WPM
        self.user_decision_speed = random.uniform(0.8, 1.4)  # Multiplier for decision making
        
        # Base timing patterns for different question types
        self.thinking_patterns = {
            'simple_question': (1.2, 3.5),      # Easy yes/no, basic demographics
            'complex_question': (3.0, 8.0),     # Multi-part, research required
            'demographic': (0.8, 2.5),          # Age, gender, location
            'opinion': (2.0, 6.0),              # Rating scales, preferences
            'brand_familiarity': (1.5, 4.0),    # Brand awareness questions
            'rating_matrix': (2.5, 7.0),        # Multiple ratings
            'multi_select': (3.0, 8.0),         # Multiple choice selection
            'trust_rating': (2.0, 5.0),         # Trust/reliability scales
            'unknown': (2.0, 6.0)               # Unknown question types
        }
        
        # Reading time factors
        self.reading_factors = {
            'short_text': 0.5,      # < 50 characters
            'medium_text': 1.0,     # 50-200 characters  
            'long_text': 1.8,       # > 200 characters
            'complex_text': 2.2     # Technical/complex content
        }
        
        # Personal timing variations throughout session
        self.session_fatigue = 1.0  # Increases over time
        self.session_start_time = time.time()
        self.actions_taken = 0
        
        print(f"🕒 Human Timing Profile: {self.user_typing_speed:.0f} WPM typing, {self.user_reading_speed:.0f} WPM reading")
    
    def calculate_human_delay(self, action_type: str, content_complexity: str = "medium", 
                            content_length: int = 100, question_content: str = "") -> float:
        """
        Calculate realistic human delay based on multiple factors.
        
        Args:
            action_type: Type of action/question
            content_complexity: 'simple', 'medium', 'complex'
            content_length: Length of content to read
            question_content: Actual question text for analysis
            
        Returns:
            float: Delay in seconds
        """
        # Get base timing range
        base_range = self.thinking_patterns.get(action_type, (2.0, 5.0))
        
        # Calculate reading time
        reading_time = self._calculate_reading_time(content_length, question_content)
        
        # Calculate thinking time
        thinking_time = self._calculate_thinking_time(base_range, content_complexity)
        
        # Apply personal factors
        personal_factor = self._get_personal_timing_factor()
        
        # Apply session factors (fatigue, consistency)
        session_factor = self._get_session_timing_factor()
        
        # Combine all factors
        total_delay = (reading_time + thinking_time) * personal_factor * session_factor
        
        # Add small random variations (micro-hesitations)
        micro_variation = random.uniform(0.1, 0.3)
        total_delay += micro_variation
        
        # Ensure minimum and maximum bounds
        min_delay = 0.5  # Never too fast
        max_delay = 15.0  # Never too slow
        
        final_delay = max(min_delay, min(total_delay, max_delay))
        
        # Update session tracking
        self.actions_taken += 1
        self._update_session_fatigue()
        
        return final_delay
    
    def _calculate_reading_time(self, content_length: int, content: str = "") -> float:
        """Calculate time needed to read content."""
        if content_length == 0:
            return 0.1
        
        # Estimate words (average 5 characters per word)
        estimated_words = content_length / 5
        
        # Base reading time
        reading_time = estimated_words / (self.user_reading_speed / 60)  # Convert WPM to words per second
        
        # Complexity adjustment
        complexity_factor = 1.0
        if content:
            content_lower = content.lower()
            # Check for complex content
            complex_indicators = ['research', 'documentary', 'sponsor', 'venue', 'statistical']
            if any(indicator in content_lower for indicator in complex_indicators):
                complexity_factor = 1.5
        
        return reading_time * complexity_factor
    
    def _calculate_thinking_time(self, base_range: Tuple[float, float], complexity: str) -> float:
        """Calculate thinking/decision time."""
        min_time, max_time = base_range
        
        # Complexity multiplier
        complexity_multipliers = {
            'simple': 0.7,
            'medium': 1.0,
            'complex': 1.4,
            'very_complex': 1.8
        }
        
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        # Apply decision speed personal factor
        adjusted_min = min_time * multiplier / self.user_decision_speed
        adjusted_max = max_time * multiplier / self.user_decision_speed
        
        # Random selection within range
        thinking_time = random.uniform(adjusted_min, adjusted_max)
        
        return thinking_time
    
    def _get_personal_timing_factor(self) -> float:
        """Get personal timing variation factor."""
        # Each person has consistent but slightly variable timing
        base_consistency = random.uniform(0.85, 1.15)
        
        # Small random variation for each action
        action_variation = random.uniform(0.95, 1.05)
        
        return base_consistency * action_variation
    
    def _get_session_timing_factor(self) -> float:
        """Get session-based timing factor (fatigue, rhythm)."""
        # Session duration effect
        session_duration = time.time() - self.session_start_time
        session_minutes = session_duration / 60
        
        # Slight slowdown over time (fatigue)
        fatigue_factor = 1.0 + (session_minutes * 0.01)  # 1% slower per minute
        
        # Rhythm factor (people get into a rhythm)
        if self.actions_taken > 5:
            rhythm_factor = random.uniform(0.95, 1.02)  # Slight speedup when in rhythm
        else:
            rhythm_factor = random.uniform(1.0, 1.1)    # Slightly slower when starting
        
        return fatigue_factor * rhythm_factor
    
    def _update_session_fatigue(self):
        """Update session fatigue factor."""
        # Gradual increase in fatigue
        self.session_fatigue += random.uniform(0.001, 0.005)
    
    def typing_delay_for_text(self, text_length: int, text_content: str = "") -> float:
        """
        Calculate realistic typing delay with pauses and corrections.
        
        Args:
            text_length: Length of text to type
            text_content: Actual text content
            
        Returns:
            float: Typing delay in seconds
        """
        if text_length == 0:
            return 0.1
        
        # Base typing time
        characters_per_second = (self.user_typing_speed * 5) / 60  # Convert WPM to chars/sec
        base_typing_time = text_length / characters_per_second
        
        # Add thinking pauses (people pause while typing)
        thinking_pauses = random.randint(0, max(1, text_length // 8))
        pause_time = thinking_pauses * random.uniform(0.3, 1.2)
        
        # Add small corrections/backspaces
        corrections = random.randint(0, max(1, text_length // 15))
        correction_time = corrections * random.uniform(0.5, 1.5)
        
        # Add start/finish delay (positioning cursor, checking result)
        start_delay = random.uniform(0.2, 0.8)
        finish_delay = random.uniform(0.1, 0.5)
        
        total_time = base_typing_time + pause_time + correction_time + start_delay + finish_delay
        
        return total_time
    
    def mouse_movement_delay(self, distance_category: str = "medium") -> float:
        """
        Calculate realistic mouse movement delay.
        
        Args:
            distance_category: 'short', 'medium', 'long'
            
        Returns:
            float: Mouse movement delay in seconds
        """
        distance_times = {
            'short': (0.1, 0.3),    # Same area of screen
            'medium': (0.2, 0.6),   # Across part of screen
            'long': (0.4, 1.0)      # Across full screen
        }
        
        min_time, max_time = distance_times.get(distance_category, (0.2, 0.6))
        
        # Add personal coordination factor
        coordination_factor = random.uniform(0.8, 1.3)
        
        base_time = random.uniform(min_time, max_time)
        return base_time * coordination_factor
    
    def page_load_wait_time(self, expected_load_time: str = "normal") -> float:
        """
        Calculate realistic page load waiting time.
        
        Args:
            expected_load_time: 'fast', 'normal', 'slow'
            
        Returns:
            float: Wait time in seconds
        """
        load_expectations = {
            'fast': (0.5, 1.5),      # Quick page updates
            'normal': (1.0, 3.0),    # Normal page loads
            'slow': (2.0, 5.0)       # Complex pages
        }
        
        min_wait, max_wait = load_expectations.get(expected_load_time, (1.0, 3.0))
        
        # Add personal patience factor
        patience_factor = random.uniform(0.7, 1.4)
        
        base_wait = random.uniform(min_wait, max_wait)
        return base_wait * patience_factor
    
    def get_question_complexity(self, question_content: str) -> str:
        """
        Analyze question content to determine complexity level.
        
        Args:
            question_content: The question text to analyze
            
        Returns:
            str: Complexity level ('simple', 'medium', 'complex', 'very_complex')
        """
        if not question_content:
            return "medium"
        
        content_lower = question_content.lower()
        content_length = len(question_content)
        
        # Simple questions
        simple_indicators = [
            'age', 'gender', 'male', 'female', 'yes', 'no',
            'select one', 'choose one', 'click'
        ]
        
        # Complex questions
        complex_indicators = [
            'research', 'documentary', 'sponsor', 'venue', 'stadium',
            'which company', 'what is the name of', 'multiple',
            'select all that apply', 'rate each', 'agreement'
        ]
        
        # Very complex questions
        very_complex_indicators = [
            'matrix', 'grid', 'table', 'multiple parts',
            'several questions', 'compare', 'analyze'
        ]
        
        # Count indicators
        simple_count = sum(1 for indicator in simple_indicators if indicator in content_lower)
        complex_count = sum(1 for indicator in complex_indicators if indicator in content_lower)
        very_complex_count = sum(1 for indicator in very_complex_indicators if indicator in content_lower)
        
        # Length-based complexity
        if content_length > 500:
            length_complexity = "complex"
        elif content_length > 200:
            length_complexity = "medium"
        else:
            length_complexity = "simple"
        
        # Determine final complexity
        if very_complex_count > 0 or length_complexity == "complex":
            return "very_complex"
        elif complex_count > simple_count or length_complexity == "medium":
            return "complex"
        elif simple_count > 0 and content_length < 100:
            return "simple"
        else:
            return "medium"
    
    def apply_human_delay(self, action_type: str, question_content: str = "", 
                         content_length: int = None) -> None:
        """
        Apply human-like delay with comprehensive timing analysis.
        
        Args:
            action_type: Type of action being performed
            question_content: The question text for analysis
            content_length: Override content length if needed
        """
        if content_length is None:
            content_length = len(question_content)
        
        # Determine complexity
        complexity = self.get_question_complexity(question_content)
        
        # Calculate delay
        delay = self.calculate_human_delay(
            action_type=action_type,
            content_complexity=complexity,
            content_length=content_length,
            question_content=question_content
        )
        
        # Apply the delay
        print(f"🕒 Human timing: {delay:.1f}s for {action_type} ({complexity} complexity)")
        time.sleep(delay)
    
    def apply_typing_delay(self, text: str) -> None:
        """
        Apply realistic typing delay.
        
        Args:
            text: Text that would be typed
        """
        delay = self.typing_delay_for_text(len(text), text)
        print(f"⌨️ Typing delay: {delay:.1f}s for {len(text)} characters")
        time.sleep(delay)
    
    def apply_mouse_delay(self, distance: str = "medium") -> None:
        """
        Apply realistic mouse movement delay.
        
        Args:
            distance: Distance category ('short', 'medium', 'long')
        """
        delay = self.mouse_movement_delay(distance)
        print(f"🖱️ Mouse delay: {delay:.1f}s for {distance} movement")
        time.sleep(delay)
    
    def apply_page_wait(self, load_type: str = "normal") -> None:
        """
        Apply realistic page load waiting time.
        
        Args:
            load_type: Expected load time ('fast', 'normal', 'slow')
        """
        delay = self.page_load_wait_time(load_type)
        print(f"⏳ Page wait: {delay:.1f}s for {load_type} load")
        time.sleep(delay)
    
    def get_timing_stats(self) -> Dict[str, Any]:
        """Get current timing statistics and user profile."""
        session_duration = time.time() - self.session_start_time
        
        return {
            "user_profile": {
                "typing_speed_wpm": self.user_typing_speed,
                "reading_speed_wpm": self.user_reading_speed,
                "decision_speed_factor": self.user_decision_speed
            },
            "session_stats": {
                "duration_minutes": session_duration / 60,
                "actions_taken": self.actions_taken,
                "current_fatigue": self.session_fatigue,
                "avg_action_interval": session_duration / max(1, self.actions_taken)
            },
            "timing_patterns": self.thinking_patterns
        }
    
    def reset_session(self):
        """Reset session-based timing factors."""
        self.session_start_time = time.time()
        self.actions_taken = 0
        self.session_fatigue = 1.0
        print("🔄 Timing session reset - fresh start!")
    
    def simulate_human_hesitation(self, probability: float = 0.3) -> None:
        """
        Occasionally simulate human hesitation/uncertainty.
        
        Args:
            probability: Chance of hesitation (0.0 to 1.0)
        """
        if random.random() < probability:
            hesitation_time = random.uniform(0.5, 2.0)
            print(f"🤔 Human hesitation: {hesitation_time:.1f}s")
            time.sleep(hesitation_time)
    
    def simulate_micro_break(self, probability: float = 0.1) -> None:
        """
        Occasionally simulate very brief micro-breaks.
        
        Args:
            probability: Chance of micro-break (0.0 to 1.0)
        """
        if random.random() < probability:
            break_time = random.uniform(1.0, 3.0)
            print(f"☕ Micro-break: {break_time:.1f}s")
            time.sleep(break_time)
            