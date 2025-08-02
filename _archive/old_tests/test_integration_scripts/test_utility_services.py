#!/usr/bin/env python3
"""
Test script for utility services (Phase 3).
Validates knowledge base, intervention manager, research engine, and reporting.
"""

import sys
import os
import tempfile
import json

# Add the survey_automation directory to the path
sys.path.insert(0, os.path.dirname(__file__))


def test_knowledge_base():
    """Test knowledge base functionality."""
    print("🧪 Testing KnowledgeBase...")
    
    try:
        from utils.knowledge_base import KnowledgeBase
        
        # Create temporary knowledge base file
        temp_kb_data = {
            "user_profile": {
                "demographics": {
                    "age": "45",
                    "gender": "Male",
                    "location": "New South Wales"
                },
                "existing_brands": {
                    "currently_use": ["Netflix", "Spotify"],
                    "familiar_with": ["Samsung", "LG"]
                }
            },
            "question_patterns": {
                "demographics_questions": {
                    "keywords": ["age", "gender", "location"]
                }
            }
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(temp_kb_data, f)
            temp_path = f.name
        
        try:
            # Test knowledge base loading
            kb = KnowledgeBase(temp_path)
            
            # Test data access methods
            demographics = kb.get_demographics()
            assert demographics["age"] == "45", "Should retrieve demographics correctly"
            
            brands = kb.get_known_brands("currently_use")
            assert "Netflix" in brands, "Should retrieve brand preferences"
            
            patterns = kb.get_question_patterns()
            assert "demographics_questions" in patterns, "Should retrieve question patterns"
            
            # Test research caching
            kb.add_research_result("test query", [{"title": "Test", "content": "Test content"}])
            cached = kb.get_research_result("test query")
            assert cached is not None, "Should cache and retrieve research results"
            
            # Test saving
            kb.set("test_key", "test_value")
            assert kb.save(), "Should save successfully"
            
            print("✅ KnowledgeBase tests passed")
            
        finally:
            # Clean up
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"❌ KnowledgeBase test failed: {e}")
        return False
    
    return True


def test_intervention_manager():
    """Test intervention manager functionality."""
    print("🧪 Testing InterventionManager...")
    
    try:
        from utils.intervention_manager import InterventionManager
        
        manager = InterventionManager()
        
        # Test initial state
        stats = manager.get_intervention_stats()
        assert stats["total_interventions"] == 0, "Should start with zero interventions"
        
        # Test intervention recording (without actual user input)
        # We'll mock the input function for testing
        import builtins
        original_input = builtins.input
        builtins.input = lambda prompt: ""  # Mock input to return immediately
        
        try:
            # Test intervention request
            result = manager.request_manual_intervention(
                "test_question_type", 
                "test reason", 
                "test page content"
            )
            assert result == True, "Should handle intervention request"
            
            # Check statistics were updated
            updated_stats = manager.get_intervention_stats()
            assert updated_stats["total_interventions"] == 1, "Should increment intervention count"
            assert "test_question_type" in updated_stats["intervention_types"], "Should track intervention types"
            
            # Test reporting
            report = manager.generate_improvement_report()
            assert len(report) > 0, "Should generate improvement report"
            
            print("✅ InterventionManager tests passed")
            
        finally:
            # Restore original input function
            builtins.input = original_input
            
    except Exception as e:
        print(f"❌ InterventionManager test failed: {e}")
        return False
    
    return True


def test_research_engine():
    """Test research engine functionality."""
    print("🧪 Testing ResearchEngine...")
    
    try:
        from utils.research_engine import ResearchEngine
        from utils.knowledge_base import KnowledgeBase
        
        # Create mock knowledge base
        kb = KnowledgeBase()
        kb.data = {"research_cache": {}}  # Start with empty cache
        
        research_engine = ResearchEngine(kb)
        
        # Test research operation
        results = research_engine.research_unknown_content(
            "What is the stadium name?",
            ["stadium", "venue", "location"]
        )
        
        # Should return mock results
        assert isinstance(results, list), "Should return list of results"
        
        # Test brand research
        brands = research_engine.research_brand_category("electronics")
        assert isinstance(brands, list), "Should return list of brands"
        
        # Test statistics
        stats = research_engine.get_research_stats()
        assert stats["total_searches"] > 0, "Should track search operations"
        
        # Test cache functionality
        cache_hit_rate = research_engine.get_cache_hit_rate()
        assert isinstance(cache_hit_rate, float), "Should calculate cache hit rate"
        
        success_rate = research_engine.get_success_rate()
        assert isinstance(success_rate, float), "Should calculate success rate"
        
        print("✅ ResearchEngine tests passed")
        
    except Exception as e:
        print(f"❌ ResearchEngine test failed: {e}")
        return False
    
    return True


