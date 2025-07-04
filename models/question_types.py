"""
Question Type Detection Module
Identifies different types of survey questions for appropriate handler selection.
"""


class QuestionTypeDetector:
    """
    Detects and classifies survey questions based on content analysis.
    """
    
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.question_stats = {
            "questions_processed": 0,
            "type_counts": {},
            "detection_history": []
        }
    
    def identify_question_type(self, page_content: str) -> str:
        """
        Identify the type of question based on page content.
        
        Args:
            page_content: The text content of the page
            
        Returns:
            str: The identified question type
        """
        content_lower = page_content.lower()
        
        # Track this detection
        self.question_stats["questions_processed"] += 1
        
        # Question type detection logic (from your original system)
        detected_type = self._analyze_content_patterns(content_lower)
        
        # Update statistics
        if detected_type in self.question_stats["type_counts"]:
            self.question_stats["type_counts"][detected_type] += 1
        else:
            self.question_stats["type_counts"][detected_type] = 1
        
        # Add to history
        self.question_stats["detection_history"].append({
            "type": detected_type,
            "content_sample": page_content[:100] + "..." if len(page_content) > 100 else page_content
        })
        
        # Keep only last 50 detections
        if len(self.question_stats["detection_history"]) > 50:
            self.question_stats["detection_history"] = self.question_stats["detection_history"][-50:]
        
        return detected_type
    
    def _analyze_content_patterns(self, content_lower: str) -> str:
        """
        Analyze content patterns to determine question type.
        """
        # Check for image-based questions
        if ("click this image" in content_lower or 
            "logo" in content_lower or 
            "click here" in content_lower and "image" in content_lower):
            return "image_selection"
        
        # Check for research-requiring questions
        elif any(indicator in content_lower for indicator in [
            "ilia topuria", "documentary", "stadium", "venue", "sponsor",
            "team sponsor", "major sponsor", "what is the name of", 
            "canberra raiders", "gio stadium"
        ]):
            return "research_required"
        
        # Check for price sensitivity questions
        elif any(keyword in content_lower for keyword in [
            "wouldn't buy/use it", "average price", "significantly more expensive",
            "close to the average price", "price for this sort of product"
        ]):
            return "price_sensitivity"
        
        # Check for brand personality questions
        elif any(keyword in content_lower for keyword in [
            "courageous", "big personality", "global", "iconic", "challenging",
            "exciting and involving", "trendy", "trusted"
        ]):
            return "brand_personality"
        
        # Check for purchase intent questions
        elif any(keyword in content_lower for keyword in [
            "would buy", "willing to pay", "purchase intent", "buy/use", "next week", "next month"
        ]):
            return "purchase_intent"
        
        # Check for brand familiarity scales
        elif any(keyword in content_lower for keyword in [
            "familiar with this brand", "currently use", "aware of this brand", 
            "never heard", "have used their products", "don't know what they do",
            "how familiar are you with", "familiar are you with the following"
        ]):
            return "brand_familiarity"
        
        # Check for trust/rating matrices
        elif any(keyword in content_lower for keyword in [
            "trustworthy", "trust", "rate", "very trustworthy"
        ]):
            return "trust_rating"
        
        # Check for consideration matrices
        elif any(keyword in content_lower for keyword in [
            "would seriously consider", "might consider", "would not consider",
            "never heard of them", "don't know enough about them"
        ]):
            return "consideration_matrix"
        
        # Check for sentiment scales
        elif any(keyword in content_lower for keyword in [
            "very positive", "positive", "neutral", "negative", "very negative"
        ]):
            return "sentiment_rating"
        
        # Check for massive rating matrices
        elif sum(1 for keyword in ["strongly agree", "somewhat agree", "neither agree", "disagree"] 
                if keyword in content_lower) >= 3:
            return "rating_matrix"
        
        # Check for interest level matrices
        elif any(keyword in content_lower for keyword in [
            "not interested at all", "very interested", "1not interested", "5very interested"
        ]):
            return "interest_matrix"
        
        # Check for frequency matrices
        elif sum(1 for keyword in ["daily", "weekly", "monthly", "quarterly", "never", "regularly", "sometimes"] 
                if keyword in content_lower) >= 4:
            return "frequency_matrix"
        
        # Check for team/event knowledge questions
        elif any(keyword in content_lower for keyword in [
            "event known", "event not known", "team known", "team not known",
            "event/team known", "event/team not known"
        ]):
            return "knowledge_matrix"
        
        # Check for sports team preferences
        elif any(keyword in content_lower for keyword in [
            "favourite team", "don't know", "no favourite team", 
            "do not follow any", "which is your favorite"
        ]):
            return "team_preference"
        
        # Check for recency/activity questions
        elif any(keyword in content_lower for keyword in [
            "in the last 12 months", "in the past year", "in the last year",
            "things you have done", "activities you have done", "select from the list those things"
        ]):
            return "recency_activities"
        
        # Check for multi-select questions
        elif any(keyword in content_lower for keyword in [
            "select all", "check all", "choose all", "multiple"
        ]):
            return "multi_select"
        
        # Check for brand naming questions
        elif any(keyword in content_lower for keyword in [
            "name", "list", "can you name", "which brands", "what brands", 
            "name some", "name any", "list some", "list any"
        ]):
            return "brand_naming"
        
        # Check for demographics
        elif any(keyword in content_lower for keyword in [
            "age", "gender", "location", "income", "employment", "education", "household"
        ]):
            return "demographics"
        
        else:
            return "unknown"
    
    def get_question_stats(self) -> dict:
        """Get question detection statistics."""
        return self.question_stats.copy()
    
    def get_most_common_types(self, limit: int = 5) -> list:
        """Get most common question types detected."""
        type_counts = self.question_stats["type_counts"]
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_types[:limit]
    
    def reset_stats(self):
        """Reset detection statistics."""
        self.question_stats = {
            "questions_processed": 0,
            "type_counts": {},
            "detection_history": []
        }
    
    def print_detection_summary(self):
        """Print detection statistics summary."""
        stats = self.question_stats
        
        if stats["questions_processed"] == 0:
            print("📊 No questions processed yet")
            return
        
        print(f"\n🔍 QUESTION TYPE DETECTION SUMMARY:")
        print(f"   Total questions processed: {stats['questions_processed']}")
        
        if stats["type_counts"]:
            print(f"   Question types detected:")
            for question_type, count in sorted(stats["type_counts"].items(), 
                                             key=lambda x: x[1], reverse=True):
                percentage = (count / stats["questions_processed"]) * 100
                print(f"   • {question_type}: {count} times ({percentage:.1f}%)")
