# consciousness_tracker.py
"""
Track and analyze consciousness engine performance over time
"""

import json
import os
from datetime import datetime
from typing import List, Dict
import statistics

class ConsciousnessTracker:
    def __init__(self, reports_dir="test_reports"):
        self.reports_dir = reports_dir
        self.temperature_tests = {}
        self.question_patterns = {}
        
    def load_all_reports(self) -> List[Dict]:
        """Load all test reports from directory"""
        reports = []
        if not os.path.exists(self.reports_dir):
            return reports
            
        for filename in os.listdir(self.reports_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.reports_dir, filename), 'r') as f:
                    reports.append(json.load(f))
        
        return sorted(reports, key=lambda x: x['session']['start_time'])
    
    def analyze_confidence_trends(self, reports: List[Dict]):
        """Analyze confidence trends over time"""
        print("\n📈 CONFIDENCE TRENDS ANALYSIS")
        print("="*60)
        
        if not reports:
            print("No reports found")
            return
        
        for report in reports:
            session_id = report['session']['session_id']
            avg_conf = report['summary'].get('avg_confidence', 0)
            total_tests = report['summary']['total_tests']
            
            print(f"Session {session_id}: {avg_conf:.0%} ({total_tests} tests)")
        
        # Overall statistics
        all_confidences = []
        for report in reports:
            for test in report.get('tests', []):
                all_confidences.append(test['confidence'])
        
        if all_confidences:
            print(f"\nOverall Statistics:")
            print(f"  Mean confidence: {statistics.mean(all_confidences):.0%}")
            print(f"  Median confidence: {statistics.median(all_confidences):.0%}")
            if len(all_confidences) > 1:
                print(f"  Std deviation: {statistics.stdev(all_confidences):.2%}")
    
    def analyze_question_types(self, reports: List[Dict]):
        """Analyze performance by question type"""
        print("\n📊 QUESTION TYPE ANALYSIS")
        print("="*60)
        
        question_stats = {}
        
        for report in reports:
            for test in report.get('tests', []):
                question = test['question'][:50]  # First 50 chars as key
                
                if question not in question_stats:
                    question_stats[question] = {
                        'answers': [],
                        'confidences': [],
                        'count': 0
                    }
                
                question_stats[question]['answers'].append(test['llm_answer'])
                question_stats[question]['confidences'].append(test['confidence'])
                question_stats[question]['count'] += 1
        
        for question, stats in question_stats.items():
            if stats['count'] > 1:
                unique_answers = len(set(stats['answers']))
                avg_confidence = statistics.mean(stats['confidences'])
                consistency = (stats['answers'].count(max(set(stats['answers']), 
                              key=stats['answers'].count)) / len(stats['answers'])) * 100
                
                print(f"\n❓ {question}...")
                print(f"   Times tested: {stats['count']}")
                print(f"   Unique answers: {unique_answers}")
                print(f"   Consistency: {consistency:.0f}%")
                print(f"   Avg confidence: {avg_confidence:.0%}")
    
    def temperature_analysis(self, temperature_values=[0.3, 0.5, 0.7, 0.9]):
        """Analyze how temperature affects responses"""
        print("\n🌡️ TEMPERATURE IMPACT ANALYSIS")
        print("="*60)
        print("Recommended test protocol:")
        print("1. Run same question with different temperature values")
        print("2. Compare consistency and confidence levels")
        print("\nSuggested temperature test values:")
        for temp in temperature_values:
            print(f"  - {temp}: {'More deterministic' if temp < 0.5 else 'Balanced' if temp < 0.8 else 'More creative'}")
    
    def generate_recommendations(self, reports: List[Dict]):
        """Generate recommendations based on analysis"""
        print("\n💡 RECOMMENDATIONS")
        print("="*60)
        
        if not reports:
            print("Run more tests to generate recommendations")
            return
        
        # Calculate overall metrics
        all_confidences = []
        consistency_issues = []
        
        for report in reports:
            for test in report.get('tests', []):
                all_confidences.append(test['confidence'])
        
        if all_confidences:
            avg_confidence = statistics.mean(all_confidences)
            
            if avg_confidence < 0.8:
                print("⚠️ Low average confidence detected ({:.0%})".format(avg_confidence))
                print("   Consider: Enriching consciousness data for uncertain areas")
            
            if avg_confidence > 0.95:
                print("📍 Very high confidence detected ({:.0%})".format(avg_confidence))
                print("   Consider: Testing more subjective/nuanced questions")
            
            # Check confidence distribution
            low_conf = sum(1 for c in all_confidences if c < 0.7)
            if low_conf > len(all_confidences) * 0.2:
                print("⚠️ Many low-confidence responses ({:.0%} below 70%)".format(
                    low_conf/len(all_confidences)))
                print("   Consider: Review and enhance consciousness for these topics")
    
    def create_summary_dashboard(self):
        """Create a comprehensive dashboard view"""
        reports = self.load_all_reports()
        
        print("\n" + "="*70)
        print(" 🧠 CONSCIOUSNESS ENGINE TRACKING DASHBOARD")
        print("="*70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Sessions: {len(reports)}")
        
        if reports:
            total_tests = sum(r['summary']['total_tests'] for r in reports)
            print(f"Total Tests Run: {total_tests}")
        
        self.analyze_confidence_trends(reports)
        self.analyze_question_types(reports)
        self.temperature_analysis()
        self.generate_recommendations(reports)
        
        print("\n" + "="*70)

if __name__ == "__main__":
    tracker = ConsciousnessTracker()
    tracker.create_summary_dashboard()