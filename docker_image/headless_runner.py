#!/usr/bin/env python3
"""
Headless Quenito Runner for Docker/VPS
Runs surveys automatically with remote monitoring
"""

import asyncio
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/quenito_headless.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('QuenitoHeadless')

async def wait_for_survey_availability():
    """Check MyOpinions periodically for available surveys"""
    from core.stealth_browser_manager import StealthBrowserManager
    from platform_adapters.adapters.myopinions_adapter import MyOpinionsAdapter
    
    logger.info("🔍 Checking for available surveys...")
    
    browser = StealthBrowserManager("quenito_myopinions")
    await browser.initialize_stealth_browser(transfer_cookies=False)
    await browser.load_saved_cookies()
    
    # Navigate to dashboard
    await browser.page.goto("https://www.myopinions.com.au/auth/dashboard")
    await asyncio.sleep(5)
    
    # Check if logged in
    try:
        # Look for login elements
        if await browser.page.locator('input[type="email"], input[type="password"]').count() > 0:
            logger.warning("⚠️ Not logged in - needs manual login first")
            await browser.close()
            return None
    except:
        pass
    
    # Check for surveys
    adapter = MyOpinionsAdapter(browser)
    surveys = await adapter.detect_available_surveys()
    
    await browser.close()
    
    if surveys:
        logger.info(f"✅ Found {len(surveys)} surveys!")
        return surveys
    else:
        logger.info("❌ No surveys available right now")
        return None

async def run_survey_session():
    """Run a complete survey session"""
    logger.info("🚀 Starting survey session...")
    
    # Import and run the main automation
    from quenito_learning_with_automation import run_integrated_learning
    
    try:
        await run_integrated_learning()
        logger.info("✅ Survey session completed successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Survey session failed: {str(e)}")
        return False

async def interactive_session():
    """Run interactive survey session with manual intervention support"""
    
    logger.info("=" * 60)
    logger.info("🎮 QUENITO INTERACTIVE SESSION (VPS MODE)")
    logger.info(f"📍 Running on VPS with Sydney IP")
    logger.info("⚠️ This session REQUIRES your interaction via VNC!")
    logger.info("=" * 60)
    
    # Import the main automation with manual flow
    from quenito_learning_with_automation import run_integrated_learning
    
    logger.info("\n📋 INSTRUCTIONS:")
    logger.info("1. Connect to VNC: http://YOUR_VPS_IP:6080")
    logger.info("2. You'll see the browser window")
    logger.info("3. Handle manual interventions when needed")
    logger.info("4. Quenito will automate what it can (~70%)")
    logger.info("\n🚀 Starting in 10 seconds...")
    
    await asyncio.sleep(10)
    
    try:
        # Run the standard learning flow that expects manual input
        await run_integrated_learning()
        logger.info("✅ Survey session completed!")
        return True
    except Exception as e:
        logger.error(f"❌ Session error: {str(e)}")
        return False

async def scheduled_check():
    """Just check for surveys and notify - don't run automatically"""
    
    logger.info("=" * 60)
    logger.info("🔍 QUENITO SURVEY CHECKER")
    logger.info("=" * 60)
    
    while True:
        try:
            logger.info("🔍 Checking for available surveys...")
            surveys = await wait_for_survey_availability()
            
            if surveys:
                logger.info("🎉 SURVEYS AVAILABLE!")
                for idx, survey in enumerate(surveys):
                    logger.info(f"  Survey {idx+1}: {survey.get('time', 'Unknown time')}")
                
                logger.info("\n💡 TO RUN SURVEYS:")
                logger.info("1. Connect via VNC: http://YOUR_VPS_IP:6080")
                logger.info("2. Run: docker exec -it quenito-automation python quenito_learning_with_automation.py")
                logger.info("3. Handle manual questions when prompted")
                
                # Send notification (could add email/telegram here later)
                with open('/app/logs/survey_available.flag', 'w') as f:
                    f.write(f"{len(surveys)} surveys available at {datetime.now()}")
            else:
                logger.info("❌ No surveys available")
            
            # Check every 30 minutes
            logger.info("⏰ Next check in 30 minutes...")
            await asyncio.sleep(1800)
            
        except KeyboardInterrupt:
            logger.info("🛑 Checker stopped")
            break
        except Exception as e:
            logger.error(f"❌ Check error: {str(e)}")
            await asyncio.sleep(600)

async def main():
    """Main entry point with options"""
    
    import argparse
    parser = argparse.ArgumentParser(description='Quenito VPS Runner')
    parser.add_argument('--mode', choices=['interactive', 'check', 'login'], 
                       default='interactive',
                       help='Run mode: interactive survey session, check for surveys, or setup login')
    
    args = parser.parse_args()
    
    if args.mode == 'login':
        logger.info("🔐 Login setup mode...")
        logger.info("1. Open VNC: http://YOUR_VPS_IP:6080")
        logger.info("2. Browser will open to MyOpinions")
        logger.info("3. Login manually")
        logger.info("4. Cookies will be saved automatically")
        
        from core.stealth_browser_manager import StealthBrowserManager
        
        browser = StealthBrowserManager("quenito_myopinions")
        await browser.initialize_stealth_browser(headless=False)
        await browser.page.goto("https://www.myopinions.com.au/login")
        
        logger.info("⏰ Waiting for login (2 minutes timeout)...")
        await asyncio.sleep(120)
        
        # Save cookies
        await browser.save_cookies()
        await browser.close()
        logger.info("✅ Login saved!")
    
    elif args.mode == 'check':
        # Run survey checker (notifies when available)
        await scheduled_check()
    
    else:  # interactive
        # Run interactive session (requires VNC interaction)
        await interactive_session()

if __name__ == "__main__":
    from datetime import timedelta
    asyncio.run(main())
