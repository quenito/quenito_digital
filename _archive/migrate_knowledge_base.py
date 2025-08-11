# migrate_knowledge_base.py
"""
Migrate knowledge base to persona-based structure
Moves persona-specific data while keeping system components in place
"""

import os
import json
import shutil
from datetime import datetime

def migrate_knowledge_base():
    """Migrate knowledge base to persona structure"""
    
    print("🔄 KNOWLEDGE BASE MIGRATION")
    print("="*50)
    
    # Paths
    old_kb_path = "data/knowledge_base.json"
    new_kb_path = "personas/quenito/knowledge_base.json"
    backup_path = f"data/knowledge_base_backup_{int(datetime.now().timestamp())}.json"
    
    # Check if migration needed
    if not os.path.exists(old_kb_path):
        print("❌ No knowledge base found at data/knowledge_base.json")
        print("✅ Creating fresh knowledge base for Quenito...")
        
        # Create fresh knowledge base
        os.makedirs("personas/quenito", exist_ok=True)
        fresh_kb = {
            "persona": "quenito",
            "created": datetime.now().isoformat(),
            "brain_learning": {
                "intervention_history": [],
                "success_patterns": {},
                "strategy_preferences": {},
                "handler_performance": {}
            },
            "survey_responses": {},
            "platform_patterns": {
                "myopinions": {}
            }
        }
        
        with open(new_kb_path, 'w') as f:
            json.dump(fresh_kb, f, indent=2)
        
        print(f"✅ Created fresh knowledge base at: {new_kb_path}")
        return
    
    # Load existing knowledge base
    print(f"📄 Loading existing knowledge base...")
    with open(old_kb_path, 'r') as f:
        kb_data = json.load(f)
    
    # Backup original
    shutil.copy2(old_kb_path, backup_path)
    print(f"💾 Backup saved to: {backup_path}")
    
    # Separate system vs persona data
    system_data = {}
    persona_data = {
        "persona": "quenito",
        "migrated": datetime.now().isoformat(),
        "original_backup": backup_path
    }
    
    # Migrate persona-specific sections
    persona_sections = [
        'brain_learning',
        'survey_responses', 
        'user_responses',
        'demographics',
        'automation_history',
        'learning_session'
    ]
    
    system_sections = [
        'platform_patterns',
        'question_patterns',
        'ui_patterns',
        'system_config'
    ]
    
    for section in kb_data:
        if section in persona_sections:
            persona_data[section] = kb_data[section]
            print(f"  ➡️ Moving '{section}' to persona knowledge")
        elif section in system_sections:
            system_data[section] = kb_data[section]
            print(f"  📌 Keeping '{section}' in system data")
        else:
            # Default: move to persona
            persona_data[section] = kb_data[section]
            print(f"  ➡️ Moving '{section}' to persona (unclassified)")
    
    # Save migrated data
    os.makedirs("personas/quenito", exist_ok=True)
    
    # Save persona knowledge
    with open(new_kb_path, 'w') as f:
        json.dump(persona_data, f, indent=2)
    print(f"\n✅ Persona knowledge saved to: {new_kb_path}")
    
    # Update system knowledge base (keep for shared patterns)
    if system_data:
        system_kb_path = "data/system_knowledge.json"
        with open(system_kb_path, 'w') as f:
            json.dump(system_data, f, indent=2)
        print(f"✅ System patterns saved to: {system_kb_path}")
    
    # Remove old file
    os.remove(old_kb_path)
    print(f"🗑️ Removed old knowledge base")
    
    print("\n📊 Migration Summary:")
    print(f"  Persona data sections: {len([s for s in kb_data if s in persona_sections])}")
    print(f"  System data sections: {len([s for s in kb_data if s in system_sections])}")
    print(f"  Total sections migrated: {len(kb_data)}")

def update_knowledge_base_class():
    """Update KnowledgeBase class to use new persona structure"""
    
    print("\n🔧 Updating KnowledgeBase class...")
    
    kb_class_path = "data/knowledge_base.py"
    
    # Read current class
    with open(kb_class_path, 'r') as f:
        content = f.read()
    
    # Check if already updated
    if "personas/quenito/knowledge_base.json" in content:
        print("✅ KnowledgeBase class already updated!")
        return
    
    # Update the file path
    content = content.replace(
        'self.file_path = "data/knowledge_base.json"',
        'self.file_path = "personas/quenito/knowledge_base.json"'
    )
    
    # Backup and update
    backup_path = "data/knowledge_base_class_backup.py"
    shutil.copy2(kb_class_path, backup_path)
    
    with open(kb_class_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated KnowledgeBase class to use persona structure")
    print(f"💾 Backup saved to: {backup_path}")

def check_user_profile_usage():
    """Check if user_profile.py is still being used"""
    
    print("\n🔍 Checking user_profile.py usage...")
    
    # Search for imports of user_profile
    import_count = 0
    files_using_profile = []
    
    for root, dirs, files in os.walk("."):
        # Skip venv and git directories
        if "venv" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    if "user_profile" in content and filepath != "./data/user_profile.py":
                        import_count += 1
                        files_using_profile.append(filepath)
                except:
                    pass
    
    if import_count > 0:
        print(f"⚠️ user_profile.py is still used in {import_count} files:")
        for f in files_using_profile:
            print(f"   - {f}")
        print("💡 Consider updating these to use persona profiles instead")
    else:
        print("✅ user_profile.py is not used anywhere - safe to remove!")
        print("💡 Run: rm data/user_profile.py")

if __name__ == "__main__":
    print("🚀 QUENITO KNOWLEDGE MIGRATION TOOL")
    print("="*50)
    
    # Step 1: Migrate knowledge base
    migrate_knowledge_base()
    
    # Step 2: Update KnowledgeBase class
    update_knowledge_base_class()
    
    # Step 3: Check user_profile usage
    check_user_profile_usage()
    
    print("\n✅ MIGRATION COMPLETE!")
    print("\n📝 Next steps:")
    print("1. Review the migration results")
    print("2. Test with: python verify_learning_system.py")
    print("3. Run your first survey with: python quenito_survey_mvp.py")
    
    print("\n💡 The 'data/' folder now contains only system-wide components")
    print("💡 Quenito's personal knowledge is in 'personas/quenito/'")