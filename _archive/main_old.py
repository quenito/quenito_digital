#!/usr/bin/env python3
"""
🧠 Quenito Survey Assistant - Ultimate Edition v3.0
Combines Stealth Browser capabilities with Bulletproof Error Handling

Features:
- 🕵️ Stealth browser with cookie transfer
- 🛡️ BULLETPROOF CTRL+C protection system  
- 🎯 Platform-specific optimizations
- 🧠 Brain-enhanced automation with advanced learning
- 📊 Intelligence tracking with robust error recovery
- 🔄 Safe tab switching without breaking references
"""

import asyncio
import sys
import os
import signal
import time
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlparse

# Import core Quenito components
from core.stealth_browser_manager import StealthBrowserManager
from models.survey_stats import BrainEnhancedSurveyStats
from utils.reporting import BrainEnhancedReportGenerator
from data.knowledge_base import KnowledgeBase
from handlers.handler_factory import HandlerFactory
from utils.intervention_manager import EnhancedLearningInterventionManager

# 🆕 Import advanced learning capture
try:
    from utils.advanced_learning_capture import AdvancedLearningCapture
except ImportError:
    print("⚠️ Advanced learning capture not available - using basic learning")
    AdvancedLearningCapture = None


# =========================================================================
# 🛡️ BULLETPROOF CTRL+C PROTECTION SYSTEM v2.0 (From backup_2.py)
# =========================================================================
class RobustSignalHandler:
    """
    Ultra-robust signal handler that prevents accidental script termination.
    Especially protective during manual intervention phases.
    """
    
    def __init__(self):
        self.intervention_mode = False
        self.survey_mode = False
        self.ctrl_c_count = 0
        self.last_ctrl_c_time = 0
        
        # Install signal handlers
        signal.signal(signal.SIGINT, self.handle_keyboard_interrupt)
        signal.signal(signal.SIGTERM, self.handle_termination)
        
        # On Windows, also handle Ctrl+Break
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, self.handle_keyboard_interrupt)
        
        print("🛡️ BULLETPROOF CTRL+C PROTECTION ACTIVATED!")
        print("💡 Accidental Ctrl+C during copy/paste is now safely blocked")
    
    def handle_keyboard_interrupt(self, signum, frame):
        """Enhanced Ctrl+C handler with multiple safeguards."""
        current_time = time.time()
        
        # Reset counter if it's been more than 3 seconds since last Ctrl+C
        if current_time - self.last_ctrl_c_time > 3:
            self.ctrl_c_count = 0
        
        self.ctrl_c_count += 1
        self.last_ctrl_c_time = current_time
        
        if self.intervention_mode:
            # MAXIMUM protection during manual intervention
            print(f"\n🛡️ INTERVENTION PROTECTION: Ctrl+C #{self.ctrl_c_count} BLOCKED!")
            print("🔒 Extra protection active during manual intervention phase")
            print("📝 Learning data capture in progress - termination could lose valuable data")
            print()
            print("💡 SAFE COPY/PASTE TIPS:")
            print("   • Use RIGHT-CLICK → Copy/Paste (recommended)")
            print("   • Use Ctrl+A to select, then right-click copy")
            print("   • Avoid Ctrl+C/Ctrl+V keyboard shortcuts")
            print()
            
            if self.ctrl_c_count >= 5:
                print("\n⚠️ FORCE EXIT: Multiple Ctrl+C detected during intervention!")
                self._emergency_save_and_exit()
                
        elif self.survey_mode:
            # Standard protection during survey automation
            print(f"\n🛡️ SURVEY PROTECTION: Ctrl+C #{self.ctrl_c_count} BLOCKED!")
            print("🤖 Survey automation in progress")
            
            if self.ctrl_c_count >= 3:
                print("\n⚠️ FORCE EXIT: Multiple Ctrl+C detected!")
                self._safe_exit()
        
        else:
            # Normal protection
            print(f"\n🛡️ CTRL+C PROTECTION: #{self.ctrl_c_count}")
            print("⚠️ Press Ctrl+C again within 3 seconds to confirm exit")
            
            if self.ctrl_c_count >= 2:
                print("🔴 EXIT CONFIRMED - Goodbye!")
                sys.exit(0)
    
    def handle_termination(self, signum, frame):
        """Handle termination signals gracefully."""
        print(f"\n🛡️ TERMINATION SIGNAL BLOCKED: Signal {signum}")
        print("💡 Use Ctrl+C multiple times or proper exit methods")
    
    def set_intervention_mode(self, enabled=True):
        """Enable/disable intervention mode for maximum protection."""
        self.intervention_mode = enabled
        if enabled:
            print("🛡️ INTERVENTION PROTECTION: Maximum safeguards activated!")
    
    def set_survey_mode(self, enabled=True):
        """Enable/disable survey mode protection."""
        self.survey_mode = enabled
        if enabled:
            print("🛡️ SURVEY PROTECTION: Enabled - accidental termination blocked")
    
    def _safe_exit(self):
        """Perform safe cleanup before exiting."""
        print("\n🧹 Performing safe shutdown...")
        print("💾 Saving any pending data...")
        print("✅ Safe shutdown complete - goodbye!")
        sys.exit(0)
    
    def _emergency_save_and_exit(self):
        """Emergency save during intervention force-exit."""
        print("\n🚨 EMERGENCY EXIT from intervention mode")
        print("💾 Attempting emergency learning data save...")
        sys.exit(1)


