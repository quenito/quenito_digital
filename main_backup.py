#!/usr/bin/env python3
"""
MyOpinions Survey Automation Tool v2.4.0
Enhanced modular architecture with improved handler system and validation.
Enhanced with survey completion detection and improved manual intervention.

Main entry point that orchestrates all components for seamless survey automation.
"""

import time
import sys
import os
import re

# Import core modules
from core.browser_manager import BrowserManager
from core.survey_detector import SurveyDetector  
from core.navigation_controller import NavigationController

# Import utility services
from utils.knowledge_base import KnowledgeBase
from utils.intervention_manager import InterventionManager
from utils.research_engine import ResearchEngine
from utils.reporting import ReportGenerator

# Import handler system
from handlers.handler_factory import HandlerFactory

# Import models
from models.question_types import QuestionTypeDetector
from models.survey_stats import SurveyStats


class SurveyAutomationTool:
    """
    Main survey automation orchestrator that coordinates all components.
    Enhanced with improved handler system, comprehensive error handling, and completion detection.
    """
    
    def __init__(self):
        """Initialize all components with dependency injection."""
        print("🚀 Initializing Enhanced Survey Automation Tool v2.4.0...")
        
        # Initialize utility services
        self.knowledge_base = KnowledgeBase()
        self.intervention_manager = InterventionManager()
        self.research_engine = ResearchEngine(self.knowledge_base)
        self.report_generator = ReportGenerator()
        
        # Initialize core components
        self.browser_manager = BrowserManager()
        self.survey_detector = SurveyDetector(self.browser_manager)  # Pass browser_manager to constructor
        self.navigation_controller = NavigationController()
        
        # Initialize analysis components
        self.question_detector = QuestionTypeDetector(self.knowledge_base)
        self.handler_factory = HandlerFactory(
            self.knowledge_base, 
            self.intervention_manager
        )
        self.survey_stats = SurveyStats()
        
        # Enhanced completion tracking
        self._survey_completed = False
        self._last_intervention_url = None
        
        print("✅ All components initialized successfully")
        
        # Display enhanced system summary
        self._display_system_summary()
    
    def run_persistent_session_automation(self):
        """
        Main persistent session workflow - eliminates cross-domain authentication issues.
        """
        print("\n🌟 Starting Enhanced Persistent Session Automation")
        print("Same-Browser Session Takeover Method with Improved Handlers")
        print("=" * 70)
        
        try:
            self.report_generator.start_session()
            self.survey_stats.start_survey()
            
            # Phase 1: Create persistent browser session
            if not self.browser_manager.create_persistent_browser_session():
                print("❌ Failed to create persistent browser session")
                return False
            
            # Phase 2: Manual navigation phase
            dashboard_tab = self.browser_manager.start_manual_navigation_phase()
            if not dashboard_tab:
                print("❌ Manual navigation phase failed")
                return False
            
            # Phase 3: Enhanced survey tab detection with improved timing
            print("\n" + "="*80)
            print("🔍 PHASE 2: ENHANCED SURVEY TAB DETECTION")
            print("="*80)
            
            survey_page = self.survey_detector.detect_survey_tabs_enhanced()
            if not survey_page:
                print("❌ Survey tab detection failed")
                return False
            
            # Update browser manager to use the detected survey page
            self.browser_manager.page = survey_page
            
            # Phase 4: Validate survey state
            if not self.survey_detector.validate_survey_state(survey_page):
                print("❌ Survey state validation failed")
                return False
            
            # Phase 5: Run enhanced main survey automation loop
            return self._run_main_survey_loop()
            
        except Exception as e:
            print(f"❌ Critical error in persistent session: {e}")
            return False
        
        finally:
            self._finalize_session()
    
    def run_legacy_dashboard_automation(self):
        """
        Legacy workflow starting from MyOpinions dashboard.
        """
        print("\n📋 Starting Legacy Dashboard Automation")
        print("Original Method with Manual Setup")
        print("=" * 60)
        
        try:
            self.report_generator.start_session()
            self.survey_stats.start_survey()
            
            # Create stealth browser
            if not self.browser_manager.create_stealth_browser():
                print("❌ Failed to create browser session")
                return False
            
            # Navigate to dashboard
            if not self.browser_manager.navigate_to("https://www.myopinions.com.au/auth/dashboard"):
                print("❌ Failed to navigate to dashboard")
                return False
            
            # Manual setup instructions
            self._display_manual_setup_instructions()
            
            # Wait for user to reach first question
            input("✋ Press Enter AFTER you've reached the first survey question...")
            
            # Run enhanced main survey automation loop
            return self._run_main_survey_loop()
            
        except Exception as e:
            print(f"❌ Critical error in legacy automation: {e}")
            return False
        
        finally:
            self._finalize_session()
    
    def run_url_method_automation(self):
        """
        Direct URL entry method for quick testing.
        """
        print("\n📎 Starting URL Method Automation")
        print("Direct Survey URL Entry")
        print("=" * 60)
        
        try:
            self.report_generator.start_session()
            self.survey_stats.start_survey()
            
            # Get survey URL from user
            survey_url = input("📎 Enter survey URL: ").strip()
            if not survey_url:
                print("❌ No URL provided. Exiting...")
                return False
            
            # Create browser and navigate
            if not self.browser_manager.create_stealth_browser():
                print("❌ Failed to create browser session")
                return False
            
            if not self.browser_manager.navigate_to(survey_url):
                print("❌ Failed to navigate to survey URL")
                return False
            
            # Run enhanced main survey automation loop
            return self._run_main_survey_loop()
            
        except Exception as e:
            print(f"❌ Critical error in URL method: {e}")
            return False
        
        finally:
            self._finalize_session()
    
    def _run_main_survey_loop(self):
        """
        Enhanced main survey automation loop with completion detection at every step.
        """
        print("\n" + "="*80)
        print("🤖 STARTING ENHANCED SURVEY AUTOMATION")
        print("="*80)
        
        session_stats = self.browser_manager.get_session_stats()
        if session_stats.get("session_mode") == "persistent":
            print(f"🎯 Automation target: {session_stats.get('survey_url', 'Unknown')}")
            print(f"📊 Session transfer #{session_stats.get('session_transfers', 0)}")
        
        print(f"🧠 Loaded handlers: {', '.join(self.handler_factory.get_available_handlers())}")
        print(f"🔧 Enhanced manual intervention with completion detection enabled")
        print(f"📈 Performance tracking and learning enabled")
        print(f"🛡️ Safety-first validation system active")
        
        # Initialize completion tracking
        self._survey_completed = False
        max_questions = 300
        progress_update_interval = 5
        
        try:
            while (self.survey_stats.get_total_questions() < max_questions and 
                   not getattr(self, '_survey_completed', False)):
                
                current_question = self.survey_stats.get_total_questions() + 1
                print(f"\n📝 Processing Question {current_question}")
                
                # Process current page with enhanced completion detection
                should_continue = self._process_survey_page()
                
                if not should_continue or getattr(self, '_survey_completed', False):
                    print("🏁 Survey automation completed!")
                    break
                
                # Show progress update periodically
                if current_question % progress_update_interval == 0:
                    self._display_automation_progress()
                
                # Safety delay between questions
                self.browser_manager.human_like_delay(1000, 2000)
                
                # Emergency completion check after delay
                if self._check_survey_completion():
                    print("🚨 Emergency completion detection triggered!")
                    break
        
        except Exception as e:
            print(f"❌ Error in survey loop: {e}")
            
            # Try emergency completion detection
            if self._check_survey_completion():
                print("🚨 Survey completion detected during error handling!")
            else:
                return False
        
        finally:
            # Ensure survey stats are properly ended
            if hasattr(self, 'survey_stats') and not self.survey_stats.survey_ended:
                self.survey_stats.end_survey()
            
            # Final progress summary
            print(f"\n🎯 FINAL AUTOMATION SUMMARY")
            self._display_automation_progress()
            
            # Handler recommendations
            if hasattr(self, 'handler_factory'):
                recommendations = self.handler_factory.get_handler_recommendations()
                if recommendations:
                    print(f"💡 HANDLER PERFORMANCE RECOMMENDATIONS:")
                    for rec in recommendations:
                        print(f"   {rec}")
        
        if self.survey_stats.get_total_questions() >= max_questions:
            print("⚠️ Reached maximum question limit")
        
        return True
    
    def _process_survey_page(self):
        """
        Enhanced survey page processing with completion detection.
        """
        print(f"--- Processing Survey Page ---")
        current_url = self.browser_manager.get_current_url()
        print(f"Current URL: {current_url}")
        
        # Increment question counter
        self.survey_stats.increment_question_count()
        
        # Wait for page to load
        if not self.browser_manager.wait_for_page_load():
            print("⚠️ Page load timeout - continuing anyway")
        
        # PRIORITY: Check for completion first
        if self._check_survey_completion():
            return False  # Survey is complete
        
        # Handle consent/agreement pages
        if self.navigation_controller.handle_consent_agreement_page(self.browser_manager.page):
            print("📋 Processed consent page, moving to next page")
            return True
        
        # Get page content and identify question type
        page_content = self.browser_manager.get_page_content()
        question_type = self.question_detector.identify_question_type(page_content)
        
        print(f"🔍 Initial question type detection: {question_type}")
        
        # Get best handler for this question
        handler, confidence = self.handler_factory.get_best_handler(
            self.browser_manager.page, 
            page_content
        )
        
        print(f"🎯 Handler selected: {handler.__class__.__name__} (confidence: {confidence:.2f})")
        
        # Execute handler with enhanced completion detection
        try:
            if confidence > 0.5:
                print(f"🤖 Attempting automation with {handler.__class__.__name__}")
                success = handler.handle()
                
                # Record the attempt
                handler_name = handler.__class__.__name__.replace('Handler', '').lower()
                self.handler_factory.record_handler_success(handler_name, success)
                
                if success:
                    print(f"✅ Successfully automated {question_type}")
                    self.survey_stats.increment_automated_count()
                    
                    # Check completion before navigation
                    if self._check_survey_completion():
                        return False  # Survey completed
                    
                    # Navigate to next question
                    self.browser_manager.human_like_delay(1500, 2500)
                    next_success = self.navigation_controller.find_and_click_next_button(
                        self.browser_manager.page, 
                        self.intervention_manager
                    )
                    
                    if not next_success:
                        print("⚠️ Navigation failed - checking for completion")
                        if self._check_survey_completion():
                            return False  # Survey completed
                        
                        # Request navigation assistance
                        result = self._handle_manual_intervention(
                            question_type, 
                            page_content, 
                            "Navigation assistance needed - next button not found"
                        )
                        
                        if result == "SURVEY_COMPLETE":
                            return False  # Survey completed during intervention
                    else:
                        # Navigation successful - check for completion
                        self.browser_manager.human_like_delay(2000, 3000)
                        if self._check_survey_completion():
                            return False  # Survey completed
                else:
                    print(f"🔄 Handler analysis complete - requesting manual intervention")
                    self.survey_stats.increment_intervention_count()
                    result = self._handle_manual_intervention(
                        question_type, 
                        page_content, 
                        "Handler analysis complete - manual completion recommended"
                    )
                    
                    if result == "SURVEY_COMPLETE":
                        return False  # Survey completed during intervention
            else:
                # Low confidence - manual intervention
                confidence_reason = f"Low confidence ({confidence:.2f}) - insufficient certainty for automation"
                print(f"🔄 {confidence_reason}")
                self.survey_stats.increment_intervention_count()
                result = self._handle_manual_intervention(question_type, page_content, confidence_reason)
                
                if result == "SURVEY_COMPLETE":
                    return False  # Survey completed during intervention
                
        except Exception as e:
            print(f"❌ Error processing {question_type}: {e}")
            print(f"🛡️ SAFETY: Exception caught - switching to manual intervention")
            self.survey_stats.increment_intervention_count()
            
            # Record failed attempt
            handler_name = handler.__class__.__name__.replace('Handler', '').lower()
            self.handler_factory.record_handler_success(handler_name, False)
            
            result = self._handle_manual_intervention(
                question_type, 
                page_content, 
                f"Exception prevented automatic processing: {str(e)}"
            )
            
            if result == "SURVEY_COMPLETE":
                return False  # Survey completed during intervention
        
        return True
    
    def _check_survey_completion(self):
        """
        Enhanced survey completion checking with MyOpinions-specific detection.
        """
        try:
            current_url = self.browser_manager.get_current_url()
            page_content = self.browser_manager.get_page_content().lower()
            
            # Method 1: MyOpinions specific completion patterns (HIGHEST PRIORITY)
            myopinions_patterns = [
                'surveyendpageresponded',
                'status=complete',
                'reward=',
                'myopinions.com.au/auth/dashboard'
            ]
            
            for pattern in myopinions_patterns:
                if pattern.lower() in current_url.lower():
                    print(f"🎉 MyOpinions completion detected by URL: {pattern}")
                    print(f"📍 Completion URL: {current_url}")
                    self._handle_survey_completion()
                    return True
            
            # Method 2: MyOpinions content completion phrases
            myopinions_phrases = [
                'thanks for completing the survey',
                'thank you for completing the survey',
                'points have been added to your account',
                'go to my account',
                'want to redeem even faster',
                'why not try another survey'
            ]
            
            for phrase in myopinions_phrases:
                if phrase in page_content:
                    print(f"🎉 MyOpinions completion detected by content: '{phrase}'")
                    self._handle_survey_completion()
                    return True
            
            # Method 3: Use survey detector's completion check
            if hasattr(self.survey_detector, 'is_survey_complete'):
                if self.survey_detector.is_survey_complete(self.browser_manager.page):
                    print("🎉 Survey completion detected by survey detector!")
                    self._handle_survey_completion()
                    return True
            
            # Method 4: Generic completion detection (fallback)
            generic_url_patterns = ['thank', 'complete', 'finished', 'done']
            for pattern in generic_url_patterns:
                if pattern in current_url.lower():
                    print(f"🎉 Generic completion detected by URL: {pattern}")
                    self._handle_survey_completion()
                    return True
            
            generic_phrases = [
                'survey complete', 'questionnaire complete',
                'thank you for your time', 'responses have been submitted'
            ]
            
            for phrase in generic_phrases:
                if phrase in page_content:
                    print(f"🎉 Generic completion detected by content: '{phrase}'")
                    self._handle_survey_completion()
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking survey completion: {e}")
            return False
    
    def _handle_survey_completion(self):
        """
        Handle survey completion and generate final report.
        Enhanced for MyOpinions completion scenarios.
        """
        try:
            print("\n" + "="*80)
            print("🎉 SURVEY COMPLETION DETECTED!")
            print("="*80)
            
            current_url = self.browser_manager.get_current_url()
            
            # Extract completion details
            self._extract_completion_details(current_url)
            
            # End the survey stats
            if hasattr(self, 'survey_stats') and not self.survey_stats.survey_ended:
                self.survey_stats.end_survey()
            
            # Display completion information
            print(f"📍 Final URL: {current_url}")
            
            try:
                page_content = self.browser_manager.get_page_content()
                content_preview = page_content[:300] + "..." if len(page_content) > 300 else page_content
                print(f"📄 Final page content preview:")
                print("-" * 50)
                print(content_preview)
                print("-" * 50)
            except:
                print("📄 Could not retrieve final page content")
            
            # Force finalization to ensure we get the report
            print("\n🏁 Generating final survey report...")
            
            # Set completion flag to prevent further processing
            self._survey_completed = True
            
            print("✅ Survey automation completed successfully!")
            print("🎊 Ready for final report generation!")
            
        except Exception as e:
            print(f"⚠️ Error handling survey completion: {e}")
    
    def _extract_completion_details(self, url):
        """
        Extract and display completion details from MyOpinions completion URL.
        """
        try:
            # Extract points reward from URL
            reward_match = re.search(r'reward=(\d+)', url)
            if reward_match:
                points = reward_match.group(1)
                print(f"🎁 Points Earned: {points}")
            
            # Extract status from URL
            status_match = re.search(r'status=(\w+)', url)
            if status_match:
                status = status_match.group(1)
                print(f"📊 Survey Status: {status}")
            
            # Extract project ID
            project_match = re.search(r'project_id[_=](\d+)', url)
            if project_match:
                project_id = project_match.group(1)
                print(f"🔍 Survey Project ID: {project_id}")
            
            # Get current timestamp
            import datetime
            completion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🌟 Survey completed at: {completion_time}")
            
        except Exception as e:
            print(f"⚠️ Could not extract completion details: {e}")
    
    def _handle_manual_intervention(self, question_type, page_content, reason):
        """
        Enhanced manual intervention with completion detection.
        """
        
        print(f"\n🤝 Initiating enhanced manual intervention for {question_type}")
        print(f"📝 Reason: {reason}")
        
        # Check for completion before intervention
        if self._check_survey_completion():
            print("🎉 Survey completion detected before manual intervention!")
            return "SURVEY_COMPLETE"
        
        # Set up completion checking for intervention manager
        def check_completion():
            return self._check_survey_completion()
        
        def check_page_status():
            try:
                current_url = self.browser_manager.get_current_url()
                
                # Check for completion first
                if self._check_survey_completion():
                    return "COMPLETED"
                
                # Check if URL changed (moved to next question)
                if hasattr(self, '_last_intervention_url'):
                    if current_url != self._last_intervention_url:
                        self._last_intervention_url = current_url
                        return "NEXT_QUESTION"
                
                # Store current URL for next check
                self._last_intervention_url = current_url
                return "NEXT_QUESTION"
                
            except Exception as e:
                print(f"⚠️ Error checking page status: {e}")
                return "UNKNOWN"
        
        # Enhanced intervention manager call
        if hasattr(self.intervention_manager, 'set_completion_check_callback'):
            self.intervention_manager.set_completion_check_callback(check_completion)
            self.intervention_manager.set_page_status_callback(check_page_status)
        
        # Use the intervention manager
        result = self.intervention_manager.request_manual_intervention(
            question_type,
            reason,
            page_content
        )
        
        # Handle special completion result
        if result == "SURVEY_COMPLETE":
            print("🎉 Survey completed during manual intervention!")
            return "SURVEY_COMPLETE"
        
        if result:
            print("✅ Manual intervention completed successfully")
            
            # Post-intervention completion check
            try:
                self.browser_manager.human_like_delay(2000, 3000)  # Wait for page load
                
                if self._check_survey_completion():
                    print("🎉 Survey completion detected after manual intervention!")
                    return "SURVEY_COMPLETE"
                
                new_url = self.browser_manager.get_current_url()
                print(f"📍 Post-intervention URL: {new_url}")
                
            except Exception as e:
                print(f"⚠️ Post-intervention analysis failed: {e}")
        else:
            print("⚠️ Manual intervention encountered issues")
        
        return result
    
    def _display_automation_progress(self):
        """Display current automation progress and enhanced statistics"""
        
        stats = self.survey_stats.get_stats()
        handler_stats = self.handler_factory.get_handler_stats()
        
        print(f"\n📊 AUTOMATION PROGRESS UPDATE")
        print(f"   Questions Processed: {stats.get('total_questions', 0)}")
        print(f"   Automated: {stats.get('automated_questions', 0)}")
        print(f"   Manual Interventions: {stats.get('manual_interventions', 0)}")
        
        if stats.get('total_questions', 0) > 0:
            automation_rate = (stats.get('automated_questions', 0) / stats['total_questions']) * 100
            print(f"   Current Automation Rate: {automation_rate:.1f}%")
        
        # Show top performing handlers
        print(f"   📈 Handler Performance:")
        for handler_name, handler_data in handler_stats.items():
            if handler_data['attempts'] > 0:
                print(f"      {handler_name}: {handler_data['success_rate']:.1f}% success ({handler_data['attempts']} attempts)")
        
        print(f"{'='*60}\n")
    
    def _display_system_summary(self):
        """Display enhanced system capabilities summary."""
        print(f"\n📊 ENHANCED SYSTEM CAPABILITIES:")
        
        # Handler capabilities
        available_handlers = self.handler_factory.get_available_handlers()
        print(f"   🔧 Question Handlers: {len(available_handlers)}")
        print(f"      Available: {', '.join(available_handlers)}")
        
        # Enhanced handler features
        print(f"   ⭐ NEW: Trust Rating Handler - Automated trust/reliability questions")
        print(f"   🔍 NEW: Research Handler - Intelligent research question detection")
        print(f"   👤 ENHANCED: Demographics Handler - Improved employment support")
        print(f"   📊 ENHANCED: Handler Factory - Confidence scoring & performance tracking")
        
        # Knowledge base info
        patterns = self.knowledge_base.get_question_patterns()
        print(f"   🧠 Question Patterns: {len(patterns)}")
        
        # Domain support
        domains = self.knowledge_base.get_confirmed_survey_domains()
        print(f"   🌐 Supported Domains: {len(domains)}")
        print(f"      Confirmed: {', '.join(domains)}")
        
        # Enhanced features
        print(f"   🔍 Research Engine: Ready with caching")
        print(f"   📊 Enhanced Reporting: Q&A capture, handler analytics")
        print(f"   🛡️ Safety System: Validation, error prevention, graceful degradation")
        print(f"   🎯 Learning System: Performance tracking, improvement recommendations")
    
    def _display_manual_setup_instructions(self):
        """Display manual setup instructions for legacy method."""
        print("\n" + "="*60)
        print("🔧 MANUAL SETUP REQUIRED")
        print("="*60)
        print("Please complete the following steps manually:")
        print("1. 🔐 Login to your MyOpinions account (if not already logged in)")
        print("2. 📋 Find and select the survey you want to complete")
        print("3. 🚀 Click 'START SURVEY' button")
        print("4. 📄 Handle any intro pages manually")
        print("5. 🤖 Complete any CAPTCHA if required")
        print("6. ⏹️  STOP when you reach the first actual survey question")
        print("7. ✅ Press Enter here to start enhanced automation")
        print()
        print("💡 The enhanced automation will take over once you reach Question 1!")
        print("🎯 Now featuring improved handlers and comprehensive error handling!")
        print("="*60)
    
    def _finalize_session(self):
        """
        Enhanced session finalization that ensures report generation.
        """
        print("\n🏁 Finalizing enhanced automation session...")
        
        # Ensure survey is marked as ended
        if hasattr(self, 'survey_stats') and not self.survey_stats.survey_ended:
            self.survey_stats.end_survey()
        
        # End the report session
        if hasattr(self, 'report_generator'):
            self.report_generator.end_session()
        
        # Generate comprehensive report
        try:
            survey_stats = self.survey_stats.get_stats() if hasattr(self, 'survey_stats') else {}
            session_stats = self.browser_manager.get_session_stats() if hasattr(self, 'browser_manager') else {}
            handler_stats = self.handler_factory.get_handler_stats() if hasattr(self, 'handler_factory') else {}
            intervention_stats = self.intervention_manager.get_intervention_stats() if hasattr(self, 'intervention_manager') else {}
            research_stats = self.research_engine.get_research_stats() if hasattr(self, 'research_engine') else {}
            
            # Generate and display enhanced report
            if hasattr(self, 'report_generator'):
                full_report = self.report_generator.generate_survey_report(
                    survey_stats, session_stats, handler_stats, 
                    intervention_stats, research_stats
                )
                
                print(full_report)
                
                # Save report
                try:
                    report_filepath = self.report_generator.get_report_filepath()
                    if self.report_generator.export_report(full_report, report_filepath):
                        print(f"📤 Enhanced report saved as: {report_filepath}")
                except Exception as e:
                    print(f"⚠️ Could not save report: {e}")
        
        except Exception as e:
            print(f"⚠️ Error generating final report: {e}")
            
            # Fallback - basic report
            print("\n📊 BASIC COMPLETION SUMMARY:")
            if hasattr(self, 'survey_stats'):
                stats = self.survey_stats.get_stats()
                print(f"   📈 Questions Processed: {stats.get('total_questions', 0)}")
                print(f"   🤖 Automated: {stats.get('automated_questions', 0)}")
                print(f"   🤝 Manual Interventions: {stats.get('manual_interventions', 0)}")
                if stats.get('total_questions', 0) > 0:
                    rate = (stats.get('automated_questions', 0) / stats['total_questions']) * 100
                    print(f"   📊 Automation Rate: {rate:.1f}%")
        
        # Display final performance summary
        print(f"\n🎯 FINAL PERFORMANCE SUMMARY:")
        if hasattr(self, 'survey_stats'):
            final_stats = self.survey_stats.get_stats()
            if final_stats.get('total_questions', 0) > 0:
                automation_rate = (final_stats.get('automated_questions', 0) / final_stats['total_questions']) * 100
                print(f"   📈 Final Automation Rate: {automation_rate:.1f}%")
                print(f"   🤖 Questions Automated: {final_stats.get('automated_questions', 0)}")
                print(f"   🤝 Manual Interventions: {final_stats.get('manual_interventions', 0)}")
        
        # Show completion status
        if getattr(self, '_survey_completed', False):
            print(f"   🎉 Survey Status: COMPLETED SUCCESSFULLY")
        else:
            print(f"   ⚠️ Survey Status: INCOMPLETE OR INTERRUPTED")
        
        # Handler performance summary
        if hasattr(self, 'handler_factory'):
            handler_performance = self.handler_factory.get_handler_stats()
            print(f"   🏆 Top Performing Handlers:")
            sorted_handlers = sorted(
                [(name, data) for name, data in handler_performance.items() if data['attempts'] > 0],
                key=lambda x: x[1]['success_rate'],
                reverse=True
            )
            for name, data in sorted_handlers[:3]:  # Top 3
                print(f"      {name}: {data['success_rate']:.1f}% ({data['attempts']} attempts)")
        
        # Keep browser open for review
        print("\n✋ Browser will remain open for review...")
        input("Press Enter to close browser and exit...")
        
        # Clean up
        if hasattr(self, 'browser_manager'):
            self.browser_manager.close_browser()


