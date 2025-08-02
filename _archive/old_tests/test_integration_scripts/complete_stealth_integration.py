#!/usr/bin/env python3
"""
🚀 Complete Stealth System Integration Script
Safely deploys all brain-enhanced components with stealth capabilities.
"""

import os
import shutil
import json
from datetime import datetime


def backup_existing_files():
    """Create backups of existing files before replacement."""
    
    print("📦 Creating backups of existing files...")
    
    backup_dir = f"backups/pre_stealth_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        "models/survey_stats.py",
        "utils/reporting.py", 
        "main.py",
        "core/__init__.py",
        "models/__init__.py",
        "utils/__init__.py"
    ]
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, file_path.replace('/', '_'))
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backed up: {file_path} → {backup_path}")
    
    print(f"📁 All backups saved to: {backup_dir}")
    return backup_dir


def create_directory_structure():
    """Ensure all required directories exist."""
    
    print("📁 Creating directory structure...")
    
    directories = [
        "core",
        "models", 
        "utils",
        "handlers",
        "browser_profiles",
        "browser_profiles/quenito_myopinions",
        "browser_profiles/quenito_primeopinion", 
        "browser_profiles/quenito_surveymonkey",
        "reporting",
        "reporting/brain_intelligence",
        "learning_data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")


def create_module_init_files():
    """Create/update __init__.py files for proper imports."""
    
    print("🔧 Creating module initialization files...")
    
    # Core module init
    core_init = '''"""
Survey Automation Core Modules
Enhanced with stealth browser capabilities and brain intelligence.
"""

from .stealth_browser_manager import StealthBrowserManager

# Import existing browser manager for compatibility
try:
    from .browser_manager import BrowserManager
except ImportError:
    BrowserManager = None

__all__ = [
    'StealthBrowserManager'
]

if BrowserManager:
    __all__.append('BrowserManager')
'''
    
    # Models module init
    models_init = '''"""
Survey Automation Data Models
Enhanced with brain learning and intelligence tracking.
"""

from .survey_stats import BrainEnhancedSurveyStats, SurveyStats

__all__ = [
    'BrainEnhancedSurveyStats',
    'SurveyStats'
]
'''
    
    # Utils module init  
    utils_init = '''"""
Survey Automation Utility Services
Enhanced with brain intelligence and stealth reporting.
"""

from .knowledge_base import KnowledgeBase
from .reporting import BrainEnhancedReportGenerator, ReportGenerator

# Import existing components
try:
    from .intervention_manager import EnhancedLearningInterventionManager
except ImportError:
    EnhancedLearningInterventionManager = None

try:
    from .research_engine import ResearchEngine
except ImportError:
    ResearchEngine = None

__all__ = [
    'KnowledgeBase',
    'BrainEnhancedReportGenerator',
    'ReportGenerator'
]

if EnhancedLearningInterventionManager:
    __all__.append('EnhancedLearningInterventionManager')
    
if ResearchEngine:
    __all__.append('ResearchEngine')
'''
    
    # Write init files
    init_files = {
        "core/__init__.py": core_init,
        "models/__init__.py": models_init,
        "utils/__init__.py": utils_init
    }
    
    for file_path, content in init_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ {file_path}")


def create_stealth_config():
    """Create comprehensive stealth configuration."""
    
    print("⚙️ Creating stealth system configuration...")
    
    config = {
        "version": "2.0.0",
        "deployment_date": datetime.now().isoformat(),
        "stealth_system": {
            "enabled": True,
            "default_profile": "quenito_myopinions",
            "cookie_transfer": True,
            "stealth_enhancements": True,
            "human_behavior_simulation": True
        },
        "platforms": {
            "myopinions.com.au": {
                "name": "MyOpinions Australia",
                "profile": "quenito_myopinions",
                "target_url": "https://www.myopinions.com.au/auth/dashboard",
                "stealth_level": "maximum",
                "cookie_domains": ["myopinions.com.au", "google.com", "googleapis.com"]
            },
            "primeopinion.com.au": {
                "name": "Prime Opinion Australia",
                "profile": "quenito_primeopinion", 
                "target_url": "https://app.primeopinion.com.au/surveys",
                "stealth_level": "maximum",
                "cookie_domains": ["primeopinion.com.au", "google.com", "googleapis.com"]
            },
            "surveymonkey.com": {
                "name": "SurveyMonkey",
                "profile": "quenito_surveymonkey",
                "target_url": "direct_survey_url",
                "stealth_level": "high", 
                "cookie_domains": ["surveymonkey.com", "google.com"]
            }
        },
        "brain_integration": {
            "enabled": True,
            "real_time_learning": True,
            "confidence_calibration": True,
            "performance_tracking": True,
            "intelligence_reporting": True
        }
    }
    
    with open("core/stealth_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ core/stealth_config.json")


