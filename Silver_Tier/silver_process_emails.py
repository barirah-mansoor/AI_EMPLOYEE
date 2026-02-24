#!/usr/bin/env python3
"""
Silver Tier - Process Email Tasks
Reads EMAIL_ files from Needs_Action, categorizes them, and takes action
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def categorize_email(filepath):
    """Categorize an email file and determine action"""
    content = filepath.read_text()

    # Extract key info
    category = "UNKNOWN"
    action = "FILE_ONLY"
    sender = ""

    for line in content.split('\n'):
        if line.startswith('**From:**'):
            sender = line.replace('**From:**', '').strip().lower()
        if 'category:' in line.lower():
            category = line.split(':')[-1].strip()
        if 'priority:' in line.lower():
            priority = line.split(':')[-1].strip()

    # Determine action based on sender
    if 'noreply' in sender or 'no-reply' in sender or 'notification' in sender:
        action = "FILE_ONLY"
    elif 'google' in sender or 'ai' in sender or 'gemini' in sender:
        action = "ACKNOWLEDGE"
    elif 'job' in sender or 'indeed' in sender or 'linkedin' in sender:
        action = "FILE_ONLY"
    else:
        action = "FILE_ONLY"  # Default to archive

    return category, action


def main():
    print("📧 Processing email tasks...")

    vault_path = Path.home() / "AI_Employee_Vault"
    needs_action = vault_path / "Needs_Action"
    done_folder = vault_path / "Done"

    # Find all EMAIL_ files
    email_files = list(needs_action.glob("EMAIL_*"))

    if not email_files:
        print("No email files found in Needs_Action")
        return 0

    print(f"Found {len(email_files)} email files")

    processed = 0
    acknowledge_needed = []
    file_only_count = 0

    for email_file in email_files:
        category, action = categorize_email(email_file)

        if action == "FILE_ONLY":
            # Move to Done
            done_path = done_folder / email_file.name
            email_file.rename(done_path)
            file_only_count += 1
            processed += 1
        elif action == "ACKNOWLEDGE":
            acknowledge_needed.append(email_file)
            processed += 1

    # Update Dashboard
    dashboard = vault_path / "Dashboard.md"
    if dashboard.exists():
        content = dashboard.read_text()

        # Update email counts
        content = content.replace(
            "**Emails Processed:** 0",
            f"**Emails Processed:** {processed}"
        )

        dashboard.write_text(content)

    # Log the action
    log_file = vault_path / f"Logs/{datetime.now().strftime('%Y-%m-%d')}.json"
    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "skill": "process_emails",
        "action": f"Processed {processed} emails: {file_only_count} archived, {len(acknowledge_needed)} need acknowledgment",
        "files_affected": [f.name for f in email_files],
        "approval_required": len(acknowledge_needed) > 0,
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

    print(f"✅ Processed {processed} emails")
    print(f"   📦 Archived to Done: {file_only_count}")
    print(f"   ✉️  Need acknowledgment: {len(acknowledge_needed)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
