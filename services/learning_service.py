#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're teaching Quenito to UNDERSTAND surveys, not just fill them.
Every decision should make him smarter, not just more mechanical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Learning Service - Growing smarter with every interaction
Captures patterns, not rules. Builds understanding, not scripts.
"""
from typing import Dict, Any, Optional
import time

class LearningService:
    """Service for capturing and learning from manual inputs"""
    
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.session_id = f"learning_{int(time.time())}"
    
    async def capture_manual_response(self, page, question_num: int, 
                                     vision_result: Optional[Dict] = None) -> Dict[str, Any]:
        """Capture user's manual response for learning"""
        
        capture_data = {
            'question_num': question_num,
            'timestamp': time.time(),
            'session_id': self.session_id
        }
        
        try:
            # Extract question text
            question_text = await self._extract_question_text(page)
            capture_data['question_text'] = question_text
            
            # Determine question type
            capture_data['question_type'] = self._classify_question(question_text)
            
            # Capture user's selections
            user_response = await self._capture_form_values(page)
            capture_data['response_value'] = user_response.get('primary', '')
            capture_data['response_values'] = user_response.get('all', [])
            
            # Enhance with vision if available
            if vision_result:
                capture_data['vision_confidence'] = vision_result.get('confidence_rating', 0)
                capture_data['vision_type'] = vision_result.get('question_type', '')
            
            # Store in knowledge base
            self._store_learning(capture_data)
            
            return capture_data
            
        except Exception as e:
            print(f"⚠️ Learning capture error: {e}")
            return capture_data
    
    async def _extract_question_text(self, page) -> str:
        """Extract question text from page"""
        selectors = [
            'h2:has-text("?")',
            'h3:has-text("?")',
            'label:has-text("?")',
            '.question-text',
            'legend'
        ]
        
        for selector in selectors:
            try:
                elem = await page.query_selector(selector)
                if elem:
                    text = await elem.inner_text()
                    if len(text) > 10:
                        return text.strip()
            except:
                continue
        
        return "Question text not found"
    
    async def _capture_form_values(self, page) -> Dict[str, Any]:
        """Capture all form values - FIXED for radio button label capture"""
        values = {'primary': '', 'all': []}
        
        # Check radio buttons - ENHANCED to get label text not value
        radios = await page.query_selector_all('input[type="radio"]:checked')
        for radio in radios:
            # First try to get the visible label text
            label_text = None
            
            # Method 1: Check for label with 'for' attribute
            radio_id = await radio.get_attribute('id')
            if radio_id:
                try:
                    label = await page.query_selector(f'label[for="{radio_id}"]')
                    if label:
                        label_text = await label.inner_text()
                except:
                    pass
            
            # Method 2: Check if radio is inside a label
            if not label_text:
                try:
                    label_text = await radio.evaluate('''(el) => {
                        const label = el.closest('label');
                        if (label) {
                            // Get text but exclude the input element itself
                            const text = label.textContent.trim();
                            return text;
                        }
                        return null;
                    }''')
                except:
                    pass
            
            # Method 3: Check for adjacent text (next sibling)
            if not label_text:
                try:
                    label_text = await radio.evaluate('''(el) => {
                        // Check next sibling
                        let next = el.nextSibling;
                        while (next && next.nodeType !== Node.ELEMENT_NODE) {
                            if (next.nodeType === Node.TEXT_NODE && next.textContent.trim()) {
                                return next.textContent.trim();
                            }
                            next = next.nextSibling;
                        }
                        // Check next element sibling
                        const nextEl = el.nextElementSibling;
                        if (nextEl && (nextEl.tagName === 'LABEL' || nextEl.tagName === 'SPAN')) {
                            return nextEl.textContent.trim();
                        }
                        return null;
                    }''')
                except:
                    pass
            
            # Method 4: Check parent's text content
            if not label_text:
                try:
                    label_text = await radio.evaluate('''(el) => {
                        const parent = el.parentElement;
                        if (parent && (parent.tagName === 'LABEL' || parent.tagName === 'DIV')) {
                            // Clone parent, remove input, get text
                            const clone = parent.cloneNode(true);
                            const inputs = clone.querySelectorAll('input');
                            inputs.forEach(input => input.remove());
                            return clone.textContent.trim();
                        }
                        return null;
                    }''')
                except:
                    pass
            
            # If we got label text, use it. Otherwise fall back to value attribute
            if label_text and label_text.strip():
                values['all'].append(label_text.strip())
                print(f"      📻 Captured radio label: {label_text.strip()}")
            else:
                # Fallback to value attribute (but warn about it)
                value = await radio.get_attribute('value')
                if value:
                    print(f"      ⚠️ Warning: Using value attribute '{value}' (couldn't find label)")
                    values['all'].append(value)
        
        # Check checkboxes - Already working correctly
        checkboxes = await page.query_selector_all('input[type="checkbox"]:checked')
        for checkbox in checkboxes:
            value = await checkbox.get_attribute('value')
            if not value or value == 'on':
                # Try to get label
                label = await self._get_label_for_input(page, checkbox)
                if label:
                    value = label
            if value and value != 'on':
                values['all'].append(value)
                print(f"      ☑️ Captured checkbox: {value}")
        
        # Check text inputs
        text_inputs = await page.query_selector_all('input[type="text"]:visible, input[type="number"]:visible')
        for input_elem in text_inputs:
            value = await input_elem.input_value()
            if value:
                values['all'].append(value)
                print(f"      📝 Captured text: {value}")
        
        # Check dropdowns - ENHANCED to get text not value
        selects = await page.query_selector_all('select')
        for select in selects:
            try:
                # Get the selected option's TEXT not its value
                selected_text = await select.evaluate('''(sel) => {
                    const option = sel.options[sel.selectedIndex];
                    return option ? option.textContent.trim() : null;
                }''')
                if selected_text:
                    values['all'].append(selected_text)
                    print(f"      📋 Captured dropdown text: {selected_text}")
            except:
                pass
        
        # Set primary value
        if values['all']:
            values['primary'] = values['all'][0]
        
        print(f"      📊 Total captured: {len(values['all'])} values")
        
        return values
    
    async def _get_label_for_input(self, page, input_elem) -> Optional[str]:
        """Get label text for an input element"""
        try:
            input_id = await input_elem.get_attribute('id')
            if input_id:
                label = await page.query_selector(f'label[for="{input_id}"]')
                if label:
                    return await label.inner_text()
            
            # Try parent label
            label_text = await input_elem.evaluate('''(el) => {
                const label = el.closest('label');
                return label ? label.textContent.trim() : null;
            }''')
            
            return label_text
        except:
            return None
    
    def _classify_question(self, question_text: str) -> str:
        """Classify question type based on text"""
        text_lower = question_text.lower()
        
        if 'age' in text_lower or 'old' in text_lower:
            return 'demographics_age'
        elif 'gender' in text_lower:
            return 'demographics_gender'
        elif 'postcode' in text_lower or 'zip' in text_lower:
            return 'demographics_postcode'
        elif 'brand' in text_lower:
            return 'brand_awareness'
        elif 'rate' in text_lower or 'rating' in text_lower:
            return 'rating_scale'
        elif 'select all' in text_lower or 'which of' in text_lower:
            return 'multi_select'
        else:
            return 'general'
    
    def _store_learning(self, capture_data: Dict):
        """Store learning in knowledge base"""
        if 'detailed_intervention_learning' not in self.kb.data:
            self.kb.data['detailed_intervention_learning'] = {}
        
        learning_key = f"learning_{int(capture_data['timestamp'])}_{capture_data['question_num']}"
        self.kb.data['detailed_intervention_learning'][learning_key] = capture_data
        
        # Save immediately
        self.kb.save()
        
        print(f"💾 Stored learning: {learning_key}")