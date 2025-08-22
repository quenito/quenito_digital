#!/usr/bin/env python3
"""
🔍 PATTERN REVIEW & GOVERNANCE TOOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reviews session files and suggests patterns for human approval
Maintains QA control over what gets added to learned_patterns.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import json
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter, defaultdict


class PatternReviewTool:
    """Tool for reviewing sessions and managing pattern learning"""
    
    def __init__(self, persona_name: str = "quenito"):
        self.persona_name = persona_name
        self.base_path = Path(f"personas/{persona_name}")
        self.session_path = self.base_path / "sessions"
        self.learned_patterns_path = self.base_path / "learned_patterns.json"
        self.learned_responses_path = self.base_path / "learned_responses.json"
        
        # Load existing patterns
        self.learned_patterns = self._load_json(self.learned_patterns_path, {})
        print(f"📚 Loaded {len(self.learned_patterns)} existing patterns")
    
    def _load_json(self, path: Path, default: Dict) -> Dict:
        """Load JSON file or return default"""
        if path.exists():
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, path: Path, data: Dict):
        """Save JSON file"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def analyze_recent_sessions(self, num_sessions: int = 10) -> Dict:
        """Analyze recent session files for patterns"""
        
        # Get recent session files
        session_files = sorted(glob.glob(str(self.session_path / "session_*.json")))
        if not session_files:
            print("❌ No session files found")
            return {}
        
        # Limit to recent sessions
        session_files = session_files[-num_sessions:]
        
        print(f"\n📊 Analyzing {len(session_files)} recent sessions...")
        print("=" * 60)
        
        # Collect all data
        all_automated = []
        all_manual = []
        all_failed = []
        
        for session_file in session_files:
            with open(session_file, 'r') as f:
                session = json.load(f)
                all_automated.extend(session.get("automated", []))
                all_manual.extend(session.get("manual", []))
                all_failed.extend(session.get("failed", []))
        
        # Analyze manual interventions
        manual_analysis = self._analyze_manual_interventions(all_manual)
        
        # Show statistics
        print(f"\n📈 Session Statistics:")
        print(f"   ✅ Automated: {len(all_automated)} questions")
        print(f"   🔧 Manual: {len(all_manual)} interventions")
        print(f"   ❌ Failed: {len(all_failed)} attempts")
        
        if all_automated:
            # Show automation success by source
            sources = Counter(a.get("source", "unknown") for a in all_automated if isinstance(a, dict))
            print(f"\n📊 Automation Sources:")
            for source, count in sources.most_common():
                print(f"   • {source}: {count}")
        
        return manual_analysis
    
    def _analyze_manual_interventions(self, manual_items: List[Dict]) -> Dict:
        """Analyze manual interventions for patterns"""
        
        if not manual_items:
            print("\n✅ No manual interventions found - full automation!")
            return {}
        
        print(f"\n🔍 Analyzing {len(manual_items)} manual interventions...")
        
        # Group by answer frequency
        answer_counter = Counter()
        answer_questions = defaultdict(list)
        
        for item in manual_items:
            answer = item.get("answer", "")
            question = item.get("question", "")
            
            if answer and question:
                answer_counter[answer] += 1
                answer_questions[answer].append(question)
        
        # Find potential patterns (3+ occurrences)
        potential_patterns = {}
        
        print("\n🎯 Potential Patterns Detected:")
        print("-" * 60)
        
        for answer, count in answer_counter.most_common():
            if count >= 3:
                questions = answer_questions[answer]
                
                # Find common words in questions
                common_words = self._find_common_words(questions)
                
                if common_words:
                    pattern_key = f"pattern_{len(potential_patterns) + 1}"
                    potential_patterns[pattern_key] = {
                        "answer": answer,
                        "count": count,
                        "common_words": list(common_words)[:5],
                        "sample_questions": questions[:3]
                    }
                    
                    print(f"\n📌 Pattern #{len(potential_patterns)}:")
                    print(f"   Answer: '{answer}' (used {count} times)")
                    print(f"   Common words: {', '.join(list(common_words)[:5])}")
                    print(f"   Sample questions:")
                    for q in questions[:2]:
                        print(f"      • {q[:80]}...")
        
        if not potential_patterns:
            print("   ℹ️ No patterns found (need 3+ repeated answers)")
        
        # Show all manual interventions summary
        print("\n📝 All Manual Interventions Summary:")
        print("-" * 60)
        for answer, count in answer_counter.most_common(10):
            print(f"   • '{answer}': {count} time(s)")
            if count < 3:
                print(f"     (Need {3-count} more to suggest as pattern)")
        
        return potential_patterns
    
    def _find_common_words(self, questions: List[str]) -> set:
        """Find common words across questions"""
        if not questions:
            return set()
        
        # Convert to lowercase and split
        word_sets = [set(q.lower().split()) for q in questions]
        
        # Find intersection
        common = word_sets[0]
        for word_set in word_sets[1:]:
            common &= word_set
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                      'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                      'how', 'when', 'where', 'what', 'which', 'who', 'whom', 'this', 'that',
                      'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                      'could', 'may', 'might', 'must', 'can', 'your', 'you', 'please'}
        
        common -= stop_words
        
        return common
    
    def add_pattern(self, pattern_name: str, keywords: List[str], 
                    response: str, confidence: float = 0.90,
                    response_logic: str = None):
        """
        Add a new pattern after human review
        
        Example usage:
        tool.add_pattern(
            pattern_name="shopping_frequency",
            keywords=["often", "shop", "groceries"],
            response="Weekly",
            confidence=0.95
        )
        """
        
        # Validate inputs
        if not pattern_name or not keywords or not (response or response_logic):
            print("❌ Invalid pattern: need name, keywords, and response/logic")
            return False
        
        # Check if pattern already exists
        if pattern_name in self.learned_patterns:
            print(f"⚠️ Pattern '{pattern_name}' already exists. Use update_pattern() to modify.")
            return False
        
        # Add the pattern
        self.learned_patterns[pattern_name] = {
            "patterns": [k.lower() for k in keywords],  # Normalize to lowercase
            "confidence": confidence,
            "added_by": "human_review",
            "added_at": datetime.now().isoformat()
        }
        
        # Add response or response_logic
        if response_logic:
            self.learned_patterns[pattern_name]["response_logic"] = response_logic
        else:
            self.learned_patterns[pattern_name]["response"] = response
        
        # Save immediately
        self._save_json(self.learned_patterns_path, self.learned_patterns)
        
        print(f"✅ Added pattern: {pattern_name}")
        print(f"   Keywords: {keywords}")
        print(f"   Response: {response or response_logic}")
        print(f"   Confidence: {confidence}")
        
        return True
    
    def list_patterns(self):
        """List all current patterns"""
        print("\n📚 Current Patterns:")
        print("=" * 60)
        
        if not self.learned_patterns:
            print("   No patterns found")
            return
        
        for name, data in self.learned_patterns.items():
            print(f"\n📌 {name}:")
            print(f"   Patterns: {data.get('patterns', [])}")
            if 'response' in data:
                print(f"   Response: {data['response']}")
            elif 'response_logic' in data:
                print(f"   Logic: {data['response_logic']}")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
            if 'added_at' in data:
                print(f"   Added: {data['added_at'][:10]}")
    
    def remove_pattern(self, pattern_name: str):
        """Remove a pattern (with confirmation)"""
        if pattern_name not in self.learned_patterns:
            print(f"❌ Pattern '{pattern_name}' not found")
            return False
        
        # Show pattern details
        pattern = self.learned_patterns[pattern_name]
        print(f"\n⚠️ About to remove pattern: {pattern_name}")
        print(f"   Patterns: {pattern.get('patterns', [])}")
        print(f"   Response: {pattern.get('response', pattern.get('response_logic', 'N/A'))}")
        
        # Confirm
        confirm = input("\nAre you sure? (yes/no): ").lower()
        if confirm == 'yes':
            del self.learned_patterns[pattern_name]
            self._save_json(self.learned_patterns_path, self.learned_patterns)
            print(f"✅ Removed pattern: {pattern_name}")
            return True
        else:
            print("❌ Removal cancelled")
            return False
    
    def generate_add_commands(self, patterns: Dict):
        """Generate commands to add suggested patterns"""
        
        if not patterns:
            return
        
        print("\n📝 Commands to Add These Patterns:")
        print("=" * 60)
        print("# Review each suggestion and run if appropriate:\n")
        
        for i, (key, data) in enumerate(patterns.items(), 1):
            answer = data['answer']
            common_words = data['common_words']
            
            # Generate a sensible pattern name
            pattern_name = f"{answer.lower().replace(' ', '_')}_{common_words[0] if common_words else 'pattern'}"
            
            print(f"# Pattern {i}: {answer}")
            print(f"tool.add_pattern(")
            print(f'    pattern_name="{pattern_name}",')
            print(f'    keywords={common_words[:3]},')
            print(f'    response="{answer}",')
            print(f'    confidence=0.90')
            print(f")\n")


def main():
    """Main execution"""
    print("🔍 PATTERN REVIEW & GOVERNANCE TOOL")
    print("=" * 60)
    
    # Initialize tool
    tool = PatternReviewTool()
    
    # Analyze recent sessions
    patterns = tool.analyze_recent_sessions(num_sessions=20)
    
    # Generate add commands if patterns found
    if patterns:
        tool.generate_add_commands(patterns)
    
    # List current patterns
    tool.list_patterns()
    
    print("\n💡 Interactive Mode:")
    print("   tool = PatternReviewTool()")
    print("   tool.add_pattern(...)")
    print("   tool.list_patterns()")
    print("   tool.remove_pattern('pattern_name')")
    
    return tool


if __name__ == "__main__":
    tool = main()