#!/usr/bin/env python3
"""
Greptile PR Review via Query API - Alternative approach when GitHub App isn't configured
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from greptile_api import GreptileAPI

class GreptileReviewer:
    def __init__(self):
        self.api = GreptileAPI()
    
    def get_pr_diff(self, pr_url: str) -> tuple[bool, str, dict]:
        """Get PR diff and metadata"""
        # Extract repo and PR number
        parts = pr_url.strip('/').split('/')
        if len(parts) < 4 or parts[-2] != 'pull':
            return False, "Invalid PR URL format", {}
        
        owner = parts[-4]
        repo_name = parts[-3] 
        pr_number = parts[-1]
        repo = f"{owner}/{repo_name}"
        
        # Get PR info
        result = subprocess.run(
            ["gh", "pr", "view", pr_number, "--repo", repo, "--json", "title,author,body,state"],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            return False, f"Failed to get PR info: {result.stderr}", {}
        
        pr_info = json.loads(result.stdout)
        
        # Get diff
        result = subprocess.run(
            ["gh", "pr", "diff", pr_number, "--repo", repo],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            return False, f"Failed to get diff: {result.stderr}", {}
        
        return True, result.stdout, {
            "repo": repo,
            "pr_number": pr_number,
            "title": pr_info.get("title", ""),
            "author": pr_info.get("author", {}).get("login", ""),
            "body": pr_info.get("body", ""),
            "state": pr_info.get("state", "")
        }
    
    def review_pr_via_query(self, pr_url: str, indexed_repo: str = None) -> dict:
        """Review a PR by querying an indexed repo with the diff"""
        
        # Get PR diff
        success, diff, pr_info = self.get_pr_diff(pr_url)
        if not success:
            return {"success": False, "error": diff}
        
        print(f"\n📋 PR #{pr_info['pr_number']}: {pr_info['title']}")
        print(f"   Author: {pr_info['author']}")
        print(f"   Repo: {pr_info['repo']}")
        
        # Use the PR's repo if it's indexed; otherwise (optionally) auto-enable & wait.
        context_note = ""
        if indexed_repo:
            query_repo = indexed_repo
        else:
            status = self.api.check_repo_status(pr_info['repo'])
            repo_status = str(status.get('status', '')).upper() if status.get('success') else ""

            if repo_status in {'PROCESSED', 'COMPLETED'}:
                query_repo = pr_info['repo']
            else:
                # Try to enable & wait briefly so we can use the correct repo as context.
                try:
                    self.api.enable_repo(pr_info['repo'])
                except Exception:
                    pass

                # Keep this short for interactive use; indexing can take longer, in which case we fall back.
                wait = self.api.wait_for_indexing(pr_info['repo'], timeout_minutes=5)
                if wait.get('success'):
                    query_repo = pr_info['repo']
                else:
                    # Fallback: use a known-indexed repo to satisfy the query API.
                    # IMPORTANT: we instruct the model to ONLY use the diff (repo context may be irrelevant).
                    query_repo = "bigph00t/strainwise"
                    context_note = (
                        f"NOTE: The target repo ({pr_info['repo']}) is not indexed yet. "
                        f"This request is being sent with context repo {query_repo} ONLY as a transport requirement. "
                        "Do NOT assume anything about the target repo beyond what is shown in the diff. "
                        "Review the diff strictly on its own merits."
                    )
                    print(f"\n⚠️  {pr_info['repo']} not indexed yet; using {query_repo} as a placeholder context")

        # Build review prompt
        prompt = f"""Please provide a thorough code review for this pull request.

{context_note}

**PR Title**: {pr_info['title']}
**Description**: {pr_info['body'] or 'No description provided'}

**Review Guidelines**:
1. Code quality and best practices
2. Potential bugs or security issues
3. Performance considerations
4. Suggestions for improvement
5. Documentation and comments

**Diff to Review**:
```diff
{diff[:8000]}{'... [truncated]' if len(diff) > 8000 else ''}
```

Please structure your review with:
- Summary of changes
- Detailed feedback by file
- Overall recommendation (approve/request changes/comment)
"""
        
        print(f"\n🔍 Sending to Greptile for review (using {query_repo} context)...")
        
        # Query Greptile
        response = self.api.query_repository(query_repo, prompt)
        
        if response['success']:
            return {
                "success": True,
                "review": response['response'],
                "pr_info": pr_info,
                "context_repo": query_repo
            }
        else:
            return {
                "success": False,
                "error": response.get('error', 'Unknown error')
            }
    
    def post_review_comment(self, pr_url: str, review_text: str) -> bool:
        """Post the review as a PR comment"""
        parts = pr_url.strip('/').split('/')
        owner = parts[-4]
        repo_name = parts[-3]
        pr_number = parts[-1]
        repo = f"{owner}/{repo_name}"
        
        # Add header to distinguish from GitHub App reviews
        comment = f"""## 🔍 Greptile Code Review (via API)

{review_text}

---
*This review was generated using the Greptile Query API. For automatic reviews on new PRs, install the [Greptile GitHub App](https://github.com/apps/greptile-app).*"""
        
        result = subprocess.run(
            ["gh", "pr", "comment", pr_number, "--repo", repo, "--body", comment],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"\n✅ Review posted to PR!")
            return True
        else:
            print(f"\n❌ Failed to post comment: {result.stderr}")
            return False


def main():
    if len(sys.argv) < 2:
        print("""
Greptile PR Review (via Query API)

Usage:
  greptile_review.py <pr-url> [--post] [--repo <indexed-repo>]

Options:
  --post              Post review as PR comment
  --repo <repo>       Use specific indexed repo for context

Examples:
  greptile_review.py https://github.com/owner/repo/pull/123
  greptile_review.py https://github.com/owner/repo/pull/123 --post
  greptile_review.py https://github.com/owner/repo/pull/123 --repo bigph00t/strainwise
""")
        sys.exit(1)
    
    pr_url = sys.argv[1]
    post_comment = "--post" in sys.argv
    
    # Check for custom repo
    indexed_repo = None
    if "--repo" in sys.argv:
        idx = sys.argv.index("--repo")
        if idx + 1 < len(sys.argv):
            indexed_repo = sys.argv[idx + 1]
    
    reviewer = GreptileReviewer()
    result = reviewer.review_pr_via_query(pr_url, indexed_repo)
    
    if result['success']:
        print("\n" + "="*60)
        print("📝 REVIEW:")
        print("="*60)
        print(result['review'])
        print("="*60)
        
        # Save to file
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"review_{result['pr_info']['repo'].replace('/', '_')}_PR{result['pr_info']['pr_number']}_{timestamp}.md"
        
        review_dir = Path.home() / "greptile-reviews"
        review_dir.mkdir(exist_ok=True)
        filepath = review_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"# Review: {result['pr_info']['repo']} PR #{result['pr_info']['pr_number']}\n\n")
            f.write(f"**Title**: {result['pr_info']['title']}\n")
            f.write(f"**Author**: {result['pr_info']['author']}\n")
            f.write(f"**Context Repo**: {result['context_repo']}\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("## Review\n\n")
            f.write(result['review'])
        
        print(f"\n💾 Review saved to: {filepath}")
        
        # Post comment if requested
        if post_comment:
            reviewer.post_review_comment(pr_url, result['review'])
    else:
        print(f"\n❌ Review failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()