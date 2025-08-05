# cleanup_bad_learning_data.py
"""
Clean up learning entries that have no useful response data
Keep only entries with actual text responses, not indices
"""

import json
import os
from datetime import datetime

def cleanup_knowledge_base(backup=True):
    """Remove learning entries with only numeric indices as responses"""
    
    kb_path = "personas/quenito/knowledge_base.json"
    
    # Load knowledge base
    with open(kb_path, 'r') as f:
        kb_data = json.load(f)
    
    # Backup first if requested
    if backup:
        backup_path = f"personas/quenito/knowledge_base_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_path, 'w') as f:
            json.dump(kb_data, f, indent=2)
        print(f"✅ Backup saved to: {backup_path}")
    
    # Track what we're cleaning
    total_entries = 0
    removed_entries = 0
    kept_entries = 0
    
    # Check detailed_intervention_learning section
    if 'detailed_intervention_learning' in kb_data:
        learning_data = kb_data['detailed_intervention_learning']
        entries_to_remove = []
        
        for key, entry in learning_data.items():
            total_entries += 1
            
            # Check if this has useful data
            response_value = entry.get('response_value', '')
            response_values = entry.get('response_values', [])
            
            # Criteria for BAD data:
            # 1. Empty response
            # 2. Single digit number (0-9)
            # 3. All values are single digits
            is_bad_data = (
                not response_value or
                response_value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ''] or
                (response_values and all(v in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] for v in response_values))
            )
            
            # BUT KEEP if it's from successful automation
            if entry.get('automation_success', False):
                is_bad_data = False
            
            if is_bad_data:
                entries_to_remove.append(key)
                removed_entries += 1
                print(f"❌ Removing: {key}")
                print(f"   Question: {entry.get('question_text', '')[:60]}...")
                print(f"   Response: '{response_value}' (useless!)")
            else:
                kept_entries += 1
                print(f"✅ Keeping: {key}")
                print(f"   Question: {entry.get('question_text', '')[:60]}...")
                print(f"   Response: '{response_value}'")
        
        # Remove bad entries
        for key in entries_to_remove:
            del learning_data[key]
    
    # Save cleaned knowledge base
    with open(kb_path, 'w') as f:
        json.dump(kb_data, f, indent=2)
    
    print("\n" + "="*60)
    print("🧹 CLEANUP COMPLETE")
    print(f"📊 Total entries reviewed: {total_entries}")
    print(f"❌ Entries removed: {removed_entries}")
    print(f"✅ Entries kept: {kept_entries}")
    print(f"💾 Cleaned knowledge base saved!")
    
    return removed_entries, kept_entries

def analyze_bad_patterns():
    """Analyze what types of questions are failing to capture properly"""
    
    kb_path = "personas/quenito/knowledge_base.json"
    
    with open(kb_path, 'r') as f:
        kb_data = json.load(f)
    
    bad_patterns = {}
    
    if 'detailed_intervention_learning' in kb_data:
        for key, entry in kb_data['detailed_intervention_learning'].items():
            response_value = entry.get('response_value', '')
            
            # If it's a bad capture
            if response_value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '']:
                question_type = entry.get('question_type', 'unknown')
                if question_type not in bad_patterns:
                    bad_patterns[question_type] = []
                
                bad_patterns[question_type].append({
                    'question': entry.get('question_text', '')[:80],
                    'bad_response': response_value,
                    'element_type': entry.get('element_type', '')
                })
    
    print("\n📊 BAD CAPTURE PATTERNS:")
    print("="*60)
    for q_type, examples in bad_patterns.items():
        print(f"\n❌ {q_type.upper()} ({len(examples)} failures)")
        for i, ex in enumerate(examples[:3]):  # Show first 3
            print(f"   {i+1}. {ex['question']}...")
            print(f"      Got: '{ex['bad_response']}' from {ex['element_type']}")

if __name__ == "__main__":
    print("🧹 QUENITO KNOWLEDGE BASE CLEANUP")
    print("="*60)
    
    # First analyze patterns
    analyze_bad_patterns()
    
    print("\n⚠️  This will remove all learning entries with only numeric indices!")
    print("✅ A backup will be created first")
    
    confirm = input("\nProceed with cleanup? (yes/no): ")
    
    if confirm.lower() == 'yes':
        removed, kept = cleanup_knowledge_base()
        
        if removed > 0:
            print("\n💡 RECOMMENDATION:")
            print("Now run surveys with the FIXED capture method to collect real data!")
    else:
        print("❌ Cleanup cancelled")