def main():
    """Main entry point for the enhanced survey automation tool."""
    print("🚀 MyOpinions Survey Automation Tool v2.4.0")
    print("Enhanced Modular Architecture with Improved Handlers & Validation")
    print("=" * 70)
    
    try:
        # Initialize the enhanced tool
        tool = SurveyAutomationTool()
        
        # Display method options
        print("\n🎯 Choose your automation method:")
        print("1. 🌟 Persistent Session (RECOMMENDED) - Same browser takeover with enhanced handlers")
        print("2. 📋 Legacy Dashboard - Start from dashboard with improved automation")
        print("3. 📎 URL Method - Paste existing survey URL with enhanced processing")
        print()
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        success = False
        
        if choice == "1":
            print("\n🌟 Starting enhanced persistent session automation...")
            success = tool.run_persistent_session_automation()
        elif choice == "2":
            print("\n📋 Starting fresh from MyOpinions dashboard with enhanced automation...")
            success = tool.run_legacy_dashboard_automation()
        elif choice == "3":
            print("\n📎 Using URL method with enhanced processing...")
            success = tool.run_url_method_automation()
        else:
            print("❌ Invalid choice. Please run the tool again and select 1, 2, or 3.")
            return
        
        if success:
            print("\n🎉 Enhanced survey automation completed successfully!")
            print("📊 Check the detailed report above for performance insights and recommendations!")
        else:
            print("\n⚠️ Survey automation encountered issues")
            print("💡 Check the enhanced error reporting for improvement suggestions")
            
    except KeyboardInterrupt:
        print("\n⏹️ User interrupted the automation")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()