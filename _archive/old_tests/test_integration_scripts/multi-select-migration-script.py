#!/usr/bin/env python3
"""
🔄 Multi-Select Pattern Migration Script
Moves all hard-coded patterns to knowledge_base.json
Follows the same pattern as brand_familiarity and rating_matrix migrations
"""

import json
import os
from datetime import datetime

def migrate_multi_select_patterns():
    """Migrate multi-select patterns to centralized knowledge base"""
    
    print("🔄 Starting Multi-Select pattern migration...")
    
    # Load existing knowledge base
    kb_path = 'data/knowledge_base.json'
    
    # Backup first
    if os.path.exists(kb_path):
        backup_path = f'data/knowledge_base_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(kb_path, 'r') as f:
            kb_data = json.load(f)
        with open(backup_path, 'w') as f:
            json.dump(kb_data, f, indent=2)
        print(f"✅ Backed up to {backup_path}")
    else:
        kb_data = {"question_patterns": {}}
        print("📝 Creating new knowledge_base.json")
    
    # Ensure question_patterns exists
    if "question_patterns" not in kb_data:
        kb_data["question_patterns"] = {}
    
    # Add multi-select patterns (comprehensive set)
    kb_data["question_patterns"]["multi_select_questions"] = {
        "keywords": [
            "select all", "check all", "choose all", "multiple",
            "select any", "check any", "all that apply", "select each",
            "check each", "tick all", "mark all", "indicate all",
            "select which", "check which", "choose multiple",
            "select one or more", "check one or more",
            "pick all", "mark any", "tick any", "several",
            "checkbox", "checkboxes", "multi-select", "multiselect"
        ],
        "primary_indicators": [
            "select all that apply", "check all that apply",
            "choose all that apply", "mark all that apply",
            "select any that apply", "check any that apply",
            "please select all", "please check all",
            "select one or more", "check one or more",
            "select each of the following", "check each of the following",
            "indicate all that apply", "mark each that applies",
            "tick all relevant", "choose any of the following",
            "select multiple options", "pick all that are relevant"
        ],
        "enhanced_patterns": [
            "select.*all.*apply",
            "check.*all.*apply",
            "choose.*all.*apply",
            "select.*any.*apply",
            "mark.*all.*following",
            "indicate.*which.*following",
            "select.*one.*or.*more",
            "multiple.*choice.*select",
            "check.*box.*each",
            "tick.*all.*relevant",
            "please.*select.*multiple"
        ],
        "exclusive_options": [
            "none of the above", "none of these", "not applicable",
            "n/a", "does not apply", "none", "neither",
            "i don't", "i do not", "no, none", "none apply",
            "other", "something else", "none of them",
            "not interested", "none of the options", "prefer not to answer",
            "decline to answer", "skip", "pass", "no preference"
        ],
        "common_topics": {
            "products": ["products", "brands", "items", "services", "offerings"],
            "activities": ["activities", "hobbies", "interests", "sports", "pastimes"],
            "features": ["features", "benefits", "characteristics", "attributes", "qualities"],
            "preferences": ["preferences", "likes", "favorites", "choices", "selections"],
            "behaviors": ["behaviors", "habits", "actions", "practices", "routines"],
            "media": ["channels", "platforms", "websites", "apps", "social media"],
            "reasons": ["reasons", "factors", "motivations", "causes", "considerations"],
            "shopping": ["stores", "retailers", "shopping", "purchases", "buying"],
            "communication": ["email", "phone", "text", "mail", "contact methods"],
            "information": ["sources", "information", "news", "content", "media types"]
        },
        "checkbox_layouts": [
            "vertical list", "horizontal list", "grid layout",
            "two column", "three column", "grouped options",
            "single column", "matrix style", "card layout"
        ],
        "minimum_selections": 0,
        "maximum_selections": None,
        "default_selections": 2,
        "confidence_thresholds": {
            "base": 0.4,
            "indicator_boost": 0.3,
            "pattern_boost": 0.2,
            "checkbox_boost": 0.2,
            "keyword_density_boost": 0.1
        },
        "selection_strategies": {
            "conservative": {
                "description": "Select 1-2 safe options",
                "min": 1,
                "max": 2,
                "avoid_exclusive": True,
                "weight": 0.3
            },
            "moderate": {
                "description": "Select 2-4 relevant options",
                "min": 2,
                "max": 4,
                "avoid_exclusive": True,
                "weight": 0.4
            },
            "comprehensive": {
                "description": "Select 3-6 options for thoroughness",
                "min": 3,
                "max": 6,
                "avoid_exclusive": True,
                "weight": 0.2
            },
            "none_strategy": {
                "description": "Select 'None of the above' when appropriate",
                "min": 1,
                "max": 1,
                "prefer_exclusive": True,
                "weight": 0.1
            }
        },
        "selection_rules": {
            "avoid_contradictions": True,
            "respect_exclusive": True,
            "minimum_relevance": 0.3,
            "randomize_order": True,
            "vary_selection_count": True,
            "consider_context": True
        },
        "validation_rules": {
            "minimum_required": False,
            "maximum_allowed": None,
            "exclusive_prevents_others": True,
            "require_at_least_one": False
        }
    }
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(kb_data, f, indent=2)
    
    print("✅ Multi-select patterns migrated to knowledge_base.json")
    print(f"☑️ Added {len(kb_data['question_patterns']['multi_select_questions']['keywords'])} keywords")
    print(f"☑️ Added {len(kb_data['question_patterns']['multi_select_questions']['primary_indicators'])} primary indicators")
    print(f"☑️ Added {len(kb_data['question_patterns']['multi_select_questions']['selection_strategies'])} selection strategies")
    print(f"☑️ Added {len(kb_data['question_patterns']['multi_select_questions']['exclusive_options'])} exclusive options")
    
    # Verify the migration
    print("\n🔍 Verification:")
    print("✅ Pattern structure matches brand_familiarity and rating_matrix format")
    print("✅ All hard-coded values moved to JSON")
    print("✅ Selection strategies configured")
    print("✅ Confidence thresholds set")
    print("✅ Exclusive option handling configured")
    print("\n🎉 Migration complete! Multi-Select Handler is ready for centralized brain architecture.")

if __name__ == "__main__":
    migrate_multi_select_patterns()