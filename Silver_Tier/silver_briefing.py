#!/usr/bin/env python3
"""
Silver Tier - Daily Briefing
Generates enhanced briefing with email stats and system status
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta


def get_email_stats():
    """Get email processing stats"""
    vault_path = Path.home() / "AI_Employee_Vault"
    gmail_path = vault_path / "Silver_Tier/Gmail"

    processed = 0
    if gmail_path.exists():
        processed_path = gmail_path / "Processed"
        if processed_path.exists():
            processed = len(list(processed_path.glob("*.json")))

    return {
        "emails_processed": processed,
        "last_sync": "Today"
    }


def get_queue_counts():
    """Get queue folder counts"""
    vault_path = Path.home() / "AI_Employee_Vault"

    folders = {
        "Needs Action": "Needs_Action",
        "Plans": "Plans",
        "Pending Approval": "Pending_Approval",
        "Done": "Done"
    }

    counts = {}
    for name, path in folders.items():
        full_path = vault_path / path
        if full_path.exists():
            counts[name] = len(list(full_path.glob("*")))
        else:
            counts[name] = 0

    return counts


def get_system_status():
    """Get system component status"""
    vault_path = Path.home() / "AI_Employee_Vault"

    status = []

    # Check Gmail credentials
    creds_path = vault_path / "Silver_Tier/Credentials"
    if creds_path.exists() and list(creds_path.glob("*.json")):
        status.append("✅ Gmail API: Connected")
    else:
        status.append("❌ Gmail API: Not configured")

    # Check scheduler
    pid_file = vault_path / ".watcher.pid"
    if pid_file.exists():
        status.append("✅ Watcher: Running")
    else:
        status.append("❌ Watcher: Not running")

    return status


def generate_briefing():
    """Generate the daily briefing"""
    vault_path = Path.home() / "AI_Employee_Vault"
    today = datetime.now().strftime('%Y-%m-%d')

    email_stats = get_email_stats()
    queue_counts = get_queue_counts()
    system_status = get_system_status()

    briefing = f"""# 🤖 AI Employee Daily Briefing

> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Today's Summary

| Metric | Value |
|--------|-------|
| Emails Processed | {email_stats['emails_processed']} |
| Last Sync | {email_stats['last_sync']} |

## 📥 Queue Status

| Folder | Count |
|--------|-------|
| Needs Action | {queue_counts['Needs Action']} |
| Plans | {queue_counts['Plans']} |
| Pending Approval | {queue_counts['Pending Approval']} |
| Done | {queue_counts['Done']} |

## 🔧 System Status

{chr(10).join(system_status)}

## 🎯 Today's Focus

- Process remaining emails in Needs_Action
- Review any pending approvals
- Monitor system health

## 📝 Action Items

1. Run `bash run_ai_employee.sh process_gmail` to sync new emails
2. Run `bash run_ai_employee.sh process_emails` to categorize emails
3. Check Dashboard.md for detailed metrics

---
*AI Employee | Silver Tier | {today}*
"""

    # Save briefing
    briefing_path = vault_path / "Briefings" / f"Briefing_{today}.md"
    briefing_path.write_text(briefing)

    # Also update Dashboard with today's date
    dashboard = vault_path / "Dashboard.md"
    if dashboard.exists():
        content = dashboard.read_text()
        content = content.replace(
            "Last Updated: 2026-02-21",
            f"Last Updated: {today}"
        )
        dashboard.write_text(content)

    return briefing


def main():
    print("🥈 Generating Silver Tier Briefing...")

    briefing = generate_briefing()

    print("✅ Briefing generated!")
    print(f"📄 Saved to: Briefings/Briefing_{datetime.now().strftime('%Y-%m-%d')}.md")

    # Print to console
    print("\n" + "="*50)
    print(briefing)
    print("="*50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
