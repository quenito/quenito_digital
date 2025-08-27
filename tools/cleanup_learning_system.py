#!/usr/bin/env python3
"""
Quenito Learning System Cleanup & Restructure
Following the official Learning System Architecture document
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any

class LearningSystemCleaner:
    def __init__(self):
        self.base_path = "personas/quenito"
        self.backup_dir = f"{self.base_path}/backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.stats = {
            "removed_empty": 0,
            "moved_qa_pairs": 0,
            "core_identity_fields": 0,
            "existing_learned": 0
        }
    
    def backup_all_files(self):
        """Create backups before any modifications"""
        print("📦 Creating backups...")
        os.makedirs(self.backup_dir, exist_ok=True)
        
        files_to_backup = [
            "knowledge_base.json",
            "learned_responses.json",
            "learned_patterns.json"
        ]
        
        for file in files_to_backup:
            src = f"{self.base_path}/{file}"
            if os.path.exists(src):
                dst = f"{self.backup_dir}/{file}"
                shutil.copy2(src, dst)
                print(f"  ✅ Backed up {file}")
    
    def clean_knowledge_base(self):
        """Restructure knowledge_base to ONLY contain core identity"""
        print("\n🧠 Restructuring knowledge_base.json...")
        
        kb_path = f"{self.base_path}/knowledge_base.json"
        with open(kb_path, 'r') as f:
            current_kb = json.load(f)
        
        # Extract Q&A entries that need to be moved
        qa_entries = {}
        entries_to_remove = []
        
        for key, value in current_kb.items():
            # Identify learning entries (Q&A pairs)
            if key.startswith("learning_") or "question_text" in str(value):
                # Check if it has valid response data
                if isinstance(value, dict):
                    response_val = value.get('response_value', '')
                    response_vals = value.get('response_values', [])
                    
                    if response_val or response_vals:
                        # Valid Q&A - prepare for moving
                        question = value.get('question_text', '')
                        if question and len(question) > 20:
                            qa_entries[question] = {
                                "answer": response_val if response_val else response_vals,
                                "element_type": value.get('element_type', 'unknown'),
                                "confidence": value.get('vision_confidence', 85) / 100,
                                "success_count": 1,
                                "last_used": datetime.now().isoformat()
                            }
                            self.stats["moved_qa_pairs"] += 1
                    else:
                        # Empty response - mark for removal
                        self.stats["removed_empty"] += 1
                
                entries_to_remove.append(key)
        
        # Remove all Q&A entries from knowledge_base
        for key in entries_to_remove:
            del current_kb[key]
            print(f"  ❌ Removed: {key[:50]}...")
        
        # Build clean core identity structure
        clean_kb = {
            "identity": {
                "name": "Matt",
                "age": 45,
                "birth_year": 1980,
                "gender": "Male"
            },
            "location": {
                "city": "Sydney",
                "state": "NSW",
                "postcode": "2217",
                "suburb": "Kingsgrove",
                "country": "Australia"
            },
            "family": {
                "marital_status": "Married",
                "spouse": "Partner",
                "children_count": 2,
                "children_ages": [3, 6],
                "children_genders": ["Female", "Female"]
            },
            "work": {
                "employer": "Woolworths",
                "role": "Data Analyst", 
                "industry": "Retail",
                "years_experience": 10
            },
            "preferences": {
                "brands": {
                    "positive": ["Nature's Way", "Swisse", "Mars", "Cadbury", 
                                "Weet-Bix", "Vegemite", "Lilydale", "Inghams"],
                    "quality": ["Weet-Bix", "Lilydale", "Vegemite", "Cadbury", "Inghams"],
                    "value": ["Nature's Way", "Swisse"],
                    "poor_value": ["Cadbury", "Bega"]
                },
                "shopping": {
                    "grocery": ["Woolworths", "Coles", "Aldi"],
                    "mattress_retailers": ["Koala", "IKEA"],
                    "visited_retailers": ["Harvey Norman", "Myer", "David Jones"]
                },
                "activities": {
                    "weekend": ["Watched TV", "Family time"],
                    "interests": ["Technology", "Data", "Automation"]
                }
            },
            "demographics": {
                "income_bracket": "AUD 40,000 - 49,999",
                "household_income": "AUD 80,000 - 99,999",
                "sexuality": "Heterosexual"
            }
        }
        
        # Preserve any existing valid core data
        for key in ["identity", "location", "family", "work", "preferences", "demographics"]:
            if key in current_kb and isinstance(current_kb[key], dict):
                # Merge with our clean structure
                clean_kb[key].update(current_kb[key])
        
        self.stats["core_identity_fields"] = sum(len(v) for v in clean_kb.values() if isinstance(v, dict))
        
        # Save clean knowledge base
        with open(kb_path, 'w') as f:
            json.dump(clean_kb, f, indent=2)
        
        print(f"  ✅ Knowledge base cleaned: {len(clean_kb)} core categories")
        
        return qa_entries
    
    def update_learned_responses(self, qa_entries: Dict[str, Any]):
        """Move valid Q&A pairs to learned_responses.json"""
        print("\n💡 Updating learned_responses.json...")
        
        lr_path = f"{self.base_path}/learned_responses.json"
        
        # Load existing learned responses
        if os.path.exists(lr_path):
            with open(lr_path, 'r') as f:
                learned = json.load(f)
            self.stats["existing_learned"] = len(learned)
        else:
            learned = {}
        
        # Add moved Q&A pairs
        for question, data in qa_entries.items():
            if question not in learned:
                learned[question] = data
                print(f"  ➕ Added: {question[:60]}...")
            else:
                # Update confidence if higher
                if data['confidence'] > learned[question].get('confidence', 0):
                    learned[question]['confidence'] = data['confidence']
                learned[question]['success_count'] += 1
        
        # Save updated learned responses
        with open(lr_path, 'w') as f:
            json.dump(learned, f, indent=2)
        
        print(f"  ✅ Learned responses updated: {len(learned)} total Q&As")
    
    def create_learned_patterns(self):
        """Create learned_patterns.json with initial patterns"""
        print("\n🎯 Creating learned_patterns.json...")
        
        lp_path = f"{self.base_path}/learned_patterns.json"
        
        patterns = {
            "gender": {
                "patterns": [
                    "are you male or female",
                    "what is your gender",
                    "which gender do you belong"
                ],
                "response": "Male",
                "confidence": 1.0
            },
            "age": {
                "patterns": [
                    "how old are you",
                    "what is your age",
                    "birth year"
                ],
                "response_logic": "return_age_or_birth_year",
                "confidence": 1.0
            },
            "children": {
                "patterns": [
                    "children under 18",
                    "children aged under",
                    "kids in household",
                    "do you have children"
                ],
                "response": "Yes",
                "response_logic": "check_if_needs_ages",
                "confidence": 0.95
            },
            "location": {
                "patterns": [
                    "what is your postcode",
                    "where do you live",
                    "suburb",
                    "city"
                ],
                "response_logic": "return_location_field",
                "confidence": 1.0
            },
            "industry_screening": {
                "patterns": [
                    "work in any of the following industries",
                    "employed in any of these",
                    "family members work"
                ],
                "response_logic": "if_retail_exists_select_else_none",
                "confidence": 0.95
            },
            "brand_awareness": {
                "patterns": [
                    "which brands have you heard of",
                    "brands are you aware of",
                    "heard of the following brands"
                ],
                "response_logic": "select_known_brands",
                "confidence": 0.90
            }
        }
        
        with open(lp_path, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        print(f"  ✅ Created patterns file with {len(patterns)} patterns")
    
    def print_summary(self):
        """Print cleanup summary"""
        print("\n" + "="*60)
        print("🎉 CLEANUP COMPLETE!")
        print("="*60)
        print(f"📊 Statistics:")
        print(f"  • Removed empty entries: {self.stats['removed_empty']}")
        print(f"  • Moved valid Q&A pairs: {self.stats['moved_qa_pairs']}")
        print(f"  • Core identity fields: {self.stats['core_identity_fields']}")
        print(f"  • Total learned responses: {self.stats['existing_learned'] + self.stats['moved_qa_pairs']}")
        print(f"\n✅ All files backed up to: {self.backup_dir}")
        print("\n🚀 Learning system is now properly structured!")
    
    def run(self):
        """Execute complete cleanup"""
        print("🧹 QUENITO LEARNING SYSTEM CLEANUP")
        print("="*60)
        
        # Step 1: Backup
        self.backup_all_files()
        
        # Step 2: Clean knowledge base and extract Q&As
        qa_entries = self.clean_knowledge_base()
        
        # Step 3: Update learned responses
        self.update_learned_responses(qa_entries)
        
        # Step 4: Create patterns file
        self.create_learned_patterns()
        
        # Step 5: Summary
        self.print_summary()


if __name__ == "__main__":
    cleaner = LearningSystemCleaner()
    cleaner.run()