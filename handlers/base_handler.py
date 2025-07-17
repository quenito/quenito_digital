"""
Base Handler Module - FIXED
Abstract base class for all question handlers with common functionality.
Enhanced with Human-Like Timing Manager integration for realistic automation behavior.

FIXED: Added BaseHandler alias to resolve import errors
FIXED: Added missing typing imports
"""

from abc import ABC, abstractmethod
import random
import time
from typing import Dict, Any
from utils.human_timing_manager import HumanLikeTimingManager


class BaseQuestionHandler(ABC):
    """
    Abstract base class for all question handlers.
    Provides common functionality and enforces handler interface.
    Enhanced with realistic human timing patterns.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        self.page = page
        self.knowledge_base = knowledge_base
        self.intervention_manager = intervention_manager
        
        # Initialize enhanced timing manager
        try:
            self.timing_manager = HumanLikeTimingManager()
            print(f"⏱️ Handler initialized with enhanced human timing")
        except Exception as e:
            print(f"⚠️ Could not initialize timing manager: {e}")
            self.timing_manager = None
    
    @abstractmethod
    def can_handle(self, page_content: str) -> float:
        """
        Determine if this handler can process the current question.
        
        Args:
            page_content: The text content of the current page
            
        Returns:
            float: Confidence score between 0.0 and 1.0
                  0.0 = Cannot handle at all
                  1.0 = Perfect match, definitely can handle
        """
        pass
    
    @abstractmethod
    def handle(self) -> bool:
        """
        Process the current question.
        
        Returns:
            bool: True if successfully handled, False if manual intervention needed
        """
        pass
    
    # Enhanced human-like delay with realistic timing patterns
    
    def human_like_delay(self, min_ms=None, max_ms=None, action_type="general", question_content=""):
        """Enhanced human-like delay with realistic timing patterns."""
        
        if hasattr(self, 'timing_manager') and self.timing_manager:
            # Use enhanced timing with question context
            question_type = getattr(self, 'question_type', self._get_handler_question_type())
            complexity = self._assess_question_complexity(question_content)
            
            return self.timing_manager.apply_human_delay(
                action_type=action_type,
                question_type=question_type,
                complexity=complexity,
                question_content=question_content
            )
        else:
            # Fallback to original method
            delay = random.randint(min_ms or 1500, max_ms or 4000) / 1000
            time.sleep(delay)
            return delay

    def _get_handler_question_type(self):
        """Get question type from handler class name."""
        class_name = self.__class__.__name__.lower()
        if 'demographics' in class_name:
            return 'demographics'
        elif 'brand' in class_name:
            return 'brand_familiarity'
        elif 'rating' in class_name:
            return 'rating_matrix'
        else:
            return 'general'

    def _assess_question_complexity(self, question_content):
        """Assess question complexity for timing calculations."""
        if not question_content:
            return 'medium'
        
        content_length = len(question_content)
        word_count = len(question_content.split())
        
        if content_length > 200 or word_count > 30:
            return 'high'
        elif content_length < 50 or word_count < 8:
            return 'low'
        else:
            return 'medium'
    
    # Common utility methods available to all handlers
    
    def get_user_profile(self):
        """Get user profile from knowledge base."""
        return self.knowledge_base.get("user_profile", {})
    
    def get_demographics(self):
        """Get user demographics from knowledge base."""
        return self.get_user_profile().get("demographics", {})
    
    def get_brand_preferences(self):
        """Get user brand preferences from knowledge base."""
        return self.get_user_profile().get("existing_brands", {})
    
    def get_interests(self):
        """Get user interests from knowledge base."""
        return self.get_user_profile().get("interests_and_preferences", {})
    
    def get_question_patterns(self):
        """Get question patterns from knowledge base."""
        return self.knowledge_base.get("question_patterns", {})
    
    def log_success(self, action_description: str):
        """Log successful action with consistent formatting."""
        print(f"✅ {action_description}")
    
    def log_attempt(self, action_description: str):
        """Log attempt with consistent formatting."""
        print(f"🔍 {action_description}")
    
    def log_failure(self, reason: str):
        """Log failure with consistent formatting."""
        print(f"❌ {reason}")
    
    def request_intervention(self, reason: str):
        """Request manual intervention through the intervention manager."""
        if self.intervention_manager:
            return self.intervention_manager.request_intervention(reason)
        else:
            print(f"🔄 Manual intervention needed: {reason}")
            return False

    def log_handler_start(self):
        """Log when handler starts processing."""
        handler_name = self.__class__.__name__
        print(f"🎯 {handler_name} starting...")

    def analyze_page_content(self, content: str) -> Dict[str, Any]:
        """Analyze page content for question patterns."""
        return {
            'content_length': len(content),
            'word_count': len(content.split()),
            'contains_form': 'form' in content.lower(),
            'contains_input': 'input' in content.lower(),
            'contains_select': 'select' in content.lower()
        }


# IMPORTANT FIX: Add BaseHandler alias for import compatibility
BaseHandler = BaseQuestionHandler

# Also add a simple alias for the most common import pattern
class BaseHandler(BaseQuestionHandler):
    """Alias for BaseQuestionHandler to maintain import compatibility."""
    pass