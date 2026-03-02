#!/usr/bin/env python3
"""
Platinum Learning System
Self-learning capabilities for continuous improvement
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


class LearningSystem:
    """
    Self-learning system that:
    - Tracks performance metrics
    - Learns from user feedback
    - Adapts to user preferences
    - Improves over time
    """

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.client = anthropic.Anthropic() if DEPENDENCIES_OK else None
        self.learning_file = self.vault / "Platinum_Tier/Learning/learning_data.json"
        self.feedback_file = self.vault / "Platinum_Tier/Learning/feedback_loops/feedback.json"

    def record_feedback(self, action_type: str, action_data: Dict, user_feedback: str, rating: int = 3):
        """
        Record user feedback for learning

        Args:
            action_type: Type of action (email, research, task, etc.)
            action_data: Data about the action taken
            user_feedback: User's text feedback
            rating: 1-5 rating (1=bad, 5=excellent)
        """
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "action_data": action_data,
            "user_feedback": user_feedback,
            "rating": rating
        }

        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)

        feedbacks = []
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file) as f:
                    feedbacks = json.load(f)
            except:
                feedbacks = []

        feedbacks.append(feedback_entry)

        with open(self.feedback_file, 'w') as f:
            json.dump(feedbacks[-500:], f, indent=2)  # Keep last 500

        # Trigger learning update
        self._update_learning_model(action_type, rating)

    def _update_learning_model(self, action_type: str, rating: int):
        """Update learning model based on feedback"""
        learning_data = self.load_learning_data()

        if 'action_ratings' not in learning_data:
            learning_data['action_ratings'] = {}

        if action_type not in learning_data['action_ratings']:
            learning_data['action_ratings'][action_type] = {
                'total': 0,
                'sum': 0,
                'average': 0
            }

        stats = learning_data['action_ratings'][action_type]
        stats['total'] += 1
        stats['sum'] += rating
        stats['average'] = stats['sum'] / stats['total']
        stats['last_updated'] = datetime.now().isoformat()

        self.save_learning_data(learning_data)

    def load_learning_data(self) -> Dict:
        """Load learning data"""
        if self.learning_file.exists():
            try:
                with open(self.learning_file) as f:
                    return json.load(f)
            except:
                pass

        return {
            'created': datetime.now().isoformat(),
            'action_ratings': {},
            'user_preferences': {},
            'patterns': {},
            'improvements': []
        }

    def save_learning_data(self, data: Dict):
        """Save learning data"""
        self.learning_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.learning_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_action_confidence(self, action_type: str) -> float:
        """Get confidence level for an action type based on past ratings"""
        learning_data = self.load_learning_data()
        stats = learning_data.get('action_ratings', {}).get(action_type, {})
        return stats.get('average', 3.0) / 5.0  # Normalize to 0-1

    def learn_user_preference(self, category: str, preference: str, value: any):
        """Learn a user preference"""
        learning_data = self.load_learning_data()

        if 'user_preferences' not in learning_data:
            learning_data['user_preferences'] = {}

        if category not in learning_data['user_preferences']:
            learning_data['user_preferences'][category] = {}

        learning_data['user_preferences'][category][preference] = {
            'value': value,
            'learned_at': datetime.now().isoformat()
        }

        self.save_learning_data(learning_data)

    def get_user_preference(self, category: str, preference: str, default=None):
        """Get learned user preference"""
        learning_data = self.load_learning_data()
        pref_data = learning_data.get('user_preferences', {}).get(category, {}).get(preference, {})
        return pref_data.get('value', default)

    def analyze_patterns(self) -> Dict:
        """Analyze patterns from feedback and usage"""
        feedbacks = []
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file) as f:
                    feedbacks = json.load(f)
            except:
                pass

        patterns = {
            'total_feedbacks': len(feedbacks),
            'average_rating': 0,
            'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'action_performance': {},
            'trends': []
        }

        if feedbacks:
            ratings = [f.get('rating', 3) for f in feedbacks]
            patterns['average_rating'] = sum(ratings) / len(ratings)

            for r in ratings:
                patterns['rating_distribution'][r] = patterns['rating_distribution'].get(r, 0) + 1

            # Calculate per-action performance
            action_ratings = {}
            for f in feedbacks:
                action = f.get('action_type', 'unknown')
                if action not in action_ratings:
                    action_ratings[action] = []
                action_ratings[action].append(f.get('rating', 3))

            for action, ratings in action_ratings.items():
                patterns['action_performance'][action] = {
                    'average': sum(ratings) / len(ratings),
                    'count': len(ratings)
                }

        return patterns

    def generate_improvement_suggestions(self) -> List[str]:
        """Generate suggestions for improvement based on learning"""
        patterns = self.analyze_patterns()
        suggestions = []

        # Check for low-rated actions
        for action, stats in patterns.get('action_performance', {}).items():
            if stats['average'] < 3.0:
                suggestions.append(f"Improve {action} handling (avg rating: {stats['average']:.1f})")

        # Check overall rating
        if patterns['average_rating'] < 3.5:
            suggestions.append("Overall satisfaction is below optimal - review recent feedback")

        # Add general suggestions
        if patterns['total_feedbacks'] < 10:
            suggestions.append("Collect more feedback for better learning")

        return suggestions

    def get_learning_report(self) -> str:
        """Generate learning report"""
        patterns = self.analyze_patterns()
        suggestions = self.generate_improvement_suggestions()
        learning_data = self.load_learning_data()

        report = f"""# 🧠 Platinum Learning Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 Feedback Analysis

- **Total Feedback Entries:** {patterns['total_feedbacks']}
- **Average Rating:** {patterns['average_rating']:.2f}/5.0

### Rating Distribution
"""

        for rating, count in sorted(patterns['rating_distribution'].items()):
            bar = '█' * (count // 2) if count > 0 else ''
            report += f"  {rating}★: {bar} ({count})\n"

        report += "\n### Action Performance\n"
        for action, stats in patterns.get('action_performance', {}).items():
            emoji = '✅' if stats['average'] >= 4.0 else '⚠️' if stats['average'] >= 3.0 else '❌'
            report += f"  {emoji} {action}: {stats['average']:.2f}/5.0 ({stats['count']} ratings)\n"

        report += "\n## 👤 Learned Preferences\n"
        for category, prefs in learning_data.get('user_preferences', {}).items():
            report += f"\n### {category.title()}\n"
            for pref, data in prefs.items():
                report += f"  • {pref}: {data.get('value')}\n"

        if suggestions:
            report += "\n## 💡 Improvement Suggestions\n"
            for s in suggestions:
                report += f"  • {s}\n"

        report += "\n---\n*Generated by Platinum Learning System*\n"

        # Save report
        report_file = self.vault / f"Platinum_Tier/Reports/Performance/learning_{datetime.now().strftime('%Y%m%d')}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)

        return report


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    learning = LearningSystem(vault_path)

    print("🧠 Platinum Learning System")
    print("=" * 50)

    # Generate learning report
    report = learning.get_learning_report()
    print(report)


if __name__ == "__main__":
    main()
