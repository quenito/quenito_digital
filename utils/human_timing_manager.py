#!/usr/bin/env python3
"""
Human-Like Timing Manager (Standalone Version)
Realistic timing patterns with complexity-based delays and personal variations.
No dependencies on other utils modules.
"""

import random
import time
from typing import Dict, Tuple


class HumanLikeTimingManager:
    """
    Advanced human-like timing with complexity analysis and personal patterns.
    Creates realistic delays that match how humans actually interact with surveys.
    """
    
    def __init__(self):
        """Initialize with personal characteristics that vary per session."""
        # Personal characteristics (varies per session to simulate different users)
        self.user_typing_speed = random.uniform(40, 80)  # Words per minute
        self.thinking_speed = random.uniform(0.8, 1.3)   # How fast they think
        self.decision_confidence = random.uniform(0.7, 1.1)  # Decision making speed
        
        print(f"🧠 Human Profile: {self.user_typing_speed:.0f} WPM, "
              f"thinking speed {self.thinking_speed:.1f}x, "
              f"decision confidence {self.decision_confidence:.1f}x")
        
        # Base timing patterns for different question types (min_seconds, max_seconds)
        self.timing_patterns = {
            'demographics': (0.8, 2.5),      # Quick factual questions (age, gender)
            'simple_rating': (1.2, 3.5),     # Basic 1-5 rating scales
            'complex_rating': (2.5, 6.0),    # Complex rating matrices
            'multi_select': (2.0, 5.0),      # Multiple choice with multiple answers
            'opinion': (3.0, 8.0),           # Opinion questions requiring thought
            'brand_familiarity': (1.5, 4.0), # Brand awareness questions
            'research_required': (4.0, 12.0), # Questions needing research
            'unknown': (2.0, 6.0)            # Unknown question types
        }
    
    def calculate_human_delay(self, question_type: str, complexity: str, 
                            content_length: int, question_content: str = "") -> float:
        """
        Calculate realistic human delay based on multiple factors.
        
        Args:
            question_type: Type of question (demographics, opinion, etc.)
            complexity: Complexity level (simple, medium, complex)
            content_length: Length of question content in characters
            question_content: Actual question text for analysis
            
        Returns:
            float: Delay in seconds (realistic human timing)
        """
        # Step 1: Get base timing range for this question type
        base_range = self.timing_patterns.get(question_type, (2.0, 6.0))
        
        # Step 2: Apply complexity multiplier
        complexity_multipliers = {
            'simple': 0.7,      # 30% faster for simple questions
            'medium': 1.0,      # Normal speed
            'complex': 1.4      # 40% slower for complex questions
        }
        complexity_factor = complexity_multipliers.get(complexity, 1.0)
        
        # Step 3: Content length factor (longer content = more reading time)
        # Every 500 characters adds 30% more time
        content_factor = 1.0 + (content_length / 500) * 0.3
        
        # Step 4: Analyze question complexity from actual content
        question_complexity_factor = self._analyze_question_complexity(question_content)
        
        # Step 5: Apply personal characteristics
        personal_factor = self.thinking_speed * self.decision_confidence
        
        # Step 6: Calculate final timing range
        min_delay = (base_range[0] * complexity_factor * content_factor * 
                    question_complexity_factor * personal_factor)
        max_delay = (base_range[1] * complexity_factor * content_factor * 
                    question_complexity_factor * personal_factor)
        
        # Step 7: Add random variation within the range
        final_delay = random.uniform(min_delay, max_delay)
        
        # Step 8: Ensure minimum realistic delay (humans need at least 0.8 seconds)
        return max(final_delay, 0.8)
    
    def _analyze_question_complexity(self, question_content: str) -> float:
        """
        Analyze question content for complexity indicators.
        Returns a multiplier based on how complex the question appears.
        """
        if not question_content:
            return 1.0
            
        # Keywords that indicate different complexity levels
        complexity_keywords = {
            'simple': ['age', 'gender', 'name', 'yes', 'no', 'select', 'choose'],
            'medium': ['opinion', 'think', 'feel', 'rate', 'scale', 'how much', 'how often'],
            'complex': ['compare', 'analyze', 'evaluate', 'explain', 'why', 'likelihood', 
                       'relationship', 'influence', 'impact', 'consider all']
        }
        
        content_lower = question_content.lower()
        
        # Count complexity indicators
        simple_count = sum(1 for word in complexity_keywords['simple'] if word in content_lower)
        medium_count = sum(1 for word in complexity_keywords['medium'] if word in content_lower)
        complex_count = sum(1 for word in complexity_keywords['complex'] if word in content_lower)
        
        # Calculate complexity factor
        if complex_count > 0:
            return 1.3 + (complex_count * 0.2)  # 30% base + 20% per complex word
        elif medium_count > 0:
            return 1.0 + (medium_count * 0.1)   # Normal + 10% per medium word
        else:
            return 0.8 + (simple_count * 0.05)  # 20% faster + 5% per simple word
    
    def typing_delay_for_text(self, text: str) -> float:
        """
        Calculate realistic typing delay for text input.
        Simulates actual human typing with pauses and corrections.
        """
        if not text:
            return 0
            
        # Step 1: Calculate base typing time
        chars_per_second = self.user_typing_speed / 60 * 5  # Convert WPM to chars/second
        base_time = len(text) / chars_per_second
        
        # Step 2: Add thinking pauses (humans pause every 10-15 characters to think)
        pause_points = len(text) // random.randint(10, 15)
        pause_time = pause_points * random.uniform(0.3, 1.2)
        
        # Step 3: Add correction time (humans occasionally backspace and retype)
        correction_chance = 0.15  # 15% chance of making a correction
        correction_time = 0
        if random.random() < correction_chance:
            correction_time = random.uniform(0.5, 2.0)
        
        total_time = base_time + pause_time + correction_time
        return max(total_time, 0.5)  # Minimum 0.5 seconds even for short text
    
    def apply_human_delay(self, action_type: str = "general", question_type: str = "unknown", 
                         complexity: str = "medium", question_content: str = "") -> float:
        """
        Apply human-like delay based on action and question context.
        This is the main method you'll call from your handlers.
        
        Args:
            action_type: Type of action (reading, clicking, typing, etc.)
            question_type: Type of question being processed
            complexity: Complexity level of the question
            question_content: Question text for analysis
            
        Returns:
            float: Actual delay applied in seconds
        """
        # Calculate appropriate delay based on question
        content_length = len(question_content) if question_content else 100
        delay = self.calculate_human_delay(question_type, complexity, content_length, question_content)
        
        # Apply action-specific adjustments
        action_multipliers = {
            'reading': 0.8,      # Reading is faster than decision making
            'clicking': 0.6,     # Quick physical action
            'typing': 1.2,       # Slower due to physical input
            'thinking': 1.4,     # Extra time for complex decisions
            'scrolling': 0.5,    # Quick scrolling action
            'general': 1.0       # Default timing
        }
        
        # Calculate final delay
        final_delay = delay * action_multipliers.get(action_type, 1.0)
        
        # Add a small random variation (±10%) to make it even more human-like
        variation = random.uniform(0.9, 1.1)
        final_delay *= variation
        
        # Ensure reasonable bounds (0.3 to 15 seconds max)
        final_delay = max(0.3, min(final_delay, 15.0))
        
        # Apply the delay
        print(f"⏱️ Human timing: {final_delay:.1f}s ({action_type} on {question_type})")
        time.sleep(final_delay)
        
        return final_delay
    
    def quick_delay(self, min_seconds: float = 0.5, max_seconds: float = 1.5) -> float:
        """
        Quick delay for simple actions like page loads or navigation.
        
        Args:
            min_seconds: Minimum delay time
            max_seconds: Maximum delay time
            
        Returns:
            float: Actual delay applied
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    def reading_delay(self, text_length: int) -> float:
        """
        Delay for reading text content.
        Assumes average reading speed of 200-300 words per minute.
        
        Args:
            text_length: Length of text to read in characters
            
        Returns:
            float: Reading delay in seconds
        """
        # Average reading speed: 250 words per minute = ~1250 characters per minute
        reading_speed_chars_per_second = 1250 / 60  # ~21 chars per second
        
        # Calculate base reading time
        base_reading_time = text_length / reading_speed_chars_per_second
        
        # Add processing time (humans need time to understand, not just read)
        processing_time = base_reading_time * random.uniform(0.3, 0.7)
        
        total_time = base_reading_time + processing_time
        
        # Apply bounds (minimum 0.5 seconds, maximum 10 seconds for reading)
        final_time = max(0.5, min(total_time, 10.0))
        
        print(f"📖 Reading delay: {final_time:.1f}s for {text_length} characters")
        time.sleep(final_time)
        
        return final_time


# Test the timing manager if run directly
if __name__ == "__main__":
    print("🧪 Testing Human-Like Timing Manager")
    print("=" * 40)
    
    # Create a timing manager instance
    timing = HumanLikeTimingManager()
    
    # Test different scenarios
    test_scenarios = [
        ("demographics", "simple", "What is your age?"),
        ("opinion", "complex", "How do you feel about the environmental impact of social media platforms and their responsibility for climate change?"),
        ("brand_familiarity", "medium", "How familiar are you with the following brands?"),
        ("multi_select", "medium", "Which of the following activities do you enjoy? (Select all that apply)")
    ]
    
    print("\n🎯 Testing timing patterns:")
    for question_type, complexity, question in test_scenarios:
        delay = timing.calculate_human_delay(
            question_type=question_type, 
            complexity=complexity, 
            content_length=len(question),
            question_content=question
        )
        print(f"   {question_type:15} ({complexity:7}): {delay:.1f}s")
    
    print("\n📖 Testing reading delay:")
    long_text = "This is a longer piece of text that might appear in a survey question or instructions. It requires more time to read and understand properly."
    reading_time = timing.reading_delay(len(long_text))
    
    print("\n✅ Human-Like Timing Manager test completed!")
    print("🎉 Ready for integration with your survey automation system!")