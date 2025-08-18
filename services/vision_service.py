#!/usr/bin/env python3
"""
👁️ Vision Service v2.0
Wraps vision_mvp.py with clean service interface.
"""
from typing import Dict, Any, Optional
import os
import time
from vision_mvp import QuenitoVision

class VisionService:
    """Clean service wrapper for vision capabilities"""
    
    def __init__(self, platform: str = "myopinions", enabled: bool = True):
        self.enabled = enabled
        self.platform = platform
        
        if self.enabled:
            self.vision = QuenitoVision(platform=platform)
            # Migrate any old patterns
            self.vision.migrate_existing_patterns()
        else:
            self.vision = None
    
    async def analyze_page(self, page, question_num: int) -> Optional[Dict[str, Any]]:
        """Analyze current page with vision"""
        if not self.enabled:
            return None
        
        try:
            # Take screenshot
            screenshot_path = f"vision_data/question_{question_num}_{int(time.time())}.png"
            os.makedirs("vision_data", exist_ok=True)
            await page.screenshot(path=screenshot_path)
            
            # Analyze with vision
            print("👁️ Analyzing with vision...")
            result = await self.vision.analyze_screenshot(screenshot_path)
            
            return result
        except Exception as e:
            print(f"⚠️ Vision error: {e}")
            return None
    
    async def store_success_pattern(self, page, question_num: int, 
                                   vision_result: Dict, automation_result: Dict):
        """Store successful automation pattern"""
        if not self.enabled:
            return
        
        screenshot_path = f"vision_data/question_{question_num}_{int(time.time())}.png"
        await self.vision.store_pattern(
            screenshot_path,
            vision_result,
            {
                'success': True,
                'automation_type': 'single_question',
                **automation_result
            }
        )
    
    async def store_learning_pattern(self, page, question_num: int,
                                    vision_result: Dict, learning_data: Dict):
        """Store pattern from manual learning"""
        if not self.enabled:
            return
        
        screenshot_path = f"vision_data/question_{question_num}_{int(time.time())}.png"
        await self.vision.store_pattern(
            screenshot_path,
            vision_result,
            {
                'success': True,
                'capture_type': 'manual_learning',
                **learning_data
            }
        )