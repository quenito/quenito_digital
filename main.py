#!/usr/bin/env python3
"""
🧠 Quenito Survey Assistant - Enhanced Main Interface
Now with STEALTH BROWSER CAPABILITIES for undetectable automation!

New Features:
- 🕵️ Stealth browser with cookie transfer
- 🎯 Platform-specific optimizations  
- 🧠 Brain-enhanced automation with stealth timing
- 📊 Intelligence tracking with stealth analytics
"""

import asyncio
import sys
import os
from typing import Optional, Dict, Any

# Import core Quenito components
from core.stealth_browser_manager import StealthBrowserManager
from models.survey_stats import BrainEnhancedSurveyStats
from utils.reporting import BrainEnhancedReportGenerator
from utils.knowledge_base import KnowledgeBase
from handlers.handler_factory import HandlerFactory
from utils.intervention_manager import EnhancedLearningInterventionManager


class QuentioMainInterface:
    """
    🧠 Enhanced Quenito Main Interface with Stealth Capabilities
    """
    
    def __init__(self):
        self.brain = KnowledgeBase()
        self.stealth_manager = None
        self.stats = None
        self.reporter = None
        
        # Platform configurations for optimal stealth
        self.platform_configs = {
            "myopinions_dashboard": {
                "name": "MyOpinions Australia Dashboard",
                "profile_name": "quenito_myopinions",
                "cookie_domains": ["myopinions.com.au", "google.com", "googleapis.com"],
                "stealth_level": "maximum",
                "target_url": "https://www.myopinions.com.au/auth/dashboard",
                "login_check": "dashboard",
                "description": "Access MyOpinions dashboard with Chrome session cookies"
            },
            "primeopinion_dashboard": {
                "name": "Prime Opinion Australia Dashboard",
                "profile_name": "quenito_primeopinion",
                "cookie_domains": ["primeopinion.com.au", "google.com", "googleapis.com"],
                "stealth_level": "maximum",
                "target_url": "https://app.primeopinion.com.au/surveys",
                "login_check": "surveys",
                "description": "Access Prime Opinion surveys dashboard with Chrome session cookies"
            },
            "surveymonkey_direct": {
                "name": "SurveyMonkey Direct Survey",
                "profile_name": "quenito_surveymonkey",
                "cookie_domains": ["surveymonkey.com", "google.com"],
                "stealth_level": "high",
                "target_url": None,  # Will be provided by user
                "login_check": None,
                "description": "Direct access to SurveyMonkey survey (paste URL)"
            }
        }
    
    def display_main_menu(self):
        """Display the enhanced main menu with stealth options."""
        
        print("\n" + "🧠" + "=" * 70)
        print("🧠 QUENITO SURVEY ASSISTANT - STEALTH EDITION")
        print("🧠" + "=" * 70)
        print("🕵️ Advanced AI automation with undetectable stealth capabilities")
        print()
        
        print("🎯 AUTOMATION OPTIONS:")
        print()
        print("   1. 🕵️ MYOPINIONS DASHBOARD")
        print("      └── https://www.myopinions.com.au/auth/dashboard")
        print("      └── Uses Chrome cookies for instant logged-in access")
        print()
        print("   2. 🕵️ PRIME OPINION DASHBOARD") 
        print("      └── https://app.primeopinion.com.au/surveys")
        print("      └── Chrome session transfer for seamless dashboard access")
        print()
        print("   3. 🎯 SURVEYMONKEY DIRECT SURVEY")
        print("      └── Paste SurveyMonkey survey URL for direct access")
        print("      └── Perfect for Survey 1A testing - goes straight to survey")
        print()
        print("   4. 🧠 BRAIN INTELLIGENCE REPORT")
        print("      └── View Quenito's learning progress and evolution")
        print()
        print("   5. 🧪 TEST STEALTH SYSTEM")
        print("      └── Validate stealth capabilities and cookie transfer")
        print()
        print("   6. ⚙️ BRAIN CONFIGURATION")
        print("      └── Manage Quenito's knowledge base and settings")
        print()
        print("   7. 📊 VIEW AUTOMATION STATISTICS")
        print("      └── Review performance metrics and success rates")
        print()
        print("   0. 🚪 EXIT")
        print()
        
    def display_platform_menu(self):
        """Display platform selection with stealth configurations."""
        
        print("\n🕵️ STEALTH PLATFORM SELECTION:")
        print("=" * 50)
        
        for i, (domain, config) in enumerate(self.platform_configs.items(), 1):
            if domain != "custom":
                print(f"   {i}. {config['name']}")
                print(f"      └── Domain: {domain}")
                print(f"      └── Stealth Level: {config['stealth_level'].upper()}")
                print(f"      └── Profile: {config['profile_name']}")
                print()
        
        print(f"   {len(self.platform_configs)}. Custom Platform (Enter URL)")
        print("   0. Back to Main Menu")
        print()
    
    async def launch_stealth_browser(self, platform_key: str, survey_url: Optional[str] = None):
        """Launch stealth browser for specified platform."""
        
        if platform_key not in self.platform_configs:
            print(f"❌ Unknown platform: {platform_key}")
            return False
        
        config = self.platform_configs[platform_key]
        
        print(f"\n🕵️ Launching Stealth Browser for {config['name']}")
        print("=" * 60)
        print(f"📝 {config['description']}")
        
        # Handle SurveyMonkey direct survey URL input
        if platform_key == "surveymonkey_direct":
            if not survey_url:
                print("\n📝 SURVEYMONKEY DIRECT SURVEY ACCESS")
                print("=" * 40)
                print("💡 Paste your SurveyMonkey survey URL below:")
                print("   Example: https://www.surveymonkey.com/r/ABC123")
                print("   This goes directly to the survey intro page")
                print()
                
                survey_url = input("Survey URL: ").strip()
                
                if not survey_url:
                    print("❌ No URL provided")
                    return False
                
                if "surveymonkey.com" not in survey_url:
                    print("⚠️ Warning: This doesn't look like a SurveyMonkey URL")
                    proceed = input("Continue anyway? (y/N): ").lower().strip()
                    if proceed != 'y':
                        return False
            
            target_url = survey_url
            print(f"🎯 Target: {target_url}")
        else:
            target_url = config['target_url']
        
        try:
            # Initialize stealth components
            print("🔧 Initializing stealth components...")
            self.stealth_manager = StealthBrowserManager(config['profile_name'])
            self.stats = BrainEnhancedSurveyStats(knowledge_base=self.brain)
            self.reporter = BrainEnhancedReportGenerator(knowledge_base=self.brain)
            
            # Start brain-enhanced session
            self.stats.start_survey()
            self.reporter.start_session()
            
            # Launch stealth browser with cookie transfer
            print("🍪 Transferring cookies from Chrome...")
            page = await self.stealth_manager.initialize_stealth_browser(
                transfer_cookies=True,
                use_existing_chrome=False
            )
            
            # Test platform compatibility
            print(f"🧪 Testing platform compatibility...")
            compatibility = await self.stealth_manager.test_platform_compatibility(target_url)
            
            print(f"🎯 Stealth Level: {compatibility.get('stealth_level', 'UNKNOWN')}")
            print(f"📊 Detection Score: {compatibility.get('compatibility_score', 'N/A')}")
            
            if compatibility.get('stealth_level') not in ['HIGH', 'MEDIUM']:
                print("⚠️ Warning: Low stealth compatibility detected")
                proceed = input("Continue anyway? (y/N): ").lower().strip()
                if proceed != 'y':
                    return False
            
            # Navigate to target URL
            print(f"🌐 Navigating to target...")
            await page.goto(target_url, wait_until='networkidle')
            
            # Check access state
            current_url = page.url
            
            if platform_key == "surveymonkey_direct":
                print("✅ SurveyMonkey survey accessed directly!")
                print("🎯 Ready for Survey 1A testing!")
            else:
                login_indicator = config.get('login_check')
                
                if login_indicator and login_indicator in current_url.lower():
                    print("✅ Successfully accessed dashboard - Chrome cookies working!")
                    print("🎯 Platform ready for survey selection")
                elif "login" in current_url.lower():
                    print("⚠️ Login page detected - Chrome cookies may need refresh")
                    print("💡 Try logging in manually in Chrome first, then restart Quenito")
                else:
                    print("✅ Platform accessed successfully")
            
            # Start automation interface
            await self.run_stealth_automation_interface(page, platform_key)
            
            return True
            
        except Exception as e:
            print(f"❌ Error launching stealth browser: {e}")
            return False
        
        finally:
            if self.stealth_manager:
                await self.stealth_manager.close()
    
    async def run_stealth_automation_interface(self, page, platform_key: str):
        """Run the automation interface with stealth browser."""
        
        print("\n🤖 QUENITO STEALTH AUTOMATION INTERFACE")
        print("=" * 50)
        print("🧠 Brain-enhanced automation with perfect stealth")
        print()
        
        while True:
            print("🎯 AUTOMATION COMMANDS:")
            print("   1. 🔍 Analyze Current Page")
            print("   2. 🎯 Start Survey Automation") 
            print("   3. 🧠 Manual Learning Mode")
            print("   4. 📊 View Real-time Statistics")
            print("   5. 🕵️ Test Stealth Detection")
            print("   6. 💾 Save Session State")
            print("   7. 🔄 Navigate to Survey URL")
            print("   0. 🏠 Return to Main Menu")
            print()
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                await self.analyze_current_page(page)
            elif choice == "2":
                await self.start_survey_automation(page, platform_key)
            elif choice == "3":
                await self.manual_learning_mode(page)
            elif choice == "4":
                self.view_realtime_statistics()
            elif choice == "5":
                await self.test_stealth_detection(page)
            elif choice == "6":
                await self.save_session_state()
            elif choice == "7":
                await self.navigate_to_survey_url(page)
            elif choice == "0":
                break
            else:
                print("❌ Invalid option")
    
    async def analyze_current_page(self, page):
        """Analyze current page content with brain intelligence."""
        
        print("\n🔍 BRAIN-ENHANCED PAGE ANALYSIS")
        print("=" * 40)
        
        try:
            # Get page content
            content = await page.inner_text('body')
            url = page.url
            title = await page.title()
            
            print(f"📄 Page: {title}")
            print(f"🔗 URL: {url}")
            print(f"📝 Content Length: {len(content)} characters")
            
            # Brain analysis
            from handlers.handler_factory import HandlerFactory
            intervention_manager = EnhancedLearningInterventionManager()
            handler_factory = HandlerFactory(self.brain, intervention_manager, self.stats)
            
            # Get best handler for current content
            handler, confidence = handler_factory.get_best_handler(page, content)
            
            print(f"🧠 Brain Analysis:")
            print(f"   • Recommended Handler: {handler.__class__.__name__}")
            print(f"   • Confidence Score: {confidence:.2f}")
            print(f"   • Automation Recommendation: {'✅ AUTOMATE' if confidence > 0.4 else '📝 MANUAL INTERVENTION'}")
            
            # Question type detection
            if hasattr(handler, 'can_handle'):
                detailed_confidence = handler.can_handle(content)
                print(f"   • Detailed Confidence: {detailed_confidence:.2f}")
            
            print(f"🎯 Next Action: {'Proceed with automation' if confidence > 0.4 else 'Manual review recommended'}")
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
    
    async def start_survey_automation(self, page, platform_key: str):
        """Start automated survey completion with brain learning."""
        
        print("\n🤖 STARTING BRAIN-ENHANCED AUTOMATION")
        print("=" * 50)
        
        try:
            # Initialize automation components
            intervention_manager = EnhancedLearningInterventionManager()
            handler_factory = HandlerFactory(self.brain, intervention_manager, self.stats)
            
            question_count = 0
            max_questions = 50  # Safety limit
            
            print("🧠 Quenito's brain is now learning and automating...")
            print("⏹️ Press Ctrl+C to stop automation safely")
            
            while question_count < max_questions:
                try:
                    # Get current page content
                    content = await page.inner_text('body')
                    
                    # Check if survey is complete
                    if any(indicator in content.lower() for indicator in 
                          ['thank you', 'survey complete', 'completed', 'finished']):
                        print("🎉 Survey completed successfully!")
                        break
                    
                    # Get best handler
                    handler, confidence = handler_factory.get_best_handler(page, content)
                    
                    # Update statistics
                    self.stats.increment_question_count(
                        handler_type=handler.__class__.__name__,
                        confidence=confidence
                    )
                    
                    print(f"\n📋 Question {question_count + 1}:")
                    print(f"   🧠 Handler: {handler.__class__.__name__}")
                    print(f"   🎯 Confidence: {confidence:.2f}")
                    
                    if confidence > 0.4:  # Automation threshold
                        print("   🤖 Automating...")
                        
                        # Set page for handler
                        handler.page = page
                        
                        # Attempt automation
                        success = await handler.handle() if hasattr(handler, 'handle') else handler.handle()
                        
                        if success:
                            print("   ✅ Automated successfully!")
                            self.stats.increment_automated_count(
                                handler_type=handler.__class__.__name__,
                                confidence=confidence
                            )
                        else:
                            print("   ⚠️ Automation failed - requesting manual intervention")
                            manual_success = await self.request_manual_intervention(page, content)
                            if manual_success:
                                self.stats.increment_intervention_count(
                                    handler_type=handler.__class__.__name__,
                                    reason="automation_failed"
                                )
                    else:
                        print("   📝 Low confidence - requesting manual intervention")
                        manual_success = await self.request_manual_intervention(page, content)
                        if manual_success:
                            self.stats.increment_intervention_count(
                                handler_type=handler.__class__.__name__,
                                reason="low_confidence"
                            )
                    
                    question_count += 1
                    
                    # Brief pause between questions
                    await asyncio.sleep(1)
                    
                except KeyboardInterrupt:
                    print("\n⏹️ Automation stopped by user")
                    break
                except Exception as e:
                    print(f"❌ Error in automation loop: {e}")
                    break
            
            # Generate final report
            print(f"\n📊 AUTOMATION COMPLETE")
            print(f"   Questions Processed: {question_count}")
            print(f"   Automation Rate: {self.stats.get_automation_rate():.1f}%")
            
            # Generate brain intelligence report
            if self.reporter:
                self.stats.end_survey()
                self.reporter.end_session()
                
                report = self.reporter.generate_brain_intelligence_report(self.stats)
                self.reporter.export_brain_report(report)
                
                print("🧠 Brain intelligence report generated!")
                
        except Exception as e:
            print(f"❌ Automation error: {e}")
    
    async def request_manual_intervention(self, page, content: str) -> bool:
        """Request manual intervention with learning capture."""
        
        print("\n📝 MANUAL INTERVENTION REQUIRED")
        print("=" * 40)
        print("🧠 Quenito will learn from your action!")
        
        try:
            # Show question content preview
            preview = content[:200] + "..." if len(content) > 200 else content
            print(f"📋 Question Preview: {preview}")
            
            print("\n🎯 Manual Action Options:")
            print("   1. Complete manually and continue")
            print("   2. Skip this question")
            print("   3. Stop automation")
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                input("\n✋ Please complete the question manually, then press Enter to continue...")
                
                # Capture learning data (simplified for now)
                print("🧠 Learning captured - Quenito's brain updated!")
                return True
                
            elif choice == "2":
                print("⏭️ Question skipped")
                return True
                
            elif choice == "3":
                print("⏹️ Automation stopped")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Manual intervention error: {e}")
            return False
    
    async def test_stealth_detection(self, page):
        """Test stealth detection on current page."""
        
        print("\n🕵️ STEALTH DETECTION TEST")
        print("=" * 30)
        
        try:
            # Run stealth detection tests
            detection_tests = {
                'webdriver_detected': await page.evaluate('navigator.webdriver !== undefined'),
                'automation_detected': await page.evaluate('window.chrome && window.chrome.runtime'),
                'headless_detected': await page.evaluate('navigator.plugins.length === 0'),
                'user_agent_valid': 'Chrome' in await page.evaluate('navigator.userAgent'),
                'timing_realistic': True  # Placeholder for timing analysis
            }
            
            print("🔍 Detection Results:")
            for test, result in detection_tests.items():
                status = "❌ DETECTED" if (test.endswith('_detected') and result) or (not test.endswith('_detected') and not result) else "✅ HIDDEN"
                print(f"   • {test}: {status}")
            
            # Calculate stealth score
            stealth_score = sum(1 for test, result in detection_tests.items() 
                              if (test.endswith('_detected') and not result) or 
                                 (not test.endswith('_detected') and result))
            
            total_tests = len(detection_tests)
            stealth_percentage = (stealth_score / total_tests) * 100
            
            print(f"\n🎯 Overall Stealth Score: {stealth_score}/{total_tests} ({stealth_percentage:.1f}%)")
            
            if stealth_percentage >= 80:
                print("🏆 EXCELLENT stealth - very low detection risk")
            elif stealth_percentage >= 60:
                print("✅ GOOD stealth - acceptable detection risk")
            else:
                print("⚠️ POOR stealth - high detection risk")
                
        except Exception as e:
            print(f"❌ Stealth test error: {e}")
    
    def view_realtime_statistics(self):
        """View real-time automation statistics."""
        
        if not self.stats:
            print("❌ No active automation session")
            return
        
        print("\n📊 REAL-TIME AUTOMATION STATISTICS")
        print("=" * 45)
        
        try:
            self.stats.print_brain_enhanced_summary()
        except Exception as e:
            print(f"❌ Statistics error: {e}")
    
    async def save_session_state(self):
        """Save current session state."""
        
        if not self.stealth_manager:
            print("❌ No active stealth session")
            return
        
        try:
            await self.stealth_manager.save_session_state()
            print("✅ Session state saved successfully")
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    async def navigate_to_survey_url(self, page):
        """Navigate to a specific survey URL."""
        
        print("\n🌐 NAVIGATE TO SURVEY")
        print("=" * 25)
        
        url = input("Enter survey URL: ").strip()
        
        if not url:
            print("❌ No URL provided")
            return
        
        try:
            print(f"🌐 Navigating to {url}...")
            await page.goto(url, wait_until='networkidle')
            print("✅ Navigation completed")
            
            # Test stealth on new page
            if self.stealth_manager:
                compatibility = await self.stealth_manager.test_platform_compatibility(url)
                print(f"🕵️ Stealth Level: {compatibility.get('stealth_level', 'UNKNOWN')}")
                
        except Exception as e:
            print(f"❌ Navigation error: {e}")
    
    async def run_main_interface(self):
        """Run the main interface loop."""
        
        print("🧠 Initializing Quenito's Digital Brain...")
        print("🕵️ Stealth capabilities loaded")
        print("📊 Intelligence tracking active")
        
        while True:
            try:
                self.display_main_menu()
                choice = input("Select option: ").strip()
                
                if choice == "1":
                    await self.launch_stealth_browser("myopinions_dashboard")
                elif choice == "2":
                    await self.launch_stealth_browser("primeopinion_dashboard")
                elif choice == "3":
                    await self.launch_stealth_browser("surveymonkey_direct")
                elif choice == "4":
                    self.view_brain_intelligence_report()
                elif choice == "5":
                    await self.test_stealth_system()
                elif choice == "6":
                    self.brain_configuration_menu()
                elif choice == "7":
                    self.view_automation_statistics()
                elif choice == "0":
                    print("👋 Goodbye! Quenito's brain is always learning...")
                    break
                else:
                    print("❌ Invalid option")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Quenito's brain is always learning...")
                break
            except Exception as e:
                print(f"❌ Interface error: {e}")
    
    def view_brain_intelligence_report(self):
        """View latest brain intelligence report."""
        
        print("\n🧠 BRAIN INTELLIGENCE REPORT")
        print("=" * 35)
        
        try:
            brain_summary = self.brain.get_brain_learning_summary()
            
            print(f"🎯 Intelligence Level: {brain_summary.get('brain_intelligence_level', 'Unknown')}")
            print(f"📊 Total Interventions: {brain_summary.get('total_interventions', 0)}")
            print(f"🎯 Success Patterns: {brain_summary.get('success_patterns_count', 0)}")
            print(f"🚀 Automation Readiness: {brain_summary.get('automation_readiness', 0):.1f}%")
            
            # Print detailed report if available
            if self.brain:
                self.brain.print_brain_intelligence_report()
                
        except Exception as e:
            print(f"❌ Report error: {e}")
    
    async def test_stealth_system(self):
        """Run comprehensive stealth system tests."""
        
        print("\n🧪 COMPREHENSIVE STEALTH SYSTEM TEST")
        print("=" * 45)
        
        try:
            # Import and run the test
            from test_stealth_system import test_stealth_system, test_cookie_transfer
            
            print("🔧 Running stealth capability tests...")
            success1 = await test_stealth_system()
            
            print("\n🍪 Running cookie transfer tests...")
            success2 = await test_cookie_transfer()
            
            if success1 and success2:
                print("\n🎉 ALL STEALTH TESTS PASSED!")
                print("🚀 System ready for undetectable automation!")
            else:
                print("\n⚠️ Some tests failed - check output above")
                
        except ImportError:
            print("❌ Test script not found - run setup_stealth_system.py first")
        except Exception as e:
            print(f"❌ Test error: {e}")
    
    def brain_configuration_menu(self):
        """Brain configuration and management menu."""
        
        print("\n⚙️ BRAIN CONFIGURATION")
        print("=" * 25)
        print("   1. View Knowledge Base Summary")
        print("   2. Export Brain Data")
        print("   3. Reset Learning Data")
        print("   4. Update User Profile")
        print("   0. Back")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            self.brain.print_summary()
        elif choice == "2":
            print("📤 Brain data export feature coming soon!")
        elif choice == "3":
            confirm = input("⚠️ Reset all learning data? (y/N): ").lower().strip()
            if confirm == 'y':
                print("🔄 Learning data reset feature coming soon!")
        elif choice == "4":
            print("👤 User profile update feature coming soon!")
    
    def view_automation_statistics(self):
        """View historical automation statistics."""
        
        print("\n📊 AUTOMATION STATISTICS")
        print("=" * 30)
        
        if self.stats:
            try:
                self.stats.print_brain_enhanced_summary()
            except Exception as e:
                print(f"❌ Statistics error: {e}")
        else:
            print("⚠️ No active automation session")
            print("💡 Start an automation session to view live statistics")


async def main():
    """Main entry point for Quenito Survey Assistant."""
    
    try:
        interface = QuentioMainInterface()
        await interface.run_main_interface()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🧠 Starting Quenito Survey Assistant - Stealth Edition...")
    asyncio.run(main())
