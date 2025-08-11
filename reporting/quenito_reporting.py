"""
Quenito Business Reporting System
Complete analytics and tracking for survey automation business
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import time

@dataclass
class SurveyCompletion:
    """Data class for tracking survey completions"""
    timestamp: float
    platform: str
    survey_id: str
    topic: str
    points: int
    duration_seconds: int
    questions_total: int
    questions_automated: int
    automation_rate: float
    vision_api_calls: int
    pattern_matches: int
    earnings_usd: float
    
class QuenitoReporting:
    """Complete business reporting system for Quenito"""
    
    def __init__(self, data_dir: str = "personas/quenito/reporting"):
        self.data_dir = data_dir
        self.current_session_file = None
        self.session_start = None
        self.session_data = {
            'surveys': [],
            'totals': {},
            'hourly_rate': 0
        }
        
        # Platform point values (customize these)
        self.point_values = {
            'myopinions': 0.01,      # $0.01 per point
            'yougov': 0.001,         # $0.001 per point  
            'swagbucks': 0.01,       # 1 SB = $0.01
            'toluna': 0.0003,        # 3000 points = $1
            'ipsos': 0.01,           # $0.01 per point
            'default': 0.01
        }
        
        os.makedirs(self.data_dir, exist_ok=True)
        self.load_historical_data()
    
    def start_session(self, session_name: Optional[str] = None):
        """Start a new reporting session"""
        self.session_start = time.time()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if session_name:
            filename = f"session_{timestamp}_{session_name}.json"
        else:
            filename = f"session_{timestamp}.json"
        
        self.current_session_file = os.path.join(self.data_dir, filename)
        
        print(f"""
