# verify_learning_system.py
"""
Verify that Quenito's learning system is properly connected
Critical for ensuring the second survey run uses learned patterns!
"""

import os
import json
from pathlib import Path

def verify_learning_components():
    """Check all learning components are in place"""
    
    print("🔍 VERIFYING QUENITO'S LEARNING SYSTEM")
    print("="*50)
    
    components = {
        "Knowledge Base": "data/knowledge_base.json",
        "Brain Learning": "data/brain_learning.py",
        "Intervention Manager": "utils/intervention_manager.py",
        "Pattern Manager": "data/pattern_manager.py",
        "Learning Data Dir": "learning_data/",
        "Screenshots Dir": "learning_data/screenshots/",
        "Persona Knowledge": "personas/quenito/knowledge_base.json"
    }
    
    all_good = True
    
    for component, path in components.items():
        if os.path.exists(path):
            print(f"✅ {component}: {path}")
        else:
            print(f"❌ {component}: NOT FOUND at {path}")
            all_good = False
    
    # Check if knowledge base has learning sections
    kb_path = "data/knowledge_base.json"
    if os.path.exists(kb_path):
        with open(kb_path, 'r') as f:
            kb_data = json.load(f)
        
        print("\n📊 Knowledge Base Structure:")
        if 'brain_learning' in kb_data:
            print("  ✅ brain_learning section exists")
            if 'intervention_history' in kb_data['brain_learning']:
                count = len(kb_data['brain_learning']['intervention_history'])
                print(f"  ✅ intervention_history: {count} entries")
            if 'success_patterns' in kb_data['brain_learning']:
                count = len(kb_data['brain_learning']['success_patterns'])
                print(f"  ✅ success_patterns: {count} patterns")
        else:
            print("  ⚠️ brain_learning section missing - will be created on first use")
    
    # Check persona-specific knowledge
    persona_kb = "personas/quenito/knowledge_base.json"
    if os.path.exists(persona_kb):
        with open(persona_kb, 'r') as f:
            persona_data = json.load(f)
        print(f"\n📁 Quenito's Personal Knowledge:")
        print(f"  ✅ File exists with {len(persona_data)} entries")
    
    # Create missing directories
    os.makedirs("learning_data", exist_ok=True)
    os.makedirs("learning_data/screenshots", exist_ok=True)
    
    return all_good

def check_recent_learning():
    """Check for recent learning data"""
    
    print("\n🧠 RECENT LEARNING ACTIVITY:")
    print("="*50)
    
    learning_dir = "learning_data"
    if os.path.exists(learning_dir):
        files = list(Path(learning_dir).glob("*.json"))
        if files:
            print(f"✅ Found {len(files)} learning files")
            # Show most recent
            latest = max(files, key=os.path.getctime)
            print(f"📄 Most recent: {latest.name}")
            with open(latest, 'r') as f:
                data = json.load(f)
            print(f"   Type: {data.get('question_type', 'Unknown')}")
            print(f"   Response: {data.get('manual_response', 'Unknown')}")
        else:
            print("⚠️ No learning files yet - will be created during first survey")
    
def test_learning_connection():
    """Quick test of learning system connection"""
    
    print("\n🧪 TESTING LEARNING CONNECTIONS:")
    print("="*50)
    
    try:
        # Test knowledge base import
        from data.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        print("✅ KnowledgeBase loads successfully")
        
        # Test intervention manager
        from utils.intervention_manager import EnhancedLearningInterventionManager
        print("✅ InterventionManager loads successfully")
        
        # Test brain learning
        from data.brain_learning import BrainLearning
        print("✅ BrainLearning loads successfully")
        
        print("\n🎉 ALL LEARNING SYSTEMS CONNECTED!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 QUENITO LEARNING SYSTEM CHECK")
    print("="*50)
    
    # Verify components
    components_ok = verify_learning_components()
    
    # Check recent learning
    check_recent_learning()
    
    # Test connections
    connections_ok = test_learning_connection()
    
    print("\n📊 SUMMARY:")
    print("="*50)
    if components_ok and connections_ok:
        print("✅ Learning system is READY!")
        print("🚀 Quenito will capture and learn from manual interventions")
        print("🧠 Second survey run will use learned patterns!")
    else:
        print("⚠️ Some components need attention")
        print("💡 Fix any missing components before running surveys")