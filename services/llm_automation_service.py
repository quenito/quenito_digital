#!/usr/bin/env python3
"""
🧠 LLM AUTOMATION SERVICE v4.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enhanced with Intelligent Learning System Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import os
import asyncio
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
from services.intelligent_learning_system import IntelligentLearningSystem

# Load environment variables
load_dotenv()


class LLMAutomationService:
    """Enhanced LLM service with intelligent learning"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client with error handling
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = AsyncOpenAI(api_key=api_key)
        
        # Initialize Intelligent Learning System
        self.learning = IntelligentLearningSystem()
        
        # Load core knowledge for context
        self.knowledge_base = self.learning.knowledge_base
        
        print("🧠 LLM Automation Service v4.0 initialized")
        print("   ✅ Intelligent Learning System integrated")
        print(f"   📚 {len(self.learning.learned_responses)} exact Q&As loaded")
        print(f"   🎯 {len(self.learning.learned_patterns)} patterns loaded")
        print("   ✅ Matt's profile loaded (Age 45, Born 1980)")
    
    async def get_response(self, question: str, options: Optional[List[str]] = None, 
                          element_type: str = "unknown") -> Dict[str, Any]:
        """
        Get automation response with intelligent learning.
        Priority: Exact match → Pattern match → LLM → Manual
        """
        
        # Log the question
        print(f"\n   🤔 Processing: {question[:100]}...")
        
        # Step 1: Check learning system first (exact matches and patterns)
        learned_response = await self.learning.get_response_for_question(
            question, element_type, options
        )
        
        if learned_response:
            print(f"   ✅ Using learned response: {learned_response['value']}")
            return learned_response
        
        # Step 2: Check if it's an industry screening question
        if self._is_screening_question(question, options):
            print("   🏢 Industry screening detected - selecting safe option")
            
            # Find "Retail" or "None of the above"
            if options:
                for opt in options:
                    if "retail" in opt.lower():
                        response = {
                            "success": True,
                            "value": opt,
                            "confidence": 0.95,
                            "source": "screening_logic"
                        }
                        # Record this for learning
                        self.learning.record_successful_automation(
                            question, opt, element_type, 0.95
                        )
                        return response
                    elif "none" in opt.lower():
                        response = {
                            "success": True,
                            "value": opt,
                            "confidence": 0.95,
                            "source": "screening_logic"
                        }
                        self.learning.record_successful_automation(
                            question, opt, element_type, 0.95
                        )
                        return response
        
        # Step 3: Use LLM with knowledge base context
        llm_response = await self._call_llm(question, options, element_type)
        
        # Step 4: If successful, record for learning
        if llm_response.get("success"):
            self.learning.record_successful_automation(
                question,
                llm_response["value"],
                element_type,
                llm_response.get("confidence", 0.85)
            )
        
        return llm_response
    
    async def _call_llm(self, question: str, options: Optional[List[str]], 
                       element_type: str) -> Dict[str, Any]:
        """Call LLM with Matt's profile context"""
        
        try:
            # Build context with knowledge base
            context = f"""You are answering as Matt, whose profile is:
{json.dumps(self.knowledge_base, indent=2)}

Question: {question}
Element Type: {element_type}
"""
            
            if options:
                context += f"\nOptions available: {', '.join(options[:10])}"
                if len(options) > 10:
                    context += f" (and {len(options) - 10} more)"
            
            # Add specific instructions based on element type
            if element_type == "radio":
                context += "\n\nSelect ONE option from the list. Return ONLY the exact text of your choice."
            elif element_type == "checkbox":
                context += "\n\nSelect ALL that apply. Return options separated by semicolons (;)."
            elif element_type == "select":
                context += "\n\nChoose from the dropdown. Return ONLY the exact text of your choice."
            elif element_type == "text":
                context += "\n\nProvide a text response that fits Matt's profile."
            
            # Make the API call
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Matt, a 45-year-old data analyst from Sydney. Answer based on your profile."},
                    {"role": "user", "content": context}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "value": answer,
                "confidence": 0.85,
                "source": "llm"
            }
            
        except Exception as e:
            print(f"   ⚠️ LLM call failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "source": "llm"
            }
    
    def _is_screening_question(self, question: str, options: List[str]) -> bool:
        """Detect if this is an industry screening question"""
        screening_keywords = [
            "work in any of these",
            "employed in any of",
            "work for any of the following",
            "family members work",
            "any of your immediate family",
            "household members work"
        ]
        
        exclusion_industries = [
            "market research", "advertising", "media", 
            "journalism", "public relations", "pr",
            "marketing", "survey", "polling"
        ]
        
        # Check if question matches screening pattern
        question_lower = question.lower()
        is_screening = any(keyword in question_lower for keyword in screening_keywords)
        
        # Check if options contain typical exclusion industries
        if is_screening and options:
            options_text = " ".join(options).lower()
            has_exclusions = any(industry in options_text for industry in exclusion_industries)
            has_none_option = any("none" in opt.lower() for opt in options)
            
            return has_exclusions and has_none_option
        
        return False
    
    def record_manual_intervention(self, question: str, answer: Any, element_type: str):
        """Record when user manually answers - for learning analysis"""
        self.learning.record_manual_intervention(question, answer, element_type)
        print(f"   📝 Manual intervention recorded for review")
    
    def save_session(self):
        """Save the learning session for analysis"""
        self.learning.save_session()
        stats = self.learning.get_learning_stats()
        print(f"\n📊 Session Summary:")
        print(f"   Automated: {stats['current_session']['automated']}")
        print(f"   Manual: {stats['current_session']['manual']}")
        print(f"   Total learned Q&As: {stats['learned_responses']['total']}")
        print(f"   High confidence: {stats['learned_responses']['high_confidence']}")
    
    def get_learning_stats(self) -> Dict:
        """Get current learning statistics"""
        return self.learning.get_learning_stats()


# For backward compatibility
def save_learned_preference(self, question: str, answer: str, element_type: str):
    """Legacy method - redirects to new learning system"""
    self.learning.record_successful_automation(question, answer, element_type, 0.85)