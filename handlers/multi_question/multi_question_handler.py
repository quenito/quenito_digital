"""Main handler for multi-question pages"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .multi_question_brain import MultiQuestionBrain
from .multi_question_patterns import MultiQuestionPatterns

@dataclass
class MultiQuestionResponse:
    """Response for multiple questions"""
    responses: List[Dict[str, Any]]
    success: bool
    confidence: float

class MultiQuestionHandler:
    """Handles automation of multi-question pages"""
    
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
        self.detector = MultiQuestionBrain()
        self.patterns = MultiQuestionPatterns(knowledge_base)
    
    def calculate_confidence(self, vision_result: Dict) -> float:
        """Calculate confidence for handling multi-question page"""
        
        # Base confidence from vision
        vision_confidence = vision_result.get('confidence_rating', 0) / 100
        
        # Check if we can parse the questions properly
        questions = self.detector.parse_questions(vision_result)
        if not questions:
            return 0.0
        
        # Calculate confidence based on known question types
        known_questions = 0
        for q in questions:
            category = self.detector.identify_question_category(q['text'])
            if category != 'unknown':
                known_questions += 1
        
        parse_confidence = known_questions / len(questions) if questions else 0
        
        # Combined confidence
        return min(0.95, (vision_confidence * 0.6) + (parse_confidence * 0.4))
    
    def handle(self, vision_result: Dict, element_type: str = None) -> MultiQuestionResponse:
        """Generate responses for all questions on the page"""
        
        if not self.detector.is_multi_question(vision_result):
            return MultiQuestionResponse(responses=[], success=False, confidence=0.0)
        
        questions = self.detector.parse_questions(vision_result)
        responses = []
        
        for question in questions:
            category = self.detector.identify_question_category(question['text'])
            response_value = self.patterns.get_response_for_category(category)
            
            responses.append({
                'question': question['text'],
                'type': question['type'],
                'category': category,
                'value': response_value,
                'selector_hints': self._get_selector_hints(question['type'], category)
            })
        
        confidence = self.calculate_confidence(vision_result)
        
        return MultiQuestionResponse(
            responses=responses,
            success=True,
            confidence=confidence
        )
    
    def _get_selector_hints(self, input_type: str, category: str) -> Dict:
        """Get selector hints for automation"""
        
        hints = {
            'type': input_type,
            'category': category,
            'selectors': []
        }
        
        # Type-specific selectors
        if input_type in ['radio', 'radio button']:
            hints['selectors'] = [
                f'input[type="radio"]',
                f'label:has-text("{category}")'
            ]
        elif input_type in ['text', 'text input', 'textbox']:
            hints['selectors'] = [
                f'input[type="text"]',
                f'input[type="number"]',
                f'input[placeholder*="{category}"]'
            ]
        elif input_type in ['dropdown', 'select']:
            hints['selectors'] = [
                'select',
                f'select[name*="{category}"]'
            ]
        elif input_type == 'checkbox':
            hints['selectors'] = [
                'input[type="checkbox"]',
                f'label:has-text("{category}")'
            ]
        
        return hints