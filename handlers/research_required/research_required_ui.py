#!/usr/bin/env python3
"""
🔬 Research Required UI Module
Handles all UI interactions for research questions
"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio

class ResearchRequiredUI:
    """UI interaction methods for research required questions"""
    
    def __init__(self, page):
        """Initialize with page object"""
        self.page = page
        print("🖥️ Research Required UI module initialized")
    
    async def detect_ui_elements(self) -> Dict[str, Any]:
        """Detect available UI elements for research questions"""
        elements = {
            'text_areas': [],
            'text_inputs': [],
            'skip_button': None,
            'submit_button': None,
            'buttons': [],
            'instructions': None
        }
        
        try:
            # Check for text areas (most common for research responses)
            text_areas = await self.page.query_selector_all('textarea')
            if text_areas:
                elements['text_areas'] = text_areas
                print(f"📝 Found {len(text_areas)} text areas")
            
            # Check for text inputs
            text_inputs = await self.page.query_selector_all('input[type="text"]')
            if text_inputs:
                elements['text_inputs'] = text_inputs
                print(f"📝 Found {len(text_inputs)} text inputs")
            
            # Look for skip button
            skip_selectors = [
                'button:has-text("Skip")',
                'button:has-text("skip")',
                'button:has-text("Next")',
                'button:has-text("Pass")',
                'a:has-text("Skip")',
                'input[value="Skip"]'
            ]
            
            for selector in skip_selectors:
                skip_button = await self.page.query_selector(selector)
                if skip_button:
                    elements['skip_button'] = skip_button
                    print("⏭️ Found skip button")
                    break
            
            # Find submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Submit")',
                'button:has-text("Continue")',
                'button:has-text("Next")'
            ]
            
            for selector in submit_selectors:
                submit_button = await self.page.query_selector(selector)
                if submit_button:
                    # Make sure it's not the skip button
                    if submit_button != elements['skip_button']:
                        elements['submit_button'] = submit_button
                        print("✅ Found submit button")
                        break
            
            # Get all buttons for analysis
            all_buttons = await self.page.query_selector_all('button, input[type="button"], input[type="submit"]')
            elements['buttons'] = all_buttons
            
            # Look for instruction text
            instruction_element = await self._find_instruction_text()
            if instruction_element:
                elements['instructions'] = instruction_element
                print("📋 Found instruction text")
            
        except Exception as e:
            print(f"❌ Error detecting UI elements: {e}")
        
        return elements
    
    async def _find_instruction_text(self) -> Optional[Any]:
        """Find instruction text that might contain research requirements"""
        selectors = [
            '.instructions', '.question-instructions',
            'p:has-text("research")', 'div:has-text("research")',
            '.research-instructions', '.additional-info'
        ]
        
        for selector in selectors:
            try:
                element = await self.page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and len(text) > 20:
                        return element
            except:
                continue
        
        return None
    
    async def handle_skip(self, elements: Dict[str, Any]) -> bool:
        """Try to skip the research question"""
        try:
            if elements['skip_button']:
                await elements['skip_button'].click()
                print("⏭️ Clicked skip button")
                await asyncio.sleep(0.5)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error skipping question: {e}")
            return False
    
    async def submit_placeholder_response(self, elements: Dict[str, Any], response: str) -> bool:
        """Submit a placeholder response"""
        try:
            # Try text areas first
            if elements['text_areas']:
                text_area = elements['text_areas'][0]
                await text_area.fill(response)
                print(f"📝 Filled text area with: {response}")
                
                # Submit if button available
                if elements['submit_button']:
                    await asyncio.sleep(0.3)
                    await elements['submit_button'].click()
                    print("📤 Submitted placeholder response")
                    return True
            
            # Try text inputs
            elif elements['text_inputs']:
                text_input = elements['text_inputs'][0]
                await text_input.fill(response)
                print(f"📝 Filled text input with: {response}")
                
                # Submit
                if elements['submit_button']:
                    await asyncio.sleep(0.3)
                    await elements['submit_button'].click()
                    print("📤 Submitted placeholder response")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error submitting response: {e}")
            return False
    
    async def get_question_text(self) -> str:
        """Extract the question text from the page"""
        try:
            # Common question selectors
            selectors = [
                'h1', 'h2', 'h3', 'h4',
                '.question-text', '.question',
                'label:has-text("research")',
                'div[role="heading"]',
                '.survey-question'
            ]
            
            for selector in selectors:
                element = await self.page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and len(text) > 10:
                        # Check if it contains research-related keywords
                        research_keywords = ['research', 'look up', 'find', 'investigate', 'gather']
                        if any(keyword in text.lower() for keyword in research_keywords):
                            return text.strip()
            
            # Fallback: get all text and find research-related content
            all_text = await self.page.inner_text('body')
            lines = all_text.split('\n')
            
            for line in lines:
                if len(line) > 20 and any(keyword in line.lower() for keyword in ['research', 'look up', 'find information']):
                    return line.strip()
            
            return ""
            
        except Exception as e:
            print(f"❌ Error getting question text: {e}")
            return ""
    
    async def extract_research_requirements(self, elements: Dict[str, Any]) -> List[str]:
        """Extract specific research requirements from the page"""
        requirements = []
        
        try:
            # Check instruction element
            if elements.get('instructions'):
                text = await elements['instructions'].inner_text()
                requirements.append(text)
            
            # Check for lists of items to research
            list_selectors = ['ul li', 'ol li', '.research-item', '.requirement']
            for selector in list_selectors:
                items = await self.page.query_selector_all(selector)
                for item in items:
                    text = await item.inner_text()
                    if text and len(text) > 5:
                        requirements.append(text.strip())
            
            # Check for bullet points or numbered items in main text
            main_text_element = await self.page.query_selector('.question-content, .survey-content, main')
            if main_text_element:
                text = await main_text_element.inner_text()
                # Extract items that look like research topics
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('•') or line.startswith('-') or 
                               (len(line) > 2 and line[0].isdigit() and line[1] in '.)')):
                        requirements.append(line)
            
        except Exception as e:
            print(f"⚠️ Error extracting requirements: {e}")
        
        return requirements
    
    async def check_for_required_field(self, elements: Dict[str, Any]) -> bool:
        """Check if the research field is required"""
        try:
            # Check text areas
            for text_area in elements.get('text_areas', []):
                required = await text_area.get_attribute('required')
                if required:
                    return True
                
                # Check for aria-required
                aria_required = await text_area.get_attribute('aria-required')
                if aria_required == 'true':
                    return True
            
            # Check text inputs
            for text_input in elements.get('text_inputs', []):
                required = await text_input.get_attribute('required')
                if required:
                    return True
                
                aria_required = await text_input.get_attribute('aria-required')
                if aria_required == 'true':
                    return True
            
            # Check for required indicators in labels
            labels = await self.page.query_selector_all('label')
            for label in labels:
                text = await label.inner_text()
                if '*' in text or 'required' in text.lower():
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking required status: {e}")
            return False