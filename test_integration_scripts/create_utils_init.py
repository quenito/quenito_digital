#!/usr/bin/env python3
"""
Script to create __init__.py files for utils modules.
"""

import os

def create_utils_init():
    """Create __init__.py for utils module."""
    
    utils_init_content = '''"""
Survey Automation Utility Services
Core utility modules for knowledge base, interventions, research, and reporting.
"""

from .knowledge_base import KnowledgeBase
from .intervention_manager import InterventionManager
from .research_engine import ResearchEngine
from .reporting import ReportGenerator

__all__ = [
    'KnowledgeBase',
    'InterventionManager', 
    'ResearchEngine',
    'ReportGenerator'
]
'''
    
    try:
        with open('utils/__init__.py', 'w') as f:
            f.write(utils_init_content)
        print("✅ Created utils/__init__.py")
        return True
    except Exception as e:
        print(f"❌ Error creating utils/__init__.py: {e}")
        return False

def create_core_init():
    """Create __init__.py for core module."""
    
    core_init_content = '''"""
Survey Automation Core Modules
Core infrastructure for browser management, survey detection, and navigation.
"""

from .browser_manager import BrowserManager
from .survey_detector import SurveyDetector
from .navigation_controller import NavigationController

__all__ = [
    'BrowserManager',
    'SurveyDetector',
    'NavigationController'
]
'''
    
    try:
        with open('core/__init__.py', 'w') as f:
            f.write(core_init_content)
        print("✅ Created core/__init__.py")
        return True
    except Exception as e:
        print(f"❌ Error creating core/__init__.py: {e}")
        return False

def main():
    """Create all __init__.py files."""
    print("🏗️  Creating __init__.py files for modules...")
    
    success = True
    success &= create_utils_init()
    success &= create_core_init()
    
    if success:
        print("\n🎉 All __init__.py files created successfully!")
        print("✅ Modules are ready for testing")
        return True
    else:
        print("\n❌ Some files could not be created")
        return False

if __name__ == "__main__":
    main()
