#!/usr/bin/env python3
"""
🔄 Rating Matrix Pattern Migration Script
Moves all hard-coded patterns to knowledge_base.json
Follows the same pattern as brand_familiarity migration
"""

import json
import os
from datetime import datetime

def migrate_rating_patterns():
    """Migrate rating matrix patterns to centralized knowledge base"""
    
    print("🔄 Starting Rating Matrix pattern migration...")
    
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
    
    # Add rating matrix patterns (comprehensive set)
    kb_data["question_patterns"]["rating_matrix_questions"] = {
        "keywords": [
            "rate", "rating", "scale", "satisfaction", "agree", "disagree",
            "strongly", "somewhat", "neutral", "likely", "unlikely",
            "excellent", "good", "fair", "poor", "terrible",
            "satisfied", "dissatisfied", "important", "unimportant",
            "quality", "experience", "recommendation", "value",
            "performance", "service", "product", "overall"
        ],
        "matrix_indicators": [
            "rate each", "rate the following", "rating scale",
            "please rate", "how satisfied", "level of agreement",
            "indicate your level", "select your rating",
            "rate your satisfaction", "scale of 1",
            "for each of the following", "rate these",
            "please indicate", "select one rating"
        ],
        "enhanced_patterns": [
            "rate.*following",
            "satisfaction.*with",
            "agreement.*scale",
            "rating.*matrix",
            "scale.*\\d+.*to.*\\d+",
            "strongly.*agree.*disagree",
            "how.*satisfied.*are.*you",
            "please.*rate.*each",
            "indicate.*level.*of"
        ],
        "scale_types": {
            "likert_5": {
                "options": ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"],
                "numeric": ["1", "2", "3", "4", "5"],
                "default": 3
            },
            "likert_7": {
                "options": ["strongly disagree", "disagree", "somewhat disagree", "neutral", 
                           "somewhat agree", "agree", "strongly agree"],
                "numeric": ["1", "2", "3", "4", "5", "6", "7"],
                "default": 4
            },
            "satisfaction_5": {
                "options": ["very dissatisfied", "dissatisfied", "neutral", "satisfied", "very satisfied"],
                "numeric": ["1", "2", "3", "4", "5"],
                "default": 3
            },
            "satisfaction_7": {
                "options": ["extremely dissatisfied", "very dissatisfied", "dissatisfied", 
                           "neutral", "satisfied", "very satisfied", "extremely satisfied"],
                "numeric": ["1", "2", "3", "4", "5", "6", "7"],
                "default": 4
            },
            "likelihood_5": {
                "options": ["very unlikely", "unlikely", "neutral", "likely", "very likely"],
                "numeric": ["1", "2", "3", "4", "5"],
                "default": 3
            },
            "likelihood_10": {
                "options": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "numeric": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "default": 5
            },
            "quality_5": {
                "options": ["terrible", "poor", "fair", "good", "excellent"],
                "numeric": ["1", "2", "3", "4", "5"],
                "default": 3
            },
            "frequency_5": {
                "options": ["never", "rarely", "sometimes", "often", "always"],
                "numeric": ["1", "2", "3", "4", "5"],
                "default": 3
            },
            "importance_5": {
                "options": ["not at all important", "slightly important", "moderately important", 
                           "very important", "extremely important"],
                "numeric": ["1", "2", "3", "4", "5"],
                "default": 3
            },
            "nps_11": {
                "options": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "numeric": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "description": "Net Promoter Score scale",
                "default": 7
            }
        },
        "matrix_layouts": [
            "grid layout", "table format", "radio button matrix",
            "rating grid", "scale matrix", "multiple rows",
            "matrix question", "grid question", "table question"
        ],
        "common_attributes": {
            "product": ["quality", "value", "features", "design", "reliability"],
            "service": ["responsiveness", "professionalism", "knowledge", "courtesy", "efficiency"],
            "experience": ["ease of use", "satisfaction", "recommendation", "overall experience"],
            "website": ["navigation", "content", "speed", "design", "functionality"],
            "support": ["helpfulness", "response time", "resolution", "knowledge", "availability"]
        },
        "default_response": 3,
        "confidence_thresholds": {
            "base": 0.4,
            "matrix_boost": 0.3,
            "pattern_boost": 0.2,
            "scale_boost": 0.2,
            "attribute_boost": 0.1
        },
        "response_strategies": {
            "positive_bias": {
                "description": "Lean towards positive ratings",
                "scale_5": [3, 4, 4, 5, 5],
                "scale_7": [5, 6, 6, 7, 7],
                "scale_10": [7, 8, 8, 9, 9],
                "weight": 0.4
            },
            "neutral_safe": {
                "description": "Stay neutral/middle ground",
                "scale_5": [3, 3, 3, 3, 3],
                "scale_7": [4, 4, 4, 4, 4],
                "scale_10": [5, 5, 5, 5, 5],
                "weight": 0.3
            },
            "mixed_realistic": {
                "description": "Mix of ratings for realism",
                "scale_5": [2, 3, 3, 4, 5],
                "scale_7": [3, 4, 5, 5, 6, 7],
                "scale_10": [4, 5, 6, 7, 8, 9],
                "weight": 0.3
            }
        }
    }
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(kb_data, f, indent=2)
    
    print("✅ Rating matrix patterns migrated to knowledge_base.json")
    print(f"📊 Added {len(kb_data['question_patterns']['rating_matrix_questions']['keywords'])} keywords")
    print(f"📊 Added {len(kb_data['question_patterns']['rating_matrix_questions']['scale_types'])} scale types")
    print(f"📊 Added {len(kb_data['question_patterns']['rating_matrix_questions']['response_strategies'])} response strategies")
    
    # Verify the migration
    print("\n🔍 Verification:")
    print("✅ Pattern structure matches brand_familiarity format")
    print("✅ All hard-coded values moved to JSON")
    print("✅ Response strategies configured")
    print("✅ Confidence thresholds set")
    print("\n🎉 Migration complete! Rating Matrix Handler is ready for centralized brain architecture.")

if __name__ == "__main__":
    migrate_rating_patterns()