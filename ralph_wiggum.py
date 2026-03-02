#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Autonomous Task Completion Hook
Prevents Claude from stopping mid-task by checking current task status.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
VAULT_PATH = Path("/mnt/c/Users/Admin/AI_Employee_Vault")
CURRENT_TASK_FILE = VAULT_PATH / "Plans" / "CURRENT_TASK.md"
RALPH_LOG_FILE = VAULT_PATH / "Logs" / "ralph_wiggum.json"
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS", "10"))


def read_task_file() -> dict:
    """Read the current task file and parse frontmatter."""
    if not CURRENT_TASK_FILE.exists():
        return {"exists": False}

    content = CURRENT_TASK_FILE.read_text()

    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2].strip()

            task_data = {"exists": True, "body": body}

            # Parse frontmatter lines
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    task_data[key.strip()] = value.strip()

            return task_data

    return {"exists": True, "body": content}


def log_iteration(decision: str, reason: str, task_data: dict):
    """Log the Ralph Wiggum iteration."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "reason": reason,
        "task": task_data.get("task", "unknown"),
        "status": task_data.get("status", "unknown"),
        "iterations": task_data.get("iterations", "1")
    }

    # Read existing logs
    logs = []
    if RALPH_LOG_FILE.exists():
        try:
            logs = json.loads(RALPH_LOG_FILE.read_text())
        except json.JSONDecodeError:
            logs = []

    logs.append(log_entry)

    # Write back
    RALPH_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    RALPH_LOG_FILE.write_text(json.dumps(logs, indent=2))


def main():
    """Main Ralph Wiggum hook logic."""
    task_data = read_task_file()

    # If no task file exists, allow exit
    if not task_data.get("exists", False):
        output = {"decision": "allow", "reason": "No active task - allowing exit"}
        print(json.dumps(output))
        return

    status = task_data.get("status", "").lower()
    iterations = int(task_data.get("iterations", "0"))

    # If no task (idle, empty, or no task), allow exit
    if status in ("idle", "", "none", "done") or not task_data.get("task"):
        output = {"decision": "allow", "reason": "No active task - allowing exit"}
        print(json.dumps(output))
        return

    # If task is done, allow exit and clean up
    if status == "done":
        output = {"decision": "allow", "reason": "Task marked as complete - allowing exit"}
        print(json.dumps(output))
        return

    # Check if max iterations reached
    if iterations >= MAX_ITERATIONS:
        output = {
            "decision": "allow",
            "reason": f"Max iterations ({MAX_ITERATIONS}) reached - allowing exit"
        }
        print(json.dumps(output))
        return

    # Task is in progress - block exit
    output = {
        "decision": "block",
        "reason": f"Task '{task_data.get('task', 'unknown')}' is {status}. Continue working until status is 'done'."
    }
    print(json.dumps(output))

    # Log this iteration
    log_iteration("block", output["reason"], task_data)


if __name__ == "__main__":
    main()
