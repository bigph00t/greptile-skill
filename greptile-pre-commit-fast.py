#!/usr/bin/env python3
"""
Fast Greptile pre-commit review - optimized for speed
"""

import subprocess
import sys
import os

# Add greptile-skill to path
sys.path.insert(0, os.path.expanduser('~/greptile-skill'))

from greptile_api import GreptileAPI

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def get_staged_diff():
    """Get the diff of staged changes"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged', '--name-status'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return None, None
        
        files_summary = result.stdout.strip()
        
        # Get full diff
        result = subprocess.run(
            ['git', 'diff', '--staged'],
            capture_output=True,
            text=True
        )
        
        return result.stdout, files_summary
    except:
        return None, None

def main():
    print(f"{BLUE}🔍 Greptile Pre-Commit Review{NC}")
    
    # Get staged changes
    diff, files_summary = get_staged_diff()
    
    if not diff:
        print(f"{GREEN}✅ No staged changes to review{NC}")
        return 0
    
    # Show what we're reviewing
    print(f"\n{YELLOW}Files to review:{NC}")
    print(files_summary)
    
    # Skip review for certain files
    skip_patterns = ['.md', '.txt', '.json', 'package-lock.json', '.gitignore']
    if all(any(pattern in line for pattern in skip_patterns) for line in files_summary.split('\n') if line):
        print(f"{GREEN}✅ Only documentation/config files - skipping review{NC}")
        return 0
    
    # Limit diff size for faster reviews
    if len(diff) > 10000:
        print(f"{YELLOW}⚠️  Large diff ({len(diff)} chars) - truncating for speed{NC}")
        diff = diff[:10000] + "\n... (truncated)"
    
    print(f"\n{BLUE}⏳ Getting AI review...{NC}")
    
    try:
        api = GreptileAPI()
        
        # Quick review prompt
        result = api.query_repository('bigph00t/strainwise', f"""
Quick pre-commit review of this diff. Be concise.

{diff}

Respond with:
ISSUES: [YES|NO]
If YES, list only CRITICAL issues (security, bugs).
Skip style/formatting issues.
""")
        
        if not result['success']:
            print(f"{RED}❌ Review failed: {result.get('error', 'Unknown')}{NC}")
            return 1
        
        review = result['response']
        
        # Display review
        print(f"\n{GREEN}📝 Review Complete:{NC}")
        print("-" * 60)
        print(review)
        print("-" * 60)
        
        # Check for issues
        if "ISSUES: YES" in review or "CRITICAL" in review.upper():
            print(f"\n{RED}❌ Issues found!{NC}")
            response = input(f"{YELLOW}Commit anyway? (y/N): {NC}")
            if response.lower() != 'y':
                print(f"{RED}Commit aborted.{NC}")
                return 1
        else:
            print(f"\n{GREEN}✅ No critical issues found{NC}")
        
        return 0
        
    except Exception as e:
        print(f"{RED}❌ Error: {str(e)}{NC}")
        response = input(f"{YELLOW}Review failed. Commit anyway? (y/N): {NC}")
        if response.lower() != 'y':
            return 1
        return 0

if __name__ == "__main__":
    sys.exit(main())