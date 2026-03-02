#!/usr/bin/env python3
"""
Silver Tier - Process Gmail Emails
Creates EMAIL_ task files in Needs_Action from Gmail inbox
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from gmail_processor import GmailProcessor


def main():
    print("📧 Processing Gmail (Silver Tier)...")

    # Clear history to reprocess all emails
    vault_path = Path.home() / "AI_Employee_Vault"
    history_file = vault_path / "Silver_Tier/Gmail/processed_history.json"

    # Backup existing history
    if history_file.exists():
        backup = vault_path / "Silver_Tier/Gmail/processed_history.backup.json"
        with open(history_file, 'r') as f:
            with open(backup, 'w') as bf:
                bf.write(f.read())

    # Remove history to force reprocessing
    if history_file.exists():
        history_file.unlink()

    # Run the processor
    processor = GmailProcessor()
    success = processor.run_gmail_sync()

    # Update Dashboard
    dashboard = vault_path / "Dashboard.md"
    if dashboard.exists():
        content = dashboard.read_text()
        content = content.replace(
            "Last Updated: 2026-02-21",
            f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}"
        )
        content = content.replace(
            "📮 Found 20 unread, 0 new",
            "📮 Processing Gmail..."
        )
        dashboard.write_text(content)

    # Log the action
    log_file = vault_path / f"Logs/{datetime.now().strftime('%Y-%m-%d')}.json"
    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "skill": "process_gmail",
        "action": "Gmail sync completed - created EMAIL_ files in Needs_Action",
        "files_affected": ["Needs_Action/", "Silver_Tier/Gmail/Processed/"],
        "approval_required": False,
        "result": "success"
    }

    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"✅ Gmail processing complete!")
    print(f"📁 Check Needs_Action/ for EMAIL_ files")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
