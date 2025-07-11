#!/usr/bin/env python3
"""
Enhanced Learning Intervention Manager
Comprehensive data capture with learning capabilities for survey automation improvement.
"""

import time
import json
import os
from typing import Dict, Any, List, Optional
from utils.intervention_manager import InterventionManager


class EnhancedLearningInterventionManager(InterventionManager):
    """
    Enhanced intervention manager with comprehensive learning capabilities.
    Extends the base InterventionManager with data capture and learning features.
    """
    
    def __init__(self):
        super().__init__()
        
        # Enhanced learning data structures
        self.learning_session_data = {
            "session_id": f"session_{int(time.time())}",
            "start_time": time.time(),
            "interventions": [],
            "page_captures": [],
            "learning_insights": [],
            "handler_performance": {}
        }
        
        # Ultra-conservative confidence thresholds (98-99%)
        self.confidence_thresholds = {
            "demographics": 0.98,        # 98% - highest confidence needed
            "brand_familiarity": 0.98,   # 98% - matrix questions need precision
            "rating_matrix": 0.99,       # 99% - complex interactions
            "multi_select": 0.97,        # 97% - multiple selections
            "trust_rating": 0.96,        # 96% - scaling questions
            "research_required": 0.95,   # 95% - research complexity
            "unknown": 0.99              # 99% - unknown patterns
        }
        
        # Create learning data directory
        self.learning_data_dir = "learning_data"
        os.makedirs(self.learning_data_dir, exist_ok=True)
    
    def enhanced_manual_intervention_flow(self, question_type: str, reason: str, page_content: str = "", page=None) -> str:
        """
        Enhanced manual intervention with comprehensive data capture and learning.
        
        Args:
            question_type: Type of question requiring intervention
            reason: Reason why automation failed
            page_content: Content of the current page
            page: Playwright page object for advanced capture
            
        Returns:
            str: Result of intervention ("COMPLETE" or "SURVEY_COMPLETE")
        """
        print("\n" + "="*80)
        print("🔄 ENHANCED LEARNING MODE: Manual intervention required")
        print("📚 System is capturing comprehensive learning data...")
        print("="*80)
        
        intervention_start_time = time.time()
        
        # Phase 1: Capture pre-intervention state
        print("📸 Phase 1: Capturing page state...")
        pre_intervention_data = self._capture_comprehensive_page_state(page, question_type, reason)
        
        # Phase 2: Display intervention context
        self._display_enhanced_intervention_context(question_type, reason, page_content)
        
        # Phase 3: User completes manually
        print("🔧 MANUAL INTERVENTION INSTRUCTIONS:")
        print("1. Please complete this question manually in the browser")
        print("2. Click the 'Next' or 'Continue' button to move to the next question")
        print("3. Wait until the next question loads completely")
        print("4. Press Enter here to resume automation")
        print()
        print("📊 Learning System Status:")
        print(f"   • Question Type: {question_type}")
        print(f"   • Confidence Threshold: {self.confidence_thresholds.get(question_type, 0.95):.0%}")
        print(f"   • Learning Data: Being captured for future enhancement")
        print()
        
        user_input = input("✋ Press Enter AFTER you've completed the question and moved to the next page...")
        
        # Phase 4: Capture post-intervention state
        print("📸 Phase 2: Capturing response data...")
        post_intervention_data = self._capture_user_response_data(page)
        
        # Phase 5: Analyze and learn
        print("🧠 Phase 3: Analyzing learning opportunities...")
        learning_insights = self._analyze_learning_opportunities(
            pre_intervention_data, post_intervention_data, question_type, reason
        )
        
        # Phase 6: Store learning data
        intervention_duration = time.time() - intervention_start_time
        self._store_intervention_learning_data({
            "question_type": question_type,
            "reason": reason,
            "pre_state": pre_intervention_data,
            "post_state": post_intervention_data,
            "learning_insights": learning_insights,
            "duration": intervention_duration,
            "timestamp": time.time()
        })
        
        print("✅ Learning data captured! System intelligence enhanced!")
        print("🚀 Resuming automation with improved capabilities...")
        print("="*80 + "\n")
        
        # Check for survey completion
        if self._check_completion_after_intervention(page):
            return "SURVEY_COMPLETE"
        
        return "COMPLETE"
    
    def _capture_comprehensive_page_state(self, page, question_type: str, reason: str) -> Dict[str, Any]:
        """
        Capture comprehensive page state for learning analysis.
        """
        try:
            if not page:
                return {"error": "No page object available"}
            
            # Basic page information
            page_data = {
                "url": page.url,
                "title": page.title(),
                "timestamp": time.time(),
                "question_type": question_type,
                "failure_reason": reason
            }
            
            # Page content
            try:
                page_data["full_content"] = page.inner_text('body')
                page_data["content_length"] = len(page_data["full_content"])
            except Exception as e:
                page_data["content_error"] = str(e)
            
            # Form elements analysis
            page_data["form_elements"] = self._catalog_form_elements(page)
            
            # Interactive elements
            page_data["interactive_elements"] = self._find_interactive_elements(page)
            
            # Screenshot capture (optional - can be enabled for detailed analysis)
            if self._should_capture_screenshot():
                try:
                    screenshot_path = f"{self.learning_data_dir}/screenshot_{int(time.time())}.png"
                    page.screenshot(path=screenshot_path, full_page=True)
                    page_data["screenshot_path"] = screenshot_path
                except Exception as e:
                    page_data["screenshot_error"] = str(e)
            
            return page_data
            
        except Exception as e:
            return {"capture_error": str(e), "timestamp": time.time()}
    
    def _catalog_form_elements(self, page) -> Dict[str, Any]:
        """Catalog all form elements on the page for learning."""
        try:
            elements_data = {
                "radio_buttons": [],
                "checkboxes": [],
                "text_inputs": [],
                "dropdowns": [],
                "buttons": []
            }
            
            # Radio buttons
            radios = page.query_selector_all('input[type="radio"]')
            for i, radio in enumerate(radios):
                try:
                    elements_data["radio_buttons"].append({
                        "index": i,
                        "value": radio.get_attribute('value') or "",
                        "name": radio.get_attribute('name') or "",
                        "id": radio.get_attribute('id') or "",
                        "visible": radio.is_visible(),
                        "enabled": not radio.is_disabled()
                    })
                except:
                    continue
            
            # Checkboxes
            checkboxes = page.query_selector_all('input[type="checkbox"]')
            for i, checkbox in enumerate(checkboxes):
                try:
                    elements_data["checkboxes"].append({
                        "index": i,
                        "value": checkbox.get_attribute('value') or "",
                        "name": checkbox.get_attribute('name') or "",
                        "visible": checkbox.is_visible(),
                        "enabled": not checkbox.is_disabled()
                    })
                except:
                    continue
            
            # Text inputs
            text_inputs = page.query_selector_all('input[type="text"], input[type="number"], input:not([type])')
            for i, input_elem in enumerate(text_inputs):
                try:
                    elements_data["text_inputs"].append({
                        "index": i,
                        "type": input_elem.get_attribute('type') or "text",
                        "placeholder": input_elem.get_attribute('placeholder') or "",
                        "name": input_elem.get_attribute('name') or "",
                        "visible": input_elem.is_visible(),
                        "enabled": not input_elem.is_disabled()
                    })
                except:
                    continue
            
            # Dropdowns
            selects = page.query_selector_all('select')
            for i, select in enumerate(selects):
                try:
                    options = []
                    select_options = select.query_selector_all('option')
                    for option in select_options:
                        options.append({
                            "value": option.get_attribute('value') or "",
                            "text": option.inner_text() or ""
                        })
                    
                    elements_data["dropdowns"].append({
                        "index": i,
                        "name": select.get_attribute('name') or "",
                        "options": options,
                        "visible": select.is_visible(),
                        "enabled": not select.is_disabled()
                    })
                except:
                    continue
            
            return elements_data
            
        except Exception as e:
            return {"error": str(e)}
    
    def _find_interactive_elements(self, page) -> Dict[str, Any]:
        """Find all interactive elements for learning."""
        try:
            interactive_data = {
                "buttons": [],
                "links": [],
                "clickable_elements": []
            }
            
            # Buttons
            buttons = page.query_selector_all('button, input[type="submit"], input[type="button"]')
            for i, button in enumerate(buttons):
                try:
                    interactive_data["buttons"].append({
                        "index": i,
                        "text": button.inner_text() or "",
                        "value": button.get_attribute('value') or "",
                        "type": button.get_attribute('type') or "",
                        "visible": button.is_visible(),
                        "enabled": not button.is_disabled()
                    })
                except:
                    continue
            
            return interactive_data
            
        except Exception as e:
            return {"error": str(e)}
    
    def _capture_user_response_data(self, page) -> Dict[str, Any]:
        """Capture what the user did during manual intervention."""
        try:
            if not page:
                return {"error": "No page object available"}
            
            response_data = {
                "timestamp": time.time(),
                "url_after": page.url,
                "title_after": page.title(),
            }
            
            # Try to capture any form changes (this is challenging, so we'll focus on page changes)
            try:
                response_data["content_after"] = page.inner_text('body')
                response_data["content_length_after"] = len(response_data["content_after"])
            except Exception as e:
                response_data["content_error"] = str(e)
            
            return response_data
            
        except Exception as e:
            return {"capture_error": str(e)}
    
    def _analyze_learning_opportunities(self, pre_data: Dict, post_data: Dict, question_type: str, reason: str) -> Dict[str, Any]:
        """Analyze the intervention to identify learning opportunities."""
        insights = {
            "question_type": question_type,
            "failure_reason": reason,
            "learning_opportunities": [],
            "suggested_improvements": [],
            "pattern_analysis": {},
            "timestamp": time.time()
        }
        
        # Analyze form elements for patterns
        if "form_elements" in pre_data:
            form_elements = pre_data["form_elements"]
            
            # Count element types
            insights["pattern_analysis"] = {
                "radio_count": len(form_elements.get("radio_buttons", [])),
                "checkbox_count": len(form_elements.get("checkboxes", [])),
                "text_input_count": len(form_elements.get("text_inputs", [])),
                "dropdown_count": len(form_elements.get("dropdowns", []))
            }
            
            # Generate learning opportunities based on element patterns
            if question_type == "demographics":
                insights["learning_opportunities"].append("Demographics handler needs enhancement for this element pattern")
                insights["suggested_improvements"].append("Update demographics element selectors")
            
            elif question_type == "unknown":
                insights["learning_opportunities"].append("New question pattern discovered")
                insights["suggested_improvements"].append(f"Create new handler for {question_type} questions")
        
        # URL change analysis
        if pre_data.get("url") != post_data.get("url_after"):
            insights["learning_opportunities"].append("Page navigation occurred during intervention")
            insights["suggested_improvements"].append("Improve navigation detection logic")
        
        return insights
    
    def _store_intervention_learning_data(self, intervention_data: Dict[str, Any]):
        """Store intervention learning data for batch processing."""
        # Add to session data
        self.learning_session_data["interventions"].append(intervention_data)
        
        # Save to file for persistence
        filename = f"{self.learning_data_dir}/intervention_{int(time.time())}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(intervention_data, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️ Could not save learning data: {e}")
    
    def _display_enhanced_intervention_context(self, question_type: str, reason: str, page_content: str):
        """Display enhanced context for the intervention."""
        print(f"📍 Question Type: {question_type}")
        print(f"❌ Automation Failure Reason: {reason}")
        print(f"🎯 Confidence Threshold: {self.confidence_thresholds.get(question_type, 0.95):.0%}")
        
        if page_content:
            print("\n📄 Page Content Sample:")
            print("-" * 40)
            content_sample = page_content[:300] + "..." if len(page_content) > 300 else page_content
            print(content_sample)
            print("-" * 40)
        
        # Provide question-specific guidance
        self._provide_enhanced_guidance(question_type)
    
    def _provide_enhanced_guidance(self, question_type: str):
        """Provide enhanced guidance based on question type."""
        guidance_map = {
            "demographics": [
                "💡 Demographics: Fill with your actual information",
                "🎯 Learning Focus: Element detection patterns",
                "📊 This helps improve automation accuracy"
            ],
            "unknown": [
                "💡 Unknown Question: New pattern detected!",
                "🔍 Learning Focus: Question type classification", 
                "🚀 Your response will create new automation capabilities"
            ],
            "trust_rating": [
                "💡 Trust Rating: Select moderate trust levels",
                "⭐ Learning Focus: Scale detection and response patterns"
            ]
        }
        
        guidance = guidance_map.get(question_type, [
            "💡 General: Answer naturally and accurately",
            "📚 Learning Focus: General automation improvement"
        ])
        
        print(f"\n🎓 LEARNING GUIDANCE FOR {question_type.upper()}:")
        for tip in guidance:
            print(f"   {tip}")
        print()
    
    def _should_capture_screenshot(self) -> bool:
        """Determine if we should capture screenshots (configurable)."""
        # Start with False for performance, can be enabled for detailed analysis
        return False
    
    def _check_completion_after_intervention(self, page) -> bool:
        """Check if survey completed after intervention."""
        try:
            if not page:
                return False
            
            # Quick completion check
            current_url = page.url.lower()
            completion_patterns = [
                'complete', 'thank', 'finish', 'done', 'success',
                'myopinions.com.au/auth', 'reward='
            ]
            
            return any(pattern in current_url for pattern in completion_patterns)
            
        except Exception:
            return False
    
    def generate_learning_session_report(self) -> Dict[str, Any]:
        """Generate comprehensive learning report for the session."""
        session_duration = time.time() - self.learning_session_data["start_time"]
        
        report = {
            "session_summary": {
                "session_id": self.learning_session_data["session_id"],
                "duration_minutes": session_duration / 60,
                "total_interventions": len(self.learning_session_data["interventions"]),
                "learning_opportunities": sum(len(i.get("learning_insights", {}).get("learning_opportunities", [])) 
                                            for i in self.learning_session_data["interventions"])
            },
            "intervention_breakdown": {},
            "learning_insights": [],
            "improvement_recommendations": []
        }
        
        # Analyze interventions by type
        for intervention in self.learning_session_data["interventions"]:
            q_type = intervention["question_type"]
            if q_type not in report["intervention_breakdown"]:
                report["intervention_breakdown"][q_type] = {
                    "count": 0,
                    "total_duration": 0,
                    "reasons": []
                }
            
            report["intervention_breakdown"][q_type]["count"] += 1
            report["intervention_breakdown"][q_type]["total_duration"] += intervention["duration"]
            report["intervention_breakdown"][q_type]["reasons"].append(intervention["reason"])
        
        # Generate improvement recommendations
        for q_type, data in report["intervention_breakdown"].items():
            avg_duration = data["total_duration"] / data["count"]
            report["improvement_recommendations"].append({
                "question_type": q_type,
                "priority": "high" if data["count"] >= 3 else "medium",
                "recommendation": f"Enhance {q_type} handler - {data['count']} interventions, avg {avg_duration:.1f}s"
            })
        
        return report
    
    def save_learning_session(self):
        """Save complete learning session data."""
        session_file = f"{self.learning_data_dir}/session_{self.learning_session_data['session_id']}.json"
        try:
            # Generate final report
            final_report = self.generate_learning_session_report()
            self.learning_session_data["final_report"] = final_report
            
            # Save session
            with open(session_file, 'w') as f:
                json.dump(self.learning_session_data, f, indent=2, default=str)
            
            print(f"📊 Learning session saved: {session_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving learning session: {e}")
            return False