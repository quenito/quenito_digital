#!/usr/bin/env python3
"""
Script to create __init__.py for models module.
"""

def create_models_init():
    """Create __init__.py for models module."""
    
    models_init_content = '''"""
Survey Automation Data Models
Core data models for question detection and statistics tracking.
"""

from .question_types import QuestionTypeDetector
from .survey_stats import SurveyStats

__all__ = [
    'QuestionTypeDetector',
    'SurveyStats'
]
'''
    
    try:
        with open('models/__init__.py', 'w') as f:
            f.write(models_init_content)
        print("✅ Created models/__init__.py")
        return True
    except Exception as e:
        print(f"❌ Error creating models/__init__.py: {e}")
        return False

def main():
    """Create models __init__.py file."""
    print("🏗️  Creating models/__init__.py...")
    
    if create_models_init():
        print("\n🎉 Models __init__.py created successfully!")
        print("✅ Ready for final testing")
        return True
    else:
        print("\n❌ Failed to create models __init__.py")
        return False

if __name__ == "__main__":
    main()