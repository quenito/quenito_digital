import os
import json
from openai import OpenAI
from typing import Dict, List, Optional, Any
import base64
from datetime import datetime
from dotenv import load_dotenv

class ConsciousnessEngine:
    def __init__(self, consciousness_path: str = "matt_consciousness_v2.json"):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client with error handling
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.consciousness = self.load_consciousness(consciousness_path)
        self.test_results = []
        
    def load_consciousness(self, path: str) -> dict:
        """Load Matt's consciousness from JSON file"""
        with open(path, 'r') as f:
            return json.load(f)
    
    async def analyze_screenshot(self, screenshot_path: str) -> Dict:
        """Extract question and options from screenshot using GPT-4 Vision"""
        with open(screenshot_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": """Analyze this survey screenshot and extract the question, any subheadings/instructions, and options.

    IMPORTANT: Capture BOTH the main question AND any subheading or instruction text that appears below it.

    Identify the question type:
    - DROPDOWN/SELECT: If you see dropdown menus, select boxes, or fields with arrows indicating dropdowns
    - GRID/MATRIX: If you see a table/grid where each row needs its own answer
    - MULTI-SELECT: If instructions say "select multiple" or "select up to X" with checkboxes
    - SINGLE-SELECT: If there are radio buttons for choosing one option

    For DROPDOWN questions (date of birth, location selectors, etc):
    - Set "question_type" to "dropdown"
    - List the dropdown fields in "dropdown_fields" (e.g., ["Month", "Year"] or ["Country", "State", "City"])
    - If there are visible options, list them in "options"

    For GRID/MATRIX questions:
    - Set "question_type" to "grid"
    - List items needing answers in "grid_items" 
    - List column options in "options"

    For MULTI-SELECT questions:
    - Set "question_type" to "multi_select"
    - List all options in "options"
    - Include selection limit in "selection_limit"

    For SINGLE-SELECT questions:
    - Set "question_type" to "single_select"
    - List all options in "options"

    Return ONLY valid JSON:
    {
        "question": "the main question text",
        "subheading": "any instruction text (if present)",
        "question_type": "dropdown|grid|multi_select|single_select",
        "dropdown_fields": ["field1", "field2"], // only for dropdown type
        "options": ["option1", "option2"], // if options are visible
        "selection_limit": 6, // only for multi-select
        "grid_items": ["item1", "item2"] // only for grid
    }"""},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }],
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            result = json.loads(content)
            
            # Log detection for debugging
            if result.get('question_type') == 'dropdown':
                print(f"✅ Dropdown question detected with fields: {result.get('dropdown_fields', [])}")
            
            return result
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {content}")
            return {
                "question": "Parse error",
                "question_type": "unknown",
                "raw_response": content,
                "error": "Could not parse JSON response"
            }
    
    async def reason_and_answer(self, question: str, options: List[str] = None, question_type: str = None, grid_items: List[str] = None, subheading: str = None, selection_limit: int = None) -> Dict:
        """Core reasoning engine - this is where Matt thinks"""
        
        # Combine question with subheading for full context
        full_question = question
        if subheading:
            full_question = f"{question}\n{subheading}"
        
        # Detect question type patterns from both question and subheading
        is_multi_select = question_type == "multi_select" or any(phrase in full_question.lower() for phrase in [
            'select up to', 'maximum of', 'choose multiple', 'select all', 
            'check all', 'select a maximum', 'select at least'
        ])
        
        is_grid = question_type == "grid" or any(phrase in question.lower() for phrase in [
            'for each', 'each of the following', 'rate each', 'for every'
        ])
        
        # Build appropriate prompt based on question type
        if is_grid and grid_items:
            prompt = f"""You are Matt, a 45-year-old data analyst from Sydney, Australia. 
Here is your complete consciousness and identity:

{json.dumps(self.consciousness, indent=2)}

GRID QUESTION: {question}
Items to evaluate: {grid_items}
Options for each item: {options}

This is a GRID question where you must select one option for EACH item listed.

Based on your consciousness, especially your consumption patterns:
- Beer: Pale ales (Balter XPA), 1-2 some weekdays, 3-4 weekends
- Sparkling cider: Every few months with wife  
- Wine: 1-2 times per year at restaurants
- Spirits: Rarely, sometimes not even once a year

IMPORTANT: You MUST provide an answer for EACH item in the grid.

Respond with JSON only:
{{
    "answer": {{
        "Beer": "selected option for beer",
        "Spirits": "selected option for spirits",
        "Red wine (incl. Rose)": "selected option",
        // ... one entry for each grid item
    }},
    "reasoning": "your authentic thought process as Matt",
    "confidence": 0.0-1.0
}}"""

        elif is_multi_select:
            # Multi-select prompt with selection limit awareness
            limit_instruction = ""
            if selection_limit:
                limit_instruction = f"\nIMPORTANT: You must select EXACTLY {selection_limit} options."
            elif subheading and "maximum" in subheading.lower():
                limit_instruction = f"\nIMPORTANT: Follow the selection instructions: {subheading}"
            
            prompt = f"""You are Matt, a 45-year-old data analyst from Sydney, Australia. 
Here is your complete consciousness and identity:

{json.dumps(self.consciousness, indent=2)}

Survey Question: {question}
{f'Instructions: {subheading}' if subheading else ''}
Available Options: {options}

This is a MULTI-SELECT question. {limit_instruction}

For personality/values questions, select options that truly reflect who you are:
- Family-focused father of two young daughters
- Practical, efficiency-driven but values human connection
- Data analyst who enjoys solving puzzles
- Right-leaning practical voter
- Sports enthusiast (NRL, F1, NASCAR)

Respond with JSON only:
{{
    "answer": ["option1", "option2", "option3"],
    "reasoning": "your authentic thought process as Matt",
    "confidence": 0.0-1.0
}}"""

        else:
            # Single-select prompt (default)
            prompt = f"""You are Matt, a 45-year-old data analyst from Sydney, Australia. 
Here is your complete consciousness and identity:

{json.dumps(self.consciousness, indent=2)}

Survey Question: {question}
Available Options: {options if options else "Free text response required"}

Select the ONE option that best represents how Matt would respond.

Respond with JSON only:
{{
    "answer": "exact option text or value to select",
    "reasoning": "your authentic thought process as Matt",
    "confidence": 0.0-1.0
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        result['timestamp'] = datetime.now().isoformat()
        result['question'] = question
        result['question_type'] = question_type or ("grid" if is_grid else "multi_select" if is_multi_select else "single_select")
        
        return result
    
    async def test_screenshot_flow(self, before_path: str, after_path: str = None) -> Dict:
        """Complete test flow for screenshot comparison"""
        
        # Extract question from screenshot
        screenshot_data = await self.analyze_screenshot(before_path)
        
        # Get Matt's reasoned answer
        answer = await self.reason_and_answer(
            screenshot_data['question'],
            screenshot_data.get('options'),
            screenshot_data.get('question_type'),
            screenshot_data.get('grid_items'),
            screenshot_data.get('subheading'),
            screenshot_data.get('selection_limit')
        )
        
        # Store for analysis
        test_result = {
            "screenshot": before_path,
            "question": screenshot_data['question'],
            "question_type": screenshot_data.get('question_type', 'unknown'),
            "options": screenshot_data.get('options'),
            "grid_items": screenshot_data.get('grid_items'),
            "llm_answer": answer['answer'],
            "reasoning": answer['reasoning'],
            "confidence": answer['confidence']
        }
        
        if after_path:
            test_result['matt_actual_answer'] = "To be extracted from after screenshot"
            
        self.test_results.append(test_result)
        
        return test_result
    
    def generate_test_report(self) -> str:
        """Generate report of test results"""
        report = "CONSCIOUSNESS ENGINE TEST REPORT\n" + "="*60 + "\n\n"
        
        total_confidence = 0
        for i, result in enumerate(self.test_results, 1):
            report += f"Test {i}: {result['question'][:50]}...\n"
            report += f"Question Type: {result.get('question_type', 'unknown')}\n"
            report += f"Answer: {result['llm_answer']}\n"
            report += f"Confidence: {result['confidence']:.0%}\n"
            report += f"Reasoning: {result['reasoning'][:200]}...\n"
            report += "-"*40 + "\n"
            total_confidence += result['confidence']
        
        avg_confidence = total_confidence / len(self.test_results) if self.test_results else 0
        report += f"\nAVERAGE CONFIDENCE: {avg_confidence:.0%}\n"
        
        return report