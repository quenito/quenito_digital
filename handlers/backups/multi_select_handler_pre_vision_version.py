#!/usr/bin/env python3
"""
☑️ Multi-Select Handler v2.0 - REFACTORED MODULAR ARCHITECTURE
Orchestrates multi-select question automation using clean module separation.

This handler coordinates:
- Pattern matching (multi_select_patterns.py)
- UI interactions (multi_select_ui.py)
- Brain learning (multi_select_brain.py)

Handles checkbox questions, multiple choice selections, and "select all that apply" formats.
"""

from typing import Dict, List, Any, Optional
from handlers.base_handler import BaseHandler
from .multi_select_patterns import MultiSelectPatterns
from .multi_select_ui import MultiSelectUI
from .multi_select_brain import MultiSelectBrain


class MultiSelectHandler(BaseHandler):
    """
    ☑️ Refactored Multi-Select Handler - Clean Orchestration
    
    Expected to boost automation from 30% → 85-90%!
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Get patterns from knowledge base
        question_patterns = knowledge_base.get("question_patterns", {})
        multi_patterns = question_patterns.get("multi_select_questions", {})
        
        # Initialize modular components with centralized patterns
        self.patterns = MultiSelectPatterns(multi_patterns)
        self.ui = MultiSelectUI(page)
        self.brain = MultiSelectBrain(knowledge_base)
        
        print("☑️ Refactored Multi-Select Handler initialized!")
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
            
            # Detect topic for additional context
            topic = self.patterns.detect_topic_category(page_content)
            if topic:
                confidence += 0.05
                print(f"☑️ Detected topic: {topic}")
            
            # Apply brain learning adjustments
            final_confidence = self.brain.calculate_selection_confidence(
                topic or 'general',
                confidence
            )
            
            print(f"☑️ Multi-Select confidence: {final_confidence:.3f}")
            return final_confidence
            
        except Exception as e:
            print(f"❌ Error in multi-select can_handle: {e}")
            return 0.0
    
    async def handle(self) -> bool:
        """Process multi-select questions"""
        self.log_handler_start()
        
        try:
            # Detect all checkboxes
            checkboxes = await self.ui.detect_all_checkboxes()
            
            if not checkboxes:
                print("❌ No checkboxes detected")
                return self.request_intervention("No checkboxes found")
            
            print(f"☑️ Found {len(checkboxes)} checkboxes")
            
            # Get checkbox labels
            options = []
            for checkbox in checkboxes:
                label = await self.ui.get_checkbox_label(checkbox)
                if label:
                    options.append(label)
            
            # Detect if exclusive option present
            has_exclusive = self.patterns.has_exclusive_option(' '.join(options))
            
            # Get topic/context
            page_content = await self.page.inner_text('body')
            topic = self.patterns.detect_topic_category(page_content) or 'general'
            
            # Get selection strategy from brain
            strategy = self.brain.get_selection_strategy(topic, options)
            
            # Determine which options to select
            if strategy.get('prefer_exclusive') and has_exclusive:
                # Handle exclusive option
                for option in options:
                    if self.patterns.is_exclusive_option(option):
                        success = await self.ui.handle_exclusive_option(option)
                        if success:
                            self.brain.store_successful_selection(
                                topic, [option], options, True
                            )
                        return success
            else:
                # Select multiple options based on strategy
                selections = self._choose_selections(
                    options, 
                    strategy,
                    topic
                )
                
                # Apply selections
                results = await self.ui.select_multiple_checkboxes(selections)
                
                # Count successes
                success_count = sum(1 for s in results.values() if s)
                
                if success_count > 0:
                    # Store learning
                    selected = [s for s, v in results.items() if v]
                    self.brain.store_successful_selection(
                        topic, selected, options, True
                    )
                    
                    # Navigate to next
                    await self.ui.try_navigation()
                    return True
                
            return self.request_intervention("Failed to select checkboxes")
            
        except Exception as e:
            self.logger.error(f"Multi-select handler error: {e}")
            return self.request_intervention(f"Error: {str(e)}")
    
    def _choose_selections(self, options: List[str], strategy: Dict[str, Any], topic: str) -> List[str]:
        """Choose which options to select based on strategy and learning"""
        selections = []
        
        # First check if brain has learned selections for this topic
        learned = self.brain.get_learned_selections(topic, options)
        if learned:
            return learned[:strategy.get('max', 4)]
        
        # Otherwise use relevance scoring
        scores = self.brain.get_option_relevance_scores(options, topic)
        
        # Sort options by score
        sorted_options = sorted(
            options,
            key=lambda o: scores.get(o, 0.5),
            reverse=True
        )
        
        # Select based on strategy limits
        min_select = strategy.get('min', 1)
        max_select = strategy.get('max', 4)
        
        # Select top scoring options
        for i, option in enumerate(sorted_options):
            if self.patterns.is_exclusive_option(option):
                continue  # Skip exclusive options in multi-select
            
            if scores.get(option, 0.5) >= 0.3:  # Minimum relevance
                selections.append(option)
                
            if len(selections) >= max_select:
                break
        
        # Ensure minimum selections
        if len(selections) < min_select and sorted_options:
            for option in sorted_options:
                if option not in selections and not self.patterns.is_exclusive_option(option):
                    selections.append(option)
                    if len(selections) >= min_select:
                        break
        
        return selections