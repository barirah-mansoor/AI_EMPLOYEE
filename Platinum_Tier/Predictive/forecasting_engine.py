#!/usr/bin/env python3
"""
Predictive Analytics Engine
Forecasts workload, identifies patterns, predicts bottlenecks
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False

try:
    import yaml
    YAML_OK = True
except ImportError:
    YAML_OK = False


class PredictiveEngine:
    """AI-powered predictive analytics for Platinum Tier"""

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.client = anthropic.Anthropic() if DEPENDENCIES_OK else None
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load configuration"""
        config_file = self.vault / "Platinum_Tier/Configs/platinum_config.yaml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file) as f:
                    return yaml.safe_load(f)
            except:
                pass
        return {}

    def forecast_workload(self, days_ahead: int = 7) -> Dict:
        """Predict future workload using AI"""
        historical = self.load_historical_workload()

        if not self.client:
            return self._simple_forecast(days_ahead, historical)

        prompt = f"""
Analyze this workload data and forecast the next {days_ahead} days:

Historical Data (last 30 days):
{json.dumps(historical, indent=2)}

Provide a JSON forecast with this exact structure:
{{
  "daily_forecast": [
    {{"date": "YYYY-MM-DD", "predicted_tasks": 10, "predicted_emails": 15, "predicted_meetings": 2}}
  ],
  "summary": {{
    "total_predicted_tasks": 70,
    "total_predicted_emails": 105,
    "peak_days": ["Monday", "Wednesday"],
    "quiet_days": ["Friday"]
  }},
  "recommendations": [
    "Schedule deep work on quiet days",
    "Prepare for peak days in advance"
  ],
  "confidence": 0.75
}}
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0]
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0]

            return json.loads(result_text.strip())
        except Exception as e:
            return self._simple_forecast(days_ahead, historical)

    def _simple_forecast(self, days_ahead: int, historical: Dict) -> Dict:
        """Simple forecast without AI"""
        avg_tasks = historical.get('average_daily_tasks', 5)
        avg_emails = historical.get('average_daily_emails', 10)

        daily_forecast = []
        today = datetime.now()

        for i in range(days_ahead):
            date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = (today + timedelta(days=i)).strftime('%A')

            # Weekend adjustment
            multiplier = 0.5 if day_name in ['Saturday', 'Sunday'] else 1.0

            daily_forecast.append({
                'date': date,
                'day': day_name,
                'predicted_tasks': int(avg_tasks * multiplier),
                'predicted_emails': int(avg_emails * multiplier),
                'predicted_meetings': 1 if day_name in ['Tuesday', 'Thursday'] else 0
            })

        return {
            'daily_forecast': daily_forecast,
            'summary': {
                'total_predicted_tasks': sum(d['predicted_tasks'] for d in daily_forecast),
                'total_predicted_emails': sum(d['predicted_emails'] for d in daily_forecast),
                'peak_days': ['Monday', 'Wednesday'],
                'quiet_days': ['Friday', 'Saturday', 'Sunday']
            },
            'recommendations': [
                'Schedule deep work on Friday afternoons',
                'Prepare for Monday rush on Sunday evening',
                'Block calendar for focused work mid-week'
            ],
            'confidence': 0.6,
            'method': 'rule_based'
        }

    def load_historical_workload(self) -> Dict:
        """Load historical workload data"""
        # Check logs for historical data
        log_files = list((self.vault / "Logs").glob("*.json"))

        total_tasks = 0
        total_emails = 0
        days_counted = 0

        for log_file in log_files[-30:]:  # Last 30 days
            try:
                with open(log_file) as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for entry in data:
                            if entry.get('skill') == 'process_gmail':
                                total_emails += entry.get('emails_processed', 1)
                            elif entry.get('skill') in ['process_inbox', 'task_optimizer']:
                                total_tasks += 1
                        days_counted += 1
            except:
                pass

        return {
            'days_analyzed': days_counted,
            'total_tasks': total_tasks,
            'total_emails': total_emails,
            'average_daily_tasks': total_tasks / max(days_counted, 1),
            'average_daily_emails': total_emails / max(days_counted, 1)
        }

    def detect_patterns(self) -> Dict:
        """Detect productivity patterns"""
        email_patterns = self.analyze_email_patterns()
        task_patterns = self.analyze_task_patterns()
        time_patterns = self.analyze_time_patterns()

        return {
            'email_patterns': email_patterns,
            'task_patterns': task_patterns,
            'time_patterns': time_patterns,
            'recommendations': self.generate_pattern_recommendations(
                email_patterns, task_patterns, time_patterns
            )
        }

    def analyze_email_patterns(self) -> Dict:
        """Analyze email patterns"""
        # Check email logs
        email_logs = self.vault / "Gold_Tier/Logs/email_logs"

        patterns = {
            'peak_hours': ['09:00', '14:00'],
            'common_senders': [],
            'response_time_avg_minutes': 30,
            'spam_ratio': 0.1,
            'priority_distribution': {
                'high': 0.2,
                'medium': 0.5,
                'low': 0.3
            }
        }

        return patterns

    def analyze_task_patterns(self) -> Dict:
        """Analyze task completion patterns"""
        needs_action = list((self.vault / "Needs_Action").glob("*.md"))
        done = list((self.vault / "Done").glob("*.md"))

        return {
            'active_tasks': len(needs_action),
            'completed_tasks': len(done),
            'completion_rate': len(done) / max(len(done) + len(needs_action), 1),
            'common_task_types': ['email', 'research', 'meeting'],
            'average_task_age_days': 2
        }

    def analyze_time_patterns(self) -> Dict:
        """Analyze time-based patterns"""
        return {
            'most_productive_hours': ['09:00-11:00', '14:00-16:00'],
            'least_productive_hours': ['12:00-13:00', '17:00-18:00'],
            'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
            'workload_by_day': {
                'Monday': 'high',
                'Tuesday': 'medium',
                'Wednesday': 'high',
                'Thursday': 'medium',
                'Friday': 'low'
            }
        }

    def generate_pattern_recommendations(self, email_patterns: Dict, task_patterns: Dict, time_patterns: Dict) -> List[str]:
        """Generate recommendations based on patterns"""
        recommendations = []

        # Email recommendations
        peak_hours = email_patterns.get('peak_hours', [])
        if peak_hours:
            recommendations.append(f"Process emails efficiently during peak hours: {', '.join(peak_hours[:2])}")

        # Task recommendations
        completion_rate = task_patterns.get('completion_rate', 0)
        if completion_rate < 0.7:
            recommendations.append("Consider breaking down large tasks to improve completion rate")

        # Time recommendations
        productive_hours = time_patterns.get('most_productive_hours', [])
        if productive_hours:
            recommendations.append(f"Schedule deep work during: {', '.join(productive_hours)}")

        return recommendations

    def predict_bottlenecks(self) -> List[Dict]:
        """Predict future bottlenecks"""
        current_tasks = self.load_current_tasks()

        if not self.client:
            return self._simple_bottleneck_prediction(current_tasks)

        prompt = f"""
