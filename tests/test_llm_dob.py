# test_llm_dob.py
import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv  # To load from .env file

class TestLLMAutomation:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment or .env file
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "your-api-key-here":
            print("⚠️ Please set your OpenAI API key!")
            print("Option 1: Add to .env file: OPENAI_API_KEY=sk-...")
            print("Option 2: Export in terminal: export OPENAI_API_KEY=sk-...")
            raise ValueError("OpenAI API key not configured")
            
        self.client = AsyncOpenAI(api_key=api_key)
        
        # ENHANCED PROMPT WITH CLEAR DOB INSTRUCTIONS
        self.system_prompt = """You are completing surveys as Matt, age 45, from Sydney.

YOUR PERSONAL DETAILS (Always use these - they are YOUR real details):
📅 Date of Birth: June 1980 (Month: June, Year: 1980)
🚹 Gender: Male
📍 Location: Postcode 2217, NSW, Sydney, Australia
💑 Marital Status: Married
👨‍👩‍👧‍👧 Children: Yes - 2 daughters (ages 3 and 6)
💼 Employment: Full-time
💰 Income: Personal $100-150k, Household $200-500k
🏥 Private Health: Yes - Medibank

CRITICAL RULES:
1. NEVER say "I prefer not to provide" - these ARE your details
2. For Date of Birth questions:
   - If asking for Month: Answer "June"
   - If asking for Year: Answer "1980"
   - If asking for full date: Answer "June 1980"
3. These are YOUR real details for YOUR survey rewards

When asked for date of birth in ANY format, provide June 1980."""

    async def get_response(self, question, options=None):
        """Get LLM response for a survey question"""
        
        user_message = f"Survey question: {question}"
        if options:
            user_message += f"\nOptions: {options}"
        user_message += "\n\nProvide a direct answer using my personal details. If it's a date of birth question, use June 1980."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for consistency
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

async def test_dob_handling():
    """Test Date of Birth handling specifically"""
    
    try:
        llm = TestLLMAutomation()
    except ValueError:
        return
    
    # Test various DOB question formats
    test_questions = [
        {
            "question": "What is your date of birth?",
            "expected": "June 1980"
        },
        {
            "question": "Please select your birth month and year",
            "expected": "Month: June, Year: 1980"
        },
        {
            "question": "Date of Birth (Month/Year)",
            "expected": "June/1980"
        },
        {
            "question": "When were you born?",
            "expected": "June 1980"
        },
        {
            "question": "What is your age?",
            "expected": "45"
        },
        {
            "question": "Are you...?",
            "options": ["Male", "Female"],
            "expected": "Male"
        },
        {
            "question": "Select your age group:",
            "options": ["18-24", "25-34", "35-44", "45-54", "55-64"],
            "expected": "45-54"
        },
        {
            "question": "Do you have private health insurance?",
            "options": ["Yes", "No"],
            "expected": "Yes"
        }
    ]
    
    print("=" * 60)
    print("🧪 TESTING LLM DATE OF BIRTH HANDLING")
    print("=" * 60)
    
    for test in test_questions:
        question = test["question"]
        options = test.get("options")
        expected = test["expected"]
        
        response = await llm.get_response(question, options)
        
        # Check if response matches expected
        success = expected.lower() in response.lower() or response.lower() in expected.lower()
        status = "✅" if success else "❌"
        
        print(f"\n{status} Question: {question}")
        if options:
            print(f"   Options: {options}")
        print(f"   Expected: {expected}")
        print(f"   LLM Response: {response}")
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("🎯 TEST COMPLETE")
    print("=" * 60)

# Run the test
if __name__ == "__main__":
    asyncio.run(test_dob_handling())