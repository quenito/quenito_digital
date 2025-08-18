#!/usr/bin/env python3
"""
📊 Learning Dashboard v1.0
Real-time insights into Quenito's learning progress
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import statistics

class LearningDashboard:
    """Interactive dashboard for survey learning analytics"""
    
    def __init__(self, persona_name: str = "quenito"):
        self.persona_name = persona_name
        self.base_path = f"personas/{persona_name}"
        
        # Load all data sources
        self.learned_preferences = self._load_json("learned_preferences.json")
        self.visual_patterns = self._load_visual_patterns()
        self.session_reports = self._load_session_reports()
        
    def _load_json(self, filename: str) -> Dict:
        """Load JSON file safely"""
        filepath = os.path.join(self.base_path, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _load_visual_patterns(self) -> List[Dict]:
        """Load all visual patterns"""
        patterns = []
        pattern_dir = os.path.join(self.base_path, "visual_patterns")
        
        if os.path.exists(pattern_dir):
            for platform in os.listdir(pattern_dir):
                platform_dir = os.path.join(pattern_dir, platform)
                if os.path.isdir(platform_dir):
                    for file in os.listdir(platform_dir):
                        if file.endswith('.json'):
                            filepath = os.path.join(platform_dir, file)
                            try:
                                with open(filepath, 'r') as f:
                                    patterns.append(json.load(f))
                            except:
                                pass
        return patterns
    
    def _load_session_reports(self) -> List[Dict]:
        """Load all session reports"""
        reports = []
        report_dir = os.path.join(self.base_path, "reporting")
        
        if os.path.exists(report_dir):
            for file in os.listdir(report_dir):
                if file.startswith('session_') and file.endswith('.json'):
                    filepath = os.path.join(report_dir, file)
                    try:
                        with open(filepath, 'r') as f:
                            reports.append(json.load(f))
                    except:
                        pass
        
        return sorted(reports, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def generate_dashboard(self):
        """Generate complete dashboard output"""
        print("\n" + "="*80)
        print("📊 QUENITO LEARNING DASHBOARD")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Persona: {self.persona_name}")
        print("="*80)
        
        # 1. Overview Stats
        self._show_overview_stats()
        
        # 2. Learning Progress
        self._show_learning_progress()
        
        # 3. Question Type Analysis
        self._show_question_analysis()
        
        # 4. Brand Intelligence
        self._show_brand_intelligence()
        
        # 5. Success Patterns
        self._show_success_patterns()
        
        # 6. Recent Performance
        self._show_recent_performance()
        
        # 7. Optimization Suggestions
        self._show_optimization_suggestions()
        
        print("\n" + "="*80)
        print("📈 END OF DASHBOARD")
        print("="*80)
    
    def _show_overview_stats(self):
        """Show high-level statistics"""
        print("\n🎯 OVERVIEW STATS")
        print("-"*40)
        
        # Count learned patterns
        total_patterns = len(self.learned_preferences.get('question_patterns', {}))
        total_brands = len(self.learned_preferences.get('brand_responses', {}))
        total_successful = len(self.learned_preferences.get('successful_answers', []))
        total_visual = len(self.visual_patterns)
        total_sessions = len(self.session_reports)
        
        # Calculate automation rate
        automation_rates = []
        for report in self.session_reports:
            if 'automation_rate' in report:
                automation_rates.append(report['automation_rate'])
        
        avg_automation = statistics.mean(automation_rates) if automation_rates else 0
        
        print(f"📚 Learned Patterns: {total_patterns}")
        print(f"🏢 Known Brands: {total_brands}")
        print(f"✅ Successful Q&As: {total_successful}")
        print(f"👁️ Visual Patterns: {total_visual}")
        print(f"📋 Survey Sessions: {total_sessions}")
        print(f"🤖 Avg Automation Rate: {avg_automation:.1f}%")
        
        # Recent activity
        if self.learned_preferences.get('successful_answers'):
            recent = self.learned_preferences['successful_answers'][-1]
            recent_time = datetime.fromisoformat(recent['timestamp'])
            time_ago = datetime.now() - recent_time
            
            if time_ago.days == 0:
                time_str = f"{time_ago.seconds // 3600} hours ago"
            else:
                time_str = f"{time_ago.days} days ago"
            
            print(f"⏰ Last Learning: {time_str}")
    
    def _show_learning_progress(self):
        """Show learning progress over time"""
        print("\n📈 LEARNING PROGRESS")
        print("-"*40)
        
        # Group successful answers by day
        daily_learning = defaultdict(int)
        
        for answer in self.learned_preferences.get('successful_answers', []):
            timestamp = datetime.fromisoformat(answer['timestamp'])
            day = timestamp.strftime('%Y-%m-%d')
            daily_learning[day] += 1
        
        # Show last 7 days
        for i in range(7):
            day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            count = daily_learning.get(day, 0)
            bar = "█" * min(count, 20)
            print(f"{day}: {bar} {count}")
    
    def _show_question_analysis(self):
        """Analyze question types and responses"""
        print("\n❓ QUESTION TYPE ANALYSIS")
        print("-"*40)
        
        # Categorize questions
        question_types = Counter()
        response_patterns = defaultdict(list)
        
        for answer in self.learned_preferences.get('successful_answers', []):
            q = answer['question'].lower()
            a = answer['answer']
            
            # Categorize
            if any(word in q for word in ['age', 'old', 'birth']):
                qtype = "Demographics - Age"
            elif any(word in q for word in ['gender', 'male', 'female']):
                qtype = "Demographics - Gender"
            elif any(word in q for word in ['postcode', 'zip', 'postal']):
                qtype = "Demographics - Location"
            elif any(word in q for word in ['income', 'salary', 'earn']):
                qtype = "Demographics - Income"
            elif any(word in q for word in ['brand', 'familiar', 'heard']):
                qtype = "Brand Familiarity"
            elif any(word in q for word in ['agree', 'opinion', 'think']):
                qtype = "Opinion"
            elif any(word in q for word in ['often', 'frequency', 'times']):
                qtype = "Frequency"
            elif any(word in q for word in ['satisfied', 'satisfaction']):
                qtype = "Satisfaction"
            else:
                qtype = "Other"
            
            question_types[qtype] += 1
            response_patterns[qtype].append(a)
        
        # Show distribution
        for qtype, count in question_types.most_common():
            percentage = (count / sum(question_types.values()) * 100) if question_types else 0
            print(f"  {qtype}: {count} ({percentage:.1f}%)")
            
            # Show most common responses for this type
            if qtype in response_patterns:
                common_responses = Counter(response_patterns[qtype]).most_common(3)
                for response, resp_count in common_responses:
                    print(f"    → {response}: {resp_count}x")
    
    def _show_brand_intelligence(self):
        """Show brand familiarity patterns"""
        print("\n🏢 BRAND INTELLIGENCE")
        print("-"*40)
        
        brands = self.learned_preferences.get('brand_responses', {})
        
        if brands:
            print(f"Known Brands: {len(brands)}")
            
            # Group by familiarity level
            familiarity_groups = defaultdict(list)
            for brand, familiarity in brands.items():
                familiarity_groups[familiarity].append(brand)
            
            for level, brand_list in familiarity_groups.items():
                print(f"\n  {level}:")
                for brand in brand_list[:10]:  # Show first 10
                    print(f"    • {brand}")
                if len(brand_list) > 10:
                    print(f"    ... and {len(brand_list) - 10} more")
        else:
            print("  No brand data collected yet")
    
    def _show_success_patterns(self):
        """Show most successful response patterns"""
        print("\n✨ SUCCESS PATTERNS")
        print("-"*40)
        
        # Analyze visual patterns for high confidence
        high_confidence_patterns = []
        
        for pattern in self.visual_patterns:
            if pattern.get('confidence_rating', 0) > 90:
                high_confidence_patterns.append({
                    'type': pattern.get('question_type'),
                    'confidence': pattern.get('confidence_rating'),
                    'handler': pattern.get('handler_used')
                })
        
        if high_confidence_patterns:
            # Group by type
            by_type = defaultdict(list)
            for p in high_confidence_patterns:
                by_type[p['type']].append(p['confidence'])
            
            print("High Confidence Question Types:")
            for qtype, confidences in by_type.items():
                avg_conf = statistics.mean(confidences)
                print(f"  {qtype}: {avg_conf:.1f}% avg confidence ({len(confidences)} patterns)")
        
        # Show automation success by handler
        handler_success = defaultdict(lambda: {'success': 0, 'total': 0})
        
        for report in self.session_reports:
            if 'stats' in report:
                stats = report['stats']
                handler = stats.get('primary_handler', 'Unknown')
                handler_success[handler]['total'] += 1
                if stats.get('automation_rate', 0) > 80:
                    handler_success[handler]['success'] += 1
        
        print("\nHandler Performance:")
        for handler, stats in handler_success.items():
            if stats['total'] > 0:
                success_rate = (stats['success'] / stats['total']) * 100
                print(f"  {handler}: {success_rate:.1f}% success rate ({stats['total']} sessions)")
    
    def _show_recent_performance(self):
        """Show recent session performance"""
        print("\n📊 RECENT PERFORMANCE (Last 5 Sessions)")
        print("-"*40)
        
        for report in self.session_reports[:5]:
            timestamp = report.get('timestamp', 'Unknown')
            platform = report.get('platform', 'Unknown')
            automation_rate = report.get('automation_rate', 0)
            questions = report.get('stats', {}).get('questions_total', 0)
            
            # Parse timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = timestamp
            
            # Performance indicator
            if automation_rate >= 90:
                indicator = "🟢"
            elif automation_rate >= 70:
                indicator = "🟡"
            else:
                indicator = "🔴"
            
            print(f"{indicator} {time_str} | {platform:12} | {questions:3} Qs | {automation_rate:5.1f}% automated")
    
    def _show_optimization_suggestions(self):
        """Provide optimization suggestions based on data"""
        print("\n💡 OPTIMIZATION SUGGESTIONS")
        print("-"*40)
        
        suggestions = []
        
        # Check automation rate trend
        if self.session_reports:
            recent_rates = [r.get('automation_rate', 0) for r in self.session_reports[:5]]
            older_rates = [r.get('automation_rate', 0) for r in self.session_reports[5:10]]
            
            if recent_rates and older_rates:
                recent_avg = statistics.mean(recent_rates)
                older_avg = statistics.mean(older_rates)
                
                if recent_avg > older_avg + 5:
                    suggestions.append("✅ Great! Automation improving (+{:.1f}% recently)".format(recent_avg - older_avg))
                elif recent_avg < older_avg - 5:
                    suggestions.append("⚠️ Automation declining (-{:.1f}% recently)".format(older_avg - recent_avg))
        
        # Check for missing common patterns
        if len(self.learned_preferences.get('brand_responses', {})) < 10:
            suggestions.append("📝 Build brand database: Only {} brands learned".format(
                len(self.learned_preferences.get('brand_responses', {}))))
        
        # Check for question diversity
        question_types = set()
        for answer in self.learned_preferences.get('successful_answers', [])[-50:]:
            question_types.add(answer.get('type'))
        
        if len(question_types) < 5:
            suggestions.append("🎯 Limited question diversity: Focus on different survey types")
        
        # Success rate check
        if self.session_reports:
            low_automation = [r for r in self.session_reports if r.get('automation_rate', 0) < 70]
            if len(low_automation) > len(self.session_reports) * 0.3:
                suggestions.append("🔧 Review failed automations: {}% of sessions below 70%".format(
                    int(len(low_automation) / len(self.session_reports) * 100)))
        
        if suggestions:
            for suggestion in suggestions:
                print(f"  {suggestion}")
        else:
            print("  ✨ All systems optimal! Keep surveying!")
    
    def export_metrics(self, filepath: str = None):
        """Export dashboard metrics to JSON"""
        if not filepath:
            filepath = f"{self.base_path}/dashboard_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        metrics = {
            "generated": datetime.now().isoformat(),
            "persona": self.persona_name,
            "total_learned_patterns": len(self.learned_preferences.get('question_patterns', {})),
            "total_brands": len(self.learned_preferences.get('brand_responses', {})),
            "total_successful_qa": len(self.learned_preferences.get('successful_answers', [])),
            "total_visual_patterns": len(self.visual_patterns),
            "total_sessions": len(self.session_reports),
            "recent_sessions": self.session_reports[:10]
        }
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"\n💾 Metrics exported to: {filepath}")


# Quick launch script
if __name__ == "__main__":
    dashboard = LearningDashboard(persona_name="quenito")
    dashboard.generate_dashboard()
    
    # Optionally export
    export = input("\nExport metrics to file? (y/n): ")
    if export.lower() == 'y':
        dashboard.export_metrics()