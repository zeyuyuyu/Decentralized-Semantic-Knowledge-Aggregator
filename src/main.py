import os
import git
import time
import requests
from datetime import datetime
from typing import Dict, List

class GitSentinel:
    def __init__(self, repo_path: str, webhook_url: str = None):
        self.repo_path = repo_path
        self.webhook_url = webhook_url
        self.repo = git.Repo(repo_path)
        self.last_commit = self.repo.head.commit

    def check_changes(self) -> Dict:
        """Check repository for new changes"""
        current = self.repo.head.commit
        if current != self.last_commit:
            changes = {
                'new_commits': [],
                'modified_files': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Get all new commits
            for commit in self.repo.iter_commits(f'{self.last_commit}..HEAD'):
                changes['new_commits'].append({
                    'hash': commit.hexsha,
                    'author': commit.author.name,
                    'message': commit.message,
                    'date': commit.committed_datetime.isoformat()
                })
            
            # Get modified files
            diff = self.last_commit.diff(current)
            changes['modified_files'] = [d.a_path for d in diff]
            
            self.last_commit = current
            return changes
        return None

    def notify(self, changes: Dict) -> None:
        """Send webhook notification about changes"""
        if self.webhook_url and changes:
            try:
                requests.post(
                    self.webhook_url,
                    json=changes,
                    headers={'Content-Type': 'application/json'}
                )
            except requests.exceptions.RequestException as e:
                print(f'Failed to send webhook notification: {e}')

    def monitor(self, interval: int = 60) -> None:
        """Continuously monitor repository for changes"""
        print(f'Starting GitSentinel monitoring for {self.repo_path}')
        while True:
            try:
                self.repo.remote().fetch()
                changes = self.check_changes()
                if changes:
                    print(f'Changes detected: {len(changes["new_commits"])} new commits')
                    self.notify(changes)
                time.sleep(interval)
            except KeyboardInterrupt:
                print('\nStopping GitSentinel monitoring')
                break
            except Exception as e:
                print(f'Error during monitoring: {e}')
                time.sleep(interval)

def main():
    repo_path = os.getenv('REPO_PATH', '.')
    webhook_url = os.getenv('WEBHOOK_URL')
    interval = int(os.getenv('CHECK_INTERVAL', '60'))
    
    sentinel = GitSentinel(repo_path, webhook_url)
    sentinel.monitor(interval)

if __name__ == '__main__':
    main()