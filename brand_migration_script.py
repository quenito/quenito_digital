#!/usr/bin/env python3
"""
🔄 Brand Familiarity Pattern Migration Script
Migrates hard-coded patterns to centralized knowledge_base.json
"""

import json
import os
from datetime import datetime


def migrate_brand_patterns():
    """Migrate brand familiarity patterns to knowledge base"""
    
    print("🔄 Starting brand familiarity pattern migration...")
    
    # Load existing knowledge base
    kb_path = "data/knowledge_base.json"
    
    try:
        with open(kb_path, 'r') as f:
            knowledge_base = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {kb_path} not found!")
        return False
    
    # Backup current file
    backup_path = f"data/knowledge_base_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_path, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    print(f"✅ Backup created: {backup_path}")
    
    # Define brand familiarity patterns
    brand_patterns = {
        "keywords": [
            "familiar", "brand", "heard of", "currently use", 
            "aware of", "recognize", "know", "experience with", 
            "used before", "awareness", "familiarity"
        ],
        "matrix_indicators": [
            "how familiar are you with",
            "rate your familiarity",
            "please indicate your familiarity",
            "familiarity with these brands",
            "which of these brands",
            "brand awareness",
            "rate each brand",
            "for each brand"
        ],
        "enhanced_patterns": [
            "familiar.*with.*brands?",
            "brand.*familiar",
            "heard.*of.*brand",
            "aware.*of.*these",
            "recognize.*brand",
            "experience.*with.*brand",
            "used.*these.*brands",
            "know.*about.*brands"
        ],
        "response_levels": {
            "very_familiar": [
                "very familiar", "extremely familiar", "highly familiar", 
                "know very well", "use regularly", "definitely know"
            ],
            "somewhat_familiar": [
                "somewhat familiar", "moderately familiar", "familiar", 
                "heard of", "know of", "aware of", "recognize"
            ],
            "not_familiar": [
                "not familiar", "slightly familiar", "barely familiar", 
                "not very familiar", "limited familiarity", "vaguely familiar"
            ],
            "never_heard": [
                "never heard", "not heard of", "unknown", "unfamiliar", 
                "don't know", "no familiarity", "completely unfamiliar"
            ]
        },
        "matrix_layouts": [
            "radio button matrix", "grid layout", "multiple rows",
            "rate each", "for each brand", "each of the following",
            "matrix-table", "brand-grid", "familiarity-matrix"
        ],
        "common_brands": {
            "technology": [
                "apple", "samsung", "microsoft", "google", "sony", 
                "dell", "hp", "lenovo", "asus", "lg", "intel", 
                "amd", "nvidia", "ibm", "oracle", "adobe"
            ],
            "sports": [
                "nike", "adidas", "puma", "reebok", "under armour", 
                "new balance", "asics", "converse", "vans", "fila",
                "champion", "sketchers", "brooks", "mizuno"
            ],
            "food": [
                "coca-cola", "pepsi", "mcdonald's", "kfc", "subway", 
                "starbucks", "nestle", "kraft", "kellogg's", "general mills",
                "domino's", "pizza hut", "burger king", "wendy's", "taco bell"
            ],
            "automotive": [
                "toyota", "ford", "chevrolet", "honda", "nissan", 
                "bmw", "mercedes", "volkswagen", "audi", "mazda",
                "hyundai", "kia", "subaru", "tesla", "volvo"
            ],
            "retail": [
                "walmart", "target", "amazon", "costco", "kroger", 
                "walgreens", "cvs", "home depot", "lowe's", "best buy",
                "macy's", "nordstrom", "kohl's", "tjmaxx", "ross"
            ],
            "finance": [
                "visa", "mastercard", "american express", "paypal", 
                "chase", "bank of america", "wells fargo", "citi",
                "capital one", "discover", "square", "stripe"
            ],
            "fashion": [
                "zara", "h&m", "gap", "old navy", "forever 21",
                "uniqlo", "gucci", "louis vuitton", "chanel", "prada",
                "ralph lauren", "tommy hilfiger", "calvin klein"
            ],
            "entertainment": [
                "netflix", "disney", "hulu", "amazon prime", "hbo",
                "spotify", "apple music", "youtube", "twitch", "tiktok",
                "facebook", "instagram", "twitter", "snapchat"
            ]
        },
        "default_response": "somewhat_familiar",
        "confidence_thresholds": {
            "base": 0.4,
            "matrix_boost": 0.3,
            "pattern_boost": 0.2,
            "option_boost": 0.2,
            "brand_count_boost": 0.1
        },
        "strategy_settings": {
            "variety_ratios": {
                "very_familiar": 0.2,
                "somewhat_familiar": 0.5,
                "not_familiar": 0.2,
                "never_heard": 0.1
            },
            "category_preferences": {
                "high_interest": "very_familiar",
                "medium_interest": "somewhat_familiar",
                "low_interest": "not_familiar"
            }
        }
    }
    
    # Add to knowledge base
    if "question_patterns" not in knowledge_base:
        knowledge_base["question_patterns"] = {}
    
    # Update brand familiarity patterns
    knowledge_base["question_patterns"]["brand_familiarity_questions"] = brand_patterns
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    
    print("✅ Brand familiarity patterns added to knowledge base")
    
    # Verify the update
    print("\n📊 Migration Summary:")
    print(f"   - Keywords: {len(brand_patterns['keywords'])}")
    print(f"   - Matrix indicators: {len(brand_patterns['matrix_indicators'])}")
    print(f"   - Response levels: {len(brand_patterns['response_levels'])}")
    print(f"   - Brand categories: {len(brand_patterns['common_brands'])}")
    
    total_brands = sum(len(brands) for brands in brand_patterns['common_brands'].values())
    print(f"   - Total brands: {total_brands}")
    
    return True


if __name__ == "__main__":
    success = migrate_brand_patterns()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("\n🎯 Next steps:")
        print("1. Create handlers/brand_familiarity/ directory")
        print("2. Add the 4 new module files")
        print("3. Update imports in handler_factory.py")
        print("4. Test the refactored handler")
    else:
        print("\n❌ Migration failed!")