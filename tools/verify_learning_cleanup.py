#!/usr/bin/env python3
"""
🔍 LEARNING SYSTEM CLEANUP VERIFICATION
Ensures all files are properly structured after cleanup
"""

import json
import os
from datetime import datetime
from pathlib import Path

def verify_cleanup():
    """Verify the learning system cleanup was successful"""
    
    print("🔍 VERIFYING LEARNING SYSTEM CLEANUP")
    print("=" * 60)
    
    base_path = Path("personas/quenito")
    results = {
        "knowledge_base": {"status": "❌", "issues": []},
        "learned_responses": {"status": "❌", "issues": []},
        "learned_patterns": {"status": "❌", "issues": []},
        "overall": True
    }
    
    # 1. Verify knowledge_base.json
    print("\n📚 Checking knowledge_base.json...")
    kb_path = base_path / "knowledge_base.json"
    if kb_path.exists():
        with open(kb_path, 'r') as f:
            kb = json.load(f)
        
        # Check for required categories
        required_categories = ["personal", "demographics", "preferences", "behavior", "metadata", "learning_stats"]
        missing = [cat for cat in required_categories if cat not in kb]
        
        if missing:
            results["knowledge_base"]["issues"].append(f"Missing categories: {missing}")
            results["overall"] = False
        else:
            print(f"   ✅ All 6 core categories present")
            
        # Check for any leftover intervention data
        if "detailed_intervention_learning_data" in kb:
            results["knowledge_base"]["issues"].append("Old intervention data still present")
            results["overall"] = False
        else:
            print(f"   ✅ No old intervention data found")
            
        # Count fields
        total_fields = sum(len(v) if isinstance(v, dict) else 1 for v in kb.values())
        print(f"   📊 Total fields: {total_fields}")
        
        if not results["knowledge_base"]["issues"]:
            results["knowledge_base"]["status"] = "✅"
    else:
        results["knowledge_base"]["issues"].append("File not found")
        results["overall"] = False
    
    # 2. Verify learned_responses.json
    print("\n💡 Checking learned_responses.json...")
    lr_path = base_path / "learned_responses.json"
    if lr_path.exists():
        with open(lr_path, 'r') as f:
            lr = json.load(f)
        
        # Check structure
        if "responses" not in lr:
            results["learned_responses"]["issues"].append("Missing 'responses' key")
            results["overall"] = False
        else:
            responses = lr["responses"]
            valid_count = 0
            invalid_count = 0
            
            for key, value in responses.items():
                # Handle both string and dict responses
                if isinstance(value, dict):
                    # If it's a dict, check if it has an 'answer' key
                    if value.get("answer") and str(value["answer"]).strip():
                        valid_count += 1
                    else:
                        invalid_count += 1
                        results["learned_responses"]["issues"].append(f"Empty response for: {key[:50]}...")
                elif isinstance(value, str):
                    if value and value.strip():  # Non-empty response
                        valid_count += 1
                    else:
                        invalid_count += 1
                        results["learned_responses"]["issues"].append(f"Empty response for: {key[:50]}...")
                else:
                    # Unknown type
                    invalid_count += 1
                    results["learned_responses"]["issues"].append(f"Invalid type for: {key[:50]}...")
            
            print(f"   ✅ Valid responses: {valid_count}")
            if invalid_count > 0:
                print(f"   ⚠️  Empty responses: {invalid_count}")
            
            # Check metadata
            if "metadata" in lr:
                print(f"   ✅ Metadata present: last_updated = {lr['metadata'].get('last_updated', 'N/A')}")
            
            if valid_count > 0 and invalid_count == 0:
                results["learned_responses"]["status"] = "✅"
    else:
        results["learned_responses"]["issues"].append("File not found")
        results["overall"] = False
    
    # 3. Verify learned_patterns.json
    print("\n🎯 Checking learned_patterns.json...")
    lp_path = base_path / "learned_patterns.json"
    if lp_path.exists():
        with open(lp_path, 'r') as f:
            lp = json.load(f)
        
        # Check structure
        if "patterns" not in lp:
            results["learned_patterns"]["issues"].append("Missing 'patterns' key")
            results["overall"] = False
        else:
            patterns = lp["patterns"]
            print(f"   ✅ Pattern categories: {len(patterns)}")
            
            for category, items in patterns.items():
                if isinstance(items, list):
                    print(f"      • {category}: {len(items)} patterns")
                else:
                    results["learned_patterns"]["issues"].append(f"Invalid structure for {category}")
            
            if not results["learned_patterns"]["issues"]:
                results["learned_patterns"]["status"] = "✅"
    else:
        results["learned_patterns"]["issues"].append("File not found")
        results["overall"] = False
    
    # 4. Check for backups
    print("\n💾 Checking for backups...")
    backup_dirs = list(base_path.glob("backups_*"))
    if backup_dirs:
        latest_backup = sorted(backup_dirs)[-1]
        print(f"   ✅ Latest backup: {latest_backup.name}")
        
        # List backup contents
        backup_files = list(latest_backup.glob("*.json"))
        print(f"   📁 Backup contains {len(backup_files)} files:")
        for bf in backup_files:
            print(f"      • {bf.name}")
    else:
        print("   ⚠️  No backups found")
    
    # 5. Final Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    for component, data in results.items():
        if component != "overall":
            status = data["status"]
            issues = data["issues"]
            print(f"\n{component}: {status}")
            if issues:
                for issue in issues:
                    print(f"   ⚠️  {issue}")
    
    print("\n" + "=" * 60)
    if results["overall"]:
        print("✅ LEARNING SYSTEM IS PROPERLY STRUCTURED!")
        print("🚀 Ready for survey automation!")
    else:
        print("⚠️  SOME ISSUES DETECTED - Review above")
        print("💡 Run cleanup script again if needed")
    print("=" * 60)
    
    return results["overall"]

if __name__ == "__main__":
    try:
        success = verify_cleanup()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)