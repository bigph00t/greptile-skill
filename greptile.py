#!/usr/bin/env python3
"""
Greptile Workflow - Simple commands for enabling repos and getting PR reviews
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from greptile_api import GreptileAPI
import requests

class GreptileWorkflow:
    def __init__(self):
        self.api = GreptileAPI()
        self.notes_dir = Path.home() / "greptile-reviews"
        self.notes_dir.mkdir(exist_ok=True)
    
    def enable(self, repo: str) -> bool:
        """Enable a repo and wait for indexing"""
        print(f"\n🔧 Enabling {repo}...")
        
        # Check if already indexed
        status = self.api.check_repo_status(repo)
        if status.get('success') and status.get('status') == 'COMPLETED':
            print(f"✅ {repo} is already indexed!")
            return True
        
        # Enable the repo (auto-detects branch)
        result = self.api.enable_repo(repo)
        
        if not result['success']:
            if "already being processed" in result.get('error', ''):
                print(f"⏳ {repo} is already being indexed...")
            else:
                print(f"❌ Failed to enable: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"✅ {result['message']}")
        
        # Wait for indexing
        print(f"\n⏳ Waiting for indexing to complete...")
        wait_result = self.api.wait_for_indexing(repo, timeout_minutes=30)
        
        if wait_result['success']:
            print(f"✅ {repo} is ready for reviews!")
            return True
        else:
            print(f"❌ Indexing failed: {wait_result.get('error', 'Unknown error')}")
            return False
    
    def wait_for_review(self, pr_url: str, save_notes: bool = True) -> dict:
        """Trigger and get Greptile review on a PR"""
        print(f"\n🔍 Triggering review on: {pr_url}")
        
        # Use manual review via query API
        from greptile_review import GreptileReviewer
        reviewer = GreptileReviewer()
        
        result = reviewer.review_pr_via_query(pr_url)
        if result['success']:
            print(f"\n✅ Review completed!")
            
            # Save notes if requested
            if save_notes:
                self._save_review_notes(
                    result['pr_info']['repo'], 
                    result['pr_info']['pr_number'], 
                    result['review']
                )
            
            return {
                "success": True,
                "review": result['review'],
                "pr": pr_url
            }
        else:
            print(f"\n❌ Review failed: {result.get('error', 'Unknown error')}")
            return {"success": False, "error": result.get('error', 'Failed to get review')}
        
        owner = parts[-4]
        repo_name = parts[-3]
        pr_number = parts[-1]
        repo = f"{owner}/{repo_name}"
        
        # Poll for review (up to 5 minutes)
        max_attempts = 30
        for i in range(max_attempts):
            try:
                # Check PR comments for Greptile review
                result = subprocess.run(
                    ["gh", "pr", "view", pr_number, "--repo", repo, "--comments", "--json", "comments"],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    comments = data.get('comments', [])
                    
                    # Look for Greptile comment
                    for comment in comments:
                        if 'greptile' in comment.get('author', {}).get('login', '').lower():
                            review_body = comment.get('body', '')
                            print(f"\n✅ Review received!")
                            print(f"\n📝 Review:\n{review_body}")
                            
                            # Save notes if requested
                            if save_notes:
                                self._save_review_notes(repo, pr_number, review_body)
                            
                            return {
                                "success": True,
                                "review": review_body,
                                "pr": pr_url
                            }
            except Exception as e:
                print(f"Error checking PR: {e}")
            
            # Wait before next check
            if i < max_attempts - 1:
                print(f"\r⏳ Waiting for review... ({i+1}/{max_attempts})", end='', flush=True)
                time.sleep(10)
        
        print("\n❌ No review received within 5 minutes")
        return {"success": False, "error": "Timeout waiting for review"}
    
    def _save_review_notes(self, repo: str, pr_number: str, review: str):
        """Save review notes to file"""
        timestamp = time.strftime("%Y-%m-%d_%H-%M")
        filename = f"{repo.replace('/', '_')}_{pr_number}_{timestamp}.md"
        filepath = self.notes_dir / filename
        
        content = f"""# Greptile Review: {repo} PR #{pr_number}
Date: {time.strftime("%Y-%m-%d %H:%M")}

## Review

{review}

---
"""
        
        filepath.write_text(content)
        print(f"\n💾 Review saved to: {filepath}")
    
    def status(self):
        """Check status of all recently reviewed PRs"""
        print("\n📊 Recent Reviews:")
        
        # List recent review files
        review_files = sorted(self.notes_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
        
        if not review_files:
            print("No reviews found yet")
            return
        
        for file in review_files:
            print(f"  - {file.name}")


def main():
    if len(sys.argv) < 2:
        print("""
Greptile Workflow Commands:

  Enable repo and wait for indexing:
    greptile enable <repo>
    
  Wait for PR review:
    greptile review <pr-url>
    
  Check recent reviews:
    greptile status
    
Examples:
    greptile enable bigph00t/my-app
    greptile review https://github.com/bigph00t/my-app/pull/123
""")
        sys.exit(1)
    
    workflow = GreptileWorkflow()
    command = sys.argv[1]
    
    if command == "enable":
        if len(sys.argv) < 3:
            print("Usage: greptile enable <repo>")
            sys.exit(1)
        workflow.enable(sys.argv[2])
    
    elif command == "review":
        if len(sys.argv) < 3:
            print("Usage: greptile review <pr-url>")
            sys.exit(1)
        workflow.wait_for_review(sys.argv[2])
    
    elif command == "status":
        workflow.status()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()