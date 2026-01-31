#!/usr/bin/env python3
"""
Greptile API Integration - Enable repos and manage reviews
"""

import os
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class GreptileAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GREPTILE_API_KEY')
        if not self.api_key:
            secret_path = Path.home() / 'secrets' / 'greptile_api_key'
            if secret_path.exists():
                self.api_key = secret_path.read_text().strip()
        
        if not self.api_key:
            raise ValueError("Greptile API key not found")
        
        self.base_url = "https://api.greptile.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_default_branch(self, repo: str) -> str:
        """Get the default branch for a repo using GitHub CLI"""
        try:
            result = subprocess.run(
                ["gh", "api", f"repos/{repo}", "--jq", ".default_branch"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "main"  # fallback
    
    def enable_repo(self, repo: str, branch: str = None, remote: str = "github") -> Dict:
        """
        Enable a repository for Greptile indexing
        
        Args:
            repo: Repository in format "owner/name"
            branch: Branch to index (auto-detects if not provided)
            remote: Remote type (github or gitlab)
        
        Returns:
            API response with indexing status
        """
        # Auto-detect branch if not provided
        if branch is None:
            branch = self.get_default_branch(repo)
        payload = {
            "remote": remote,
            "repository": repo,
            "branch": branch
        }
        
        response = requests.post(
            f"{self.base_url}/repositories",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'repo': repo,
                'message': data.get('message', 'Repository enabled'),
                'status': data.get('repoData', {}).get('status'),
                'status_url': data.get('statusEndpoint')
            }
        else:
            return {
                'success': False,
                'repo': repo,
                'error': response.text,
                'status_code': response.status_code
            }
    
    def check_repo_status(self, repo: str, branch: str = "main", remote: str = "github") -> Dict:
        """Check indexing status of a repository"""
        # URL encode the repo identifier
        repo_id = f"{remote}:{branch}:{repo}".replace('/', '%2F').replace(':', '%3A')
        
        response = requests.get(
            f"{self.base_url}/v2/repositories/{repo_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'repo': repo,
                'status': data.get('status'),
                'processing_sha': data.get('processingSha'),
                'last_processed_sha': data.get('lastProcessedSha'),
                'chunks_processed': data.get('chunksProcessed', 0),
                'total_chunks': data.get('totalChunks', 0),
                'message': data.get('message', '')
            }
        else:
            return {
                'success': False,
                'repo': repo,
                'error': response.text
            }
    
    def enable_all_repos(self, repos: List[str]) -> List[Dict]:
        """Enable multiple repositories"""
        results = []
        
        for repo in repos:
            print(f"\n🔧 Enabling {repo}...")
            result = self.enable_repo(repo)
            results.append(result)
            
            if result['success']:
                print(f"✅ {result['message']}")
                print(f"   Status: {result.get('status', 'Unknown')}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            
            # Small delay between requests
            time.sleep(1)
        
        return results
    
    def wait_for_indexing(self, repo: str, timeout_minutes: int = 60) -> Dict:
        """Wait for repository indexing to complete"""
        print(f"\n⏳ Waiting for {repo} to be indexed...")
        
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        check_interval = 30  # Check every 30 seconds
        
        while True:
            status = self.check_repo_status(repo)
            
            if not status['success']:
                return status
            
            repo_status = status.get('status', '').upper()
            
            if repo_status == 'PROCESSED':
                elapsed = time.time() - start_time
                print(f"\n✅ {repo} indexed successfully in {elapsed/60:.1f} minutes!")
                return {
                    'success': True,
                    'repo': repo,
                    'status': 'indexed',
                    'time_minutes': elapsed / 60
                }
            elif repo_status in ['FAILED', 'ERROR']:
                print(f"\n❌ {repo} indexing failed: {status.get('message', '')}")
                return {
                    'success': False,
                    'repo': repo,
                    'status': repo_status,
                    'error': status.get('message', 'Indexing failed')
                }
            else:
                # Still processing
                chunks = status.get('chunks_processed', 0)
                total = status.get('total_chunks', 0)
                if total > 0:
                    progress = (chunks / total) * 100
                    print(f"\r⏳ Processing: {chunks}/{total} chunks ({progress:.1f}%)", end='', flush=True)
                else:
                    print(f"\r⏳ Status: {repo_status}", end='', flush=True)
            
            # Check timeout
            if time.time() - start_time > timeout_seconds:
                print(f"\n⏰ Timeout after {timeout_minutes} minutes")
                return {
                    'success': False,
                    'repo': repo,
                    'status': 'timeout',
                    'error': f'Indexing not completed after {timeout_minutes} minutes'
                }
            
            time.sleep(check_interval)
    
    def query_repository(self, repo: str, query: str, branch: str = "main", remote: str = "github") -> Dict:
        """Query a repository for code understanding"""
        payload = {
            "messages": [
                {
                    "id": "0",
                    "role": "user",
                    "content": query
                }
            ],
            "repositories": [
                {
                    "remote": remote,
                    "repository": repo,
                    "branch": branch
                }
            ],
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/v2/query",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'response': data.get('message', ''),
                'sources': data.get('sources', [])
            }
        else:
            return {
                'success': False,
                'error': response.text
            }


# CLI interface
if __name__ == "__main__":
    import sys
    
    api = GreptileAPI()
    
    if len(sys.argv) < 2:
        print("Usage: greptile_api.py [enable|enable-all|status|wait|query] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "enable":
        if len(sys.argv) < 3:
            print("Usage: greptile_api.py enable <repo>")
            sys.exit(1)
        
        result = api.enable_repo(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "enable-all":
        repos = [
            "bigph00t/tiny-html-parser",
            "bigph00t/claude-mem-bridge",
            "bigph00t/clawdbot-skills",
            "bigph00t/doc-ingestion-pipeline"
        ]
        results = api.enable_all_repos(repos)
        
        print("\n📊 Summary:")
        enabled = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"✅ Enabled: {len(enabled)}")
        for r in enabled:
            print(f"   - {r['repo']}")
        
        if failed:
            print(f"\n❌ Failed: {len(failed)}")
            for r in failed:
                print(f"   - {r['repo']}: {r.get('error', 'Unknown error')}")
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("Usage: greptile_api.py status <repo>")
            sys.exit(1)
        
        result = api.check_repo_status(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "wait":
        if len(sys.argv) < 3:
            print("Usage: greptile_api.py wait <repo> [timeout-minutes]")
            sys.exit(1)
        
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        result = api.wait_for_indexing(sys.argv[2], timeout)
        print(json.dumps(result, indent=2))
    
    elif command == "query":
        if len(sys.argv) < 4:
            print("Usage: greptile_api.py query <repo> <question>")
            sys.exit(1)
        
        repo = sys.argv[2]
        query = ' '.join(sys.argv[3:])
        result = api.query_repository(repo, query)
        
        if result['success']:
            print(f"\n💬 Response:\n{result['response']}")
            if result.get('sources'):
                print("\n📍 Sources:")
                for source in result['sources']:
                    print(f"   - {source}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")