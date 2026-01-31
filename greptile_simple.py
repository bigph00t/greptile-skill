#!/usr/bin/env python3
"""
Simplified Greptile workflow for AI agents
"""

import sys
import subprocess
from pathlib import Path
from greptile_api import GreptileAPI
from greptile_review import GreptileReviewer

def main():
    if len(sys.argv) < 2:
        print("""
Greptile Simple Commands:

  greptile_simple enable <repo>           - Enable repo for code analysis
  greptile_simple review <pr-url>         - Get AI review on a PR
  greptile_simple review-post <pr-url>    - Get review and post as comment

Examples:
  greptile_simple enable bigph00t/my-app
  greptile_simple review https://github.com/owner/repo/pull/123
""")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "enable":
        if len(sys.argv) < 3:
            print("Usage: greptile_simple enable <repo>")
            sys.exit(1)
        
        api = GreptileAPI()
        repo = sys.argv[2]
        
        print(f"🔧 Enabling {repo}...")
        result = api.enable_repo(repo)
        
        if result['success']:
            print(f"✅ {result['message']}")
            
            # Wait for indexing
            print("⏳ Waiting for indexing...")
            wait_result = api.wait_for_indexing(repo, timeout_minutes=30)
            
            if wait_result['success']:
                print(f"✅ {repo} is ready for code analysis!")
            else:
                print(f"❌ {wait_result.get('error', 'Indexing failed')}")
        else:
            err = result.get('error', '') or ''
            # Greptile returns a 4xx when already indexing; still allow waiting.
            if "already" in err.lower() and "process" in err.lower():
                print("⏳ Already indexing...")
                print("⏳ Waiting for indexing...")
                wait_result = api.wait_for_indexing(repo, timeout_minutes=30)
                if wait_result.get('success'):
                    print(f"✅ {repo} is ready for code analysis!")
                else:
                    print(f"❌ {wait_result.get('error', 'Indexing failed')}")
            else:
                print(f"❌ {result.get('error', 'Failed')}")
    
    elif command in ["review", "review-post"]:
        if len(sys.argv) < 3:
            print(f"Usage: greptile_simple {command} <pr-url>")
            sys.exit(1)
        
        pr_url = sys.argv[2]
        post = command == "review-post"
        
        reviewer = GreptileReviewer()
        result = reviewer.review_pr_via_query(pr_url)
        
        if result['success']:
            print("\n" + "="*60)
            print("📝 CODE REVIEW:")
            print("="*60)
            print(result['review'])
            print("="*60)
            
            # Save review
            from datetime import datetime
            review_dir = Path.home() / "greptile-reviews"
            review_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"{result['pr_info']['repo'].replace('/', '_')}_PR{result['pr_info']['pr_number']}_{timestamp}.md"
            filepath = review_dir / filename
            
            with open(filepath, 'w') as f:
                f.write(f"# Review: {result['pr_info']['title']}\n\n")
                f.write(result['review'])
            
            print(f"\n💾 Saved to: {filepath}")
            
            if post:
                if reviewer.post_review_comment(pr_url, result['review']):
                    print("✅ Posted to PR!")
        else:
            print(f"❌ {result.get('error', 'Review failed')}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()