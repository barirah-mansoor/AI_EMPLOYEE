#!/usr/bin/env python3
"""
Silver Tier - System Monitor
Checks system health, APIs, resources, and performance
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


def check_gmail_api():
    """Check Gmail API connection"""
    vault_path = Path.home() / "AI_Employee_Vault"
    creds_path = vault_path / "Silver_Tier/Credentials"

    if creds_path.exists() and list(creds_path.glob("*.json")):
        token_path = creds_path / "token.json"
        if token_path.exists():
            return {"status": "✅ Connected", "detail": "Token found"}
        return {"status": "⚠️  Partial", "detail": "Credentials without token"}
    return {"status": "❌ Not configured", "detail": "No credentials"}


def check_scheduler():
    """Check if scheduler/watcher is running"""
    vault_path = Path.home() / "AI_Employee_Vault"
    pid_file = vault_path / ".watcher.pid"

    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            # Check if process exists
            os.kill(pid, 0)
            return {"status": "✅ Running", "detail": f"PID: {pid}"}
        except:
            return {"status": "❌ Dead", "detail": "PID file stale"}
    return {"status": "❌ Not running", "detail": "No PID file"}


def check_vault_folders():
    """Check all vault folders exist"""
    vault_path = Path.home() / "AI_Employee_Vault"
    required_folders = [
        "Needs_Action", "Plans", "Pending_Approval", "Approved",
        "Done", "Inbox", "Logs", "Briefings", "Accounting", "Silver_Tier"
    ]

    results = []
    for folder in required_folders:
        path = vault_path / folder
        if path.exists():
            count = len(list(path.glob("*")))
            results.append(f"  ✅ {folder}: {count} items")
        else:
            results.append(f"  ❌ {folder}: MISSING")

    return results


def check_disk_space():
    """Check disk space"""
    try:
        result = subprocess.run(
            ["df", "-h", str(Path.home())],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            return {
                "status": "✅ OK",
                "detail": f"{parts[3]} free of {parts[1]}"
            }
    except:
        pass
    return {"status": "⚠️  Unknown", "detail": "Could not check"}


def check_gmail_stats():
    """Get Gmail processing stats"""
    vault_path = Path.home() / "AI_Employee_Vault"
    gmail_path = vault_path / "Silver_Tier/Gmail"

    if not gmail_path.exists():
        return {"status": "❌ No Gmail data", "detail": "Run process_gmail first"}

    processed = len(list((gmail_path / "Processed").glob("*.json"))) if (gmail_path / "Processed").exists() else 0

    return {"status": "✅ Active", "detail": f"{processed} emails processed"}


def main():
    print("🔍 Running Silver Tier System Monitor...")
    print("="*50)

    checks = {
        "Gmail API": check_gmail_api(),
        "Scheduler": check_scheduler(),
        "Disk Space": check_disk_space(),
        "Gmail Stats": check_gmail_stats(),
    }

    print("\n## 🟢 System Components")
    for name, result in checks.items():
        print(f"  {name}: {result['status']} - {result['detail']}")

    print("\n## 📁 Vault Folders")
    for folder in check_vault_folders():
        print(folder)

    # Log to file
    vault_path = Path.home() / "AI_Employee_Vault"
    log_file = vault_path / f"Logs/{datetime.now().strftime('%Y-%m-%d')}.json"

    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "skill": "system_monitor",
        "action": "System health check completed",
        "files_affected": [],
        "approval_required": False,
        "result": "success",
        "details": checks
    }

    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

    print("\n" + "="*50)
    print("✅ System monitor complete!")
    print("📝 Logged to today's audit")

    return 0


if __name__ == "__main__":
    sys.exit(main())
