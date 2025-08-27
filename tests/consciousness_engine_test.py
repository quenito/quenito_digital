# consciousness_engine_test.py
import json
import asyncio
from datetime import datetime

class ConsciousnessEngine:
    def __init__(self):
        self.consciousness = self.load_matt_consciousness()
        
    def load_matt_consciousness(self):
        """Load Matt's complete consciousness structure"""
        return {
            "identity": {
                "name": "Matt",
                "age": 45,
                "birth_month": "March",
                "birth_year": 1980,
                "occupation": "Data Analyst",
                "employer": "Woolworths",
                "location": "Kogarah, Sydney NSW 2217",
                "family": {
                    "marital_status": "Married",
                    "children": [{"age": 6}, {"age": 3}]
                }
            },
            "values": {
                "core_hierarchy": ["family_security", "financial_stability", "fairness", "practical_efficiency"],
                "money": "Tool for security, hate debt",
                "community": "Look after mates, help disadvantaged kids"
            },
            "reasoning_style": {
                "decision_framework": "practical_family_optimizer",
                "satisfaction_baseline": 7,
                "concern_levels": {
                    "default": "moderate",
                    "family_impact": "heightened"
                }
            },
            "lifestyle": {
                "fast_food": "McDonald's is go-to",
                "shopping": "Weekly Woolies run, hate it",
                "sports_passion": ["NRL", "Formula 1", "Cricket"],
                "outdoor": ["Beach", "Camping", "Hiking"]
            },
            "brand_awareness": self.get_brand_awareness()
        }
    
    def get_brand_awareness(self):
        """Brand awareness compiled from Matt's data"""
        return {
            "supermarkets": {
                "know_well": ["Woolworths", "Coles", "ALDI"],
                "know_somewhat": ["IGA", "Harris Farm"],
                "work_for": "Woolworths"
            },
            "banks": {
                "know_well": ["Commonwealth Bank", "ING"],
                "know_somewhat": ["ANZ", "NAB", "Westpac"],
                "customer_of": ["Commonwealth Bank", "ING"]
            },
            "insurance": {
                "know_well": ["NRMA", "AAMI", "Medibank"],
                "know_somewhat": ["Allianz", "Budget Direct", "Bupa"],
                "customer_of": {"car": "NRMA", "home": "AAMI", "health": "Medibank"}
            },
            "airlines": {
                "know_well": ["Qantas", "Jetstar"],
                "know_somewhat": ["Virgin", "Rex"],
                "prefer": "Qantas"
            },
            "beer": {
                "know_well": ["Balter XPA", "Carlton", "VB", "Tooheys"],
                "prefer": "Balter XPA"
            },
            "fast_food": {
                "know_well": ["McDonald's", "KFC", "Hungry Jack's", "Subway"],
                "know_somewhat": ["Red Rooster", "Domino's", "Pizza Hut"],
                "prefer": "McDonald's"
            },
            "retail": {
                "know_well": ["Kmart", "Target", "Big W", "Bunnings", "Officeworks"],
                "know_somewhat": ["Myer", "David Jones"],
                "shop_at": ["Kmart", "Target", "Bunnings", "Officeworks"]
            },
            "streaming": {
                "know_well": ["Netflix", "Amazon Prime", "Disney+", "Kayo", "Stan"],
                "subscriber": ["Netflix", "Amazon Prime", "Disney+", "Kayo"]
            },
            "automotive": {
                "know_well": ["Nissan", "Toyota", "Mazda", "Holden"],
                "own": "Nissan X-Trail 2013"
            },
            "sports": {
                "know_well": ["NRL teams", "F1 teams", "Cricket Australia"],
                "passionate": ["South Sydney Rabbitohs", "Red Bull Racing"]
            }
        }
    
    def reason_through_question(self, question, options=None, question_type=None):
        """
        Main reasoning engine - simulating LLM reasoning locally for testing
        """
        
        # FACTUAL QUESTIONS
        if "born" in question.lower() and "month" in question.lower():
            return {
                "answer": {"month": "March", "year": "1980"},
                "confidence": 1.0,
                "reasoning": "Factual data from identity"
            }
        
        # VALUES QUESTION
        if "values are important" in question.lower():
            reasoning = """
            My core values: family first, security, mateship.
            Family is everything. Financial security matters for them.
            Community/mateship is Australian core value I hold.
            Money is tool not value. Innovation only if practical.
            """
            selected = ["Family", "Security", "Community"]
            return {
                "answer": selected,
                "confidence": 0.95,
                "reasoning": reasoning
            }
        
        # FRIEND DESCRIPTION
        if "friend describe you" in question.lower():
            reasoning = """
            4am riser pushing side projects = Ambitious
            Always there for family and mates = Reliable, Caring  
            Data analyst, efficiency focused = Practical
            Not the loud party type, more reserved = not Fun-loving
            """
            return {
                "answer": ["Reliable", "Practical", "Ambitious", "Caring"],
                "confidence": 0.9,
                "reasoning": reasoning
            }
        
        # BRAND RECENCY
        if "mcdonald" in question.lower():
            reasoning = """
            McDonald's is my go-to fast food. With 6 & 3 year old kids,
            probably hit Maccas every 2-3 weeks. Sometimes weekly if busy.
            """
            return {
                "answer": "Past month",
                "confidence": 0.85,
                "reasoning": reasoning
            }
        
        # SATISFACTION RATING
        if "satisfied" in question.lower() and "mortgage" in question.lower():
            reasoning = """
            CBA customer. No major issues but concerned about rates.
            Baseline satisfaction is 7. Slight concern drops it to 6.
            Practical nature means I don't switch without clear benefit.
            """
            return {
                "answer": 6,
                "confidence": 0.85,
                "reasoning": reasoning
            }
        
        # DEFAULT
        return {
            "answer": "Need LLM integration for this question type",
            "confidence": 0.0,
            "reasoning": "Question type not in test scenarios"
        }

# TEST RUNNER
def run_tests():
    engine = ConsciousnessEngine()
    
    test_questions = [
        {
            "question": "When were you born? Month and Year",
            "type": "factual_split"
        },
        {
            "question": "Which of these values are important to you?",
            "options": ["Family", "Money", "Success", "Adventure", "Security", "Innovation", "Community", "Freedom"],
            "type": "multi_select"
        },
        {
            "question": "How would a friend describe you?",
            "options": ["Ambitious", "Reliable", "Fun-loving", "Serious", "Creative", "Practical", "Adventurous", "Caring"],
            "type": "multi_select"
        },
        {
            "question": "When did you last purchase from McDonald's?",
            "options": ["Past week", "Past month", "Past 3 months", "Past 6 months", "Past year", "Over a year ago"],
            "type": "single_select"
        },
        {
            "question": "How satisfied are you with your current mortgage provider?",
            "scale": "0-10",
            "type": "scale_rating"
        }
    ]
    
    print("🧪 CONSCIOUSNESS ENGINE TEST RESULTS\n")
    print("=" * 60)
    
    for test in test_questions:
        result = engine.reason_through_question(
            test["question"],
            test.get("options"),
            test.get("type")
        )
        
        print(f"\n📋 QUESTION: {test['question']}")
        if test.get("options"):
            print(f"   OPTIONS: {test['options']}")
        print(f"\n🧠 REASONING: {result['reasoning'].strip()}")
        print(f"\n✅ ANSWER: {result['answer']}")
        print(f"📊 CONFIDENCE: {result['confidence']:.0%}")
        print("-" * 60)

if __name__ == "__main__":
    run_tests()