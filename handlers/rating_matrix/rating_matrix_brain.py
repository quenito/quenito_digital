#!/usr/bin/env python3
"""
🧠 Rating Matrix Brain Module v2.0 - Learning & Intelligence Integration
Connects rating matrix handling to Quenito's central knowledge base.

This module manages:
- Learning from successful matrix automations
- Storing and retrieving brand ratings
- Tracking satisfaction scores
- Applying learned patterns to new matrices
- Reporting successes/failures for continuous improvement

ARCHITECTURE: Bridge between rating matrix handler and knowledge base
"""

import time
import random
from typing import Dict, Any, Optional, List, Tuple


class RatingMatrixBrain:
    """
    🧠 Brain Integration for Rating Matrices
    
    Manages all learning and intelligence for rating matrices:
    - Learns optimal ratings for brands
    - Remembers satisfaction patterns
    - Applies successful strategies
    - Reports outcomes for continuous learning
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize brain integration with knowledge base
        
        Args:
            knowledge_base: Reference to Quenito's central knowledge base
        """
        self.brain = knowledge_base
        self.last_matrix_type = None
        self.last_strategy_used = None
        self.rating_history = {}
        print("🧠 RatingMatrixBrain initialized with knowledge base connection")
    
    # ========================================
    # LEARNED RATING RETRIEVAL
    # ========================================
    
    async def get_learned_ratings(self, brand: str, matrix_type: str) -> Optional[Dict[str, int]]:
        """
        Get previously learned ratings for a brand
        
        Returns dict like: {'familiarity': 4, 'quality': 5, 'value': 3}
        """
        try:
            if not self.brain:
                return None
            
            # Check learned ratings in knowledge base
            learned_ratings = self.brain.get("learned_ratings", {})
            
            # Create key for this brand-matrix combination
            brand_key = f"{matrix_type}_{brand.lower().replace(' ', '_')}"
            
            if brand_key in learned_ratings:
                rating_data = learned_ratings[brand_key]
                print(f"🎯 Found learned ratings for {brand}: {rating_data}")
                return rating_data.get('ratings', {})
            
            # Check brand familiarity patterns
            if matrix_type == 'brand_familiarity':
                # Look for brand category patterns
                brand_patterns = self.brain.get("brand_familiarity_patterns", {})
                for category, pattern_data in brand_patterns.items():
                    if brand.lower() in [b.lower() for b in pattern_data.get('brands', [])]:
                        default_rating = pattern_data.get('default_familiarity', 3)
                        print(f"🎯 Using category default for {brand}: {default_rating}")
                        return {'familiarity': default_rating}
            
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving learned ratings: {e}")
            return None
    
    # ========================================
    # RATING GENERATION
    # ========================================
    
    def get_brand_familiarity_rating(self, brand: str) -> int:
        """
        Generate appropriate familiarity rating for a brand (1-5 scale)
        Uses patterns and randomization for human-like responses
        """
        try:
            # Check if we have profile preferences
            if self.brain:
                user_profile = self.brain.get("user_profile", {})
                preferred_brands = user_profile.get("preferred_brands", [])
                avoided_brands = user_profile.get("avoided_brands", [])
                
                # High familiarity for preferred brands
                if any(pref.lower() in brand.lower() for pref in preferred_brands):
                    return random.choice([4, 5])
                
                # Low familiarity for avoided brands
                if any(avoid.lower() in brand.lower() for avoid in avoided_brands):
                    return random.choice([1, 2])
            
            # Brand category patterns
            well_known_indicators = [
                'coca', 'pepsi', 'nike', 'adidas', 'apple', 'samsung', 
                'microsoft', 'google', 'amazon', 'walmart', 'mcdonalds'
            ]
            
            less_known_indicators = [
                'generic', 'store brand', 'private label', 'local'
            ]
            
            brand_lower = brand.lower()
            
            # Check for well-known brands
            if any(indicator in brand_lower for indicator in well_known_indicators):
                return random.choice([4, 5])  # High familiarity
            
            # Check for less-known brands
            if any(indicator in brand_lower for indicator in less_known_indicators):
                return random.choice([1, 2])  # Low familiarity
            
            # Default: moderate familiarity with some randomness
            return random.choice([2, 3, 3, 4])  # Bias toward middle
            
        except Exception as e:
            print(f"❌ Error generating familiarity rating: {e}")
            return 3  # Safe default
    
    def get_satisfaction_rating(self, brand: str, attribute: str) -> int:
        """
        Generate satisfaction rating for brand-attribute combination
        Uses realistic patterns based on attribute type
        """
        try:
            # Base rating with some randomness
            base_rating = random.choice([3, 3, 4, 4, 4, 5])  # Bias toward positive
            
            # Adjust based on attribute
            attribute_lower = attribute.lower()
            
            if 'quality' in attribute_lower:
                # Quality ratings tend to be more critical
                adjustment = random.choice([-1, 0, 0, 1])
            elif 'value' in attribute_lower or 'price' in attribute_lower:
                # Value ratings vary more
                adjustment = random.choice([-1, -1, 0, 1])
            elif 'service' in attribute_lower or 'support' in attribute_lower:
                # Service ratings tend to be extreme
                adjustment = random.choice([-2, 0, 0, 1, 2])
            elif 'innovation' in attribute_lower or 'design' in attribute_lower:
                # Innovation ratings depend on brand perception
                if any(tech in brand.lower() for tech in ['apple', 'google', 'tesla']):
                    adjustment = random.choice([0, 1, 1])
                else:
                    adjustment = random.choice([-1, 0, 0])
            else:
                adjustment = 0
            
            # Apply adjustment and clamp to valid range
            final_rating = base_rating + adjustment
            return max(1, min(5, final_rating))
            
        except Exception as e:
            print(f"❌ Error generating satisfaction rating: {e}")
            return 3  # Safe default
    
    # ========================================
    # RATING STORAGE
    # ========================================
    
    async def save_rating(self, brand: str, matrix_type: str, ratings: Dict[str, int]) -> bool:
        """
        Save successful rating to knowledge base for future use
        
        Args:
            brand: Brand name
            matrix_type: Type of matrix (brand_familiarity, satisfaction_matrix)
            ratings: Dict of attribute->rating mappings
        """
        try:
            if not self.brain:
                return False
            
            # Get existing learned ratings
            learned_ratings = self.brain.get("learned_ratings", {})
            
            # Create key for this brand-matrix combination
            brand_key = f"{matrix_type}_{brand.lower().replace(' ', '_')}"
            
            # Update or create rating entry
            if brand_key in learned_ratings:
                # Update existing ratings
                existing = learned_ratings[brand_key]
                existing['ratings'].update(ratings)
                existing['last_updated'] = time.time()
                existing['success_count'] = existing.get('success_count', 0) + 1
            else:
                # Create new entry
                learned_ratings[brand_key] = {
                    'brand': brand,
                    'matrix_type': matrix_type,
                    'ratings': ratings,
                    'first_rated': time.time(),
                    'last_updated': time.time(),
                    'success_count': 1
                }
            
            # Save back to knowledge base
            self.brain.set("learned_ratings", learned_ratings)
            if hasattr(self.brain, 'save_data'):
                self.brain.save_data()
            
            print(f"🧠 Saved ratings for {brand}: {ratings}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving rating: {e}")
            return False
    
    # ========================================
    # SUCCESS/FAILURE REPORTING
    # ========================================
    
    async def report_success(self, strategy_used: str, execution_time: float,
                           matrix_type: str, brands_processed: int,
                           success_rate: float, confidence_score: float = 0.0):
        """Report successful matrix automation to brain for learning"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"matrix_{int(time.time())}",
                "matrix_type": matrix_type,
                "strategy_used": strategy_used,
                "execution_time": execution_time,
                "brands_processed": brands_processed,
                "success_rate": success_rate,
                "confidence_score": confidence_score,
                "result": "SUCCESS",
                "automation_success": True
            }
            
            # Store for future reference
            self.last_strategy_used = strategy_used
            self.last_matrix_type = matrix_type
            
            # Report to brain
            if self.brain and hasattr(self.brain, 'learn_successful_automation'):
                success = await self.brain.learn_successful_automation(learning_data)
                if success:
                    print(f"🧠 SUCCESS LEARNED: {strategy_used} for {matrix_type}")
                    print(f"📊 Processed {brands_processed} brands with {success_rate:.1%} success")
                    
                    # Update matrix success rate
                    await self._update_matrix_patterns(matrix_type, success_rate)
                else:
                    print(f"⚠️ Failed to save learning data")
            else:
                print(f"⚠️ Brain connection not available for learning")
                
        except Exception as e:
            print(f"❌ Error reporting success to brain: {e}")
    
    async def report_failure(self, error_message: str, page_content: str,
                           matrix_type: str = None, confidence_score: float = 0.0):
        """Report automation failure to brain for learning"""
        try:
            learning_data = {
                "timestamp": time.time(),
                "session_id": f"matrix_{int(time.time())}",
                "matrix_type": matrix_type or self.last_matrix_type or "unknown",
                "error_message": error_message,
                "page_snippet": page_content[:200],
                "confidence_score": confidence_score,
                "result": "FAILURE",
                "automation_success": False
            }
            
            # Report failure for learning
            if self.brain and hasattr(self.brain, 'learn_from_failure'):
                await self.brain.learn_from_failure(learning_data)
                print(f"🧠 FAILURE LEARNED: {error_message}")
            else:
                print(f"⚠️ Brain connection not available for failure learning")
                
        except Exception as e:
            print(f"❌ Error reporting failure to brain: {e}")
    
    # ========================================
    # CONFIDENCE ADJUSTMENTS
    # ========================================
    
    def get_confidence_adjustment(self, matrix_type: str, base_confidence: float) -> float:
        """Get confidence adjustment based on learning history"""
        try:
            if self.brain and hasattr(self.brain, 'get_confidence_adjustment_suggestions'):
                adjustment = self.brain.get_confidence_adjustment_suggestions(
                    handler_name="rating_matrix_handler",
                    question_type=matrix_type
                )
                
                if adjustment:
                    # Apply adjustments based on success history
                    if matrix_type == 'brand_familiarity':
                        # Brand familiarity is critical - apply full adjustments
                        return adjustment
                    else:
                        # Other matrices - apply conservative adjustments
                        return adjustment * 0.7
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error getting confidence adjustment: {e}")
            return 0.0
    
    # ========================================
    # PATTERN LEARNING
    # ========================================
    
    async def _update_matrix_patterns(self, matrix_type: str, success_rate: float):
        """Update matrix patterns with success data"""
        try:
            if self.brain:
                rating_matrices = self.brain.get("rating_matrices", {})
                
                if matrix_type not in rating_matrices:
                    rating_matrices[matrix_type] = {
                        "patterns": [],
                        "success_rate": 0.0,
                        "total_attempts": 0,
                        "confidence_threshold": 0.7
                    }
                
                # Update success rate with rolling average
                matrix_data = rating_matrices[matrix_type]
                total_attempts = matrix_data.get("total_attempts", 0) + 1
                current_rate = matrix_data.get("success_rate", 0.0)
                
                # Calculate new rolling average
                new_rate = ((current_rate * (total_attempts - 1)) + success_rate) / total_attempts
                
                matrix_data["success_rate"] = round(new_rate, 3)
                matrix_data["total_attempts"] = total_attempts
                
                # Update in knowledge base
                self.brain.set("rating_matrices", rating_matrices)
                
                # Save to disk
                if hasattr(self.brain, 'save_data'):
                    self.brain.save_data()
                
                print(f"🧠 Updated {matrix_type} patterns - Success rate: {new_rate:.1%}")
                
        except Exception as e:
            print(f"❌ Error updating matrix patterns: {e}")
    
    # ========================================
    # STATE TRACKING
    # ========================================
    
    def set_detected_matrix_type(self, matrix_type: str):
        """Set the currently detected matrix type"""
        self.last_matrix_type = matrix_type
    
    def get_last_matrix_type(self) -> Optional[str]:
        """Get the last detected matrix type"""
        return self.last_matrix_type
    
    def get_last_strategy_used(self) -> Optional[str]:
        """Get the last strategy that was used"""
        return self.last_strategy_used
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def get_rating_statistics(self) -> Dict[str, Any]:
        """Get statistics about learned ratings"""
        try:
            if not self.brain:
                return {}
            
            learned_ratings = self.brain.get("learned_ratings", {})
            
            stats = {
                'total_brands_learned': len(learned_ratings),
                'brands_by_matrix_type': {},
                'average_ratings': {},
                'most_rated_brands': []
            }
            
            # Analyze by matrix type
            for brand_key, rating_data in learned_ratings.items():
                matrix_type = rating_data.get('matrix_type', 'unknown')
                
                if matrix_type not in stats['brands_by_matrix_type']:
                    stats['brands_by_matrix_type'][matrix_type] = 0
                stats['brands_by_matrix_type'][matrix_type] += 1
                
                # Track most frequently rated
                success_count = rating_data.get('success_count', 0)
                stats['most_rated_brands'].append({
                    'brand': rating_data.get('brand', 'Unknown'),
                    'count': success_count
                })
            
            # Sort most rated brands
            stats['most_rated_brands'].sort(key=lambda x: x['count'], reverse=True)
            stats['most_rated_brands'] = stats['most_rated_brands'][:10]  # Top 10
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting rating statistics: {e}")
            return {}
    
    def __str__(self) -> str:
        """String representation"""
        return f"RatingMatrixBrain(connected={self.brain is not None})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        stats = self.get_rating_statistics()
        return f"RatingMatrixBrain(brands_learned={stats.get('total_brands_learned', 0)})"