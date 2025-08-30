# test_consciousness.py

import asyncio
import json
import os
from datetime import datetime
from consciousness_engine_production import ConsciousnessEngine

class ConsciousnessTestRunner:
    def __init__(self):
        self.engine = ConsciousnessEngine(consciousness_path="matt_consciousness_v3.json")
        self.test_results = []
        self.test_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "temperature": 0.7,
            "model": "gpt-4o-mini"
        }
    
    async def run_single_test(self, screenshot_path):
        """Run a single test with detailed logging"""
        result = await self.engine.test_screenshot_flow(screenshot_path)
        
        # Enhanced display
        print(f"\n{'='*70}")
        print(f"📸 Screenshot: {screenshot_path}")
        print(f"{'='*70}")
        print(f"📋 Question: {result['question']}")
        
        # Display options if available
        if result.get('options'):
            print(f"\n📝 Available Options:")
            
            # Handle multi-select answers
            selected_answers = result['llm_answer'] if isinstance(result['llm_answer'], list) else [result['llm_answer']]
            
            for i, option in enumerate(result['options'], 1):
                selected = "✅" if option in selected_answers else "  "
                print(f"   {selected} {i}. {option}")
        else:
            print(f"📝 Free text response required")
        
        # Display answer(s)
        if isinstance(result['llm_answer'], list):
            print(f"\n🎯 Selected Answers ({len(result['llm_answer'])} choices):")
            for answer in result['llm_answer']:
                print(f"   • {answer}")
        else:
            print(f"\n🎯 Selected Answer: {result['llm_answer']}")
            
        print(f"💭 Confidence: {result['confidence']:.0%}")
        print(f"🧠 Reasoning: {result['reasoning'][:200]}...")
        
        # Store for detailed tracking
        self.test_results.append(result)
        
        return result
    
    async def run_multiple_times(self, screenshot_path, runs=3):
        """Test consistency by running same question multiple times"""
        print(f"\n{'='*70}")
        print(f"🔄 CONSISTENCY TEST: Running {runs} times")
        print(f"{'='*70}")
        
        answers = []
        confidences = []
        
        for i in range(runs):
            result = await self.engine.test_screenshot_flow(screenshot_path)
            answers.append(result['llm_answer'])
            confidences.append(result['confidence'])
            
            # Special handling for multi-select answers
            if isinstance(result['llm_answer'], list):
                print(f"Run {i+1}: {len(result['llm_answer'])} values selected")
                print(f"         Values: {', '.join(result['llm_answer'][:3])}...")
                print(f"         Confidence: {result['confidence']:.0%}")
            else:
                print(f"Run {i+1}: Answer='{result['llm_answer']}', Confidence={result['confidence']:.0%}")
        
        # Analyze consistency for multi-select answers
        if all(isinstance(a, list) for a in answers):
            # For multi-select, check overlap between selections
            all_selected = [set(a) for a in answers]
            common_selections = set.intersection(*all_selected)
            union_selections = set.union(*all_selected)
            
            consistency_score = len(common_selections) / len(union_selections) if union_selections else 0
            
            print(f"\n📊 Multi-Select Consistency Analysis:")
            print(f"   Always selected ({len(common_selections)}): {', '.join(sorted(common_selections))}")
            print(f"   Sometimes selected: {', '.join(sorted(union_selections - common_selections))}")
            print(f"   Consistency score: {consistency_score:.0%}")
            print(f"   Average confidence: {sum(confidences) / len(confidences):.0%}")
            
            return {
                "answers": answers,
                "confidences": confidences,
                "consistency_score": consistency_score,
                "common_selections": list(common_selections),
                "all_selections": list(union_selections)
            }
        else:
            # Original consistency analysis for single-select
            unique_answers = set(str(a) for a in answers)
            consistency_rate = (answers.count(max(set(answers), key=answers.count)) / len(answers)) * 100
            avg_confidence = sum(confidences) / len(confidences)
            
            print(f"\n📊 Consistency Analysis:")
            print(f"   Unique answers: {len(unique_answers)} ({', '.join(unique_answers)})")
            print(f"   Consistency rate: {consistency_rate:.0f}%")
            print(f"   Average confidence: {avg_confidence:.0%}")
            print(f"   Confidence range: {min(confidences):.0%} - {max(confidences):.0%}")
            
            return {
                "answers": answers,
                "confidences": confidences,
                "consistency_rate": consistency_rate,
                "unique_answers": list(unique_answers)
            }
    
    def generate_detailed_report(self):
        """Generate comprehensive test report"""
        report = {
            "session": self.test_session,
            "summary": {
                "total_tests": len(self.test_results),
                "avg_confidence": 0,
                "question_types": {},
                "confidence_distribution": {
                    "100%": 0,
                    "90-99%": 0,
                    "80-89%": 0,
                    "70-79%": 0,
                    "<70%": 0
                }
            },
            "tests": self.test_results
        }
        
        # Calculate statistics
        if self.test_results:
            confidences = [r['confidence'] for r in self.test_results]
            report['summary']['avg_confidence'] = sum(confidences) / len(confidences)
            
            # Confidence distribution
            for conf in confidences:
                if conf == 1.0:
                    report['summary']['confidence_distribution']['100%'] += 1
                elif conf >= 0.9:
                    report['summary']['confidence_distribution']['90-99%'] += 1
                elif conf >= 0.8:
                    report['summary']['confidence_distribution']['80-89%'] += 1
                elif conf >= 0.7:
                    report['summary']['confidence_distribution']['70-79%'] += 1
                else:
                    report['summary']['confidence_distribution']['<70%'] += 1
        
        # Save to file
        report_filename = f"test_reports/consciousness_test_{self.test_session['session_id']}.json"
        os.makedirs("test_reports", exist_ok=True)
        
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n{'='*70}")
        print("📊 TEST SESSION SUMMARY")
        print(f"{'='*70}")
        print(f"Session ID: {self.test_session['session_id']}")
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Average Confidence: {report['summary']['avg_confidence']:.0%}")
        print(f"\nConfidence Distribution:")
        for range_name, count in report['summary']['confidence_distribution'].items():
            if count > 0:
                print(f"   {range_name}: {count} tests")
        print(f"\n📁 Full report saved to: {report_filename}")
        
        return report

async def main():
    runner = ConsciousnessTestRunner()
    
    # Test screenshots
    test_screenshots = [
        "screenshots/prime_opinion_q1_before.png"
        #"screenshots/prime_opinion_q2_before.png"
        #"screenshots/prime_opinion_q3_before.png"
    ]
    
    # Run main tests
    for screenshot in test_screenshots:
        await runner.run_single_test(screenshot)
    
    # Enhanced consistency testing with question selection
    print(f"\n{'='*70}")
    print("CONSISTENCY TESTING OPTIONS")
    print(f"{'='*70}")
    print("1. Test Question 1 (Age group)")
    print("2. Test Question 2 (Friend description)")
    print("3. Test Question 3 (Values - Multi-select)")
    print("4. Skip consistency testing")
    
    choice = input("\nSelect which question to test for consistency (1-4): ")
    
    if choice in ['1', '2', '3']:
        question_index = int(choice) - 1
        screenshot = test_screenshots[question_index]
        
        # Ask for number of runs
        runs_input = input("How many times to run? (default 5): ")
        runs = int(runs_input) if runs_input.isdigit() else 5
        
        await runner.run_multiple_times(screenshot, runs=runs)
    elif choice != '4':
        print("Invalid selection, skipping consistency test")
    
    # Generate final report
    runner.generate_detailed_report()

if __name__ == "__main__":
    asyncio.run(main())