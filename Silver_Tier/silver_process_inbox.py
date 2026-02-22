#!/usr/bin/env python3
"""
Silver Tier - Process Inbox
Triages files in Needs_Action folder and creates plans
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import shutil


def get_priority_from_email(file_path):
    """Extract priority from email file"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        # Check for priority in frontmatter
        if 'priority: RED' in content.lower():
            return "🔴 RED"
        elif 'priority: YELLOW' in content.lower():
            return "🟡 YELLOW"
        elif 'priority: GREEN' in content.lower():
            return "🟢 GREEN"
        return "⚪ LOW"
    except:
        return "⚪ LOW"


def categorize_email(filename):
    """Categorize email by filename pattern"""
    filename_lower = filename.lower()

    if 'job' in filename_lower or 'developer' in filename_lower or 'front_end' in filename_lower or 'full_stack' in filename_lower:
        return "Job Alert"
    elif 'newsletter' in filename_lower or 'ai_' in filename_lower or 'weekly' in filename_lower:
        return "AI Newsletter"
    elif 'tactiq' in filename_lower or 'meeting' in filename_lower:
        return "Meeting"
    elif 'notification' in filename_lower or 'reminder' in filename_lower:
        return "Notification"
    else:
        return "Other"


def process_inbox():
    """Main function to process Needs_Action folder"""
    vault_path = Path.home() / "AI_Employee_Vault"
    needs_action = vault_path / "Needs_Action"
    plans_dir = vault_path / "Plans"
    done_dir = vault_path / "Done"
    pending_dir = vault_path / "Pending_Approval"

    # Ensure directories exist
    for d in [needs_action, plans_dir, done_dir, pending_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Get all files in Needs_Action
    files = sorted(needs_action.glob("*"))

    if not files:
        print("📥 No files in Needs_Action folder")
        print("✅ Inbox is empty!")
        return 0

    print(f"📥 Processing {len(files)} files in Needs_Action...")
    print("=" * 50)

    stats = {
        "FILE_ONLY": 0,
        "ACKNOWLEDGE": 0,
        "PENDING_APPROVAL": 0,
        "categories": {}
    }

    processed_today = []

    for file_path in files:
        if not file_path.is_file():
            continue

        filename = file_path.name

        # Skip duplicates
        if filename.endswith('.md') and filename.startswith('EMAIL_'):
            # Get priority and category
            priority = get_priority_from_email(file_path)
            category = categorize_email(filename)

            # Track categories
            stats["categories"][category] = stats["categories"].get(category, 0) + 1

            # Most emails are FILE_ONLY (no response needed)
            action = "FILE_ONLY"
            stats["FILE_ONLY"] += 1

            # Check for special cases that need attention
            if 'gemini' in filename.lower() and 'migration' in filename.lower():
                action = "ACKNOWLEDGE"
                stats["ACKNOWLEDGE"] += 1

            # Create plan file
            plan_filename = f"PLAN_{filename.replace('.md', '')}_{datetime.now().strftime('%Y%m%d')}.md"
            plan_path = plans_dir / plan_filename

            plan_content = f"""# Plan: {filename}

## Details
- **Source:** {file_path.read_text(encoding='utf-8', errors='ignore').splitlines()[0][:100] if file_path.stat().st_size > 0 else 'Email'}
- **Priority:** {priority}
- **Category:** {category}
- **Action Required:** {action}

## Analysis
This email was analyzed and categorized as {action}.

- **Category:** {category}
- **Response Needed:** {'Yes' if action != 'FILE_ONLY' else 'No'}

## Recommended Actions
- [ ] Move to Done after review

## Approval Required
{'No - standard email archiving' if action == 'FILE_ONLY' else 'Yes - requires human review'}

---
*Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            plan_path.write_text(plan_content)

            # Move to Done
            done_path = done_dir / filename
            shutil.move(str(file_path), str(done_path))

            processed_today.append(filename)

    # Print summary
    print("\n## Summary")
    print(f"| Category | Count |")
    print(f"|----------|-------|")
    for cat, count in sorted(stats["categories"].items()):
        print(f"| {cat} | {count} |")

    print(f"\n### Actions Taken:")
    print(f"  - FILE_ONLY: {stats['FILE_ONLY']}")
    print(f"  - ACKNOWLEDGE: {stats['ACKNOWLEDGE']}")

    # Log to file
    log_file = vault_path / f"Logs/{datetime.now().strftime('%Y-%m-%d')}.json"
    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "skill": "process_inbox",
        "action": f"Processed {len(files)} files - {stats['FILE_ONLY']} archived, {stats['ACKNOWLEDGE']} acknowledged",
        "files_affected": [f"Needs_Action/ ({len(files)} files)", f"Plans/ ({len(files)} plans)", f"Done/"],
        "approval_required": False,
        "result": "success",
        "stats": stats
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
    print(f"✅ Inbox processed: {len(files)} files")
    print(f"📁 Moved to Done: {len(files)} files")
    print(f"📋 Plans created: {len(files)} files")
    print("📝 Logged to today's audit")

    # Update Dashboard
    update_dashboard(vault_path, len(files))

    return 0


def update_dashboard(vault_path, processed_count):
    """Update Dashboard.md with new counts"""
    dashboard = vault_path / "Dashboard.md"
    if not dashboard.exists():
        return

    content = dashboard.read_text()

    # Update queue counts
    needs_action_count = len(list((vault_path / "Needs_Action").glob("*")))
    plans_count = len(list((vault_path / "Plans").glob("*.md")))
    done_count = len(list((vault_path / "Done").glob("*")))
    pending_count = len(list((vault_path / "Pending_Approval").glob("*")))

    # Replace counts
    content = content.replace(
        "| Needs Action | 0 |",
        f"| Needs Action | {needs_action_count} |"
    )
    content = content.replace(
        "| Plans Active | 100 |",
        f"| Plans Active | {plans_count} |"
    )
    content = content.replace(
        "| Done (Total) | 200 |",
        f"| Done (Total) | {done_count} |"
    )

    # Update timestamp
    content = content.replace(
        "Last Updated: 2026-02-22",
        f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}"
    )

    # Update today's activity
    content = content.replace(
        "Today's Email Activity",
        f"Today's Email Activity (Updated: {datetime.now().strftime('%H:%M')})"
    )

    dashboard.write_text(content)


def main():
    return process_inbox()


if __name__ == "__main__":
    sys.exit(main())
