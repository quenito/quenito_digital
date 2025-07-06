"""
Enhanced Survey Detector Module
Improved tab detection and survey identification with better timing and reliability.
Enhanced with MyOpinions-specific completion detection.
FIXED: Completion detection no longer triggers false positives on actual questions.
UPDATED: Enhanced completion detection for industry/occupation questions.
"""

import time
import re
from typing import List, Dict, Any, Optional


class SurveyDetector:
    """
    Enhanced survey tab detection and identification with improved timing logic.
    """
    
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        
        # Known survey domains with confidence scores
        self.confirmed_survey_domains = {
            'yoursurveynow.com': 0.95,
            'qualtrics.com': 0.90,
            'decipherinc.com': 0.85,
            'survey.cmix.com': 0.90,
            'surveycmix.com': 0.90,
            'survey-au.yoursurveynow.com': 0.95,  # Added the specific subdomain
            'survey.alchemer.com': 0.90,  
            'alchemer.com': 0.85,         
            'surveys.tapestryresearch.com': 0.90,  # NEW DOMAIN ADDED
            'tapestryresearch.com': 0.85,          # NEW DOMAIN ADDED
        }
        
        # Survey content indicators
        self.survey_indicators = {
            'strong': [
                'survey', 'questionnaire', 'opinion', 'feedback',
                'research', 'study', 'poll', 'evaluation'
            ],
            'medium': [
                'question', 'answer', 'select', 'choose', 'rate',
                'agree', 'disagree', 'opinion', 'preference'
            ],
            'navigation': [
                'next', 'continue', 'submit', 'finish', 'complete',
                'previous', 'back', 'skip'
            ]
        }
        
        # Exclusion patterns
        self.exclusion_patterns = [
            'myopinions.com.au/auth/dashboard',
            'about:blank',
            'data:text/html',
            'chrome-extension://',
            'moz-extension://'
        ]
    
    def detect_survey_tabs_enhanced(self, max_attempts=4, base_wait=4):
        """
        Enhanced tab detection with progressive waiting and multiple detection methods.
        
        Args:
            max_attempts: Maximum number of detection attempts
            base_wait: Base wait time between attempts (seconds)
            
        Returns:
            page object of detected survey tab or None
        """
        print(f"🔍 Starting enhanced survey tab detection with {max_attempts} attempts...")
        
        for attempt in range(1, max_attempts + 1):
            print(f"🔍 Attempt {attempt}/{max_attempts}: Searching for survey tabs...")
            
            # Use comprehensive detection methods
            tabs = self._comprehensive_tab_detection()
            
            # Analyze tabs for survey content
            survey_candidates = self._analyze_tabs_for_survey_content(tabs)
            
            if survey_candidates:
                # Found potential survey tabs
                best_candidate = self._select_best_survey_candidate(survey_candidates)
                if best_candidate and best_candidate['confidence'] > 0.7:
                    print(f"✅ Auto-selected survey tab: {best_candidate['url']}")
                    return best_candidate['page']
            
            # Calculate dynamic wait time (progressively longer waits)
            if attempt < max_attempts:
                wait_time = base_wait + (attempt - 1) * 2
                print(f"⏳ Only found {len(tabs)} tabs, waiting {wait_time}s for survey tab to fully load...")
                time.sleep(wait_time)
                
                # Wait for any new page loads to complete
                self._wait_for_page_loads()
        
        print(f"⚠️ Final attempt: Found {len(tabs)} tabs")
        
        # If no auto-detection, fall back to manual selection
        return self._handle_manual_tab_selection(tabs)
    
    def _comprehensive_tab_detection(self):
        """Use multiple methods to detect all available tabs."""
        all_tabs = []
        unique_urls = set()
        detection_methods = []
        
        try:
            # Method 1: Direct context pages (most reliable)
            if hasattr(self.browser_manager, 'context') and self.browser_manager.context:
                try:
                    context_pages = self.browser_manager.context.pages
                    page_count = len(context_pages)
                    detection_methods.append(f"Direct context ({page_count} pages)")
                    
                    for page in context_pages:
                        try:
                            url = page.url
                            if url and url not in unique_urls:
                                unique_urls.add(url)
                                title = ""
                                try:
                                    title = page.title()
                                except:
                                    pass
                                
                                all_tabs.append({
                                    'page': page,
                                    'url': url,
                                    'title': title,
                                    'source': 'direct_context'
                                })
                        except Exception as e:
                            print(f"🔍 Error accessing page in context: {e}")
                except Exception as e:
                    print(f"🔍 Error with direct context: {e}")
            
            # Method 2: Browser contexts (backup method)
            if hasattr(self.browser_manager, 'browser') and self.browser_manager.browser:
                try:
                    contexts = self.browser_manager.browser.contexts
                    context_count = len(contexts)
                    detection_methods.append(f"Browser contexts ({context_count} contexts)")
                    
                    for context in contexts:
                        for page in context.pages:
                            try:
                                url = page.url
                                if url and url not in unique_urls:
                                    unique_urls.add(url)
                                    title = ""
                                    try:
                                        title = page.title()
                                    except:
                                        pass
                                    
                                    all_tabs.append({
                                        'page': page,
                                        'url': url,
                                        'title': title,
                                        'source': 'browser_contexts'
                                    })
                            except Exception as e:
                                continue  # Skip problematic pages
                except Exception as e:
                    print(f"🔍 Error accessing browser contexts: {e}")
            
            # Method 3: Browser manager pages (if available)
            if hasattr(self.browser_manager, 'get_all_pages'):
                try:
                    manager_pages = self.browser_manager.get_all_pages()
                    page_count = len(manager_pages)
                    detection_methods.append(f"Browser manager ({page_count} pages)")
                    
                    for page in manager_pages:
                        try:
                            url = page.url
                            if url and url not in unique_urls:
                                unique_urls.add(url)
                                title = ""
                                try:
                                    title = page.title()
                                except:
                                    pass
                                
                                all_tabs.append({
                                    'page': page,
                                    'url': url,
                                    'title': title,
                                    'source': 'browser_manager'
                                })
                        except Exception as e:
                            continue
                except Exception as e:
                    print(f"🔍 Error with browser manager: {e}")
            
            # Method 4: Raw browser access (last resort)
            try:
                if hasattr(self.browser_manager, 'browser') and self.browser_manager.browser:
                    detection_methods.append("Raw browser access")
                    # Force browser to update its internal page list
                    for context in self.browser_manager.browser.contexts:
                        pages = context.pages  # This forces a refresh
            except Exception as e:
                print(f"🔍 Error with raw browser access: {e}")
            
        except Exception as e:
            print(f"🔍 Error in comprehensive tab detection: {e}")
        
        methods_used = ", ".join(detection_methods)
        print(f"🔍 Tab detection methods tried: {methods_used}")
        print(f"🔍 Total unique tabs found: {len(all_tabs)}")
        
        return all_tabs
    
    def _wait_for_page_loads(self):
        """Wait for any pending page loads to complete."""
        try:
            if hasattr(self.browser_manager, 'context') and self.browser_manager.context:
                # Wait for all pages to be in a stable state
                for page in self.browser_manager.context.pages:
                    try:
                        # Wait for page to be loaded with a reasonable timeout
                        page.wait_for_load_state('networkidle', timeout=3000)
                    except Exception:
                        # If timeout, continue - page might already be loaded
                        continue
        except Exception as e:
            print(f"🔍 Note: Could not wait for page loads: {e}")
    
    def _analyze_tabs_for_survey_content(self, tabs):
        """Analyze tabs and identify potential survey tabs with confidence scores."""
        survey_candidates = []
        
        for tab in tabs:
            url = tab['url']
            title = tab.get('title', '')
            
            # Skip excluded patterns
            if self._is_excluded_tab(url):
                print(f"❌ {self._get_exclusion_reason(url)}: {url}")
                continue
            
            # Calculate confidence score
            confidence = self._calculate_survey_confidence(url, title, tab['page'])
            
            if confidence > 0.3:  # Minimum threshold for consideration
                survey_candidates.append({
                    'page': tab['page'],
                    'url': url,
                    'title': title,
                    'confidence': confidence,
                    'source': tab['source']
                })
                print(f"✅ Survey candidate found: {url} (confidence: {confidence:.2f})")
            else:
                print(f"❌ Low confidence tab: {url} (confidence: {confidence:.2f})")
        
        return survey_candidates
    
    def _calculate_survey_confidence(self, url, title, page):
        """Calculate confidence score that this is a survey tab."""
        confidence = 0.0
        
        # Domain-based confidence (highest priority)
        for domain, domain_confidence in self.confirmed_survey_domains.items():
            if domain in url:
                confidence += domain_confidence
                break
        
        # URL pattern analysis
        survey_url_patterns = [
            r'survey', r'questionnaire', r'opinion', r'feedback',
            r'research', r'poll', r'study'
        ]
        
        url_lower = url.lower()
        for pattern in survey_url_patterns:
            if re.search(pattern, url_lower):
                confidence += 0.2
                break
        
        # Title analysis
        if title:
            title_lower = title.lower()
            for indicator in self.survey_indicators['strong']:
                if indicator in title_lower:
                    confidence += 0.1
        
        # Content analysis (with error handling)
        try:
            if page and confidence < 0.8:  # Only check content if not already confident
                content = page.inner_text('body').lower()
                
                # Count strong indicators
                strong_matches = sum(1 for indicator in self.survey_indicators['strong'] 
                                   if indicator in content)
                confidence += min(strong_matches * 0.1, 0.3)
                
                # Count navigation indicators
                nav_matches = sum(1 for indicator in self.survey_indicators['navigation'] 
                                if indicator in content)
                confidence += min(nav_matches * 0.05, 0.2)
                
        except Exception as e:
            print(f"🔍 Could not analyze content for {url}: {e}")
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _is_excluded_tab(self, url):
        """Check if tab should be excluded from survey detection."""
        return any(pattern in url for pattern in self.exclusion_patterns)
    
    def _get_exclusion_reason(self, url):
        """Get reason why tab was excluded."""
        if 'about:blank' in url:
            return "Empty tab excluded"
        elif 'myopinions.com.au/auth/dashboard' in url:
            return "MyOpinions dashboard excluded"
        elif 'chrome-extension://' in url or 'moz-extension://' in url:
            return "Browser extension excluded"
        else:
            return "Excluded tab"
    
    def _select_best_survey_candidate(self, candidates):
        """Select the best survey candidate from the list."""
        if not candidates:
            return None
        
        # Sort by confidence score (highest first)
        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Return the highest confidence candidate
        return candidates[0]
    
    def _handle_manual_tab_selection(self, tabs):
        """Handle manual tab selection when automatic detection fails."""
        if not tabs:
            print("❌ No tabs found for manual selection!")
            return None
        
        print("\n❌ No survey tabs detected!")
        print("\n🔧 TROUBLESHOOTING:")
        print("• Make sure you clicked 'START SURVEY' on MyOpinions")
        print("• Verify the survey opened in a new tab")
        print("• Check that you're on the first survey question")
        print("• New domain? It might need manual confirmation...")
        
        print("\n🔧 MANUAL TAB SELECTION")
        print("=" * 40)
        print("\nAvailable tabs:")
        
        for i, tab in enumerate(tabs, 1):
            url = tab['url']
            title = tab.get('title', '')
            
            # Create previews
            title_preview = title[:50] + "..." if len(title) > 50 else title
            url_preview = url[:80] + "..." if len(url) > 80 else url
            
            print(f"{i}. {url_preview}")
            if title_preview:
                print(f"   Title: {title_preview}")
        
        print(f"\nOptions:")
        print(f"• Enter 1-{len(tabs)} to select a tab")
        print(f"• Enter 'r' to refresh/rescan for new tabs")
        print(f"• Enter 'q' to quit")
        
        while True:
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 'r':
                print("🔄 Rescanning for tabs...")
                return self.detect_survey_tabs_enhanced()
            elif choice == 'q':
                print("❌ User chose to quit")
                return None
            elif choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(tabs):
                    selected_tab = tabs[choice_num - 1]
                    
                    # Preview the selected tab
                    print(f"\n📄 Preview of selected tab:")
                    print(f"URL: {selected_tab['url']}")
                    
                    try:
                        page = selected_tab['page']
                        content = page.inner_text('body')
                        content_preview = content[:200] + "..." if len(content) > 200 else content
                        print(f"Content preview: {content_preview}")
                    except Exception as e:
                        print(f"Could not preview content: {e}")
                    
                    confirm = input(f"\nConfirm this selection? (y/n): ").strip().lower()
                    if confirm == 'y':
                        print(f"✅ Manually selected: {selected_tab['url']}")
                        return selected_tab['page']
                    else:
                        print("Selection cancelled, choose again...")
                        continue
                else:
                    print(f"❌ Invalid choice. Please enter 1-{len(tabs)}, 'r', or 'q'")
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(tabs)}, 'r', or 'q'")
    
    def validate_survey_state(self, page):
        """
        Validate that the page is ready for survey automation.
        
        Args:
            page: Playwright page object
            
        Returns:
            bool: True if page is ready for automation
        """
        try:
            print("\n⚠️ Automatic survey state validation failed")
            print("Let's manually verify the current state...")
            
            # Get page content preview
            content = page.inner_text('body')
            content_preview = content[:300] + "..." if len(content) > 300 else content
            
            print(f"\n📄 Current page content preview:")
            print("-" * 60)
            print(content_preview)
            print("-" * 60)
            
            print(f"\n❓ Manual Verification Questions:")
            print("1. Can you see a survey question on the screen?")
            print("2. Is there a 'Next' or 'Continue' button visible?")
            print("3. Are you NOT on a welcome/intro/thank you page?")
            
            confirmation = input("\nAre you on a survey question ready for automation? (y/n): ").strip().lower()
            
            if confirmation == 'y':
                print("✅ Manual confirmation received - starting automation!")
                return True
            else:
                print("❌ Manual verification failed - cannot start automation")
                return False
                
        except Exception as e:
            print(f"❌ Error validating survey state: {e}")
            return False
    
    # ========== ENHANCED COMPLETION DETECTION METHODS ==========
    
    def is_survey_complete(self, page):
        """
        Enhanced survey completion detection with Universal + MyOpinions-specific triggers.
        """
        try:
            current_url = page.url
            page_content = page.inner_text('body').lower()
            page_title = page.title().lower()
            
            print(f"🔍 Checking completion for URL: {current_url}")
            
            # PRIORITY 1: Universal completion detection (NEW - works for ANY platform)
            if self._check_universal_completion(current_url, page_content, page_title, page):
                return True
            
            # PRIORITY 2: MyOpinions specific completion detection (EXISTING)
            if self._check_myopinions_completion(current_url, page_content, page):
                return True
            
            # PRIORITY 3: Generic completion detection (EXISTING - fallback)
            if self._check_generic_completion(current_url, page_content, page_title):
                return True
            
            # PRIORITY 4: Check for no more survey questions (EXISTING - enhanced)
            if self._no_survey_questions_detected(page_content):
                print(f"🎉 Survey completion detected - no more questions found")
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking survey completion: {e}")
            return False
    
    def _check_myopinions_completion(self, current_url, page_content, page):
        """
        Check for MyOpinions-specific completion indicators.
        """
        
        # Method 1: URL-based completion detection (HIGHEST PRIORITY)
        url_completion_patterns = [
            'status=complete',
            'surveyendpageresponded',
            'reward=',
            'myopinions.com.au/surveyendpageresponded',
            'myopinions.com.au/auth/dashboard',
            'myopinions.com.au/member'
        ]
        
        for pattern in url_completion_patterns:
            if pattern.lower() in current_url.lower():
                print(f"🎉 MyOpinions completion detected by URL pattern: {pattern}")
                print(f"📍 Completion URL: {current_url}")
                return True
        
        # Method 2: Content-based completion detection (HIGH PRIORITY)
        myopinions_completion_phrases = [
            'thanks for completing the survey',
            'thank you for completing the survey',
            'survey complete',
            'points have been added to your account',
            'enjoy!',
            'want to redeem even faster',
            'why not try another survey',
            'go to my account',
            'active bonus offers',
            'please check back later for earning opportunities'
        ]
        
        for phrase in myopinions_completion_phrases:
            if phrase in page_content:
                print(f"🎉 MyOpinions completion detected by content: '{phrase}'")
                return True
        
        # Method 3: Check for MyOpinions dashboard elements
        try:
            # Check for "Go to my account" link
            account_links = page.query_selector_all('a')
            for link in account_links:
                try:
                    link_text = link.inner_text().lower()
                    if 'go to my account' in link_text or 'my account' in link_text:
                        print(f"🎉 MyOpinions completion detected by account link: {link_text}")
                        return True
                except:
                    continue
            
            # Check for points notification
            if 'points' in page_content and 'added' in page_content:
                print(f"🎉 MyOpinions completion detected by points notification")
                return True
                
            # Check for survey offer buttons (indicates we're back on main page)
            offer_buttons = page.query_selector_all('button, a')
            for button in offer_buttons:
                try:
                    button_text = button.inner_text().lower()
                    if any(phrase in button_text for phrase in ['start survey', 'start qualification', 'earn more']):
                        print(f"🎉 MyOpinions completion detected by survey offers: {button_text}")
                        return True
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Error checking MyOpinions elements: {e}")
        
        return False
    
    def _check_universal_completion(self, current_url, page_content, page_title, page):
        """
        Universal completion detection for ANY survey platform.
        Enhanced for SurveyMonkey, Qualtrics, Typeform, and other platforms.
        """
        
        # UNIVERSAL METHOD 1: URL-based completion patterns
        universal_url_patterns = [
            'complete', 'finished', 'done', 'thank', 'thanks', 'success',
            'submitted', 'end', 'final', 'conclusion', 'closed', 'finish'
        ]
        
        for pattern in universal_url_patterns:
            if pattern in current_url.lower():
                print(f"🎉 Universal completion detected by URL pattern: {pattern}")
                print(f"📍 Completion URL: {current_url}")
                return True
        
        # UNIVERSAL METHOD 2: Page content completion phrases
        universal_completion_phrases = [
            'thank you for completing',
            'survey complete',
            'questionnaire complete', 
            'your responses have been submitted',
            'thank you for participating',
            'survey has been completed',
            'research complete',
            'study complete',
            'thank you for your time',
            'your participation is complete',
            'responses have been recorded',
            'survey is now complete',
            'thank you for taking',
            'survey successfully submitted',
            'questionnaire submitted',
            'we appreciate your participation',
            'thank you for completing this survey',  # SurveyMonkey specific
            'your survey response has been recorded', # SurveyMonkey specific
            'survey submitted successfully'           # SurveyMonkey specific
        ]
        
        for phrase in universal_completion_phrases:
            if phrase in page_content:
                print(f"🎉 Universal completion detected by content: '{phrase}'")
                return True
        
        # UNIVERSAL METHOD 3: Title-based completion detection
        title_completion_patterns = [
            'complete', 'thank you', 'finished', 'done', 'submitted', 'success'
        ]
        
        for pattern in title_completion_patterns:
            if pattern in page_title:
                print(f"🎉 Universal completion detected by title: '{pattern}'")
                return True
        
        # UNIVERSAL METHOD 4: Check for completion page indicators
        # Look for elements that suggest completion
        try:
            completion_elements = page.query_selector_all('*')
            for element in completion_elements:
                if element.is_visible():
                    element_text = element.inner_text().lower()
                    if ('thank you' in element_text and 'complet' in element_text) or \
                    ('survey' in element_text and 'finish' in element_text) or \
                    ('response' in element_text and 'record' in element_text):
                        print(f"🎉 Universal completion detected by element text")
                        return True
        except:
            pass
        
        # UNIVERSAL METHOD 5: Check for absence of survey questions
        # If there are no more form elements and no question indicators, likely complete
        try:
            form_elements = page.query_selector_all('input[type="text"], input[type="radio"], input[type="checkbox"], select, textarea')
            usable_forms = [el for el in form_elements if el.is_visible() and not el.is_disabled()]
            
            question_indicators = [
                'question', 'select', 'choose', 'rate', 'answer', 'please enter'
            ]
            
            question_count = sum(1 for indicator in question_indicators if indicator in page_content)
            
            if len(usable_forms) == 0 and question_count < 2:
                print(f"🎉 Universal completion detected - no more questions or forms")
                return True
        except:
            pass
        
        return False

    def _check_generic_completion(self, current_url, page_content, page_title):
        """
        Generic completion detection for non-MyOpinions surveys.
        """
        
        # Generic URL patterns
        generic_url_patterns = [
            'thank', 'complete', 'finished', 'done', 'submitted',
            'success', 'end', 'final'
        ]
        
        for pattern in generic_url_patterns:
            if pattern in current_url.lower():
                print(f"🎉 Generic completion detected by URL pattern: {pattern}")
                return True
        
        # Generic content patterns
        generic_completion_phrases = [
            'thank you for your time',
            'survey complete',
            'questionnaire complete',
            'your responses have been submitted',
            'thank you for participating',
            'survey has been completed',
            'research complete',
            'study complete'
        ]
        
        for phrase in generic_completion_phrases:
            if phrase in page_content:
                print(f"🎉 Generic completion detected by content: {phrase}")
                return True
        
        # Generic title patterns
        generic_title_patterns = [
            'complete', 'thank you', 'finished', 'done', 'submitted'
        ]
        
        for pattern in generic_title_patterns:
            if pattern in page_title:
                print(f"🎉 Generic completion detected by title: {pattern}")
                return True
        
        return False
    
    def _no_survey_questions_detected(self, page_content):
        """
        ENHANCED: Check if there are no more survey questions on the page.
        Better handling of industry/occupation questions and all question types.
        """
        
        # Enhanced question indicators
        question_indicators = [
            'question', 'select one', 'choose', 'rate', 'agree', 'disagree',
            'how likely', 'which of the following', 'please select',
            'what is your', 'enter', 'input', 'age', 'years old', 'work in',
            'household work', 'select all that apply', 'please enter your',
            'which gender', 'in which country', 'in which of the following'
        ]
        
        # Form element indicators - more comprehensive
        form_indicators = [
            'input', 'select', 'textarea', 'radio', 'checkbox', 
            'button', 'submit', 'next', 'continue', 'form'
        ]
        
        # Count question indicators
        question_count = sum(1 for indicator in question_indicators if indicator in page_content.lower())
        
        # Count form elements 
        form_count = sum(1 for indicator in form_indicators if indicator in page_content.lower())
        
        # Enhanced logic: Only consider completed if VERY few indicators AND no obvious form elements
        has_questions = question_count >= 2 or form_count >= 3
        
        # Special check: Definite question phrases (EXPANDED FOR ALL TYPES)
        definite_question_phrases = [
            'what is your', 'please enter', 'how old', 'select your',
            'choose your', 'what year', 'years old', 'which gender',
            'please enter your age', 'in which country', 'in which of the following',
            'do you, or does anyone', 'work in any of the following',
            'select all that apply', 'please select one answer',
            'which of the following regions', 'enter a number in the box'
        ]
        
        has_definite_question = any(phrase in page_content.lower() for phrase in definite_question_phrases)
        
        if has_definite_question:
            print(f"🔍 Definite question detected - not completed")
            return False
        
        # Additional check: Look for industry/occupation lists
        industry_indicators = [
            'marketing', 'journalism', 'advertising', 'banking', 'television',
            'market research', 'retail', 'media', 'fashion', 'none of these',
            'it', 'television', 'banking'
        ]
        
        industry_count = sum(1 for indicator in industry_indicators if indicator in page_content.lower())
        
        if industry_count >= 3:  # If we see multiple industry options, it's definitely a question
            print(f"🔍 Industry/occupation question detected - not completed")
            return False
        
        # Additional check: Look for demographic option lists
        demographic_options = [
            'male', 'female', 'other', 'non-binary', 'new south wales', 'victoria',
            'queensland', 'south australia', 'western australia', 'tasmania'
        ]
        
        demo_option_count = sum(1 for option in demographic_options if option in page_content.lower())
        
        if demo_option_count >= 2:  # If we see multiple demographic options, it's a question
            print(f"🔍 Demographic options detected - not completed")
            return False
        
        if has_questions:
            print(f"🔍 Question indicators found: questions={question_count}, forms={form_count}")
            return False
        
        print(f"🔍 No question indicators found: questions={question_count}, forms={form_count}")
        return True
    
    def handle_survey_completion(self, page):
        """
        Handle the survey completion process and trigger report generation.
        Enhanced for MyOpinions specific completion scenarios.
        """
        try:
            print("\n🎉 SURVEY COMPLETION DETECTED!")
            print("="*80)
            
            current_url = page.url
            page_content = page.inner_text('body')
            
            print(f"📍 Completion URL: {current_url}")
            
            # Extract completion details
            self._extract_completion_details(current_url, page_content)
            
            print(f"📄 Completion page preview:")
            print("-" * 60)
            content_preview = page_content[:400] + "..." if len(page_content) > 400 else page_content
            print(content_preview)
            print("-" * 60)
            
            print(f"\n✅ Survey automation completed successfully!")
            print(f"🏆 Ready to generate final report...")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error handling survey completion: {e}")
            return True  # Still consider it completed
    
    def _extract_completion_details(self, url, content):
        """
        Extract and display completion details from MyOpinions completion page.
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
            
            # Look for points message in content
            content_lower = content.lower()
            if 'points have been added' in content_lower:
                # Try to extract the exact points message
                lines = content.split('\n')
                for line in lines:
                    if 'points have been added' in line.lower():
                        print(f"💰 Points Message: {line.strip()}")
                        break
            
            # Check for survey type/ID
            if 'project_id' in url:
                project_match = re.search(r'project_id[_=](\d+)', url)
                if project_match:
                    project_id = project_match.group(1)
                    print(f"🔍 Survey Project ID: {project_id}")
            
            import datetime
            completion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🌟 Survey completed at: {completion_time}")
            
        except Exception as e:
            print(f"⚠️ Could not extract completion details: {e}")
    
    def check_for_emergency_completion(self, page):
        """
        Emergency completion check for edge cases.
        """
        try:
            current_url = page.url
            
            # Check if we've returned to MyOpinions dashboard
            if 'myopinions.com.au/auth' in current_url:
                print(f"🏠 Returned to MyOpinions dashboard - survey completed")
                return True
            
            # Check for obvious completion phrases
            page_text = page.inner_text('body').lower()
            
            emergency_completion_phrases = [
                'thank you for your time and considered responses',
                'survey is now complete',
                'your participation is complete',
                'thank you for participating',
                'responses have been recorded',
                'study is complete'
            ]
            
            for phrase in emergency_completion_phrases:
                if phrase in page_text:
                    print(f"🚨 Emergency completion detected: {phrase}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error in emergency completion check: {e}")
            return False
    
    # ========== EXISTING METHODS CONTINUE ==========
    
    def get_confirmed_domains(self):
        """Get list of confirmed survey domains."""
        return list(self.confirmed_survey_domains.keys())
    
    def add_survey_domain(self, domain, confidence=0.8):
        """Add a new survey domain to the detection list."""
        self.confirmed_survey_domains[domain] = confidence
        print(f"✅ Added survey domain: {domain} (confidence: {confidence})")
    
    def get_detection_stats(self):
        """Get statistics about detection performance."""
        return {
            'confirmed_domains': len(self.confirmed_survey_domains),
            'survey_indicators': {
                'strong': len(self.survey_indicators['strong']),
                'medium': len(self.survey_indicators['medium']),
                'navigation': len(self.survey_indicators['navigation'])
            },
            'exclusion_patterns': len(self.exclusion_patterns)
        }


# Helper function for easy integration
def detect_survey_tab(browser_manager):
    """
    Simple function to detect survey tab using enhanced detection.
    
    Args:
        browser_manager: Browser manager instance
        
    Returns:
        Playwright page object of detected survey tab or None
    """
    detector = SurveyDetector(browser_manager)
    return detector.detect_survey_tabs_enhanced()