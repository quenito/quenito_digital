#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're teaching Quenito to UNDERSTAND surveys, not just fill them.
Every decision should make him smarter, not just more mechanical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Page Orchestrator - Understanding survey FLOW, not just pages
Navigates with intelligence, not rules.
"""
import asyncio
import random
from typing import Dict, List, Optional

class PageOrchestrator:
    """
    Orchestrates page navigation and multi-question handling
    """
    
    def __init__(self, automation_service, llm_service, vision_service, page):
        self.automation = automation_service
        self.llm = llm_service
        self.vision = vision_service
        self.page = page
        
    async def handle_page(self, screenshot_base64: str) -> Dict:
        """
        Main orchestration based on page structure
        """
        # Get vision analysis
        vision_result = await self.vision.analyze_page(screenshot_base64)
        
        # Check for completion first
        if vision_result.get('is_complete'):
            return await self._handle_completion()
        
        # Check for transition page
        if vision_result.get('is_transition'):
            return await self._handle_transition()
        
        # Route based on page type
        page_type = vision_result.get('page_type', 'question_page')
        
        if page_type == 'multi_question':
            return await self._handle_multi_question_page(vision_result)
        elif page_type == 'matrix_page':
            return await self._handle_matrix_page(vision_result)
        else:
            return await self._handle_single_question(vision_result)
    
    async def _handle_completion(self) -> Dict:
        """
        Handle survey completion page
        """
        print("\n" + "="*60)
        print("🎉 SURVEY COMPLETE DETECTED!")
        print("="*60)
        print("✅ Stopping automation - survey is finished")
        
        return {
            "status": "complete",
            "action": "stop_automation",
            "message": "Survey successfully completed"
        }
    
    async def _handle_transition(self) -> Dict:
        """
        Handle transition/instruction pages
        """
        print("\n📄 TRANSITION PAGE - Just clicking continue...")
        
        # Find and click continue button
        await self._click_continue()
        
        return {
            "status": "transition",
            "action": "clicked_continue",
            "automated": True
        }
    
    async def _handle_multi_question_page(self, vision_result: Dict) -> Dict:
        """
        Handle pages with multiple questions (Age + Gender + Postcode)
        """
        questions = vision_result.get('questions', [])
        results = {
            "automated": [],
            "manual": [],
            "status": "success"
        }
        
        print(f"\n{'='*60}")
        print(f"📋 MULTI-QUESTION PAGE: {len(questions)} questions detected")
        print(f"{'='*60}")
        
        for i, question in enumerate(questions, 1):
            print(f"\n❓ Question {i}/{len(questions)}: {question['text'][:60]}...")
            
            # Special handling for birth year
            if question.get('is_birth_year') or 'born' in question['text'].lower():
                print("📅 Birth year detected - using dropdown selection")
                success = await self._handle_birth_year_dropdown()
                if success:
                    results["automated"].append("Birth year: 1980")
                else:
                    results["manual"].append(question)
                continue
            
            # Build context for LLM
            llm_context = self._build_multi_question_context(question, i, len(questions))
            
            # Get LLM response
            response = await self.llm.get_response_with_context({
                "question": question['text'],
                "element_type": question.get('element_type', 'unknown'),
                "context": llm_context
            })

            # Extract the actual value from the response dictionary
            if response and isinstance(response, dict) and response.get('success'):
                response_value = response.get('value', '')
            elif response and isinstance(response, str):
                response_value = response
            else:
                response_value = None

            if response_value and response_value != "NEED_MANUAL":
                # Fill the field with the extracted string value
                success = await self._fill_field(question, response_value)
                if success:
                    results["automated"].append(f"{question['text']}: {response_value}")
                    print(f"✅ Automated: {response_value}")
        
        # Handle manual interventions if needed
        if results["manual"]:
            print(f"\n🔧 {len(results['manual'])} fields need manual input")
            print("Please fill these fields manually:")
            for q in results["manual"]:
                print(f"  • {q['text'][:60]}...")
            print("\n⚠️ Fill ALL fields but do NOT click continue")
            print("Press ENTER here when done...")
            input()
        
        # Now click continue
        print("\n✅ All fields complete, clicking continue...")
        await self._click_continue()
        
        return results
    
    async def _handle_single_question(self, vision_result: Dict) -> Dict:
        """
        Handle standard single question page
        """
        # Check if it's actually a transition page that wasn't caught
        question_text = vision_result.get('questions', [{}])[0].get('text', '')
        
        transition_phrases = [
            "we are now going to",
            "in the next section",
            "please read",
            "following statement",
            "we will show you"
        ]
        
        if any(phrase in question_text.lower() for phrase in transition_phrases):
            print("📄 Detected transition text - just clicking continue")
            await self._click_continue()
            return {"status": "transition", "automated": True}
        
        # Regular question handling
        return {"status": "use_standard_flow"}
    
    async def _handle_matrix_page(self, vision_result: Dict) -> Dict:
        """
        Handle matrix/grid questions
        """
        # Let existing handlers deal with matrices
        return {"status": "use_handlers"}
    
    async def _handle_birth_year_dropdown(self) -> bool:
        """
        Specific handling for birth year dropdown
        """
        try:
            # Find the dropdown element
            dropdowns = await self.page.query_selector_all("select")
            
            for dropdown in dropdowns:
                # Check if it contains years
                options_text = await dropdown.inner_text()
                if "1980" in options_text or "1979" in options_text:
                    # This is likely the birth year dropdown
                    await dropdown.select_option(value="1980")
                    print("✅ Selected 1980 from birth year dropdown")
                    return True
            
            print("⚠️ Could not find birth year dropdown")
            return False
            
        except Exception as e:
            print(f"❌ Error handling birth year: {e}")
            return False
    
    async def _click_continue(self) -> bool:
        """
        Click continue/next button
        """
        try:
            # Try multiple selectors
            selectors = [
                "button:has-text('Continue')",
                "button:has-text('Next')",
                "button:has-text('Submit')",
                "input[type='submit']",
                "button[type='submit']",
                ".continue-button",
                "#continue-button"
            ]
            
            for selector in selectors:
                try:
                    button = await self.page.query_selector(selector)
                    if button and await button.is_visible():
                        await button.click()
                        print(f"✅ Clicked continue button")
                        await self.page.wait_for_load_state("networkidle", timeout=5000)
                        return True
                except:
                    continue
            
            print("⚠️ Could not find continue button")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking continue: {e}")
            return False
    
    async def _fill_field(self, question: Dict, response: str) -> bool:
        """
        Fill a field based on question info and element type
        """
        try:
            element_type = question.get('element_type', 'unknown')
            
            if element_type == 'text':
                inputs = await self.page.query_selector_all("input[type='text']:visible")
                if inputs and len(inputs) > question.get('id', 1) - 1:
                    await inputs[question.get('id', 1) - 1].fill(response)
                    return True
                    
            elif element_type == 'radio':
                # Find radio with matching label
                radios = await self.page.query_selector_all("input[type='radio']")
                for radio in radios:
                    label = await self._get_element_label(radio)
                    if response.lower() in label.lower():
                        await radio.click()
                        return True
                        
            elif element_type == 'dropdown':
                selects = await self.page.query_selector_all("select")
                if selects and len(selects) > question.get('id', 1) - 1:
                    await selects[question.get('id', 1) - 1].select_option(label=response)
                    return True
                    
        except Exception as e:
            print(f"❌ Error filling field: {e}")
        
        return False
    
    async def _get_element_label(self, element) -> str:
        """
        Get label text for an element
        """
        try:
            # Try aria-label first
            label = await element.get_attribute("aria-label")
            if label:
                return label
            
            # Try finding associated label
            id_attr = await element.get_attribute("id")
            if id_attr:
                label_element = await self.page.query_selector(f"label[for='{id_attr}']")
                if label_element:
                    return await label_element.inner_text()
            
            # Try next sibling text
            parent = await element.evaluate_handle("el => el.parentElement")
            if parent:
                text = await parent.inner_text()
                return text
                
        except:
            pass
        
        return ""
    
    def _build_multi_question_context(self, question: Dict, index: int, total: int) -> str:
        """
        Build context for multi-question pages
        """
        context = f"""
        This is question {index} of {total} on this page.
        Question: {question['text']}
        Element Type: {question.get('element_type', 'unknown')}
        
        IMPORTANT:
        - Answer this specific question with your personal details
        - Age: 45, Gender: Male, Postcode: 2217
        - Do NOT click continue yet - more questions to answer
        - Fill this field then move to the next question
        
        Your answer for this field:
        """
        
        return context