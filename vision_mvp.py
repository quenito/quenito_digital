import os
from openai import OpenAI
import base64
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class QuenitoVision:
    """Quenito's eyes - simplified and working!"""
    
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.patterns_dir = "personas/quenito/visual_patterns"
        os.makedirs(self.patterns_dir, exist_ok=True)
    
    async def analyze_screenshot(self, screenshot_path, question_context=""):
        """See and understand any survey question"""
        
        # Read and encode the image
        with open(screenshot_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        try:
            # IMPROVED PROMPT - More specific about returning text labels
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": """Analyze this survey question screenshot and tell me:
                                1. What type of question is this? (age, gender, checkbox, radio, dropdown, text, etc)
                                2. What is the exact question text?
                                3. What clickable elements do you see? List the TEXT/LABELS of all options (e.g., "YouTube", "Male", "25-34")
                                4. Is there a Continue/Next button visible?
                                5. Rate your confidence 0-100
                                
                                IMPORTANT: For checkboxes and radio buttons, always return the TEXT LABEL of options, never just numbers or indices.
                                For example, return "YouTube" not "1", return "Male" not "0", return "25-34" not "3"
                                
                                Respond in JSON format with keys:
                                - question_type
                                - question_text or exact_question_text
                                - clickable_elements
                                - continue_button_visible
                                - confidence_rating"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            # Get the response
            content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                # Clean up the response if needed
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                    
                return json.loads(content)
            except:
                # If JSON parsing fails, return the raw response
                return {
                    "raw_response": content,
                    "question_type": "parse_error",
                    "error": "Could not parse JSON response"
                }
                
        except Exception as e:
            print(f"❌ Error calling API: {str(e)}")
            return {
                "question_type": "error",
                "error": str(e)
            }
    
    async def store_pattern(self, screenshot_path, vision_result, automation_data):
        """Store visual pattern for future learning"""
        
        pattern_id = f"pattern_{int(datetime.now().timestamp())}"
        pattern_file = os.path.join(self.patterns_dir, f"{pattern_id}.json")
        
        # Store the pattern data
        pattern_data = {
            "id": pattern_id,
            "timestamp": datetime.now().isoformat(),
            "screenshot": screenshot_path,
            "vision_analysis": vision_result,
            "automation": automation_data
        }
        
        try:
            with open(pattern_file, 'w') as f:
                json.dump(pattern_data, f, indent=2)
            
            print(f"💾 Saved pattern to: {pattern_file}")
            return pattern_id
            
        except Exception as e:
            print(f"❌ Error saving pattern: {str(e)}")
            return None