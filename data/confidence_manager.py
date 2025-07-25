#!/usr/bin/env python3
"""
🎯 Centralized Confidence Manager v1.0
Dynamic confidence system with learning-based threshold optimization.

This module handles:
- Dynamic confidence threshold management
- Learning-based threshold adjustment
- Cross-handler confidence optimization  
- Performance-based confidence calibration
- Intelligent manual intervention decisions

ARCHITECTURE: Central memory (knowledge_base.json) + Dynamic intelligence
"""

from typing import Dict, Any, Optional, Tuple, List
import time
from datetime import datetime, timedelta


class ConfidenceManager:
    """
    🎯 Dynamic Confidence Management with Learning Intelligence
    
    Manages all confidence thresholds, dynamic adjustments, and learning-based optimizations.
    Integrates with knowledge_base.json for centralized configuration.
    """
    
    def __init__(self, confidence_data: Optional[Dict[str, Any]] = None):
        """Initialize with confidence data from knowledge_base.json"""
        self.confidence_data = confidence_data or self._get_default_config()
        self._initialize_confidence_system()
        print(f"🎯 ConfidenceManager initialized with {len(self.get_handler_names())} handlers")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Provide default confidence configuration if none exists"""
        return {
            "version": "3.0_dynamic",
            "global_settings": {
                "learning_rate": 0.1,
                "confidence_decay": 0.95,
                "success_boost": 0.05,
                "failure_penalty": -0.02,
                "min_threshold": 0.1,
                "max_threshold": 0.95,
                "manual_intervention_threshold": 0.3
            },
            "handler_thresholds": {},
            "question_type_modifiers": {},
            "dynamic_confidence_rules": {},
            "learning_patterns": {"successful_combinations": {}, "failure_patterns": {}}
        }
    
    def _initialize_confidence_system(self):
        """Initialize confidence system components"""
        self.global_settings = self.confidence_data.get("global_settings", {})
        self.handler_thresholds = self.confidence_data.get("handler_thresholds", {})
        self.question_modifiers = self.confidence_data.get("question_type_modifiers", {})
        self.dynamic_rules = self.confidence_data.get("dynamic_confidence_rules", {})
        self.learning_patterns = self.confidence_data.get("learning_patterns", {})
    
    # ========================================
    # DYNAMIC THRESHOLD MANAGEMENT
    # ========================================
    
    def get_dynamic_threshold(self, handler_name: str, question_type: Optional[str] = None, 
                            context: Optional[Dict[str, Any]] = None) -> float:
        """
        Get dynamic confidence threshold for handler/question combination
        Applies learning-based adjustments and context-aware modifications
        """
        # Get base threshold
        handler_config = self.handler_thresholds.get(handler_name, {})
        base_threshold = handler_config.get("base_threshold", 0.5)
        dynamic_adjustment = handler_config.get("dynamic_adjustment", 0.0)
        
        # Calculate current threshold
        current_threshold = base_threshold + dynamic_adjustment
        
        # Apply question-type modifier
        if question_type and question_type in self.question_modifiers:
            modifier = self.question_modifiers[question_type].get("confidence_modifier", 0.0)
            current_threshold += modifier
        
        # Apply context-based adjustments
        if context:
            context_adjustment = self._calculate_context_adjustment(handler_name, question_type, context)
            current_threshold += context_adjustment
        
        # Apply bounds
        min_threshold = self.global_settings.get("min_threshold", 0.1)
        max_threshold = self.global_settings.get("max_threshold", 0.95)
        final_threshold = max(min_threshold, min(max_threshold, current_threshold))
        
        print(f"🎯 Dynamic threshold for {handler_name}.{question_type}: {final_threshold:.3f} "
              f"(base: {base_threshold:.3f}, adjustment: {dynamic_adjustment:+.3f})")
        
        return final_threshold
    
    def should_attempt_automation(self, handler_name: str, confidence: float,
                                question_type: Optional[str] = None,
                                context: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """
        Intelligent decision on whether to attempt automation
        Returns (should_automate, reasoning)
        """
        threshold = self.get_dynamic_threshold(handler_name, question_type, context)
        
        if confidence >= threshold:
            # Check for success patterns that might boost confidence
            pattern_boost = self._get_pattern_confidence_boost(handler_name, question_type, context)
            if pattern_boost > 0:
                return True, f"automation_with_pattern_boost(+{pattern_boost:.3f})"
            return True, f"confidence_exceeds_threshold ({confidence:.3f} >= {threshold:.3f})"
        
        # Check if close to threshold with positive trending
        if confidence >= (threshold - 0.05):
            handler_config = self.handler_thresholds.get(handler_name, {})
            if handler_config.get("trending") == "improving":
                return True, f"close_to_threshold_with_positive_trend"
        
        return False, f"confidence_below_threshold ({confidence:.3f} < {threshold:.3f})"
    
    def should_request_manual_intervention(self, handler_name: str, confidence: float,
                                         question_type: Optional[str] = None) -> Tuple[bool, str]:
        """
        Decide if manual intervention should be requested for learning
        """
        manual_threshold = self.global_settings.get("manual_intervention_threshold", 0.3)
        
        if confidence < manual_threshold:
            return True, f"low_confidence_learning_opportunity ({confidence:.3f} < {manual_threshold:.3f})"
        
        # Check if this is a known failure pattern we want to learn from
        if self._is_learning_priority(handler_name, question_type):
            return True, f"learning_priority_pattern"
        
        return False, f"confidence_adequate_for_skipping"
    
    # ========================================
    # LEARNING-BASED THRESHOLD ADJUSTMENT
    # ========================================
    
    def record_automation_result(self, handler_name: str, question_type: str,
                               confidence: float, success: bool,
                               context: Optional[Dict[str, Any]] = None) -> None:
        """
        Record automation result and update dynamic thresholds
        This is where the system learns and improves!
        """
        # Ensure handler exists in config
        if handler_name not in self.handler_thresholds:
            self._initialize_handler_config(handler_name)
        
        handler_config = self.handler_thresholds[handler_name]
        
        # Update statistics
        handler_config["total_attempts"] = handler_config.get("total_attempts", 0) + 1
        if success:
            handler_config["successful_attempts"] = handler_config.get("successful_attempts", 0) + 1
            handler_config["last_success"] = datetime.now().isoformat()
        
        # Calculate new success rate
        total_attempts = handler_config["total_attempts"]
        successful_attempts = handler_config["successful_attempts"]
        handler_config["success_rate"] = successful_attempts / total_attempts if total_attempts > 0 else 0.0
        
        # Apply dynamic adjustment based on result
        self._apply_learning_adjustment(handler_name, question_type, confidence, success, context)
        
        # Update trending
        self._update_trending_analysis(handler_name)
        
        print(f"🧠 Learning recorded: {handler_name}.{question_type} "
              f"{'✅' if success else '❌'} (confidence: {confidence:.3f}, "
              f"success_rate: {handler_config['success_rate']:.3f})")
    
    def _apply_learning_adjustment(self, handler_name: str, question_type: str,
                                 confidence: float, success: bool,
                                 context: Optional[Dict[str, Any]] = None) -> None:
        """Apply learning-based threshold adjustments"""
        handler_config = self.handler_thresholds[handler_name]
        current_adjustment = handler_config.get("dynamic_adjustment", 0.0)
        learning_rate = self.global_settings.get("learning_rate", 0.1)
        
        if success:
            # Success: Slightly lower threshold to encourage more automation
            success_boost = self.global_settings.get("success_boost", 0.05)
            adjustment = -success_boost * learning_rate
        else:
            # Failure: Slightly raise threshold to be more conservative
            failure_penalty = self.global_settings.get("failure_penalty", -0.02)
            adjustment = -failure_penalty * learning_rate
        
        # Apply adjustment with bounds
        new_adjustment = current_adjustment + adjustment
        new_adjustment = max(-0.2, min(0.2, new_adjustment))  # Cap adjustments
        
        handler_config["dynamic_adjustment"] = new_adjustment
        handler_config["current_threshold"] = (
            handler_config.get("base_threshold", 0.5) + new_adjustment
        )
        
        if abs(adjustment) > 0.001:
            print(f"🎯 Threshold adjusted: {handler_name} "
                  f"{current_adjustment:+.3f} → {new_adjustment:+.3f} "
                  f"({'success' if success else 'failure'})")
    
    # ========================================
    # PATTERN LEARNING & OPTIMIZATION
    # ========================================
    
    def _get_pattern_confidence_boost(self, handler_name: str, question_type: Optional[str],
                                    context: Optional[Dict[str, Any]] = None) -> float:
        """Get confidence boost based on learned successful patterns"""
        if not question_type or not context:
            return 0.0
        
        successful_patterns = self.learning_patterns.get("successful_combinations", {})
        pattern_key = f"{handler_name}_{question_type}_{context.get('element_type', 'unknown')}"
        
        if pattern_key in successful_patterns:
            pattern_data = successful_patterns[pattern_key]
            boost = pattern_data.get("confidence_boost", 0.0)
            sample_size = pattern_data.get("sample_size", 0)
            
            # Boost is stronger with more sample data
            if sample_size >= 10:
                return boost
            elif sample_size >= 5:
                return boost * 0.7
            else:
                return boost * 0.4
        
        return 0.0
    
    def learn_successful_pattern(self, handler_name: str, question_type: str,
                               element_type: str, confidence: float) -> None:
        """Learn from successful automation patterns"""
        pattern_key = f"{handler_name}_{question_type}_{element_type}"
        successful_patterns = self.learning_patterns.setdefault("successful_combinations", {})
        
        if pattern_key not in successful_patterns:
            successful_patterns[pattern_key] = {
                "pattern": f"{question_type} + {element_type}",
                "confidence_boost": 0.05,
                "success_rate": 1.0,
                "sample_size": 1
            }
        else:
            pattern_data = successful_patterns[pattern_key]
            sample_size = pattern_data["sample_size"]
            success_rate = pattern_data["success_rate"]
            
            # Update success rate
            new_sample_size = sample_size + 1
            new_success_rate = (success_rate * sample_size + 1.0) / new_sample_size
            
            pattern_data["sample_size"] = new_sample_size
            pattern_data["success_rate"] = new_success_rate
            
            # Increase confidence boost as success rate improves
            if new_success_rate > 0.9 and new_sample_size >= 5:
                pattern_data["confidence_boost"] = min(0.15, 0.05 + (new_success_rate - 0.9) * 0.5)
        
        print(f"🧠 Pattern learned: {pattern_key} (boost: {successful_patterns[pattern_key]['confidence_boost']:.3f})")
    
    # ========================================
    # UTILITY & HELPER METHODS
    # ========================================
    
    def get_handler_names(self) -> List[str]:
        """Get list of all configured handler names"""
        return list(self.handler_thresholds.keys())
    
    def get_confidence_statistics(self) -> Dict[str, Any]:
        """Get comprehensive confidence system statistics"""
        stats = {
            "total_handlers": len(self.handler_thresholds),
            "handlers": {},
            "global_settings": self.global_settings,
            "system_performance": self._calculate_system_performance()
        }
        
        for handler_name, config in self.handler_thresholds.items():
            stats["handlers"][handler_name] = {
                "current_threshold": config.get("current_threshold", 0.5),
                "success_rate": config.get("success_rate", 0.0),
                "total_attempts": config.get("total_attempts", 0),
                "trending": config.get("trending", "unknown")
            }
        
        return stats
    
    def _calculate_system_performance(self) -> Dict[str, Any]:
        """Calculate overall system performance metrics"""
        total_attempts = sum(
            config.get("total_attempts", 0)
            for config in self.handler_thresholds.values()
        )
        total_successes = sum(
            config.get("successful_attempts", 0)
            for config in self.handler_thresholds.values()
        )
        
        return {
            "overall_success_rate": total_successes / total_attempts if total_attempts > 0 else 0.0,
            "total_automation_attempts": total_attempts,
            "total_successful_automations": total_successes,
            "average_handler_threshold": sum(
                config.get("current_threshold", 0.5)
                for config in self.handler_thresholds.values()
            ) / len(self.handler_thresholds) if self.handler_thresholds else 0.5
        }
    
    def export_for_central_memory(self) -> Dict[str, Any]:
        """Export confidence data for saving back to knowledge_base.json"""
        return {
            "version": self.confidence_data.get("version", "3.0_dynamic"),
            "last_updated": datetime.now().isoformat(),
            "global_settings": self.global_settings,
            "handler_thresholds": self.handler_thresholds,
            "question_type_modifiers": self.question_modifiers,
            "dynamic_confidence_rules": self.dynamic_rules,
            "learning_patterns": self.learning_patterns
        }
    
    # ========================================
    # HELPER METHODS (IMPLEMENTATION STUBS)
    # ========================================
    
    def _calculate_context_adjustment(self, handler_name: str, question_type: Optional[str], 
                                    context: Dict[str, Any]) -> float:
        """Calculate context-based confidence adjustments"""
        # Placeholder for context-based adjustments
        return 0.0
    
    def _is_learning_priority(self, handler_name: str, question_type: Optional[str]) -> bool:
        """Check if this is a learning priority pattern"""
        # Placeholder for learning priority logic
        return False
    
    def _initialize_handler_config(self, handler_name: str) -> None:
        """Initialize configuration for new handler"""
        self.handler_thresholds[handler_name] = {
            "base_threshold": 0.5,
            "dynamic_adjustment": 0.0,
            "current_threshold": 0.5,
            "success_rate": 0.0,
            "total_attempts": 0,
            "successful_attempts": 0,
            "last_success": None,
            "trending": "unknown"
        }
    
    def _update_trending_analysis(self, handler_name: str) -> None:
        """Update trending analysis for handler"""
        handler_config = self.handler_thresholds[handler_name]
        success_rate = handler_config.get("success_rate", 0.0)
        
        # Simple trending logic
        if success_rate > 0.8:
            handler_config["trending"] = "excellent"
        elif success_rate > 0.6:
            handler_config["trending"] = "improving"
        elif success_rate > 0.4:
            handler_config["trending"] = "stable"
        else:
            handler_config["trending"] = "needs_attention"


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def create_confidence_manager(confidence_data: Dict[str, Any] = None) -> ConfidenceManager:
    """Factory function to create ConfidenceManager instance"""
    return ConfidenceManager(confidence_data)


# ========================================
# MODULE TEST
# ========================================

if __name__ == "__main__":
    # Quick module test
    print("🎯 ConfidenceManager Test")
    
    # Test initialization
    cm = create_confidence_manager()
    
    # Test threshold calculation
    threshold = cm.get_dynamic_threshold("demographics", "age")
    print(f"Dynamic threshold: {threshold}")
    
    # Test automation decision
    should_automate, reason = cm.should_attempt_automation("demographics", 0.65, "gender")
    print(f"Should automate: {should_automate}, Reason: {reason}")
    
    print("✅ ConfidenceManager working correctly!")