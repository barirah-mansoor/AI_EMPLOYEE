#!/usr/bin/env python3
"""
AI Employee Orchestrator
Manages all AI Employee processes and ensures they stay running
"""

import subprocess
import time
import signal
import sys
from pathlib import Path
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AI_Employee_Orchestrator")

class ProcessManager:
    """Manages AI Employee processes"""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.processes = {}
        self.running = True

        # Create necessary directories
        (self.vault_path / "Logs").mkdir(exist_ok=True)
        (self.vault_path / "Needs_Action").mkdir(exist_ok=True)
        (self.vault_path / "Inbox").mkdir(exist_ok=True)

    def start_gmail_watcher(self):
        """Start the Gmail watcher process"""
        try:
            process = subprocess.Popen([
                sys.executable, "-c",
                f"import sys; sys.path.insert(0, '{self.vault_path}'); "
                f"from Silver_Tier.silver_process_inbox import process_inbox; "
                f"process_inbox()"
            ])
            self.processes['gmail_watcher'] = process
            logger.info("Gmail watcher started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Gmail watcher: {e}")
            return False

    def start_scheduler(self):
        """Start the task scheduler"""
        try:
            process = subprocess.Popen([
                sys.executable, "-c",
                f"import sys; sys.path.insert(0, '{self.vault_path}'); "
                f"from Gold_Tier.Automation.orchestrator import start_scheduler; "
                f"start_scheduler()"
            ])
            self.processes['scheduler'] = process
            logger.info("Scheduler started")
            return True
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            return False

    def start_gold_orchestrator(self):
        """Start the Gold Tier orchestrator"""
        try:
            process = subprocess.Popen([
                sys.executable, "Gold_Tier/Automation/orchestrator.py"
            ])
            self.processes['gold_orchestrator'] = process
            logger.info("Gold Tier orchestrator started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Gold Tier orchestrator: {e}")
            return False

    def start_platinum_orchestrator(self):
        """Start the Platinum Tier orchestrator"""
        try:
            process = subprocess.Popen([
                sys.executable, "Platinum_Tier/orchestrator.py", "start"
            ])
            self.processes['platinum_orchestrator'] = process
            logger.info("Platinum Tier orchestrator started")
            return True
        except Exception as e:
            logger.error(f"Failed to start Platinum Tier orchestrator: {e}")
            return False

    def check_processes(self):
        """Check if all processes are running and restart if needed"""
        for name, process in self.processes.items():
            if process.poll() is not None:  # Process has died
                logger.warning(f"Process {name} died, restarting...")
                # Attempt to restart based on process type
                if name == 'gmail_watcher':
                    self.start_gmail_watcher()
                elif name == 'scheduler':
                    self.start_scheduler()
                elif name == 'gold_orchestrator':
                    self.start_gold_orchestrator()
                elif name == 'platinum_orchestrator':
                    self.start_platinum_orchestrator()

    def start_all(self):
        """Start all AI Employee processes"""
        logger.info("Starting AI Employee Orchestrator...")

        # Start all processes
        self.start_gmail_watcher()
        self.start_scheduler()
        self.start_gold_orchestrator()
        self.start_platinum_orchestrator()

        logger.info(f"Started {len(self.processes)} processes")

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # Main monitoring loop
        while self.running:
            try:
                self.check_processes()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()

    def shutdown(self):
        """Gracefully shut down all processes"""
        logger.info("Shutting down all processes...")
        self.running = False

        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"Terminated {name}")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"Force killed {name}")
            except Exception as e:
                logger.error(f"Error terminating {name}: {e}")

        logger.info("All processes terminated")


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '.')

    orchestrator = ProcessManager(vault_path)

    print("🤖 AI Employee Orchestrator")
    print("=" * 50)
    print("Starting AI Employee services...")
    print("Press Ctrl+C to stop")

    try:
        orchestrator.start_all()
    except KeyboardInterrupt:
        print("\nStopping orchestrator...")
        orchestrator.shutdown()
    except Exception as e:
        logger.error(f"Critical error: {e}")
        orchestrator.shutdown()


if __name__ == "__main__":
    main()