#!/usr/bin/env python3
"""
One-time migration script to organize existing patterns into platform folders
Run this ONCE to organize your existing visual patterns
"""

import os
import json
import shutil
from datetime import datetime

def migrate_visual_patterns():
    """Migrate existing patterns to platform-specific folders"""
    
    print("\n" + "="*60)
    print("📦 VISUAL PATTERN MIGRATION TOOL")
    print("="*60)
    
    base_dir = "personas/quenito/visual_patterns"
    
    if not os.path.exists(base_dir):
        print("❌ No visual_patterns directory found!")
        return
    
    # Create platform directories
    myopinions_dir = os.path.join(base_dir, "myopinions")
    yougov_dir = os.path.join(base_dir, "yougov")
    
    os.makedirs(myopinions_dir, exist_ok=True)
    os.makedirs(yougov_dir, exist_ok=True)
    
    migrated_count = 0
    already_organized = 0
    
    # Process all files in base directory
    for filename in os.listdir(base_dir):
        file_path = os.path.join(base_dir, filename)
        
        # Skip if it's already a directory
        if os.path.isdir(file_path):
            print(f"📁 Skipping directory: {filename}")
            already_organized += 1
            continue
        
        # Only process JSON files
        if not filename.endswith('.json'):
            print(f"⏭️ Skipping non-JSON file: {filename}")
            continue
        
        try:
            # Read the pattern file
            with open(file_path, 'r') as f:
                pattern_data = json.load(f)
            
            # Determine platform
            platform = pattern_data.get('platform', 'myopinions')  # Default to myopinions
            
            # Check if automation data hints at platform
            if 'automation' in pattern_data:
                automation = pattern_data.get('automation', {})
                if isinstance(automation, dict):
                    if automation.get('platform') == 'yougov':
                        platform = 'yougov'
            
            # Check filename for platform hints
            if 'yougov' in filename.lower():
                platform = 'yougov'
            
            # Update pattern data with platform
            pattern_data['platform'] = platform
            
            # Determine target directory
            if platform == 'yougov':
                target_dir = yougov_dir
            else:
                target_dir = myopinions_dir
            
            # Create new path
            new_path = os.path.join(target_dir, filename)
            
            # Save to new location
            with open(new_path, 'w') as f:
                json.dump(pattern_data, f, indent=2)
            
            # Remove old file
            os.remove(file_path)
            
            print(f"✅ Migrated: {filename} → {platform}/")
            migrated_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 MIGRATION COMPLETE!")
    print("="*60)
    print(f"✅ Migrated: {migrated_count} patterns")
    print(f"📁 Already organized: {already_organized} directories")
    
    # Show final structure
    print("\n📂 New Structure:")
    print(f"  {base_dir}/")
    
    # Count patterns in each platform
    myopinions_count = len([f for f in os.listdir(myopinions_dir) if f.endswith('.json')])
    yougov_count = len([f for f in os.listdir(yougov_dir) if f.endswith('.json')]) if os.path.exists(yougov_dir) else 0
    
    print(f"    ├── myopinions/ ({myopinions_count} patterns)")
    print(f"    └── yougov/ ({yougov_count} patterns)")
    
    print("\n✨ Your patterns are now organized by platform!")
    print("🚀 Future patterns will automatically go to the right folder!")

if __name__ == "__main__":
    migrate_visual_patterns()
    input("\n✅ Press Enter to close >>> ")