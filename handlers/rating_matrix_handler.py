"""
Rating Matrix Handler Module
Handles rating matrix and agreement scale questions.
"""

from .base_handler import BaseQuestionHandler


class RatingMatrixHandler(BaseQuestionHandler):
    """
    Handles rating matrix and agreement scale questions.
    """
    
    def can_handle(self, page_content: str) -> float:
        """
        Determine confidence for handling rating matrix and agreement scale questions.
        
        Returns:
            float: Confidence score (0.0-1.0)
        """
        content_lower = page_content.lower()
        
        # TODO: Implement specific detection logic for rating matrix and agreement scale
        keywords = ['strongly agree', 'somewhat agree', 'disagree', 'rating', 'scale']
        
        if self.check_keywords_in_content(keywords, content_lower):
            matches = self.count_keyword_matches(keywords, content_lower)
            confidence = min(matches * 0.2, 0.8)  # Max 0.8 confidence
            return confidence
        
        return 0.0
    
    def handle(self) -> bool:
        """
        Process rating matrix and agreement scale questions.
        
        Returns:
            bool: True if successfully handled
        """
        self.log_handler_start()
        
        # TODO: Implement specific handling logic for rating matrix and agreement scale
        
        # For now, request manual intervention
        return self.request_intervention(
            "RatingMatrixHandler not yet fully implemented - manual completion recommended"
        )

    def check_keywords_in_content(self, content: str, keywords: list) -> float:
        """Basic keyword checking method for handlers missing this functionality"""
        if not content or not keywords:
            return 0.0
        
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
        confidence = min(matches / len(keywords), 1.0) if keywords else 0.0
        
        print(f"🔍 Keyword check: {matches}/{len(keywords)} matches = {confidence:.3f} confidence")
        return confidence