#!/usr/bin/env python3
"""
🧠 Trust Rating Brain Module
Integrates with knowledge base for learning and intelligence
"""

from typing import Dict, List, Any, Optional

class TrustRatingBrain:
    """Brain integration for trust rating learning"""
    
    def __init__(self, knowledge_base):
        """Initialize with knowledge base connection"""
        self.brain = knowledge_base
        self.learned_trust_levels = {}
        self.entity_trust_history = {}
        print("🧠 Trust Rating Brain module initialized")
    
    def get_learned_trust_level(self, entity: str, scale_type: str) -> Optional[int]:
        """
        Get previously learned trust level for an entity
        
        Args:
            entity: The entity being rated (company, brand, website, etc.)
            scale_type: Type of scale (trust_5, trust_7, trust_10, etc.)
            
        Returns:
            Preferred trust rating or None if no learning available
        """
        if not self.brain:
            return None
        
        # Check if we have learned trust for this entity
        learned_key = f'trust_{entity.lower().replace(" ", "_")}'
        learned = self.brain.get('learned_automations', {}).get(learned_key, {})
        
        if learned and 'trust_level' in learned:
            # Get the appropriate value for this scale type
            scale_data = self.brain.get('question_patterns', {}).get(
                'trust_rating_questions', {}
            ).get('scale_types', {}).get(scale_type, {})
            
            if scale_data:
                # Map learned trust percentage to scale
                trust_percent = learned['trust_level']
                scale_range = scale_data.get('range', [])
                if scale_range:
                    # Convert percentage to scale value
                    scale_min = min(scale_range)
                    scale_max = max(scale_range)
                    scale_value = scale_min + (trust_percent / 100) * (scale_max - scale_min)
                    return round(scale_value)
        
        return None
    
    def get_trust_strategy(self, entity: str, context: str) -> str:
        """
        Determine trust rating strategy based on entity and context
        
        Returns:
            Strategy name: 'conservative_positive', 'neutral_safe', or 'moderate_positive'
        """
        # Check if entity is known
        if self.get_learned_trust_level(entity, 'trust_10'):
            return 'moderate_positive'  # We know this entity
        
        # Check context clues
        context_lower = context.lower()
        
        # Government or official sources - higher trust
        if any(word in context_lower for word in ['government', 'official', 'certified']):
            return 'moderate_positive'
        
        # Unknown or questionable - stay conservative
        if any(word in context_lower for word in ['unknown', 'new', 'unfamiliar']):
            return 'neutral_safe'
        
        # Default to conservative positive
        return 'conservative_positive'
    
    def calculate_trust_confidence(self, entity: str, base_confidence: float) -> float:
        """Apply learning-based confidence adjustments"""
        confidence = base_confidence
        
        # Boost if we've rated this entity before
        if self.get_learned_trust_level(entity, 'trust_10'):
            confidence += 0.2
        
        # Check handler success rate
        handler_stats = self.brain.get('handler_performance', {}).get('trust_rating', {})
        if handler_stats.get('success_rate', 0) > 0.8:
            confidence += 0.1
        
        return min(confidence, 0.98)
    
    def store_trust_rating(self, entity: str, trust_level: int, scale_type: str, success: bool):
        """
        Store successful trust rating for learning
        
        Args:
            entity: The entity that was rated
            trust_level: The trust level selected
            scale_type: The type of scale used
            success: Whether the rating was successful
        """
        if not self.brain:
            return
        
        # Get scale info to normalize trust level
        scale_data = self.brain.get('question_patterns', {}).get(
            'trust_rating_questions', {}
        ).get('scale_types', {}).get(scale_type, {})
        
        if scale_data:
            scale_range = scale_data.get('range', [])
            if scale_range:
                # Convert to percentage
                scale_min = min(scale_range)
                scale_max = max(scale_range)
                trust_percent = ((trust_level - scale_min) / (scale_max - scale_min)) * 100
                
                learning_data = {
                    'question_type': f'trust_{entity.lower().replace(" ", "_")}',
                    'strategy_used': 'trust_rating',
                    'trust_level': trust_percent,
                    'scale_type': scale_type,
                    'actual_value': trust_level,
                    'entity': entity,
                    'success': success,
                    'confidence_score': 0.9
                }
                
                # Store in learned automations
                self.brain.learn_successful_automation(learning_data)
                
                print(f"🧠 Learned: {entity} → {trust_level} ({trust_percent:.0f}% trust)")
    
    def analyze_entity_type(self, entity: str, context: str) -> str:
        """
        Analyze what type of entity is being rated
        
        Returns:
            Entity type: 'company', 'brand', 'website', 'source', 'person', or 'unknown'
        """
        entity_lower = entity.lower()
        context_lower = context.lower()
        
        # Check entity categories from patterns
        entity_types = self.brain.get('question_patterns', {}).get(
            'trust_rating_questions', {}
        ).get('trust_entities', {})
        
        for entity_type, keywords in entity_types.items():
            if any(keyword in entity_lower or keyword in context_lower for keyword in keywords):
                return entity_type.rstrip('s')  # Remove plural
        
        return 'unknown'
    
    def get_entity_trust_history(self, entity: str) -> List[Dict[str, Any]]:
        """Get history of trust ratings for an entity"""
        if entity in self.entity_trust_history:
            return self.entity_trust_history[entity]
        return []