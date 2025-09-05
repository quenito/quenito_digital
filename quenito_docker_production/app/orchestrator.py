#!/usr/bin/env python3
"""
Quenito Production Orchestrator
Simplified version for initial testing
"""

import anthropic
import asyncio
import json
import os
import sys
from datetime import datetime

class QuenitoOrchestrator:
    """
    Main Quenito controller - matches demo container configuration
    """
    
    def __init__(self):
        # Use exact model from successful demo
        self.MODEL = "claude-sonnet-4-20250514"
        self.API_PROVIDER = "anthropic"
        
        # Initialize Anthropic client
        self.client = anthropic.AsyncAnthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
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
    
    async def wait_for_manual_setup(self):
        """Wait for human to complete login/captcha/navigation"""
        print("\n" + "="*60)
        print("MANUAL SETUP PHASE")
        print("="*60)
        print("\n1. Connect via VNC: vnc://localhost:5900")
        print("   Password: quenito123")
        print("\n2. In Firefox, navigate to survey site")
        print("3. Login to your account")
        print("4. Handle any CAPTCHA")
        print("5. Start a survey and get to the first question")
        print("\n6. Return here and press Enter...")
        print("="*60 + "\n")
        
        input("Press Enter when you're on the first survey question: ")
        
        print("\n✅ Quenito taking over now!\n")
        print("="*60)
        
    async def complete_survey(self):
        """Main survey completion loop"""
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
                
                # Call Computer Use API
                print(f"\n📝 Processing question {self.questions_answered + 1}...")
                
                response = await self.client.beta.messages.create(
                    model=self.MODEL,
                    max_tokens=4096,
                    system=system_prompt if not messages else None,
                    tools=[
                        {
                            "type": "computer_20241022",
                            "name": "computer",
                            "display_width_px": 1920,
                            "display_height_px": 1080
                        }
                    ],
                    messages=messages + [{"role": "user", "content": user_message}]
                )
                
                # Check response
                response_text = str(response.content)
                print(f"Response: {response_text[:200]}...")
                
                # Check for completion
                if any(phrase in response_text.lower() for phrase in 
                       ["survey complete", "thank you", "survey has been completed"]):
                    print("\n🎉 Survey completed!")
                    break
                
                # Check if manual intervention needed
                if any(word in response_text.lower() for word in 
                       ["cannot", "unable", "failed", "error"]):
                    await self.request_manual_intervention()
                    messages = []  # Clear context after manual intervention
                    continue
                
                # Continue conversation if tool use requested
                if response.stop_reason == "tool_use":
                    messages.append({"role": "assistant", "content": response.content})
                    # In production, tool results would be added here
                    # For now, we'll simulate continuation
                    messages.append({"role": "user", "content": [
                        {"type": "tool_result", "content": "Action completed"}
                    ]})
                    
                self.questions_answered += 1
                print(f"✅ Question {self.questions_answered} completed")
                
                # Small delay to not overwhelm the system
                await asyncio.sleep(2)
                
            except KeyboardInterrupt:
                print("\n⏸️  Paused - Manual intervention")
                input("Press Enter to resume: ")
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
        
        input("Press Enter when ready to continue: ")
        print("\n✅ Resuming Quenito...\n")

async def main():
    """Main entry point"""
    print("\n🤖 QUENITO PRODUCTION v1.0")
    print("="*60)
    
    # Check API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("ERROR: ANTHROPIC_API_KEY not set!")
        sys.exit(1)
    
    # Run orchestrator
    orchestrator = QuenitoOrchestrator()
    await orchestrator.complete_survey()

if __name__ == "__main__":
    asyncio.run(main())
