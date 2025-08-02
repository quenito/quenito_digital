#!/usr/bin/env python3
"""
🚀 Quenito Architecture Migration Script
Migrates existing structure to multi-persona scaling architecture
Respects existing folder structure and only adds what's needed
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class QuentioMigrator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.dry_run = True  # Set to False to actually perform migration
        
    def run(self):
        """Execute the migration"""
        print("🚀 Quenito Architecture Migration Tool")
        print("=" * 50)
        
        # Ask for confirmation
        response = input("Run in dry-run mode? (y/n) [y]: ").lower() or 'y'
        self.dry_run = response == 'y'
        
        if self.dry_run:
            print("\n📋 DRY RUN MODE - No changes will be made")
        else:
            print("\n⚡ LIVE MODE - Changes will be applied")
            confirm = input("Are you sure? (yes/no): ")
            if confirm != 'yes':
                print("Migration cancelled.")
                return
        
        print("\n" + "=" * 50)
        
        # Execute migration steps
        self.create_new_directories()
        self.organize_browser_profiles()
        self.split_knowledge_base()
        self.archive_old_content()
        self.create_config_files()
        
        print("\n✅ Migration complete!")
        if self.dry_run:
            print("Run with dry_run=False to apply changes")
    
    def create_new_directories(self):
        """Create new directories for scaling architecture"""
        print("\n📁 Creating new directories...")
        
        new_dirs = [
            # Platform adapters
            "platform_adapters",
            "platform_adapters/adapters",
            "platform_adapters/configs",
            
            # Personas
            "personas",
            "personas/quenito",
            "personas/quenita",
            "personas/shared",
            
            # Monitoring (separate from reporting)
            "monitoring",
            "monitoring/dashboard",
            "monitoring/analytics",
            
            # Scheduling
            "scheduling",
            
            # Archive
            "_archive",
            "_archive/old_tests",
            "_archive/old_reports",
            "_archive/old_code",
            "_archive/demos",
        ]
        
        for dir_path in new_dirs:
            if not os.path.exists(dir_path):
                if not self.dry_run:
                    os.makedirs(dir_path, exist_ok=True)
                print(f"  ✅ Create: {dir_path}")
            else:
                print(f"  ⏭️  Exists: {dir_path}")
    
    def organize_browser_profiles(self):
        """Organize browser profiles by persona and platform"""
        print("\n🌐 Organizing browser profiles...")
        
        persona_profiles = [
            "browser_profiles/quenito_myopinions",
            "browser_profiles/quenito_primeopinion",
            "browser_profiles/quenito_lifepointspanel",
            "browser_profiles/quenito_opinionworld",
            "browser_profiles/quenita_myopinions",
            "browser_profiles/quenita_primeopinion",
            "browser_profiles/quenita_lifepointspanel",
            "browser_profiles/quenita_opinionworld",
        ]
        
        for profile in persona_profiles:
            if not os.path.exists(profile):
                if not self.dry_run:
                    os.makedirs(profile, exist_ok=True)
                print(f"  ✅ Create: {profile}")
    
    def split_knowledge_base(self):
        """Split knowledge_base.json into persona-specific and shared"""
        print("\n🧠 Splitting knowledge base...")
        
        kb_path = "data/knowledge_base.json"
        
        if os.path.exists(kb_path):
            with open(kb_path, 'r') as f:
                kb = json.load(f)
            
            # Separate technical patterns from personal responses
            technical_patterns = {
                "ui_patterns": {},
                "element_selectors": {},
                "platform_patterns": {},
                "question_detection": {}
            }
            
            # Extract technical patterns (these are shared)
            for key in ["ui_patterns", "selectors", "patterns", "platform_specific"]:
                if key in kb:
                    technical_patterns[key] = kb[key]
            
            # Initial persona knowledge bases
            quenito_kb = {
                "demographics": {
                    "age": 34,
                    "gender": "male",
                    "location": "Sydney, NSW",
                    "postcode": "2000"
                },
                "response_patterns": {},
                "learned_responses": {}
            }
            
            quenita_kb = {
                "demographics": {
                    "age": 32,
                    "gender": "female",
                    "location": "Parramatta, NSW",
                    "postcode": "2150"
                },
                "response_patterns": {},
                "learned_responses": {}
            }
            
            # Save split knowledge bases
            files_to_create = [
                ("personas/shared/technical_patterns.json", technical_patterns),
                ("personas/quenito/knowledge_base.json", quenito_kb),
                ("personas/quenita/knowledge_base.json", quenita_kb),
            ]
            
            for file_path, content in files_to_create:
                if not self.dry_run:
                    with open(file_path, 'w') as f:
                        json.dump(content, f, indent=2)
                print(f"  ✅ Create: {file_path}")
            
            # Keep original as backup
            backup_path = f"data/knowledge_base_backup_{self.timestamp}.json"
            if not self.dry_run:
                shutil.copy2(kb_path, backup_path)
            print(f"  📋 Backup: {backup_path}")
        else:
            print("  ⚠️  No knowledge_base.json found in /data/")
    
    def archive_old_content(self):
        """Archive old test directories and demos"""
        print("\n📦 Archiving old content...")
        
        to_archive = [
            ("quenito_integration_test", "_archive/old_tests/"),
            ("quenito_test", "_archive/old_tests/"),
            ("test_integration_scripts", "_archive/old_tests/"),
            ("demos", "_archive/demos/"),
        ]
        
        # Archive old survey reports (keep last 5)
        survey_reports = [d for d in os.listdir('.') if d.startswith('survey_report_')]
        if len(survey_reports) > 5:
            survey_reports.sort()
            for report in survey_reports[:-5]:  # Keep last 5
                to_archive.append((report, "_archive/old_reports/"))
        
        for source, dest in to_archive:
            if os.path.exists(source):
                dest_path = os.path.join(dest, source)
                if not self.dry_run:
                    shutil.move(source, dest_path)
                print(f"  📦 Archive: {source} → {dest}")
            else:
                print(f"  ⏭️  Not found: {source}")
    
    def create_config_files(self):
        """Create initial configuration files"""
        print("\n⚙️  Creating configuration files...")
        
        # Platform adapter config
        platform_config = {
            "platforms": {
                "myopinions": {
                    "name": "MyOpinions Australia",
                    "url": "https://www.myopinions.com.au",
                    "points_per_dollar": 100,
                    "login_url": "/auth/login",
                    "dashboard_url": "/auth/dashboard"
                },
                "primeopinion": {
                    "name": "Prime Opinion",
                    "url": "https://app.primeopinion.com.au",
                    "points_per_dollar": 65,
                    "login_url": "/login",
                    "dashboard_url": "/surveys"
                }
            }
        }
        
        # Rotation schedule template
        rotation_schedule = {
            "week_template": {
                "monday": {
                    "quenito": ["myopinions", "lifepointspanel"],
                    "quenita": ["primeopinion", "opinionworld"]
                },
                "tuesday": {
                    "quenito": ["primeopinion", "opinionworld"],
                    "quenita": ["myopinions", "lifepointspanel"]
                },
                "wednesday": "REST_DAY",
                "thursday": {
                    "quenito": ["myopinions", "octopus"],
                    "quenita": ["primeopinion", "lifepointspanel"]
                },
                "friday": {
                    "quenito": ["lifepointspanel", "opinionworld"],
                    "quenita": ["myopinions", "octopus"]
                },
                "saturday": {
                    "quenito": ["myopinions"],
                    "quenita": "REST_DAY"
                },
                "sunday": {
                    "quenito": "REST_DAY",
                    "quenita": ["primeopinion"]
                }
            }
        }
        
        configs_to_create = [
            ("platform_adapters/configs/platforms.json", platform_config),
            ("scheduling/rotation_schedule.json", rotation_schedule),
        ]
        
        for file_path, content in configs_to_create:
            if not self.dry_run:
                with open(file_path, 'w') as f:
                    json.dump(content, f, indent=2)
            print(f"  ✅ Create: {file_path}")
    
    def create_readme(self):
        """Create README for new architecture"""
        readme_content = """# 🚀 Quenito Multi-Persona Architecture

## New Structure Overview

### 📁 platform_adapters/
Platform-specific navigation and automation logic

### 📁 personas/
Individual persona profiles and knowledge bases
- `quenito/` - Jack Chen's profile and responses
- `quenita/` - Emma Rodriguez's profile and responses  
- `shared/` - Technical patterns used by all personas

### 📁 monitoring/
Real-time dashboards and analytics (separate from reporting)

### 📁 scheduling/
Platform rotation and session scheduling logic

### 📁 _archive/
Old tests, demos, and legacy code

## Migration Complete! 

Your existing handlers, browser profiles, and core systems remain unchanged.
Only new scaling features have been added.
"""
        
        if not self.dry_run:
            with open("ARCHITECTURE.md", 'w') as f:
                f.write(readme_content)
        print("\n📄 Created ARCHITECTURE.md")


if __name__ == "__main__":
    migrator = QuentioMigrator()
    migrator.run()
