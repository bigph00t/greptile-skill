#!/usr/bin/env python3
import subprocess
import json
from greptile_api import GreptileAPI

# Get default branches for all repos
repos = [
    "bigph00t/tiny-html-parser",
    "bigph00t/claude-mem-bridge", 
    "bigph00t/clawdbot-skills",
    "bigph00t/doc-ingestion-pipeline"
]

api = GreptileAPI()

for repo in repos:
    # Get default branch from GitHub
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--jq", ".default_branch"],
            capture_output=True, text=True
        )
        branch = result.stdout.strip() if result.returncode == 0 else "main"
    except:
        branch = "main"
    
    print(f"\n🔧 Enabling {repo} (branch: {branch})...")
    
    # Check current status first
    status = api.check_repo_status(repo, branch=branch)
    if status['success'] and status.get('status') in ['COMPLETED', 'PROCESSING']:
        print(f"   ✅ Already indexed/indexing")
        continue
    
    # Enable the repo
    result = api.enable_repo(repo, branch=branch)
    if result['success']:
        print(f"   ✅ {result['message']}")
    else:
        print(f"   ❌ {result.get('error', 'Failed')}")

