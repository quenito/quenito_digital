#!/usr/bin/env python3
"""
🧠 QUENITO: Intelligent Learning System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A proper learning architecture that knows what to learn and when to use it
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import json
import os
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path


class IntelligentLearningSystem:
    """
    Manages the complete learning loop for Quenito
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
        
        # Load all knowledge stores
        self.knowledge_base = self._load_json(self.knowledge_base_path, self._get_default_knowledge())
        self.learned_responses = self._load_json(self.learned_responses_path, {})
        self.learned_patterns = self._load_json(self.learned_patterns_path, self._get_default_patterns())
        
        # Session tracking
        self.current_session = {
            "timestamp": datetime.now().isoformat(),
            "automated": [],
            "manual": [],
            "failed": []
        }
        
        print(f"🧠 Intelligent Learning System initialized")
        print(f"   📚 Knowledge base: Core identity loaded")
        print(f"   💡 Learned responses: {len(self.learned_responses)} exact Q&As")
        print(f"   🎯 Learned patterns: {len(self.learned_patterns)} patterns")
    
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
    
    def _get_default_knowledge(self) -> Dict:
        """Matt's core identity - NEVER changes"""
        return {
            "identity": {
                "name": "Matt",
                "age": 45,
                "birth_year": 1980,
                "birth_month": "March",
                "gender": "Male"
            },
            "location": {
                "city": "Sydney",
                "state": "NSW",
                "postcode": "2217",
                "country": "Australia"
            },
            "family": {
                "marital_status": "Married",
                "children": True,
                "children_count": 2,
                "children_ages": [3, 6],
                "children_genders": ["Female", "Female"],
                "household_size": 4
            },
            "work": {
                "employment_status": "Full-time",
                "industry": "Retail",
                "company": "Woolworths",
                "position": "Data Analyst",
                "income_personal": "$100,000-$149,999",
                "income_household": "$200,000-$499,999"
            },
            "preferences": {
                "brands": {
                    "supermarkets": ["Woolworths", "Coles", "Aldi"],
                    "banks": ["Commonwealth Bank", "Westpac"],
                    "insurance": ["Medibank Private"],
                    "airlines": ["Qantas", "Virgin"],
                    "tech": ["Apple", "Samsung", "Google"]
                },
                "shopping": {
                    "frequency": "Weekly",
                    "online_shopping": True,
                    "preferred_time": "Evening"
                },
                "media": {
                    "news": ["ABC News", "Sydney Morning Herald"],
                    "streaming": ["Netflix", "Disney+"],
                    "social": ["Facebook", "LinkedIn"]
                }
            }
        }
    
    def _get_default_patterns(self) -> Dict:
        """Default question patterns"""
        return {
            "gender": {
                "patterns": [
                    "are you male or female",
                    "what is your gender",
                    "please indicate your gender",
                    "gender identity"
                ],
                "response": "Male",
                "confidence": 1.0
            },
            "industry_screening": {
                "patterns": [
                    "work in any of the following industries",
                    "employed in any of these",
                    "household work in",
                    "family members work"
                ],
                "response_logic": "if_retail_exists_select_else_none_of_above",
                "confidence": 0.95
            },
            "children": {
                "patterns": [
                    "children aged under 18",
                    "children living in your household",
                    "do you have any children",
                    "kids at home"
                ],
                "response": "Yes",
                "confidence": 1.0
            },
            "age_range": {
                "patterns": [
                    "which age group",
                    "age range",
                    "how old are you"
                ],
                "response_logic": "select_range_containing_45",
                "confidence": 1.0
            }
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
            return {
                "success": True,
                "value": exact_match["answer"],
                "confidence": 0.99,
                "source": "exact_match"
            }
        
        # Step 2: Check pattern match (high confidence)
        pattern_match = self._check_pattern_match(question, element_type, options)
        if pattern_match:
            print(f"   🎯 PATTERN MATCH: {pattern_match['answer']}")
            return {
                "success": True,
                "value": pattern_match["answer"],
                "confidence": 0.95,
                "source": "pattern_match"
            }
        
        # Step 3: Use LLM with knowledge base context
        # (This would call the existing LLM service)
        return None  # Let LLM service handle it
    
    def _check_exact_match(self, question: str, element_type: str) -> Optional[Dict]:
        """Check for exact question match"""
        q_normalized = question.lower().strip()
        
        # Must be a substantial question (not "..." or empty)
        if len(q_normalized) < 20:
            return None
        
        # Check learned responses
        if q_normalized in self.learned_responses:
            learned = self.learned_responses[q_normalized]
            
            # Validate element type matches
            if learned.get("element_type") == element_type:
                # Check confidence and usage count
                if learned.get("confidence", 0) >= 0.9 and learned.get("success_count", 0) >= 1:
                    return {
                        "answer": learned["answer"],
                        "confidence": learned.get("confidence", 0.95)
                    }
        
        return None
    
    def _check_pattern_match(self, question: str, element_type: str, 
                            options: Optional[List[str]] = None) -> Optional[Dict]:
        """Check for pattern-based match"""
        q_lower = question.lower()
        
        # Check each pattern category
        for category, pattern_data in self.learned_patterns.items():
            patterns = pattern_data.get("patterns", [])
            
            # Check if question matches any pattern
            for pattern in patterns:
                if pattern in q_lower:
                    # Special logic for some patterns
                    if pattern_data.get("response_logic") == "if_retail_exists_select_else_none_of_above":
                        # Industry screening logic
                        if options:
                            if any("retail" in opt.lower() for opt in options):
                                return {"answer": "Retail", "confidence": 0.95}
                            elif any("none" in opt.lower() for opt in options):
                                return {"answer": "None of the above", "confidence": 0.95}
                    
                    elif pattern_data.get("response_logic") == "select_range_containing_45":
                        # Age range logic
                        if options:
                            for opt in options:
                                # Check if 45 is in this range
                                import re
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
        
        # Update learned responses (only high confidence)
        if confidence >= 0.85:
            q_normalized = question.lower().strip()
            
            if q_normalized in self.learned_responses:
                # Update existing
                self.learned_responses[q_normalized]["success_count"] += 1
                self.learned_responses[q_normalized]["last_used"] = datetime.now().isoformat()
                # Boost confidence slightly with each success
                self.learned_responses[q_normalized]["confidence"] = min(
                    self.learned_responses[q_normalized].get("confidence", 0.9) + 0.01,
                    0.99
                )
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
            
            # Save immediately
            self._save_json(self.learned_responses_path, self.learned_responses)
            print(f"   💾 Learned: {question[:40]}... → {answer}")
    
    # ========== LEARNING FROM MANUAL ==========
    
    def record_manual_intervention(self,
                                  question: str,
                                  answer: Any,
                                  element_type: str):
        """Record manual intervention for review and learning"""
        
        # Add to session
        self.current_session["manual"].append({
            "question": question,
            "answer": answer,
            "element_type": element_type,
            "timestamp": datetime.now().isoformat()
        })
        
        # Manual interventions go to session file for review
        # They are NOT automatically trusted
        print(f"   📝 Manual intervention recorded for review")
    
    # ========== SESSION MANAGEMENT ==========
    
    def save_session(self):
        """Save current session for analysis"""
        session_file = self.session_path / f"session_{int(datetime.now().timestamp())}.json"
        self._save_json(session_file, self.current_session)
        
        # Analyze session for patterns
        self._analyze_session_for_patterns()
        
        print(f"   💾 Session saved: {len(self.current_session['automated'])} automated, "
              f"{len(self.current_session['manual'])} manual")
    
    def _analyze_session_for_patterns(self):
        """Analyze session to identify new patterns"""
        
        # Look for repeated manual interventions (might be a pattern)
        manual_answers = {}
        for item in self.current_session["manual"]:
            answer = item["answer"]
            if answer in manual_answers:
                manual_answers[answer] += 1
            else:
                manual_answers[answer] = 1
        
        # If same answer given 3+ times manually, it might be a preference
        for answer, count in manual_answers.items():
            if count >= 3:
                print(f"   🔍 Pattern detected: '{answer}' used {count} times manually")
                # Could add to learned patterns after review
    
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
            
            # Skip if success rate is too low
            if data.get("success_count", 0) < 1:
                removed.append(question)
                continue
            
            # Skip "Male" for non-gender questions
            if data.get("answer") == "Male" and "gender" not in question and "sex" not in question:
                removed.append(question)
                continue
            
            # Keep good ones
            cleaned[question] = data
        
        if removed:
            print(f"   🧹 Cleaned {len(removed)} problematic entries")
            self.learned_responses = cleaned
            self._save_json(self.learned_responses_path, self.learned_responses)
    
    # ========== STATISTICS ==========
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learning"""
        return {
            "knowledge_base": {
                "categories": len(self.knowledge_base),
                "last_updated": self.knowledge_base.get("last_updated", "unknown")
            },
            "learned_responses": {
                "total": len(self.learned_responses),
                "high_confidence": sum(1 for r in self.learned_responses.values() 
                                     if r.get("confidence", 0) >= 0.95),
                "frequently_used": sum(1 for r in self.learned_responses.values() 
                                     if r.get("success_count", 0) >= 5)
            },
            "patterns": {
                "total": len(self.learned_patterns),
                "categories": list(self.learned_patterns.keys())
            },
            "current_session": {
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


# ========== STANDALONE UTILITIES ==========

def migrate_existing_learning():
    """
    Migrate existing learning files to new structure
    """
    print("🔄 Migrating existing learning data...")
    
    persona_path = Path("personas/quenito")
    
    # Clean up knowledge_base.json (remove individual Q&As)
    kb_path = persona_path / "knowledge_base.json"
    if kb_path.exists():
        with open(kb_path, 'r') as f:
            kb = json.load(f)
        
        # Remove learning_* entries
        cleaned_kb = {}
        for key, value in kb.items():
            if not key.startswith("learning_"):
                cleaned_kb[key] = value
        
        # Backup original
        import shutil
        shutil.copy(kb_path, kb_path.with_suffix('.backup.json'))
        
        # Save cleaned version
        with open(kb_path, 'w') as f:
            json.dump(cleaned_kb, f, indent=2)
        
        print(f"   ✅ Cleaned knowledge_base.json")
    
    # Clean learned_responses.json
    lr_path = persona_path / "learned_responses.json"
    if lr_path.exists():
        learning = IntelligentLearningSystem()
        learning.cleanup_learned_responses()
        print(f"   ✅ Cleaned learned_responses.json")
    
    print("✅ Migration complete!")


if __name__ == "__main__":
    # Run migration when executed directly
    migrate_existing_learning()
    
    # Show stats
    learning = IntelligentLearningSystem()
    stats = learning.get_learning_stats()
    print("\n📊 Learning System Status:")
    print(json.dumps(stats, indent=2))