#!/usr/bin/env python3
"""
Greptile integration for automated code reviews
"""

import os
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class GreptileManager:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GREPTILE_API_KEY')
        if not self.api_key:
            # Try to read from secrets
            secret_path = Path.home() / 'secrets' / 'greptile_api_key'
            if secret_path.exists():
                self.api_key = secret_path.read_text().strip()
        
        if not self.api_key:
            raise ValueError("Greptile API key not found")
        
        self.base_url = "https://api.greptile.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Track repos in a local file
        self.config_file = Path.home() / '.greptile' / 'repos.json'
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
    
    def load_config(self):
        """Load tracked repositories"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'repos': [],
                'pending_reviews': [],
                'last_check': None
            }
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_repo(self, repo: str) -> Dict:
        """Enable Greptile on a repository"""
        # Parse repo name
        if '/' not in repo:
            # Try to get from git remote
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                repo = url.split('github.com/')[-1].replace('.git', '')
        
        # Call Greptile API to index the repo
        response = requests.post(
            f"{self.base_url}/repos",
            headers=self.headers,
            json={
                "repository": repo,
                "branch": "main"  # Could make this configurable
            }
        )
        
        if response.status_code == 200:
            # Add to tracked repos
            if repo not in self.config['repos']:
                self.config['repos'].append(repo)
                self.save_config()
            
            return {
                'success': True,
                'repo': repo,
                'message': f"Greptile enabled on {repo}"
            }
        else:
            return {
                'success': False,
                'repo': repo,
                'error': response.text
            }
    
    def trigger_review(self, pr_url: str) -> Dict:
        """Trigger a code review on a PR"""
        # Extract repo and PR number from URL
        # Format: https://github.com/owner/repo/pull/123
        parts = pr_url.split('/')
        repo = f"{parts[-4]}/{parts[-3]}"
        pr_number = parts[-1]
        
        # Ensure repo is set up
        if repo not in self.config['repos']:
            setup_result = self.setup_repo(repo)
            if not setup_result['success']:
                return setup_result
        
        # Trigger review
        response = requests.post(
            f"{self.base_url}/reviews",
            headers=self.headers,
            json={
                "repository": repo,
                "pr_number": int(pr_number),
                "review_type": "comprehensive"  # or "security", "performance"
            }
        )
        
        if response.status_code == 200:
            review_id = response.json().get('review_id')
            
            # Track pending review
            self.config['pending_reviews'].append({
                'review_id': review_id,
                'pr_url': pr_url,
                'repo': repo,
                'pr_number': pr_number,
                'started_at': datetime.now().isoformat(),
                'status': 'pending'
            })
            self.save_config()
            
            return {
                'success': True,
                'review_id': review_id,
                'message': f"Review triggered for PR #{pr_number}"
            }
        else:
            return {
                'success': False,
                'error': response.text
            }
    
    def check_review_status(self, review_id: str) -> Dict:
        """Check the status of a review"""
        response = requests.get(
            f"{self.base_url}/reviews/{review_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.text}
    
    def get_pending_reviews(self) -> List[Dict]:
        """Get all pending reviews"""
        pending = []
        updated_reviews = []
        
        for review in self.config['pending_reviews']:
            if review['status'] == 'pending':
                # Check current status
                status = self.check_review_status(review['review_id'])
                
                if 'error' not in status:
                    review['status'] = status.get('status', 'pending')
                    review['last_checked'] = datetime.now().isoformat()
                    
                    if review['status'] == 'pending':
                        pending.append(review)
                
                updated_reviews.append(review)
            else:
                updated_reviews.append(review)
        
        self.config['pending_reviews'] = updated_reviews
        self.config['last_check'] = datetime.now().isoformat()
        self.save_config()
        
        return pending
    
    def setup_all_repos(self, repos: List[str]) -> List[Dict]:
        """Set up multiple repositories"""
        results = []
        for repo in repos:
            result = self.setup_repo(repo)
            results.append(result)
        return results
    
    def create_reminder(self) -> str:
        """Create a reminder message for pending reviews"""
        pending = self.get_pending_reviews()
        
        if not pending:
            return "No pending code reviews! 🎉"
        
        message = f"📝 **{len(pending)} Pending Code Reviews:**\n\n"
        
        for review in pending:
            pr_url = review['pr_url']
            started = review['started_at']
            
            # Calculate age
            start_time = datetime.fromisoformat(started)
            age = datetime.now() - start_time
            age_str = f"{age.total_seconds() / 3600:.1f} hours ago"
            
            message += f"- [{review['repo']} PR #{review['pr_number']}]({pr_url})\n"
            message += f"  Started: {age_str}\n\n"
        
        return message


# CLI interface
if __name__ == "__main__":
    import sys
    
    manager = GreptileManager()
    
    if len(sys.argv) < 2:
        print("Usage: greptile.py [setup|review|status|pending|setup-all] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "setup":
        if len(sys.argv) < 3:
            print("Usage: greptile.py setup <repo>")
            sys.exit(1)
        
        result = manager.setup_repo(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "setup-all":
        repos = [
            "bigph00t/tiny-html-parser",
            "bigph00t/claude-mem-bridge", 
            "bigph00t/clawdbot-skills",
            "bigph00t/doc-ingestion-pipeline"
        ]
        results = manager.setup_all_repos(repos)
        for result in results:
            print(json.dumps(result, indent=2))
    
    elif command == "review":
        if len(sys.argv) < 3:
            print("Usage: greptile.py review <pr-url>")
            sys.exit(1)
        
        result = manager.trigger_review(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "pending":
        pending = manager.get_pending_reviews()
        print(f"\n{len(pending)} pending reviews:")
        for review in pending:
            print(f"- {review['repo']} PR #{review['pr_number']}")
    
    elif command == "status":
        reminder = manager.create_reminder()
        print(reminder)