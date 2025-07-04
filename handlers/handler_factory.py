"""
Handler Factory Module
Intelligent handler selection based on confidence scoring.
"""

from .demographics_handler import DemographicsHandler
from .brand_familiarity_handler import BrandFamiliarityHandler
from .rating_matrix_handler import RatingMatrixHandler
from .multi_select_handler import MultiSelectHandler
from .trust_rating_handler import TrustRatingHandler  # NEW
from .recency_activities_handler import RecencyActivitiesHandler
from .research_handler import ResearchHandler  # NEW
from .unknown_handler import UnknownHandler

class HandlerFactory:
    """Enhanced handler factory with new handlers and improved selection logic"""
    
    def __init__(self, knowledge_base, intervention_manager):
        self.knowledge_base = knowledge_base
        self.intervention_manager = intervention_manager
        
        # Initialize all handlers
        self.handlers = {
            'demographics': DemographicsHandler(None, knowledge_base, intervention_manager),
            'brand_familiarity': BrandFamiliarityHandler(None, knowledge_base, intervention_manager),
            'rating_matrix': RatingMatrixHandler(None, knowledge_base, intervention_manager),
            'multi_select': MultiSelectHandler(None, knowledge_base, intervention_manager),
            'trust_rating': TrustRatingHandler(None, knowledge_base, intervention_manager),  # NEW
            'recency_activities': RecencyActivitiesHandler(None, knowledge_base, intervention_manager),
            'research_required': ResearchHandler(None, knowledge_base, intervention_manager),  # NEW
            'unknown': UnknownHandler(None, knowledge_base, intervention_manager)
        }
        
        # Handler statistics for performance tracking
        self.handler_stats = {
            name: {'attempts': 0, 'successes': 0, 'confidence_scores': []} 
            for name in self.handlers.keys()
        }
    
    def get_best_handler(self, page, page_content):
        """Get the best handler for the current question with enhanced confidence scoring"""
        
        # Update page reference for all handlers
        for handler in self.handlers.values():
            handler.page = page
        
        # Test each handler's confidence (excluding 'unknown' for initial testing)
        handler_confidences = []
        
        for name, handler in self.handlers.items():
            if name == 'unknown':  # Skip unknown for confidence testing
                continue
                
            try:
                can_handle = handler.can_handle(page_content)
                base_confidence = 1.0 if can_handle else 0.0
                
                # Apply confidence adjustments based on content analysis
                adjusted_confidence = self.apply_confidence_adjustments(
                    name, base_confidence, page_content
                )
                
                handler_confidences.append((name, handler, adjusted_confidence))
                
                # Log confidence for debugging
                if adjusted_confidence > 0.0:
                    print(f"   📊 {name}: {adjusted_confidence:.2f} confidence")
                
            except Exception as e:
                print(f"   ❌ Error testing handler {name}: {e}")
                handler_confidences.append((name, handler, 0.0))
        
        # Sort by confidence (highest first)
        handler_confidences.sort(key=lambda x: x[2], reverse=True)
        
        # Select best handler based on confidence threshold
        if handler_confidences and handler_confidences[0][2] > 0.5:
            best_name, best_handler, best_confidence = handler_confidences[0]
            
            # Update statistics
            self.handler_stats[best_name]['attempts'] += 1
            self.handler_stats[best_name]['confidence_scores'].append(best_confidence)
            
            print(f"🎯 Selected handler: {best_name} (confidence: {best_confidence:.2f})")
            return best_handler, best_confidence
        else:
            # Fall back to unknown handler
            print("🔄 No confident handler found, using unknown handler")
            self.handler_stats['unknown']['attempts'] += 1
            return self.handlers['unknown'], 0.0
    
    def apply_confidence_adjustments(self, handler_name, base_confidence, page_content):
        """Apply handler-specific confidence adjustments"""
        
        if base_confidence == 0.0:
            return 0.0
        
        content_lower = page_content.lower()
        adjusted_confidence = base_confidence
        
        # Handler-specific confidence boosts
        if handler_name == 'trust_rating':
            # Boost confidence for clear trust rating indicators
            trust_indicators = ['trustworthy', 'how much do you trust', 'rate the trust']
            if any(indicator in content_lower for indicator in trust_indicators):
                adjusted_confidence = min(1.0, adjusted_confidence + 0.2)
            
            # Check for rating scale elements
            if any(num in content_lower for num in ['1', '2', '3', '4', '5', '6', '7']):
                adjusted_confidence = min(1.0, adjusted_confidence + 0.1)
        
        elif handler_name == 'research_required':
            # Boost confidence for clear research indicators
            research_indicators = ['sponsor', 'venue', 'stadium', 'which company', 'where is']
            matching_indicators = sum(1 for indicator in research_indicators if indicator in content_lower)
            if matching_indicators >= 2:
                adjusted_confidence = min(1.0, adjusted_confidence + 0.3)
            elif matching_indicators == 1:
                adjusted_confidence = min(1.0, adjusted_confidence + 0.1)
        
        elif handler_name == 'demographics':
            # Boost for multiple demographic indicators
            demo_indicators = ['age', 'gender', 'employment', 'income', 'education', 'location']
            matching_demos = sum(1 for indicator in demo_indicators if indicator in content_lower)
            if matching_demos >= 2:
                adjusted_confidence = min(1.0, adjusted_confidence + 0.2)
        
        elif handler_name == 'brand_familiarity':
            # Boost for brand familiarity matrix patterns
            if 'familiar' in content_lower and 'brand' in content_lower:
                adjusted_confidence = min(1.0, adjusted_confidence + 0.2)
        
        elif handler_name == 'multi_select':
            # Boost for clear multi-select indicators
            multi_indicators = ['select all', 'check all', 'multiple', 'more than one']
            if any(indicator in content_lower for indicator in multi_indicators):
                adjusted_confidence = min(1.0, adjusted_confidence + 0.2)
        
        # Apply penalties for conflicting patterns
        adjusted_confidence = self.apply_confidence_penalties(
            handler_name, adjusted_confidence, content_lower
        )
        
        return max(0.0, adjusted_confidence)
    
    def apply_confidence_penalties(self, handler_name, confidence, content_lower):
        """Apply penalties for conflicting patterns"""
        
        # Penalty if multiple handlers might match strongly
        if handler_name == 'trust_rating' and 'familiar' in content_lower:
            # Trust questions usually don't ask about familiarity
            confidence = max(0.0, confidence - 0.3)
        
        elif handler_name == 'demographics' and any(word in content_lower for word in ['sponsor', 'venue']):
            # Demographics questions usually don't ask about sponsors/venues
            confidence = max(0.0, confidence - 0.2)
        
        elif handler_name == 'brand_familiarity' and 'trustworthy' in content_lower:
            # Brand familiarity is different from trust ratings
            confidence = max(0.0, confidence - 0.2)
        
        return confidence
    
    def record_handler_success(self, handler_name, success):
        """Record the success/failure of a handler execution"""
        if handler_name in self.handler_stats:
            if success:
                self.handler_stats[handler_name]['successes'] += 1
            
            # Calculate success rate
            attempts = self.handler_stats[handler_name]['attempts']
            successes = self.handler_stats[handler_name]['successes']
            success_rate = (successes / attempts * 100) if attempts > 0 else 0
            
            print(f"📊 {handler_name} performance: {successes}/{attempts} ({success_rate:.1f}% success rate)")
    
    def get_handler_stats(self):
        """Get comprehensive handler performance statistics"""
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
                'total_confidence_scores': len(confidence_scores)
            }
        
        return stats
    
    def get_available_handlers(self):
        """Get list of available handler names"""
        return list(self.handlers.keys())
    
    def reset_stats(self):
        """Reset handler statistics (useful for testing)"""
        for handler_name in self.handler_stats:
            self.handler_stats[handler_name] = {
                'attempts': 0, 
                'successes': 0, 
                'confidence_scores': []
            }
        print("📊 Handler statistics reset")
    
    def get_handler_recommendations(self):
        """Get recommendations for handler improvements"""
        recommendations = []
        
        for handler_name, data in self.handler_stats.items():
            attempts = data['attempts']
            successes = data['successes']
            
            if attempts > 0:
                success_rate = (successes / attempts) * 100
                
                if success_rate < 50 and attempts >= 3:
                    recommendations.append(f"❌ {handler_name}: Low success rate ({success_rate:.1f}%) - needs improvement")
                elif success_rate < 75 and attempts >= 5:
                    recommendations.append(f"⚠️ {handler_name}: Moderate success rate ({success_rate:.1f}%) - consider enhancement")
                elif success_rate >= 90 and attempts >= 3:
                    recommendations.append(f"✅ {handler_name}: Excellent performance ({success_rate:.1f}%)")
        
        if not recommendations:
            recommendations.append("📊 Insufficient data for handler recommendations - run more surveys")
        
        return recommendations