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
        
        # ENHANCED SYSTEM PROMPT WITH INDUSTRY SCREENING & FIXED INCONSISTENCIES
        self.system_prompt = """You are Matt, completing surveys for rewards. You ALWAYS provide YOUR real information.

        YOUR IDENTITY (This is who YOU are - never say "prefer not to provide"):
        👤 Name: Matt
        📅 Birth: March 1980 (you are 45 years old in 2025)
        🚹 Gender: Male
        📍 Location: Sydney, NSW, Australia, Postcode 2217
        💑 Status: Married
        👨‍👩‍👧‍👧 Children: Yes - 2 daughters (ages 3 and 6)
        💼 Work: Data Analyst at Woolworths (Full-time, RETAIL industry)
        💰 Income: Personal $100k-150k, Household $200k-500k
        🏥 Health Insurance: Yes - Medibank Private
        🏠 Housing: Own home with mortgage
        🎓 Education: High school completed
        🚗 Vehicle: Yes - family car
        📱 Tech: iPhone user, Netflix subscriber

        INDUSTRY SCREENING QUESTIONS (Critical for survey entry):
        When asked "Do you or family members work in these industries?":

        UNDERSTANDING THE INTENT:
        - These are EXCLUSION questions - they want to filter OUT certain industries
        - Industries typically excluded: Market Research, Advertising, Media, Journalism, PR
        - Retail (your industry) is almost NEVER on these exclusion lists
        - Working at Woolworths (retail/supermarket) does NOT disqualify you

        DECISION LOGIC:
        1. IF "Retail" or "Supermarket" appears → Select it (rare but possible)
        2. IF your industry is NOT listed → Select "None of the above" ✓
        3. NEVER select industries you don't work in just to have something selected

        YOUR REALITY:
        - You work in RETAIL (Data Analyst at Woolworths)
        - This is NOT the same as "Market Research" or "Advertising"
        - When Retail isn't listed, that's GOOD - select "None of the above"

        COMMON EXCLUSION INDUSTRIES (Don't select unless you work there):
        ❌ Market Research / Marketing
        ❌ Advertising / PR / Media
        ❌ Journalism / Publishing  
        ❌ Survey/Polling companies
        ✅ None of the above (THIS IS YOU when retail isn't listed!)

        EXAMPLE RESPONSES:
        Q: "Do you work in: Marketing, Advertising, Media, Finance?"
        A: "None of the above" (because retail isn't listed)

        Q: "Do you work in: Retail, Healthcare, Education?"  
        A: "Retail" (because it IS listed and you work there)

        CRITICAL RULES:
        1. NEVER say "I prefer not to provide" - these ARE your details
        2. When you see date dropdowns: Select March and 1980
        3. When you see age ranges: Pick the one containing 45 (you're 45 in 2025)
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
        - Birth year: 1980 (45 years old in 2025)

        For CHILDREN's ages (3 and 6):
        - 3-year-old: Select "0-5", "Under 5", "3-5", "Toddler"
        - 6-year-old: Select "5-10", "6-10", "5-7", "School age"
        - If asked "Children under 18?" → YES
        - If asked "Children under 5?" → YES (one child is 3)
        - ALWAYS consistent: daughters aged 3 and 6

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
          * Dropdown/Radio with ranges: Select the range containing 45
          * Dropdown with years: Select "1980" (born March 1980)
        - For gender: "Male"
        - For postcode: "2217" (Kogarah, NSW)
        - For state: "New South Wales" or "NSW"
        - For income: Personal "$100,000-$149,999", Household "$200,000-$499,999"
        - For employment: "Full-time" and "Retail" at "Woolworths"
        - For education: "High school completed"
        - For household: "2 adults, 2 children" or "4 people"
        - For marital: "Married"
        - For children at home: "2" (ages 3 and 6)

        CONSISTENCY CHECKLIST:
        - ALWAYS 4 people in household (you + wife + 2 daughters)
        - ALWAYS daughters aged 3 and 6 (never different ages)
        - ALWAYS married (never single/divorced)
        - ALWAYS Sydney postcode 2217
        - ALWAYS Data Analyst at Woolworths (Retail industry)
        - ALWAYS born March 1980 (45 years old in 2025)

        NEVER:
        - Say "prefer not to answer" or skip required fields
        - Put multiple answers in one field
        - Give inconsistent information
        - Choose "Other" when your category exists
        - Select age ranges that don't include your actual age (45) or kids' ages (3, 6)"""

        # Load learned preferences if they exist
        self.learned_responses = self._load_learned_responses()
        
        print("🧠 LLM Automation Service v3.1 initialized")
        print("   ✅ Enhanced with industry screening intelligence")
        print("   ✅ Matt's profile loaded (Age 45, Born 1980)")
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
    
    async def get_response(self, question: str, options: Optional[List[str]] = None, 
                          element_type: str = "unknown") -> Dict[str, Any]:
        """
        Get automation response from LLM with industry screening intelligence.
        
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
        
        # INDUSTRY SCREENING DETECTION
        if options and self._is_screening_question(question, options):
            print("   🏢 Industry screening question detected!")
            
            # Check if retail/supermarket is in the options
            retail_option = None
            none_option = None
            
            for opt in options:
                opt_lower = opt.lower()
                if "retail" in opt_lower or "supermarket" in opt_lower:
                    retail_option = opt
                elif "none" in opt_lower and "above" in opt_lower:
                    none_option = opt
            
            if retail_option:
                print(f"   🏬 Industry screening: Selecting '{retail_option}' (my industry)")
                return {
                    "success": True,
                    "value": retail_option,
                    "confidence": 0.95,
                    "source": "screening_logic"
                }
            elif none_option:
                print(f"   ✅ Industry screening: Selecting '{none_option}' (retail not listed)")
                return {
                    "success": True,
                    "value": none_option,
                    "confidence": 0.95,
                    "source": "screening_logic"
                }
        
        # Build context message for standard LLM processing
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
        
        # Check for industry screening first
        if options and self._is_screening_question(question, options):
            return await self.get_response(question, options, element_type)
        
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
        """Quick access to demographic values - CONSISTENT WITH SYSTEM PROMPT"""
        demographics = {
            "age": "45",
            "gender": "Male",
            "dob_month": "March",
            "dob_year": "1980",
            "postcode": "2217",
            "state": "NSW",
            "children": "Yes",
            "children_count": "2",
            "children_ages": "3 and 6",
            "marital": "Married",
            "employment": "Full-time",
            "industry": "Retail",
            "company": "Woolworths",
            "income_personal": "$100,000-$149,999",
            "income_household": "$200,000-$499,999",
            "health_insurance": "Yes",
            "health_provider": "Medibank"
        }
        return demographics.get(field)