╔══════════════════════════════════════════════════════╗
║          🚀 QUENITO SESSION STARTED                   ║
║          {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                        ║
╚══════════════════════════════════════════════════════╝
        """)
    
    def log_survey_completion(self, 
                             platform: str,
                             survey_id: str,
                             topic: str,
                             points: int,
                             duration_seconds: int,
                             questions_total: int,
                             questions_automated: int,
                             vision_api_calls: int,
                             pattern_matches: int):
        """Log a completed survey"""
        
        # Calculate earnings
        point_value = self.point_values.get(platform.lower(), self.point_values['default'])
        earnings = points * point_value
        
        # Calculate automation rate
        automation_rate = (questions_automated / questions_total * 100) if questions_total > 0 else 0
        
        # Create completion record
        completion = SurveyCompletion(
            timestamp=time.time(),
            platform=platform,
            survey_id=survey_id,
            topic=topic,
            points=points,
            duration_seconds=duration_seconds,
            questions_total=questions_total,
            questions_automated=questions_automated,
            automation_rate=automation_rate,
            vision_api_calls=vision_api_calls,
            pattern_matches=pattern_matches,
            earnings_usd=earnings
        )
        
        # Add to session
        self.session_data['surveys'].append(asdict(completion))
        
        # Save immediately
        self.save_session()
        
        # Print immediate feedback
        print(f"""
✅ SURVEY COMPLETED!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Platform: {platform}
📝 Topic: {topic}
💰 Points: {points} (${earnings:.2f})
⏱️  Duration: {duration_seconds//60}m {duration_seconds%60}s
🤖 Automation: {questions_automated}/{questions_total} ({automation_rate:.1f}%)
👁️  Vision Calls: {vision_api_calls} (${vision_api_calls * 0.001:.3f})
🎯 Pattern Matches: {pattern_matches}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
        
        return completion
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        
        if not self.session_data['surveys']:
            return {'status': 'No surveys completed yet'}
        
        surveys = self.session_data['surveys']
        session_duration = time.time() - self.session_start if self.session_start else 0
        
        # Calculate totals
        total_surveys = len(surveys)
        total_points = sum(s['points'] for s in surveys)
        total_earnings = sum(s['earnings_usd'] for s in surveys)
        total_questions = sum(s['questions_total'] for s in surveys)
        total_automated = sum(s['questions_automated'] for s in surveys)
        total_vision_calls = sum(s['vision_api_calls'] for s in surveys)
        total_pattern_matches = sum(s['pattern_matches'] for s in surveys)
        avg_automation_rate = (total_automated / total_questions * 100) if total_questions > 0 else 0
        
        # Calculate hourly rate
        hours_worked = session_duration / 3600
        hourly_rate = total_earnings / hours_worked if hours_worked > 0 else 0
        
        # Group by platform
        by_platform = {}
        for survey in surveys:
            platform = survey['platform']
            if platform not in by_platform:
                by_platform[platform] = {
                    'count': 0,
                    'points': 0,
                    'earnings': 0
                }
            by_platform[platform]['count'] += 1
            by_platform[platform]['points'] += survey['points']
            by_platform[platform]['earnings'] += survey['earnings_usd']
        
        # Group by topic
        by_topic = {}
        for survey in surveys:
            topic = survey['topic']
            if topic not in by_topic:
                by_topic[topic] = 0
            by_topic[topic] += 1
        
        return {
            'session_duration_seconds': int(session_duration),
            'session_duration_formatted': self._format_duration(session_duration),
            'total_surveys': total_surveys,
            'total_points': total_points,
            'total_earnings': total_earnings,
            'hourly_rate': hourly_rate,
            'total_questions': total_questions,
            'total_automated': total_automated,
            'automation_rate': avg_automation_rate,
            'vision_api_calls': total_vision_calls,
            'vision_api_cost': total_vision_calls * 0.001,
            'pattern_matches': total_pattern_matches,
            'by_platform': by_platform,
            'by_topic': by_topic,
            'profit_after_api': total_earnings - (total_vision_calls * 0.001)
        }
    
    def print_session_report(self):
        """Print beautiful session report"""
        
        stats = self.get_session_stats()
        
        if 'status' in stats:
            print(stats['status'])
            return
        
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    📊 QUENITO SESSION REPORT                      ║
╚══════════════════════════════════════════════════════════════════╝

⏱️  SESSION TIME: {stats['session_duration_formatted']}
💰 HOURLY RATE: ${stats['hourly_rate']:.2f}/hour

📈 PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Surveys Completed:     {stats['total_surveys']}
Total Points:          {stats['total_points']:,}
Total Earnings:        ${stats['total_earnings']:.2f}
Automation Rate:       {stats['automation_rate']:.1f}%
Vision API Cost:       ${stats['vision_api_cost']:.3f}
Net Profit:           ${stats['profit_after_api']:.2f}

🤖 AUTOMATION STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Questions Total:       {stats['total_questions']}
Questions Automated:   {stats['total_automated']}
Pattern Matches:       {stats['pattern_matches']}
Vision API Calls:      {stats['vision_api_calls']}

📊 BY PLATFORM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
        
        for platform, data in stats['by_platform'].items():
            print(f"{platform:15} | Surveys: {data['count']:3} | Points: {data['points']:6,} | ${data['earnings']:.2f}")
        
        print(f"""
📝 BY TOPIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
        
        for topic, count in sorted(stats['by_topic'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"{topic:20} | {count} surveys")
        
        print("\n" + "═" * 70 + "\n")
    
    def get_daily_report(self, date: Optional[datetime] = None) -> Dict:
        """Get report for a specific day"""
        
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y%m%d")
        daily_data = {
            'date': date_str,
            'surveys': [],
            'total_earnings': 0,
            'total_points': 0,
            'total_surveys': 0
        }
        
        # Load all sessions for this day
        for filename in os.listdir(self.data_dir):
            if date_str in filename and filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r') as f:
                    session = json.load(f)
                    daily_data['surveys'].extend(session.get('surveys', []))
        
        # Calculate totals
        daily_data['total_surveys'] = len(daily_data['surveys'])
        daily_data['total_points'] = sum(s['points'] for s in daily_data['surveys'])
        daily_data['total_earnings'] = sum(s['earnings_usd'] for s in daily_data['surveys'])
        
        return daily_data
    
    def get_weekly_report(self) -> Dict:
        """Get report for the current week"""
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_data = {
            'week_start': week_start.strftime("%Y-%m-%d"),
            'daily_earnings': {},
            'total_earnings': 0,
            'total_surveys': 0,
            'best_day': None,
            'best_day_earnings': 0
        }
        
        for i in range(7):
            day = week_start + timedelta(days=i)
            daily = self.get_daily_report(day)
            
            day_str = day.strftime("%A")
            weekly_data['daily_earnings'][day_str] = daily['total_earnings']
            weekly_data['total_earnings'] += daily['total_earnings']
            weekly_data['total_surveys'] += daily['total_surveys']
            
            if daily['total_earnings'] > weekly_data['best_day_earnings']:
                weekly_data['best_day'] = day_str
                weekly_data['best_day_earnings'] = daily['total_earnings']
        
        weekly_data['average_daily'] = weekly_data['total_earnings'] / 7
        weekly_data['projected_monthly'] = weekly_data['total_earnings'] * 4.33
        
        return weekly_data
    
    def print_weekly_summary(self):
        """Print weekly performance summary"""
        
        report = self.get_weekly_report()
        
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    📅 WEEKLY PERFORMANCE SUMMARY                  ║
║                    Week of {report['week_start']}                      ║
╚══════════════════════════════════════════════════════════════════╝

💰 TOTAL EARNINGS: ${report['total_earnings']:.2f}
📊 TOTAL SURVEYS: {report['total_surveys']}
📈 DAILY AVERAGE: ${report['average_daily']:.2f}
🚀 MONTHLY PROJECTION: ${report['projected_monthly']:.2f}

📊 DAILY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
        
        for day, earnings in report['daily_earnings'].items():
            bar = "█" * int(earnings / 10) if earnings > 0 else ""
            star = "⭐" if day == report['best_day'] else "  "
            print(f"{day:10} {star} ${earnings:6.2f} {bar}")
        
        # Progress toward goal
        weekly_goal = 2000
        progress = (report['total_earnings'] / weekly_goal) * 100
        
        print(f"""
🎯 GOAL PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal:      ${weekly_goal}/week
Current:   ${report['total_earnings']:.2f} ({progress:.1f}%)
Needed:    ${weekly_goal - report['total_earnings']:.2f}
""")
        
        if progress >= 100:
            print("🎉 WEEKLY GOAL ACHIEVED! 🎉")
        elif progress >= 75:
            print("🔥 Almost there! Keep pushing!")
        elif progress >= 50:
            print("💪 Halfway to goal! You got this!")
        else:
            print("📈 Building momentum...")
        
        print("\n" + "═" * 70 + "\n")
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    def save_session(self):
        """Save current session data"""
        if self.current_session_file:
            # Update totals
            self.session_data['totals'] = self.get_session_stats()
            
            with open(self.current_session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
    
    def load_historical_data(self):
        """Load all historical data for analysis"""
        self.historical_data = []
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.historical_data.append(data)
    
    def get_lifetime_stats(self) -> Dict:
        """Get all-time statistics"""
        
        all_surveys = []
        for session in self.historical_data:
            all_surveys.extend(session.get('surveys', []))
        
        if not all_surveys:
            return {'status': 'No historical data'}
        
        total_earnings = sum(s['earnings_usd'] for s in all_surveys)
        total_surveys = len(all_surveys)
        total_points = sum(s['points'] for s in all_surveys)
        
        # Find best day ever
        daily_earnings = {}
        for survey in all_surveys:
            date = datetime.fromtimestamp(survey['timestamp']).date()
            if date not in daily_earnings:
                daily_earnings[date] = 0
            daily_earnings[date] += survey['earnings_usd']
        
        best_day = max(daily_earnings.items(), key=lambda x: x[1]) if daily_earnings else (None, 0)
        
        return {
            'total_earnings': total_earnings,
            'total_surveys': total_surveys,
            'total_points': total_points,
            'best_day': best_day[0].strftime("%Y-%m-%d") if best_day[0] else None,
            'best_day_earnings': best_day[1],
            'days_active': len(daily_earnings)
        }


# Usage example for integration
if __name__ == "__main__":
    # Initialize reporting
    reporter = QuenitoReporting()
    
    # Start a session
    reporter.start_session("morning_grind")
    
    # Log a completed survey (call this after each survey)
    reporter.log_survey_completion(
        platform="MyOpinions",
        survey_id="MO_12345",
        topic="Consumer Products",
        points=150,
        duration_seconds=320,
        questions_total=15,
        questions_automated=12,
        vision_api_calls=8,
        pattern_matches=7
    )
    
    # Print reports
    reporter.print_session_report()
    reporter.print_weekly_summary()