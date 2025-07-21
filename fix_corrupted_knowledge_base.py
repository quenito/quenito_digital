# 🔧 KNOWLEDGE BASE CORRUPTION FIX
# Run this to reset the corrupted knowledge_base.json

import json
import os
import shutil
import time
from datetime import datetime

def fix_corrupted_knowledge_base():
    """Fix the corrupted knowledge base file"""
    
    knowledge_base_path = "data/knowledge_base.json"
    backup_path = f"data/knowledge_base_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        # 1. Backup the corrupted file
        if os.path.exists(knowledge_base_path):
            shutil.copy2(knowledge_base_path, backup_path)
            print(f"📋 Corrupted file backed up to: {backup_path}")
        
        # 2. Create a fresh knowledge base with brain learning structures
        fresh_knowledge_base = {
            "user_profile": {
                "age": "45",
                "gender": "Male",
                "location": "New South Wales",
                "postcode": "2217",
                "occupation": "Data Analyst",
                "employment_status": "Full-time",
                "industry": "Retail",
                "personal_income": "$100,000 to $149,999",
                "household_income": "$200,000 to $499,999",
                "education": "High school education",
                "marital_status": "Married/civil partnership",
                "household_size": "4",
                "children": "Yes",
                "pets": "Yes",
                "birth_country": "Australia",
                "work_sector": "Private Sector",
                "work_arrangement": "Mix of on-site and home-based",
                "sub_industry": "Supermarkets",
                "occupation_level": "Academic/Professional",
                "location_type": "In a large metropolitan city"
            },
            "demographics_questions": {
                "age": {
                    "patterns": ["how old", "age", "what is your age"],
                    "responses": ["45", "forty-five"]
                },
                "gender": {
                    "patterns": ["gender", "male", "female", "sex"],
                    "responses": ["Male", "M"]
                },
                "location": {
                    "patterns": ["state", "location", "where do you live"],
                    "responses": ["New South Wales", "NSW"]
                }
            },
            "brain_learning": {
                "success_patterns": {},
                "handler_performance": {
                    "demographics_handler": {
                        "total_attempts": 0,
                        "successful_attempts": 0,
                        "success_rate": 0.0,
                        "avg_confidence": 0.0,
                        "trend": "new"
                    }
                },
                "strategy_preferences": {},
                "last_session": {
                    "learning_events": [],
                    "session_id": f"session_{int(time.time())}",
                    "start_time": time.time()
                },
                "last_updated": time.time()
            },
            "intervention_learning": {},
            "automation_stats": {
                "total_questions": 0,
                "successful_automations": 0,
                "manual_interventions": 0,
                "success_rate": 0.0
            }
        }
        
        # 3. Save the fresh knowledge base
        os.makedirs("data", exist_ok=True)
        with open(knowledge_base_path, 'w', encoding='utf-8') as f:
            json.dump(fresh_knowledge_base, f, indent=2, ensure_ascii=False)
        
        print("✅ Fresh knowledge base created!")
        print("🧠 Brain learning structures initialized")
        print("🎯 Ready for strategy learning and automation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing knowledge base: {e}")
        return False

if __name__ == "__main__":
    fix_corrupted_knowledge_base()