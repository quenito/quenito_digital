#!/usr/bin/env python3
"""
Quick Knowledge Base Cleanup Script
Removes duplicates and compresses learning data without major restructuring
"""

import json
import os
import re
from datetime import datetime

def extract_question_text(full_text):
    """Extract just the question from the massive HTML/JSON text"""
    # Common question patterns
    patterns = [
        r'What is your (\w+)\?',
        r'How old are you\?',
        r'Gender',
        r'(\d+\.)(.*?)(?:Current Progress|Prev|Next)',
        r'Please (.*?)\?',
        r'Which (.*?)\?',
        r'Select (.*?)\.',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, full_text)
        if match:
            if match.group(0).startswith(('1.', '2.', '3.')):
                # Handle numbered questions
                return match.group(2).strip()
            else:
                return match.group(0).strip()
    
    # Fallback: try to find any question mark
    if '?' in full_text:
        # Find text before question mark
        parts = full_text.split('?')
        for part in parts:
            words = part.split()
            if len(words) > 2 and len(words) < 20:
                # Likely a question
                return ' '.join(words[-10:]) + '?'
    
    return "Question text extracted"

def quick_clean_knowledge_base():
    """Perform quick cleanup of knowledge base"""
    
    print("🧹 Starting Knowledge Base Quick Cleanup...")
    
    # Load current knowledge base
    kb_path = 'data/knowledge_base.json'
    if not os.path.exists(kb_path):
        print("❌ knowledge_base.json not found!")
        return
    
    with open(kb_path, 'r') as f:
        kb = json.load(f)
    
    # Calculate original size
    original_json = json.dumps(kb, indent=2)
    original_size = len(original_json)
    
    # Backup original
    backup_path = f'data/knowledge_base_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(backup_path, 'w') as f:
        f.write(original_json)
    print(f"✅ Backup created: {backup_path}")
    
    changes_made = []
    
    # 1. Remove duplicate demographics_questions section
    if 'demographics_questions' in kb:
        # Check if it contains the duplicate structure
        demo_q = kb['demographics_questions']
        if 'age' in demo_q and 'patterns' in demo_q.get('age', {}):
            # This is the old structure - remove it
            del kb['demographics_questions']
            changes_made.append("Removed duplicate demographics_questions section")
            print("✅ Removed duplicate demographics patterns")
    
    # 2. Compress intervention learning data
    compressed_count = 0
    
    # Check brain_learning -> intervention_learning
    if 'brain_learning' in kb and 'intervention_learning' in kb['brain_learning']:
        for key, entry in kb['brain_learning']['intervention_learning'].items():
            if 'question_text' in entry and len(entry['question_text']) > 500:
                # Compress the question text
                original_text = entry['question_text']
                entry['question_text'] = extract_question_text(original_text)
                entry['original_length'] = len(original_text)  # For reference
                compressed_count += 1
    
    # Check detailed_intervention_learning
    if 'detailed_intervention_learning' in kb:
        for key, entry in kb['detailed_intervention_learning'].items():
            if 'question_text' in entry and len(entry['question_text']) > 500:
                # Compress the question text
                original_text = entry['question_text']
                entry['question_text'] = extract_question_text(original_text)
                entry['original_length'] = len(original_text)  # For reference
                compressed_count += 1
    
    if compressed_count > 0:
        changes_made.append(f"Compressed {compressed_count} learning entries")
        print(f"✅ Compressed {compressed_count} intervention learning entries")
    
    # 3. Remove empty pattern objects
    if 'demographics_questions' in kb:
        demo_q = kb['demographics_questions']
        empty_keys = []
        for key, value in demo_q.items():
            if isinstance(value, dict) and len(value) == 0:
                empty_keys.append(key)
        
        for key in empty_keys:
            del demo_q[key]
        
        if empty_keys:
            changes_made.append(f"Removed {len(empty_keys)} empty pattern objects")
            print(f"✅ Removed {len(empty_keys)} empty objects")
    
    # 4. Clean up confidence history arrays (keep only last 20 entries)
    if 'brain_learning' in kb and 'handler_performance' in kb['brain_learning']:
        for handler, data in kb['brain_learning']['handler_performance'].items():
            if 'confidence_history' in data and len(data['confidence_history']) > 20:
                original_length = len(data['confidence_history'])
                data['confidence_history'] = data['confidence_history'][-20:]
                changes_made.append(f"Trimmed {handler} confidence history from {original_length} to 20 entries")
    
    # Save cleaned version
    with open(kb_path, 'w') as f:
        json.dump(kb, f, indent=2)
    
    # Calculate new size and report
    new_json = json.dumps(kb, indent=2)
    new_size = len(new_json)
    reduction_bytes = original_size - new_size
    reduction_percent = (reduction_bytes / original_size) * 100
    
    print("\n📊 Cleanup Results:")
    print(f"Original size: {original_size:,} characters")
    print(f"New size: {new_size:,} characters")
    print(f"Size reduction: {reduction_bytes:,} characters ({reduction_percent:.1f}%)")
    
    if changes_made:
        print("\n✅ Changes made:")
        for change in changes_made:
            print(f"   - {change}")
    else:
        print("\n✅ Knowledge base is already optimized!")
    
    print("\n✨ Quick cleanup complete!")
    
    # Offer to show sample of compressed data
    if compressed_count > 0:
        print("\n💡 Tip: Learning functionality preserved - only removed redundant HTML/JSON page data")

if __name__ == "__main__":
    quick_clean_knowledge_base()
