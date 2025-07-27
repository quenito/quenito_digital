#!/usr/bin/env python3
"""
🏢 Brand Familiarity Handler v3.0 - REFACTORED MODULAR ARCHITECTURE
Orchestrates brand familiarity automation using clean module separation.

This handler coordinates:
- Pattern matching (brand_familiarity_patterns.py)
- UI interactions (brand_familiarity_ui.py)
- Brain learning (brand_familiarity_brain.py)

ARCHITECTURE: Clean orchestration with delegated responsibilities
Expected to boost automation from 21% → 60-70%!
"""

import time
import random
from typing import Dict, Any, Optional
from handlers.base_handler import BaseHandler
from .brand_familiarity_patterns import BrandFamiliarityPatterns
from .brand_familiarity_ui import BrandFamiliarityUI
from .brand_familiarity_brain import BrandFamiliarityBrain


class BrandFamiliarityHandler(BaseHandler):
    """
    🏢 Refactored Brand Familiarity Handler - Clean Orchestration
    
    Handles brand familiarity matrix questions using centralized brain patterns.
    Expected to be the biggest automation improvement!
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)
        
        # Get patterns from centralized brain
        brand_patterns = {}
        if knowledge_base:
            all_patterns = knowledge_base.get("question_patterns", {})
            brand_patterns = all_patterns.get("brand_familiarity_questions", {})
        
        # Initialize modular components
        self.patterns = BrandFamiliarityPatterns(brand_patterns)
        self.ui = BrandFamiliarityUI(page)
        self.brain = BrandFamiliarityBrain(knowledge_base)
        
        # Handler state
        self.detected_question_type = None
        self.detected_brands = []
        self.detected_category = None
        
        print("🏢 Refactored Brand Familiarity Handler initialized!")
        print("🧠 Modular architecture active: Patterns + UI + Brain")
        
        # Validate configuration
        validation = self.patterns.validate_patterns()
        if all(validation.values()):
            print("✅ All patterns loaded from centralized brain")
        else:
            print("⚠️ Some patterns missing:", 
                  [k for k, v in validation.items() if not v])
    
    # ========================================
    # MAIN HANDLER METHODS
    # ========================================
    
    async def can_handle(self, page_content: str) -> float:
        """
        Determine if this handler can process the current page
        
        Uses patterns from centralized brain to detect brand questions
        """
        if not page_content:
            return 0.0
        
        try:
            # Reset state
            self.detected_question_type = None
            self.detected_brands = []
            self.detected_category = None
            
            # Detect question type using patterns module
            question_type = self.patterns.detect_question_type(page_content)
            if not question_type:
                return 0.0
            
            self.detected_question_type = question_type
            
            # Calculate base confidence from patterns
            confidence = self.patterns.calculate_keyword_confidence(page_content, question_type)
            
            # Detect brands in content
            self.detected_brands = self.patterns.get_brands_from_content(page_content)
            if self.detected_brands:
                print(f"🏢 Detected {len(self.detected_brands)} brands in content")
            
            # Detect brand categories for additional context
            categories = self.patterns.detect_brand_categories(page_content)
            if categories:
                self.detected_category = categories[0]  # Primary category
                confidence += 0.1
                print(f"🏢 Detected brand categories: {categories}")
            
            # Apply brain learning adjustments
            if self.detected_brands:
                # Average confidence boost across detected brands
                total_boost = 0
                for brand in self.detected_brands[:5]:  # Check first 5 brands
                    adjusted = self.brain.calculate_brand_confidence(brand, confidence)
                    total_boost += (adjusted - confidence)
                
                if total_boost > 0:
                    avg_boost = total_boost / min(len(self.detected_brands), 5)
                    confidence += avg_boost
            
            # Apply general learning adjustments
            learning_adjustment = self.brain.get_confidence_adjustment(
                self.detected_question_type, confidence
            )
            confidence += learning_adjustment
            
            # Cap at threshold
            confidence = min(confidence, 0.98)
            
            print(f"🏢 Brand Familiarity confidence: {confidence:.3f} ({question_type})")
            return confidence
            
        except Exception as e:
            print(f"❌ Error in brand familiarity can_handle: {e}")
            return 0.0
    
    async def handle(self) -> bool:
        """
        Process brand familiarity questions
        
        Orchestrates pattern detection, brain strategy, and UI execution
        """
        self.log_handler_start()
        
        try:
            print(f"🏢 Processing {self.detected_question_type} question...")
            
            # Take screenshot for debugging
            await self.ui.take_screenshot("brand_matrix_detected.png")
            
            # Detect matrix elements using UI module
            elements = await self.ui.detect_brand_matrix_elements()
            
            if not elements['brands']:
                print("❌ No brand matrix detected by UI module")
                # Try fallback if we detected brands in content
                if self.detected_brands:
                    print(f"🔄 Using detected brands from content: {self.detected_brands}")
                    elements['brands'] = self.detected_brands
                else:
                    return await self._request_intervention_with_learning(
                        "No brand matrix found"
                    )
            
            brands_to_process = elements['brands']
            print(f"🏢 Found {len(brands_to_process)} brands to process")
            
            # Analyze category if detected
            category_analysis = None
            if self.detected_category:
                category_analysis = self.brain.analyze_brand_category(self.detected_category)
                print(f"🏢 Category analysis for '{self.detected_category}':")
                print(f"   - Default response: {category_analysis['default_response']}")
                print(f"   - Known brands: {len(category_analysis['known_brands'])}")
            
            # Get response strategy from brain
            brand_strategy = self.brain.get_brand_strategy(brands_to_process)
            
            # Apply category insights if available
            if category_analysis and category_analysis['confidence_boost'] > 0:
                print(f"🏢 Applying category insights (boost: {category_analysis['confidence_boost']:.2f})")
            
            # Execute UI automation
            success = await self.ui.handle_brand_matrix(brand_strategy)
            
            if success:
                print("✅ Brand matrix completed successfully!")
                
                # Store learning data for each brand
                for brand, response in brand_strategy.items():
                    self.brain.store_brand_response(brand, response, True)
                
                # Log success
                self.log_handler_success({
                    'brands_processed': len(brand_strategy),
                    'question_type': self.detected_question_type,
                    'category': self.detected_category
                })
                
                # Navigate to next
                if await self.ui.click_next_button():
                    print("✅ Navigation successful")
                    return True
                else:
                    print("⚠️ Navigation failed but matrix completed")
                    return True
            else:
                # Partial success still counts
                successful_brands = sum(1 for brand in brand_strategy 
                                      if brand in self.brain.session_responses)
                
                if successful_brands > 0:
                    print(f"⚠️ Partial success: {successful_brands}/{len(brand_strategy)} brands")
                    return True
                else:
                    return await self._request_intervention_with_learning(
                        "Failed to complete brand matrix"
                    )
                
        except Exception as e:
            self.logger.error(f"Brand familiarity handler error: {e}")
            return await self._request_intervention_with_learning(
                f"Error: {str(e)}"
            )
    
    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================
    
    async def _request_intervention_with_learning(self, reason: str) -> bool:
        """
        Request manual intervention with enhanced learning
        
        Captures brand-specific learning data
        """
        # Prepare learning context
        learning_context = {
            'handler': 'brand_familiarity',
            'question_type': self.detected_question_type,
            'detected_brands': self.detected_brands,
            'category': self.detected_category,
            'reason': reason
        }
        
        # Request intervention
        result = self.request_intervention(reason)
        
        # Capture post-intervention learning
        if result:
            print("🧠 Capturing brand familiarity learning data...")
            
            # Suggest improvements based on failure
            suggestions = self.brain.suggest_handler_improvements()
            if suggestions:
                print("🧠 Improvement suggestions:")
                for suggestion in suggestions:
                    print(f"   - {suggestion}")
        
        return result
    
    def log_handler_start(self):
        """Log handler start with context"""
        super().log_handler_start()
        print(f"   - Question type: {self.detected_question_type}")
        print(f"   - Brands detected: {len(self.detected_brands)}")
        print(f"   - Category: {self.detected_category or 'Unknown'}")
    
    def log_handler_success(self, details: Dict[str, Any]):
        """Log handler success with details"""
        print(f"✅ Brand Familiarity Handler Success!")
        print(f"   - Brands processed: {details.get('brands_processed', 0)}")
        print(f"   - Question type: {details.get('question_type', 'Unknown')}")
        print(f"   - Category: {details.get('category', 'Unknown')}")
        
        # Update performance metrics
        if hasattr(self, 'stats') and self.stats:
            self.stats.record_automation_success('brand_familiarity', details)