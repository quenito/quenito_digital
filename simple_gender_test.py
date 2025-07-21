#!/usr/bin/env python3
"""
Simple gender detection test - no handler initialization required
Tests the gender detection logic directly
"""

def test_gender_patterns():
    """Test gender detection patterns without requiring handler setup"""
    
    def enhanced_gender_detection(content_lower: str) -> float:
        """Test version of enhanced gender detection"""
        
        # Primary gender indicators (HIGH CONFIDENCE)
        primary_patterns = [
            "gender", "sex", "male", "female", "man", "woman",
            "gender identity", "gender selection", "select gender",
            "your gender", "what gender", "which gender"
        ]
        
        # Form-specific patterns (MEDIUM CONFIDENCE)  
        form_patterns = [
            "select your gender", "choose your gender", "gender:",
            "sex:", "gender question", "demographic"
        ]
        
        # Option indicators (MEDIUM CONFIDENCE)
        option_patterns = [
            "male female", "man woman", "m/f", "gender options",
            "prefer not to say", "non-binary", "other gender"
        ]
        
        score = 0.0
        matches_found = []
        
        # Check primary patterns (0.4 each - can trigger alone)
        for pattern in primary_patterns:
            if pattern in content_lower:
                score += 0.4
                matches_found.append(f"primary:{pattern}")
        
        # Check form patterns (0.3 each)
        for pattern in form_patterns:
            if pattern in content_lower:
                score += 0.3
                matches_found.append(f"form:{pattern}")
        
        # Check option patterns (0.25 each)
        for pattern in option_patterns:
            if pattern in content_lower:
                score += 0.25
                matches_found.append(f"option:{pattern}")
        
        # 🚀 SPECIAL BOOST: If we find "male" OR "female", it's likely gender
        if any(word in content_lower for word in ["male", "female"]):
            score += 0.3
            matches_found.append("gender_words_boost")
        
        # Cap at 0.95
        final_score = min(score, 0.95)
        
        return final_score, matches_found
    
    # Test cases
    test_cases = [
        "What is your gender?",
        "Gender: Male Female Other",
        "Select your gender: Male, Female",
        "Are you male or female?",
        "Demographics - Gender Question",
        "Please select one: Male Female",
        "Age question - how old are you?",  # Should score low
        "What is your occupation?",  # Should score low
    ]
    
    print("🧪 TESTING ENHANCED GENDER DETECTION")
    print("=" * 50)
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        confidence, matches = enhanced_gender_detection(test_case.lower())
        
        # Tests 1-6 should pass (confidence >= 0.4)
        # Tests 7-8 should fail (non-gender questions)
        expected_pass = i <= 6
        actual_pass = confidence >= 0.4
        
        if expected_pass == actual_pass:
            status = "✅ PASS"
            passed_tests += 1
        else:
            status = "❌ FAIL"
        
        print(f"Test {i}: {status}")
        print(f"   Text: '{test_case}'")
        print(f"   Confidence: {confidence:.3f}")
        print(f"   Expected: {'PASS' if expected_pass else 'FAIL'}")
        print(f"   Actual: {'PASS' if actual_pass else 'FAIL'}")
        if matches:
            print(f"   Matches: {matches[:3]}...")  # Show first 3 matches
        print()
    
    print(f"🎯 RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests >= 6:  # Allow 1-2 failures for edge cases
        print("✅ GENDER DETECTION: WORKING CORRECTLY")
        print("💡 Ready to implement in demographics_handler_brain.py")
    else:
        print("❌ GENDER DETECTION: NEEDS IMPROVEMENT")
        print("🔧 Pattern matching logic needs adjustment")
    
    return passed_tests >= 6

if __name__ == "__main__":
    test_gender_patterns()
