#!/usr/bin/env python3
"""
AI Employee Vault - Filesystem Watcher

Monitors ~/AI_Employee_Vault/Inbox for new files and automatically:
- Copies them to /Needs_Action/
- Creates metadata companion .md files
- Logs actions to /Logs/YYYY-MM-DD.json
- Updates Dashboard.md queue counts

Uses watchdog for real-time events with 15-second polling backup.
"""

import json
import os
import re
import shutil
import sys
import time
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent


# Vault paths
VAULT_ROOT: Path = Path.home() / "AI_Employee_Vault"
INBOX_DIR: Path = VAULT_ROOT / "Inbox"
NEEDS_ACTION_DIR: Path = VAULT_ROOT / "Needs_Action"
LOGS_DIR: Path = VAULT_ROOT / "Logs"
DASHBOARD_PATH: Path = VAULT_ROOT / "Dashboard.md"

# Track processed files to avoid duplicates
processed_files: set[str] = set()
lock = threading.Lock()


def get_timestamp() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def get_today_log_path() -> Path:
    """Return the path to today's log file."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return LOGS_DIR / f"{today}.json"


def log_action(
    skill: str,
    action: str,
    files_affected: list[str],
    approval_required: bool = False,
    result: str = "success",
) -> None:
    """Append a JSON log entry to today's log file."""
    log_path = get_today_log_path()
    entry = {
        "timestamp": get_timestamp(),
        "skill": skill,
        "action": action,
        "files_affected": files_affected,
        "approval_required": approval_required,
        "result": result,
    }

    # Read existing log entries or start fresh
    entries: list[dict] = []
    if log_path.exists():
        try:
            raw = log_path.read_text(encoding="utf-8").strip()
            if raw:
                entries = json.loads(raw)
        except (json.JSONDecodeError, OSError):
            entries = []

    entries.append(entry)

    try:
        log_path.write_text(
            json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as e:
        print(f"[ERROR] Failed to write log: {e}")


def update_dashboard_queue_count() -> None:
    """Update the Needs Action count in Dashboard.md."""
    if not DASHBOARD_PATH.exists():
        return

    try:
        # Count files in Needs_Action (exclude metadata .md companions)
        count = sum(
            1 for f in NEEDS_ACTION_DIR.iterdir()
            if f.is_file() and not f.name.startswith("META_")
        )

        content = DASHBOARD_PATH.read_text(encoding="utf-8")
        updated = re.sub(
            r"(\| Needs Action\s*\|\s*)\d+(\s*\|)",
            rf"\g<1>{count}\2",
            content,
        )
        DASHBOARD_PATH.write_text(updated, encoding="utf-8")
    except OSError as e:
        print(f"[ERROR] Failed to update dashboard: {e}")


def determine_file_type(filepath: Path) -> str:
    """Determine a human-readable file type from extension."""
    ext_map = {
        ".pdf": "PDF Document",
        ".doc": "Word Document",
        ".docx": "Word Document",
        ".xls": "Spreadsheet",
        ".xlsx": "Spreadsheet",
        ".csv": "CSV Data",
        ".txt": "Text File",
        ".md": "Markdown Document",
        ".jpg": "Image (JPEG)",
        ".jpeg": "Image (JPEG)",
        ".png": "Image (PNG)",
        ".eml": "Email",
        ".msg": "Email",
        ".json": "JSON Data",
        ".xml": "XML Data",
        ".html": "HTML Document",
        ".zip": "Archive (ZIP)",
    }
    return ext_map.get(filepath.suffix.lower(), f"File ({filepath.suffix or 'unknown'})")


def create_metadata_file(original_path: Path, dest_path: Path) -> Path:
    """Create a companion metadata .md file in Needs_Action."""
    now = get_timestamp()
    file_type = determine_file_type(original_path)
    size_kb = round(dest_path.stat().st_size / 1024, 2)

    meta_name = f"META_{dest_path.stem}.md"
    meta_path = NEEDS_ACTION_DIR / meta_name

    content = f"""---
type: "{file_type}"
original_name: "{original_path.name}"
size_kb: {size_kb}
received_at: "{now}"
priority: "normal"
status: "pending"
---

## File Details
- **Original Name:** {original_path.name}
- **Type:** {file_type}
- **Size:** {size_kb} KB
- **Received:** {now}
- **Source:** Inbox watcher (auto-detected)

## Suggested Actions
- [ ] Review file contents and classify priority
- [ ] Create a task plan in /Plans/
- [ ] Route to appropriate handler or request approval
"""

    try:
        meta_path.write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"[ERROR] Failed to create metadata file: {e}")

    return meta_path


