#!/usr/bin/env python3
"""
AI Employee Automation Scheduler for Silver Tier
Handles scheduled execution of AI skills
"""

import schedule
import time
import subprocess
import json
import logging
from datetime import datetime
from pathlib import Path
import threading
import signal
import sys


class AIEmployeeScheduler:
    def __init__(self):
        self.vault_path = Path.home() / "AI_Employee_Vault"
        self.running = True
        self.setup_logging()
        self.load_schedule_config()

        # Handle graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def setup_logging(self):
        """Setup logging for scheduler"""
        log_path = self.vault_path / "Silver_Tier/Automation/Logs"
        log_path.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path / 'scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_schedule_config(self):
        """Load scheduling configuration"""
        config_file = self.vault_path / "Silver_Tier/Automation/schedule_config.json"

        default_config = {
            "enabled": True,
            "daily_tasks": {
                "08:00": ["process_gmail"],
                "09:00": ["silver_briefing"],
                "12:00": ["process_gmail", "process_inbox"],
                "17:00": ["daily_briefing", "send_emails"],
                "22:00": ["system_monitor"]
            },
            "weekly_tasks": {
                "monday_09:00": ["audit_week"]
            },
            "hourly_tasks": ["process_gmail"]
        }

        if not config_file.exists():
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            self.config = default_config
        else:
            with open(config_file, 'r') as f:
                self.config = json.load(f)

    def run_skill(self, skill_name):
        """Execute an AI Employee skill"""
        try:
            self.logger.info(f"🤖 Running scheduled skill: {skill_name}")

            # Run skill via the AI Employee system
            cmd = [
                'bash', '-c',
                f'cd {self.vault_path} && bash run_ai_employee.sh {skill_name}'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

            if result.returncode == 0:
                self.logger.info(f"✅ Scheduled skill completed: {skill_name}")
                return True
            else:
                self.logger.error(f"❌ Scheduled skill failed: {skill_name}")
                self.logger.error(f"Error output: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.error(f"⏰ Skill {skill_name} timed out after 10 minutes")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error running {skill_name}: {e}")
            return False

    def setup_schedule(self):
        """Setup all scheduled tasks"""
        if not self.config.get("enabled", True):
            self.logger.info("📴 Scheduler is disabled in config")
            return

        # Setup daily tasks
        for time_str, skills in self.config.get("daily_tasks", {}).items():
            for skill in skills:
                schedule.every().day.at(time_str).do(self.run_skill, skill)

        # Setup hourly tasks
        for skill in self.config.get("hourly_tasks", []):
            schedule.every().hour.at(":00").do(self.run_skill, skill)

        # Setup weekly tasks
        for day_time, skills in self.config.get("weekly_tasks", {}).items():
            day, time_str = day_time.split("_")
            for skill in skills:
                getattr(schedule.every(), day.lower()).at(time_str).do(self.run_skill, skill)

        self.logger.info("📅 Scheduler configured with:")
        self.logger.info(f"  • Daily tasks: {len(self.config.get('daily_tasks', {}))}")
        self.logger.info(f"  • Hourly tasks: {len(self.config.get('hourly_tasks', []))}")
        self.logger.info(f"  • Weekly tasks: {len(self.config.get('weekly_tasks', {}))}")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False

    def run(self):
        """Main scheduler loop"""
        self.setup_schedule()
        self.logger.info("🚀 AI Employee Scheduler started...")

        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                break

        self.logger.info("👋 AI Employee Scheduler stopped")


if __name__ == "__main__":
    scheduler = AIEmployeeScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("\n👋 Scheduler stopped by user")
    sys.exit(0)
