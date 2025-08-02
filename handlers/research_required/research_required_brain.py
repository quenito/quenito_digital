#!/usr/bin/env python3
"""
🧠 Research Required Brain Module
Integrates with knowledge base for learning and intelligence
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

class ResearchRequiredBrain:
    """Brain integration for research required learning"""
    
    def __init__(self, knowledge_base):
        """Initialize with knowledge base connection"""
        self.brain = knowledge_base
        self.research_history = []
        self.skip_success_rate = {}
        print("🧠 Research Required Brain module initialized")
    
    def learn_from_research_handling(self, question_text: str, strategy_used: str, 
                                   success: bool, research_type: str) -> None:
        """Learn from how research questions were handled"""
        try:
            learning_data = {
                'question_text': question_text,
                'strategy_used': strategy_used,
                'success': success,
                'research_type': research_type,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in brain
            if hasattr(self.brain, 'store_handler_improvement_pattern'):
                self.brain.store_handler_improvement_pattern(
                    handler_type='research_required',
                    pattern_type='research_handling',
                    pattern_data=learning_data,
                    success_indicator='handled_successfully' if success else 'needs_improvement'
                )
                print(f"🧠 Learned research handling pattern: {strategy_used} ({research_type})")
            
            # Update local history
            self.research_history.append(learning_data)
            
            # Track skip success rate
            if strategy_used == 'skip':
                if research_type not in self.skip_success_rate:
                    self.skip_success_rate[research_type] = {'success': 0, 'total': 0}
                
                self.skip_success_rate[research_type]['total'] += 1
                if success:
                    self.skip_success_rate[research_type]['success'] += 1
            
        except Exception as e:
            print(f"❌ Error learning from research handling: {e}")
    
    def get_best_strategy(self, research_type: str, available_strategies: List[str]) -> str:
        """Get the best strategy based on learning"""
        try:
            # Check skip success rate for this research type
            if 'skip' in available_strategies and research_type in self.skip_success_rate:
                rate_data = self.skip_success_rate[research_type]
                if rate_data['total'] > 3:  # Need enough data
                    success_rate = rate_data['success'] / rate_data['total']
                    if success_rate > 0.8:  # 80% success rate
                        print(f"🧠 Skip strategy recommended (success rate: {success_rate:.1%})")
                        return 'skip'
            
            # Check historical patterns
            recent_successes = self._get_recent_successes(research_type)
            if recent_successes:
                # Get most successful strategy
                strategy_counts = {}
                for entry in recent_successes:
                    strategy = entry['strategy_used']
                    strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
                
                best_strategy = max(strategy_counts, key=strategy_counts.get)
                if best_strategy in available_strategies:
                    print(f"🧠 Historical data suggests: {best_strategy}")
                    return best_strategy
            
            # Default preference order
            preference_order = ['skip', 'placeholder', 'acknowledge']
            for strategy in preference_order:
                if strategy in available_strategies:
                    return strategy
            
            return available_strategies[0] if available_strategies else 'placeholder'
            
        except Exception as e:
            print(f"❌ Error getting best strategy: {e}")
            return 'placeholder'
    
    def _get_recent_successes(self, research_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent successful handlings of this research type"""
        successes = []
        
        for entry in reversed(self.research_history):
            if (entry.get('research_type') == research_type and 
                entry.get('success', False)):
                successes.append(entry)
                if len(successes) >= limit:
                    break
        
        return successes
    
    def generate_intelligent_placeholder(self, research_type: str, topics: List[str]) -> str:
        """Generate an intelligent placeholder based on learning"""
        try:
            # Base templates by research type
            templates = {
                'product': "Product research pending: {details}",
                'company': "Company analysis to be conducted: {details}",
                'market': "Market research required: {details}",
                'technical': "Technical specifications to be gathered: {details}",
                'general': "Research pending: {details}"
            }
            
            template = templates.get(research_type, templates['general'])
            
            # Create details from topics
            if topics:
                details = ", ".join(topics[:3])  # First 3 topics
                if len(topics) > 3:
                    details += f" and {len(topics) - 3} more items"
            else:
                details = "comprehensive analysis required"
            
            response = template.format(details=details)
            
            # Add timestamp if learned to be useful
            if self._should_add_timestamp(research_type):
                response += f" (as of {datetime.now().strftime('%Y-%m-%d')})"
            
            return response
            
        except Exception as e:
            print(f"❌ Error generating placeholder: {e}")
            return "Research pending"
    
    def _should_add_timestamp(self, research_type: str) -> bool:
        """Check if timestamps improve success rate"""
        # This would check historical data to see if timestamps help
        # For now, return True for time-sensitive research types
        return research_type in ['market', 'technical']
    
    def analyze_research_patterns(self) -> Dict[str, Any]:
        """Analyze learned research patterns for reporting"""
        analysis = {
            'total_research_questions': len(self.research_history),
            'strategies_used': {},
            'success_by_type': {},
            'skip_effectiveness': {},
            'common_research_types': {},
            'learning_insights': []
        }
        
        if not self.research_history:
            return analysis
        
        # Analyze strategies used
        for entry in self.research_history:
            strategy = entry.get('strategy_used', 'unknown')
            analysis['strategies_used'][strategy] = \
                analysis['strategies_used'].get(strategy, 0) + 1
        
        # Success by research type
        type_stats = {}
        for entry in self.research_history:
            research_type = entry.get('research_type', 'unknown')
            if research_type not in type_stats:
                type_stats[research_type] = {'success': 0, 'total': 0}
            
            type_stats[research_type]['total'] += 1
            if entry.get('success', False):
                type_stats[research_type]['success'] += 1
        
        for research_type, stats in type_stats.items():
            if stats['total'] > 0:
                analysis['success_by_type'][research_type] = \
                    stats['success'] / stats['total']
        
        # Skip effectiveness
        analysis['skip_effectiveness'] = {
            research_type: (data['success'] / data['total']) if data['total'] > 0 else 0
            for research_type, data in self.skip_success_rate.items()
        }
        
        # Common research types
        research_type_counts = {}
        for entry in self.research_history:
            research_type = entry.get('research_type', 'unknown')
            research_type_counts[research_type] = \
                research_type_counts.get(research_type, 0) + 1
        
        analysis['common_research_types'] = dict(
            sorted(research_type_counts.items(), 
                  key=lambda x: x[1], 
                  reverse=True)[:5]
        )
        
        # Generate insights
        if analysis['skip_effectiveness']:
            best_skip_type = max(analysis['skip_effectiveness'], 
                               key=analysis['skip_effectiveness'].get)
            if analysis['skip_effectiveness'][best_skip_type] > 0.8:
                analysis['learning_insights'].append(
                    f"Skip strategy highly effective for {best_skip_type} research ({analysis['skip_effectiveness'][best_skip_type]:.0%} success)"
                )
        
        return analysis
    
    def should_attempt_research(self, research_type: str, complexity: str = 'medium') -> bool:
        """Determine if we should attempt to handle this research question"""
        # Check historical success rates
        if research_type in self.skip_success_rate:
            rate_data = self.skip_success_rate[research_type]
            if rate_data['total'] > 5:
                success_rate = rate_data['success'] / rate_data['total']
                if success_rate < 0.3:  # Low success rate
                    print(f"⚠️ Low success rate for {research_type} research ({success_rate:.0%})")
                    return False
        
        # Complexity check
        if complexity == 'high':
            # Only attempt if we have good historical data
            recent_successes = self._get_recent_successes(research_type, limit=3)
            if len(recent_successes) < 2:
                print("⚠️ High complexity research without sufficient learning data")
                return False
        
        return True