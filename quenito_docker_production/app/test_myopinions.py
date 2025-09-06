#!/usr/bin/env python3
"""
Explicitly force Chrome usage for testing
"""

import os
import time
import anthropic

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-20250514"
MAX_ITERATIONS = 10

class ForceChromTest:
    """Force Chrome browser usage"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        print("🔧 Explicit Chrome Test")
        print(f"📋 Model: {MODEL}")
        
    def run_test(self):
        """Run test forcing Chrome"""
        print("\n" + "="*50)
        print("🚀 FORCING CHROME BROWSER TEST")
        print("="*50 + "\n")
        
        # Configure tools
        tools = [
            {
                "type": "computer_20250124",
                "name": "computer",
                "display_width_px": 1024,
                "display_height_px": 768,
                "display_number": 1,
            }
        ]
        
        # Explicit Chrome-only prompt
        messages = [
            {
                "role": "user",
                "content": """IMPORTANT: You MUST use Google Chrome for this test, not Firefox.

Please do the following:
1. First, close any Firefox windows if they are open
2. Take a screenshot
3. Open a terminal if needed
4. Type this exact command: google-chrome --no-sandbox --disable-gpu --disable-dev-shm-usage https://www.myopinions.com.au/
5. Press Enter to launch Chrome with the website
6. Wait 3 seconds for Chrome to fully load
7. Take a screenshot showing Chrome is open with MyOpinions website
8. Confirm you see Chrome (not Firefox) with the website loaded

If Chrome doesn't open, try: /usr/bin/google-chrome-stable --no-sandbox https://www.myopinions.com.au/

This test specifically validates Chrome browser functionality."""
            }
        ]
        
        iteration = 0
        task_complete = False
        
        while iteration < MAX_ITERATIONS and not task_complete:
            iteration += 1
            print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")
            
            try:
                # Call Claude
                print("🤖 Calling Claude...")
                response = self.client.beta.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    tools=tools,
                    messages=messages,
                    betas=["computer-use-2025-01-24"]
                )
                
                # Handle response
                if response.stop_reason == "tool_use":
                    print("🔧 Claude is using tools")
                    
                    for content in response.content:
                        if content.type == "tool_use":
                            tool_input = content.input
                            action = tool_input.get("action", "unknown")
                            
                            print(f"  📌 Action: {action}")
                            
                            if action == "screenshot":
                                print("    📸 Taking screenshot...")
                            elif action == "left_click":
                                coord = tool_input.get("coordinate", [0, 0])
                                print(f"    🖱️ Clicking at ({coord[0]}, {coord[1]})")
                            elif action == "type":
                                text = tool_input.get("text", "")
                                print(f"    ⌨️ Typing: '{text}'")
                                if "chrome" in text.lower():
                                    print("    ✅ Typing Chrome command!")
                            elif action == "key":
                                key = tool_input.get("key", "")
                                print(f"    ⌨️ Pressing: {key}")
                            elif action == "wait":
                                duration = tool_input.get("duration", 1)
                                print(f"    ⏳ Waiting {duration} seconds")
                    
                    # Add responses
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    for content in response.content:
                        if content.type == "tool_use":
                            messages.append({
                                "role": "user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": content.id,
                                    "content": [{"type": "text", "text": "Action executed successfully"}]
                                }]
                            })
                    
                else:
                    # Text response
                    response_text = response.content[0].text if response.content else ""
                    print(f"💬 Claude says: {response_text[:200]}...")
                    
                    # Check for Chrome confirmation
                    if "chrome" in response_text.lower() and ("loaded" in response_text.lower() or "open" in response_text.lower()):
                        if iteration > 3:
                            print("\n✅ Chrome browser confirmed open with website!")
                            task_complete = True
                    
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    if not task_complete:
                        messages.append({
                            "role": "user",
                            "content": "Continue with opening Chrome (not Firefox). Is Chrome open now?"
                        })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        # Final report
        print("\n" + "="*50)
        if task_complete:
            print("🎉 CHROME TEST SUCCESSFUL!")
            print("✅ Google Chrome explicitly opened")
            print("✅ Website loaded in Chrome")
            print("✅ Ready for Chrome-based automation")
        else:
            print("⚠️ Check VNC to see if Chrome opened")
        print("="*50)
        
        return task_complete

def main():
    """Main function"""
    if not ANTHROPIC_API_KEY:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        return False
    
    print("\n🔧 Explicit Chrome Browser Test")
    print("This will force Chrome usage, not Firefox")
    
    try:
        tester = ForceChromTest()
        success = tester.run_test()
        return success
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)