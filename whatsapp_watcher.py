#!/usr/bin/env python3
"""
WhatsApp Watcher - Monitors WhatsApp Web for urgent messages
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuration
VAULT_PATH = Path("/mnt/c/Users/Admin/AI_Employee_Vault")
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
SILVER_TIER = VAULT_PATH / "Silver_Tier"
PROCESSED_CACHE = SILVER_TIER / ".whatsapp_processed.json"
DEV_MODE = os.environ.get("DEV_MODE", "false").lower() == "true"
POLL_INTERVAL = 30  # seconds

# Keywords that trigger action creation
URGENT_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 'deadline', 'important']


def load_processed_cache() -> List[str]:
    """Load processed message IDs from cache."""
    if PROCESSED_CACHE.exists():
        try:
            return json.loads(PROCESSED_CACHE.read_text())
        except json.JSONDecodeError:
            return []
    return []


def save_processed_cache(message_ids: List[str]):
    """Save processed message IDs to cache."""
    PROCESSED_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_CACHE.write_text(json.dumps(message_ids, indent=2))


def log_detection(message: Dict[str, Any]):
    """Log message detection to audit log."""
    log_file = VAULT_PATH / "Logs" / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    logs = []
    if log_file.exists():
        try:
            logs = json.loads(log_file.read_text())
        except json.JSONDecodeError:
            pass

    logs.append({
        "timestamp": datetime.now().isoformat(),
        "skill": "whatsapp_watcher",
        "action": "message_detected",
        "files_affected": [],
        "approval_required": False,
        "result": "success",
        "details": message
    })

    log_file.write_text(json.dumps(logs, indent=2))


def create_needs_action_file(message: Dict[str, Any]) -> Path:
    """Create a Needs_Action file for a detected message."""
    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    contact_safe = message.get("from", "unknown").replace(" ", "_").replace("/", "_")
    filename = f"WHATSAPP_{contact_safe}_{timestamp}.md"

    # Determine priority
    priority = "🔴 URGENT" if message.get("is_urgent") else "🟡 HIGH" if message.get("keyword") else "🟢 NORMAL"

    content = f"""---
type: whatsapp_message
from: "{message.get('from', 'Unknown')}"
text: "{message.get('text', '')[:200]}"
received: "{message.get('timestamp', datetime.now().isoformat())}"
priority: {priority}
status: pending
---

# WhatsApp Message

**From:** {message.get('from', 'Unknown')}
**Time:** {message.get('timestamp', datetime.now().isoformat())}
**Priority:** {priority}

## Message Text

{message.get('text', '')}

## Detected Keywords

{message.get('keywords_found', [])}

## Action Required

- [ ] Review message
- [ ] Determine appropriate response
- [ ] Create follow-up task if needed
"""

    file_path = NEEDS_ACTION / filename
    file_path.write_text(content)
    return file_path


def get_dev_mode_messages() -> List[Dict[str, Any]]:
    """Get synthetic messages for DEV_MODE."""
    dev_messages_file = SILVER_TIER / "Templates" / "whatsapp_test_messages.json"

    if dev_messages_file.exists():
        try:
            return json.loads(dev_messages_file.read_text())
        except json.JSONDecodeError:
            pass

    # Default dev messages
    return [
        {
            "id": "dev_001",
            "from": "John Smith",
            "text": "Urgent: Client needs invoice by EOD today. Please process ASAP!",
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "dev_002",
            "from": "Sarah Johnson",
            "text": "Hey, can you help with the payment processing? Important deadline tomorrow.",
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "dev_003",
            "from": "Mike Wilson",
            "text": "Quick question about the project deadline - need to discuss ASAP",
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "dev_004",
            "from": "Lisa Brown",
            "text": "Thanks for your help yesterday!",
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "dev_005",
            "from": "Tom Davis",
            "text": "Invoice #1234 attached. Please review and process payment when possible.",
            "timestamp": datetime.now().isoformat()
        }
    ]


def check_whatsapp_messages() -> List[Dict[str, Any]]:
    """Check for new WhatsApp messages."""
    processed_ids = load_processed_cache()
    new_messages = []

    if DEV_MODE:
        messages = get_dev_mode_messages()
    else:
        # Real WhatsApp Web integration would go here
        # For now, simulate with dev mode
        messages = get_dev_mode_messages()

    for msg in messages:
        msg_id = msg.get("id", "")

        # Skip if already processed
        if msg_id in processed_ids:
            continue

        # Check for urgent keywords
        text_lower = msg.get("text", "").lower()
        keywords_found = [kw for kw in URGENT_KEYWORDS if kw in text_lower]

        message_data = {
            "id": msg_id,
            "from": msg.get("from", "Unknown"),
            "text": msg.get("text", ""),
            "timestamp": msg.get("timestamp", datetime.now().isoformat()),
            "keywords_found": keywords_found,
            "is_urgent": len(keywords_found) > 0
        }

        new_messages.append(message_data)

    return new_messages


def run_watcher():
    """Main watcher loop."""
    print(f"WhatsApp Watcher starting...")
    print(f"DEV_MODE: {DEV_MODE}")
    print(f"Vault path: {VAULT_PATH}")

    if not DEV_MODE:
        print("Warning: Real WhatsApp Web integration not implemented yet")
        print("Set DEV_MODE=true to use synthetic messages")
        return

    processed_ids = load_processed_cache()

    while True:
        try:
            new_messages = check_whatsapp_messages()

            for msg in new_messages:
                # Create needs action file
                file_path = create_needs_action_file(msg)
                print(f"Created: {file_path.name}")

                # Log detection
                log_detection(msg)

                # Add to processed cache
                processed_ids.append(msg.get("id", ""))

            if new_messages:
                save_processed_cache(processed_ids)
                print(f"Processed {len(new_messages)} new messages")
            else:
                print(f"No new messages at {datetime.now().strftime('%H:%M:%S')}")

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\nWhatsApp Watcher stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(POLL_INTERVAL * 2)  # Exponential backoff


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WhatsApp Watcher")
    parser.add_argument("--once", action="store_true", help="Run once instead of loop")
    args = parser.parse_args()

    if args.once:
        messages = check_whatsapp_messages()
        print(f"Found {len(messages)} new messages")
        for msg in messages:
            file_path = create_needs_action_file(msg)
            print(f"Created: {file_path.name}")
    else:
        run_watcher()
