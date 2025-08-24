#!/usr/bin/env python3
"""
🔧 FIX LEARNING SYSTEM STRUCTURE
Restructures files to match the architecture guide requirements
"""

import json
import os
from datetime import datetime
from pathlib import Path

def fix_learning_structure():
    """Fix the structure of learning system files"""
    
    print("🔧 FIXING LEARNING SYSTEM STRUCTURE")
    print("=" * 60)
    
    base_path = Path("personas/quenito")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create new backup before fixing
    backup_dir = base_path / f"backups_fix_{timestamp}"
    backup_dir.mkdir(exist_ok=True)
    print(f"📦 Creating backup: {backup_dir.name}")
    
    # 1. Fix knowledge_base.json structure
    print("\n📚 Fixing knowledge_base.json...")
    kb_path = base_path / "knowledge_base.json"
    
    if kb_path.exists():
        # Backup current
        with open(kb_path, 'r') as f:
            kb_current = json.load(f)
        with open(backup_dir / "knowledge_base.json", 'w') as f:
            json.dump(kb_current, f, indent=2)
        
        # Restructure to match architecture guide
        kb_fixed = {
            "personal": {},
            "demographics": {},
            "preferences": {},
            "behavior": {},
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
        
        # Migrate existing data to proper categories
        for key, value in kb_current.items():
            if key in ["name", "full_name", "first_name", "last_name"]:
                kb_fixed["personal"][key] = value
            elif key in ["age", "gender", "birth_year", "location", "city", "state", "postcode"]:
                kb_fixed["demographics"][key] = value
            elif key in ["marital_status", "children_count", "children_ages", "family"]:
                kb_fixed["demographics"][key] = value
            elif key in ["occupation", "industry", "company", "employment_status"]:
                kb_fixed["demographics"][key] = value
            elif key in ["shopping_frequency", "preferred_brands", "brand_preferences"]:
                kb_fixed["preferences"][key] = value
            elif key in ["survey_style", "response_patterns"]:
                kb_fixed["behavior"][key] = value
            elif key not in ["personal", "demographics", "preferences", "behavior", "metadata", "learning_stats"]:
                # Put any other fields in preferences for now
                kb_fixed["preferences"][key] = value
        
        # Save fixed structure
        with open(kb_path, 'w') as f:
            json.dump(kb_fixed, f, indent=2)
        
        print(f"   ✅ Restructured with 6 required categories")
        print(f"   📊 Migrated {len(kb_current)} fields to proper categories")
    
    # 2. Fix learned_responses.json structure
    print("\n💡 Fixing learned_responses.json...")
    lr_path = base_path / "learned_responses.json"
    
    if lr_path.exists():
        # Backup current
        with open(lr_path, 'r') as f:
            lr_current = json.load(f)
        with open(backup_dir / "learned_responses.json", 'w') as f:
            json.dump(lr_current, f, indent=2)
        
        # Check if it's already properly structured
        if "responses" not in lr_current:
            # Assume current structure IS the responses, wrap it
            lr_fixed = {
                "responses": lr_current if isinstance(lr_current, dict) else {},
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_responses": len(lr_current) if isinstance(lr_current, dict) else 0,
                    "version": "1.0"
                }
            }
        else:
            lr_fixed = lr_current
            if "metadata" not in lr_fixed:
                lr_fixed["metadata"] = {
                    "last_updated": datetime.now().isoformat(),
                    "total_responses": len(lr_fixed.get("responses", {})),
                    "version": "1.0"
                }
        
        # Save fixed structure
        with open(lr_path, 'w') as f:
            json.dump(lr_fixed, f, indent=2)
        
        print(f"   ✅ Added 'responses' wrapper key")
        print(f"   📊 Total responses: {len(lr_fixed['responses'])}")
    else:
        # Create new file with proper structure
        lr_fixed = {
            "responses": {},
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_responses": 0,
                "version": "1.0"
            }
        }
        with open(lr_path, 'w') as f:
            json.dump(lr_fixed, f, indent=2)
        print(f"   ✅ Created new learned_responses.json with proper structure")
    
    # 3. Fix learned_patterns.json structure
    print("\n🎯 Fixing learned_patterns.json...")
    lp_path = base_path / "learned_patterns.json"
    
    if lp_path.exists():
        # Backup current
        with open(lp_path, 'r') as f:
            lp_current = json.load(f)
        with open(backup_dir / "learned_patterns.json", 'w') as f:
            json.dump(lp_current, f, indent=2)
        
        # Check if it's already properly structured
        if "patterns" not in lp_current:
            # Assume current structure IS the patterns, wrap it
            lp_fixed = {
                "patterns": lp_current if isinstance(lp_current, dict) else {
                    "demographics": [],
                    "screening": [],
                    "preferences": [],
                    "behavior": [],
                    "brand": [],
                    "general": []
                },
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "total_patterns": sum(len(v) if isinstance(v, list) else 1 
                                        for v in (lp_current.values() if isinstance(lp_current, dict) else [])),
                    "version": "1.0"
                }
            }
        else:
            lp_fixed = lp_current
            if "metadata" not in lp_fixed:
                lp_fixed["metadata"] = {
                    "last_updated": datetime.now().isoformat(),
                    "total_patterns": sum(len(v) if isinstance(v, list) else 1 
                                        for v in lp_fixed.get("patterns", {}).values()),
                    "version": "1.0"
                }
        
        # Save fixed structure
        with open(lp_path, 'w') as f:
            json.dump(lp_fixed, f, indent=2)
        
        print(f"   ✅ Added 'patterns' wrapper key")
        print(f"   📊 Pattern categories: {len(lp_fixed['patterns'])}")
    else:
        # Create new file with proper structure
        lp_fixed = {
            "patterns": {
                "demographics": [],
                "screening": [],
                "preferences": [],
                "behavior": [],
                "brand": [],
                "general": []
            },
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_patterns": 0,
                "version": "1.0"
            }
        }
        with open(lp_path, 'w') as f:
            json.dump(lp_fixed, f, indent=2)
        print(f"   ✅ Created new learned_patterns.json with proper structure")
    
    # 4. Create sessions directory for manual intervention data
    print("\n📁 Creating sessions directory...")
    sessions_dir = base_path / "sessions"
    sessions_dir.mkdir(exist_ok=True)
    print(f"   ✅ Sessions directory ready: {sessions_dir}")
    
    # 5. Check for any intervention data in knowledge_base and extract it
    print("\n🔍 Checking for misplaced intervention data...")
    if kb_path.exists():
        with open(kb_path, 'r') as f:
            kb_data = json.load(f)
        
        # Look for any keys that might be intervention data
        intervention_keys = []
        for category in kb_data.values():
            if isinstance(category, dict):
                for key in list(category.keys()):
                    # Check if this looks like intervention data (long question text)
                    if len(key) > 50 or '?' in key:
                        intervention_keys.append(key)
        
        if intervention_keys:
            print(f"   ⚠️  Found {len(intervention_keys)} potential intervention entries")
            print(f"   💡 These should be moved to session files or learned_responses")
            
            # Create a session file for these
            session_file = sessions_dir / f"recovered_interventions_{timestamp}.json"
            recovered_data = {
                "session_id": f"recovery_{timestamp}",
                "timestamp": datetime.now().isoformat(),
                "recovered_interventions": {}
            }
            
            # Extract intervention data
            for category_name, category_data in kb_data.items():
                if isinstance(category_data, dict):
                    for key in list(category_data.keys()):
                        if len(key) > 50 or '?' in key:
                            recovered_data["recovered_interventions"][key] = category_data[key]
                            del category_data[key]
            
            if recovered_data["recovered_interventions"]:
                with open(session_file, 'w') as f:
                    json.dump(recovered_data, f, indent=2)
                
                # Save cleaned knowledge base
                with open(kb_path, 'w') as f:
                    json.dump(kb_data, f, indent=2)
                
                print(f"   ✅ Moved {len(recovered_data['recovered_interventions'])} entries to: {session_file.name}")
        else:
            print(f"   ✅ No misplaced intervention data found")
    
    print("\n" + "=" * 60)
    print("✅ STRUCTURE FIXING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   • knowledge_base.json: 6 required categories")
    print(f"   • learned_responses.json: Proper 'responses' structure")
    print(f"   • learned_patterns.json: Proper 'patterns' structure")
    print(f"   • sessions/: Directory created for interventions")
    print(f"   • Backup saved to: {backup_dir.name}")
    print("\n🚀 Now run verify_learning_cleanup.py to confirm!")

if __name__ == "__main__":
    try:
        fix_learning_structure()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()