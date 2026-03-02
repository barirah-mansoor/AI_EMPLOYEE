#!/usr/bin/env python3
"""
Platinum Slack Integration
Real-time Slack bot with AI capabilities
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    import yaml
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False

# Slack imports - optional
try:
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    App = None
    SocketModeHandler = None


class PlatinumSlackBot:
    """AI-powered Slack bot for Platinum Tier"""

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.config = self.load_config()
        self.client = anthropic.Anthropic() if DEPENDENCIES_OK else None
        self.app = None

        if SLACK_AVAILABLE and self.is_configured():
            self.initialize_slack_app()

    def load_config(self) -> Dict:
        """Load configuration"""
        config_file = self.vault / "Platinum_Tier/Configs/platinum_config.yaml"
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}

    def is_configured(self) -> bool:
        """Check if Slack is configured"""
        slack_config = self.config.get('integrations', {}).get('slack', {})
        return (
            slack_config.get('enabled', False) and
            slack_config.get('bot_token') and
            slack_config.get('signing_secret')
        )

    def initialize_slack_app(self):
        """Initialize Slack app with handlers"""
        slack_config = self.config.get('integrations', {}).get('slack', {})

        self.app = App(
            token=slack_config.get('bot_token'),
            signing_secret=slack_config.get('signing_secret')
        )

        self.register_commands()
        self.register_events()

    def register_commands(self):
        """Register slash commands"""
        if not self.app:
            return

        @self.app.command("/briefing")
        def handle_briefing(ack, command, respond):
            ack()
            briefing = self.generate_briefing()
            respond(briefing)

        @self.app.command("/tasks")
        def handle_tasks(ack, command, respond):
            ack()
            tasks = self.get_prioritized_tasks()
            respond(tasks)

        @self.app.command("/research")
        def handle_research(ack, command, respond):
            ack()
            topic = command.get('text', 'general')
            respond(f":mag_right: Researching: {topic}...")
            result = self.conduct_research(topic)
            respond(result)

        @self.app.command("/analytics")
        def handle_analytics(ack, command, respond):
            ack()
            analytics = self.get_analytics()
            respond(analytics)

        @self.app.command("/predict")
        def handle_predict(ack, command, respond):
            ack()
            prediction = self.get_prediction()
            respond(prediction)

    def register_events(self):
        """Register event handlers"""
        if not self.app:
            return

        @self.app.event("app_mention")
        def handle_mention(event, say):
            text = event.get('text', '')
            response = self.process_mention(text)
            say(response)

        @self.app.event("message")
        def handle_message(event, say):
            # Only respond in monitored channels
            channels = self.config.get('integrations', {}).get('slack', {}).get('channels', {})
            if event.get('channel') in channels.values():
                if self.should_respond(event):
                    response = self.generate_response(event.get('text', ''))
                    say(response)

    def should_respond(self, event: Dict) -> bool:
        """Determine if bot should respond"""
        # Don't respond to own messages
        if event.get('bot_id'):
            return False
        # Add more logic here
        return True

    def generate_briefing(self) -> str:
        """Generate Slack-formatted briefing"""
        try:
            from Gold_Tier.AI_Agents.email_agent import EmailAgent
            from Gold_Tier.AI_Agents.task_optimizer import TaskOptimizer

            email_agent = EmailAgent(str(self.vault))
            task_optimizer = TaskOptimizer(str(self.vault))

            email_results = email_agent.execute()
            task_results = task_optimizer.execute()

            processed = email_results.get('processed', 0) if email_results else 0
            auto_responded = email_results.get('auto_responded', 0) if email_results else 0
            total_tasks = task_results.get('workload_analysis', {}).get('stats', {}).get('total', 0) if task_results else 0

            briefing = f"""
*:sunrise: Morning Intelligence Briefing*

*:email: Email Status*
• Processed: {processed}
• Auto-responded: {auto_responded}
• Needs review: {email_results.get('queued_for_review', 0) if email_results else 0}

*:white_check_mark: Task Optimization*
• Total tasks: {total_tasks}
• High priority: {len(task_results.get('prioritized_tasks', {}).get('do_first', [])) if task_results else 0}

*:bulb: Top Actions Today*
1. Check queued emails
2. Review high-priority tasks
3. Prepare for meetings

