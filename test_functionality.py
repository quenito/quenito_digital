# Create test_functionality.py
#!/usr/bin/env python3
import asyncio

async def test_rating_matrix_functionality():
    from handlers.rating_matrix.rating_matrix_handler import RatingMatrixHandler
    
    # Mock knowledge base
    mock_kb = {
        "rating_matrices": {
            "brand_familiarity": {
                "patterns": ["familiar", "familiarity", "brand awareness"],
                "confidence_threshold": 0.7
            }
        }
    }
    
    class MockKB:
        def get(self, key, default=None):
            return mock_kb.get(key, default)
    
    # Create handler instance
    handler = RatingMatrixHandler(None, MockKB(), None)
    
    # Test content
    test_content = "How familiar are you with these brands? Rate each brand below."
    
    # Test confidence calculation
    confidence = await handler.can_handle(test_content)
    print(f"Confidence for brand familiarity content: {confidence:.3f}")
    print(f"Detected type: {handler.detected_matrix_type}")
    
    # Test with list input (this was the bug we fixed)
    list_content = ["How familiar", "are you with", "these brands?"]
    confidence2 = await handler.can_handle(list_content)
    print(f"\nConfidence for list input: {confidence2:.3f}")
    print("✅ List input handled correctly - no attribute error!")

asyncio.run(test_rating_matrix_functionality())