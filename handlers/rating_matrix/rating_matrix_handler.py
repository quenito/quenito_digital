#!/usr/bin/env python3
"""
📊 Rating Matrix Handler v2.0 - REFACTORED MODULAR ARCHITECTURE
Orchestrates rating matrix automation using clean module separation.

This handler coordinates:
- Pattern matching (rating_matrix_patterns.py)
- UI interactions (rating_matrix_ui.py) 
- Brain learning (rating_matrix_brain.py)

Handles brand familiarity matrices, satisfaction grids, and rating scales.

ARCHITECTURE: Clean orchestration with delegated responsibilities
"""

import time
import random
from typing import Dict, List, Any, Optional, Tuple
from handlers.base_handler import BaseHandler
from .rating_matrix_patterns import RatingMatrixPatterns
from .rating_matrix_ui import RatingMatrixUI
from .rating_matrix_brain import RatingMatrixBrain


class RatingMatrixHandler(BaseHandler):
    """
    📊 Refactored Rating Matrix Handler - Clean Orchestration
    
    Coordinates pattern matching, UI interaction, and brain learning
    for automated rating matrix and brand familiarity handling.
    """
    
    def __init__(self, page, knowledge_base, intervention_manager):
        """Initialize handler with modular components"""
        super().__init__(page, knowledge_base, intervention_manager)

        # Get patterns from knowledge base (UPDATED)
        question_patterns = knowledge_base.get("question_patterns", {})
        rating_patterns = question_patterns.get("rating_matrix_questions", {})

        # Initialize modular components
        self.patterns = RatingMatrixPatterns(rating_patterns)
        self.ui = RatingMatrixUI(page)
        self.brain = RatingMatrixBrain(knowledge_base)
            
        # Handler state
        self.detected_matrix_type = None
        self.last_confidence = 0.0
        self.detected_brands = []
        self.detected_attributes = []
        
        # Human behavior simulation
        self.wpm = random.randint(40, 80)
        self.thinking_speed = random.uniform(0.8, 1.3)
        self.decision_confidence = random.uniform(0.7, 1.2)
        
        print("📊 Refactored Rating Matrix Handler initialized!")
        print("🧠 Modular architecture active: Patterns + UI + Brain")
        print(f"⏱️ Human simulation: {self.wpm} WPM, thinking {self.thinking_speed:.1f}x")
    
    # ========================================
    # MAIN HANDLER METHODS
    # ========================================
    
    async def can_handle(self, page_content: str) -> float:
        """Determine if this handler can process the current page"""
        if not page_content:
            return 0.0
        
        try:
            # FIX for 'list' attribute error - ensure string type
            if isinstance(page_content, list):
                page_content = ' '.join(str(item) for item in page_content)
            elif not isinstance(page_content, str):
                page_content = str(page_content)
            
            confidence = await self.get_confidence(page_content)
            print(f"📊 Rating Matrix confidence: {confidence:.3f}")
            return confidence
            
        except Exception as e:
            print(f"❌ Error in rating matrix can_handle: {e}")
            return 0.0
    
    async def get_confidence(self, page_content: str) -> float:
        """Calculate confidence score for rating matrix detection"""
        if not page_content:
            return 0.0
        
        try:
            # Ensure string type
            if not isinstance(page_content, str):
                page_content = str(page_content)
            
            content_lower = page_content.lower()
            
            # Use patterns module to detect matrix type
            detected_type = self.patterns.detect_matrix_type(page_content)
            
            if detected_type:
                # Calculate keyword confidence
                base_confidence = self.patterns.calculate_keyword_confidence(page_content, detected_type)
                
                # Detect brands and attributes
                self.detected_brands = self.patterns.extract_brands(page_content)
                self.detected_attributes = self.patterns.extract_attributes(page_content, detected_type)
                
                # Apply brain learning adjustments
                adjustment = self.brain.get_confidence_adjustment(detected_type, base_confidence)
                final_confidence = min(base_confidence + adjustment, 1.0)
                
                # Store detection results
                self.detected_matrix_type = detected_type
                self.last_confidence = final_confidence
                self.brain.set_detected_matrix_type(detected_type)
                
                print(f"🎯 Detected: {detected_type} matrix (confidence: {final_confidence:.3f})")
                print(f"🏷️ Brands found: {len(self.detected_brands)}")
                print(f"📊 Attributes: {self.detected_attributes[:3]}...")  # Show first 3
                
                return final_confidence
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error calculating confidence: {e}")
            return 0.0
    
    async def handle(self) -> bool:
        """Main handler execution - orchestrates the automation"""
        print(f"📊 Rating Matrix Handler starting...")
        
        if not self.page:
            print("❌ No page available")
            return False
        
        try:
            # Apply reading delay
            self.page_analysis_delay()
            
            # Get page content
            page_content = await self._get_page_content()
            
            # Detect matrix type if not already done
            if not self.detected_matrix_type:
                self.detected_matrix_type = self.patterns.detect_matrix_type(page_content)
                self.detected_brands = self.patterns.extract_brands(page_content)
                self.detected_attributes = self.patterns.extract_attributes(page_content, self.detected_matrix_type)
            
            if self.detected_matrix_type:
                print(f"📊 Processing {self.detected_matrix_type} matrix")
                print(f"🏷️ Brands to rate: {self.detected_brands}")
                
                # Process the rating matrix
                success = await self.process_rating_matrix(
                    self.detected_matrix_type,
                    self.detected_brands,
                    self.detected_attributes,
                    page_content
                )
                
                if success:
                    # Try navigation
                    nav_success = await self.ui.try_navigation()
                    if nav_success:
                        print("✅ Rating matrix automated + navigation successful!")
                    return True
                
                return False
            else:
                print("⚠️ Could not identify rating matrix type")
                await self.brain.report_failure(
                    "Unknown matrix type",
                    page_content[:200],
                    confidence_score=self.last_confidence
                )
                return False
                
        except Exception as e:
            print(f"❌ Error in rating matrix handler: {e}")
            await self.brain.report_failure(str(e), "", confidence_score=self.last_confidence)
            return False
    
    # ========================================
    # MATRIX PROCESSING
    # ========================================
    
    async def process_rating_matrix(self, matrix_type: str, brands: List[str], 
                                   attributes: List[str], page_content: str) -> bool:
        """Process a rating matrix by filling in ratings for each brand"""
        start_time = time.time()
        
        try:
            # Step 1: Detect matrix structure on page
            matrix_info = await self.ui.detect_matrix_structure()
            if not matrix_info:
                print("❌ Could not detect matrix structure")
                return False
            
            print(f"📊 Found matrix: {matrix_info['rows']} rows x {matrix_info['cols']} columns")
            
            # Step 2: Process each brand
            success_count = 0
            total_ratings = len(brands) * (len(attributes) if attributes else 1)
            
            for brand_idx, brand in enumerate(brands):
                print(f"\n🏷️ Rating brand {brand_idx + 1}/{len(brands)}: {brand}")
                
                # Check for learned ratings
                learned_ratings = await self.brain.get_learned_ratings(brand, matrix_type)
                
                if matrix_type == 'brand_familiarity':
                    # Single rating per brand
                    rating = learned_ratings.get('familiarity') if learned_ratings else None
                    if not rating:
                        rating = self.brain.get_brand_familiarity_rating(brand)
                    
                    if await self.ui.rate_brand_familiarity(brand_idx, rating, matrix_info):
                        success_count += 1
                        await self.brain.save_rating(brand, matrix_type, {'familiarity': rating})
                        
                elif matrix_type == 'satisfaction_matrix':
                    # Multiple attributes per brand
                    for attr_idx, attribute in enumerate(attributes):
                        rating = learned_ratings.get(attribute) if learned_ratings else None
                        if not rating:
                            rating = self.brain.get_satisfaction_rating(brand, attribute)
                        
                        if await self.ui.rate_satisfaction_cell(brand_idx, attr_idx, rating, matrix_info):
                            success_count += 1
                            await self.brain.save_rating(brand, matrix_type, {attribute: rating})
                
                # Human-like delay between brands
                self.thinking_delay()
            
            # Calculate success rate
            success_rate = success_count / total_ratings if total_ratings > 0 else 0
            execution_time = time.time() - start_time
            
            if success_rate >= 0.8:  # 80% threshold for success
                print(f"✅ Matrix automation successful! ({success_count}/{total_ratings} ratings)")
                await self.brain.report_success(
                    strategy_used="matrix_grid_navigation",
                    execution_time=execution_time,
                    matrix_type=matrix_type,
                    brands_processed=len(brands),
                    success_rate=success_rate,
                    confidence_score=self.last_confidence
                )
                return True
            else:
                print(f"⚠️ Matrix automation partial: {success_count}/{total_ratings}")
                await self.brain.report_failure(
                    f"Low success rate: {success_rate:.1%}",
                    page_content[:200],
                    matrix_type=matrix_type,
                    confidence_score=self.last_confidence
                )
                return False
                
        except Exception as e:
            print(f"❌ Error processing rating matrix: {e}")
            await self.brain.report_failure(
                str(e),
                page_content[:200],
                matrix_type=matrix_type,
                confidence_score=self.last_confidence
            )
            return False
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    async def _get_page_content(self) -> str:
        """Get page content with fallback strategies"""
        try:
            # Try standard method
            content = await self.page.locator('body').text_content()
            if content:
                return content
        except:
            pass
        
        try:
            # Try JavaScript evaluation
            content = await self.page.evaluate('() => document.body.textContent')
            if content:
                return content
        except:
            pass
        
        # Fallback
        return "Unable to extract page content"
    
    def page_analysis_delay(self):
        """Human-like delay for page analysis"""
        delay = random.uniform(0.5, 2.0) * self.thinking_speed
        time.sleep(delay)
        print(f"🧠 Page analysis delay: {delay:.2f}s")
    
    def thinking_delay(self):
        """Human-like delay between rating decisions"""
        delay = random.uniform(0.3, 1.0) * self.thinking_speed
        time.sleep(delay)
    
    def human_like_delay(self, action_type: str = "general"):
        """Human-like delays for different actions"""
        if action_type == "thinking":
            delay = random.uniform(0.8, 2.5) / self.thinking_speed
        elif action_type == "decision":
            delay = random.uniform(0.5, 1.5) / self.decision_confidence
        elif action_type == "clicking":
            delay = random.uniform(0.2, 0.5)
        else:
            delay = random.uniform(0.3, 1.0)
        
        time.sleep(delay)
        print(f"⏱️ Human delay ({action_type}): {delay:.2f}s")