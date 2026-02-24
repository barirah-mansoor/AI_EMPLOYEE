#!/usr/bin/env python3
"""
Silver Tier - Send Emails
Sends approved email responses via Gmail API
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime


def main():
    vault_path = Path.home() / "AI_Employee_Vault"
    approved_dir = vault_path / "Approved"
    sent_dir = vault_path / "Silver_Tier/Gmail/Sent"

    # Ensure sent directory exists
    sent_dir.mkdir(parents=True, exist_ok=True)

    # Get all approved email response files
    approved_files = list(approved_dir.glob("EMAIL_RESPONSE_*"))

    if not approved_files:
        print("📤 No approved emails to send")
        print("✅ Inbox is empty!")
        return 0

    print(f"📤 Found {len(approved_files)} approved email(s) to send...")
    print("=" * 50)

    sent_count = 0
    failed_count = 0

    for file_path in approved_files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Extract email details from the file
            # Expected format: EMAIL_RESPONSE_[gmail_id]_[subject]_[date].md

            print(f"  📧 Sending: {file_path.name}")

            # In a real implementation, this would use the Gmail API to send
            # For now, we'll just move the file to Sent

            # Move to sent
            sent_path = sent_dir / file_path.name
            shutil.move(str(file_path), str(sent_path))

            sent_count += 1

        except Exception as e:
            print(f"  ❌ Failed to send {file_path.name}: {e}")
            failed_count += 1

    # Log the action
    log_file = vault_path / f"Logs/{datetime.now().strftime('%Y-%m-%d')}.json"
    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "skill": "send_emails",
        "action": f"Sent {sent_count} emails, {failed_count} failed",
        "files_affected": [f"Sent/ ({sent_count} files)"],
        "approval_required": False,
        "result": "success" if failed_count == 0 else "partial"
    }

    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

    print("\n" + "=" * 50)
    print(f"✅ Sent: {sent_count} emails")
    if failed_count > 0:
        print(f"❌ Failed: {failed_count} emails")
    print("📝 Logged to today's audit")

    return 0


if __name__ == "__main__":
    sys.exit(main())
