"""
Survey Automation Utility Services
Enhanced with brain intelligence and stealth reporting.
"""

from .knowledge_base import KnowledgeBase
from .reporting import BrainEnhancedReportGenerator, ReportGenerator

# Import existing components
try:
    from .intervention_manager import EnhancedLearningInterventionManager
except ImportError:
    EnhancedLearningInterventionManager = None

try:
    from .research_engine import ResearchEngine
except ImportError:
    ResearchEngine = None

__all__ = [
    'KnowledgeBase',
    'BrainEnhancedReportGenerator',
    'ReportGenerator'
]

if EnhancedLearningInterventionManager:
    __all__.append('EnhancedLearningInterventionManager')
    
if ResearchEngine:
    __all__.append('ResearchEngine')
