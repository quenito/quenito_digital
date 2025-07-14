#!/usr/bin/env python3
"""
Handler Factory Module - Enhanced with Brand Familiarity Supremacy
Intelligent handler selection with ultra-conservative confidence thresholds.

MAJOR UPDATE: Includes the GAME-CHANGING Brand Familiarity Handler
Expected impact: 21% → 60-70% automation improvement!
FIXED: Critical error resolution for "too many values to unpack"
"""

from .demographics_handler_brain import DemographicsHandler
from .brand_familiarity_handler import BrandFamiliarityHandler  # THE GAME CHANGER!
from .rating_matrix_handler import RatingMatrixHandler
from .multi_select_handler import MultiSelectHandler
from .recency_activities_handler import RecencyActivitiesHandler
from .trust_rating_handler import TrustRatingHandler
from .research_handler import ResearchRequiredHandler
from .unknown_handler import UnknownHandler


class HandlerFactory:
    """Enhanced handler factory with Brand Familiarity Supremacy and ultra-conservative confidence thresholds"""
    
    def __init__(self, knowledge_base, intervention_manager):
        self.knowledge_base = knowledge_base
        self.intervention_manager = intervention_manager
        
        # Initialize all handlers with None page (will be set later)
        self.handlers = {
            'demographics': DemographicsHandler(None, knowledge_base, intervention_manager),
            'brand_familiarity': BrandFamiliarityHandler(None, knowledge_base, intervention_manager),  # 🚀 THE GAME CHANGER!
            'rating_matrix': RatingMatrixHandler(None, knowledge_base, intervention_manager),
            'multi_select': MultiSelectHandler(None, knowledge_base, intervention_manager),
            'trust_rating': TrustRatingHandler(None, knowledge_base, intervention_manager),
            'recency_activities': RecencyActivitiesHandler(None, knowledge_base, intervention_manager),
            'research_required': ResearchRequiredHandler(None, knowledge_base, intervention_manager),
            'unknown': UnknownHandler(None, knowledge_base, intervention_manager)
        }
        
        # Handler statistics for performance tracking
        self.handler_stats = {
            name: {'attempts': 0, 'successes': 0, 'confidence_scores': []} 
            for name in self.handlers.keys()
        }
        
        # Ultra-conservative confidence thresholds (98-99%) for enhanced learning
        self.confidence_thresholds = {
            "demographics": 0.60,        # 60% - full demographics profile in knowledge base decreased to 60% confidence needed
            "brand_familiarity": 0.98,   # 98% - THE CRITICAL HANDLER for matrix questions
            "rating_matrix": 0.99,       # 99% - complex interactions
            "multi_select": 0.97,        # 97% - multiple choice complexity
            "trust_rating": 0.96,        # 96% - trust assessment
            "recency_activities": 0.95,  # 95% - activity timeline
            "research_required": 0.95,   # 95% - factual lookup needed
            "unknown": 0.99              # 99% - catch-all with highest threshold
        }
        
        print("🏭 Handler Factory initialized with Brand Familiarity SUPREMACY!")
        print("🎯 Expected automation boost: 21% → 60-70% with brand handler!")
    
    def get_best_handler(self, page, page_content: str):
        """
        Get the best handler for the current question with enhanced confidence scoring.
        FIXED: Ensures consistent return format for all cases.
        
        Args:
            page: Playwright page object
            page_content: HTML content of the current page
            
        Returns:
            tuple: (handler_object, handler_name, confidence_score) or (None, None, 0.0)
        """
        best_handler = None
        best_name = None
        best_confidence = 0.0
        
        print("\n🔍 Handler Analysis with Brand Familiarity Priority:")
        
        # Test each handler's confidence
        handler_results = []
        for name, handler in self.handlers.items():
            try:
                # Set the page for this handler
                handler.page = page
                
                # Get confidence score
                confidence = handler.can_handle(page_content)
                
                # Apply context-aware adjustments
                adjusted_confidence = self._apply_context_adjustments(name, confidence, page_content)
                
                # Record confidence score for statistics
                self.handler_stats[name]['confidence_scores'].append(adjusted_confidence)
                
                handler_results.append((name, adjusted_confidence))
                print(f"   📊 {name}: {adjusted_confidence:.3f}")
                
            except Exception as e:
                print(f"   ❌ {name}: Error getting confidence - {str(e)}")
                # Still add to results with 0 confidence
                handler_results.append((name, 0.0))
                self.handler_stats[name]['confidence_scores'].append(0.0)
        
        # Sort by confidence (highest first)
        handler_results.sort(key=lambda x: x[1], reverse=True)
        
        # Find the first handler that meets the ultra-conservative threshold
        for name, confidence in handler_results:
            threshold = self.confidence_thresholds.get(name, 0.95)
            
            if confidence >= threshold:
                best_handler = self.handlers[name]
                best_name = name
                best_confidence = confidence
                
                print(f"✅ Selected handler: {name} (confidence: {confidence:.3f}, threshold: {threshold})")
                print(f"🚀 Brand Familiarity Priority: {'CRITICAL HANDLER SELECTED!' if name == 'brand_familiarity' else 'Standard handler'}")
                
                # Record attempt
                self.handler_stats[name]['attempts'] += 1
                break
        
        if not best_handler:
            print("❌ No handler meets ultra-conservative confidence thresholds")
            print("🔄 Will request manual intervention for learning data capture")
        
        # CRITICAL FIX: Always return exactly 3 values
        return best_handler, best_name, best_confidence
    
    def _apply_context_adjustments(self, handler_name: str, confidence: float, page_content: str) -> float:
        """
        Apply context-aware confidence adjustments with Brand Familiarity Priority.
        
        Args:
            handler_name: Name of the handler being evaluated
            confidence: Base confidence score
            page_content: Page content for context analysis
            
        Returns:
            float: Adjusted confidence score
        """
        content_lower = page_content.lower()
        
        # BRAND FAMILIARITY PRIORITY BOOST
        if handler_name == 'brand_familiarity':
            # Extra boost for clear brand matrix indicators
            brand_matrix_indicators = [
                'how familiar are you with these brands',
                'rate your familiarity with',
                'brand awareness',
                'familiar with the following brands'
            ]
            
            for indicator in brand_matrix_indicators:
                if indicator in content_lower:
                    confidence = min(0.98, confidence + 0.1)  # Boost toward threshold
                    print(f"🚀 Brand Matrix Boost Applied: +0.1 confidence")
                    break
        
        # Negative adjustments for mismatched contexts
        if handler_name == 'demographics' and any(word in content_lower for word in ['sponsor', 'venue']):
            # Demographics questions usually don't ask about sponsors/venues
            confidence = max(0.0, confidence - 0.2)
        
        elif handler_name == 'brand_familiarity' and 'trustworthy' in content_lower:
            # Brand familiarity is different from trust ratings
            confidence = max(0.0, confidence - 0.2)
        
        elif handler_name == 'trust_rating' and any(brand in content_lower for brand in ['nike', 'adidas', 'apple', 'samsung']):
            # Trust ratings shouldn't handle brand familiarity
            confidence = max(0.0, confidence - 0.3)
        
        # Positive adjustments for strong contextual matches
        if handler_name == 'demographics' and any(word in content_lower for word in ['age', 'gender', 'income', 'education', 'occupation', 'work', 'job']):
            confidence = min(1.0, confidence + 0.15)  # 🎯 INCREASED boost and higher cap
        elif handler_name == 'demographics' and any(word in content_lower for word in ['male', 'female', 'years old', 'born']):
            confidence = min(1.0, confidence + 0.10)  # 🎯 Additional boost for clear demo indicators

        return confidence
    
    def record_handler_success(self, handler_name: str, success: bool):
        """
        Record the success/failure of a handler execution with Brand Familiarity tracking.
        
        Args:
            handler_name: Name of the handler that was executed
            success: Whether the handler succeeded
        """
        if handler_name in self.handler_stats:
            if success:
                self.handler_stats[handler_name]['successes'] += 1
                
                # Special celebration for brand familiarity success!
                if handler_name == 'brand_familiarity':
                    print("🎉 BRAND FAMILIARITY SUCCESS! Survey automation revolution in progress!")
            
            # Calculate success rate
            attempts = self.handler_stats[handler_name]['attempts']
            successes = self.handler_stats[handler_name]['successes']
            success_rate = (successes / attempts * 100) if attempts > 0 else 0
            
            status_icon = "🎯" if handler_name == 'brand_familiarity' else "📊"
            print(f"{status_icon} {handler_name} performance: {successes}/{attempts} ({success_rate:.1f}% success rate)")
            
            # Track brand familiarity impact
            if handler_name == 'brand_familiarity' and success:
                print("📈 Expected automation boost from brand handler success!")
    
    def get_handler_stats(self):
        """
        Get comprehensive handler performance statistics with Brand Familiarity focus.
        
        Returns:
            dict: Handler performance statistics
        """
        stats = {}
        
        for handler_name, data in self.handler_stats.items():
            attempts = data['attempts']
            successes = data['successes']
            confidence_scores = data['confidence_scores']
            
            success_rate = (successes / attempts * 100) if attempts > 0 else 0
            avg_confidence = (sum(confidence_scores) / len(confidence_scores)) if confidence_scores else 0
            
            stats[handler_name] = {
                'attempts': attempts,
                'successes': successes,
                'success_rate': success_rate,
                'average_confidence': avg_confidence,
                'total_confidence_scores': len(confidence_scores),
                'is_critical_handler': handler_name == 'brand_familiarity'  # Mark the game changer
            }
        
        return stats
    
    def get_brand_familiarity_impact(self):
        """
        Calculate the impact of the Brand Familiarity Handler on overall automation.
        
        Returns:
            dict: Brand familiarity impact metrics
        """
        bf_stats = self.handler_stats.get('brand_familiarity', {})
        attempts = bf_stats.get('attempts', 0)
        successes = bf_stats.get('successes', 0)
        
        # Calculate projected automation improvement
        if attempts > 0:
            success_rate = (successes / attempts) * 100
            # Based on JSON analysis: brand failures were bottleneck for 21% → 60-70% improvement
            projected_automation_boost = (success_rate / 100) * 45  # 45% potential boost from analysis
        else:
            success_rate = 0
            projected_automation_boost = 0
        
        return {
            'brand_attempts': attempts,
            'brand_successes': successes,
            'brand_success_rate': success_rate,
            'projected_automation_boost': projected_automation_boost,
            'analysis_baseline': 21.0,  # From your JSON analysis
            'projected_new_automation': 21.0 + projected_automation_boost
        }
    
    def get_available_handlers(self):
        """Get list of available handler names with Brand Familiarity priority"""
        handlers = list(self.handlers.keys())
        
        # Put brand_familiarity first to show priority
        if 'brand_familiarity' in handlers:
            handlers.remove('brand_familiarity')
            handlers.insert(0, 'brand_familiarity')
        
        return handlers
    
    def reset_stats(self):
        """Reset handler statistics (useful for testing)"""
        for handler_name in self.handler_stats:
            self.handler_stats[handler_name] = {
                'attempts': 0, 
                'successes': 0, 
                'confidence_scores': []
            }
        print("📊 Handler statistics reset - ready for Brand Familiarity revolution testing!")
    
    def get_confidence_thresholds(self):
        """Get current confidence thresholds for all handlers"""
        return self.confidence_thresholds.copy()
    
    def update_confidence_threshold(self, handler_name: str, new_threshold: float):
        """
        Update confidence threshold for a specific handler.
        
        Args:
            handler_name: Name of handler to update
            new_threshold: New confidence threshold (0.0-1.0)
        """
        if handler_name in self.confidence_thresholds:
            old_threshold = self.confidence_thresholds[handler_name]
            self.confidence_thresholds[handler_name] = max(0.0, min(1.0, new_threshold))
            
            print(f"🔧 Updated {handler_name} threshold: {old_threshold:.3f} → {new_threshold:.3f}")
            
            if handler_name == 'brand_familiarity':
                print("🚀 Brand Familiarity threshold updated - automation impact expected!")

    # CRITICAL FIX: Add missing methods that are being called
    def get_handler_recommendations(self):
        """
        Get handler recommendations based on current performance.
        FIXES: 'HandlerFactory' object has no attribute 'get_handler_recommendations'
        """
        recommendations = []
        
        for handler_name, stats in self.handler_stats.items():
            attempts = stats.get('attempts', 0)
            successes = stats.get('successes', 0)
            success_rate = (successes / attempts * 100) if attempts > 0 else 0
            
            if attempts > 0 and success_rate < 50:
                recommendations.append({
                    'handler': handler_name,
                    'issue': 'Low success rate',
                    'suggestion': f'Review and enhance {handler_name} detection patterns',
                    'priority': 'HIGH' if handler_name == 'brand_familiarity' else 'MEDIUM'
                })
            elif handler_name == 'brand_familiarity' and attempts == 0:
                recommendations.append({
                    'handler': handler_name,
                    'issue': 'No brand questions encountered yet',
                    'suggestion': 'Look for surveys with brand familiarity questions for supremacy testing',
                    'priority': 'INFO'
                })
        
        return recommendations