#!/usr/bin/env python3
"""
🧠 QUENITO MILESTONE UPDATER
Tracks the evolution from mechanical parts to digital brain
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class MilestoneTracker:
    """
    Tracks Quenito's evolution milestones
    """
    
    def __init__(self):
        self.milestone_file = "company_docs/quenito_milestones.json"
        self.milestones = self.load_milestones()
    
    def load_milestones(self) -> Dict:
        """Load existing milestones or create new"""
        if os.path.exists(self.milestone_file):
            with open(self.milestone_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "created": datetime.now().isoformat(),
                "current_stats": {
                    "automation_rate": 41,
                    "handlers_active": 15,
                    "patterns_learned": 29,
                    "intelligence_score": 2.7
                },
                "handler_removals": [],
                "milestones_achieved": [],
                "weekly_metrics": []
            }
    
    def save_milestones(self):
        """Save milestones to file"""
        os.makedirs(os.path.dirname(self.milestone_file), exist_ok=True)
        with open(self.milestone_file, 'w') as f:
            json.dump(self.milestones, f, indent=2)
        print(f"✅ Milestones saved to {self.milestone_file}")
    
    def remove_handler(self, handler_name: str, new_automation_rate: float, 
                       commit_hash: str = None, notes: str = ""):
        """
        Record a handler removal milestone
        """
        removal = {
            "timestamp": datetime.now().isoformat(),
            "handler": handler_name,
            "old_rate": self.milestones["current_stats"]["automation_rate"],
            "new_rate": new_automation_rate,
            "improvement": new_automation_rate - self.milestones["current_stats"]["automation_rate"],
            "commit_hash": commit_hash,
            "notes": notes
        }
        
        self.milestones["handler_removals"].append(removal)
        self.milestones["current_stats"]["automation_rate"] = new_automation_rate
        self.milestones["current_stats"]["handlers_active"] -= 1
        
        # Generate celebration message
        self.celebrate_removal(handler_name, new_automation_rate)
        
        # Check for major milestones
        self.check_milestones(new_automation_rate)
        
        self.save_milestones()
    
    def celebrate_removal(self, handler: str, rate: float):
        """
        Generate celebration message for handler removal
        """
        messages = {
            "demographics_handler": "🎓 Quenito knows who he is!",
            "rating_handler": "🧠 Quenito has real opinions!",
            "brand_selection_handler": "👁️ Quenito recognizes patterns!",
            "multi_question_handler": "🏗️ Quenito sees structure!",
            "carousel_handler": "🎨 Quenito understands UI!",
            "brand_association_handler": "🔗 Quenito grasps relationships!"
        }
        
        print("\n" + "="*60)
        print("🎉 HANDLER REMOVED!")
        print("="*60)
        print(f"📦 Handler: {handler}")
        print(f"📈 New Rate: {rate}%")
        print(f"💬 {messages.get(handler, 'Another step toward pure intelligence!')}")
        print("="*60)
        
        # Generate git commit command
        commit_msg = f"🎓 MILESTONE: Removed {handler} - {rate}% automation"
        print(f"\n📝 Git commit command:")
        print(f"git add -A && git commit -m \"{commit_msg}\"")
    
    def check_milestones(self, rate: float):
        """
        Check if we hit major milestones
        """
        major_milestones = [50, 75, 85, 90, 95]
        
        for milestone in major_milestones:
            if rate >= milestone and not self.is_milestone_achieved(milestone):
                self.achieve_milestone(milestone)
    
    def is_milestone_achieved(self, milestone: int) -> bool:
        """
        Check if milestone already achieved
        """
        for m in self.milestones["milestones_achieved"]:
            if m["milestone"] == milestone:
                return True
        return False
    
    def achieve_milestone(self, milestone: int):
        """
        Record major milestone achievement
        """
        achievement = {
            "timestamp": datetime.now().isoformat(),
            "milestone": milestone,
            "handlers_remaining": self.milestones["current_stats"]["handlers_active"]
        }
        
        self.milestones["milestones_achieved"].append(achievement)
        
        print("\n" + "🌟"*30)
        print(f"   🏆 MAJOR MILESTONE: {milestone}% AUTOMATION!")
        print("🌟"*30)
        
        if milestone == 95:
            print("   🚀 QUENITO IS ALMOST HANDLER-FREE!")
    
    def weekly_update(self, automation_rate: float, patterns_learned: int, 
                     avg_confidence: float):
        """
        Record weekly metrics
        """
        week_data = {
            "week": len(self.milestones["weekly_metrics"]) + 1,
            "date": datetime.now().isoformat(),
            "automation_rate": automation_rate,
            "handlers_active": self.milestones["current_stats"]["handlers_active"],
            "patterns_learned": patterns_learned,
            "avg_confidence": avg_confidence,
            "intelligence_score": self.calculate_intelligence_score(
                automation_rate, patterns_learned, avg_confidence
            )
        }
        
        self.milestones["weekly_metrics"].append(week_data)
        self.milestones["current_stats"]["patterns_learned"] = patterns_learned
        self.milestones["current_stats"]["intelligence_score"] = week_data["intelligence_score"]
        
        self.save_milestones()
        self.print_weekly_report(week_data)
    
    def calculate_intelligence_score(self, automation: float, patterns: int, 
                                    confidence: float) -> float:
        """
        Calculate intelligence score (0-10)
        """
        # Weighted formula
        auto_score = (automation / 100) * 5  # 50% weight
        pattern_score = min(patterns / 100, 1) * 3  # 30% weight
        conf_score = confidence * 2  # 20% weight
        
        return round(auto_score + pattern_score + conf_score, 1)
    
    def print_weekly_report(self, week_data: Dict):
        """
        Print weekly progress report
        """
        print("\n" + "="*60)
        print(f"📊 WEEK {week_data['week']} REPORT")
        print("="*60)
        print(f"📈 Automation Rate: {week_data['automation_rate']}%")
        print(f"📦 Handlers Active: {week_data['handlers_active']}")
        print(f"🧠 Patterns Learned: {week_data['patterns_learned']}")
        print(f"💪 Avg Confidence: {week_data['avg_confidence']:.2f}")
        print(f"⭐ Intelligence Score: {week_data['intelligence_score']}/10")
        print("="*60)
    
    def countdown_to_freedom(self):
        """
        Show countdown to handler-free state
        """
        handlers_left = self.milestones["current_stats"]["handlers_active"]
        target_date = datetime(2025, 11, 15)
        days_left = (target_date - datetime.now()).days
        
        print("\n" + "🎯"*30)
        print("   COUNTDOWN TO HANDLER-FREE QUENITO")
        print("🎯"*30)
        print(f"   📦 Handlers Remaining: {handlers_left}")
        print(f"   📅 Days Until Target: {days_left}")
        print(f"   📈 Current Automation: {self.milestones['current_stats']['automation_rate']}%")
        print(f"   🎯 Target Automation: 95%+")
        print("🎯"*30)


def main():
    """
    Interactive milestone updater
    """
    tracker = MilestoneTracker()
    
    print("\n🧠 QUENITO MILESTONE TRACKER")
    print("="*40)
    print("1. Remove a handler")
    print("2. Weekly update")
    print("3. View countdown")
    print("4. Exit")
    print("="*40)
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        handler = input("Handler name (e.g., demographics_handler): ")
        rate = float(input("New automation rate (%): "))
        commit = input("Commit hash (optional): ") or None
        notes = input("Notes (optional): ") or ""
        
        tracker.remove_handler(handler, rate, commit, notes)
        
    elif choice == "2":
        rate = float(input("Current automation rate (%): "))
        patterns = int(input("Total patterns learned: "))
        confidence = float(input("Average confidence (0-1): "))
        
        tracker.weekly_update(rate, patterns, confidence)
        
    elif choice == "3":
        tracker.countdown_to_freedom()
    
    print("\n✅ Update complete!")


if __name__ == "__main__":
    main()