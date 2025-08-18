#!/usr/bin/env python3
"""
🧠 LLM Automation Service v3.0 - SIMPLIFIED & ENHANCED
Direct LLM-based automation with proven prompts from testing.
Priority: LLM FIRST, handlers only for complex cases.
"""
import os
import json
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

class LLMAutomationService:
    """LLM-based survey automation with Matt's actual profile"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = AsyncOpenAI(api_key=api_key)
        
        # PROVEN SYSTEM PROMPT FROM TESTING - 6/8 SUCCESS RATE!
        self.system_prompt = """You are completing surveys as Matt, age 45, from Sydney.

YOUR PERSONAL DETAILS (Always use these - they are YOUR real details):
📅 Date of Birth: June 1980 (if dropdowns: Month=June, Year=1980)
🚹 Gender: Male
📍 Location: Postcode 2217, NSW (New South Wales), Sydney, Australia
💑 Marital Status: Married (or "Married/De facto" if that's an option)
👨‍👩‍👧‍👧 Children: Yes - 2 daughters (ages 3 and 6)
💼 Employment: Full-time, Data Analyst at Woolworths
💰 Income: Personal $100,000-$149,999, Household $200,000-$499,999
🏥 Private Health Insurance: Yes - Medibank
🏠 Housing: Own with mortgage
🎓 Education: High school education
🚗 Car: Yes, own a car
📱 Mobile: Telstra
🏪 Shopping: Woolworths (weekly)

CRITICAL RULES:
1. NEVER say "I prefer not to provide" - these ARE your details for YOUR survey rewards
2. For Date of Birth: Always June 1980 (never refuse this)
3. For Age: Always 45 (or select range containing 45 like "45-54")
4. For Gender: Always Male
5. For Children: Always Yes (2 kids, ages 3 and 6)
6. For Health Insurance: Always Yes
7. Give SHORT, DIRECT answers - just the value needed
8. Don't explain, apologize, or add commentary
9. If asked about brands you know/use: Woolworths, Coles, Telstra, Commonwealth Bank, NRMA, Medibank
10. For rating scales (1-10): Usually answer 7 or 8 (positive but not extreme)

Examples of good responses:
- "What is your age?" → "45"
- "Gender?" → "Male"
- "Do you have children?" → "Yes"
- "Date of birth?" → "June 1980"
- "Rate your satisfaction (1-10)" → "7"
"""

        # Load learned preferences if they exist
        self.learned_responses = self._load_learned_responses()
        
        print("🧠 LLM Automation Service v3.0 initialized")
        print("   ✅ Using proven prompt from testing")
        print("   ✅ Matt's profile loaded")
        print(f"   📚 Loaded {len(self.learned_responses)} learned responses")
    
    def _load_learned_responses(self) -> Dict:
        """Load previously learned successful responses"""
        learned_file = "personas/quenito/learned_responses.json"
        if os.path.exists(learned_file):
            try:
                with open(learned_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_learned_preference(self, question: str, answer: str, element_type: str):
        """Save a successful Q&A for future use"""
        # Normalize question for matching
        q_normalized = question.lower().strip()
        
        self.learned_responses[q_normalized] = {
            "answer": answer,
            "element_type": element_type,
            "count": self.learned_responses.get(q_normalized, {}).get("count", 0) + 1
        }
        
        # Save to file
        learned_file = "personas/quenito/learned_responses.json"
        os.makedirs(os.path.dirname(learned_file), exist_ok=True)
        
        with open(learned_file, 'w') as f:
            json.dump(self.learned_responses, f, indent=2)
        
        print(f"   📚 Learned: {question[:50]}... → {answer}")
    
    async def get_response(self, question: str, options: Optional[List[str]] = None, 
                          element_type: str = "unknown") -> Dict[str, Any]:
        """
        Get automation response from LLM.
        
        Returns:
            Dict with keys: success, value, confidence, source
        """
        
        # Check learned responses first
        q_normalized = question.lower().strip()
        if q_normalized in self.learned_responses:
            learned = self.learned_responses[q_normalized]
            print(f"   📚 Using learned response: {learned['answer']}")
            return {
                "success": True,
                "value": learned["answer"],
                "confidence": 0.95,
                "source": "learned"
            }
        
        # Build context message
        context_message = f"Survey question: {question}"
        
        if options:
            context_message += f"\n\nAvailable options: {', '.join(options)}"
            context_message += "\n\nSelect the most appropriate option from the list."
        
        if element_type == "text":
            context_message += "\n\nProvide a short text answer."
        elif element_type == "radio":
            context_message += "\n\nSelect one option."
        elif element_type == "checkbox":
            context_message += "\n\nSelect all that apply (can be multiple)."
        elif element_type == "dropdown":
            context_message += "\n\nSelect from dropdown."
        
        context_message += "\n\nRespond with ONLY the answer value(s), nothing else."
        
        try:
            # Call GPT-4o-mini with enhanced prompt
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context_message}
                ],
                temperature=0.3,  # Low temperature for consistency
                max_tokens=150
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Clean up the answer
            answer = self._clean_answer(answer, element_type)
            
            # Check for refusal phrases (should not happen with new prompt)
            refusal_phrases = ["prefer not to", "cannot provide", "don't have", "privacy"]
            if any(phrase in answer.lower() for phrase in refusal_phrases):
                print(f"   ⚠️ LLM refused: {answer}")
                return {
                    "success": False,
                    "value": answer,
                    "confidence": 0.0,
                    "source": "llm"
                }
            
            print(f"   🤖 LLM response: {answer}")
            
            return {
                "success": True,
                "value": answer,
                "confidence": 0.85,
                "source": "llm"
            }
            
        except Exception as e:
            print(f"   ❌ LLM error: {str(e)}")
            return {
                "success": False,
                "value": None,
                "confidence": 0.0,
                "source": "error",
                "error": str(e)
            }
    
    def _clean_answer(self, answer: str, element_type: str) -> str:
        """Clean and format the LLM answer"""
        
        # Remove common prefixes
        prefixes_to_remove = [
            "I am ", "I'm ", "My answer is ", "The answer is ",
            "I would select ", "I select ", "My response is ",
            "I have ", "Yes, I have ", "No, I don't have ",
            "I was born in ", "My date of birth is "
        ]
        
        for prefix in prefixes_to_remove:
            if answer.startswith(prefix):
                answer = answer[len(prefix):]
        
        # Remove quotes
        answer = answer.strip('"\'')
        
        # For age, extract just the number
        if "age" in answer.lower() and element_type == "text":
            import re
            age_match = re.search(r'\b(\d+)\b', answer)
            if age_match:
                answer = age_match.group(1)
        
        # For yes/no questions, simplify
        if element_type == "radio":
            if answer.lower().startswith("yes"):
                answer = "Yes"
            elif answer.lower().startswith("no"):
                answer = "No"
            elif "male" in answer.lower() and "female" not in answer.lower():
                answer = "Male"
            elif "female" in answer.lower():
                answer = "Female"
        
        # Remove trailing periods
        answer = answer.rstrip('.')
        
        return answer
    
    async def get_response_with_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced method that accepts vision context and other info.
        
        Args:
            context: Dict containing question, vision_analysis, element_type, etc.
        """
        
        question = context.get("question", "")
        vision = context.get("vision_analysis", {})
        element_type = context.get("element_type", "unknown")
        options = context.get("options", [])
        
        # Add vision insights to the prompt if available
        enhanced_message = f"Survey question: {question}"
        
        if vision and vision.get("confidence_rating", 0) > 70:
            q_type = vision.get("question_type", "")
            if q_type:
                enhanced_message += f"\n\nContext: This appears to be a {q_type} question."
        
        if options:
            enhanced_message += f"\n\nOptions available: {', '.join(options)}"
        
        enhanced_message += f"\n\nElement type: {element_type}"
        enhanced_message += "\n\nProvide ONLY the answer value, nothing else."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": enhanced_message}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            answer = response.choices[0].message.content.strip()
            answer = self._clean_answer(answer, element_type)
            
            # Higher confidence when vision agrees
            confidence = 0.90 if vision.get("confidence_rating", 0) > 80 else 0.85
            
            return {
                "success": True,
                "value": answer,
                "confidence": confidence,
                "source": "llm_with_vision"
            }
            
        except Exception as e:
            print(f"   ❌ LLM error: {str(e)}")
            return {
                "success": False,
                "value": None,
                "confidence": 0.0,
                "source": "error",
                "error": str(e)
            }
    
    def get_demographic_value(self, field: str) -> Optional[str]:
        """Quick access to demographic values"""
        demographics = {
            "age": "45",
            "gender": "Male",
            "dob_month": "June",
            "dob_year": "1980",
            "postcode": "2217",
            "state": "NSW",
            "children": "Yes",
            "children_count": "2",
            "marital": "Married",
            "employment": "Full-time",
            "income_personal": "$100,000-$149,999",
            "income_household": "$200,000-$499,999",
            "health_insurance": "Yes",
            "health_provider": "Medibank"
        }
        return demographics.get(field)