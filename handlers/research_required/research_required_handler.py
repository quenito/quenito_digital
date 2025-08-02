#!/usr/bin/env python3
"""
🔬 Research Required Handler - Main Orchestrator
Refactored to use modular architecture with centralized patterns
"""

from typing import Dict, List, Any, Optional, Tuple
import asyncio
from ..base_handler import BaseHandler
from .research_required_patterns import ResearchRequiredPatterns
from .research_required_ui import ResearchRequiredUI
from .research_required_brain import ResearchRequiredBrain

class ResearchRequiredHandler(BaseHandler):
    """
    Handles research-based questions using modular architecture
    Examples: "Please research the following...", "Look up information about..."
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Get patterns from knowledge base
        question_patterns = knowledge_base.get("question_patterns", {})
        research_patterns = question_patterns.get("research_required_questions", {})
        
        # Initialize modular components
        self.patterns = ResearchRequiredPatterns(research_patterns)
        self.ui = ResearchRequiredUI(page)
        self.brain = ResearchRequiredBrain(knowledge_base)
        
        # Get user preferences
        self.user_preferences = self._get_user_preferences()
        
        print("🔬 Refactored Research Required Handler initialized!")
        print("🧠 Patterns loaded from centralized knowledge base")
    
    async def can_handle(self, question_text: str) -> Tuple[bool, float]:
        """
        Determine if this handler can handle the question
        Returns: (can_handle, confidence_score)
        """
        try:
            # Calculate confidence using patterns module
            confidence = self.patterns.calculate_confidence(question_text)
            
            # Check if it's actually a research instruction
            if self.patterns.is_research_instruction(question_text):
                confidence += 0.2  # Boost for clear instructions
            
            # Log decision
            if confidence > 0.3:  # Lower threshold for research questions
                print(f"🔬 Research Required: CAN handle (confidence: {confidence:.2f})")
                print(f"📝 Question: {question_text[:100]}...")
                return True, confidence
            else:
                return False, confidence
                
        except Exception as e:
            print(f"❌ Error in can_handle: {e}")
            return False, 0.0
    
    async def handle(self, question_text: str) -> bool:
        """
        Handle the research required question
        Returns: True if handled successfully, False otherwise
        """
        try:
            print("\n" + "="*50)
            print("🔬 HANDLING RESEARCH REQUIRED QUESTION")
            print("="*50)
            
            # Detect research type
            research_type = self.patterns.detect_research_type(question_text)
            print(f"📊 Research type: {research_type}")
            
            # Extract research topics if any
            topics = self.patterns.extract_research_topics(question_text)
            if topics:
                print(f"📋 Research topics identified: {', '.join(topics[:3])}")
            
            # Check if we should attempt this
            complexity = self._assess_complexity(question_text, topics)
            if not self.brain.should_attempt_research(research_type, complexity):
                print("❌ Research too complex based on historical data")
                return False
            
            # Detect UI elements
            elements = await self.ui.detect_ui_elements()
            if not any(elements.values()):
                print("❌ No suitable UI elements found")
                return False
            
            # Check if field is required
            is_required = await self.ui.check_for_required_field(elements)
            print(f"📝 Field required: {is_required}")
            
            # Determine available strategies
            available_strategies = []
            
            # Check skip availability
            if elements['skip_button'] or not is_required:
                available_strategies.append('skip')
            
            # Placeholder is always available if we have input fields
            if elements['text_areas'] or elements['text_inputs']:
                available_strategies.append('placeholder')
                available_strategies.append('acknowledge')
            
            if not available_strategies:
                print("❌ No available strategies for handling")
                return False
            
            print(f"📊 Available strategies: {', '.join(available_strategies)}")
            
            # Get best strategy from brain
            strategy = self.brain.get_best_strategy(research_type, available_strategies)
            print(f"🧠 Selected strategy: {strategy}")
            
            # Execute strategy
            success = False
            
            if strategy == 'skip':
                success = await self._handle_skip_strategy(elements)
            
            elif strategy == 'placeholder':
                placeholder = self.brain.generate_intelligent_placeholder(research_type, topics)
                success = await self._handle_placeholder_strategy(elements, placeholder)
            
            elif strategy == 'acknowledge':
                acknowledgment = self.patterns.get_acknowledgment_response(research_type)
                success = await self._handle_acknowledge_strategy(elements, acknowledgment)
            
            # Learn from the result
            self.brain.learn_from_research_handling(
                question_text,
                strategy,
                success,
                research_type
            )
            
            if success:
                print(f"\n✅ Successfully handled research question using {strategy} strategy!")
                
                # Store successful automation data
                await self._store_automation_success(
                    question_text,
                    strategy,
                    research_type
                )
            else:
                print(f"❌ Failed to handle research question with {strategy} strategy")
            
            return success
                
        except Exception as e:
            print(f"❌ Error handling research question: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _handle_skip_strategy(self, elements: Dict[str, Any]) -> bool:
        """Execute skip strategy"""
        print("⏭️ Attempting to skip research question...")
        return await self.ui.handle_skip(elements)
    
    async def _handle_placeholder_strategy(self, elements: Dict[str, Any], placeholder: str) -> bool:
        """Execute placeholder strategy"""
        print(f"📝 Submitting placeholder: {placeholder}")
        return await self.ui.submit_placeholder_response(elements, placeholder)
    
    async def _handle_acknowledge_strategy(self, elements: Dict[str, Any], acknowledgment: str) -> bool:
        """Execute acknowledgment strategy"""
        print(f"📝 Submitting acknowledgment: {acknowledgment}")
        return await self.ui.submit_placeholder_response(elements, acknowledgment)
    
    def _assess_complexity(self, question_text: str, topics: List[str]) -> str:
        """Assess the complexity of the research required"""
        # High complexity indicators
        high_complexity_keywords = [
            'comprehensive', 'detailed', 'in-depth', 'extensive',
            'analyze', 'compare', 'evaluate', 'assess'
        ]
        
        # Check for complexity indicators
        question_lower = question_text.lower()
        high_complexity_count = sum(1 for keyword in high_complexity_keywords 
                                  if keyword in question_lower)
        
        # Check number of topics
        if len(topics) > 5 or high_complexity_count >= 2:
            return 'high'
        elif len(topics) > 2 or high_complexity_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences for research handling"""
        try:
            # Get from knowledge base
            preferences = self.knowledge_base.get('user_preferences', {})
            
            research_prefs = {
                'auto_acknowledge_research': preferences.get('auto_acknowledge_research', False),
                'skip_when_possible': preferences.get('skip_research_when_possible', True),
                'placeholder_style': preferences.get('research_placeholder_style', 'detailed')
            }
            
            return research_prefs
            
        except Exception as e:
            print(f"⚠️ Error getting user preferences: {e}")
            return {}
    
    async def _store_automation_success(self, question_text: str, 
                                      strategy: str,
                                      research_type: str) -> None:
        """Store successful automation data for learning"""
        try:
            # Store in knowledge base
            if hasattr(self.knowledge_base, 'add_automated_response'):
                self.knowledge_base.add_automated_response(
                    question_type='research_required',
                    question_text=question_text,
                    response={
                        'strategy': strategy,
                        'research_type': research_type,
                        'success': True
                    },
                    confidence=0.85,
                    handler='research_required'
                )
            
            print("💾 Automation success data stored")
            
        except Exception as e:
            print(f"⚠️ Error storing automation data: {e}")
    
    async def learn_from_intervention(self, question_text: str, manual_response: Any) -> None:
        """Learn from manual intervention"""
        try:
            print("\n🧠 LEARNING FROM MANUAL INTERVENTION")
            
            # Analyze the manual response
            research_type = self.patterns.detect_research_type(question_text)
            
            # Determine what strategy the user used
            user_strategy = 'unknown'
            
            if isinstance(manual_response, str):
                response_lower = manual_response.lower()
                
                # Check if user skipped
                if not manual_response or len(manual_response) < 5:
                    user_strategy = 'skip'
                # Check if user provided placeholder
                elif any(word in response_lower for word in ['pending', 'to be researched', 'tbd']):
                    user_strategy = 'placeholder'
                # Check if user acknowledged
                elif any(word in response_lower for word in ['will research', 'understand', 'noted']):
                    user_strategy = 'acknowledge'
                else:
                    user_strategy = 'full_research'
            
            # Learn from the strategy
            self.brain.learn_from_research_handling(
                question_text,
                user_strategy,
                True,  # Assume manual intervention was successful
                research_type
            )
            
            print(f"✅ Learned from manual intervention: {user_strategy} strategy for {research_type} research")
            
        except Exception as e:
            print(f"❌ Error learning from intervention: {e}")