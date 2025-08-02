#!/usr/bin/env python3
"""
⏰ Recency Activities Pattern Migration Script
Adds recency activities patterns to knowledge_base.json
"""

import json
import os
from datetime import datetime

def migrate_recency_patterns():
    """Add recency activities patterns to knowledge_base.json"""
    
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
    
    # Define recency activities patterns
    recency_patterns = {
        "recency_activities_questions": {
            "keywords": [
                "last 12 months", "past year", "activities", "things you have done",
                "recent", "recently", "past 12 months", "last year", "within the year",
                "in the past year", "over the past year", "during the last year",
                "this year", "current year", "previous 12 months", "preceding year"
            ],
            "primary_indicators": [
                "in the last 12 months", "during the past year",
                "over the last 12 months", "within the past 12 months",
                "things you have done in the last 12 months",
                "activities you have done in the past year",
                "which of the following have you done",
                "select all that you have done",
                "indicate which activities", "mark all activities"
            ],
            "enhanced_patterns": [
                "last.*12.*months",
                "past.*year",
                "recent.*activities",
                "done.*in.*the.*last",
                "within.*past.*year",
                "during.*last.*12",
                "activities.*past.*months"
            ],
            "time_frames": {
                "last_month": ["last month", "past month", "in the last month", "previous month"],
                "last_3_months": ["last 3 months", "past 3 months", "last three months", "past three months"],
                "last_6_months": ["last 6 months", "past 6 months", "last six months", "past six months"],
                "last_year": ["last year", "past year", "last 12 months", "past 12 months"],
                "last_2_years": ["last 2 years", "past 2 years", "last two years", "past two years"]
            },
            "activity_categories": {
                "shopping": [
                    "purchased", "bought", "shopped", "ordered online",
                    "visited a store", "made a purchase", "shopping"
                ],
                "travel": [
                    "traveled", "flew", "visited", "vacation", "trip",
                    "stayed at hotel", "booked travel", "went abroad"
                ],
                "entertainment": [
                    "watched movie", "attended concert", "went to theater",
                    "streaming service", "sports event", "live show"
                ],
                "dining": [
                    "restaurant", "dined out", "ordered takeout", "food delivery",
                    "fast food", "coffee shop", "ate at"
                ],
                "health": [
                    "doctor visit", "medical appointment", "health checkup",
                    "dental visit", "pharmacy", "prescription", "vaccination"
                ],
                "finance": [
                    "opened account", "applied for credit", "loan application",
                    "investment", "insurance", "banking", "financial service"
                ],
                "technology": [
                    "bought device", "upgraded phone", "new computer",
                    "software purchase", "app download", "tech support"
                ],
                "home": [
                    "home improvement", "renovation", "moved", "relocated",
                    "furniture purchase", "appliance", "decoration"
                ]
            },
            "common_activities": [
                "Made an online purchase",
                "Visited a retail store",
                "Traveled by airplane",
                "Stayed at a hotel",
                "Dined at a restaurant",
                "Ordered food delivery",
                "Watched a movie in theater",
                "Attended a live event",
                "Visited a doctor",
                "Got a haircut",
                "Joined a gym",
                "Started a subscription",
                "Bought a car",
                "Moved to a new home",
                "Changed jobs",
                "None of the above"
            ],
            "confidence_thresholds": {
                "base": 0.4,
                "indicator_boost": 0.3,
                "pattern_boost": 0.2,
                "timeframe_boost": 0.2,
                "activity_boost": 0.1
            },
            "selection_strategies": {
                "conservative": {
                    "description": "Select 2-4 common activities",
                    "min": 2,
                    "max": 4,
                    "prefer_common": True,
                    "avoid_major": True
                },
                "moderate": {
                    "description": "Select 4-7 realistic activities",
                    "min": 4,
                    "max": 7,
                    "mix_categories": True,
                    "include_common": True
                },
                "active": {
                    "description": "Select 6-10 diverse activities",
                    "min": 6,
                    "max": 10,
                    "diverse_categories": True,
                    "include_seasonal": True
                }
            },
            "seasonal_considerations": {
                "summer": ["vacation", "travel", "outdoor activities"],
                "winter": ["holiday shopping", "winter sports", "indoor activities"],
                "spring": ["home improvement", "gardening", "spring cleaning"],
                "fall": ["back to school", "fall activities", "holiday prep"]
            },
            "response_logic": {
                "avoid_contradictions": True,
                "consider_demographics": True,
                "match_lifestyle": True,
                "seasonal_appropriate": True
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
    
    # Add recency patterns
    knowledge_base["question_patterns"].update(recency_patterns)
    
    # Save updated knowledge base
    with open(kb_path, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    
    print("✅ Recency activities patterns added to knowledge_base.json")
    print(f"⏰ Added {len(recency_patterns['recency_activities_questions']['keywords'])} keywords")
    print(f"🎯 Added {len(recency_patterns['recency_activities_questions']['activity_categories'])} activity categories")
    print("🧠 Patterns are now centralized in the knowledge base!")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Recency Activities Pattern Migration...")
    if migrate_recency_patterns():
        print("\n✨ Migration completed successfully!")
        print("📝 Next step: Create the modular handler structure")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")