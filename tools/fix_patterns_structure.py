#!/usr/bin/env python3
"""
🔧 FIX PATTERNS STRUCTURE
Convert individual pattern objects to lists as per architecture guide
"""

import json
from pathlib import Path
from datetime import datetime

def fix_patterns():
    """Fix learned_patterns.json to use lists as per architecture"""
    
    print("🔧 FIXING PATTERNS STRUCTURE")
    print("=" * 60)
    
    base_path = Path("personas/quenito")
    lp_path = base_path / "learned_patterns.json"
    
    if not lp_path.exists():
        print("❌ learned_patterns.json not found!")
        return
    
    # Read current patterns
    with open(lp_path, 'r') as f:
        data = json.load(f)
    
    # Backup first
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = base_path / f"learned_patterns_backup_{timestamp}.json"
    with open(backup_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"📦 Backup saved: {backup_path.name}")
    
    # Fix the structure
    if "patterns" in data:
        patterns = data["patterns"]
        fixed_patterns = {}
        
        for category, content in patterns.items():
            if isinstance(content, dict):
                # Convert single dict to list with one item
                fixed_patterns[category] = [content]
                print(f"   ✅ Converted {category} from dict to list")
            elif isinstance(content, list):
                # Already a list, keep as is
                fixed_patterns[category] = content
                print(f"   ✅ {category} already a list")
            else:
                # Empty or unknown, make empty list
                fixed_patterns[category] = []
                print(f"   ⚠️  {category} was invalid, created empty list")
        
        # Update the data
        data["patterns"] = fixed_patterns
        
        # Update metadata
        if "metadata" in data:
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            total = sum(len(v) for v in fixed_patterns.values())
            data["metadata"]["total_patterns"] = total
    
    # Save fixed version
    with open(lp_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ PATTERNS STRUCTURE FIXED!")
    print("=" * 60)
    print("\nNow patterns are properly structured as lists.")
    print("Run verify_learning_cleanup.py to confirm!")

if __name__ == "__main__":
    try:
        fix_patterns()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()