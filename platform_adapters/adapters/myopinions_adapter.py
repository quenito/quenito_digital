# platform_adapters/adapters/myopinions_adapter.py
"""
MyOpinions Platform Adapter - Integrated with Flow Handler
Handles survey detection AND complete flow automation
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from platform_adapters.base_adapter import BasePlatformAdapter
from platform_adapters.flow_handlers.myopinions_flow_handler import MyOpinionsFlowHandler

class MyOpinionsAdapter(BasePlatformAdapter):
    """MyOpinions.com.au platform adapter with integrated flow handling"""
    
    def __init__(self, browser_manager, persona_name="quenito"):
        super().__init__(browser_manager, persona_name)
        self.platform_name = "myopinions"
        self.base_url = "https://www.myopinions.com.au"
        self.points_per_dollar = 100  # 2000 points = $20 AUD
        self.flow_handler = MyOpinionsFlowHandler(browser_manager)
        self.page = browser_manager.page
        
        # Platform-specific selectors
        self.selectors = {
            "dashboard": "div.dashboard-content",
            "survey_list": "div.survey-list-item",
            "points": "span.survey-points",
            "time": "span.survey-duration",
            "start_button": "a.btn.btn-primary",  # FIXED: Now using <a> tags
            "bonus_indicator": "div.bonus-tier-badge"
        }
        
        # Bonus tier configuration
        self.bonus_tiers = {
            "starter": 0.00,
            "bronze": 0.05,    # 5% weekly bonus
            "silver": 0.075,   # 7.5% weekly bonus  
            "gold": 0.10       # 10% weekly bonus
        }
    
    # ==================== REQUIRED ABSTRACT METHODS ====================
    
    async def convert_points_to_currency(self, points: int) -> float:
        """
        Convert points to AUD currency
        2000 points = $20 AUD
        """
        return points / self.points_per_dollar
    
    async def get_available_surveys(self) -> List[Dict[str, Any]]:
        """
        Get available surveys - wraps detect_available_surveys
        Required by base adapter
        """
        return await self.detect_available_surveys()
    
    async def is_survey_complete(self) -> bool:
        """
        Check if current survey is complete
        For now, return False (manual completion required)
        """
        # In future, check for completion indicators like:
        # - "Thank you" page
        # - Points credited message
        # - Return to dashboard button
        return False
    
    async def select_best_survey(self, surveys: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Select the best survey from available options
        Strategy: Highest points first
        """
        if not surveys:
            return None
        
        # Already sorted by points in detect_available_surveys
        return surveys[0]
    
    async def track_bonus_progress(self) -> Dict[str, Any]:
        """
        Track bonus tier progress
        MyOpinions has weekly bonus tiers
        """
        try:
            # Look for bonus tier indicator on dashboard
            bonus_elem = await self.page.query_selector(self.selectors['bonus_indicator'])
            
            if bonus_elem:
                bonus_text = await bonus_elem.inner_text()
                
                # Parse tier from text
                tier = "starter"
                for tier_name in ["gold", "silver", "bronze"]:
                    if tier_name.lower() in bonus_text.lower():
                        tier = tier_name
                        break
                
                return {
                    "tier": tier,
                    "bonus_rate": self.bonus_tiers.get(tier, 0),
                    "text": bonus_text
                }
            
            return {
                "tier": "starter",
                "bonus_rate": 0,
                "text": "No bonus active"
            }
            
        except Exception as e:
            print(f"❌ Error tracking bonus: {e}")
            return {
                "tier": "unknown",
                "bonus_rate": 0,
                "text": "Could not detect bonus"
            }
    
    # ==================== EXISTING METHODS ====================
    
    async def navigate_to_surveys(self) -> bool:
        """Navigate to survey dashboard"""
        try:
            await self.page.goto(f"{self.base_url}/auth/dashboard", 
                                wait_until="networkidle")
            
            # Verify we're logged in
            if "login" in self.page.url.lower():
                print("❌ Not logged in - manual login required")
                return False
                
            print("✅ Successfully navigated to dashboard")
            return True
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
    
    async def detect_available_surveys(self) -> List[Dict[str, Any]]:
        """
        Detect available surveys on MyOpinions dashboard
        Now correctly detects <a> tag buttons
        """
        surveys = []
        
        try:
            # Wait for survey cards to load
            await self.page.wait_for_selector('.card', timeout=10000)
            
            # Find all survey cards
            cards = await self.page.query_selector_all('.card')
            
            for card in cards:
                try:
                    # Extract survey details
                    points_elem = await card.query_selector('.card-body-points')
                    time_elem = await card.query_selector('.card-body-loi')
                    topic_elem = await card.query_selector('.card-body-topic')
                    
                    # Look for <a> tags with btn btn-primary class
                    button_elem = await card.query_selector('a.btn.btn-primary')
                    
                    if button_elem:
                        # Get button text and URL
                        button_text = await button_elem.inner_text()
                        button_href = await button_elem.get_attribute('href')
                        
                        # Extract points value
                        points_text = await points_elem.inner_text() if points_elem else "0"
                        points = int(''.join(filter(str.isdigit, points_text.split()[0])))
                        
                        # Extract time estimate
                        time_text = await time_elem.inner_text() if time_elem else "Unknown"
                        
                        # Extract topic
                        topic_text = await topic_elem.inner_text() if topic_elem else "General"
                        
                        # Determine survey type
                        survey_type = "qualification" if "QUALIFICATION" in button_text else "survey"
                        
                        survey_info = {
                            'points': points,
                            'time': time_text,
                            'topic': topic_text,
                            'type': survey_type,
                            'button_text': button_text,
                            'url': button_href,
                            'element': button_elem  # Store for clicking
                        }
                        
                        surveys.append(survey_info)
                        
                except Exception as e:
                    print(f"Error parsing survey card: {e}")
                    continue
            
            print(f"✅ Found {len(surveys)} available surveys")
            
            # Sort by points (highest first)
            surveys.sort(key=lambda x: x['points'], reverse=True)
            
            return surveys
            
        except Exception as e:
            print(f"❌ Error detecting surveys: {e}")
            return []
    
    async def prepare_dashboard(self) -> bool:
        """
        Prepare dashboard by handling popups
        Uses the flow handler for consistency
        """
        try:
            print("🎯 Preparing dashboard...")
            return await self.flow_handler.handle_dashboard_popups(self.page)
        except Exception as e:
            print(f"❌ Error preparing dashboard: {e}")
            return False
    
    async def start_survey(self, survey_info: Dict[str, Any]) -> bool:
        """
        Start a survey using the complete flow handler
        This is the main integration point!
        """
        try:
            print(f"\n🚀 Starting survey automation...")
            print(f"   Survey: {survey_info['points']} points - {survey_info['topic']}")
            
            # Use the flow handler for the complete process
            return await self.flow_handler.run_complete_flow(survey_info)
            
        except Exception as e:
            print(f"❌ Error starting survey: {e}")
            return False
    
    async def run_survey_session(self) -> Dict[str, Any]:
        """
        Complete survey session with automatic survey selection
        Returns session results
        """
        results = {
            'started': datetime.now(),
            'surveys_completed': 0,
            'points_earned': 0,
            'errors': []
        }
        
        try:
            # Step 1: Navigate to dashboard
            if not await self.navigate_to_surveys():
                results['errors'].append("Failed to navigate to dashboard")
                return results
            
            # Step 2: Prepare dashboard (close popups)
            await self.prepare_dashboard()
            
            # Step 3: Detect available surveys
            surveys = await self.detect_available_surveys()
            
            if not surveys:
                results['errors'].append("No surveys available")
                return results
            
            # Step 4: Start best survey
            best_survey = surveys[0]
            
            if await self.start_survey(best_survey):
                results['surveys_attempted'] = 1
                results['current_survey'] = best_survey
                print("\n✅ Survey session started successfully!")
            else:
                results['errors'].append("Failed to start survey")
                
            results['ended'] = datetime.now()
            return results
            
        except Exception as e:
            results['errors'].append(str(e))
            results['ended'] = datetime.now()
            return results
    
    def get_points_value(self, points: int) -> float:
        """Convert points to AUD value"""
        return points / self.points_per_dollar
    
    async def check_bonus_tier(self) -> Optional[str]:
        """Check current bonus tier status"""
        try:
            # Look for bonus tier indicator on page
            tier_elem = await self.page.query_selector('.tier-badge, .bonus-tier')
            if tier_elem:
                tier_text = await tier_elem.inner_text()
                tier_lower = tier_text.lower()
                
                for tier_name in self.bonus_tiers.keys():
                    if tier_name in tier_lower:
                        print(f"🏆 Current tier: {tier_name} ({self.bonus_tiers[tier_name]*100}% bonus)")
                        return tier_name
                        
            return "starter"
            
        except Exception as e:
            print(f"Error checking bonus tier: {e}")
            return None