"""
Research Required Handler Module
Handles questions requiring research questions.
"""

from .base_handler import BaseQuestionHandler

class ResearchRequiredHandler(BaseQuestionHandler):
    """Handler for questions requiring research"""
    
    def can_handle(self, page_content: str) -> bool:
        """Check if this question requires research"""
        content_lower = page_content.lower()
        
        research_indicators = [
            "sponsor", "venue", "location", "stadium", "documentary",
            "which company sponsors", "where is", "what is the name of",
            "who sponsors", "main sponsor", "official sponsor",
            "what stadium", "which venue", "where does", "home ground",
            "which documentary", "what documentary", "film about"
        ]
        
        # Also check for patterns that suggest research is needed
        research_question_patterns = [
            "which company",
            "what is the",
            "where is the",
            "who is the",
            "name of the",
            "which brand",
            "official"
        ]
        
        has_research_indicator = any(indicator in content_lower for indicator in research_indicators)
        has_question_pattern = any(pattern in content_lower for pattern in research_question_patterns)
        
        return has_research_indicator or has_question_pattern
    
    def handle(self) -> bool:
        """Handle research-required questions"""
        print("🔍 Handling research-required question")
        
        page_content = self.page.inner_text('body')
        content_lower = page_content.lower()
        
        # For Phase 1 implementation, prioritize manual intervention for research questions
        # This ensures accuracy and provides data for future automation enhancement
        
        research_reason = self.categorize_research_type(content_lower)
        print(f"🎯 Research type detected: {research_reason}")
        print("🔄 Prioritizing manual intervention for accuracy and learning")
        
        # Log this as a research opportunity for future enhancement
        self.log_research_opportunity(page_content, research_reason)
        
        # Return False to trigger manual intervention
        return False
    
    def categorize_research_type(self, content_lower):
        """Categorize the type of research needed"""
        
        if any(word in content_lower for word in ["sponsor", "sponsors", "sponsorship"]):
            return "Brand/Company Sponsorship Research"
        elif any(word in content_lower for word in ["stadium", "venue", "ground", "arena"]):
            return "Sports Venue/Location Research"
        elif any(word in content_lower for word in ["documentary", "film", "movie"]):
            return "Media/Entertainment Research"
        elif any(word in content_lower for word in ["location", "where is", "city", "state"]):
            return "Geographic Location Research"
        elif any(word in content_lower for word in ["company", "brand", "business"]):
            return "Company/Brand Information Research"
        else:
            return "General Knowledge Research"
    
    def log_research_opportunity(self, page_content, research_type):
        """Log research opportunity for future automation enhancement"""
        
        try:
            # Extract key information for future research automation
            research_data = {
                "research_type": research_type,
                "page_content_sample": page_content[:200],
                "timestamp": "current_session",
                "potential_search_terms": self.extract_search_terms(page_content),
                "automation_potential": "high" if research_type in [
                    "Brand/Company Sponsorship Research",
                    "Sports Venue/Location Research"
                ] else "medium"
            }
            
            # This could be stored in knowledge base for future enhancement
            print(f"📊 Research opportunity logged: {research_type}")
            
            # Print potential search terms for manual reference
            if research_data["potential_search_terms"]:
                print(f"🔍 Suggested search terms: {', '.join(research_data['potential_search_terms'])}")
            
        except Exception as e:
            print(f"Warning: Could not log research opportunity: {e}")
    
    def extract_search_terms(self, page_content):
        """Extract potential search terms from the question content"""
        
        search_terms = []
        content_lower = page_content.lower()
        
        try:
            # Look for quoted text or specific names
            import re
            
            # Extract quoted strings
            quoted_matches = re.findall(r'"([^"]*)"', page_content)
            search_terms.extend(quoted_matches)
            
            # Extract proper nouns (capitalized words)
            proper_noun_matches = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', page_content)
            search_terms.extend(proper_noun_matches)
            
            # Extract specific research patterns
            if "sponsor" in content_lower:
                sponsor_matches = re.findall(r'(?:sponsor(?:s|ship)?(?:\s+of)?)\s+([A-Za-z\s]+)', page_content, re.IGNORECASE)
                search_terms.extend([match.strip() for match in sponsor_matches])
            
            if any(word in content_lower for word in ["stadium", "venue", "ground"]):
                venue_matches = re.findall(r'(?:stadium|venue|ground|arena)\s+(?:of|for)?\s*([A-Za-z\s]+)', page_content, re.IGNORECASE)
                search_terms.extend([match.strip() for match in venue_matches])
            
            # Clean up search terms
            cleaned_terms = []
            for term in search_terms:
                term = term.strip()
                if len(term) > 2 and term not in cleaned_terms:
                    cleaned_terms.append(term)
            
            return cleaned_terms[:5]  # Return top 5 most relevant terms
            
        except Exception as e:
            print(f"Warning: Could not extract search terms: {e}")
            return []
    
    def future_research_automation_placeholder(self, page_content):
        """
        Placeholder for future research automation capabilities
        
        This method outlines how research automation could work in future versions:
        1. Extract search terms from question
        2. Perform web search using research engine
        3. Parse results for relevant answers
        4. Match answers to available options on page
        5. Select most appropriate option
        
        For now, this returns False to trigger manual intervention.
        """
        
        # Future implementation would include:
        # - Integration with research_engine.py
        # - Intelligent search query construction
        # - Result parsing and option matching
        # - Confidence scoring for automated selections
        
        return False  # Always return False for Phase 1 implementation
