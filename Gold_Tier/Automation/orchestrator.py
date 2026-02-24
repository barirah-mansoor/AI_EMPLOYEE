#!/usr/bin/env python3
"""
Gold Tier Orchestrator - Automated workflow scheduling and execution
"""

import os
import sys
import json
import yaml
import signal
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Callable

# Try to import schedule
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "AI_Agents"))


class GoldOrchestrator:
    """Orchestrates automated Gold Tier workflows."""

    def __init__(self):
        self.vault_path = Path(__file__).parent.parent.parent
        self.config = self.load_config()
        self.workflows = self.load_workflows()
        self.running = False
        self.agents = {}
        self._setup_signal_handlers()

    def load_config(self) -> Dict[str, Any]:
        """Load Gold Tier configuration."""
        config_path = self.vault_path / "Gold_Tier" / "Configs" / "gold_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def load_workflows(self) -> Dict[str, Any]:
        """Load workflow configurations."""
        config_path = self.vault_path / "Gold_Tier" / "Configs" / "workflows_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("workflows", {})
        return {}

    def _setup_signal_handlers(self):
        """Setup graceful shutdown handlers."""
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def _shutdown(self, signum, frame):
        """Gracefully shutdown the orchestrator."""
        print("\n🛑 Shutting down Gold Tier Orchestrator...")
        self.running = False
        self._log_action("orchestrator_shutdown", {"signal": signum})
        sys.exit(0)

    def _log_action(self, action: str, details: Dict[str, Any] = None):
        """Log action to audit log."""
        log_dir = self.vault_path / "Gold_Tier" / "Logs" / "workflow_logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{today}.json"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "orchestrator": "gold",
            "action": action,
            "details": details or {}
        }

        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(entry)
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)

    def load_agent(self, agent_name: str):
        """Dynamically load an agent."""
        if agent_name in self.agents:
            return self.agents[agent_name]

        try:
            if agent_name == "email_agent":
                from email_agent import EmailAgent
                self.agents[agent_name] = EmailAgent()
            elif agent_name == "research_agent":
                from research_agent import ResearchAgent
                self.agents[agent_name] = ResearchAgent()
            elif agent_name == "meeting_agent":
                from meeting_agent import MeetingAgent
                self.agents[agent_name] = MeetingAgent()
            elif agent_name == "task_optimizer":
                from task_optimizer import TaskOptimizer
                self.agents[agent_name] = TaskOptimizer()
            else:
                return None
            return self.agents[agent_name]
        except Exception as e:
            print(f"⚠️  Failed to load {agent_name}: {e}")
            return None

    def execute_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Execute a named workflow."""
        workflow = self.workflows.get(workflow_name, {})
        if not workflow:
            return {"status": "error", "message": f"Workflow not found: {workflow_name}"}

        if not workflow.get("enabled", False):
            return {"status": "skipped", "message": f"Workflow disabled: {workflow_name}"}

        print(f"▶️  Executing workflow: {workflow_name}")
        self._log_action("workflow_start", {"workflow": workflow_name})

        results = []
        steps = workflow.get("steps", [])

        for step in steps:
            try:
                result = self._execute_step(step)
                results.append({"step": step, "result": result})
            except Exception as e:
                print(f"❌ Step failed: {step} - {e}")
                results.append({"step": step, "error": str(e)})

        self._log_action("workflow_complete", {
            "workflow": workflow_name,
            "steps_executed": len(results)
        })

        return {"status": "success", "workflow": workflow_name, "results": results}

    def _execute_step(self, step: str) -> Dict[str, Any]:
        """Execute a single workflow step."""
        print(f"  📋 Step: {step}")

        # Map steps to agent actions
        step_mapping = {
            "process_emails": lambda: self._run_email_agent("process_inbox"),
            "fetch_emails": lambda: self._run_email_agent("process_inbox"),
            "analyze_emails": lambda: self._run_email_agent("process_inbox"),
            "auto_respond": lambda: self._run_email_agent("process_inbox"),
            "analyze_calendar": lambda: self._run_meeting_agent("prepare"),
            "gather_context": lambda: self._run_meeting_agent("prepare"),
            "research_attendees": lambda: self._run_meeting_agent("prepare"),
            "generate_briefing": lambda: self._generate_briefing(),
            "optimize_tasks": lambda: self._run_task_optimizer("optimize"),
            "load_tasks": lambda: self._run_task_optimizer("optimize"),
            "apply_eisenhower": lambda: self._run_task_optimizer("matrix"),
            "optimize_schedule": lambda: self._run_task_optimizer("schedule"),
            "generate_recommendations": lambda: self._run_task_optimizer("optimize"),
            "collect_metrics": lambda: self._collect_analytics(),
            "analyze_trends": lambda: self._collect_analytics(),
            "generate_report": lambda: self._collect_analytics(),
        }

        handler = step_mapping.get(step)
        if handler:
            return handler()
        else:
            return {"status": "skipped", "message": f"Unknown step: {step}"}

    def _run_email_agent(self, action: str) -> Dict[str, Any]:
        """Run email agent."""
        agent = self.load_agent("email_agent")
        if agent:
            return agent.execute(action)
        return {"status": "error", "message": "Email agent unavailable"}

    def _run_meeting_agent(self, action: str) -> Dict[str, Any]:
        """Run meeting agent."""
        agent = self.load_agent("meeting_agent")
        if agent:
            return agent.execute(action)
        return {"status": "error", "message": "Meeting agent unavailable"}

    def _run_task_optimizer(self, action: str) -> Dict[str, Any]:
        """Run task optimizer."""
        agent = self.load_agent("task_optimizer")
        if agent:
            return agent.execute(action)
        return {"status": "error", "message": "Task optimizer unavailable"}

    def _generate_briefing(self) -> Dict[str, Any]:
        """Generate comprehensive morning briefing."""
        # Run email processing
        email_result = self._run_email_agent("process_inbox")

        # Run task optimization
        task_result = self._run_task_optimizer("optimize")

        # Create briefing document
        briefings_dir = self.vault_path / "Briefings"
        briefings_dir.mkdir(parents=True, exist_ok=True)

        briefing_path = briefings_dir / f"gold_briefing_{datetime.now().strftime('%Y%m%d')}.md"

        content = f"""# Gold Tier Morning Briefing

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Email Intelligence Summary
{self._format_email_summary(email_result)}

