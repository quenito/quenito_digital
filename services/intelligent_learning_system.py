#!/usr/bin/env python3
"""
🧠 QUENITO: Intelligent Learning System (FIXED VERSION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fixed to work with proper file structures and save manual interventions correctly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import json
import os
import re
import shutil
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path


class IntelligentLearningSystem:
    """
    Manages the complete learning loop for Quenito
    FIXED: Works with wrapped structures and saves manual interventions to sessions
    """
    
    def __init__(self, persona_name: str = "quenito"):
        self.persona_name = persona_name
        self.base_path = Path(f"personas/{persona_name}")
        
        # Core knowledge files
        self.knowledge_base_path = self.base_path / "knowledge_base.json"
        self.learned_responses_path = self.base_path / "learned_responses.json"
        self.learned_patterns_path = self.base_path / "learned_patterns.json"
        self.session_path = self.base_path / "sessions"
        
        # Create directories
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(exist_ok=True)
        
        # Load all knowledge stores WITH PROPER STRUCTURE
        self.knowledge_base = self._load_json(self.knowledge_base_path, self._get_default_knowledge())
        
        # Load learned responses WITH wrapper structure
        lr_data = self._load_json(self.learned_responses_path, {"responses": {}, "metadata": {}})
        self.learned_responses = lr_data.get("responses", {})
        
        # Load learned patterns WITH wrapper structure
        lp_data = self._load_json(self.learned_patterns_path, {"patterns": self._get_default_patterns(), "metadata": {}})
        self.learned_patterns = lp_data.get("patterns", self._get_default_patterns())
        
        # Session tracking
        self.current_session = {
            "session_id": f"session_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "automated": [],
            "manual": [],
            "failed": []
        }
        
        print(f"🧠 Intelligent Learning System initialized")
        print(f"   📚 Knowledge base: Core identity loaded")
        print(f"   💡 Learned responses: {len(self.learned_responses)} exact Q&As")
        print(f"   🎯 Learned patterns: {len(self.learned_patterns)} pattern categories")
        print(f"   📁 Sessions directory: {self.session_path}")
    
    def _load_json(self, path: Path, default: Dict) -> Dict:
        """Load JSON file or return default"""
        if path.exists():
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, path: Path, data: Dict):
        """Save JSON file"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_learned_responses(self):
        """Save learned responses with proper wrapper structure"""
        data = {
            "responses": self.learned_responses,
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_responses": len(self.learned_responses),
                "version": "1.0"
            }
        }
        self._save_json(self.learned_responses_path, data)
    
    def _save_learned_patterns(self):
        """Save learned patterns with proper wrapper structure"""
        data = {
            "patterns": self.learned_patterns,
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_patterns": sum(len(v) if isinstance(v, list) else 1 for v in self.learned_patterns.values()),
                "version": "1.0"
            }
        }
        self._save_json(self.learned_patterns_path, data)
    
    def _get_default_knowledge(self) -> Dict:
        """Matt's core identity with PROPER STRUCTURE"""
        return {
            "personal": {
                "name": "Matt",
                "full_name": "Matt",
                "nickname": "Quenito"
            },
            "demographics": {
                "age": 45,
                "birth_year": 1980,
                "birth_month": "March",
                "gender": "Male",
                "marital_status": "Married",
                "children": True,
                "children_count": 2,
                "children_ages": [3, 6],
                "children_genders": ["Female", "Female"],
                "household_size": 4,
                "city": "Sydney",
                "state": "NSW",
                "postcode": "2217",
                "country": "Australia",
                "employment_status": "Full-time",
                "industry": "Retail",
                "company": "Woolworths",
                "position": "Data Analyst",
                "income_personal": "$100,000-$149,999",
                "income_household": "$200,000-$499,999"
            },
            "preferences": {
                "supermarkets": ["Woolworths", "Coles", "Aldi"],
                "banks": ["Commonwealth Bank", "Westpac"],
                "insurance": ["Medibank Private"],
                "airlines": ["Qantas", "Virgin"],
                "tech": ["Apple", "Samsung", "Google"],
                "shopping_frequency": "Weekly",
                "online_shopping": True,
                "news": ["ABC News", "Sydney Morning Herald"],
                "streaming": ["Netflix", "Disney+"],
                "social_media": ["Facebook", "LinkedIn"]
            },
            "behavior": {
                "survey_style": "thoughtful",
                "response_pattern": "consistent"
            },
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "persona": "quenito"
            },
            "learning_stats": {
                "total_responses_learned": 0,
                "total_patterns_identified": 0,
                "last_learning_session": None
            }
        }
    
    def _get_default_patterns(self) -> Dict:
        """Default question patterns as LISTS"""
        return {
            "gender": [{
                "patterns": [
                    "are you male or female",
                    "what is your gender",
                    "please indicate your gender",
                    "gender identity",
                    "please select your gender",
                    "i am"
                ],
                "response": "Male",
                "confidence": 1.0
            }],
            "industry_screening": [{
                "patterns": [
                    "work in any of the following industries",
                    "employed in any of these",
                    "household work in",
                    "family members work",
                    "work for any of the following"
                ],
                "response_logic": "if_retail_exists_select_else_none_of_above",
                "confidence": 0.95
            }],
            "children": [{
                "patterns": [
                    "children aged under 18",
                    "children living in your household",
                    "do you have any children",
                    "kids at home",
                    "children under 18"
                ],
                "response": "Yes",
                "confidence": 1.0
            }],
            "age": [{
                "patterns": [
                    "which age group",
                    "age range",
                    "how old are you",
                    "please select your age",
                    "what is your age"
                ],
                "response_logic": "select_range_containing_45",
                "confidence": 1.0
            }],
            "location": [{
                "patterns": [
                    "where do you live",
                    "current location",
                    "which state",
                    "postcode"
                ],
                "response_logic": "sydney_nsw_2217",
                "confidence": 1.0
            }],
            "brand_awareness": []  # Empty list for future patterns
        }
    
    # ========== DECISION FLOW ==========
    
    async def get_response_for_question(self, 
                                       question: str, 
                                       element_type: str,
                                       options: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Main decision flow for answering questions
        Priority: Exact match → Pattern match → LLM → Learn from manual
        """
        
        # Step 1: Check exact match (highest confidence)
        exact_match = self._check_exact_match(question, element_type)
        if exact_match:
            print(f"   💡 EXACT MATCH: {exact_match['answer']}")
            
            # Increment success count and boost confidence
            q_normalized = question.lower().strip()
            if q_normalized in self.learned_responses:
                response_data = self.learned_responses[q_normalized]
                if isinstance(response_data, dict):
                    response_data["success_count"] = response_data.get("success_count", 0) + 1
                    response_data["last_used"] = datetime.now().isoformat()
                    
                    # Boost confidence with each successful use (up to 0.99)
                    current_confidence = response_data.get("confidence", 0.85)
                    response_data["confidence"] = min(current_confidence + 0.02, 0.99)
                    
                    # Save immediately WITH WRAPPER
                    self._save_learned_responses()
            
            return {
                "success": True,
                "value": exact_match["answer"],
                "confidence": exact_match.get("confidence", 0.95),
                "source": "exact_match"
            }
        
        # Step 2: Check pattern match (high confidence)
        pattern_match = self._check_pattern_match(question, element_type, options)
        if pattern_match:
            print(f"   🎯 PATTERN MATCH: {pattern_match['answer']}")
            return {
                "success": True,
                "value": pattern_match["answer"],
                "confidence": pattern_match.get("confidence", 0.95),
                "source": "pattern_match"
            }
        
        # Step 3: No match found - let LLM handle it
        return None
    
    def _check_exact_match(self, question: str, element_type: str) -> Optional[Dict]:
        """Check for exact question match"""
        q_normalized = question.lower().strip()
        
        # Must be a substantial question
        if len(q_normalized) < 20:
            return None
        
        # Check learned responses
        if q_normalized in self.learned_responses:
            learned = self.learned_responses[q_normalized]
            
            # Handle both dict and string responses
            if isinstance(learned, dict):
                # Check element type compatibility
                type_matches = (
                    learned.get("element_type") == element_type or
                    learned.get("element_type") == "unknown" or
                    element_type == "unknown"
                )
                
                if type_matches and learned.get("confidence", 0) >= 0.80:
                    return {
                        "answer": learned.get("answer", learned.get("value", "")),
                        "confidence": learned.get("confidence", 0.85)
                    }
            elif isinstance(learned, str):
                # Simple string response (legacy format)
                return {
                    "answer": learned,
                    "confidence": 0.85
                }
        
        return None
    
    def _check_pattern_match(self, question: str, element_type: str, 
                            options: Optional[List[str]] = None) -> Optional[Dict]:
        """Check for pattern-based match"""
        q_lower = question.lower()
        
        # Check each pattern category
        for category, pattern_list in self.learned_patterns.items():
            if not isinstance(pattern_list, list):
                continue
                
            for pattern_data in pattern_list:
                if not isinstance(pattern_data, dict):
                    continue
                    
                patterns = pattern_data.get("patterns", [])
                
                # Check if question matches any pattern
                for pattern in patterns:
                    if pattern in q_lower:
                        # Special logic for some patterns
                        if pattern_data.get("response_logic") == "if_retail_exists_select_else_none_of_above":
                            if options:
                                if any("retail" in opt.lower() for opt in options):
                                    return {"answer": "Retail", "confidence": 0.95}
                                elif any("none" in opt.lower() for opt in options):
                                    return {"answer": "None of the above", "confidence": 0.95}
                        
                        elif pattern_data.get("response_logic") == "select_range_containing_45":
                            if options:
                                for opt in options:
                                    numbers = re.findall(r'\d+', opt)
                                    if len(numbers) >= 2:
                                        try:
                                            if int(numbers[0]) <= 45 <= int(numbers[1]):
                                                return {"answer": opt, "confidence": 0.95}
                                        except:
                                            pass
                        
                        else:
                            # Direct response
                            if "response" in pattern_data:
                                return {
                                    "answer": pattern_data["response"],
                                    "confidence": pattern_data.get("confidence", 0.9)
                                }
        
        return None
    
    # ========== LEARNING FROM SUCCESS ==========
    
    def record_successful_automation(self, 
                                    question: str, 
                                    answer: str,
                                    element_type: str,
                                    confidence: float):
        """Record a successful automation for learning"""
        
        # Add to session
        self.current_session["automated"].append({
            "question": question,
            "answer": answer,
            "element_type": element_type,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        
        # Don't learn from trivial questions
        if len(question) < 20 or question.strip() == "...":
            return
        
        # Don't learn "Male" for non-gender questions
        if answer == "Male" and "gender" not in question.lower() and "sex" not in question.lower():
            print(f"   ⚠️ Skipping learning 'Male' for non-gender question")
            return
        
        # Update learned responses
        if confidence >= 0.80:
            q_normalized = question.lower().strip()
            
            if q_normalized in self.learned_responses:
                # Update existing
                response_data = self.learned_responses[q_normalized]
                if isinstance(response_data, dict):
                    response_data["success_count"] = response_data.get("success_count", 0) + 1
                    response_data["last_used"] = datetime.now().isoformat()
                    response_data["confidence"] = max(response_data.get("confidence", 0.85), confidence)
            else:
                # Add new
                self.learned_responses[q_normalized] = {
                    "answer": answer,
                    "element_type": element_type,
                    "confidence": confidence,
                    "success_count": 1,
                    "first_seen": datetime.now().isoformat(),
                    "last_used": datetime.now().isoformat()
                }
            
            # Save immediately WITH WRAPPER
            self._save_learned_responses()
            print(f"   💾 Learned: {question[:40]}... → {answer}")
            
            # Update learning stats in knowledge base
            if "learning_stats" in self.knowledge_base:
                self.knowledge_base["learning_stats"]["total_responses_learned"] = len(self.learned_responses)
                self.knowledge_base["learning_stats"]["last_learning_session"] = datetime.now().isoformat()
                self._save_json(self.knowledge_base_path, self.knowledge_base)
    
    # ========== LEARNING FROM MANUAL ==========
    
    def record_manual_intervention(self,
                                  question: str,
                                  answer: Any,
                                  element_type: str):
        """Record manual intervention to SESSION FILE, not knowledge base"""
        
        # Add to current session
        self.current_session["manual"].append({
            "question": question,
            "answer": answer,
            "element_type": element_type,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save session immediately to prevent loss
        self._save_current_session()
        
        print(f"   📝 Manual intervention saved to session file")
    
    def _save_current_session(self):
        """Save current session to file"""
        session_file = self.session_path / f"{self.current_session['session_id']}.json"
        self._save_json(session_file, self.current_session)
    
    # ========== SESSION MANAGEMENT ==========
    
    def save_session(self):
        """Save and finalize current session"""
        # Save final session state
        self._save_current_session()
        
        # Analyze session for patterns
        self._analyze_session_for_patterns()
        
        print(f"   💾 Session finalized: {len(self.current_session['automated'])} automated, "
              f"{len(self.current_session['manual'])} manual")
        
        # Reset session for next survey
        self.current_session = {
            "session_id": f"session_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "automated": [],
            "manual": [],
            "failed": []
        }
    
    def _analyze_session_for_patterns(self):
        """Analyze session to identify new patterns"""
        
        # Look for repeated manual interventions
        manual_answers = {}
        for item in self.current_session["manual"]:
            answer = item["answer"]
            if answer in manual_answers:
                manual_answers[answer] += 1
            else:
                manual_answers[answer] = 1
        
        # If same answer given 3+ times manually, it might be a pattern
        for answer, count in manual_answers.items():
            if count >= 3:
                print(f"   🔍 Pattern detected: '{answer}' used {count} times manually")
                # This could be reviewed and added to patterns later
    
    # ========== CLEANUP ==========
    
    def cleanup_learned_responses(self):
        """Remove problematic learned responses"""
        
        cleaned = {}
        removed = []
        
        for question, data in self.learned_responses.items():
            # Skip overly short questions
            if len(question) < 20:
                removed.append(question)
                continue
            
            # Handle both dict and string responses
            if isinstance(data, dict):
                # Skip if success rate is too low
                if data.get("success_count", 0) < 1:
                    removed.append(question)
                    continue
                
                # Skip "Male" for non-gender questions
                answer = data.get("answer", data.get("value", ""))
                if answer == "Male" and "gender" not in question and "sex" not in question:
                    removed.append(question)
                    continue
            
            # Keep good ones
            cleaned[question] = data
        
        if removed:
            print(f"   🧹 Cleaned {len(removed)} problematic entries")
            self.learned_responses = cleaned
            self._save_learned_responses()
    
    # ========== STATISTICS ==========
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learning"""
        return {
            "knowledge_base": {
                "categories": len(self.knowledge_base),
                "last_updated": self.knowledge_base.get("metadata", {}).get("last_updated", "unknown")
            },
            "learned_responses": {
                "total": len(self.learned_responses),
                "high_confidence": sum(1 for r in self.learned_responses.values() 
                                     if isinstance(r, dict) and r.get("confidence", 0) >= 0.95),
                "frequently_used": sum(1 for r in self.learned_responses.values() 
                                     if isinstance(r, dict) and r.get("success_count", 0) >= 5)
            },
            "patterns": {
                "total": sum(len(v) if isinstance(v, list) else 1 for v in self.learned_patterns.values()),
                "categories": list(self.learned_patterns.keys())
            },
            "current_session": {
                "id": self.current_session["session_id"],
                "automated": len(self.current_session["automated"]),
                "manual": len(self.current_session["manual"]),
                "failed": len(self.current_session["failed"])
            }
        }


# ========== INTEGRATION WITH LLM SERVICE ==========

class LLMServiceWithIntelligentLearning:
    """
    How to integrate this with your existing LLM service
    """
    
    def __init__(self):
        # ... existing init ...
        
        # Initialize intelligent learning
        self.learning = IntelligentLearningSystem()
        
    async def get_response(self, question: str, options: Optional[List[str]] = None,
                          element_type: str = "unknown") -> Dict[str, Any]:
        """
        Enhanced get_response with intelligent learning
        """
        
        # Step 1: Check learning system first
        learned_response = await self.learning.get_response_for_question(
            question, element_type, options
        )
        
        if learned_response:
            return learned_response
        
        # Step 2: Use LLM
        llm_response = await self._call_llm(question, options, element_type)
        
        # Step 3: If successful, record for learning
        if llm_response.get("success"):
            self.learning.record_successful_automation(
                question,
                llm_response["value"],
                element_type,
                llm_response.get("confidence", 0.85)
            )
        
        return llm_response


if __name__ == "__main__":
    # Test the system
    learning = IntelligentLearningSystem()
    stats = learning.get_learning_stats()
    print("\n📊 Learning System Status:")
    print(json.dumps(stats, indent=2))