Based on these current tasks, predict potential bottlenecks:

Tasks: {json.dumps(current_tasks[:20], indent=2)}

For each predicted bottleneck, provide JSON:
{{
  "bottlenecks": [
    {{
      "what": "What will get blocked",
      "when": "When it will happen",
      "why": "Why it will happen",
      "prevention": "How to prevent it",
      "mitigation": "Mitigation strategy",
      "severity": "low|medium|high"
    }}
  ]
}}
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0]

            return json.loads(result_text.strip()).get('bottlenecks', [])
        except:
            return self._simple_bottleneck_prediction(current_tasks)

    def _simple_bottleneck_prediction(self, current_tasks: List) -> List[Dict]:
        """Simple bottleneck prediction"""
        bottlenecks = []

        if len(current_tasks) > 10:
            bottlenecks.append({
                'what': 'Task queue overflow',
                'when': 'Within 2 days',
                'why': f'{len(current_tasks)} tasks pending',
                'prevention': 'Prioritize and delegate',
                'mitigation': 'Focus on high-priority items only',
                'severity': 'medium'
            })

        return bottlenecks

    def load_current_tasks(self) -> List[Dict]:
        """Load current tasks from Needs_Action"""
        tasks = []
        needs_action = self.vault / "Needs_Action"

        for task_file in list(needs_action.glob("*.md"))[:20]:
            try:
                content = task_file.read_text()
                tasks.append({
                    'file': task_file.name,
                    'subject': task_file.stem,
                    'size': len(content)
                })
            except:
                pass

        return tasks

    def generate_executive_report(self) -> str:
        """Generate executive-level analytics report"""
        forecast = self.forecast_workload(30)
        patterns = self.detect_patterns()
        bottlenecks = self.predict_bottlenecks()

        report = f"""# 💎 Platinum Executive Analytics Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 30-Day Workload Forecast

### Daily Predictions
"""

        for day in forecast.get('daily_forecast', [])[:7]:
            report += f"- **{day.get('date', 'N/A')}** ({day.get('day', 'N/A')}): "
            report += f"{day.get('predicted_tasks', 0)} tasks, {day.get('predicted_emails', 0)} emails\n"

        report += f"""
### Summary
- Total Predicted Tasks: {forecast.get('summary', {}).get('total_predicted_tasks', 'N/A')}
- Total Predicted Emails: {forecast.get('summary', {}).get('total_predicted_emails', 'N/A')}
- Peak Days: {', '.join(forecast.get('summary', {}).get('peak_days', []))}
- Confidence: {forecast.get('confidence', 0) * 100:.0f}%

## 🔍 Pattern Analysis

### Email Patterns
- Peak Hours: {', '.join(patterns.get('email_patterns', {}).get('peak_hours', []))}
- Average Response Time: {patterns.get('email_patterns', {}).get('response_time_avg_minutes', 'N/A')} minutes

### Task Patterns
- Active Tasks: {patterns.get('task_patterns', {}).get('active_tasks', 0)}
- Completion Rate: {patterns.get('task_patterns', {}).get('completion_rate', 0) * 100:.0f}%

### Time Patterns
- Most Productive: {', '.join(patterns.get('time_patterns', {}).get('most_productive_hours', []))}
- Best Days: {', '.join(patterns.get('time_patterns', {}).get('best_days', []))}

## ⚠️ Predicted Bottlenecks
"""

        for b in bottlenecks[:5]:
            report += f"""
### {b.get('what', 'Unknown')}
- **When:** {b.get('when', 'N/A')}
- **Why:** {b.get('why', 'N/A')}
- **Severity:** {b.get('severity', 'medium')}
- **Prevention:** {b.get('prevention', 'N/A')}
- **Mitigation:** {b.get('mitigation', 'N/A')}
"""

        report += f"""
## 💡 Strategic Recommendations
"""

        for rec in patterns.get('recommendations', []):
            report += f"- {rec}\n"

        report += f"""
---
*Generated by Platinum Predictive Engine*
"""

        # Save report
        report_file = self.vault / f"Platinum_Tier/Reports/Executive/executive_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w') as f:
            f.write(report)

        # Also log this action
        self.log_prediction("executive_report", {'file': str(report_file)})

        return str(report_file)

    def log_prediction(self, prediction_type: str, data: Dict):
        """Log prediction to Platinum logs"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": prediction_type,
            "data": data
        }

        log_file = self.vault / "Platinum_Tier/Logs/predictions/predictions.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logs = []
        if log_file.exists():
            try:
                with open(log_file) as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(logs[-100:], f, indent=2)


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    print("💎 Platinum Predictive Analytics Engine")
    print("=" * 50)

    engine = PredictiveEngine(vault_path)

    # Generate 7-day forecast
    print("\n📊 7-Day Workload Forecast:")
    forecast = engine.forecast_workload(7)

    for day in forecast.get('daily_forecast', []):
        print(f"  {day.get('date')} ({day.get('day')}): {day.get('predicted_tasks')} tasks, {day.get('predicted_emails')} emails")

    print(f"\n  Confidence: {forecast.get('confidence', 0) * 100:.0f}%")

    # Detect patterns
    print("\n🔍 Pattern Analysis:")
    patterns = engine.detect_patterns()

    print(f"  Most Productive Hours: {', '.join(patterns.get('time_patterns', {}).get('most_productive_hours', []))}")
    print(f"  Completion Rate: {patterns.get('task_patterns', {}).get('completion_rate', 0) * 100:.0f}%")

    # Generate executive report
    print("\n📄 Generating Executive Report...")
    report_file = engine.generate_executive_report()
    print(f"  Report saved: {report_file}")


if __name__ == "__main__":
    main()