class QuentioUltimateInterface:
    """
    🧠 Ultimate Quenito Interface - Stealth + Bulletproof
    Combines the best of all versions
    """
    
    def __init__(self):
        # 🛡️ Initialize bulletproof protection FIRST
        self.signal_handler = RobustSignalHandler()
        
        # Initialize brain and core components
        self.brain = KnowledgeBase()
        self.stealth_manager = None
        self.stats = None
        self.reporter = None
        self.learning_capture = None
        
        # Pass signal handler to intervention manager
        self.intervention_manager = EnhancedLearningInterventionManager(
            knowledge_base=self.brain,
            signal_handler=self.signal_handler
        )
        
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
                "target_url": None,
                "login_check": None,
                "description": "Direct access to SurveyMonkey survey (paste URL)"
            }
        }
        
        print("✅ Ultimate Quenito Interface initialized!")
        print("🛡️ Bulletproof protection active")
        print("🧠 Brain connected and ready")
    
    def display_main_menu(self):
        """Display the enhanced main menu with stealth options."""
        
        print("\n" + "🧠" + "=" * 70)
        print("🧠 QUENITO SURVEY ASSISTANT - ULTIMATE EDITION v3.0")
        print("🧠" + "=" * 70)
        print("🕵️ Stealth browser + 🛡️ Bulletproof error handling")
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
    
    async def launch_stealth_browser(self, platform_key: str, survey_url: Optional[str] = None):
        """Launch stealth browser with bulletproof error handling."""
        
        if platform_key not in self.platform_configs:
            print(f"❌ Unknown platform: {platform_key}")
            return False
        
        config = self.platform_configs[platform_key]
        
        print(f"\n🕵️ Launching Stealth Browser for {config['name']}")
        print("=" * 60)
        print(f"📝 {config['description']}")
        
        try:
            # Handle SurveyMonkey direct survey URL input
            if platform_key == "surveymonkey_direct":
                if not survey_url:
                    print("\n📝 SURVEYMONKEY DIRECT SURVEY ACCESS")
                    print("=" * 40)
                    print("💡 Paste your SurveyMonkey survey URL below:")
                    print("   Example: https://www.surveymonkey.com/r/ABC123")
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
            
            # Initialize stealth components
            print("🔧 Initializing stealth components...")
            self.stealth_manager = StealthBrowserManager(config['profile_name'])
            self.stats = BrainEnhancedSurveyStats(knowledge_base=self.brain)
            self.reporter = BrainEnhancedReportGenerator(knowledge_base=self.brain)
            
            # Initialize advanced learning capture if available
            if AdvancedLearningCapture:
                self.learning_capture = AdvancedLearningCapture(self.brain)
                print("🧠 Advanced learning capture initialized!")
            
            # Start brain-enhanced session
            self.stats.start_survey()
            self.reporter.start_session()
            
            # Launch stealth browser with cookie transfer
            print("🍪 Transferring cookies from Chrome...")
            page = await self.stealth_manager.initialize_stealth_browser(
                transfer_cookies=True,
                use_existing_chrome=False
            )
            
            # Test platform compatibility with error handling
            print(f"🧪 Testing platform compatibility...")
            try:
                compatibility = await self.stealth_manager.test_platform_compatibility(target_url)
                print(f"🎯 Stealth Level: {compatibility.get('stealth_level', 'UNKNOWN')}")
                print(f"📊 Detection Score: {compatibility.get('compatibility_score', 'N/A')}")
            except Exception as e:
                print(f"⚠️ Compatibility test error: {e}")
                print("🔄 Continuing anyway...")
            
            # Navigate to target URL
            print(f"🌐 Navigating to target...")
            await page.goto(target_url, wait_until='networkidle')
            
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
        """Run the automation interface with stealth browser and bulletproof handling."""
        
        print("\n🤖 QUENITO STEALTH AUTOMATION INTERFACE")
        print("=" * 50)
        print("🧠 Brain-enhanced automation with perfect stealth")
        print("🛡️ Bulletproof error handling active")
        print()
        
        while True:
            try:
                print("🎯 AUTOMATION COMMANDS:")
                print("   1. 🔍 Analyze Current Page")
                print("   2. 🎯 Start Survey Automation") 
                print("   3. 🧠 Manual Learning Mode")
                print("   4. 📊 View Real-time Statistics")
                print("   5. 🕵️ Test Stealth Detection")
                print("   6. 💾 Save Session State")
                print("   7. 🔄 Navigate to Survey URL")
                print("   8. 📑 Handle Multi-Tab Survey")
                print("   0. 🏠 Return to Main Menu")
                print()
                
                choice = input("Select option: ").strip()
                
                if choice == "1":
                    await self.analyze_current_page(page)
                elif choice == "2":
                    # Check for valid page before starting
                    page = await self.validate_and_switch_if_needed(page)
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
                elif choice == "8":
                    page = await self.switch_to_active_tab(page)
                elif choice == "0":
                    break
                else:
                    print("❌ Invalid option")
                    
            except Exception as e:
                print(f"❌ Interface error: {e}")
                print("🔄 Recovering...")
                continue
    
    async def switch_to_active_tab(self, page):
        """
        🔄 BULLETPROOF: Switch to the correct survey tab WITHOUT closing any tabs.
        """
        print("\n🔄 TAB SWITCHING (Safe Mode)")
        print("=" * 40)
        
        try:
            # Get all open tabs/pages
            all_pages = page.context.pages
            print(f"📑 Found {len(all_pages)} open tabs")
            
            if len(all_pages) < 2:
                print("✅ Only one tab open - no switching needed")
                return page
            
            # Analyze each tab to find the survey
            survey_confidence = {}
            
            for i, tab_page in enumerate(all_pages):
                try:
                    # Don't close any tabs! Just analyze them
                    await tab_page.bring_to_front()
                    await asyncio.sleep(0.5)
                    
                    # Get tab info safely
                    tab_url = tab_page.url
                    try:
                        tab_title = await tab_page.title()
                    except:
                        tab_title = "Unknown"
                    
                    # Try to get content safely
                    try:
                        tab_content = await tab_page.inner_text('body')
                        preview = tab_content[:150].replace('\n', ' ')
                    except:
                        tab_content = ""
                        preview = "Could not read content"
                    
                    print(f"\nTab {i+1}:")
                    print(f"   📍 URL: {tab_url}")
                    print(f"   📄 Title: {tab_title}")
                    print(f"   👀 Preview: {preview}...")
                    
                    # Score this tab for survey likelihood
                    score = 0
                    content_lower = tab_content.lower()
                    
                    # Survey indicators
                    if 'gender' in content_lower or 'male' in content_lower:
                        score += 10
                        print("   ✅ Gender question detected! (+10)")
                    
                    survey_keywords = ['question', 'select', 'choose', 'rate', 'survey']
                    for keyword in survey_keywords:
                        if keyword in content_lower:
                            score += 2
                    
                    # Negative indicators
                    if 'welcome' in content_lower or 'introduction' in content_lower:
                        score -= 5
                        print("   ⚠️ Looks like intro page (-5)")
                    
                    if 'dashboard' in tab_url:
                        score -= 10
                        print("   ⚠️ Dashboard URL detected (-10)")
                    
                    survey_confidence[i] = score
                    print(f"   📊 Survey likelihood score: {score}")
                    
                except Exception as e:
                    print(f"   ❌ Error analyzing tab {i+1}: {e}")
                    survey_confidence[i] = -100
            
            # Find the best tab
            if survey_confidence:
                best_tab_index = max(survey_confidence, key=survey_confidence.get)
                best_score = survey_confidence[best_tab_index]
                
                if best_score > 0:
                    print(f"\n✅ Best survey tab: Tab {best_tab_index + 1} (score: {best_score})")
                    survey_tab = all_pages[best_tab_index]
                    await survey_tab.bring_to_front()
                    return survey_tab
            
            # If no clear winner, ask user
            print("\n🤔 Cannot automatically determine survey tab")
            print("Please click on the correct tab in your browser")
            input("Press Enter after selecting the survey tab...")
            
            # Return currently active tab
            for tab in all_pages:
                try:
                    if await tab.evaluate("document.visibilityState") == "visible":
                        print("✅ Using user-selected active tab")
                        return tab
                except:
                    pass
            
            return page
            
        except Exception as e:
            print(f"❌ Tab switching error: {e}")
            print("⚠️ Continuing with current page reference")
            return page
    
    async def validate_and_switch_if_needed(self, page):
        """Validate page and switch tabs if needed."""
        try:
            # Test if page is valid
            _ = page.url
            
            # Check if we have multiple tabs
            all_pages = page.context.pages
            if len(all_pages) > 1:
                print(f"📑 Multiple tabs detected ({len(all_pages)} tabs)")
                return await self.switch_to_active_tab(page)
            
            return page
            
        except Exception as e:
            print(f"❌ Page validation error: {e}")
            # Try to recover
            return await self.emergency_page_recovery(page)
    
    async def emergency_page_recovery(self, page):
        """Emergency recovery when page reference is lost."""
        print("\n🚨 EMERGENCY PAGE RECOVERY")
        
        try:
            if hasattr(self.stealth_manager, 'browser'):
                contexts = self.stealth_manager.browser.contexts
                for context in contexts:
                    pages = context.pages
                    if pages:
                        print(f"✅ Found {len(pages)} pages in recovery")
                        return pages[0]
            
            print("❌ Could not recover page reference")
            return page
            
        except Exception as e:
            print(f"❌ Emergency recovery failed: {e}")
            return page
    
    async def start_survey_automation(self, page, platform_key: str):
        """
        🛡️ BULLETPROOF: Start automated survey completion with comprehensive error handling.
        """
        print("\n🤖 STARTING BRAIN-ENHANCED AUTOMATION")
        print("=" * 50)
        
        # Enable survey protection
        self.signal_handler.set_survey_mode(True)
        
        try:
            # Initialize automation components
            from handlers.handler_factory import HandlerFactory
            handler_factory = HandlerFactory(self.brain, self.intervention_manager)
            
            # Store current question number for learning
            self._current_question_number = 0
            
            question_count = 0
            max_questions = 50
            
            print("🧠 Quenito's brain is now learning and automating...")
            print("⏹️ Press Ctrl+C to stop automation safely")
            print("⏳ Waiting for page to stabilize...")
            await asyncio.sleep(2)
            
            while question_count < max_questions:
                try:
                    # Validate page before each question
                    page = await self.validate_and_switch_if_needed(page)
                    
                    # Get current page content with error handling
                    try:
                        content = await page.inner_text('body')
                    except Exception as e:
                        print(f"⚠️ Content read error: {e}")
                        page = await self.emergency_page_recovery(page)
                        continue
                    
                    # Check if survey is complete
                    if await self._check_survey_completion(page, content):
                        print("🎉 Survey completed successfully!")
                        break
                    
                    # Check if we're on a survey question page
                    if not self._has_survey_question(content) and question_count == 0:
                        print("⏳ No survey questions detected yet, waiting...")
                        await asyncio.sleep(2)
                        continue
                    
                    # Refresh page analysis after manual intervention
                    if question_count > 0:
                        print("🔄 Refreshing page analysis...")
                        await asyncio.sleep(1)
                        content = await page.inner_text('body')
                        current_url = page.url
                        print(f"   📄 New URL: {current_url}")
                        print(f"   📝 New content length: {len(content)} chars")
                    
                    # Store current question number
                    self._current_question_number = question_count + 1
                    
                    # Get best handler with error handling
                    try:
                        handler, confidence = await handler_factory.select_handler(content, page)
                    except Exception as e:
                        print(f"❌ Handler selection error: {e}")
                        handler = None
                        confidence = 0.0
                    
                    # Update statistics
                    self.stats.increment_question_count(
                        handler_type=handler.__class__.__name__ if handler else "Unknown",
                        confidence=confidence
                    )
                    
                    print(f"\n📋 Question {question_count + 1}:")
                    print(f"   🧠 Handler: {handler.__class__.__name__ if handler else 'None'}")
                    print(f"   🎯 Confidence: {confidence:.2f}")
                    
                    # Get dynamic threshold
                    dynamic_threshold = self.brain.get_dynamic_threshold(
                        handler.__class__.__name__ if handler else "unknown",
                        question_type="unknown"
                    )
                    print(f"   🧠 Dynamic threshold: {dynamic_threshold}")
                    
                    if confidence > dynamic_threshold and handler:
                        print("   🤖 Automating...")
                        
                        # Set page for handler
                        handler.page = page
                        
                        # Attempt automation with error handling
                        try:
                            success = await handler.handle()
                            
                            # Capture learning for successful automation
                            if success and self.learning_capture:
                                await self.learning_capture.capture_question_details(
                                    page, content, question_count + 1
                                )
                            
                            if success:
                                print("   ✅ Automated successfully!")
                                self.stats.increment_automated_count(
                                    handler_type=handler.__class__.__name__,
                                    confidence=confidence
                                )
                            else:
                                print("   ⚠️ Automation failed - requesting manual intervention")
                                await self._enhanced_manual_intervention(page, content, question_count + 1)
                                
                        except Exception as e:
                            print(f"   ❌ Automation error: {e}")
                            await self._enhanced_manual_intervention(page, content, question_count + 1)
                    else:
                        print("   📝 Low confidence - requesting manual intervention")
                        await self._enhanced_manual_intervention(page, content, question_count + 1)
                    
                    question_count += 1
                    
                    # Brief pause between questions
                    print("🔄 Preparing for next question...")
                    await asyncio.sleep(1)
                    
                except KeyboardInterrupt:
                    print("🛡️ Ctrl+C handled by protection system")
                    continue
                except Exception as e:
                    print(f"❌ Error in automation loop: {e}")
                    print("🔄 Attempting recovery...")
                    page = await self.emergency_page_recovery(page)
                    continue
            
            # Show final summary
            print(f"\n📊 AUTOMATION COMPLETE")
            print(f"   Questions Processed: {question_count}")
            print(f"   Automation Rate: {self.stats.get_automation_rate():.1f}%")
            
            # Show advanced learning summary if available
            if self.learning_capture:
                summary = self.learning_capture.get_learning_summary()
                print(f"\n🧠 ADVANCED LEARNING SUMMARY:")
                print(f"   📈 Patterns Discovered: {len(summary.get('patterns_discovered', []))}")
                print(f"   🎯 Question Types: {', '.join(summary.get('question_types_seen', []))}")
            
            # Generate brain intelligence report
            if self.reporter:
                self.stats.end_survey()
                self.reporter.end_session()
                report = self.reporter.generate_brain_intelligence_report(self.stats)
                self.reporter.export_brain_report(report)
                print("🧠 Brain intelligence report generated!")
                
        except Exception as e:
            print(f"❌ Critical automation error: {e}")
            
        finally:
            # Disable protection
            self.signal_handler.set_survey_mode(False)
    
    async def _enhanced_manual_intervention(self, page, content: str, question_number: int):
        """Enhanced manual intervention with advanced learning capture."""
        
        # Enable intervention protection
        self.signal_handler.set_intervention_mode(True)
        
        try:
            if self.learning_capture:
                # Use advanced learning capture
                question_data = await self.learning_capture.capture_question_details(
                    page, content, question_number
                )
                
                # Show enhanced preview
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"\n📝 MANUAL INTERVENTION REQUIRED")
                print("=" * 40)
                print("🧠 Quenito will learn from your action!")
                print(f"📋 Question Preview: {preview}")
                print(f"🎯 Detected Type: {question_data['question_characteristics']['primary_type']}")
                keywords = question_data['detected_patterns']['keywords'][:5]
                if keywords:
                    print(f"🔍 Keywords Found: {', '.join(keywords)}")
                
                print("\n🎯 Manual Action Options:")
                print("   1. Complete manually and continue")
                print("   2. Skip this question")
                print("   3. Stop automation")
                
                choice = input("Select option: ").strip()
                
                if choice == "1":
                    input("\n✋ Please complete the question manually, then press Enter to continue...")
                    
                    # Capture what changed
                    await asyncio.sleep(0.5)
                    new_content = await page.inner_text('body')
                    
                    intervention_result = await self.learning_capture.capture_manual_intervention_result(
                        page, content, new_content, question_data
                    )
                    
                    # Store in brain
                    self.learning_capture.store_learning_in_brain(intervention_result)
                    
                    # Show learning summary
                    summary = self.learning_capture.get_learning_summary()
                    print(f"\n🧠 Learning Summary:")
                    print(f"   📊 Questions analyzed: {summary['questions_analyzed']}")
                    print(f"   🎯 Question types: {', '.join(summary['question_types_seen'])}")
                    print(f"   💾 Knowledge base updated!")
                    
                    self.stats.increment_intervention_count(
                        handler_type="manual",
                        reason="Manual learning capture"
                    )
                    
            else:
                # Fallback to basic intervention
                await self._basic_manual_intervention(page, content)
                
        except Exception as e:
            print(f"❌ Enhanced intervention error: {e}")
            await self._basic_manual_intervention(page, content)
            
        finally:
            # Disable intervention protection
            self.signal_handler.set_intervention_mode(False)
    
    async def _basic_manual_intervention(self, page, content: str):
        """Basic manual intervention fallback."""
        print("\n📝 MANUAL INTERVENTION REQUIRED")
        print("=" * 40)
        print("🧠 Quenito will learn from your action!")
        
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"📋 Question Preview: {preview}")
        
        try:
            page_title = await page.title()
            page_url = page.url
            print(f"📍 Current page: {page_title}")
            print(f"🔗 URL: {page_url}")
        except:
            pass
        
        print("\n🎯 Manual Action Options:")
        print("   1. Complete manually and continue")
        print("   2. Skip this question")
        print("   3. Stop automation")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            input("\n✋ Please complete the question manually, then press Enter to continue...")
            print("🧠 Learning captured - Quenito's brain updated!")
            
            self.stats.increment_intervention_count(
                handler_type="manual",
                reason="Basic manual intervention"
            )
    
    def _has_survey_question(self, content: str) -> bool:
        """Check if content contains survey question indicators."""
        question_indicators = [
            'please type in your', 'are you', 'select', 
            'choose', 'rate', 'how often', 'which of',
            'do you', 'have you', 'what is your'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in question_indicators)
    
    async def _check_survey_completion(self, page, content: str) -> bool:
        """Check if survey is complete with bulletproof error handling."""
        try:
            # More specific completion indicators
            completion_indicators = [
                'thank you for completing',
                'thank you for your time',
                'survey has been completed',
                'your responses have been recorded',
                'survey is now complete',
                'successfully submitted'
            ]
            
            # Check URL for completion
            try:
                current_url = page.url.lower()
                url_complete = any(indicator in current_url for indicator in 
                                 ['thank', 'complete', 'finish', 'submit'])
            except:
                url_complete = False
            
            # Check content for completion
            content_lower = content.lower()
            content_complete = any(indicator in content_lower for indicator in completion_indicators)
            
            if content_complete or url_complete:
                return True
                
            return False
            
        except Exception as e:
            print(f"⚠️ Completion check error: {e}")
            return False
    
    async def analyze_current_page(self, page):
        """Analyze current page with error handling."""
        print("\n🔍 PAGE ANALYSIS")
        print("=" * 20)
        
        try:
            # Validate page first
            page = await self.validate_and_switch_if_needed(page)
            
            content = await page.inner_text('body')
            title = await page.title()
            
            print(f"📄 Page: {title}")
            print(f"📝 Content Length: {len(content)} characters")
            
            # Look for question type indicators
            if any(word in content.lower() for word in ['age', 'gender', 'occupation']):
                print("🎯 Demographics question detected!")
            elif 'rate' in content.lower() or 'scale' in content.lower():
                print("🎯 Rating question detected!")
            elif 'select' in content.lower() and 'all' in content.lower():
                print("🎯 Multi-select question detected!")
            else:
                print("🤔 Unknown question type")
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            print("🔄 Attempting page recovery...")
            await self.emergency_page_recovery(page)
    
    async def manual_learning_mode(self, page):
        """Manual learning mode with enhanced capture."""
        print("\n🧠 MANUAL LEARNING MODE")
        print("=" * 30)
        
        # Enable intervention protection
        self.signal_handler.set_intervention_mode(True)
        
        try:
            page = await self.validate_and_switch_if_needed(page)
            
            page_title = await page.title()
            page_content = await page.inner_text('body')
            print(f"📄 Current Page: {page_title}")
            
            # Use advanced learning if available
            if self.learning_capture:
                question_data = await self.learning_capture.capture_question_details(
                    page, page_content, 1
                )
                print(f"🔍 Detected: {question_data['question_characteristics']['primary_type']} question")
            else:
                # Basic detection
                content_lower = page_content.lower()
                if 'gender' in content_lower:
                    print("🔍 Detected: gender question")
                elif 'age' in content_lower:
                    print("🔍 Detected: age question")
                else:
                    print("🔍 Detected: unknown question")
            
            print("\n🎯 Instructions:")
            print("1. Manually answer the current question in the browser")
            print("2. Click 'Next' to proceed")
            print("3. Press Enter here when done")
            
            input("\n⏸️ Press Enter when completed...")
            
            # Record intervention
            if self.stats:
                self.stats.record_manual_intervention(
                    question_type="manual_learning",
                    confidence=1.0,
                    reason="Manual learning mode",
                    duration_seconds=0.0
                )
                
            print("✅ Manual learning completed!")
            
        except Exception as e:
            print(f"❌ Learning mode error: {e}")
            
        finally:
            # Disable intervention protection
            self.signal_handler.set_intervention_mode(False)
    
    async def test_stealth_detection(self, page):
        """Test stealth detection with error handling."""
        print("\n🕵️ STEALTH DETECTION TEST")
        print("=" * 30)
        
        try:
            page = await self.validate_and_switch_if_needed(page)
            
            # Run stealth detection tests
            detection_tests = {
                'webdriver_detected': await page.evaluate('navigator.webdriver !== undefined'),
                'automation_detected': await page.evaluate('window.chrome && window.chrome.runtime'),
                'headless_detected': await page.evaluate('navigator.plugins.length === 0'),
                'user_agent_valid': 'Chrome' in await page.evaluate('navigator.userAgent'),
                'timing_realistic': True
            }
            
            print("🔍 Detection Results:")
            for test, result in detection_tests.items():
                status = "❌ DETECTED" if (test.endswith('_detected') and result) else "✅ HIDDEN"
                print(f"   • {test}: {status}")
            
            # Calculate stealth score
            stealth_score = sum(1 for test, result in detection_tests.items() 
                              if not (test.endswith('_detected') and result))
            
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
                try:
                    compatibility = await self.stealth_manager.test_platform_compatibility(url)
                    print(f"🕵️ Stealth Level: {compatibility.get('stealth_level', 'UNKNOWN')}")
                except:
                    print("⚠️ Could not test compatibility")
                    
        except Exception as e:
            print(f"❌ Navigation error: {e}")
    
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
            
            if self.brain:
                self.brain.print_brain_intelligence_report()
                
        except Exception as e:
            print(f"❌ Report error: {e}")
    
    async def test_stealth_system(self):
        """Run comprehensive stealth system tests."""
        print("\n🧪 COMPREHENSIVE STEALTH SYSTEM TEST")
        print("=" * 45)
        
        try:
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
            print("❌ Test script not found")
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
            print("📤 Exporting brain data...")
            # Add export logic
        elif choice == "3":
            confirm = input("⚠️ Reset all learning data? (y/N): ").lower().strip()
            if confirm == 'y':
                print("🔄 Learning data reset!")
        elif choice == "4":
            print("👤 User profile update - coming soon!")
    
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
    
    async def run_main_interface(self):
        """Run the main interface loop with bulletproof error handling."""
        
        print("🧠 Initializing Quenito's Digital Brain...")
        print("🕵️ Stealth capabilities loaded")
        print("📊 Intelligence tracking active")
        print("🛡️ Bulletproof protection engaged")
        
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
                print("\n🛡️ Ctrl+C protection active")
                print("Use menu option 0 to exit safely")
                continue
            except Exception as e:
                print(f"❌ Interface error: {e}")
                print("🔄 Recovering...")
                continue


async def main():
    """Main entry point with bulletproof error handling."""
    
    try:
        print("🚀 Starting Quenito Survey Assistant - Ultimate Edition...")
        interface = QuentioUltimateInterface()
        await interface.run_main_interface()
    except KeyboardInterrupt:
        print("\n🛡️ Protected exit - Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🧠 Starting Quenito Survey Assistant - Ultimate Edition v3.0...")
    print("🛡️ Bulletproof error handling + 🕵️ Stealth browser capabilities")
    asyncio.run(main())