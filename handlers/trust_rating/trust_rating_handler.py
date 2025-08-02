#!/usr/bin/env python3
"""
🎯 Trust Rating Handler v2.0 - REFACTORED MODULAR ARCHITECTURE
Orchestrates trust rating automation using clean module separation.

This handler coordinates:
- Pattern matching (trust_rating_patterns.py)
- UI interactions (trust_rating_ui.py)
- Brain learning (trust_rating_brain.py)

Handles trust scales, reliability ratings, and credibility assessments.
"""

from typing import Dict, List, Any, Optional
from handlers.base_handler import BaseHandler
from .trust_rating_patterns import TrustRatingPatterns
from .trust_rating_ui import TrustRatingUI
from .trust_rating_brain import TrustRatingBrain


class TrustRatingHandler(BaseHandler):
    """
    🎯 Refactored Trust Rating Handler - Clean Orchestration
    
    Expected to boost automation from 40% → 85%!
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Get patterns from knowledge base
        question_patterns = knowledge_base.get("question_patterns", {})
        trust_patterns = question_patterns.get("trust_rating_questions", {})
        
        # Initialize modular components with centralized patterns
        self.patterns = TrustRatingPatterns(trust_patterns)
        self.ui = TrustRatingUI(page)
        self.brain = TrustRatingBrain(knowledge_base)
        
        print("🎯 Refactored Trust Rating Handler initialized!")
        print("🧠 Patterns loaded from centralized knowledge base")
    
    async def can_handle(self, page_content: str) -> float:
        """Determine if this handler can process the current page"""
        if not page_content:
            return 0.0
        
        try:
            # Detect question type using patterns module
            question_type = self.patterns.detect_question_type(page_content)
            if not question_type:
                return 0.0
            
            # Calculate base confidence
            confidence = self.patterns.calculate_keyword_confidence(page_content, question_type)
            
            # Detect entity being rated for additional context
            entity = self.patterns.detect_entity(page_content)
            if entity:
                confidence += 0.05
                print(f"🎯 Detected entity: {entity}")
            
            # Apply brain learning adjustments
            final_confidence = self.brain.calculate_trust_confidence(
                entity or 'unknown',
                confidence
            )
            
            print(f"🎯 Trust Rating confidence: {final_confidence:.3f}")
            return final_confidence
            
        except Exception as e:
            print(f"❌ Error in trust rating can_handle: {e}")
            return 0.0
    
    async def handle(self) -> bool:
        """Process trust rating questions"""
        self.log_handler_start()
        
        try:
            # Get page content
            page_content = await self.page.inner_text('body')
            
            # Detect scale type
            scale_type = self.patterns.detect_scale_type(page_content)
            if not scale_type:
                print("⚠️ Could not detect scale type, trying generic approach")
                scale_type = 'trust_7'  # Default fallback
            
            print(f"🎯 Detected scale type: {scale_type}")
            
            # Detect entity being rated
            entity = self.patterns.detect_entity(page_content) or 'unknown entity'
            
            # Get trust strategy from brain
            strategy = self.brain.get_trust_strategy(entity, page_content)
            print(f"🎯 Using strategy: {strategy}")
            
            # Check if we have learned trust for this entity
            learned_trust = self.brain.get_learned_trust_level(entity, scale_type)
            
            if learned_trust:
                print(f"🧠 Using learned trust level: {learned_trust}")
                trust_value = learned_trust
            else:
                # Get trust value based on strategy
                trust_value = self.patterns.get_trust_value(scale_type, strategy)
            
            # Try text-based selection first
            text_options = self.patterns.get_text_options(strategy)
            for text_option in text_options:
                if await self.ui.select_trust_text_option(text_option):
                    self.brain.store_trust_rating(entity, 0, scale_type, True)
                    await self.ui.try_navigation()
                    return True
            
            # Try numeric selection
            if await self.ui.select_trust_numeric_option(trust_value, scale_type):
                self.brain.store_trust_rating(entity, trust_value, scale_type, True)
                await self.ui.try_navigation()
                return True
            
            # Try scale clicking (for visual scales)
            scale_data = self.patterns.get_scale_data(scale_type)
            if await self.ui.click_scale_position(trust_value, scale_data):
                self.brain.store_trust_rating(entity, trust_value, scale_type, True)
                await self.ui.try_navigation()
                return True
            
            return self.request_intervention("Could not select trust rating")
            
        except Exception as e:
            self.logger.error(f"Trust rating handler error: {e}")
            return self.request_intervention(f"Error: {str(e)}")
    
    def _determine_trust_value(self, scale_type: str, strategy: str) -> int:
        """
        Helper method to determine appropriate trust value
        (Moved most logic to patterns module)
        """
        return self.patterns.get_trust_value(scale_type, strategy)