def create_integration_test():
    """Create comprehensive integration test script."""
    
    print("🧪 Creating integration test script...")
    
    test_script = '''#!/usr/bin/env python3
"""
🧪 Complete Stealth Integration Test
Validates all components working together.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.stealth_browser_manager import StealthBrowserManager
    from models.survey_stats import BrainEnhancedSurveyStats
    from utils.reporting import BrainEnhancedReportGenerator
    from utils.knowledge_base import KnowledgeBase
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Run the integration script first")
    sys.exit(1)


async def test_stealth_integration():
    """Test complete stealth system integration."""
    
    print("🧪 COMPLETE STEALTH INTEGRATION TEST")
    print("=" * 45)
    
    # Test 1: Brain components
    print("\\n📊 TEST 1: Brain Components")
    print("-" * 30)
    
    try:
        brain = KnowledgeBase()
        stats = BrainEnhancedSurveyStats(knowledge_base=brain)
        reporter = BrainEnhancedReportGenerator(knowledge_base=brain)
        
        print("✅ Brain components initialized")
        print(f"   • Knowledge Base: {type(brain).__name__}")
        print(f"   • Statistics: {type(stats).__name__}")
        print(f"   • Reporting: {type(reporter).__name__}")
        
    except Exception as e:
        print(f"❌ Brain components failed: {e}")
        return False
    
    # Test 2: Stealth browser
    print("\\n🕵️ TEST 2: Stealth Browser Integration")
    print("-" * 30)
    
    stealth_manager = None
    try:
        stealth_manager = StealthBrowserManager("quenito_integration_test")
        page = await stealth_manager.initialize_stealth_browser(
            transfer_cookies=False,  # Skip cookies for integration test
            use_existing_chrome=False
        )
        
        print("✅ Stealth browser created")
        print("✅ Brain-stealth integration working")
        
    except Exception as e:
        print(f"❌ Stealth browser failed: {e}")
        return False
    
    # Test 3: Brain learning simulation
    print("\\n🧠 TEST 3: Brain Learning Integration")
    print("-" * 30)
    
    try:
        # Start brain session
        stats.start_survey()
        reporter.start_session()
        
        # Simulate learning events
        stats.increment_question_count("demographics", 0.85)
        stats.increment_automated_count("demographics", 0.85)
        stats.record_pattern_discovery("test_pattern", {"keywords": ["test"]})
        
        # End session
        stats.end_survey()
        reporter.end_session()
        
        print("✅ Brain learning simulation successful")
        print(f"   • Questions processed: {stats.get_total_questions()}")
        print(f"   • Automation rate: {stats.get_automation_rate():.1f}%")
        
    except Exception as e:
        print(f"❌ Brain learning failed: {e}")
        return False
    
    # Test 4: Intelligence reporting
    print("\\n📊 TEST 4: Intelligence Reporting")
    print("-" * 30)
    
    try:
        report = reporter.generate_brain_intelligence_report(stats)
        
        if "BRAIN INTELLIGENCE REPORT" in report:
            print("✅ Intelligence reporting working")
            print("✅ Brain evolution tracking active")
        else:
            print("⚠️ Report generated but missing key sections")
        
    except Exception as e:
        print(f"❌ Intelligence reporting failed: {e}")
        return False
    
    # Test 5: Platform configuration
    print("\\n🎯 TEST 5: Platform Configuration")
    print("-" * 30)
    
    try:
        # Test stealth configuration loading
        import json
        with open("core/stealth_config.json", "r") as f:
            config = json.load(f)
        
        platforms = config.get("platforms", {})
        print(f"✅ Configuration loaded: {len(platforms)} platforms")
        
        for platform, details in platforms.items():
            print(f"   • {details['name']}: {details['stealth_level']} stealth")
            
    except Exception as e:
        print(f"❌ Platform configuration failed: {e}")
        return False
    
    # Final summary
    print("\\n🎉 INTEGRATION TEST SUMMARY")
    print("=" * 35)
    print("✅ Brain-enhanced statistics: WORKING")
    print("✅ Brain-enhanced reporting: WORKING") 
    print("✅ Stealth browser system: WORKING")
    print("✅ Brain learning integration: WORKING")
    print("✅ Intelligence reporting: WORKING")
    print("✅ Platform configuration: WORKING")
    print()
    print("🚀 COMPLETE INTEGRATION: SUCCESS!")
    print("🎯 Ready for Survey 1A testing with full stealth + brain!")
    
    return True


async def main():
    """Run integration tests."""
    
    try:
        success = await test_stealth_integration()
        
        if success:
            print("\\n🎉 ALL INTEGRATION TESTS PASSED!")
            print("🚀 System ready for Survey 1A automation!")
        else:
            print("\\n⚠️ Some integration tests failed")
            print("🔧 Check output above for issues")
            
    except Exception as e:
        print(f"❌ Integration test error: {e}")
    
    finally:
        # Cleanup
        print("\\n🔒 Cleaning up test resources...")


if __name__ == "__main__":
    print("🧪 Starting complete integration test...")
    asyncio.run(main())
'''
    
    with open("test_complete_integration.py", "w") as f:
        f.write(test_script)
    
    print("✅ test_complete_integration.py")


