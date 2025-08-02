"""
🎯 Base Platform Adapter
Abstract interface that all platform adapters must implement
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from dataclasses import dataclass


@dataclass
class Survey:
    """Survey data structure"""
    id: str
    title: str
    points: int
    time_minutes: int
    dollar_value: float
    hourly_rate: float
    element: Any  # Playwright element
    metadata: Dict = None


class BasePlatformAdapter(ABC):
    """
    Abstract base class for all survey platform adapters.
    Provides common functionality and enforces interface.
    """
    
    def __init__(self, stealth_browser_manager, persona_name: str):
        self.browser = stealth_browser_manager
        self.page = None
        self.persona_name = persona_name
        self.platform_name = ""
        self.base_url = ""
        self.points_per_dollar = 100
        
        # Setup logging
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        
        # Common selectors (override in subclasses)
        self.selectors = {
            "dashboard": "",
            "survey_list": "",
            "points": "",
            "time": "",
            "start_button": ""
        }
        
        # Session tracking
        self.session_start = None
        self.surveys_completed = 0
        self.total_points_earned = 0
        
    async def initialize_session(self) -> bool:
        """Initialize platform session with stealth browser"""
        try:
            self.logger.info(f"Initializing {self.platform_name} session for {self.persona_name}")
            
            # Get browser page from stealth manager
            self.page = await self.browser.initialize_stealth_browser(
                transfer_cookies=True,
                use_existing_chrome=False
            )
            
            self.session_start = datetime.now()
            return True
            
        except Exception as e:
            self.logger.error(f"Session initialization failed: {e}")
            return False
    
    @abstractmethod
    async def navigate_to_surveys(self) -> bool:
        """Navigate to platform's survey listing page"""
        pass
    
    @abstractmethod
    async def get_available_surveys(self) -> List[Survey]:
        """Extract all available surveys from current page"""
        pass
    
    @abstractmethod
    async def select_best_survey(self, surveys: List[Survey]) -> Optional[Survey]:
        """Select optimal survey based on platform-specific logic"""
        pass
    
    @abstractmethod
    async def start_survey(self, survey: Survey) -> bool:
        """Begin selected survey"""
        pass
    
    @abstractmethod
    async def is_survey_complete(self) -> bool:
        """Check if current survey is finished"""
        pass
    
    @abstractmethod
    def convert_points_to_currency(self, points: int) -> float:
        """Convert platform points to AUD"""
        pass
    
    @abstractmethod
    async def track_bonus_progress(self) -> Dict:
        """Monitor bonus tier and weekly earnings"""
        pass
    
    async def handle_screen_out(self) -> bool:
        """Handle screen-out scenarios"""
        self.logger.warning("Screen-out detected")
        # Default behavior - return to dashboard
        return await self.navigate_to_surveys()
    
    async def save_session_state(self):
        """Save current session progress"""
        state = {
            "platform": self.platform_name,
            "persona": self.persona_name,
            "session_start": self.session_start.isoformat() if self.session_start else None,
            "surveys_completed": self.surveys_completed,
            "total_points_earned": self.total_points_earned,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to persona's session log
        import json
        session_file = f"personas/{self.persona_name}/sessions/{self.platform_name}_session.json"
        
        try:
            with open(session_file, 'w') as f:
                json.dump(state, f, indent=2)
            self.logger.info("Session state saved")
        except Exception as e:
            self.logger.error(f"Failed to save session state: {e}")
    
    async def wait_human_like(self, min_ms: int = 1000, max_ms: int = 3000):
        """Add human-like delay between actions"""
        import random
        delay = random.randint(min_ms, max_ms)
        await self.page.wait_for_timeout(delay)
    
    async def check_login_status(self) -> bool:
        """Verify if we're logged into the platform"""
        current_url = self.page.url.lower()
        login_indicators = ['login', 'signin', 'authenticate']
        
        return not any(indicator in current_url for indicator in login_indicators)
    
    def calculate_survey_value(self, survey: Survey) -> Dict:
        """Calculate comprehensive survey value metrics"""
        return {
            "dollar_value": survey.dollar_value,
            "hourly_rate": survey.hourly_rate,
            "efficiency_score": survey.hourly_rate / max(survey.time_minutes, 1),
            "recommended": survey.hourly_rate > 15 and survey.time_minutes < 30
        }