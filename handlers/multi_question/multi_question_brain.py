# !python

"""Brain for multi-question pages - detection and intelligence"""

from typing import Dict, List, Any, Optional

class MultiQuestionBrain:
    """Brain for detecting and parsing multi-question pages"""
    
    @staticmethod
    def is_multi_question(vision_result: Dict) -> bool:
        """Check if vision detected multiple questions"""
        question_type = vision_result.get('question_type', '')
        
        # Check if it's a list (multiple questions)
        if isinstance(question_type, list):
            return True
            
        # Check for specific text patterns
        exact_text = vision_result.get('exact_question_text', [])
        if isinstance(exact_text, list) and len(exact_text) > 1:
            return True
            
        return False
    
    @staticmethod
    def parse_questions(vision_result: Dict) -> List[Dict]:
        """Parse individual questions from vision result"""
        questions = []
        
        # Handle different vision response formats
        question_types = vision_result.get('question_type', [])
        question_texts = vision_result.get('exact_question_text', [])
        
        # Format 1: Array of dictionaries (best format)
        if isinstance(question_types, list) and len(question_types) > 0:
            if isinstance(question_types[0], dict):
                # Already structured perfectly
                for q in question_types:
                    questions.append({
                        'text': q.get('question', ''),
                        'type': q.get('type', 'unknown'),
                        'index': len(questions)
                    })
            else:
                # Format 2: Parallel arrays
                if isinstance(question_texts, list):
                    for i, (q_type, q_text) in enumerate(zip(question_types, question_texts)):
                        questions.append({
                            'text': q_text,
                            'type': q_type,
                            'index': i
                        })
        
        return questions
    
    @staticmethod
    def identify_question_category(question_text: str) -> str:
        """Identify what category of question this is"""
        text_lower = question_text.lower()
        
        # Demographics
        if any(word in text_lower for word in ['gender', 'male', 'female']):
            return 'gender'
        elif any(word in text_lower for word in ['birth year', 'born', 'age']):
            return 'birth_year'
        elif any(word in text_lower for word in ['sexuality', 'sexual orientation']):
            return 'sexuality'
        elif any(word in text_lower for word in ['country', 'reside', 'live']):
            return 'country'
        elif any(word in text_lower for word in ['state', 'territory', 'province']):
            return 'state'
        elif any(word in text_lower for word in ['postcode', 'postal', 'zip']):
            return 'postcode'
        elif any(word in text_lower for word in ['education', 'degree', 'qualification']):
            return 'education'
        elif any(word in text_lower for word in ['income', 'salary', 'earn']):
            return 'income'
        elif any(word in text_lower for word in ['employment', 'occupation', 'work']):
            return 'employment'
        
        return 'unknown'