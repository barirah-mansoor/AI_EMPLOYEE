#!/usr/bin/env python3
"""
Process Watchdog - Monitors and restarts AI Employee processes
"""

import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
VAULT_PATH = Path("/mnt/c/Users/Admin/AI_Employee_Vault")
PID_DIR = Path.home() / ".ai_employee_pids"
LOG_FILE = VAULT_PATH / "Logs" / "watchdog.log"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"

# Processes to monitor
PROCESSES = {
    "orchestrator": "Gold_Tier/Automation/orchestrator.py",
    "filesystem_watcher": "Silver_Tier/filesystem_watcher.py",
    "whatsapp_watcher": "whatsapp_watcher.py",
    "finance_watcher": "finance_watcher.py",
}

CHECK_INTERVAL = 60  # seconds


def log(message: str):
    """Log to watchdog log file."""
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print(log_line.strip())


def get_pid(process_name: str) -> Optional[int]:
    """Get PID for a process from PID file."""
    pid_file = PID_DIR / f"{process_name}.pid"

    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            return pid
        except (ValueError, IOError):
            return None

    return None


def save_pid(process_name: str, pid: int):
    """Save PID to file."""
    PID_DIR.mkdir(parents=True, exist_ok=True)
    pid_file = PID_DIR / f"{process_name}.pid"
    pid_file.write_text(str(pid))


def is_process_running(pid: int) -> bool:
    """Check if a process is running."""
    try:
        # Check if process exists
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def restart_process(process_name: str, script_path: str):
    """Restart a failed process."""
    log(f"Restarting {process_name}...")

    try:
        # Start the process
        process = subprocess.Popen(
            ["python3", str(VAULT_PATH / script_path)],
            cwd=str(VAULT_PATH),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        # Save new PID
        save_pid(process_name, process.pid)

        # Create alert file
        create_restart_alert(process_name, process.pid)

        log(f"Restarted {process_name} with PID {process.pid}")

    except Exception as e:
        log(f"Failed to restart {process_name}: {e}")


def create_restart_alert(process_name: str, new_pid: int):
    """Create Needs_Action alert for process restart."""
    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ALERT_process_restart_{process_name}_{timestamp}.md"

    content = f"""---
type: system_alert
process: "{process_name}"
status: resolved
created: "{datetime.now().isoformat()}"
---

# Process Restart Alert

**Process:** {process_name}
**New PID:** {new_pid}
**Time:** {datetime.now().isoformat()}

The watchdog detected the process was not running and restarted it automatically.

## Resolution

- [x] Process restarted successfully
- [ ] Review logs if issue persists
"""

    alert_path = NEEDS_ACTION / filename
    alert_path.write_text(content)


def send_notification(title: str, message: str):
    """Send desktop notification if available."""
    try:
        # Try notify-send on Linux
        subprocess.run(
            ["notify-send", title, message],
            check=False,
            capture_output=True
        )
    except Exception:
        pass  # Notification not available, ignore


def check_processes() -> Dict[str, bool]:
    """Check all monitored processes."""
    status = {}

    for process_name, script_path in PROCESSES.items():
        pid = get_pid(process_name)

        if pid is None:
            status[process_name] = False
            continue

        if is_process_running(pid):
            status[process_name] = True
        else:
            status[process_name] = False
            log(f"Process {process_name} (PID {pid}) is not running!")
            restart_process(process_name, script_path)

    return status


def run_watchdog():
    """Main watchdog loop."""
    log("Watchdog started")
    PID_DIR.mkdir(parents=True, exist_ok=True)

    send_notification("AI Employee Watchdog", "Process watchdog started")

    while True:
        try:
            status = check_processes()

            running = sum(1 for v in status.values() if v)
            total = len(status)

            if running < total:
                log(f"Status: {running}/{total} processes running")
                send_notification(
                    "Process Alert",
                    f"{total - running} process(es) restarted"
                )
            else:
                log(f"All {total} processes running")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log("Watchdog stopped")
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(CHECK_INTERVAL)


def start_watchdog():
    """Start the watchdog in background."""
    process = subprocess.Popen(
        [sys.executable, __file__],
        cwd=str(VAULT_PATH),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    save_pid("watchdog", process.pid)
    print(f"Watchdog started with PID {process.pid}")


def stop_watchdog():
    """Stop the watchdog."""
    pid = get_pid("watchdog")

    if pid and is_process_running(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            print("Watchdog stopped")
        except OSError as e:
            print(f"Failed to stop watchdog: {e}")
    else:
        print("Watchdog not running")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Employee Process Watchdog")
    parser.add_argument("--once", action="store_true", help="Check once instead of loop")
    args = parser.parse_args()

    if args.once:
        status = check_processes()
        print(f"Process status: {status}")
    else:
        run_watchdog()
