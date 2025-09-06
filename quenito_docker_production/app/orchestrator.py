#!/usr/bin/env python3
"""
Quenito Production Orchestrator V2
Complete implementation with action execution layer
"""

import anthropic
import asyncio
import json
import os
import sys
import select
import base64
import subprocess
import time
from datetime import datetime
from PIL import Image
from io import BytesIO

class ComputerActionExecutor:
    """
    Executes computer use actions in the Docker environment
    """
    
    def __init__(self, display=":99", width=1280, height=800):
        self.display = display
        self.width = width
        self.height = height
        os.environ['DISPLAY'] = display
        
    def take_screenshot(self):
        """Capture screenshot and return as base64"""
        try:
            # Use scrot to capture screenshot
            screenshot_path = '/tmp/screenshot.png'
            subprocess.run(['scrot', screenshot_path], check=True, capture_output=True)
            
            # Open and resize if needed
            with Image.open(screenshot_path) as img:
                # Resize if larger than our max dimensions
                if img.width > self.width or img.height > self.height:
                    img.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
            # Clean up
            os.remove(screenshot_path)
            print("📸 Screenshot captured")
            return img_base64
            
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def click(self, x, y, button='left'):
        """Click at coordinates"""
        try:
            button_map = {'left': '1', 'middle': '2', 'right': '3'}
            button_num = button_map.get(button, '1')
            
            # Move to position and click
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=True)
            subprocess.run(['xdotool', 'click', button_num], check=True)
            
            print(f"🖱️ Clicked at ({x}, {y})")
            time.sleep(0.5)  # Small delay for UI to respond
            return True
            
        except Exception as e:
            print(f"❌ Click error: {e}")
            return False
    
    def type_text(self, text):
        """Type text"""
        try:
            # Use xdotool to type text
            subprocess.run(['xdotool', 'type', text], check=True)
            print(f"⌨️ Typed: '{text}'")
            time.sleep(0.3)
            return True
            
        except Exception as e:
            print(f"❌ Type error: {e}")
            return False
    
    def press_key(self, key):
        """Press a key or key combination"""
        try:
            # Handle special keys and combinations
            key_mapping = {
                'Enter': 'Return',
                'Tab': 'Tab',
                'Escape': 'Escape',
                'Backspace': 'BackSpace',
                'Delete': 'Delete',
                'Up': 'Up',
                'Down': 'Down',
                'Left': 'Left',
                'Right': 'Right',
                'PageUp': 'Page_Up',
                'PageDown': 'Page_Down',
                'Home': 'Home',
                'End': 'End'
            }
            
            # Check if it's a combination (e.g., "ctrl+a")
            if '+' in key:
                keys = key.split('+')
                # Build xdotool command for key combination
                cmd = ['xdotool', 'key']
                cmd.append('+'.join([key_mapping.get(k, k) for k in keys]))
            else:
                # Single key
                xdo_key = key_mapping.get(key, key)
                cmd = ['xdotool', 'key', xdo_key]
            
            subprocess.run(cmd, check=True)
            print(f"⌨️ Pressed: {key}")
            time.sleep(0.3)
            return True
            
        except Exception as e:
            print(f"❌ Key press error: {e}")
            return False
    
    def mouse_move(self, x, y):
        """Move mouse to coordinates"""
        try:
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=True)
            print(f"🖱️ Moved to ({x}, {y})")
            return True
            
        except Exception as e:
            print(f"❌ Mouse move error: {e}")
            return False
    
    def scroll(self, direction='down', amount=3):
        """Scroll in a direction"""
        try:
            # xdotool uses button 4 for up, 5 for down
            button = '5' if direction == 'down' else '4'
            
            for _ in range(amount):
                subprocess.run(['xdotool', 'click', button], check=True)
                time.sleep(0.1)
            
            print(f"📜 Scrolled {direction} {amount} times")
            return True
            
        except Exception as e:
            print(f"❌ Scroll error: {e}")
            return False
    
    def wait(self, seconds=1):
        """Wait for specified seconds"""
        print(f"⏳ Waiting {seconds} seconds...")
        time.sleep(seconds)
        return True