def process_new_file(filepath: Path) -> None:
    """Process a single new file detected in Inbox."""
    with lock:
        file_key = str(filepath)
        if file_key in processed_files:
            return
        processed_files.add(file_key)

    if not filepath.exists() or not filepath.is_file():
        return

    # Skip hidden files and temp files
    if filepath.name.startswith(".") or filepath.name.startswith("~"):
        return

    now_display = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now_display}] 📥 New file detected: {filepath.name}")

    try:
        # Copy file to Needs_Action
        dest = NEEDS_ACTION_DIR / filepath.name
        # Handle name collisions
        counter = 1
        while dest.exists():
            dest = NEEDS_ACTION_DIR / f"{filepath.stem}_{counter}{filepath.suffix}"
            counter += 1

        shutil.copy2(str(filepath), str(dest))
        print(f"[{now_display}]    ➜ Copied to Needs_Action/{dest.name}")

        # Create metadata companion
        meta_path = create_metadata_file(filepath, dest)
        print(f"[{now_display}]    ➜ Metadata: {meta_path.name}")

        # Log the action
        log_action(
            skill="filesystem_watcher",
            action=f"New file detected and triaged: {filepath.name}",
            files_affected=[str(dest), str(meta_path)],
            approval_required=False,
            result="success",
        )
        print(f"[{now_display}]    ➜ Logged to {get_today_log_path().name}")

        # Update dashboard
        update_dashboard_queue_count()
        print(f"[{now_display}]    ➜ Dashboard updated")
        print(f"[{now_display}] ✅ Processed: {filepath.name}")

    except Exception as e:
        print(f"[{now_display}] ❌ Error processing {filepath.name}: {e}")
        log_action(
            skill="filesystem_watcher",
            action=f"Error processing file: {filepath.name} — {e}",
            files_affected=[str(filepath)],
            approval_required=False,
            result="failed",
        )


class InboxHandler(FileSystemEventHandler):
    """Watchdog handler for new files in the Inbox directory."""

    def on_created(self, event: FileCreatedEvent) -> None:  # type: ignore[override]
        """Handle file creation events."""
        if event.is_directory:
            return
        # Small delay to allow file writes to finish
        time.sleep(0.5)
        process_new_file(Path(event.src_path))


def polling_backup() -> None:
    """Backup polling loop — scans Inbox every 15 seconds for missed files."""
    while True:
        try:
            time.sleep(15)
            if INBOX_DIR.exists():
                for item in INBOX_DIR.iterdir():
                    if item.is_file() and not item.name.startswith("."):
                        process_new_file(item)
        except Exception as e:
            print(f"[POLL ERROR] {e}")


def print_banner() -> None:
    """Print startup banner with vault info."""
    print("=" * 56)
    print("  🤖 AI Employee — Filesystem Watcher")
    print("=" * 56)
    print(f"  Vault Path : {VAULT_ROOT}")
    print(f"  Watching   : {INBOX_DIR}")
    print(f"  Logs       : {LOGS_DIR}")
    print(f"  Dashboard  : {DASHBOARD_PATH}")
    print(f"  Started    : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 56)
    print("  Drop files into Inbox/ to trigger processing.")
    print("  Press Ctrl+C to stop.")
    print("=" * 56)
    print()


def main() -> None:
    """Main entry point — start watcher and polling."""
    # Ensure directories exist
    for d in [INBOX_DIR, NEEDS_ACTION_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    print_banner()

    # Log startup
    log_action(
        skill="filesystem_watcher",
        action="Watcher started",
        files_affected=[],
        approval_required=False,
        result="success",
    )

    # Start watchdog observer
    observer = Observer()
    observer.schedule(InboxHandler(), str(INBOX_DIR), recursive=False)
    observer.start()
    print("[WATCHER] 👁️  Watchdog observer started (real-time monitoring)")

    # Start backup polling in a daemon thread
    poll_thread = threading.Thread(target=polling_backup, daemon=True)
    poll_thread.start()
    print("[WATCHER] 🔄 Backup polling active (15-second interval)")
    print()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[WATCHER] 🛑 Shutting down...")
        observer.stop()
        log_action(
            skill="filesystem_watcher",
            action="Watcher stopped by user",
            files_affected=[],
            approval_required=False,
            result="success",
        )
    observer.join()
    print("[WATCHER] Goodbye.")


if __name__ == "__main__":
    main()
