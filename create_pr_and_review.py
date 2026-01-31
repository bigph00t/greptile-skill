#!/usr/bin/env python3
"""
Helper to create a PR and immediately wait for Greptile review
"""

import sys
import subprocess
import json
import time

def create_pr_and_wait_review(title: str, body: str = ""):
    """Create PR and wait for Greptile review"""
    
    # Create the PR
    print(f"📝 Creating PR: {title}")
    result = subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body or "Auto-generated PR"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Failed to create PR: {result.stderr}")
        return False
    
    # Extract PR URL from output
    pr_url = result.stdout.strip()
    print(f"✅ PR created: {pr_url}")
    
    # Wait a moment for GitHub to process
    time.sleep(2)
    
    # Now wait for review
    print("\n🔍 Waiting for Greptile review...")
    import os
    script_path = os.path.expanduser("~/skills/greptile/greptile.py")
    subprocess.run(["python", script_path, "review", pr_url])
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: create_pr_and_review.py <title> [body]")
        sys.exit(1)
    
    title = sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else ""
    
    create_pr_and_wait_review(title, body)