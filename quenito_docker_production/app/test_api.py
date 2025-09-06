#!/usr/bin/env python3
"""
Simple API test to verify Anthropic connection and environment variables
"""

import os
import sys
import anthropic

def test_api_connection():
    print("\n" + "="*60)
    print("ANTHROPIC API CONNECTION TEST")
    print("="*60)
    
    # Check environment variable
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment!")
        print("\nEnvironment variables present:")
        for key in os.environ:
            if 'API' in key or 'KEY' in key:
                print(f"  - {key}: {os.environ[key][:10]}...")
        return False
    
    print(f"✅ API Key found: ...{api_key[-8:]}")
    print(f"   Full length: {len(api_key)} characters")
    
    # Test API connection
    print("\n📡 Testing API connection...")
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Make a simple test call
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'API connection successful!' and nothing else."}
            ]
        )
        
        print(f"✅ API Response: {response.content[0].text}")
        print("\n🎉 API CONNECTION TEST PASSED!")
        return True
        
    except anthropic.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Check that your API key is valid")
        return False
        
    except anthropic.APIError as e:
        print(f"❌ API Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    finally:
        print("="*60 + "\n")

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)