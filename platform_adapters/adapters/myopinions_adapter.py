"""
🎯 MyOpinions.com.au Platform Adapter
Handles all MyOpinions-specific automation logic
"""

import re
import json
import random
from typing import List, Dict, Optional
from datetime import datetime
import logging

from platform_adapters.base_adapter import BasePlatformAdapter, Survey


class MyOpinionsAdapter(BasePlatformAdapter):
    """
    MyOpinions.com.au specific platform adapter.
    Handles navigation, survey selection, and bonus optimization.
    """
    
    def __init__(self, stealth_browser_manager, persona_name: str):
        super().__init__(stealth_browser_manager, persona_name)
        
        # Platform configuration
        self.platform_name = "myopinions"
        self.base_url = "https://www.myopinions.com.au"
        self.points_per_dollar = 100  # 2000 points = $20 AUD
        
        # MyOpinions specific selectors
        self.selectors = {
            # Dashboard elements
            "dashboard": "div.dashboard-container",
            "points_balance": "span.points-balance",
            "tier_badge": "div.tier-status",
            
            # Survey list elements
            "survey_list": "div[class*='survey'], div.card, a[href*='start-survey']",  
            "survey_title": "h3, h4, div.title", 
            "points": "span[class*='point'], div[class*='point']",  
            "time": "span[class*='time'], span[class*='min'], div[class*='duration']",
            "start_button": "button, a", 
            
            # Survey page elements
            "survey_complete": "div.survey-complete, div.completion-message",
            "screen_out": "div.screened-out, div.disqualified",
            
            # Bonus elements
            "weekly_bonus": "div.weekly-bonus-progress",
            "tier_progress": "div.tier-progress-bar"
        }
        
        # Bonus tier configuration
        self.bonus_tiers = {
            "starter": {"rate": 0.00, "next_tier_points": 10000},
            "bronze": {"rate": 0.05, "next_tier_points": 25000},
            "silver": {"rate": 0.075, "next_tier_points": 50000},
            "gold": {"rate": 0.10, "next_tier_points": None}
        }
        
        # Survey selection preferences
        self.preferences = {
            "min_hourly_rate": 12.0,  # $12/hour minimum
            "max_time_minutes": 45,    # Avoid very long surveys initially
            "min_points": 100,         # Minimum 100 points ($1)
            "preferred_topics": ["consumer", "technology", "lifestyle"]
        }
        
        self.logger = logging.getLogger("MyOpinionsAdapter")
    
    async def navigate_to_surveys(self) -> bool:
        """Navigate to MyOpinions survey dashboard"""
        try:
            self.logger.info("Navigating to MyOpinions dashboard")
            
            # Go to dashboard
            await self.page.goto(
                f"{self.base_url}/auth/dashboard",
                wait_until="domcontentloaded"  # Changed from networkidle
            )
            
            # Wait for page to fully load
            await self.page.wait_for_load_state("domcontentloaded")
            await self.wait_human_like(2000, 3000)  # Increased wait time
            
            # Verify we're logged in
            if not await self.check_login_status():
                self.logger.error("Not logged in - cookie transfer may have failed")
                return False
            
            # Wait for survey list to appear - with longer timeout
            try:
                # Try multiple possible selectors
                survey_selectors = [
                    "div[class*='survey']",
                    "div.card",
                    "a[href*='start-survey']",
                    "[class*='RECOMMENDED']",
                    "[class*='HIGH REWARD']"
                ]
                
                found = False
                for selector in survey_selectors:
                    try:
                        await self.page.wait_for_selector(selector, timeout=5000)
                        found = True
                        self.logger.info(f"Found surveys with selector: {selector}")
                        break
                    except:
                        continue
                
                if found:
                    # Extra wait for all surveys to load
                    await self.page.wait_for_timeout(2000)
                    return True
                else:
                    self.logger.warning("No surveys found after checking all selectors")
                    # Take a screenshot for debugging
                    await self.page.screenshot(path="no_surveys_debug.png")
                    return False
                    
            except:
                self.logger.warning("No surveys currently available")
                return False
                
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            return False
    
    async def get_available_surveys(self) -> List[Survey]:
        """Extract all available surveys from MyOpinions dashboard"""
        surveys = []
        
        try:
            # Try multiple selectors
            possible_selectors = [
                "div[class*='survey']",
                "div.card:has(button)",
                "a[href*='start-survey']",
                "div:has(> button:has-text('START SURVEY'))",
                "[class*='survey-item']"
            ]
            
            survey_elements = []
            for selector in possible_selectors:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    survey_elements = elements
                    self.logger.info(f"Found {len(elements)} surveys with selector: {selector}")
                    break
            
            if not survey_elements:
                self.logger.warning("No survey elements found with any selector")
                # Debug: print page content
                content = await self.page.content()
                if len(content) > 1000:
                    self.logger.debug(f"Page loaded, content length: {len(content)}")
                return []
            
            for idx, element in enumerate(survey_elements):
                try:
                    # Get all text content from the element
                    text_content = await element.inner_text()
                    
                    # Extract points (look for patterns like "220 points", "900 points")
                    import re
                    points_match = re.search(r'(\d+)\s*points?', text_content, re.IGNORECASE)
                    points = int(points_match.group(1)) if points_match else 0
                    
                    # Extract time (look for patterns like "20 mins", "10 minutes")
                    time_match = re.search(r'(\d+)\s*min', text_content, re.IGNORECASE)
                    time_minutes = int(time_match.group(1)) if time_match else 15  # Default 15 mins
                    
                    # Extract title (first line or specific text)
                    lines = text_content.strip().split('\n')
                    title = lines[0] if lines else f"Survey {idx + 1}"
                    
                    # Skip if no points found
                    if points == 0:
                        continue
                    
                    # Calculate values
                    dollar_value = self.convert_points_to_currency(points)
                    hourly_rate = (dollar_value / time_minutes * 60) if time_minutes > 0 else 0
                    
                    # Check for bonus/recommended flags
                    is_recommended = "RECOMMENDED" in text_content.upper()
                    is_high_reward = "HIGH REWARD" in text_content.upper()
                    
                    survey = Survey(
                        id=f"myo_{idx}",
                        title=title.strip(),
                        points=points,
                        time_minutes=time_minutes,
                        dollar_value=dollar_value,
                        hourly_rate=hourly_rate,
                        element=element,
                        metadata={
                            "recommended": is_recommended,
                            "high_reward": is_high_reward,
                            "full_text": text_content
                        }
                    )
                    
                    surveys.append(survey)
                    
                    self.logger.debug(
                        f"Survey: {title[:30]}... | "
                        f"{points} pts | {time_minutes} min | "
                        f"${dollar_value:.2f} | ${hourly_rate:.2f}/hr"
                    )
                    
                except Exception as e:
                    self.logger.warning(f"Failed to parse survey {idx}: {e}")
                    continue
            
            return surveys
            
        except Exception as e:
            self.logger.error(f"Failed to extract surveys: {e}")
            return []
    
    async def select_best_survey(self, surveys: List[Survey]) -> Optional[Survey]:
        """
        Select optimal survey based on value and persona preferences.
        Prioritizes: hourly rate > total value > shortest time
        """
        if not surveys:
            return None
        
        # Filter based on preferences
        suitable_surveys = []
        
        for survey in surveys:
            # Apply minimum thresholds
            if survey.points < self.preferences["min_points"]:
                continue
            if survey.time_minutes > self.preferences["max_time_minutes"]:
                continue
            if survey.hourly_rate < self.preferences["min_hourly_rate"]:
                continue
            
            suitable_surveys.append(survey)
        
        if not suitable_surveys:
            # If no surveys meet criteria, take best available
            self.logger.warning("No surveys meet preferences, selecting best available")
            suitable_surveys = surveys
        
        # Sort by multiple criteria
        sorted_surveys = sorted(
            suitable_surveys,
            key=lambda s: (
                s.metadata.get("has_bonus", False),  # Bonus surveys first
                s.hourly_rate,                        # Then hourly rate
                s.dollar_value,                       # Then total value
                -s.time_minutes                       # Shorter is better
            ),
            reverse=True
        )
        
        best_survey = sorted_surveys[0]
        
        self.logger.info(
            f"Selected survey: '{best_survey.title[:40]}...' | "
            f"{best_survey.points} points | "
            f"{best_survey.time_minutes} mins | "
            f"${best_survey.hourly_rate:.2f}/hr"
        )
        
        return best_survey
    
    async def start_survey(self, survey: Survey) -> bool:
        """Click start button for selected survey"""
        try:
            # Find start button within survey element
            start_button = await survey.element.query_selector(
                self.selectors["start_button"]
            )
            
            if not start_button:
                self.logger.error("Start button not found")
                return False
            
            # Human-like hover before click
            await start_button.hover()
            await self.wait_human_like(500, 1000)
            
            # Click to start survey
            await start_button.click()
            
            # Wait for navigation
            await self.page.wait_for_load_state("networkidle")
            await self.wait_human_like(2000, 3000)
            
            # Verify we're in a survey
            current_url = self.page.url
            if "survey" in current_url or "q/" in current_url:
                self.logger.info("Successfully started survey")
                return True
            else:
                self.logger.warning(f"Unexpected URL after start: {current_url}")
                return False
            
        except Exception as e:
            self.logger.error(f"Failed to start survey: {e}")
            return False
    
    async def is_survey_complete(self) -> bool:
        """Check if current survey is finished"""
        try:
            # Check for completion indicators
            completion_selectors = [
                self.selectors["survey_complete"],
                "text=Thank you",
                "text=Survey complete",
                "text=You have earned"
            ]
            
            for selector in completion_selectors:
                try:
                    element = await self.page.wait_for_selector(
                        selector,
                        timeout=1000
                    )
                    if element:
                        self.logger.info("Survey completion detected")
                        return True
                except:
                    continue
            
            # Check for screen-out
            try:
                screen_out = await self.page.wait_for_selector(
                    self.selectors["screen_out"],
                    timeout=1000
                )
                if screen_out:
                    self.logger.warning("Survey screen-out detected")
                    await self.handle_screen_out()
                    return True
            except:
                pass
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking survey completion: {e}")
            return False
    
    def convert_points_to_currency(self, points: int) -> float:
        """Convert MyOpinions points to AUD"""
        return points / self.points_per_dollar
    
    async def track_bonus_progress(self) -> Dict:
        """Monitor bonus tier and weekly earnings progress"""
        try:
            bonus_info = {
                "current_tier": "unknown",
                "bonus_rate": 0.0,
                "weekly_points": 0,
                "next_tier_progress": 0.0
            }
            
            # Get current tier
            tier_element = await self.page.query_selector(self.selectors["tier_badge"])
            if tier_element:
                tier_text = await tier_element.inner_text()
                tier_name = tier_text.lower().strip()
                
                if tier_name in self.bonus_tiers:
                    bonus_info["current_tier"] = tier_name
                    bonus_info["bonus_rate"] = self.bonus_tiers[tier_name]["rate"]
            
            # Get weekly bonus progress
            weekly_element = await self.page.query_selector(self.selectors["weekly_bonus"])
            if weekly_element:
                weekly_text = await weekly_element.inner_text()
                points_match = re.search(r'(\d+)', weekly_text)
                if points_match:
                    bonus_info["weekly_points"] = int(points_match.group(1))
            
            # Get tier progress
            progress_element = await self.page.query_selector(self.selectors["tier_progress"])
            if progress_element:
                progress_text = await progress_element.get_attribute("style")
                width_match = re.search(r'width:\s*(\d+)%', progress_text)
                if width_match:
                    bonus_info["next_tier_progress"] = float(width_match.group(1))
            
            self.logger.info(f"Bonus tracking: {bonus_info}")
            return bonus_info
            
        except Exception as e:
            self.logger.error(f"Failed to track bonus: {e}")
            return {}
    
    async def complete_daily_bonus(self) -> bool:
        """Check and complete daily bonus if available"""
        try:
            # Look for daily bonus indicator
            daily_bonus = await self.page.query_selector("button.daily-bonus")
            
            if daily_bonus:
                await daily_bonus.click()
                await self.wait_human_like(1000, 2000)
                self.logger.info("Daily bonus collected!")
                return True
                
            return False
            
        except Exception as e:
            self.logger.warning(f"Daily bonus check failed: {e}")
            return False