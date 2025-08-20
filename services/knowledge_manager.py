#!/usr/bin/env python3
"""
🧠 QUENITO: Building a Digital Brain, Not Mechanical Parts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We're teaching Quenito to UNDERSTAND surveys, not just fill them.
Every decision should make him smarter, not just more mechanical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Knowledge Manager - The NEW brain manager (LLM-first architecture)
Singleton pattern ensuring ONE consistent memory across all services.
Manages personas/quenito/knowledge_base.json - Quenito's actual memories.
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

class KnowledgeManager:
    """Centralized manager for all persona knowledge"""
    
    _instance = None
    _knowledge_base = None
    
    def __new__(cls, persona_name: str = "quenito"):
        """Singleton pattern to ensure one instance per persona"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, persona_name: str = "quenito"):
        """Initialize knowledge manager"""
        
        if self._knowledge_base is None:  # Only load once
            self.persona_name = persona_name
            self.kb_path = Path(f"personas/{persona_name}/knowledge_base.json")
            self.kb_path.parent.mkdir(parents=True, exist_ok=True)
            self._knowledge_base = self.load()
            print(f"🧠 Knowledge Manager initialized for {persona_name}")
    
    def load(self) -> Dict:
        """Load knowledge base from file"""
        
        if self.kb_path.exists():
            try:
                with open(self.kb_path, 'r') as f:
                    data = json.load(f)
                    print(f"✅ Loaded knowledge base from {self.kb_path}")
                    return data
            except Exception as e:
                print(f"❌ Error loading knowledge base: {e}")
        
        print(f"📝 Creating new knowledge base for {self.persona_name}")
        return self.create_default()
    
    def save(self):
        """Save knowledge base to file"""
        
        try:
            with open(self.kb_path, 'w') as f:
                json.dump(self._knowledge_base, f, indent=2)
            
            # Update last modified
            self.set('learned_patterns.last_updated', 
                    datetime.now().strftime('%Y-%m-%d'))
            
            print(f"💾 Saved knowledge base to {self.kb_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
            return False
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get value using dot notation: 'user_profile.personal.age'"""
        
        keys = path.split('.')
        value = self._knowledge_base
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, path: str, value: Any) -> bool:
        """Set value using dot notation"""
        
        keys = path.split('.')
        target = self._knowledge_base
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        # Set the value
        target[keys[-1]] = value
        
        # Auto-save for important updates
        if 'learned' in path or 'profile' in path:
            self.save()
        
        return True
    
    def learn_response(self, question_type: str, question_text: str, response: Any):
        """Record a learned response pattern"""
        
        learned = self.get('learned_patterns.custom_responses', {})
        
        # Create question signature
        question_sig = f"{question_type}:{question_text[:50]}"
        
        learned[question_sig] = {
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.9
        }
        
        self.set('learned_patterns.custom_responses', learned)
        
        # Update stats
        total = self.get('learned_patterns.total_questions_answered', 0)
        self.set('learned_patterns.total_questions_answered', total + 1)
        
        print(f"📚 Learned new response for: {question_type}")
    
    def get_demographic(self, field: str) -> Any:
        """Quick accessor for demographics"""
        
        # Map common field names to paths
        field_map = {
            'age': 'user_profile.personal.age',
            'gender': 'user_profile.personal.gender',
            'postcode': 'user_profile.location.postcode',
            'state': 'user_profile.location.state',
            'income': 'user_profile.financial.personal_income',
            'household_income': 'user_profile.financial.household_income',
            'employment': 'user_profile.employment.employment_status',
            'education': 'user_profile.education.highest_level',
            'marital': 'user_profile.household.marital_status',
            'children': 'user_profile.household.children',
            'household': 'user_profile.household.composition'
        }
        
        path = field_map.get(field, f'user_profile.{field}')
        return self.get(path)
    
    def get_brand_preference(self, category: str) -> Any:
        """Get brand preference for a category"""
        
        return self.get(f'preferences.brands.{category}', [])
    
    def get_survey_behavior(self, behavior_type: str) -> Any:
        """Get survey behavior pattern"""
        
        return self.get(f'survey_behaviors.{behavior_type}')
    
    def update_automation_stats(self, questions_automated: int, questions_total: int):
        """Update automation statistics"""
        
        rate = (questions_automated / questions_total * 100) if questions_total > 0 else 0
        
        self.set('learned_patterns.automation_rate', round(rate, 1))
        
        # Track improvement
        sessions = self.get('learned_patterns.total_surveys_completed', 0)
        self.set('learned_patterns.total_surveys_completed', sessions + 1)
        
        print(f"📈 Automation rate: {rate:.1f}% ({questions_automated}/{questions_total})")
        
        self.save()
    
    def create_default(self) -> Dict:
        """Create default knowledge base structure"""
        
        # Would load the full JSON structure from above
        # Abbreviated here for space
        return {
            "user_profile": {
                "personal": {"age": 45, "gender": "Male"},
                # ... rest of structure
            }
        }

# Singleton instance for easy access
knowledge = KnowledgeManager()