## Task Optimization
{self._format_task_summary(task_result)}

## Recommended Actions
- Review urgent emails
- Complete high-priority tasks first
- Protect deep work time blocks

---
*Generated by Gold Tier Orchestrator*
"""
        briefing_path.write_text(content)

        return {"status": "success", "briefing_file": str(briefing_path)}

    def _format_email_summary(self, result: Dict[str, Any]) -> str:
        """Format email results for briefing."""
        if result.get("status") == "success":
            count = len(result.get("processed_emails", []))
            return f"Processed {count} emails requiring attention"
        return "No new emails processed"

    def _format_task_summary(self, result: Dict[str, Any]) -> str:
        """Format task results for briefing."""
        if result.get("status") == "success":
            report = result.get("report", {})
            count = report.get("tasks_analyzed", 0)
            return f"Analyzed {count} tasks, generated optimization recommendations"
        return "No tasks to optimize"

    def _collect_analytics(self) -> Dict[str, Any]:
        """Collect and save analytics."""
        analytics_dir = self.vault_path / "Gold_Tier" / "Analytics" / "Reports" / "Daily"
        analytics_dir.mkdir(parents=True, exist_ok=True)

        report = {
            "timestamp": datetime.now().isoformat(),
            "emails_processed": self._count_processed("email"),
            "tasks_analyzed": self._count_processed("task"),
            "briefings_generated": self._count_processed("briefing"),
            "workflows_executed": self._count_processed("workflow")
        }

        report_path = analytics_dir / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        return {"status": "success", "report": report}

    def _count_processed(self, type_name: str) -> int:
        """Count processed items of a type."""
        log_dir = self.vault_path / "Gold_Tier" / "Logs" / "workflow_logs"
        if not log_dir.exists():
            return 0

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{today}.json"

        if not log_file.exists():
            return 0

        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            return sum(1 for log in logs if type_name in log.get("action", "").lower())
        except:
            return 0

    def register_schedules(self):
        """Register all workflow schedules."""
        if not SCHEDULE_AVAILABLE:
            print("⚠️  Schedule library not available. Running in manual mode.")
            return

        for name, workflow in self.workflows.items():
            if not workflow.get("enabled", False):
                continue

            trigger = workflow.get("trigger", {})
            trigger_type = trigger.get("type")

            def make_job(n):
                return lambda: self.execute_workflow(n)

            if trigger_type == "schedule":
                time_str = trigger.get("time", "09:00")
                schedule.every().day.at(time_str).do(make_job(name))
                print(f"📅 Scheduled '{name}' at {time_str}")

            elif trigger_type == "interval":
                minutes = trigger.get("minutes", 60)
                schedule.every(minutes).minutes.do(make_job(name))
                print(f"⏰ Scheduled '{name}' every {minutes} minutes")

    def run(self):
        """Main orchestrator loop."""
        print("🥇 Gold Tier Orchestrator Starting...")
        print("=" * 50)

        # Register all schedules
        self.register_schedules()

        # Run initial briefing
        print("\n📊 Running initial briefing...")
        self._generate_briefing()

        if SCHEDULE_AVAILABLE:
            # Start scheduled loop
            self.running = True
            print("\n✅ Orchestrator running. Press Ctrl+C to stop.")
            print("-" * 50)

            while self.running:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
        else:
            print("\n✅ Initial setup complete. Schedule library needed for continuous operation.")


def main():
    """Main entry point."""
    orchestrator = GoldOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
