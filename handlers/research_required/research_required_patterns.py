#!/usr/bin/env python3
"""
🔬 Research Required Patterns Module
Centralizes all pattern definitions from knowledge_base.json
"""

from typing import Dict, List, Any, Optional, Tuple
import re

class ResearchRequiredPatterns:
    """Pattern definitions and detection for research-based questions"""
    
    def __init__(self, patterns_data: Optional[Dict[str, Any]] = None):
        """Initialize with patterns from knowledge base"""
        self.patterns_data = patterns_data or {}
        
        # Extract pattern categories
        self.keywords = self.patterns_data.get('keywords', [])
        self.primary_indicators = self.patterns_data.get('primary_indicators', [])
        self.enhanced_patterns = self.patterns_data.get('enhanced_patterns', [])
        self.research_types = self.patterns_data.get('research_types', {})
        self.action_keywords = self.patterns_data.get('action_keywords', {})
        self.confidence_thresholds = self.patterns_data.get('confidence_thresholds', {})
        self.response_strategies = self.patterns_data.get('response_strategies', {})
        self.ui_patterns = self.patterns_data.get('ui_patterns', {})
        self.learning_indicators = self.patterns_data.get('learning_indicators', {})
        
        print(f"🔬 Research Required Patterns initialized with {len(self.keywords)} keywords")
        print(f"📊 {len(self.research_types)} research types loaded")
    
    def calculate_confidence(self, question_text: str) -> float:
        """Calculate confidence score for research questions"""
        confidence = self.confidence_thresholds.get('base', 0.3)
        question_lower = question_text.lower()
        
        # Check primary indicators (highest boost)
        for indicator in self.primary_indicators:
            if indicator.lower() in question_lower:
                confidence += self.confidence_thresholds.get('indicator_boost', 0.4)
                print(f"🎯 Primary indicator matched: '{indicator}'")
                break
        
        # Check enhanced patterns
        for pattern in self.enhanced_patterns:
            if re.search(pattern, question_lower):
                confidence += self.confidence_thresholds.get('pattern_boost', 0.2)
                print(f"🔍 Enhanced pattern matched: '{pattern}'")
                break
        
        # Check keywords
        keyword_matches = sum(1 for keyword in self.keywords if keyword.lower() in question_lower)
        if keyword_matches > 0:
            confidence += self.confidence_thresholds.get('keyword_boost', 0.1) * min(keyword_matches, 2)
            print(f"📝 {keyword_matches} keywords matched")
        
        # Check action keywords
        for action_type, actions in self.action_keywords.items():
            for action in actions:
                if action.lower() in question_lower:
                    confidence += self.confidence_thresholds.get('action_boost', 0.1)
                    print(f"⚡ Action keyword detected: {action} ({action_type})")
                    break
        
        return min(confidence, 1.0)
    
    def detect_research_type(self, question_text: str) -> Optional[str]:
        """Detect the type of research required"""
        question_lower = question_text.lower()
        
        for research_type, indicators in self.research_types.items():
            for indicator in indicators:
                if indicator.lower() in question_lower:
                    return research_type
        
        return 'general'  # Default type
    
    def get_response_strategy(self, ui_elements: Dict[str, Any], user_preferences: Dict[str, Any] = None) -> str:
        """Determine the best response strategy"""
        # Check if skip is available
        if self._can_skip(ui_elements):
            return 'skip'
        
        # Check user preferences
        if user_preferences and user_preferences.get('auto_acknowledge_research', False):
            return 'acknowledge'
        
        # Default to placeholder
        return 'placeholder'
    
    def _can_skip(self, ui_elements: Dict[str, Any]) -> bool:
        """Check if skip option is available"""
        skip_keywords = ['skip', 'next', 'pass', 'continue without']
        
        # Check buttons
        if ui_elements.get('buttons'):
            for button in ui_elements['buttons']:
                # This would need to be async in real implementation
                # For now, return based on UI detection
                return True  # Simplified for pattern module
        
        return False
    
    def get_placeholder_response(self, research_type: str) -> str:
        """Get appropriate placeholder response based on research type"""
        type_specific_responses = {
            'product': "Product specifications to be researched",
            'company': "Company information pending research",
            'market': "Market analysis to be conducted",
            'technical': "Technical details to be gathered",
            'general': "Information to be researched"
        }
        
        return type_specific_responses.get(research_type, "Pending research")
    
    def get_acknowledgment_response(self, research_type: str) -> str:
        """Get appropriate acknowledgment based on research type"""
        acknowledgments = self.response_strategies.get('acknowledge', {}).get('responses', [])
        
        if acknowledgments:
            # Could randomize or select based on context
            return acknowledgments[0]
        
        return "I understand this requires research"
    
    def is_research_instruction(self, text: str) -> bool:
        """Check if text is giving research instructions rather than asking a question"""
        instruction_patterns = [
            r'please\s+research',
            r'you\s+should\s+research',
            r'need\s+to\s+research',
            r'research\s+the\s+following',
            r'look\s+up\s+the\s+following',
            r'find\s+information\s+about'
        ]
        
        text_lower = text.lower()
        for pattern in instruction_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def extract_research_topics(self, question_text: str) -> List[str]:
        """Extract specific topics that need research"""
        topics = []
        
        # Common patterns for listing research items
        patterns = [
            r'research[:\s]+(.+?)(?:\?|$)',
            r'look up[:\s]+(.+?)(?:\?|$)',
            r'find information about[:\s]+(.+?)(?:\?|$)',
            r'investigate[:\s]+(.+?)(?:\?|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, question_text.lower())
            for match in matches:
                # Split by common delimiters
                items = re.split(r'[,;]|\sand\s', match)
                topics.extend([item.strip() for item in items if item.strip()])
        
        return topics