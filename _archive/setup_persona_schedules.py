# setup_persona_schedules.py
"""
Setup persona-specific schedule files while maintaining master coordination
"""

import json
import os
from datetime import datetime

def create_persona_schedules():
    """Create persona-specific schedule files"""
    
    print("📅 SETTING UP PERSONA SCHEDULES")
    print("="*50)
    
    # Quenito's schedule
    quenito_schedule = {
        "persona": "quenito",
        "created": datetime.now().isoformat(),
        "active_days": ["monday", "tuesday", "thursday", "friday", "saturday"],
        "preferred_platforms": [
            "myopinions",
            "lifepointspanel",
            "primeopinion",
            "opinionworld",
            "octopus"
        ],
        "platform_schedule": {
            "monday": ["myopinions", "lifepointspanel"],
            "tuesday": ["primeopinion", "opinionworld"],
            "thursday": ["myopinions", "octopus"],
            "friday": ["lifepointspanel", "opinionworld"],
            "saturday": ["myopinions"]
        },
        "preferred_time_slots": {
            "morning": "09:00-12:00",
            "evening": "19:00-21:00"
        },
        "survey_preferences": {
            "min_points": 50,
            "max_duration": "25 minutes",
            "avoid_topics": [],
            "preferred_topics": ["technology", "consumer_goods", "travel"]
        },
        "daily_limits": {
            "max_surveys": 3,
            "max_screen_time": "2 hours",
            "min_break_between": "30 minutes"
        },
        "platform_specific": {
            "myopinions": {
                "priority": "high",
                "daily_check": True,
                "bonus_tier_target": "gold"
            }
        }
    }
    
    # Quenita's schedule (placeholder for now)
    quenita_schedule = {
        "persona": "quenita",
        "created": datetime.now().isoformat(),
        "active_days": ["monday", "tuesday", "thursday", "friday", "sunday"],
        "preferred_platforms": [
            "primeopinion",
            "opinionworld",
            "myopinions",
            "lifepointspanel",
            "octopus"
        ],
        "platform_schedule": {
            "monday": ["primeopinion", "opinionworld"],
            "tuesday": ["myopinions", "lifepointspanel"],
            "thursday": ["primeopinion", "lifepointspanel"],
            "friday": ["myopinions", "octopus"],
            "sunday": ["primeopinion"]
        },
        "preferred_time_slots": {
            "afternoon": "14:00-17:00",
            "evening": "20:00-22:00"
        },
        "survey_preferences": {
            "min_points": 75,
            "max_duration": "20 minutes",
            "avoid_topics": [],
            "preferred_topics": ["lifestyle", "shopping", "health"]
        },
        "daily_limits": {
            "max_surveys": 2,
            "max_screen_time": "1.5 hours",
            "min_break_between": "45 minutes"
        },
        "platform_specific": {}
    }
    
    # Save Quenito's schedule
    os.makedirs("personas/quenito", exist_ok=True)
    with open("personas/quenito/schedule.json", 'w') as f:
        json.dump(quenito_schedule, f, indent=2)
    print("✅ Created personas/quenito/schedule.json")
    
    # Save Quenita's schedule (if directory exists)
    if os.path.exists("personas/quenita"):
        with open("personas/quenita/schedule.json", 'w') as f:
            json.dump(quenita_schedule, f, indent=2)
        print("✅ Created personas/quenita/schedule.json")
    else:
        print("📁 Quenita persona not set up yet - skipping")
    
    print("\n📊 Schedule Structure:")
    print("  Master: scheduling/rotation_schedule.json (coordination)")
    print("  Quenito: personas/quenito/schedule.json (preferences)")
    print("  Quenita: personas/quenita/schedule.json (preferences)")

def check_master_schedule():
    """Check if master rotation schedule exists"""
    
    print("\n🔍 Checking master rotation schedule...")
    
    if os.path.exists("scheduling/rotation_schedule.json"):
        with open("scheduling/rotation_schedule.json", 'r') as f:
            schedule = json.load(f)
        
        print("✅ Master schedule exists!")
        print(f"   Type: {schedule.get('schedule_type')}")
        print(f"   Active personas: {schedule.get('active_personas')}")
        
        # Count active days
        active_days = sum(1 for day in schedule.get('rotation_pattern', {}).values() if day.get('active'))
        print(f"   Active days per week: {active_days}")
    else:
        print("⚠️ No master schedule found at scheduling/rotation_schedule.json")
        print("💡 The master schedule coordinates which persona works on which day")

if __name__ == "__main__":
    create_persona_schedules()
    check_master_schedule()
    
    print("\n✅ SCHEDULE SETUP COMPLETE!")
    print("\n💡 How it works:")
    print("1. Master schedule (scheduling/) assigns personas to days")
    print("2. Each persona's schedule defines their preferences")  
    print("3. System checks both when running surveys")
    print("\nExample: On Monday, master schedule activates Quenito,")
    print("         then uses Quenito's preferences for platforms/timing")