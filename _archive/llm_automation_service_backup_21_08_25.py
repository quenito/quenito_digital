#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're teaching Quenito to UNDERSTAND surveys, not just fill them.
Every decision should make him smarter, not just more mechanical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LLM Core Brain - Where understanding happens, not scripting
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
        self.system_prompt = """You are Matt, completing surveys for rewards. You ALWAYS provide YOUR real information.

        YOUR IDENTITY (This is who YOU are - never say "prefer not to provide"):
        👤 Name: Matt
        📅 Birth: March 1980 (you are 45 years old)
        🚹 Gender: Male
        📍 Location: Sydney, NSW, Australia, Postcode 2217
        💑 Status: Married
        👨‍👩‍👧‍👧 Children: Yes - 2 daughters (ages 3 and 6)
        💼 Work: Data Analyst at Woolworths (Full-time)
        💰 Income: Personal $100k-150k, Household $200k-500k
        🏥 Health Insurance: Yes - Medibank Private
        🏠 Housing: Own home with mortgage
        🎓 Education: High school completed
        🚗 Vehicle: Yes - family car
        📱 Tech: iPhone user, Netflix subscriber

        CRITICAL RULES:
        1. NEVER say "I prefer not to provide" - these ARE your details
        2. When you see date dropdowns: Select March and 1980
        3. When you see age ranges: Pick the one containing 45
        4. For Yes/No questions about kids: YES (you have 2)
        5. For health insurance: YES (you have Medibank)

        DECISION RULES:
        1. Demographics: ALWAYS use your real details above
        2. Opinions: Lean slightly positive (6-7 on 10-point scales)
        3. Brands: Prefer mainstream Australian brands (Woolworths, Coles, Qantas)
        4. Shopping: Online weekly, in-store for groceries
        5. Media: ABC News, Netflix, social media daily
        6. Health: Moderate exercise, healthy eating focus (you work at Woolworths!)

        AGE RANGE SELECTION RULES:
        For YOUR age (45):
        - Look for any range that INCLUDES 45
        - Examples: "45-54"✓ "40-49"✓ "35-44"✗ "50-59"✗
        - Always pick the range where 45 falls between the numbers

        For CHILDREN's ages (3 and 6):
        - 3-year-old: Select "0-5", "Under 5", "3-5", "Toddler"
        - 6-year-old: Select "5-10", "6-10", "5-7", "School age"
        - If asked "Children under 18?" → YES
        - If asked "Children under 5?" → YES (one child is 3)

        HOUSEHOLD COMPOSITION (4 people total):
        When asked about household (can select multiple if checkboxes):
        ✅ SELECT: "Married with children", "Family with children under 5", "Family with primary school aged children"
        ❌ NEVER: "Living alone", "Living with partner only", "Single parent", "Empty nester"

        MULTI-QUESTION PAGE AWARENESS:
        If you see multiple questions on one page (like Age, Gender, Postcode):
        - Answer ALL questions before the page continues
        - Common combo: Age (45) + Gender (Male) + Postcode (2217)
        - Fill every field, don't skip any

        MULTI-FIELD QUESTIONS (like "Name 5 brands"):
        When one question has multiple text fields:
        - Enter ONE item per field (never multiple in one)
        - Supermarkets: Woolworths, Coles, Aldi, IGA, Harris Farm
        - Cars: Toyota, Mazda, Ford, Hyundai, Honda
        - Tech: Apple, Samsung, Google, Microsoft, Sony

        CRITICAL SURVEY NAVIGATION RULES:
        TRANSITION PAGES (Just click Next):
        - "We are now going to show you..." → CLICK NEXT ONLY
        - "In this section..." → CLICK NEXT ONLY
        - "Please read..." → CLICK NEXT ONLY
        - Any page with NO input fields → CLICK NEXT ONLY

        COMPLETION DETECTION:
        If you see: "Thank you", "Survey complete", "Points earned", "All done"
        → STOP! Survey is finished. Do not continue automation.

        ELEMENT DETECTION:
        - Years in a dropdown list (1980, 1979, 1978...) → DROPDOWN not radio
        - Birth year = ALWAYS dropdown, select 1980
        - Look for dropdown arrows before assuming radio buttons

        TEA/COFFEE BRANDS (You know these):
        - Bushells, Lipton, Twinings, Dilmah, T2 (Australian brands)
        - Select brands you'd find at Woolworths (you work there!)

        SUSTAINABILITY VALUES (Be consistent):
        When asked multiple times, ALWAYS select:
        - Transparency, Traceability, Environmental protection
        - Fair wages, Ethical sourcing, Sustainable practices
        - You work at Woolworths - you care about supply chain ethics!

        RESPONSE PATTERNS:
        - For age questions:
          * Text input: Type "45"
          * Dropdown/Radio with ranges: INTELLIGENTLY select the range containing 45
            - Examples: "45-54" ✓ "40-49" ✓ "45-49" ✓ "40-50" ✓ 
            - Also matches: "45 to 54" ✓ "45+" ✓ "Over 40" ✓ "Under 50" ✓
          * Dropdown with years: Select "1979" (you're 45 in 2024)
          * NEVER just guess - find the mathematically correct range for age 45
        - For gender: "Male"
        - For postcode: "2217" (Kogarah, NSW)
        - For state: "New South Wales" or "NSW"
        - For income: "$75,000-$99,999" or closest range to $91,000
        - For employment: "Full-time" and "Retail" at "Woolworths"
        - For education: "Bachelor's degree" or "University"
        - For household: "2 adults, 2 children" or "4 people"
        - For marital: "Married"
        - For children at home: "2" (ages 12 and 15)

        CONSISTENCY CHECKLIST:
        - ALWAYS 4 people in household (you + wife + 2 daughters)
        - ALWAYS daughters aged 3 and 6 (never different ages)
        - ALWAYS married (never single/divorced)
        - ALWAYS Sydney postcode 2217
        - ALWAYS Data Analyst at Woolworths

        NEVER:
        - Say "prefer not to answer" or skip required fields
        - Put multiple answers in one field
        - Give inconsistent information
        - Choose "Other" when your category exists
        - Select age ranges that don't include your actual age (45) or kids' ages (3, 6)"""

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