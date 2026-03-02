#!/usr/bin/env python3
"""
Platinum Notion Integration
Sync tasks, projects, and knowledge with Notion workspace
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from notion_client import Client as NotionClient
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False
    NotionClient = None


class NotionIntegration:
    """Notion workspace integration for Platinum Tier"""

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.config = self.load_config()
        self.client = None

        if NOTION_AVAILABLE and self.is_configured():
            self.client = NotionClient(auth=self.config.get('integrations', {}).get('notion', {}).get('api_key'))

    def load_config(self) -> Dict:
        """Load configuration"""
        config_file = self.vault / "Platinum_Tier/Configs/platinum_config.yaml"
        if config_file.exists():
            import yaml
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}

    def is_configured(self) -> bool:
        """Check if Notion is configured"""
        notion_config = self.config.get('integrations', {}).get('notion', {})
        return (
            notion_config.get('enabled', False) and
            notion_config.get('api_key')
        )

    def sync_tasks_to_notion(self, tasks: List[Dict]) -> Dict:
        """Sync tasks to Notion database"""
        if not self.client:
            return {'status': 'error', 'message': 'Notion not configured'}

        notion_config = self.config.get('integrations', {}).get('notion', {})
        tasks_db = notion_config.get('databases', {}).get('tasks')

        if not tasks_db:
            return {'status': 'error', 'message': 'Tasks database not configured'}

        synced = []
        for task in tasks[:10]:  # Limit to 10 at a time
            try:
                # Create page in Notion
                page = self.client.pages.create(
                    parent={"database_id": tasks_db},
                    properties={
                        "Title": {"title": [{"text": {"content": task.get('subject', 'Untitled')}}]},
                        "Status": {"select": {"name": task.get('status', 'To Do')}},
                        "Priority": {"select": {"name": task.get('priority', 'Medium')}}
                    }
                )
                synced.append({'task': task.get('subject'), 'page_id': page['id']})
            except Exception as e:
                synced.append({'task': task.get('subject'), 'error': str(e)})

        return {'status': 'success', 'synced': synced}

    def sync_from_notion(self) -> List[Dict]:
        """Pull tasks from Notion database"""
        if not self.client:
            return []

        notion_config = self.config.get('integrations', {}).get('notion', {})
        tasks_db = notion_config.get('databases', {}).get('tasks')

        if not tasks_db:
            return []

        try:
            response = self.client.databases.query(database_id=tasks_db)
            tasks = []

            for page in response.get('results', []):
                props = page.get('properties', {})
                title = props.get('Title', {}).get('title', [{}])[0].get('text', {}).get('content', 'Untitled')
                status = props.get('Status', {}).get('select', {}).get('name', 'To Do')

                tasks.append({
                    'id': page['id'],
                    'subject': title,
                    'status': status,
                    'source': 'notion'
                })

            return tasks
        except Exception as e:
            print(f"Error syncing from Notion: {e}")
            return []

    def create_page(self, title: str, content: str, database_id: str = None) -> Dict:
        """Create a new page in Notion"""
        if not self.client:
            return {'status': 'error', 'message': 'Notion not configured'}

        notion_config = self.config.get('integrations', {}).get('notion', {})
        db_id = database_id or notion_config.get('databases', {}).get('knowledge')

        try:
            if db_id:
                page = self.client.pages.create(
                    parent={"database_id": db_id},
                    properties={
                        "Title": {"title": [{"text": {"content": title}}]}
                    }
                )
            else:
                return {'status': 'error', 'message': 'No database specified'}

            return {'status': 'success', 'page_id': page['id']}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def search_pages(self, query: str) -> List[Dict]:
        """Search Notion pages"""
        if not self.client:
            return []

        try:
            response = self.client.search(query=query)
            return response.get('results', [])
        except Exception as e:
            print(f"Search error: {e}")
            return []


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    print("💎 Platinum Notion Integration")
    print("=" * 50)

    integration = NotionIntegration(vault_path)

    if integration.is_configured():
        print("✅ Notion is configured")

        # Sync from Notion
        tasks = integration.sync_from_notion()
        print(f"\n📥 Found {len(tasks)} tasks in Notion")
    else:
        print("⚠️ Notion not configured")
        print("\nTo enable Notion integration:")
        print("1. Create a Notion integration at https://www.notion.so/my-integrations")
        print("2. Get your API key")
        print("3. Share databases with your integration")
        print("4. Update Platinum_Tier/Configs/platinum_config.yaml")


if __name__ == "__main__":
    main()