class QuenitoOrchestrator:
    """
    Main Quenito controller with full execution capabilities
    """
    
    def __init__(self):
        # Model configuration - matched to successful tests
        self.MODEL = "claude-sonnet-4-20250514"
        self.API_PROVIDER = "anthropic"
        
        # Display configuration - optimized resolution
        self.DISPLAY_WIDTH = 1280
        self.DISPLAY_HEIGHT = 800
        
        # Initialize Anthropic client
        self.client = anthropic.AsyncAnthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
        
        # Initialize action executor
        self.executor = ComputerActionExecutor(
            display=":99",
            width=self.DISPLAY_WIDTH,
            height=self.DISPLAY_HEIGHT
        )
        
        # Load Matt's consciousness
        self.consciousness = self.load_consciousness()
        self.questions_answered = 0
        self.manual_interventions = 0
        
    def load_consciousness(self):
        """Load Matt's consciousness file"""
        consciousness_path = '/app/consciousness/matt_consciousness_v3.json'
        if not os.path.exists(consciousness_path):
            print(f"ERROR: Consciousness file not found at {consciousness_path}")
            sys.exit(1)
            
        with open(consciousness_path, 'r') as f:
            return json.load(f)
    
    def wait_for_input(self, prompt="Press Enter to continue: ", timeout=None):
        """Robust input handler for Docker"""
        print(prompt, end='', flush=True)
        
        try:
            if sys.stdin.isatty():
                return input()
            else:
                sys.stdout.flush()
                if timeout:
                    ready, _, _ = select.select([sys.stdin], [], [], timeout)
                    if ready:
                        return sys.stdin.readline().strip()
                    else:
                        print("\n(Auto-continuing after timeout...)")
                        return ""
                else:
                    line = sys.stdin.readline().strip()
                    return line
                    
        except Exception as e:
            print(f"\n(Input error: {e}, auto-continuing...)")
            return ""
    
    async def execute_tool_call(self, tool_call):
        """
        Execute a tool call from Claude and return the result
        """
        tool_input = tool_call.input
        action = tool_input.get("action")
        
        print(f"  📌 Action: {action}")
        
        try:
            if action == "screenshot":
                screenshot = self.executor.take_screenshot()
                if screenshot:
                    return {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": screenshot
                        }
                    }
                else:
                    return {"type": "text", "text": "Failed to capture screenshot"}
            
            elif action == "left_click":
                coords = tool_input.get("coordinate", [0, 0])
                success = self.executor.click(coords[0], coords[1], 'left')
                return {"type": "text", "text": "Click successful" if success else "Click failed"}
            
            elif action == "right_click":
                coords = tool_input.get("coordinate", [0, 0])
                success = self.executor.click(coords[0], coords[1], 'right')
                return {"type": "text", "text": "Right-click successful" if success else "Right-click failed"}
            
            elif action == "middle_click":
                coords = tool_input.get("coordinate", [0, 0])
                success = self.executor.click(coords[0], coords[1], 'middle')
                return {"type": "text", "text": "Middle-click successful" if success else "Middle-click failed"}
            
            elif action == "double_click":
                coords = tool_input.get("coordinate", [0, 0])
                success = self.executor.click(coords[0], coords[1], 'left')
                if success:
                    time.sleep(0.1)
                    success = self.executor.click(coords[0], coords[1], 'left')
                return {"type": "text", "text": "Double-click successful" if success else "Double-click failed"}
            
            elif action == "type":
                text = tool_input.get("text", "")
                success = self.executor.type_text(text)
                return {"type": "text", "text": f"Typed '{text}'" if success else "Type failed"}
            
            elif action == "key":
                key = tool_input.get("key", "")
                success = self.executor.press_key(key)
                return {"type": "text", "text": f"Pressed {key}" if success else "Key press failed"}
            
            elif action == "mouse_move":
                coords = tool_input.get("coordinate", [0, 0])
                success = self.executor.mouse_move(coords[0], coords[1])
                return {"type": "text", "text": "Mouse moved" if success else "Mouse move failed"}
            
            elif action == "scroll":
                direction = tool_input.get("direction", "down")
                amount = tool_input.get("amount", 3)
                success = self.executor.scroll(direction, amount)
                return {"type": "text", "text": f"Scrolled {direction}" if success else "Scroll failed"}
            
            elif action == "wait":
                seconds = tool_input.get("seconds", 1)
                self.executor.wait(seconds)
                return {"type": "text", "text": f"Waited {seconds} seconds"}
            
            else:
                return {"type": "text", "text": f"Unknown action: {action}"}
                
        except Exception as e:
            print(f"  ❌ Action error: {e}")
            return {"type": "text", "text": f"Action failed: {str(e)}"}
    
    async def wait_for_manual_setup(self):
        """Wait for human to complete login/captcha/navigation"""
        print("\n" + "="*60)
        print("MANUAL SETUP PHASE")
        print("="*60)
        print("\n1. Connect via VNC: vnc://localhost:5900")
        print("   Password: quenito123")
        print("\n2. In browser, navigate to survey site")
        print("3. Login to your account")
        print("4. Handle any CAPTCHA")
        print("5. Start a survey and get to the first question")
        print("\n6. Return here and press Enter...")
        print("="*60 + "\n")
        
        self.wait_for_input("Press Enter when you're on the first survey question: ")
        
        print("\n✅ Quenito taking over now!\n")
        print("="*60)
        
    async def complete_survey(self):
        """Main survey completion loop with full execution"""
        # Wait for manual setup
        await self.wait_for_manual_setup()
        
        # Build system prompt with consciousness
        system_prompt = f"""You are completing a survey as Matt (Quenito).

IDENTITY AND CONSCIOUSNESS:
{json.dumps(self.consciousness, indent=2)}

INSTRUCTIONS:
1. Answer each question authentically as Matt would based on the consciousness data
2. For dropdowns with many items (like years): click field, use arrow keys to navigate, press Enter
3. For standard dropdowns: click and select directly
4. After answering, click Continue/Next/Submit to go to the next page
5. If you see "Thank you" or survey completion message, report completion

Take a screenshot first to see the current question, then proceed."""

        messages = []
        
        while True:
            try:
                # Reset context every 3 questions to prevent overflow
                if self.questions_answered > 0 and self.questions_answered % 3 == 0:
                    print(f"\n🔄 Resetting context after {self.questions_answered} questions...")
                    messages = []
                
                # Build user message
                if not messages:
                    user_message = "Take a screenshot and complete the current survey question as Matt."
                else:
                    user_message = "Continue to the next question."
                
                # Call Computer Use API with correct configuration
                print(f"\n🔍 Processing question {self.questions_answered + 1}...")
                
                response = await self.client.beta.messages.create(
                    model=self.MODEL,
                    max_tokens=4096,
                    system=system_prompt if not messages else None,
                    tools=[
                        {
                            "type": "computer_20250124",  # Correct tool version
                            "name": "computer",
                            "display_width_px": self.DISPLAY_WIDTH,   # Optimized resolution
                            "display_height_px": self.DISPLAY_HEIGHT,  # Optimized resolution
                            "display_number": 1  # X11 display number
                        }
                    ],
                    messages=messages + [{"role": "user", "content": user_message}],
                    betas=["computer-use-2025-01-24"]  # Required beta flag
                )
                
                # Process Claude's response
                if response.stop_reason == "tool_use":
                    # Claude wants to use tools
                    print("🔧 Executing actions...")
                    
                    # Add Claude's message to history
                    messages.append({"role": "assistant", "content": response.content})
                    
                    # Execute each tool call and collect results
                    tool_results = []
                    for content in response.content:
                        if content.type == "tool_use":
                            result = await self.execute_tool_call(content)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": [result]
                            })
                    
                    # Add tool results to messages
                    messages.append({"role": "user", "content": tool_results})
                    
                else:
                    # Claude provided a text response
                    response_text = response.content[0].text if response.content else ""
                    print(f"💬 Claude says: {response_text[:200]}...")
                    
                    # Check for completion
                    if any(phrase in response_text.lower() for phrase in 
                           ["survey complete", "thank you", "survey has been completed", "successfully submitted"]):
                        print("\n🎉 Survey completed!")
                        break
                    
                    # Check if manual intervention needed
                    if any(word in response_text.lower() for word in 
                           ["cannot", "unable", "failed", "error", "stuck"]):
                        await self.request_manual_intervention()
                        messages = []  # Clear context after manual intervention
                        continue
                    
                    # Add to message history
                    messages.append({"role": "assistant", "content": response.content})
                    
                    # Check if we've completed a question
                    if "continue" in response_text.lower() or "next" in response_text.lower():
                        self.questions_answered += 1
                        print(f"✅ Question {self.questions_answered} completed")
                
                # Small delay to not overwhelm the system
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("\n⏸️  Paused - Manual intervention")
                self.wait_for_input("Press Enter to resume: ")
                messages = []  # Clear context on resume
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Attempting recovery in 30 seconds...")
                await asyncio.sleep(30)
                messages = []
        
        # Final stats
        print("\n" + "="*60)
        print(f"SURVEY COMPLETE!")
        print(f"Questions answered: {self.questions_answered}")
        print(f"Manual interventions: {self.manual_interventions}")
        if self.questions_answered > 0:
            automation_rate = (1 - self.manual_interventions/self.questions_answered) * 100
            print(f"Automation rate: {automation_rate:.1f}%")
        print("="*60)
        
        # Save stats
        self.save_stats()
    
    async def request_manual_intervention(self):
        """Handle manual intervention request"""
        self.manual_interventions += 1
        print("\n" + "="*40)
        print("🔧 MANUAL INTERVENTION NEEDED")
        print("="*40)
        print("Please complete this question manually:")
        print("1. Use VNC viewer to complete question")
        print("2. Navigate to next question")
        print("3. Return here and press Enter")
        print("="*40 + "\n")
        
        self.wait_for_input("Press Enter when ready to continue: ")
        print("\n✅ Resuming Quenito...\n")
    
    def save_stats(self):
        """Save completion stats to file"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "questions_completed": self.questions_answered,
            "manual_interventions": self.manual_interventions,
            "automation_rate": (1 - self.manual_interventions/max(self.questions_answered, 1)) * 100
        }
        
        try:
            with open('/app/logs/status.json', 'w') as f:
                json.dump(stats, f, indent=2)
            print("📊 Stats saved to /app/logs/status.json")
        except Exception as e:
            print(f"⚠️ Could not save stats: {e}")

async def main():
    """Main entry point"""
    print("\n🤖 QUENITO PRODUCTION v2.0")
    print("="*60)
    print("Enhanced with full action execution")
    print("="*60)
    
    # Check API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("ERROR: ANTHROPIC_API_KEY not set!")
        print("\nTo fix this, run:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        print("docker-compose down")
        print("docker-compose up -d")
        sys.exit(1)
    else:
        print(f"✅ API Key detected: ...{os.environ.get('ANTHROPIC_API_KEY')[-8:]}")
    
    # Check for required tools
    required_tools = ['xdotool', 'scrot']
    for tool in required_tools:
        try:
            subprocess.run(['which', tool], check=True, capture_output=True)
            print(f"✅ {tool} found")
        except:
            print(f"❌ {tool} not found - installing...")
            subprocess.run(['apt-get', 'install', '-y', tool], check=True)
    
    # Run orchestrator
    orchestrator = QuenitoOrchestrator()
    await orchestrator.complete_survey()

if __name__ == "__main__":
    # For Docker exec compatibility
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 1)
    
    asyncio.run(main())