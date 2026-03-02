#!/usr/bin/env python3
"""
Natural Language Command Processor
Process commands in plain English
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False


class NLPCommandProcessor:
    """Process natural language commands into structured actions"""

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.client = anthropic.Anthropic() if DEPENDENCIES_OK else None
        self.conversation_history = []
        self.command_handlers = {
            'email': self.handle_email_command,
            'research': self.handle_research_command,
            'task': self.handle_task_command,
            'meeting': self.handle_meeting_command,
            'analytics': self.handle_analytics_command,
            'predict': self.handle_predict_command,
            'system': self.handle_system_command,
            'help': self.handle_help_command
        }

    def process_command(self, natural_language: str) -> Dict:
        """Convert natural language to structured command using AI"""
        if not self.client:
            return self._rule_based_parse(natural_language)

        prompt = f"""
Convert this natural language command into a structured action:

User said: "{natural_language}"

Return JSON with this exact structure:
{{
  "intent": "email|research|task|meeting|analytics|predict|system|help|other",
  "action": "specific action to take",
  "parameters": {{}},
  "confidence": 0.95,
  "clarification_needed": false,
  "suggested_followup": "",
  "reasoning": "Brief explanation of interpretation"
}}

Examples:
- "check my emails" → intent: "email", action: "process_emails", parameters: {{}}
- "research AI trends" → intent: "research", action: "deep_research", parameters: {{"topic": "AI trends"}}
- "what are my top tasks" → intent: "task", action: "get_priorities", parameters: {{}}
- "schedule a meeting tomorrow" → intent: "meeting", action: "schedule", parameters: {{"when": "tomorrow"}}
- "show me analytics" → intent: "analytics", action: "show_report", parameters: {{}}
- "predict my workload" → intent: "predict", action: "forecast", parameters: {{}}
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0]
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0]

            return json.loads(result_text.strip())
        except Exception as e:
            return self._rule_based_parse(natural_language)

    def _rule_based_parse(self, text: str) -> Dict:
        """Rule-based command parsing fallback"""
        text_lower = text.lower()

        # Email patterns
        if any(word in text_lower for word in ['email', 'mail', 'inbox', 'gmail']):
            return {
                'intent': 'email',
                'action': 'process_emails',
                'parameters': {},
                'confidence': 0.8,
                'clarification_needed': False
            }

        # Research patterns
        if any(word in text_lower for word in ['research', 'find info', 'look up', 'search']):
            topic = text_lower.replace('research', '').replace('find info about', '').replace('look up', '').strip()
            return {
                'intent': 'research',
                'action': 'deep_research',
                'parameters': {'topic': topic or 'general'},
                'confidence': 0.8,
                'clarification_needed': False
            }

        # Task patterns
        if any(word in text_lower for word in ['task', 'todo', 'prioritize', 'what do i need to do']):
            return {
                'intent': 'task',
                'action': 'get_priorities',
                'parameters': {},
                'confidence': 0.8,
                'clarification_needed': False
            }

        # Meeting patterns
        if any(word in text_lower for word in ['meeting', 'schedule', 'calendar', 'appointment']):
            return {
                'intent': 'meeting',
                'action': 'check_schedule',
                'parameters': {},
                'confidence': 0.7,
                'clarification_needed': True,
                'suggested_followup': 'What time would you like to schedule the meeting?'
            }

        # Analytics patterns
        if any(word in text_lower for word in ['analytics', 'report', 'stats', 'metrics', 'performance']):
            return {
                'intent': 'analytics',
                'action': 'show_report',
                'parameters': {},
                'confidence': 0.8,
                'clarification_needed': False
            }

        # Predict patterns
        if any(word in text_lower for word in ['predict', 'forecast', 'future', 'upcoming']):
            return {
                'intent': 'predict',
                'action': 'forecast',
                'parameters': {},
                'confidence': 0.8,
                'clarification_needed': False
            }

        # Help patterns
        if any(word in text_lower for word in ['help', 'what can you do', 'commands']):
            return {
                'intent': 'help',
                'action': 'show_help',
                'parameters': {},
                'confidence': 0.9,
                'clarification_needed': False
            }

        # Default
        return {
            'intent': 'other',
            'action': 'unknown',
            'parameters': {},
            'confidence': 0.5,
            'clarification_needed': True,
            'suggested_followup': 'Could you clarify what you\'d like me to do?'
        }

    def execute_command(self, command: Dict) -> Dict:
        """Execute the structured command"""
        intent = command.get('intent', 'other')
        action = command.get('action')
        params = command.get('parameters', {})

        handler = self.command_handlers.get(intent)
        if handler:
            return handler(action, params)
        else:
            return {
                'success': False,
                'message': f"Unknown intent: {intent}",
                'suggestion': "Type 'help' to see available commands"
            }

    def handle_email_command(self, action: str, params: Dict) -> Dict:
        """Handle email-related commands"""
        try:
            if action in ['process_emails', 'check_emails', 'process']:
                from Silver_Tier.silver_process_inbox import SilverInboxProcessor
                processor = SilverInboxProcessor(str(self.vault))
                result = processor.execute()
                return {
                    'success': True,
                    'message': f"Processed emails successfully",
                    'details': result
                }
            elif action in ['send', 'send_emails']:
                from Silver_Tier.silver_send_emails import SilverEmailSender
                sender = SilverEmailSender(str(self.vault))
                result = sender.execute()
                return {
                    'success': True,
                    'message': "Emails sent successfully",
                    'details': result
                }
            else:
                return {
                    'success': False,
                    'message': f"Unknown email action: {action}"
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error processing email command: {str(e)}"
            }

    def handle_research_command(self, action: str, params: Dict) -> Dict:
        """Handle research-related commands"""
        try:
            from Gold_Tier.AI_Agents.research_agent import ResearchAgent
            agent = ResearchAgent(str(self.vault))
            topic = params.get('topic', 'general research')
            result = agent.execute(topic)

            return {
                'success': True,
                'message': f"Research completed on: {topic}",
                'details': result,
                'report_file': result.get('report_file')
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error conducting research: {str(e)}"
            }

    def handle_task_command(self, action: str, params: Dict) -> Dict:
        """Handle task-related commands"""
        try:
            from Gold_Tier.AI_Agents.task_optimizer import TaskOptimizer
            optimizer = TaskOptimizer(str(self.vault))
            result = optimizer.execute()

            do_first = result.get('prioritized_tasks', {}).get('do_first', [])

            return {
                'success': True,
                'message': f"Top priority tasks retrieved",
                'tasks': do_first[:5],
                'details': result
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error getting tasks: {str(e)}"
            }

    def handle_meeting_command(self, action: str, params: Dict) -> Dict:
        """Handle meeting-related commands"""
        try:
            from Gold_Tier.AI_Agents.meeting_agent import MeetingAgent
            agent = MeetingAgent(str(self.vault))
            result = agent.execute()

            return {
                'success': True,
                'message': "Meeting preparation completed",
                'details': result
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error with meeting command: {str(e)}"
            }

    def handle_analytics_command(self, action: str, params: Dict) -> Dict:
        """Handle analytics-related commands"""
        try:
            from Gold_Tier.AI_Agents.task_optimizer import TaskOptimizer
            optimizer = TaskOptimizer(str(self.vault))
            result = optimizer.execute()

            return {
                'success': True,
                'message': "Analytics retrieved",
                'workload_analysis': result.get('workload_analysis'),
                'recommendations': result.get('recommendations')
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error getting analytics: {str(e)}"
            }

    def handle_predict_command(self, action: str, params: Dict) -> Dict:
        """Handle prediction-related commands"""
        try:
            from Platinum_Tier.Predictive.forecasting_engine import PredictiveEngine
            engine = PredictiveEngine(str(self.vault))
            forecast = engine.forecast_workload(7)

            return {
                'success': True,
                'message': "7-day forecast generated",
                'forecast': forecast
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error generating forecast: {str(e)}"
            }

    def handle_system_command(self, action: str, params: Dict) -> Dict:
        """Handle system-related commands"""
        if action == 'status':
            return {
                'success': True,
                'message': "System status",
                'status': {
                    'vault': str(self.vault),
                    'dependencies_ok': DEPENDENCIES_OK
                }
            }
        else:
            return {
                'success': False,
                'message': f"Unknown system action: {action}"
            }

    def handle_help_command(self, action: str, params: Dict) -> Dict:
        """Show help information"""
        help_text = """
💎 PLATINUM AI ASSISTANT - Available Commands

📧 EMAIL COMMANDS:
  • "check my emails" - Process inbox
  • "send pending emails" - Send approved emails
  • "email summary" - Get email overview

🔍 RESEARCH COMMANDS:
  • "research [topic]" - Deep research on topic
  • "find info about [topic]" - Quick search

📋 TASK COMMANDS:
  • "what are my tasks" - Show prioritized tasks
  • "prioritize my work" - Run task optimizer
  • "show me my top priorities" - Top 5 tasks

📅 MEETING COMMANDS:
  • "prepare for meetings" - Meeting preparation
  • "check my schedule" - View calendar

📊 ANALYTICS COMMANDS:
  • "show analytics" - Performance metrics
  • "how am I doing" - Productivity summary

🔮 PREDICTIVE COMMANDS:
  • "predict my workload" - 7-day forecast
  • "what's coming up" - Upcoming predictions

⚙️ SYSTEM COMMANDS:
  • "system status" - Check system health
  • "help" - Show this help message

Just type naturally - I understand plain English!
"""
        return {
            'success': True,
            'message': help_text
        }

    def chat_interface(self):
        """Interactive chat interface"""
        print("\n" + "=" * 50)
        print("💎 PLATINUM AI ASSISTANT")
        print("=" * 50)
        print("Type naturally - I understand plain English!")
        print("Type 'exit' or 'quit' to end session\n")

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\nAssistant: Goodbye! Have a productive day! 💎")
                    break

                # Process command
                command = self.process_command(user_input)

                # Store in history
                self.conversation_history.append({
                    'user': user_input,
                    'command': command,
                    'timestamp': datetime.now().isoformat()
                })

                # Check if clarification needed
                if command.get('clarification_needed'):
                    print(f"\nAssistant: {command.get('suggested_followup', 'Could you clarify?')}")
                    continue

                # Execute command
                result = self.execute_command(command)

                # Display result
                print(f"\nAssistant: {result.get('message', 'Done!')}")

                # Show additional details if available
                if result.get('tasks'):
                    print("\n📋 Your Top Tasks:")
                    for i, task in enumerate(result.get('tasks', [])[:5], 1):
                        print(f"  {i}. {task.get('subject', task.get('description', str(task)))}")

                if result.get('forecast'):
                    forecast = result.get('forecast')
                    print("\n🔮 7-Day Forecast:")
                    for day in forecast.get('daily_forecast', [])[:5]:
                        print(f"  • {day.get('date')} ({day.get('day')}): {day.get('predicted_tasks')} tasks")

                if result.get('report_file'):
                    print(f"\n📄 Report saved: {result.get('report_file')}")

            except KeyboardInterrupt:
                print("\n\nAssistant: Session ended. Goodbye!")
                break
            except Exception as e:
                print(f"\nAssistant: Sorry, I encountered an error: {str(e)}")
                print("Please try again or type 'help' for available commands.")


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    processor = NLPCommandProcessor(vault_path)
    processor.chat_interface()


if __name__ == "__main__":
    main()
