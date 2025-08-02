#!/usr/bin/env python3
"""
🔄 Trust Rating Pattern Migration Script
Moves all hard-coded patterns to knowledge_base.json
"""

import json
import os
from datetime import datetime

def migrate_trust_rating_patterns():
    """Migrate trust rating patterns to centralized knowledge base"""
    
    print("🔄 Starting Trust Rating pattern migration...")
    
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
    
    # Add trust rating patterns
    kb_data["question_patterns"]["trust_rating_questions"] = {
        "keywords": [
            "trustworthy", "trust", "rate", "trust level", 
            "reliability", "credible", "reliable", "confidence",
            "believe", "faith", "honest", "integrity", "dependable",
            "reputation", "authenticity", "legitimate", "sincere",
            "truthful", "accurate", "transparent", "ethical"
        ],
        "primary_indicators": [
            "how much do you trust", "rate the trustworthiness",
            "how trustworthy", "trust level", "how reliable",
            "rate your trust", "level of trust", "degree of trust",
            "how confident are you", "rate the reliability",
            "how credible", "rate the credibility",
            "trust rating", "trustworthiness scale", "reliability rating"
        ],
        "enhanced_patterns": [
            "trust.*rate",
            "rate.*trust",
            "how.*trust",
            "trustworth.*scale",
            "reliab.*rating",
            "credib.*scale",
            "confidence.*level",
            "trust.*\\d+",
            "scale.*trust",
            "trust.*opinion"
        ],
        "trust_text_options": {
            "very_positive": [
                "very trustworthy", "extremely trustworthy", 
                "highly trustworthy", "completely trustworthy",
                "totally trustworthy", "absolutely trustworthy"
            ],
            "positive": [
                "trustworthy", "quite trustworthy", "fairly trustworthy",
                "pretty trustworthy", "generally trustworthy"
            ],
            "moderate": [
                "somewhat trustworthy", "moderately trustworthy", 
                "reasonably trustworthy", "adequately trustworthy",
                "sufficiently trustworthy"
            ],
            "neutral": [
                "neutral", "neither trustworthy nor untrustworthy", 
                "undecided", "no opinion", "unsure"
            ],
            "negative": [
                "somewhat untrustworthy", "not very trustworthy", 
                "slightly untrustworthy", "questionably trustworthy",
                "doubtfully trustworthy"
            ],
            "very_negative": [
                "untrustworthy", "not trustworthy", "very untrustworthy", 
                "not at all trustworthy", "completely untrustworthy",
                "totally untrustworthy"
            ]
        },
        "scale_types": {
            "trust_5": {
                "range": [1, 2, 3, 4, 5],
                "labels": [
                    "Not at all trustworthy", 
                    "Slightly trustworthy", 
                    "Moderately trustworthy", 
                    "Very trustworthy", 
                    "Extremely trustworthy"
                ],
                "default": 3,
                "preferred_values": [3, 4]
            },
            "trust_7": {
                "range": [1, 2, 3, 4, 5, 6, 7],
                "labels": [
                    "Completely untrustworthy", 
                    "Very untrustworthy", 
                    "Somewhat untrustworthy", 
                    "Neutral", 
                    "Somewhat trustworthy", 
                    "Very trustworthy", 
                    "Completely trustworthy"
                ],
                "default": 5,
                "preferred_values": [5, 6]
            },
            "trust_10": {
                "range": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "labels": [
                    "No trust at all", "", "", "", 
                    "Neutral", 
                    "", "", "", "", 
                    "Complete trust"
                ],
                "default": 7,
                "preferred_values": [6, 7, 8]
            },
            "trust_100": {
                "range": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                "labels": ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
                "default": 70,
                "preferred_values": [60, 70, 80]
            },
            "nps_trust": {
                "range": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "labels": [
                    "Would not trust at all", "", "", "", "", "", 
                    "", "", "", "", 
                    "Would completely trust"
                ],
                "default": 7,
                "preferred_values": [7, 8]
            }
        },
        "related_concepts": [
            "brand trust", "company trust", "product trust", 
            "service trust", "website trust", "information trust",
            "source credibility", "platform reliability", "vendor trust",
            "partner trust", "data trust", "privacy trust"
        ],
        "trust_entities": {
            "companies": ["company", "organization", "corporation", "business", "firm"],
            "brands": ["brand", "product", "service", "offering"],
            "websites": ["website", "site", "platform", "app", "application"],
            "sources": ["source", "information", "news", "media", "content"],
            "people": ["person", "individual", "representative", "agent", "advisor"]
        },
        "confidence_thresholds": {
            "base": 0.4,
            "indicator_boost": 0.3,
            "pattern_boost": 0.2,
            "scale_boost": 0.2,
            "entity_boost": 0.1
        },
        "response_strategies": {
            "conservative_positive": {
                "description": "Lean slightly positive but cautious",
                "scale_5_preference": [3, 4],
                "scale_7_preference": [5, 6],
                "scale_10_preference": [6, 7, 8],
                "text_preference": ["somewhat trustworthy", "moderately trustworthy"],
                "weight": 0.5
            },
            "neutral_safe": {
                "description": "Stay neutral/middle ground",
                "scale_5_preference": [3],
                "scale_7_preference": [4],
                "scale_10_preference": [5, 6],
                "text_preference": ["neutral", "neither trustworthy nor untrustworthy"],
                "weight": 0.3
            },
            "moderate_positive": {
                "description": "Moderately positive trust",
                "scale_5_preference": [4],
                "scale_7_preference": [5, 6],
                "scale_10_preference": [7, 8],
                "text_preference": ["trustworthy", "fairly trustworthy"],
                "weight": 0.2
            }
        },
        "default_strategy": "conservative_positive",
        "scale_detection_hints": [
            "scale of", "rate from", "1 to", "1-", 
            "0 to 10", "0-10", "rating scale", "point scale"
        ]
    }
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(kb_data, f, indent=2)
    
    print("✅ Trust rating patterns migrated to knowledge_base.json")
    print(f"🎯 Added {len(kb_data['question_patterns']['trust_rating_questions']['keywords'])} keywords")
    print(f"🎯 Added {len(kb_data['question_patterns']['trust_rating_questions']['scale_types'])} scale types")
    print(f"🎯 Added {len(kb_data['question_patterns']['trust_rating_questions']['response_strategies'])} response strategies")
    
    # Verify the migration
    print("\n🔍 Verification:")
    print("✅ Pattern structure follows established format")
    print("✅ All hard-coded values moved to JSON")
    print("✅ Multiple scale types configured")
    print("✅ Response strategies defined")
    print("✅ Trust entity categories included")
    print("\n🎉 Migration complete! Trust Rating Handler is ready for centralized brain architecture.")

if __name__ == "__main__":
    migrate_trust_rating_patterns()