_Full report: Dashboard.md_
"""
        except Exception as e:
            briefing = f":warning: Could not generate briefing: {e}"

        return briefing

    def get_prioritized_tasks(self) -> str:
        """Get prioritized task list"""
        try:
            from Gold_Tier.AI_Agents.task_optimizer import TaskOptimizer
            optimizer = TaskOptimizer(str(self.vault))
            results = optimizer.execute()

            do_first = results.get('prioritized_tasks', {}).get('do_first', [])

            tasks_text = "*:clipboard: Prioritized Tasks*\n\n"
            for i, task in enumerate(do_first[:5], 1):
                tasks_text += f"{i}. {task.get('subject', 'Unknown')}\n"

            return tasks_text
        except Exception as e:
            return f":warning: Could not get tasks: {e}"

    def conduct_research(self, topic: str) -> str:
        """Conduct research and return Slack-formatted result"""
        try:
            from Gold_Tier.AI_Agents.research_agent import ResearchAgent
            agent = ResearchAgent(str(self.vault))
            result = agent.execute(topic)

            summary = result.get('summary', 'No summary available')[:500]
            report_file = result.get('report_file', 'N/A')

            return f"""
*:mag_right: Research Complete: {topic}*

{summary}...

_Full report: {report_file}_
"""
        except Exception as e:
            return f":warning: Research failed: {e}"

    def get_analytics(self) -> str:
        """Get analytics summary"""
        try:
            from Gold_Tier.Analytics.Reports.Daily.daily_report_generator import generate_daily_report
            # Simplified analytics
            return """
*:chart_with_upwards_trend: Analytics Summary*

• Emails processed today: N/A
• Tasks completed: N/A
• Average response time: N/A
• Productivity score: N/A

_Detailed analytics in Platinum_Tier/Reports/_
"""
        except Exception as e:
            return f":warning: Could not get analytics: {e}"

    def get_prediction(self) -> str:
        """Get workload prediction"""
        try:
            from Platinum_Tier.Predictive.forecasting_engine import PredictiveEngine
            engine = PredictiveEngine(str(self.vault))
            forecast = engine.forecast_workload(7)

            return f"""
*:crystal_ball: 7-Day Forecast*

{json.dumps(forecast, indent=2)[:500]}...

_Full forecast in Platinum_Tier/Reports/Predictive/_
"""
        except Exception as e:
            return f":warning: Could not generate prediction: {e}"

    def process_mention(self, text: str) -> str:
        """Process @mention and generate response"""
        # Remove the bot mention
        clean_text = text.split('>', 1)[-1].strip() if '>' in text else text

        if self.client:
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    messages=[{"role": "user", "content": f"Respond briefly to: {clean_text}"}]
                )
                return response.content[0].text
            except:
                pass

        return f"I received your message: {clean_text}"

    def generate_response(self, text: str) -> str:
        """Generate AI response to message"""
        if not self.client:
            return "I'm here to help!"

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": f"Briefly respond to: {text}"}]
            )
            return response.content[0].text
        except:
            return "I'm processing your request."

    def start(self):
        """Start Slack bot"""
        if not SLACK_AVAILABLE:
            print("❌ Slack Bolt not installed. Run: pip install slack-bolt")
            return

        if not self.is_configured():
            print("❌ Slack not configured. Update platinum_config.yaml with your Slack credentials.")
            return

        if not self.app:
            print("❌ Slack app not initialized.")
            return

        slack_config = self.config.get('integrations', {}).get('slack', {})
        app_token = slack_config.get('app_token')

        if not app_token:
            print("❌ App token not found in config.")
            return

        print("💎 Platinum Slack Bot starting...")
        handler = SocketModeHandler(self.app, app_token)
        handler.start()


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    print("💎 Platinum Slack Integration")
    print("=" * 50)

    bot = PlatinumSlackBot(vault_path)

    if bot.is_configured():
        print("✅ Slack is configured")
        print("Starting bot...")
        bot.start()
    else:
        print("⚠️ Slack not configured")
        print("\nTo enable Slack integration:")
        print("1. Create a Slack app at https://api.slack.com/apps")
        print("2. Get your Bot User OAuth Token and Signing Secret")
        print("3. Update Platinum_Tier/Configs/platinum_config.yaml")
        print("\nRequired config:")
        print("""
integrations:
  slack:
    enabled: true
    bot_token: "xoxb-your-bot-token"
    signing_secret: "your-signing-secret"
    app_token: "xapp-your-app-token"
    channels:
      notifications: "CXXXXXXXX"
      commands: "CXXXXXXXX"
""")


if __name__ == "__main__":
    main()
