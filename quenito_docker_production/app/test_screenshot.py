#!/usr/bin/env python3
"""
Test with correct model for computer use
"""

import anthropic
import asyncio
import os

async def test_screenshot():
    print("\n" + "="*60)
    print("SCREENSHOT TOOL TEST - FIXED")
    print("="*60)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    print(f"✅ API Key: ...{api_key[-8:]}")
    
    client = anthropic.AsyncAnthropic(api_key=api_key)
    
    # Use the model that supports computer use
    MODEL = "claude-3-5-sonnet-20241022"  # This model supports computer tools
    
    print(f"\nTest Configuration:")
    print(f"  Model: {MODEL}")
    print(f"  Tool: computer_20241022")
    
    try:
        print("\n📸 Requesting screenshot...")
        
        response = await client.beta.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=[{
                "type": "computer_20241022",
                "name": "computer",
                "display_width_px": 1280,
                "display_height_px": 800
            }],
            messages=[{
                "role": "user",
                "content": "Take a screenshot and describe what you see."
            }]
        )
        
        print(f"\n✅ API call successful!")
        print(f"Stop reason: {response.stop_reason}")
        
        for block in response.content:
            if hasattr(block, "type"):
                if block.type == "tool_use":
                    print(f"✅ Tool requested: {block.name}")
                    print(f"Tool input: {block.input}")
                    return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_screenshot())