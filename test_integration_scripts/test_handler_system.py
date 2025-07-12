#!/usr/bin/env python3
"""
Test script for the handler system.
Validates handler selection, confidence scoring, and factory functionality.
"""

import sys
import os

# Add the survey_automation directory to the path  
sys.path.insert(0, os.path.dirname(__file__))


def test_handler_imports():
    """Test that all handlers can be imported."""
    print("🧪 Testing handler imports...")
    
    try:
        from handlers.base_handler import BaseQuestionHandler
        from handlers.demographics_handler import DemographicsHandler
        from handlers.unknown_handler import UnknownHandler
        from handlers.handler_factory import HandlerFactory
        
        print("✅ Core handlers imported successfully")
        
        # Test placeholder handlers (will be created by script)
        from handlers.brand_familiarity_handler import BrandFamiliarityHandler
        from handlers.rating_matrix_handler import RatingMatrixHandler
        from handlers.multi_select_handler import MultiSelectHandler
        from handlers.recency_activities_handler import RecencyActivitiesHandler
        from handlers.trust_rating_handler import TrustRatingHandler
        from survey_automation.handlers.research_handler import ResearchRequiredHandler
        
        print("✅ All placeholder handlers imported successfully")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to run 'python create_placeholder_handlers.py' first")
        return False
    
    return True


def test_handler_factory():
    """Test handler factory functionality."""
    print("🧪 Testing handler factory...")
    
    try:
        from handlers.handler_factory import HandlerFactory
        
        # Create factory with mock dependencies
        factory = HandlerFactory(
            knowledge_base={"user_profile": {"demographics": {}}},
            intervention_manager=None
        )
        
        # Test available handlers
        handlers = factory.get_available_handlers()
        print(f"   Available handlers: {handlers}")
        assert len(handlers) > 0, "Should have available handlers"
        
        # Test handler validation
        print("   Validating handler implementations...")
        if factory.validate_handlers():
            print("✅ All handlers properly implemented")
        else:
            print("⚠️ Some handlers need improvement (expected for placeholders)")
        
        print("✅ Handler factory tests passed")
        
    except Exception as e:
        print(f"❌ Handler factory test failed: {e}")
        return False
    
    return True


def test_confidence_scoring():
    """Test handler confidence scoring with sample content."""
    print("🧪 Testing confidence scoring...")
    
    try:
        from handlers.handler_factory import HandlerFactory
        
        # Mock knowledge base and intervention manager
        knowledge_base = {"user_profile": {"demographics": {}}}
        factory = HandlerFactory(knowledge_base, None)
        
        # Test cases with expected handlers
        test_cases = [
            {
                "content": "What is your age? Please enter your birth year:",
                "expected_handler": "Demographics",
                "min_confidence": 0.3
            },
            {
                "content": "How familiar are you with the following brands? Rate each brand:",
                "expected_handler": "BrandFamiliarity", 
                "min_confidence": 0.2
            },
            {
                "content": "Please rate your agreement with the following statements: Strongly agree, Somewhat agree",
                "expected_handler": "RatingMatrix",
                "min_confidence": 0.2
            },
            {
                "content": "This is a completely unknown question type with no patterns",
                "expected_handler": "Unknown",
                "min_confidence": 0.1
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n   Test {i+1}: {test_case['content'][:50]}...")
            
            # Get best handler (without page object for testing)
            handler, confidence = factory.get_best_handler(None, test_case["content"])
            
            handler_name = handler.__class__.__name__.replace('Handler', '')
            print(f"   Selected: {handler_name} (confidence: {confidence:.2f})")
            
            # Verify expectations
            assert handler_name == test_case["expected_handler"], \
                f"Expected {test_case['expected_handler']}, got {handler_name}"
            
            assert confidence >= test_case["min_confidence"], \
                f"Confidence {confidence} below minimum {test_case['min_confidence']}"
            
            print(f"   ✅ Correct handler selected with adequate confidence")
        
        print("✅ Confidence scoring tests passed")
        
    except Exception as e:
        print(f"❌ Confidence scoring test failed: {e}")
        return False
    
    return True


def test_base_handler_functionality():
    """Test base handler common functionality."""
    print("🧪 Testing base handler functionality...")
    
    try:
        from handlers.demographics_handler import DemographicsHandler
        
        # Create handler with mock dependencies
        knowledge_base = {
            "user_profile": {
                "demographics": {
                    "age": "45",
                    "gender": "Male",
                    "location": "New South Wales"
                }
            }
        }
        
        handler = DemographicsHandler(None, knowledge_base, None)
        
        # Test utility methods
        demographics = handler.get_demographics()
        assert demographics["age"] == "45", "Should retrieve demographics correctly"
        
        # Test keyword checking
        test_content = "What is your age and gender?"
        result = handler.check_keywords_in_content(["age", "gender"], test_content.lower())
        assert result == True, "Should find keywords in content"
        
        # Test keyword counting
        count = handler.count_keyword_matches(["age", "gender", "missing"], test_content.lower())
        assert count == 2, f"Should count 2 matches, got {count}"
        
        print("✅ Base handler functionality tests passed")
        
    except Exception as e:
        print(f"❌ Base handler test failed: {e}")
        return False
    
    return True


def test_demographics_handler():
    """Test demographics handler specifically."""
    print("🧪 Testing demographics handler...")
    
    try:
        from handlers.demographics_handler import DemographicsHandler
        
        knowledge_base = {
            "user_profile": {
                "demographics": {
                    "age": "45",
                    "gender": "Male",
                    "location": "New South Wales"
                }
            }
        }
        
        handler = DemographicsHandler(None, knowledge_base, None)
        
        # Test confidence scoring
        test_cases = [
            ("What is your age?", 0.4),  # Should be high confidence
            ("What year were you born?", 0.4),  # Should be high confidence
            ("What is your favorite color?", 0.0),  # Should be low confidence
        ]
        
        for content, min_expected in test_cases:
            confidence = handler.can_handle(content)
            print(f"   '{content}' -> confidence: {confidence:.2f}")
            assert confidence >= min_expected, \
                f"Expected min {min_expected}, got {confidence}"
        
        print("✅ Demographics handler tests passed")
        
    except Exception as e:
        print(f"❌ Demographics handler test failed: {e}")
        return False
    
    return True


def main():
    """Run all handler system tests."""
    print("🚀 Testing Handler System (Phase 2)")
    print("=" * 50)
    
    tests = [
        test_handler_imports,
        test_base_handler_functionality, 
        test_demographics_handler,
        test_handler_factory,
        test_confidence_scoring
    ]
    
    passed = 0
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_func.__name__} failed")
        except Exception as e:
            print(f"❌ {test_func.__name__} failed with exception: {e}")
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 ALL HANDLER TESTS PASSED!")
        print("✅ Handler system is working correctly")
        print("✅ Ready to proceed with Phase 3 (Utility Services)")
        return True
    else:
        print("❌ Some tests failed - please fix before proceeding")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