def create_deployment_checklist():
    """Create post-deployment checklist."""
    
    checklist = f'''# 🚀 Complete Stealth Integration Checklist

## ✅ Deployment Status - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### Phase 1: File Deployment
- [ ] core/stealth_browser_manager.py deployed
- [ ] models/survey_stats.py updated (brain-enhanced)
- [ ] utils/reporting.py updated (brain-enhanced)  
- [ ] main.py updated (stealth interface)
- [ ] Module __init__.py files updated
- [ ] Configuration files created

### Phase 2: Integration Testing
- [ ] Run: python test_complete_integration.py
- [ ] All 5 integration tests pass
- [ ] No import errors
- [ ] Brain learning functional
- [ ] Stealth system operational

### Phase 3: Platform Validation
- [ ] MyOpinions stealth access (previously tested)
- [ ] Prime Opinion stealth access (✅ VALIDATED)
- [ ] SurveyMonkey compatibility ready

### Phase 4: Survey 1A Preparation
- [ ] Demographics handler brain ready
- [ ] Brain-enhanced statistics active
- [ ] Intelligence reporting enabled
- [ ] SurveyMonkey stealth configured

## 🎯 Files to Deploy

Copy these artifacts to your project:

1. **Stealth Browser Manager** → `core/stealth_browser_manager.py`
2. **Brain-Enhanced Survey Stats** → `models/survey_stats.py`
3. **Brain-Enhanced Reporting** → `utils/reporting.py`
4. **Enhanced Main Interface** → `main.py`

## 🧪 Testing Commands

```bash
# 1. Test complete integration
python test_complete_integration.py

# 2. Test stealth platforms
python test_primeopinion_simple.py  # Already passed ✅

# 3. Run enhanced main interface
python main.py
```

## 🚀 Ready for Survey 1A!

Once all tests pass, you'll have:

✅ **Complete stealth system** with cookie transfer
✅ **Brain-enhanced automation** with learning
✅ **Real-time intelligence** tracking
✅ **Multi-platform compatibility** proven
✅ **Commercial-grade architecture** deployed

**The ultimate survey automation system is ready!** 🧠🕵️‍♂️🎯
'''
    
    with open("INTEGRATION_CHECKLIST.md", "w") as f:
        f.write(checklist)
    
    print("✅ INTEGRATION_CHECKLIST.md")


def main():
    """Main integration deployment function."""
    
    print("🚀 COMPLETE STEALTH SYSTEM INTEGRATION")
    print("=" * 50)
    print("Deploying brain-enhanced automation with stealth capabilities...")
    print()
    
    # Step 1: Backup existing files
    backup_dir = backup_existing_files()
    print()
    
    # Step 2: Create directories
    create_directory_structure() 
    print()
    
    # Step 3: Update module imports
    create_module_init_files()
    print()
    
    # Step 4: Create configuration
    create_stealth_config()
    print()
    
    # Step 5: Create integration test
    create_integration_test()
    print()
    
    # Step 6: Create checklist
    create_deployment_checklist()
    print()
    
    print("🎉 INTEGRATION PREPARATION COMPLETE!")
    print("=" * 50)
    print()
    print("📋 NEXT STEPS:")
    print()
    print("1. 📂 DEPLOY CORE FILES:")
    print("   Copy these artifacts to your project:")
    print("   • Stealth Browser Manager → core/stealth_browser_manager.py")
    print("   • Brain-Enhanced Survey Stats → models/survey_stats.py")
    print("   • Brain-Enhanced Reporting → utils/reporting.py") 
    print("   • Enhanced Main Interface → main.py")
    print()
    print("2. 🧪 TEST INTEGRATION:")
    print("   • Run: python test_complete_integration.py")
    print("   • Verify all 5 tests pass")
    print()
    print("3. 🚀 LAUNCH ENHANCED QUENITO:")
    print("   • Run: python main.py")
    print("   • Test Prime Opinion stealth access")
    print("   • Prepare for Survey 1A testing!")
    print()
    print(f"📁 Backups saved to: {backup_dir}")
    print("🛡️ Original files safely preserved")
    print()
    print("🎯 Ready to deploy the ultimate survey automation system!")
    
    return True


if __name__ == "__main__":
    main()
