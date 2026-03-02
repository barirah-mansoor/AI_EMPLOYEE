#!/usr/bin/env python3
"""
Base Watcher Template for AI Employee
Following the hackathon pattern for all watchers
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
import json
from datetime import datetime

class BaseWatcher(ABC):
    """Template for all watcher implementations"""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        # Set up logging
        logging.basicConfig(level=logging.INFO)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def run(self):
        """Main run loop for the watcher"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except Exception as e:
                self.logger.error(f'Error in {self.__class__.__name__}: {e}')
            time.sleep(self.check_interval)


# Example implementation - File System Watcher
class FileSystemWatcher(BaseWatcher):
    """Monitor file system changes and create action items"""

    def __init__(self, vault_path: str, watch_folder: str = "Inbox", check_interval: int = 30):
        super().__init__(vault_path, check_interval)
        self.watch_folder = Path(vault_path) / watch_folder
        self.processed_files = set()

        # Create necessary directories
        self.watch_folder.mkdir(exist_ok=True)
        self.needs_action.mkdir(exist_ok=True)

    def check_for_updates(self) -> list:
        """Check for new files in the watch folder"""
        new_files = []
        for file_path in self.watch_folder.iterdir():
            if file_path.is_file() and file_path not in self.processed_files:
                new_files.append(file_path)
                self.processed_files.add(file_path)
        return new_files

    def create_action_file(self, file_path: Path) -> Path:
        """Create an action file for the new file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f"FILE_{timestamp}_{file_path.name.replace('.', '_')}.md"
        action_filepath = self.needs_action / action_filename

        content = f"""---
type: file_drop
original_name: {file_path.name}
size_bytes: {file_path.stat().st_size}
received: {datetime.now().isoformat()}
status: pending
---

# New File Received

A new file has been dropped in the Inbox:

**Original Name:** {file_path.name}
**Size:** {file_path.stat().st_size} bytes
**Location:** {file_path}

## Suggested Actions
- [ ] Review file content
- [ ] Determine appropriate action
- [ ] Process or archive as needed
"""

        action_filepath.write_text(content)
        self.logger.info(f"Created action file: {action_filepath}")
        return action_filepath


# Example implementation - Generic Event Watcher
class EventWatcher(BaseWatcher):
    """Generic watcher that can be extended for specific events"""

    def __init__(self, vault_path: str, event_source: str, check_interval: int = 60):
        super().__init__(vault_path, check_interval)
        self.event_source = event_source
        self.last_check = datetime.now()

    def check_for_updates(self) -> list:
        """Check for new events from the source"""
        # This would be overridden by specific implementations
        # For demonstration, return empty list
        return []

    def create_action_file(self, event) -> Path:
        """Create action file for the event"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f"EVENT_{self.event_source}_{timestamp}.md"
        action_filepath = self.needs_action / action_filename

        content = f"""---
type: event
source: {self.event_source}
timestamp: {datetime.now().isoformat()}
status: pending
---

# New Event Detected

Event from: {self.event_source}
Time: {datetime.now().isoformat()}

## Details
{event}

## Suggested Actions
- [ ] Analyze event
- [ ] Take appropriate action
- [ ] Log outcome
"""

        action_filepath.write_text(content)
        return action_filepath


def main():
    """Example usage"""
    import sys
    vault_path = sys.argv[1] if len(sys.argv) > 1 else "."

    # Example: Start a file system watcher
    watcher = FileSystemWatcher(vault_path, "Inbox", 30)
    print(f"Starting file system watcher for vault: {vault_path}")
    print("Press Ctrl+C to stop...")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nWatcher stopped by user")


if __name__ == "__main__":
    main()
