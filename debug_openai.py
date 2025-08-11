from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    client = OpenAI()
    
    # Simple text test first
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'Vision ready!'"}],
        max_tokens=10
    )
    
    print("✅ API Key works!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API Error: {e}")