# handler_adapter.py
"""
Simple adapter to use handlers for automation without complex initialization
This bridges between the learning system and the handler architecture
Now with smart age detection for both text and radio formats!
"""

class SimpleHandler:
    """Simplified handler interface for automation attempts"""
    
    def __init__(self, knowledge_base, handler_type):
        self.kb = knowledge_base
        self.handler_type = handler_type
        
    def calculate_confidence(self, question_type, question_text):
        """Calculate confidence based on knowledge base data"""
        
        # Check if we have learned responses for this type
        learned_responses = 0
        
        # Count learned patterns
        if 'detailed_intervention_learning' in self.kb.data:
            for entry in self.kb.data['detailed_intervention_learning'].values():
                if entry.get('question_type') == question_type:
                    learned_responses += 1
        
        # Base confidence from learning
        base_confidence = min(0.9, 0.3 + (learned_responses * 0.1))
        
        # Boost for specific known patterns
        text_lower = question_text.lower()
        
        if self.handler_type == 'demographics':
            if any(word in text_lower for word in ['age', 'old', 'year born']):
                return min(0.95, base_confidence + 0.2)
            elif any(word in text_lower for word in ['gender', 'pronoun']):
                return min(0.95, base_confidence + 0.15)
            elif any(word in text_lower for word in ['postcode', 'postal', 'zip']):
                return min(0.95, base_confidence + 0.1)
                
        return base_confidence
    
    def handle(self, question_text):
        """Get response from knowledge base"""
        
        # Create response object
        class Response:
            def __init__(self, value):
                self.response_value = value
        
        # Try to find a learned response
        text_lower = question_text.lower()
        
        # Direct mappings from profile
        if 'age' in text_lower or 'old' in text_lower:
            return Response(self.kb.data.get('user_profile', {}).get('age', '45'))
        elif 'gender' in text_lower or 'pronoun' in text_lower:
            return Response('Male')
        elif 'postcode' in text_lower or 'postal' in text_lower:
            return Response(self.kb.data.get('user_profile', {}).get('postcode', '2217'))
        elif 'income' in text_lower:
            return Response('$350,000 - $399,999')
            
        return None


class SmartHandler:
    """Enhanced handler that handles both age formats"""
    
    def __init__(self, knowledge_base, handler_type):
        self.kb = knowledge_base
        self.handler_type = handler_type
        
        # Age range mappings from universal detector
        self.age_ranges = {
            '18-24': range(18, 25),
            '25-34': range(25, 35),
            '35-44': range(35, 45),
            '45-54': range(45, 55),
            '55-64': range(55, 65),
            '65+': range(65, 120)
        }
    
    def handle(self, question_text, element_type=None):
        """Get response based on element type"""
        
        class Response:
            def __init__(self, value):
                self.response_value = value
        
        text_lower = question_text.lower()
        
        # Handle age questions
        if 'age' in text_lower or 'old' in text_lower:
            user_age = int(self.kb.data.get('user_profile', {}).get('age', '45'))
            
            # Check if this is a radio range question
            if element_type == 'radio' or any(r in question_text for r in ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']):
                # Find appropriate age range
                for range_label, age_range in self.age_ranges.items():
                    if user_age in age_range:
                        return Response(range_label)
                # Fallback
                return Response('45-54')
            else:
                # Text input - return exact age
                return Response(str(user_age))
        
        # Other demographics
        elif 'gender' in text_lower or 'pronoun' in text_lower:
            return Response('Male')
        elif 'postcode' in text_lower or 'postal' in text_lower:
            return Response(self.kb.data.get('user_profile', {}).get('postcode', '2217'))
        elif 'income' in text_lower:
            return Response('$350,000 - $399,999')
            
        return None
    
    def calculate_confidence(self, question_type, question_text):
        """Calculate confidence with awareness of age format"""
        
        # Base confidence calculation (existing)
        learned_responses = 0
        
        if 'detailed_intervention_learning' in self.kb.data:
            for entry in self.kb.data['detailed_intervention_learning'].values():
                if entry.get('question_type') == question_type:
                    learned_responses += 1
        
        base_confidence = min(0.9, 0.3 + (learned_responses * 0.1))
        
        text_lower = question_text.lower()
        
        if self.handler_type == 'demographics':
            if any(word in text_lower for word in ['age', 'old', 'year born']):
                # High confidence for both text and radio age questions
                return min(0.95, base_confidence + 0.2)
            elif any(word in text_lower for word in ['gender', 'pronoun']):
                return min(0.95, base_confidence + 0.15)
            elif any(word in text_lower for word in ['postcode', 'postal', 'zip']):
                return min(0.95, base_confidence + 0.1)
                
        return base_confidence


# Create simple handlers for automation
def create_simple_handlers(kb):
    """Create simplified handlers for automation testing"""
    return {
        'demographics': SmartHandler(kb, 'demographics'),
        'general': SmartHandler(kb, 'general'),
        'rating_matrix': SmartHandler(kb, 'rating_matrix'),
        'brand_familiarity': SmartHandler(kb, 'brand_familiarity'),
        'multi_select': SmartHandler(kb, 'multi_select')
    }