def test_reporting():
    """Test reporting functionality."""
    print("🧪 Testing ReportGenerator...")
    
    try:
        from utils.reporting import ReportGenerator
        
        reporter = ReportGenerator()
        
        # Create mock statistics
        survey_stats = {
            "total_questions": 20,
            "automated_questions": 18,
            "manual_interventions": 2,
            "research_performed": 1,
            "start_time": 1000,
            "end_time": 1300  # 5 minutes
        }
        
        session_stats = {
            "session_mode": "persistent",
            "start_time": 1000,
            "manual_navigation_time": 1100,
            "automation_start_time": 1200,
            "dashboard_url": "https://myopinions.com.au/dashboard",
            "survey_url": "https://survey.example.com/test",
            "session_transfers": 1
        }
        
        handler_stats = {
            "total_selections": 20,
            "handler_usage": {
                "Demographics": 5,
                "BrandFamiliarity": 3,
                "RatingMatrix": 8,
                "Unknown": 4
            },
            "confidence_scores": [0.8, 0.7, 0.9, 0.6]
        }
        
        intervention_stats = {
            "total_interventions": 2,
            "intervention_types": {
                "unknown": 1,
                "demographics": 1
            },
            "total_manual_time": 120
        }
        
        research_stats = {
            "total_searches": 1,
            "cache_hits": 0,
            "cache_misses": 1,
            "failed_searches": 0
        }
        
        # Test report generation
        full_report = reporter.generate_survey_report(
            survey_stats, session_stats, handler_stats, 
            intervention_stats, research_stats
        )
        
        assert len(full_report) > 0, "Should generate full report"
        assert "ENHANCED SURVEY AUTOMATION REPORT" in full_report, "Should include report title"
        assert "90.0%" in full_report, "Should calculate automation rate correctly"
        
        # Test quick summary
        quick_summary = reporter.generate_quick_summary(survey_stats)
        assert len(quick_summary) > 0, "Should generate quick summary"
        assert "20 questions" in quick_summary, "Should include question count"
        
        # Test export functionality
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            success = reporter.export_report(full_report, temp_path)
            assert success, "Should export report successfully"
            
            # Verify file was created and contains content
            with open(temp_path, 'r') as f:
                content = f.read()
            assert len(content) > 0, "Exported file should contain content"
            assert "ENHANCED SURVEY AUTOMATION REPORT" in content, "Should export correct content"
            
        finally:
            os.unlink(temp_path)
        
        print("✅ ReportGenerator tests passed")
        
    except Exception as e:
        print(f"❌ ReportGenerator test failed: {e}")
        return False
    
    return True


def test_utility_integration():
    """Test integration between utility services."""
    print("🧪 Testing utility services integration...")
    
    try:
        from utils.knowledge_base import KnowledgeBase
        from utils.intervention_manager import InterventionManager
        from utils.research_engine import ResearchEngine
        from utils.reporting import ReportGenerator
        
        # Create integrated system
        kb = KnowledgeBase()
        intervention_manager = InterventionManager()
        research_engine = ResearchEngine(kb)
        reporter = ReportGenerator()
        
        # Test that they work together
        assert hasattr(kb, 'get_demographics'), "KnowledgeBase should have required methods"
        assert hasattr(intervention_manager, 'get_intervention_stats'), "InterventionManager should have required methods"
        assert hasattr(research_engine, 'research_unknown_content'), "ResearchEngine should have required methods"
        assert hasattr(reporter, 'generate_survey_report'), "ReportGenerator should have required methods"
        
        # Test data flow
        stats = intervention_manager.get_intervention_stats()
        research_stats = research_engine.get_research_stats()
        
        # These should be compatible with reporter
        mock_survey_stats = {"total_questions": 1, "automated_questions": 1, "manual_interventions": 0}
        mock_session_stats = {"session_mode": "test"}
        mock_handler_stats = {"total_selections": 1, "handler_usage": {}}
        
        report = reporter.generate_survey_report(
            mock_survey_stats, mock_session_stats, mock_handler_stats, stats, research_stats
        )
        
        assert len(report) > 0, "Should generate integrated report"
        
        print("✅ Utility services integration tests passed")
        
    except Exception as e:
        print(f"❌ Utility integration test failed: {e}")
        return False
    
    return True


def main():
    """Run all utility services tests."""
    print("🚀 Testing Utility Services (Phase 3)")
    print("=" * 50)
    
    tests = [
        test_knowledge_base,
        test_intervention_manager,
        test_research_engine,
        test_reporting,
        test_utility_integration
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
        print("🎉 ALL UTILITY SERVICE TESTS PASSED!")
        print("✅ Utility services are working correctly")
        print("✅ Ready to proceed with Phase 4 (Main Entry Point)")
        return True
    else:
        print("❌ Some tests failed - please fix before proceeding")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
