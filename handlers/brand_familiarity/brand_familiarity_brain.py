#!/usr/bin/env python3
"""
🧠 Brand Familiarity Brain Module
Integrates with knowledge base for learning and intelligence

This module:
- Retrieves learned brand preferences
- Applies confidence adjustments
- Stores successful automations
- Analyzes brand patterns
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class BrandFamiliarityBrain:
    """Brain integration for brand familiarity learning"""
    
    def __init__(self, knowledge_base):
        """Initialize with knowledge base connection"""
        self.brain = knowledge_base
        self.learned_brands = {}
        self.success_patterns = {}
        self.session_responses = {}  # Track responses within session
        
        # Load user's brand preferences from brain
        self._load_user_brands()
        
        print("🧠 Brand Familiarity Brain module initialized")
        print(f"   - User brands loaded: {len(self.learned_brands)} known brands")
    
    def _load_user_brands(self):
        """Load user's brand preferences from knowledge base"""
        if not self.brain:
            return
        
        # Get user profile brand data
        user_profile = self.brain.get('user_profile', {})
        existing_brands = user_profile.get('existing_brands', {})
        
        # Map currently used brands
        for brand in existing_brands.get('currently_use', []):
            self.learned_brands[brand.lower()] = 'very_familiar'
        
        # Map familiar brands
        for brand in existing_brands.get('familiar_with', []):
            if brand.lower() not in self.learned_brands:
                self.learned_brands[brand.lower()] = 'somewhat_familiar'
        
        # Load learned automations
        learned = self.brain.get('learned_automations', {})
        for key, data in learned.items():
            if key.startswith('brand_'):
                brand_name = key.replace('brand_', '')
                if data.get('result') == 'SUCCESS':
                    self.learned_brands[brand_name] = data.get('response_value', 'somewhat_familiar')
    
    def get_learned_response(self, brand: str) -> Optional[str]:
        """
        Get learned familiarity level for a brand
        
        Priority order:
        1. Session response (consistency within survey)
        2. User profile (currently use > familiar with)
        3. Learned automations
        4. None (will use default)
        """
        brand_lower = brand.lower()
        
        # Check session responses first (consistency)
        if brand_lower in self.session_responses:
            return self.session_responses[brand_lower]
        
        # Check learned brands
        if brand_lower in self.learned_brands:
            return self.learned_brands[brand_lower]
        
        # Check for similar brands (partial match)
        for known_brand, response in self.learned_brands.items():
            if known_brand in brand_lower or brand_lower in known_brand:
                print(f"🧠 Found similar brand: {known_brand} → {response}")
                return response
        
        return None
    
    def calculate_brand_confidence(self, brand: str, base_confidence: float) -> float:
        """
        Apply learning-based confidence adjustments
        
        Boosts confidence if:
        - We've seen this brand before
        - Handler has high success rate
        - Similar brands were successful
        """
        confidence = base_confidence
        
        # Boost if we know this brand
        if self.get_learned_response(brand):
            confidence += 0.2
            print(f"🧠 Confidence boost: Known brand (+0.2)")
        
        # Check handler success rate
        handler_stats = self.brain.get('handler_performance', {}).get('brand_familiarity', {})
        success_rate = handler_stats.get('success_rate', 0)
        
        if success_rate > 0.8:
            confidence += 0.1
            print(f"🧠 Confidence boost: High success rate ({success_rate:.0%}) (+0.1)")
        
        # Check recent successes
        recent_successes = handler_stats.get('recent_successes', 0)
        if recent_successes >= 3:
            confidence += 0.05
            print(f"🧠 Confidence boost: Recent success streak (+0.05)")
        
        return min(confidence, 0.98)
    
    def store_brand_response(self, brand: str, response_level: str, success: bool):
        """
        Store successful brand response for learning
        
        Updates:
        - Learned automations
        - Session responses
        - Handler statistics
        """
        if not self.brain:
            return
        
        brand_lower = brand.lower()
        
        # Store in session for consistency
        self.session_responses[brand_lower] = response_level
        
        if success:
            # Update learned brands
            self.learned_brands[brand_lower] = response_level
            
            # Store in learned automations
            learning_data = {
                'question_type': f'brand_{brand_lower}',
                'strategy_used': 'matrix_selection',
                'response_value': response_level,
                'execution_time': 1.0,
                'confidence_score': 0.9,
                'result': 'SUCCESS',
                'element_type': 'radio_matrix',
                'automation_success': True,
                'learned_at': datetime.now().timestamp()
            }
            
            self.brain.learn_successful_automation(learning_data)
            print(f"🧠 Learned: {brand} → {response_level} ✓")
            
            # Update handler statistics
            self._update_handler_stats(success=True)
        else:
            # Record failure for learning
            self._update_handler_stats(success=False)
    
    def get_brand_strategy(self, brands: List[str]) -> Dict[str, str]:
        """
        Get response strategy for multiple brands
        
        Returns optimal response for each brand based on:
        - Learned preferences
        - Default strategies
        - Variety (avoid all same response)
        """
        strategy = {}
        response_counts = {'very_familiar': 0, 'somewhat_familiar': 0, 'not_familiar': 0}
        
        # First pass: Apply learned responses
        for brand in brands:
            learned = self.get_learned_response(brand)
            if learned:
                strategy[brand] = learned
                response_counts[learned] = response_counts.get(learned, 0) + 1
        
        # Second pass: Fill in missing with variety
        for brand in brands:
            if brand not in strategy:
                # Choose response to create realistic variety
                if response_counts['somewhat_familiar'] < len(brands) * 0.5:
                    response = 'somewhat_familiar'
                elif response_counts['not_familiar'] < len(brands) * 0.3:
                    response = 'not_familiar'
                else:
                    response = 'very_familiar'
                
                strategy[brand] = response
                response_counts[response] += 1
        
        # Log strategy
        print(f"🧠 Brand strategy for {len(brands)} brands:")
        for level, count in response_counts.items():
            if count > 0:
                print(f"   - {level}: {count} brands")
        
        return strategy
    
    def analyze_brand_category(self, category: str) -> Dict[str, Any]:
        """
        Analyze patterns for a brand category
        
        Returns insights about user's relationship with category
        """
        analysis = {
            'category': category,
            'default_response': 'somewhat_familiar',
            'confidence_boost': 0.0,
            'known_brands': [],
            'success_rate': 0.0
        }
        
        # Check if user has preferences in this category
        user_interests = self.brain.get('user_profile', {}).get('interests_and_preferences', {})
        
        if category in user_interests.get('high_interest', []):
            analysis['default_response'] = 'very_familiar'
            analysis['confidence_boost'] = 0.15
        elif category in user_interests.get('low_interest', []):
            analysis['default_response'] = 'not_familiar'
            analysis['confidence_boost'] = 0.1
        
        # Find known brands in category
        brand_patterns = self.brain.get('question_patterns', {}).get('brand_familiarity_questions', {})
        category_brands = brand_patterns.get('common_brands', {}).get(category, [])
        
        for brand in category_brands:
            if brand.lower() in self.learned_brands:
                analysis['known_brands'].append(brand)
        
        # Calculate category success rate
        category_key = f'brand_category_{category}'
        category_stats = self.brain.get('detailed_intervention_learning', {}).get(category_key, {})
        
        if category_stats:
            successes = category_stats.get('successes', 0)
            attempts = category_stats.get('attempts', 1)
            analysis['success_rate'] = successes / attempts
        
        return analysis
    
    def get_confidence_adjustment(self, question_type: str, base_confidence: float) -> float:
        """
        Get confidence adjustment based on learning data
        
        This method integrates with the broader confidence system
        """
        adjustment = 0.0
        
        # Check if we have successful patterns for this question type
        patterns = self.brain.get('detailed_intervention_learning', {})
        
        for pattern_key, pattern_data in patterns.items():
            if 'brand' in pattern_key and pattern_data.get('result') == 'SUCCESS':
                # Successful brand automation in history
                adjustment += 0.05
                break
        
        # Check handler-specific learning
        handler_learning = self.brain.get('handler_improvement_patterns', {}).get('brand_familiarity', {})
        
        if handler_learning:
            # Apply learned confidence adjustments
            if handler_learning.get('average_success_rate', 0) > 0.8:
                adjustment += 0.1
            
            # Check for specific pattern matches
            if handler_learning.get('matrix_detection_improved', False):
                adjustment += 0.05
        
        return adjustment
    
    def suggest_handler_improvements(self) -> List[str]:
        """
        Suggest improvements based on learning data
        
        Returns list of actionable improvements
        """
        suggestions = []
        
        # Analyze failure patterns
        failures = self._analyze_failure_patterns()
        
        if failures.get('unknown_brands', 0) > 5:
            suggestions.append("Add more brand mappings to knowledge base")
        
        if failures.get('detection_failures', 0) > 3:
            suggestions.append("Improve matrix layout detection patterns")
        
        if failures.get('selection_failures', 0) > 3:
            suggestions.append("Enhance radio button selection strategies")
        
        # Analyze success patterns
        successes = self._analyze_success_patterns()
        
        if successes.get('category_bias'):
            suggestions.append(f"Strong performance in {successes['category_bias']} category")
        
        return suggestions
    
    def _update_handler_stats(self, success: bool):
        """Update handler performance statistics"""
        if not self.brain:
            return
        
        stats_key = 'handler_performance'
        stats = self.brain.get(stats_key, {})
        
        if 'brand_familiarity' not in stats:
            stats['brand_familiarity'] = {
                'total_attempts': 0,
                'successful_attempts': 0,
                'recent_successes': 0,
                'success_rate': 0.0
            }
        
        handler_stats = stats['brand_familiarity']
        handler_stats['total_attempts'] += 1
        
        if success:
            handler_stats['successful_attempts'] += 1
            handler_stats['recent_successes'] = min(handler_stats['recent_successes'] + 1, 10)
        else:
            handler_stats['recent_successes'] = max(handler_stats['recent_successes'] - 1, 0)
        
        # Update success rate
        if handler_stats['total_attempts'] > 0:
            handler_stats['success_rate'] = (
                handler_stats['successful_attempts'] / handler_stats['total_attempts']
            )
        
        # Store back to brain
        self.brain.data[stats_key] = stats
    
    def _analyze_failure_patterns(self) -> Dict[str, int]:
        """Analyze patterns in failures"""
        failures = {
            'unknown_brands': 0,
            'detection_failures': 0,
            'selection_failures': 0
        }
        
        # Analyze intervention data
        interventions = self.brain.get('detailed_intervention_learning', {})
        
        for key, data in interventions.items():
            if 'brand' in key and data.get('result') != 'SUCCESS':
                reason = data.get('reason', '').lower()
                
                if 'unknown' in reason or 'not found' in reason:
                    failures['unknown_brands'] += 1
                elif 'detect' in reason:
                    failures['detection_failures'] += 1
                elif 'select' in reason or 'click' in reason:
                    failures['selection_failures'] += 1
        
        return failures
    
    def _analyze_success_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in successes"""
        patterns = {
            'total_successes': len(self.learned_brands),
            'category_bias': None,
            'common_response': None
        }
        
        # Find most common response level
        response_counts = {}
        for response in self.learned_brands.values():
            response_counts[response] = response_counts.get(response, 0) + 1
        
        if response_counts:
            patterns['common_response'] = max(response_counts, key=response_counts.get)
        
        # Find category bias
        category_counts = {}
        brand_patterns = self.brain.get('question_patterns', {}).get('brand_familiarity_questions', {})
        common_brands = brand_patterns.get('common_brands', {})
        
        for category, brands in common_brands.items():
            for brand in brands:
                if brand.lower() in self.learned_brands:
                    category_counts[category] = category_counts.get(category, 0) + 1
        
        if category_counts:
            patterns['category_bias'] = max(category_counts, key=category_counts.get)
        
        return patterns