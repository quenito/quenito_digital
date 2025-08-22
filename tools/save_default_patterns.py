#!/usr/bin/env python3
"""
Save default patterns to learned_patterns.json
Run this once to populate the file with defaults
"""
from services.intelligent_learning_system import IntelligentLearningSystem

# Initialize system
print("🔄 Initializing learning system...")
learning = IntelligentLearningSystem()

# Save the default patterns to file
learning._save_json(learning.learned_patterns_path, learning.learned_patterns)

print("✅ Default patterns saved to learned_patterns.json")
print(f"📊 Total patterns: {len(learning.learned_patterns)}")
print(f"📁 File location: {learning.learned_patterns_path}")
print("\nPatterns saved:")
for name, data in learning.learned_patterns.items():
    print(f"  • {name}: {data.get('response', data.get('response_logic', 'custom logic'))}")