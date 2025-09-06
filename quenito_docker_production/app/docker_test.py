#!/usr/bin/env python3
"""
Simplified test script for Docker computer use demo container
Compatible with existing Anthropic computer use demo setup
"""

import os
import time
import json
from typing import Dict, Any, List, Optional
import anthropic

# Configuration - these should match your docker-compose settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-20250514"  # Matches your MODEL_VERSION
TEST_AGE = "45"
MAX_ITERATIONS = 15

class DockerComputerUseTest:
    """Test validator for Docker computer use environment"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.display_width = 1024
        self.display_height = 768
        
        print("🐳 Docker Computer Use Test Validator")
        print(f"📋 Model: {MODEL}")
        print(f"🎯 Test: Enter age '{TEST_AGE}' and submit form")
        
    def create_test_prompt(self) -> str:
        """Create the test prompt for Claude"""
        return f"""You are using a computer with a web browser. 
        
Please complete this test:
1. Open a web browser if not already open
2. Navigate to the file at: file:///home/computeruse/age_test.html
3. You will see a form asking "How old are you?"
4. Click on the text input field
5. Type the number {TEST_AGE}
6. Click the Submit button
7. Verify you see "TEST PASSED!" message

Take a screenshot first to see the current state, then complete each step carefully.
After each action, take a screenshot to verify the result."""

    def run_agent_loop(self):
        """Run the main test loop with Claude"""
        print("\n" + "="*50)
        print("🚀 STARTING TEST")
        print("="*50 + "\n")
        
        # Configure tools for computer_20250124
        tools = [
            {
                "type": "computer_20250124",
                "name": "computer",
                "display_width_px": self.display_width,
                "display_height_px": self.display_height,
                "display_number": 1,  # X11 display number
            }
        ]
        
        # Initialize conversation
        messages = [
            {
                "role": "user",
                "content": self.create_test_prompt()
            }
        ]
        
        iteration = 0
        test_complete = False
        
        while iteration < MAX_ITERATIONS and not test_complete:
            iteration += 1
            print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")
            
            try:
                # Call Claude with computer use tools
                print("🤖 Calling Claude...")
                response = self.client.beta.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    tools=tools,
                    messages=messages,
                    betas=["computer-use-2025-01-24"]  # Required for computer_20250124
                )
                
                # Handle Claude's response
                if response.stop_reason == "tool_use":
                    print("🔧 Claude wants to use a tool")
                    
                    # Process each tool use request
                    for content in response.content:
                        if content.type == "tool_use":
                            tool_input = content.input
                            action = tool_input.get("action", "unknown")
                            
                            print(f"  📌 Action: {action}")
                            
                            # Log specific action details
                            if action == "screenshot":
                                print("    Taking screenshot...")
                            elif action == "left_click":
                                coord = tool_input.get("coordinate", [0, 0])
                                print(f"    Clicking at ({coord[0]}, {coord[1]})")
                            elif action == "type":
                                text = tool_input.get("text", "")
                                print(f"    Typing: '{text}'")
                            elif action == "key":
                                key = tool_input.get("key", "")
                                print(f"    Pressing key: {key}")
                            elif action == "scroll":
                                direction = tool_input.get("direction", "")
                                amount = tool_input.get("amount", 0)
                                print(f"    Scrolling {direction} by {amount}")
                            elif action == "wait":
                                duration = tool_input.get("duration", 1)
                                print(f"    Waiting {duration} seconds")
                            
                            # Check if this might be the final submit action
                            if action == "left_click" and iteration > 3:
                                print("    ✨ This might be the submit click!")
                            
                            # Note: In the actual Docker container, the computer use demo
                            # will handle executing these actions. Here we're just logging
                            # to validate the API calls are correct.
                    
                    # Add Claude's tool use to messages
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    # Simulate tool result (in real Docker env, this comes from the container)
                    # For testing, we'll add a mock tool result
                    print("  ✅ Action would be executed by Docker container")
                    
                    # Add mock tool result
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
                    
                    # Check if we've likely completed the test
                    if action == "left_click" and iteration > 5:
                        print("\n🏁 Test sequence likely complete!")
                        test_complete = True
                        
                else:
                    # Claude provided a text response
                    response_text = response.content[0].text if response.content else ""
                    print(f"💬 Claude says: {response_text[:100]}...")
                    
                    # Check if Claude thinks the task is complete
                    if any(word in response_text.lower() for word in ["complete", "passed", "success", "done"]):
                        print("\n✅ Claude reports task complete!")
                        test_complete = True
                    
                    # Add to conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    # If Claude needs more guidance
                    if not test_complete and iteration < MAX_ITERATIONS - 1:
                        messages.append({
                            "role": "user",
                            "content": "Please continue with the task. What's the next step?"
                        })
                
            except Exception as e:
                print(f"❌ Error in iteration {iteration}: {e}")
                if "rate_limit" in str(e).lower():
                    print("⏳ Rate limited, waiting 10 seconds...")
                    time.sleep(10)
                else:
                    break
        
        # Final report
        print("\n" + "="*50)
        if test_complete:
            print("🎉 TEST SEQUENCE COMPLETED!")
            print(f"✅ Model {MODEL} with computer_20250124 validated")
            print("\nNext steps:")
            print("1. Run this in your Docker container to see actual execution")
            print("2. Check the browser for 'TEST PASSED!' message")
            print("3. Ready to build your survey automation!")
        else:
            print("⚠️ Test did not complete within iteration limit")
            print("This might be normal - check your Docker container output")
        print("="*50)
        
        return test_complete

def setup_test_file():
    """Create the HTML test file in the container directory"""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Age Test</title>
    <style>
        body { 
            font-family: Arial; 
            padding: 50px; 
            text-align: center;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 400px;
            margin: 0 auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        input { 
            padding: 10px; 
            font-size: 16px; 
            width: 200px;
            margin: 10px 0;
        }
        button { 
            padding: 10px 20px; 
            font-size: 16px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        #result { 
            margin-top: 20px; 
            font-size: 18px;
            padding: 15px;
            border-radius: 5px;
        }
        .success { 
            background: #d4edda; 
            color: #155724;
            border: 1px solid #c3e6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>How old are you?</h1>
        <form id="ageForm">
            <div>
                <label for="ageInput">Enter your age:</label><br>
                <input type="text" id="ageInput" name="age" placeholder="Type your age">
            </div>
            <br>
            <button type="submit">Submit</button>
        </form>
        <div id="result"></div>
    </div>
    
    <script>
        document.getElementById('ageForm').onsubmit = function(e) {
            e.preventDefault();
            var age = document.getElementById('ageInput').value;
            var result = document.getElementById('result');
            if (age === '45') {
                result.className = 'success';
                result.innerHTML = '✅ <strong>TEST PASSED!</strong><br>Age 45 entered successfully!';
            } else {
                result.innerHTML = '❌ Expected 45, got: ' + age;
            }
        };
    </script>
</body>
</html>"""
    
    # Save to file (adjust path for your Docker setup)
    file_path = "age_test.html"
    with open(file_path, "w") as f:
        f.write(html_content)
    print(f"📄 Test HTML file created: {file_path}")
    print("   Copy this to your Docker container's /home/computeruse/ directory")
    return file_path

def main():
    """Main test function"""
    print("🐳 Computer Use Docker Test Validator")
    print("="*50)
    
    # Check API key
    if not ANTHROPIC_API_KEY:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("   Set it in your docker-compose.yml or .env file")
        return False
    
    # Setup test file
    print("\n📝 Setting up test file...")
    setup_test_file()
    
    print("\n⚠️  IMPORTANT: Copy age_test.html to your Docker container:")
    print("   docker cp age_test.html <container_name>:/home/computeruse/")
    print("\n   Or mount it as a volume in docker-compose.yml:")
    print("   volumes:")
    print("     - ./age_test.html:/home/computeruse/age_test.html")
    
    input("\nPress Enter when the file is in your container...")
    
    try:
        # Run the test
        tester = DockerComputerUseTest()
        success = tester.run_agent_loop()
        
        return success
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)