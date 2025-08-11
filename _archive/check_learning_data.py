# check_learning_data.py
"""
Check what was saved in Quenito's knowledge base
"""

import json
import os
from datetime import datetime

def check_learning_data():
    """Display Quenito's learned data"""
    
    kb_path = "personas/quenito/knowledge_base.json"
    
    print("🔍 CHECKING QUENITO'S LEARNING DATA")
    print("="*50)
    
    if not os.path.exists(kb_path):
        print(f"❌ No knowledge base found at: {kb_path}")
        return
    
    with open(kb_path, 'r') as f:
        data = json.load(f)
    
    print(f"✅ Knowledge base found!")
    print(f"📁 Location: {kb_path}")
    print(f"📊 File size: {os.path.getsize(kb_path)} bytes")
    
    # Check for learning sessions
    if 'learning_sessions' in data:
        sessions = data['learning_sessions']
        print(f"\n📚 Learning Sessions: {len(sessions)}")
        
        for session in sessions:
            print(f"\n📅 Session: {session.get('id', 'Unknown')}")
            print(f"   Started: {session.get('started', 'Unknown')}")
            
            if 'survey' in session:
                survey = session['survey']
                print(f"   Survey: {survey.get('time', 'Unknown')} - {survey.get('points', 0)} points")
            
            if 'questions' in session:
                questions = session['questions']
                print(f"   Questions captured: {len(questions)}")
                
                for i, q in enumerate(questions, 1):
                    print(f"\n   Question {i}:")
                    print(f"     Type detected: {q.get('detected_type', 'Unknown')}")
                    print(f"     Timestamp: {q.get('timestamp', 'Unknown')}")
                    print(f"     Preview: {q.get('question_preview', '')[:100]}...")
    
    # Show raw data structure
    print("\n📋 Raw data structure:")
    print(json.dumps(data, indent=2, default=str)[:500] + "...")
    
    # Check for any ElementHandle issues
    print("\n🔍 Checking for serialization issues...")
    element_handles = []
    
    def find_element_handles(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'element' or 'ElementHandle' in str(v):
                    element_handles.append(f"{path}.{k}")
                elif isinstance(v, (dict, list)):
                    find_element_handles(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                find_element_handles(v, f"{path}[{i}]")
    
    find_element_handles(data)
    
    if element_handles:
        print(f"⚠️ Found {len(element_handles)} ElementHandle references:")
        for eh in element_handles:
            print(f"   - {eh}")
    else:
        print("✅ No ElementHandle serialization issues found")

if __name__ == "__main__":
    check_learning_data()