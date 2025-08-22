#!/usr/bin/env python3
"""
🧪 TEST LEARNING SYSTEM INTEGRATION
"""
import asyncio
import os
from services.intelligent_learning_system import IntelligentLearningSystem
from services.llm_automation_service import LLMAutomationService
from openai import AsyncOpenAI
from dotenv import load_dotenv

def __init__(self):
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    self.client = AsyncOpenAI(api_key=api_key)

async def test_learning_system():
    """Test the integrated learning system"""
    
    print("🧪 Testing Intelligent Learning System Integration\n")
    print("=" * 60)
    
    # Initialize the service
    llm_service = LLMAutomationService()
    
    # Show initial stats
    stats = llm_service.get_learning_stats()
    print("\n📊 Initial Stats:")
    print(f"   Learned Q&As: {stats['learned_responses']['total']}")
    print(f"   Patterns: {stats['patterns']['total']}")
    print(f"   Categories: {stats['patterns']['categories']}")
    
    # Test 1: Pattern matching (gender)
    print("\n🧪 Test 1: Pattern Matching")
    response = await llm_service.get_response(
        "What is your gender?",
        ["Male", "Female", "Other"],
        "radio"
    )
    print(f"   Question: What is your gender?")
    print(f"   Response: {response['value']}")
    print(f"   Source: {response.get('source', 'unknown')}")
    print(f"   Confidence: {response.get('confidence', 0)}")
    
    # Test 2: Industry screening
    print("\n🧪 Test 2: Industry Screening")
    response = await llm_service.get_response(
        "Do you or anyone in your household work in any of the following industries?",
        ["Marketing", "Advertising", "Retail", "None of the above"],
        "radio"
    )
    print(f"   Response: {response['value']}")
    print(f"   Source: {response.get('source', 'unknown')}")
    
    # Test 3: New question (will use LLM)
    print("\n🧪 Test 3: New Question (LLM)")
    response = await llm_service.get_response(
        "How often do you shop for groceries?",
        ["Daily", "Weekly", "Fortnightly", "Monthly"],
        "radio"
    )
    print(f"   Response: {response['value']}")
    print(f"   Source: {response.get('source', 'unknown')}")
    
    # Test 4: Check if it learned from Test 3
    print("\n🧪 Test 4: Same Question Again (Should be learned)")
    response = await llm_service.get_response(
        "How often do you shop for groceries?",
        ["Daily", "Weekly", "Fortnightly", "Monthly"],
        "radio"
    )
    print(f"   Response: {response['value']}")
    print(f"   Source: {response.get('source', 'unknown')}")
    
    # Test 5: Manual intervention simulation
    print("\n🧪 Test 5: Recording Manual Intervention")
    llm_service.record_manual_intervention(
        "What is your favorite color?",
        "Blue",
        "text"
    )
    print("   Manual answer recorded: Blue")
    
    # Save session
    print("\n💾 Saving Session...")
    llm_service.save_session()
    
    # Final stats
    final_stats = llm_service.get_learning_stats()
    print("\n📊 Final Stats:")
    print(f"   Learned Q&As: {final_stats['learned_responses']['total']}")
    print(f"   Session automated: {final_stats['current_session']['automated']}")
    print(f"   Session manual: {final_stats['current_session']['manual']}")
    
    print("\n✅ Testing Complete!")


if __name__ == "__main__":
    asyncio.run(test_learning_system())