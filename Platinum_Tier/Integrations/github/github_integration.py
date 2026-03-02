#!/usr/bin/env python3
"""
Platinum GitHub Integration
Repository management, PR review, and issue automation
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from github import Github
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    Github = None


class GitHubIntegration:
    """GitHub integration for Platinum Tier"""

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.config = self.load_config()
        self.client = None

        if GITHUB_AVAILABLE and self.is_configured():
            self.client = Github(self.config.get('integrations', {}).get('github', {}).get('token'))

    def load_config(self) -> Dict:
        """Load configuration"""
        config_file = self.vault / "Platinum_Tier/Configs/platinum_config.yaml"
        if config_file.exists():
            import yaml
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {}

    def is_configured(self) -> bool:
        """Check if GitHub is configured"""
        github_config = self.config.get('integrations', {}).get('github', {})
        return (
            github_config.get('enabled', False) and
            github_config.get('token')
        )

    def list_repos(self) -> List[Dict]:
        """List accessible repositories"""
        if not self.client:
            return []

        repos = []
        try:
            for repo in self.client.get_user().get_repos():
                repos.append({
                    'name': repo.full_name,
                    'description': repo.description,
                    'stars': repo.stargazers_count,
                    'issues': repo.open_issues_count,
                    'url': repo.html_url
                })
        except Exception as e:
            print(f"Error listing repos: {e}")

        return repos

    def get_open_issues(self, repo_name: str) -> List[Dict]:
        """Get open issues from a repository"""
        if not self.client:
            return []

        try:
            repo = self.client.get_repo(repo_name)
            issues = []

            for issue in repo.get_issues(state='open'):
                issues.append({
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body,
                    'labels': [l.name for l in issue.labels],
                    'created_at': issue.created_at.isoformat(),
                    'url': issue.html_url
                })

            return issues
        except Exception as e:
            print(f"Error getting issues: {e}")
            return []

    def get_pull_requests(self, repo_name: str) -> List[Dict]:
        """Get open pull requests from a repository"""
        if not self.client:
            return []

        try:
            repo = self.client.get_repo(repo_name)
            prs = []

            for pr in repo.get_pulls(state='open'):
                prs.append({
                    'number': pr.number,
                    'title': pr.title,
                    'body': pr.body,
                    'user': pr.user.login,
                    'created_at': pr.created_at.isoformat(),
                    'additions': pr.additions,
                    'deletions': pr.deletions,
                    'changed_files': pr.changed_files,
                    'url': pr.html_url
                })

            return prs
        except Exception as e:
            print(f"Error getting PRs: {e}")
            return []

    def review_pr(self, repo_name: str, pr_number: int) -> Dict:
        """Generate AI-powered PR review"""
        if not self.client:
            return {'status': 'error', 'message': 'GitHub not configured'}

        try:
            repo = self.client.get_repo(repo_name)
            pr = repo.get_pull(pr_number)

            # Get the diff
            files = pr.get_files()

            review = {
                'pr_number': pr_number,
                'title': pr.title,
                'files_reviewed': [],
                'recommendations': []
            }

            for file in files[:10]:  # Limit to 10 files
                review['files_reviewed'].append({
                    'filename': file.filename,
                    'additions': file.additions,
                    'deletions': file.deletions,
                    'status': file.status
                })

            # Basic recommendations
            if pr.additions > 500:
                review['recommendations'].append("Large PR - consider breaking into smaller changes")
            if pr.changed_files > 10:
                review['recommendations'].append("Many files changed - ensure proper testing")

            return review
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def create_issue(self, repo_name: str, title: str, body: str, labels: List[str] = None) -> Dict:
        """Create a new issue"""
        if not self.client:
            return {'status': 'error', 'message': 'GitHub not configured'}

        try:
            repo = self.client.get_repo(repo_name)
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels or []
            )

            return {
                'status': 'success',
                'issue_number': issue.number,
                'url': issue.html_url
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_repo_stats(self, repo_name: str) -> Dict:
        """Get repository statistics"""
        if not self.client:
            return {}

        try:
            repo = self.client.get_repo(repo_name)

            return {
                'name': repo.full_name,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'watchers': repo.watchers_count,
                'open_issues': repo.open_issues_count,
                'language': repo.language,
                'size': repo.size,
                'created_at': repo.created_at.isoformat(),
                'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}


def main():
    """Main entry point"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    print("💎 Platinum GitHub Integration")
    print("=" * 50)

    integration = GitHubIntegration(vault_path)

    if integration.is_configured():
        print("✅ GitHub is configured")

        # List repos
        repos = integration.list_repos()
        print(f"\n📦 Found {len(repos)} repositories")

        for repo in repos[:5]:
            print(f"  • {repo['name']} ({repo['stars']} stars, {repo['issues']} issues)")
    else:
        print("⚠️ GitHub not configured")
        print("\nTo enable GitHub integration:")
        print("1. Create a Personal Access Token at https://github.com/settings/tokens")
        print("2. Update Platinum_Tier/Configs/platinum_config.yaml")
        print("\nRequired config:")
        print("""
integrations:
  github:
    enabled: true
    token: "ghp_your_token"
    repos: ["owner/repo1", "owner/repo2"]
""")


if __name__ == "__main__":
    main()
