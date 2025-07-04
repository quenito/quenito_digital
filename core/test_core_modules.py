#!/usr/bin/env python3
"""
Test script for core modules extraction.
Validates that the browser management and session detection work correctly.
"""

import sys
import os

# Add the survey_automation directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from core.browser_manager import BrowserManager
from core.survey_detector import SurveyDetector
from core.navigation_controller import NavigationController


def test_browser_manager():
    """Test browser manager functionality."""
    print("🧪 Testing BrowserManager...")
    
    browser_manager = BrowserManager()
    
    # Test session stats
    stats = browser_manager.get_session_stats()
    assert isinstance(stats, dict), "Session stats should be a dictionary"
    assert "session_mode" in stats, "Session stats should have session_mode"
    
    # Test delay function
    import time
    start_time = time.time()
    browser_manager.human_like_delay(100, 200)  # Short delay for testing
    elapsed = time.time() - start_time
    assert 0.1 <= elapsed <= 0.25, f"Delay should be between 0.1-0.25s, got {elapsed}"
    
    print("✅ BrowserManager tests passed!")


def test_survey_detector():
    """Test survey detector functionality."""
    print("🧪 Testing SurveyDetector...")
    
    detector = SurveyDetector()
    
    # Test domain detection
    test_urls = [
        ("https://survey.cmix.com/12345/test", True),
        ("https://qualtrics.com/survey/123", True),
        ("https://myopinions.com.au/dashboard", False),
        ("https://google.com", False),
        ("https://yoursurveynow.com/survey", True)
    ]
    
    for url, expected in test_urls:
        # Create a mock page object
        class MockPage:
            def inner_text(self, selector):
                return "test survey content what is your age rate your experience"
            def title(self):
                return "Survey Page"
        
        mock_page = MockPage()
        result = detector.is_survey_tab(url, mock_page)
        assert result == expected, f"URL {url} should return {expected}, got {result}"
    
    print("✅ SurveyDetector tests passed!")


def test_navigation_controller():
    """Test navigation controller functionality."""
    print("🧪 Testing NavigationController...")
    
    nav_controller = NavigationController()
    
    # Test navigation stats
    stats = nav_controller.get_navigation_stats()
    assert isinstance(stats, dict), "Navigation stats should be a dictionary"
    assert "buttons_found_automatically" in stats, "Should track button detection"
    
    # Test human-like delay
    import time
    start_time = time.time()
    nav_controller._human_like_delay(50, 100)  # Short delay for testing
    elapsed = time.time() - start_time
    assert 0.05 <= elapsed <= 0.15, f"Delay should be between 0.05-0.15s, got {elapsed}"
    
    print("✅ NavigationController tests passed!")


def test_integration():
    """Test integration between modules."""
    print("🧪 Testing module integration...")
    
    # Test that modules can be imported and instantiated together
    browser_manager = BrowserManager()
    survey_detector = SurveyDetector()
    nav_controller = NavigationController()
    
    # Test that they have expected interfaces
    assert hasattr(browser_manager, 'create_persistent_browser_session'), "BrowserManager missing key method"
    assert hasattr(survey_detector, 'detect_and_switch_to_survey_tab'), "SurveyDetector missing key method"
    assert hasattr(nav_controller, 'find_and_click_next_button'), "NavigationController missing key method"
    
    print("✅ Integration tests passed!")


def main():
    """Run all tests."""
    print("🚀 Testing Core Modules Extraction")
    print("=" * 50)
    
    try:
        test_browser_manager()
        test_survey_detector()
        test_navigation_controller()
        test_integration()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Core modules are working correctly")
        print("✅ Ready to proceed with Phase 2 (Handler System)")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("🔧 Please fix the issue before proceeding")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)