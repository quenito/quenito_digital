#!/usr/bin/env python3
"""
⏰ Recency Activities Handler - Main Orchestrator
Refactored to use modular architecture with centralized patterns
"""

from typing import Dict, List, Any, Optional, Tuple
import asyncio
from ..base_handler import BaseHandler
from .recency_activities_patterns import RecencyActivitiesPatterns
from .recency_activities_ui import RecencyActivitiesUI
from .recency_activities_brain import RecencyActivitiesBrain

class RecencyActivitiesHandler(BaseHandler):
    """
    Handles time-based activity questions using modular architecture
    Examples: "Which activities have you done in the last 12 months?"
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Get patterns from knowledge base
        question_patterns = knowledge_base.get("question_patterns", {})
        recency_patterns = question_patterns.get("recency_activities_questions", {})
        
        # Initialize modular components
        self.patterns = RecencyActivitiesPatterns(recency_patterns)
        self.ui = RecencyActivitiesUI(page)
        self.brain = RecencyActivitiesBrain(knowledge_base)
        
        # Get user profile
        self.user_profile = self._get_user_profile()
        
        print("⏰ Refactored Recency Activities Handler initialized!")
        print("🧠 Patterns loaded from centralized knowledge base")
    
    async def can_handle(self, question_text: str) -> Tuple[bool, float]:
        """
        Determine if this handler can handle the question
        Returns: (can_handle, confidence_score)
        """
        try:
            # Calculate confidence using patterns module
            confidence = self.patterns.calculate_confidence(question_text)
            
            # Log decision
            if confidence > 0.4:
                print(f"⏰ Recency Activities: CAN handle (confidence: {confidence:.2f})")
                print(f"📝 Question: {question_text[:100]}...")
                return True, confidence
            else:
                return False, confidence
                
        except Exception as e:
            print(f"❌ Error in can_handle: {e}")
            return False, 0.0
    
    async def handle(self, question_text: str) -> bool:
        """
        Handle the recency/activities question
        Returns: True if handled successfully, False otherwise
        """
        try:
            print("\n" + "="*50)
            print("⏰ HANDLING RECENCY ACTIVITIES QUESTION")
            print("="*50)
            
            # Detect time frame
            time_frame = self.patterns.detect_time_frame(question_text)
            print(f"⏱️ Time frame: {time_frame or 'last_year (default)'}")
            
            # Detect UI elements
            elements = await self.ui.detect_ui_elements()
            if not any(elements.values()):
                print("❌ No suitable UI elements found")
                return False
            
            # Get available activities
            available_activities = await self.ui.get_available_activities(elements)
            if not available_activities:
                print("❌ No activities found to select")
                return False
            
            # Extract just the text for processing
            activity_texts = [text for _, text in available_activities]
            print(f"📊 Found {len(activity_texts)} available activities")
            
            # Detect activity categories
            categories = self.patterns.detect_activity_categories(question_text, activity_texts)
            if categories:
                print(f"🎯 Detected categories: {', '.join(categories)}")
            
            # Get selection strategy
            strategy = self.patterns.get_selection_strategy(self.user_profile)
            print(f"📐 Using {strategy.get('description', 'moderate')} strategy")
            
            # Get intelligent activity selection
            selected_activities = self.brain.get_intelligent_activity_selection(
                activity_texts,
                time_frame or 'last_year',
                self.user_profile,
                strategy
            )
            
            # Validate combination
            if not self.patterns.validate_activity_combination(selected_activities):
                print("⚠️ Invalid activity combination detected, adjusting...")
                # Remove last activity and try again
                selected_activities = selected_activities[:-1]
            
            # Filter by demographics
            selected_activities = self.patterns.filter_activities_by_demographics(
                selected_activities,
                self.user_profile
            )
            
            print(f"\n🎯 Selected {len(selected_activities)} activities:")
            for i, activity in enumerate(selected_activities, 1):
                print(f"  {i}. {activity}")
            
            # Handle the selection
            if selected_activities:
                success = await self.ui.select_activities(
                    selected_activities,
                    available_activities,
                    elements
                )
                
                if success:
                    print("\n✅ Successfully automated recency activities question!")
                    
                    # Store successful automation data
                    await self._store_automation_success(
                        question_text,
                        selected_activities,
                        time_frame
                    )
                    
                    return True
                else:
                    print("❌ Failed to select activities in UI")
                    return False
            else:
                # No activities to select - try "None of the above"
                print("📭 No activities to select, trying 'None' option...")
                success = await self.ui.handle_none_option(available_activities, elements)
                return success
                
        except Exception as e:
            print(f"❌ Error handling recency activities: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _get_user_profile(self) -> Dict[str, Any]:
        """Get user profile from knowledge base"""
        try:
            # Get user responses
            user_responses = self.knowledge_base.get('user_responses', {})
            
            profile = {
                'age': self._extract_age(user_responses.get('age', '')),
                'gender': user_responses.get('gender', ''),
                'occupation': user_responses.get('occupation', ''),
                'income': user_responses.get('income', ''),
                'location': user_responses.get('location', '')
            }
            
            return profile
            
        except Exception as e:
            print(f"⚠️ Error getting user profile: {e}")
            return {}
    
    def _extract_age(self, age_response: str) -> int:
        """Extract numeric age from response"""
        try:
            # Handle range responses
            if '-' in age_response:
                # Take midpoint of range
                start, end = age_response.split('-')
                start = int(''.join(filter(str.isdigit, start)))
                end = int(''.join(filter(str.isdigit, end)))
                return (start + end) // 2
            else:
                # Extract first number
                import re
                numbers = re.findall(r'\d+', age_response)
                if numbers:
                    return int(numbers[0])
        except:
            pass
        
        return 35  # Default age
    
    async def _store_automation_success(self, question_text: str, 
                                      selected_activities: List[str],
                                      time_frame: Optional[str]) -> None:
        """Store successful automation data for learning"""
        try:
            # Store in knowledge base
            if hasattr(self.knowledge_base, 'add_automated_response'):
                self.knowledge_base.add_automated_response(
                    question_type='recency_activities',
                    question_text=question_text,
                    response={
                        'activities': selected_activities,
                        'time_frame': time_frame,
                        'count': len(selected_activities)
                    },
                    confidence=0.85,
                    handler='recency_activities'
                )
            
            print("💾 Automation success data stored")
            
        except Exception as e:
            print(f"⚠️ Error storing automation data: {e}")
    
    async def learn_from_intervention(self, question_text: str, manual_response: Any) -> None:
        """Learn from manual intervention"""
        try:
            print("\n🧠 LEARNING FROM MANUAL INTERVENTION")
            
            # Parse manual response
            selected_activities = []
            if isinstance(manual_response, list):
                selected_activities = manual_response
            elif isinstance(manual_response, str):
                # Split by common delimiters
                import re
                selected_activities = re.split(r'[,;]|\n', manual_response)
                selected_activities = [a.strip() for a in selected_activities if a.strip()]
            
            if selected_activities:
                # Detect time frame
                time_frame = self.patterns.detect_time_frame(question_text)
                
                # Learn from selection
                self.brain.learn_from_manual_selection(
                    question_text,
                    selected_activities,
                    time_frame or 'last_year',
                    self.user_profile
                )
                
                print(f"✅ Learned from {len(selected_activities)} manually selected activities")
            
        except Exception as e:
            print(f"❌ Error learning from intervention: {e}")