"""
Survey Statistics Module
Tracks survey completion statistics and performance metrics.
"""

import time


class SurveyStats:
    """
    Tracks comprehensive survey automation statistics.
    """
    
    def __init__(self):
        """Initialize survey statistics tracking."""
        self.survey_started = False
        self.survey_ended = False  # FIX 4: ADDED MISSING ATTRIBUTE
        self.start_time = None
        self.end_time = None
        self.total_questions = 0
        self.automated_questions = 0
        self.manual_interventions = 0
        self.session_stats = {}
        
        # Legacy stats structure for compatibility
        self.stats = {
            "total_questions": 0,
            "automated_questions": 0,
            "manual_interventions": 0,
            "research_performed": 0,
            "start_time": None,
            "end_time": None,
            "question_types_encountered": {}
        }
    
    def start_survey(self):
        """Mark the start of survey processing."""
        self.survey_started = True
        self.start_time = time.time()
        self.stats["start_time"] = self.start_time
        print("⏰ Survey timing started")
    
    def end_survey(self):
        """Mark the end of survey processing."""
        if not self.survey_ended:  # FIX 4: ENHANCED END_SURVEY METHOD
            self.survey_ended = True
            self.end_time = time.time()
            self.stats["end_time"] = self.end_time
            print("📊 Survey statistics finalized")
            print("⏰ Survey timing completed")
    
    def increment_question_count(self):
        """Increment the total question count."""
        self.total_questions += 1
        self.stats["total_questions"] += 1
    
    def increment_automated_count(self):
        """Increment the automated question count."""
        self.automated_questions += 1
        self.stats["automated_questions"] += 1
    
    def increment_intervention_count(self):
        """Increment the manual intervention count."""
        self.manual_interventions += 1
        self.stats["manual_interventions"] += 1
    
    def increment_research_count(self):
        """Increment the research operation count."""
        self.stats["research_performed"] += 1
    
    def add_question_type(self, question_type: str):
        """Track a question type encounter."""
        if question_type in self.stats["question_types_encountered"]:
            self.stats["question_types_encountered"][question_type] += 1
        else:
            self.stats["question_types_encountered"][question_type] = 1
    
    def get_total_questions(self) -> int:
        """Get total questions processed."""
        return self.total_questions
    
    def get_automated_questions(self) -> int:
        """Get automated questions count."""
        return self.automated_questions
    
    def get_manual_interventions(self) -> int:
        """Get manual interventions count."""
        return self.manual_interventions
    
    def get_automation_rate(self) -> float:
        """Calculate automation rate as percentage."""
        if self.total_questions > 0:
            return (self.automated_questions / self.total_questions) * 100
        return 0.0
    
    def get_total_time(self) -> float:
        """Get total processing time in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def get_questions_per_minute(self) -> float:
        """Calculate questions processed per minute."""
        total_time = self.get_total_time()
        if total_time > 0 and self.total_questions > 0:
            return (self.total_questions / total_time) * 60
        return 0.0
    
    def get_automated_count(self):
        """Get number of successfully automated questions."""
        return getattr(self, 'automated_count', 0)

    def get_intervention_count(self):
        """Get number of manual interventions.""" 
        return getattr(self, 'intervention_count', 0)

    def get_total_questions(self):
        """Get total number of questions processed."""
        return getattr(self, 'total_questions', 0)

    def increment_automated_count(self):
        """Increment automated question counter."""
        if not hasattr(self, 'automated_count'):
            self.automated_count = 0
        self.automated_count += 1

    def increment_intervention_count(self):
        """Increment intervention counter."""
        if not hasattr(self, 'intervention_count'):
            self.intervention_count = 0
        self.intervention_count += 1

    def increment_question_count(self):
        """Increment total question counter."""
        if not hasattr(self, 'total_questions'):
            self.total_questions = 0
        self.total_questions += 1

    def get_stats(self) -> dict:
        """Get all statistics."""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset all statistics."""
        self.survey_started = False
        self.survey_ended = False
        self.start_time = None
        self.end_time = None
        self.total_questions = 0
        self.automated_questions = 0
        self.manual_interventions = 0
        self.session_stats = {}
        
        self.stats = {
            "total_questions": 0,
            "automated_questions": 0,
            "manual_interventions": 0,
            "research_performed": 0,
            "start_time": None,
            "end_time": None,
            "question_types_encountered": {}
        }
        print("🔄 Survey statistics reset")
    
    def print_quick_summary(self):
        """Print a quick statistics summary."""
        print(f"\n📊 QUICK SURVEY SUMMARY:")
        print(f"   Questions processed: {self.total_questions}")
        print(f"   Automated: {self.automated_questions}")
        print(f"   Manual interventions: {self.manual_interventions}")
        print(f"   Automation rate: {self.get_automation_rate():.1f}%")
        
        if self.get_total_time() > 0:
            print(f"   Total time: {self.get_total_time()/60:.1f} minutes")
            print(f"   Questions/minute: {self.get_questions_per_minute():.1f}")