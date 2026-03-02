#!/usr/bin/env python3
"""
Task Optimizer Agent - AI-powered task prioritization and scheduling
"""

import os
import json
import re
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import defaultdict

# Import base agent
import sys
sys.path.insert(0, str(Path(__file__).parent))
from base_agent import BaseAgent


class TaskOptimizer(BaseAgent):
    """AI-powered task optimization agent."""

    def __init__(self):
        super().__init__("task_optimizer")
        self.agent_config = self._load_agent_config()

    def _load_agent_config(self) -> Dict[str, Any]:
        """Load agent-specific configuration."""
        config_path = self.vault_path / "Gold_Tier" / "Configs" / "agents_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("agents", {}).get("task_optimizer", {})
        return {"enabled": True, "optimization_frequency": "hourly"}

    def load_all_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from all sources in the vault."""
        tasks = []

        # Load from Needs_Action folder
        needs_action = self.vault_path / "Needs_Action"
        if needs_action.exists():
            for task_file in needs_action.glob("*.md"):
                content = task_file.read_text()
                tasks.append({
                    "source": "Needs_Action",
                    "file": str(task_file.name),
                    "content": content,
                    "created": datetime.fromtimestamp(task_file.stat().st_ctime).isoformat()
                })

        # Load from Plans folder
        plans_dir = self.vault_path / "Plans"
        if plans_dir.exists():
            for plan_file in plans_dir.glob("*.md"):
                content = plan_file.read_text()
                tasks.append({
                    "source": "Plans",
                    "file": str(plan_file.name),
                    "content": content,
                    "created": datetime.fromtimestamp(plan_file.stat().st_ctime).isoformat()
                })

        # Load from Briefings (extract action items)
        briefings_dir = self.vault_path / "Briefings"
        if briefings_dir.exists():
            for brief_file in briefings_dir.glob("*.md"):
                content = brief_file.read_text()
                if "action" in content.lower() or "todo" in content.lower():
                    tasks.append({
                        "source": "Briefings",
                        "file": str(brief_file.name),
                        "content": content,
                        "created": datetime.fromtimestamp(brief_file.stat().st_ctime).isoformat()
                    })

        return tasks

    def apply_eisenhower_matrix(self, tasks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize tasks using Eisenhower Matrix."""
        prompt = f"""Analyze these tasks and categorize them using the Eisenhower Matrix.

Tasks:
{json.dumps(tasks, indent=2, default=str)}

Return JSON with tasks categorized by quadrant:
{{
    "urgent_important": [
        {{
            "task": "brief description",
            "original_file": "source file",
            "reason": "why this is urgent and important",
            "suggested_action": "Do first / immediate action"
        }}
    ],
    "important_not_urgent": [
        {{
            "task": "brief description",
            "original_file": "source file",
            "reason": "why this is important but not urgent",
            "suggested_action": "Schedule time"
        }}
    ],
    "urgent_not_important": [
        {{
            "task": "brief description",
            "original_file": "source file",
            "reason": "why this is urgent but not important",
            "suggested_action": "Delegate or minimize"
        }}
    ],
    "not_urgent_not_important": [
        {{
            "task": "brief description",
            "original_file": "source file",
            "reason": "why this is neither",
            "suggested_action": "Consider eliminating"
        }}
    ],
    "summary": {{
        "total_tasks": 0,
        "do_first_count": 0,
        "schedule_count": 0,
        "delegate_count": 0,
        "eliminate_count": 0
    }}
}}"""

        response = self.call_claude(prompt, system="You are a productivity expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: simple categorization
            return {
                "urgent_important": tasks[:len(tasks)//4] if tasks else [],
                "important_not_urgent": tasks[len(tasks)//4:len(tasks)//2] if tasks else [],
                "urgent_not_important": tasks[len(tasks)//2:3*len(tasks)//4] if tasks else [],
                "not_urgent_not_important": tasks[3*len(tasks)//4:] if tasks else [],
                "summary": {"total_tasks": len(tasks)},
                "error": "Failed to parse Eisenhower analysis"
            }

    def optimize_schedule(self, matrix: Dict[str, Any],
                          current_time: datetime = None) -> Dict[str, Any]:
        """Generate optimized daily schedule based on Eisenhower Matrix."""
        current_time = current_time or datetime.now()

        prompt = f"""Create an optimized daily schedule based on this Eisenhower Matrix analysis.

Current Time: {current_time.strftime('%H:%M')}
Working Hours: 09:00 - 17:00

Eisenhower Matrix:
{json.dumps(matrix, indent=2, default=str)}

Return JSON:
{{
    "daily_schedule": [
        {{
            "time_block": "09:00-10:30",
            "task": "description",
            "category": "deep_work|admin|meetings|break",
            "energy_level": "high|medium|low",
            "focus_required": true/false
        }}
    ],
    "deep_work_blocks": ["time1", "time2"],
    "admin_blocks": ["time1"],
    "breaks": ["time1", "time2"],
    "protected_time": "Description of time protected for important work",
    "flexibility_buffer": "Time reserved for unexpected tasks"
}}"""

        response = self.call_claude(prompt, system="You are a time management expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "daily_schedule": [],
                "error": "Failed to generate schedule"
            }

    def identify_bottlenecks(self, tasks: List[Dict[str, Any]],
                             matrix: Dict[str, Any]) -> Dict[str, Any]:
        """Identify potential bottlenecks and blockers."""
        prompt = f"""Analyze these tasks for potential bottlenecks and blockers.

Tasks:
{json.dumps(tasks, indent=2, default=str)}

Eisenhower Analysis:
{json.dumps(matrix, indent=2, default=str)}

Return JSON:
{{
    "bottlenecks": [
        {{
            "type": "dependency|resource|time|information",
            "description": "what's blocked",
            "blocking_tasks": ["task1", "task2"],
            "resolution": "how to unblock"
        }}
    ],
    "overloaded_areas": ["area1", "area2"],
    "resource_conflicts": ["conflict description"],
    "recommendations": ["rec1", "rec2"],
    "risk_level": "low|medium|high"
}}"""

        response = self.call_claude(prompt, system="You are a workflow optimization expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "bottlenecks": [],
                "recommendations": [],
                "risk_level": "unknown"
            }

    def generate_recommendations(self, matrix: Dict[str, Any],
                                 schedule: Dict[str, Any],
                                 bottlenecks: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable recommendations."""
        prompt = f"""Generate actionable productivity recommendations.

Eisenhower Matrix:
{json.dumps(matrix, indent=2, default=str)}

Optimized Schedule:
{json.dumps(schedule, indent=2, default=str)}

Identified Bottlenecks:
{json.dumps(bottlenecks, indent=2, default=str)}

Return JSON:
{{
    "priority_actions": [
        {{
            "action": "specific action to take",
            "impact": "high|medium|low",
            "effort": "high|medium|low",
            "deadline": "when to do it"
        }}
    ],
    "focus_recommendations": ["rec1", "rec2"],
    "delegation_opportunities": ["opportunity1"],
    "time_saving_tips": ["tip1", "tip2"],
    "weekly_goals": ["goal1", "goal2"],
    "avoid_these": ["thing to avoid1"],
    "energy_management": "Advice on managing energy throughout day"
}}"""

        response = self.call_claude(prompt, system="You are a productivity coach. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "priority_actions": [],
                "error": "Failed to generate recommendations"
            }

        result["generated_at"] = datetime.now().isoformat()
        return result

    def save_optimization_report(self, report: Dict[str, Any]) -> Path:
        """Save optimization report to Analytics."""
        reports_dir = self.vault_path / "Gold_Tier" / "Analytics" / "Reports" / "Daily"
        reports_dir.mkdir(parents=True, exist_ok=True)

        filename = f"task_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = reports_dir / filename

        with open(file_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        self.logger.info(f"Report saved to {file_path}")
        return file_path

    def execute(self, action: str = "optimize", **kwargs) -> Dict[str, Any]:
        """Main execution method."""
        if action == "optimize":
            # Load all tasks
            tasks = self.load_all_tasks()

            # Apply Eisenhower Matrix
            matrix = self.apply_eisenhower_matrix(tasks)

            # Optimize schedule
            schedule = self.optimize_schedule(matrix)

            # Identify bottlenecks
            bottlenecks = self.identify_bottlenecks(tasks, matrix)

            # Generate recommendations
            recommendations = self.generate_recommendations(matrix, schedule, bottlenecks)

            # Compile full report
            report = {
                "generated_at": datetime.now().isoformat(),
                "tasks_analyzed": len(tasks),
                "eisenhower_matrix": matrix,
                "optimized_schedule": schedule,
                "bottlenecks": bottlenecks,
                "recommendations": recommendations
            }

            # Save report
            report_path = self.save_optimization_report(report)

            # Log action
            self.log_action("task_optimization", {
                "tasks_analyzed": len(tasks),
                "report_saved": str(report_path),
                "risk_level": bottlenecks.get("risk_level", "unknown")
            })

            return {
                "status": "success",
                "report": report,
                "report_file": str(report_path),
                "timestamp": datetime.now().isoformat()
            }

        elif action == "matrix":
            tasks = self.load_all_tasks()
            return {
                "status": "success",
                "matrix": self.apply_eisenhower_matrix(tasks)
            }

        elif action == "schedule":
            matrix = kwargs.get("matrix", {})
            return {
                "status": "success",
                "schedule": self.optimize_schedule(matrix)
            }

        else:
            return {"status": "error", "message": f"Unknown action: {action}"}


if __name__ == "__main__":
    import yaml  # Ensure yaml is imported

    agent = TaskOptimizer()
    result = agent.execute("optimize")
    print(json.dumps(result, indent=2, default=str))
