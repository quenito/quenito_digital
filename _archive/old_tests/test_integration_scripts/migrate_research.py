#!/usr/bin/env python3
"""
🔬 Research Required Pattern Migration Script
Adds research required patterns to knowledge_base.json
"""

import json
import os
from datetime import datetime

def migrate_research_patterns():
    """Add research required patterns to knowledge_base.json"""
    
    # Try multiple possible paths
    possible_paths = [
        'data/knowledge_base.json',
        './data/knowledge_base.json',
        '../data/knowledge_base.json',
        'knowledge_base.json',
        './knowledge_base.json'
    ]
    
    kb_path = None
    for path in possible_paths:
        if os.path.exists(path):
            kb_path = path
            print(f"✅ Found knowledge_base.json at: {path}")
            break
    
    if not kb_path:
        print("❌ Error: knowledge_base.json not found!")
        print("Searched in these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        print("\nPlease ensure you're running this script from the project root directory")
        print("Current directory:", os.getcwd())
        return False
    
    # Load existing knowledge base
    try:
        with open(kb_path, 'r') as f:
            knowledge_base = json.load(f)
    except Exception as e:
        print(f"❌ Error loading knowledge_base.json: {e}")
        return False
    
    # Define research required patterns
    research_patterns = {
        "research_required_questions": {
            "keywords": [
                "research", "look up", "search", "find information",
                "gather data", "investigate", "explore", "study",
                "review", "analyze", "examine", "check", "verify",
                "additional information", "more details", "further research"
            ],
            "primary_indicators": [
                "requires research", "needs research", "research required",
                "please research", "look up information", "search for",
                "find out about", "gather information", "investigate further",
                "requires additional information", "needs verification",
                "check the following", "verify information", "confirm details"
            ],
            "enhanced_patterns": [
                "research.*required",
                "needs?.*research",
                "look.*up.*information",
                "gather.*data",
                "find.*information",
                "search.*for.*details",
                "investigate.*further",
                "additional.*research",
                "verify.*information"
            ],
            "research_types": {
                "product": ["product research", "product information", "product details", "specifications"],
                "company": ["company research", "company information", "corporate data", "business info"],
                "market": ["market research", "market analysis", "industry research", "competitive analysis"],
                "technical": ["technical research", "technical specifications", "documentation", "technical details"],
                "general": ["general research", "background information", "contextual information", "overview"]
            },
            "action_keywords": {
                "search": ["search", "look up", "find", "locate", "discover"],
                "analyze": ["analyze", "examine", "study", "review", "assess"],
                "verify": ["verify", "confirm", "check", "validate", "authenticate"],
                "gather": ["gather", "collect", "compile", "accumulate", "assemble"]
            },
            "confidence_thresholds": {
                "base": 0.3,
                "indicator_boost": 0.4,
                "pattern_boost": 0.2,
                "keyword_boost": 0.1,
                "action_boost": 0.1
            },
            "response_strategies": {
                "acknowledge": {
                    "description": "Acknowledge research requirement",
                    "responses": [
                        "I understand this requires research",
                        "This needs additional investigation",
                        "Further research is needed",
                        "I'll need to gather more information"
                    ]
                },
                "skip": {
                    "description": "Skip if allowed",
                    "check_skip_option": True,
                    "skip_messages": [
                        "Skipping research question",
                        "Moving to next question",
                        "Research skipped"
                    ]
                },
                "placeholder": {
                    "description": "Provide placeholder response",
                    "responses": [
                        "Pending research",
                        "To be researched",
                        "Information to be gathered",
                        "Research in progress"
                    ]
                }
            },
            "ui_patterns": {
                "text_input": ["textarea", "input[type='text']", "text field"],
                "skip_button": ["skip", "next", "continue", "pass"],
                "submit_button": ["submit", "save", "continue", "next"]
            },
            "learning_indicators": {
                "successful_skip": "User successfully skipped research question",
                "placeholder_accepted": "Placeholder response was accepted",
                "manual_research": "User provided researched information"
            }
        }
    }
    
    # Add patterns to knowledge base
    if "question_patterns" not in knowledge_base:
        knowledge_base["question_patterns"] = {}
    
    # Backup existing file
    backup_path = f"{kb_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_path, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    print(f"✅ Backup created: {backup_path}")
    
    # Add research patterns
    knowledge_base["question_patterns"].update(research_patterns)
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    
    print("✅ Research required patterns added to knowledge_base.json")
    print(f"🔬 Added {len(research_patterns['research_required_questions']['keywords'])} keywords")
    print(f"🎯 Added {len(research_patterns['research_required_questions']['research_types'])} research types")
    print("🧠 Patterns are now centralized in the knowledge base!")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Research Required Pattern Migration...")
    if migrate_research_patterns():
        print("\n✨ Migration completed successfully!")
        print("📝 Next step: Create the modular handler structure")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
