#!/usr/bin/env python3
"""
Greptile integration v2 - Based on actual Greptile workflow
Greptile is a GitHub/GitLab app that auto-reviews PRs
"""

import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class GreptileWorkflow:
    def __init__(self):
        self.config_file = Path.home() / '.greptile' / 'repos.json'
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
        
    def load_config(self):
        """Load tracked repositories and review status"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'enabled_repos': [],
                'pending_reviews': [],
                'last_check': None
            }
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def enable_repo(self, repo: str) -> Dict:
        """
        Mark repo as Greptile-enabled (actual enabling is done via web app)
        """
        if repo not in self.config['enabled_repos']:
            self.config['enabled_repos'].append(repo)
            self.save_config()
        
        return {
            'repo': repo,
            'message': f"Marked {repo} as Greptile-enabled. Make sure to enable it at https://app.greptile.com",
            'web_url': 'https://app.greptile.com'
        }
    
    def create_pr_and_wait(self, 
                          title: str, 
                          body: str,
                          branch: str = None,
                          base: str = 'main',
                          wait_minutes: int = 5) -> Dict:
        """
        Create PR and wait for Greptile review before proceeding
        """
        # Get current repo
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {'error': 'Not in a git repository'}
        
        repo_url = result.stdout.strip()
        repo_name = repo_url.split('github.com/')[-1].replace('.git', '')
        
        # Get current branch if not specified
        if not branch:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True
            )
            branch = result.stdout.strip()
        
        # Create the PR
        print(f"📝 Creating PR: {title}")
        result = subprocess.run(
            ['gh', 'pr', 'create', 
             '--title', title,
             '--body', body,
             '--base', base,
             '--head', branch],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {'error': f'Failed to create PR: {result.stderr}'}
        
        pr_url = result.stdout.strip()
        pr_number = pr_url.split('/')[-1]
        
        # Track the PR for review
        review_entry = {
            'pr_url': pr_url,
            'pr_number': pr_number,
            'repo': repo_name,
            'created_at': datetime.now().isoformat(),
            'title': title,
            'status': 'waiting_for_greptile'
        }
        
        self.config['pending_reviews'].append(review_entry)
        self.save_config()
        
        print(f"✅ PR created: {pr_url}")
        print(f"⏳ Waiting {wait_minutes} minutes for Greptile review...")
        
        # Wait for Greptile to review
        wait_seconds = wait_minutes * 60
        check_interval = 30  # Check every 30 seconds
        
        for i in range(0, wait_seconds, check_interval):
            time.sleep(check_interval)
            
            # Check if Greptile has commented
            result = subprocess.run(
                ['gh', 'pr', 'view', pr_number, '--json', 'comments'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                pr_data = json.loads(result.stdout)
                greptile_comments = [
                    c for c in pr_data.get('comments', [])
                    if 'greptile' in c.get('author', {}).get('login', '').lower()
                ]
                
                if greptile_comments:
                    print(f"🔍 Greptile has reviewed! Found {len(greptile_comments)} comments")
                    
                    # Update status
                    for r in self.config['pending_reviews']:
                        if r['pr_number'] == pr_number:
                            r['status'] = 'reviewed'
                            r['reviewed_at'] = datetime.now().isoformat()
                            r['comment_count'] = len(greptile_comments)
                    self.save_config()
                    
                    return {
                        'pr_url': pr_url,
                        'status': 'reviewed',
                        'comments': greptile_comments,
                        'message': 'Greptile review complete!'
                    }
            
            remaining = wait_seconds - i - check_interval
            if remaining > 0:
                print(f"⏳ Still waiting... {remaining}s remaining")
        
        print("⏰ Wait time expired. Greptile review may still be pending.")
        return {
            'pr_url': pr_url,
            'status': 'timeout',
            'message': f'Created PR but Greptile review not detected after {wait_minutes} minutes'
        }
    
    def check_pr_reviews(self, repo: Optional[str] = None) -> List[Dict]:
        """
        Check status of Greptile reviews on recent PRs
        """
        cmd = ['gh', 'pr', 'list', '--json', 'number,title,url,createdAt,comments']
        if repo:
            cmd.extend(['--repo', repo])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return []
        
        prs = json.loads(result.stdout)
        reviewed_prs = []
        
        for pr in prs:
            # Check if Greptile has commented
            greptile_comments = [
                c for c in pr.get('comments', [])
                if 'greptile' in c.get('author', {}).get('login', '').lower()
            ]
            
            if greptile_comments:
                reviewed_prs.append({
                    'pr_number': pr['number'],
                    'title': pr['title'],
                    'url': pr['url'],
                    'greptile_comments': len(greptile_comments),
                    'created_at': pr['createdAt']
                })
        
        return reviewed_prs
    
    def setup_repos(self, repos: List[str]) -> str:
        """
        Guide for setting up Greptile on repos
        """
        message = "🔧 **Greptile Setup Guide**\n\n"
        message += "1. Go to https://app.greptile.com\n"
        message += "2. Install the GitHub app if not already done\n"
        message += "3. Select these repositories:\n\n"
        
        for repo in repos:
            self.enable_repo(repo)
            message += f"   - {repo}\n"
        
        message += "\n4. Wait for indexing (1-2 hours for large repos)\n"
        message += "5. Greptile will automatically review new PRs!\n"
        
        return message
    
    def wait_for_review(self, pr_url: str, wait_minutes: int = 10) -> Dict:
        """
        Wait for Greptile to review an existing PR
        """
        pr_number = pr_url.split('/')[-1]
        
        print(f"⏳ Waiting up to {wait_minutes} minutes for Greptile review on PR #{pr_number}...")
        
        wait_seconds = wait_minutes * 60
        check_interval = 30
        
        for i in range(0, wait_seconds, check_interval):
            result = subprocess.run(
                ['gh', 'pr', 'view', pr_number, '--json', 'comments'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                pr_data = json.loads(result.stdout)
                greptile_comments = [
                    c for c in pr_data.get('comments', [])
                    if 'greptile' in c.get('author', {}).get('login', '').lower()
                ]
                
                if greptile_comments:
                    return {
                        'status': 'reviewed',
                        'comment_count': len(greptile_comments),
                        'comments': greptile_comments
                    }
            
            time.sleep(check_interval)
            print(f"Still waiting... {wait_seconds - i - check_interval}s remaining")
        
        return {'status': 'timeout', 'message': 'No Greptile review detected'}


# CLI interface
if __name__ == "__main__":
    import sys
    
    greptile = GreptileWorkflow()
    
    if len(sys.argv) < 2:
        print("Usage: greptile_v2.py [setup|status|create-pr-wait|wait|check] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "setup":
        repos = [
            "bigph00t/tiny-html-parser",
            "bigph00t/claude-mem-bridge",
            "bigph00t/clawdbot-skills",
            "bigph00t/doc-ingestion-pipeline"
        ]
        print(greptile.setup_repos(repos))
    
    elif command == "create-pr-wait":
        if len(sys.argv) < 4:
            print("Usage: greptile_v2.py create-pr-wait <title> <body> [wait-minutes]")
            sys.exit(1)
        
        title = sys.argv[2]
        body = sys.argv[3]
        wait_minutes = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        
        result = greptile.create_pr_and_wait(title, body, wait_minutes=wait_minutes)
        print(json.dumps(result, indent=2))
    
    elif command == "wait":
        if len(sys.argv) < 3:
            print("Usage: greptile_v2.py wait <pr-url> [wait-minutes]")
            sys.exit(1)
        
        pr_url = sys.argv[2]
        wait_minutes = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        result = greptile.wait_for_review(pr_url, wait_minutes)
        print(json.dumps(result, indent=2))
    
    elif command == "check":
        repo = sys.argv[2] if len(sys.argv) > 2 else None
        reviews = greptile.check_pr_reviews(repo)
        
        if reviews:
            print(f"\n📝 PRs with Greptile reviews:")
            for r in reviews:
                print(f"- PR #{r['pr_number']}: {r['title']}")
                print(f"  Comments: {r['greptile_comments']}")
                print(f"  URL: {r['url']}\n")
        else:
            print("No PRs with Greptile reviews found")
    
    elif command == "status":
        print(f"\n🔍 Greptile Status")
        print(f"Enabled repos: {len(greptile.config['enabled_repos'])}")
        for repo in greptile.config['enabled_repos']:
            print(f"  - {repo}")
        
        pending = [r for r in greptile.config['pending_reviews'] if r['status'] == 'waiting_for_greptile']
        if pending:
            print(f"\nPending reviews: {len(pending)}")
            for r in pending:
                print(f"  - {r['repo']} PR #{r['pr_number']}: {r['title']}")