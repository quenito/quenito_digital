import os
from openai import OpenAI
import base64
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class QuenitoVision:
    """Quenito's eyes - simplified and working! NOW WITH PLATFORM ORGANIZATION!"""
    
    def __init__(self, model="gpt-4o-mini", platform="myopinions"):
        self.client = OpenAI()
        self.model = model
        self.platform = platform  # Track which platform we're on
        
        # Base patterns directory
        self.base_patterns_dir = "personas/quenito/visual_patterns"
        
        # Platform-specific subdirectory
        self.patterns_dir = os.path.join(self.base_patterns_dir, platform)
        
        # Create directories if they don't exist
        os.makedirs(self.patterns_dir, exist_ok=True)
        
        # Also ensure base dir exists for backward compatibility
        os.makedirs(self.base_patterns_dir, exist_ok=True)
        
        print(f"👁️ Vision initialized for platform: {platform}")
        print(f"📁 Patterns will be saved to: {self.patterns_dir}")
    
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
        """Store visual pattern for future learning - NOW WITH PLATFORM ORGANIZATION!"""
        
        # Generate pattern ID with platform prefix
        pattern_id = f"{self.platform}_pattern_{int(datetime.now().timestamp())}"
        pattern_file = os.path.join(self.patterns_dir, f"{pattern_id}.json")
        
        # Store the pattern data with platform info
        pattern_data = {
            "id": pattern_id,
            "platform": self.platform,  # Track which platform this is from
            "timestamp": datetime.now().isoformat(),
            "screenshot": screenshot_path,
            "vision_analysis": vision_result,
            "automation": automation_data
        }
        
        try:
            with open(pattern_file, 'w') as f:
                json.dump(pattern_data, f, indent=2)
            
            print(f"💾 Saved {self.platform} pattern to: {pattern_file}")
            return pattern_id
            
        except Exception as e:
            print(f"❌ Error saving pattern: {str(e)}")
            return None
    
    def get_platform_patterns(self, platform=None):
        """Get all patterns for a specific platform or current platform"""
        target_platform = platform or self.platform
        platform_dir = os.path.join(self.base_patterns_dir, target_platform)
        
        if not os.path.exists(platform_dir):
            return []
        
        patterns = []
        for filename in os.listdir(platform_dir):
            if filename.endswith('.json'):
                with open(os.path.join(platform_dir, filename), 'r') as f:
                    patterns.append(json.load(f))
        
        return patterns
    
    def get_all_patterns(self):
        """Get patterns from ALL platforms for cross-platform learning"""
        all_patterns = {}
        
        # Check each platform subdirectory
        if os.path.exists(self.base_patterns_dir):
            for platform_dir in os.listdir(self.base_patterns_dir):
                platform_path = os.path.join(self.base_patterns_dir, platform_dir)
                if os.path.isdir(platform_path):
                    all_patterns[platform_dir] = self.get_platform_patterns(platform_dir)
        
        return all_patterns
    
    def migrate_existing_patterns(self):
        """One-time migration to move existing patterns to myopinions folder"""
        migrated_count = 0
        
        # Check for patterns in the base directory
        for filename in os.listdir(self.base_patterns_dir):
            file_path = os.path.join(self.base_patterns_dir, filename)
            
            # Only process JSON files in the root (not in subdirectories)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                # Move to myopinions subdirectory
                myopinions_dir = os.path.join(self.base_patterns_dir, "myopinions")
                os.makedirs(myopinions_dir, exist_ok=True)
                
                new_path = os.path.join(myopinions_dir, filename)
                
                # Load, update, and save with platform info
                with open(file_path, 'r') as f:
                    pattern_data = json.load(f)
                
                # Add platform if not present
                if 'platform' not in pattern_data:
                    pattern_data['platform'] = 'myopinions'
                
                # Save to new location
                with open(new_path, 'w') as f:
                    json.dump(pattern_data, f, indent=2)
                
                # Remove old file
                os.remove(file_path)
                migrated_count += 1
                print(f"📦 Migrated: {filename} → myopinions/")
        
        if migrated_count > 0:
            print(f"✅ Migrated {migrated_count} patterns to platform folders!")
        
        return migrated_count