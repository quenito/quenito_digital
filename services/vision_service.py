#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vision Service - Teaching Quenito to SEE patterns, not match templates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fixed: Better error handling for API responses
"""
import json
import base64
import os
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

class VisionService:
    """
    Enhanced vision service with structural page understanding
    """
    
    def __init__(self):
        # Load environment variables - EXACTLY like LLM service!
        load_dotenv()
        
        # Initialize OpenAI client - EXACTLY like LLM service!
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.enabled = True
        
        print("✅ Vision Service initialized with API key")
    
    async def analyze_page(self, screenshot_base64: str) -> Dict:
        """
        Comprehensive page analysis with structure detection
        FIXED: Better error handling for empty/malformed responses
        """
        try:
            analysis_prompt = """Analyze this survey page and provide detailed structural information.

            CRITICAL DETECTIONS:
            
            1. PAGE TYPE IDENTIFICATION:
               - "question_page" = Has actual questions to answer
               - "multi_question" = Multiple questions on same page
               - "transition_page" = Just instructions with Continue button
               - "completion_page" = Survey complete/thank you page
               - "matrix_page" = Rating grid or checkbox matrix
            
            2. FOR TRANSITION PAGES:
               Look for phrases like:
               - "We are now going to show you..."
               - "In the next section..."
               - "Please read the following..."
            
            3. FOR COMPLETION PAGES:
               Look for:
               - "Thank you for participating"
               - "Survey complete"
               - "Points have been credited"
            
            Return ONLY valid JSON with this structure:
            {
                "page_type": "question_page",
                "is_transition": false,
                "is_complete": false,
                "question_count": 1,
                "questions": [
                    {
                        "text": "question text here",
                        "element_type": "radio/checkbox/text/dropdown",
                        "id": 1
                    }
                ],
                "confidence_rating": 85
            }
            
            IMPORTANT: Return ONLY the JSON object, no markdown, no explanations."""
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are analyzing survey pages. Return ONLY valid JSON, no markdown or explanations."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": analysis_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{screenshot_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Get the content
            content = response.choices[0].message.content
            
            # Check if response is empty
            if not content or content.strip() == "":
                print("⚠️ Empty vision response, using defaults")
                return self._get_default_response()
            
            # Clean the content - remove markdown if present
            content = content.strip()
            
            # Remove markdown code blocks if present
            if "```json" in content:
                # Extract JSON from markdown
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                if json_end > json_start:
                    content = content[json_start:json_end].strip()
            elif "```" in content:
                # Remove generic markdown blocks
                content = content.replace("```", "").strip()
            
            # Try to parse JSON
            try:
                result = json.loads(content)
                
                # Validate the structure
                if not isinstance(result, dict):
                    print("⚠️ Invalid JSON structure (not a dict), using defaults")
                    return self._get_default_response()
                
                # Ensure required fields exist
                if "page_type" not in result:
                    result["page_type"] = "question_page"
                if "is_transition" not in result:
                    result["is_transition"] = False
                if "is_complete" not in result:
                    result["is_complete"] = False
                if "questions" not in result:
                    result["questions"] = []
                if "confidence_rating" not in result:
                    result["confidence_rating"] = 70
                
                # Log critical detections
                if result.get('is_transition'):
                    print("🔄 TRANSITION PAGE DETECTED - Will skip to next")
                if result.get('is_complete'):
                    print("✅ COMPLETION PAGE DETECTED - Survey finished!")
                    
                return result
                
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing error: {e}")
                print(f"   Content was: {content[:200]}...")
                return self._get_default_response()
            
        except Exception as e:
            print(f"❌ Vision analysis error: {e}")
            return self._get_default_response()
    
    def _get_default_response(self) -> Dict:
        """
        Return a safe default response when vision fails
        """
        return {
            "page_type": "question_page",
            "is_transition": False,
            "is_complete": False,
            "question_count": 1,
            "questions": [],
            "confidence_rating": 0,
            "error": True
        }
    
    async def detect_element_type(self, screenshot_base64: str, element_description: str) -> str:
        """
        Specific element type detection when main analysis is uncertain
        """
        prompt = f"""
        Look at this form element: {element_description}
        
        DETERMINE THE EXACT TYPE:
        - If it has a dropdown arrow and shows years = "dropdown"
        - If it has circular radio buttons = "radio"
        - If it has square checkboxes = "checkbox"
        - Birth year questions are ALWAYS dropdowns!
        
        Return only one word: dropdown, radio, checkbox, or text
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{screenshot_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=10,
                temperature=0
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            # Validate the response
            valid_types = ["dropdown", "radio", "checkbox", "text", "select", "textarea"]
            if result in valid_types:
                return result
            else:
                return "unknown"
            
        except Exception as e:
            print(f"⚠️ Element detection error: {e}")
            return "unknown"