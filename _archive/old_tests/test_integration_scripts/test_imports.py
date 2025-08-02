#!/usr/bin/env python3
print("Testing rating_matrix imports...")

try:
    from handlers.rating_matrix.rating_matrix_handler import RatingMatrixHandler
    print("✅ rating_matrix_handler imported")
    
    from handlers.rating_matrix.rating_matrix_patterns import RatingMatrixPatterns
    print("✅ rating_matrix_patterns imported")
    
    from handlers.rating_matrix.rating_matrix_ui import RatingMatrixUI
    print("✅ rating_matrix_ui imported")
    
    from handlers.rating_matrix.rating_matrix_brain import RatingMatrixBrain
    print("✅ rating_matrix_brain imported")
    
    print("\n🎉 All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")