#!/usr/bin/env python3
"""Deep investigation of Greptile API capabilities"""

import requests
import json
import os
from pathlib import Path

# Get API key
api_key = os.environ.get('GREPTILE_API_KEY')
if not api_key:
    secret_path = Path.home() / 'secrets' / 'greptile_api_key'
    if secret_path.exists():
        api_key = secret_path.read_text().strip()

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("=== GREPTILE API DEEP INVESTIGATION ===\n")

# 1. Test basic auth
print("1. Testing Authentication...")
response = requests.get("https://api.greptile.com/v2/repositories", headers=headers)
print(f"   Auth test: {response.status_code}")
if response.status_code == 200:
    print("   ✓ API key is valid")
else:
    print(f"   ✗ Auth failed: {response.text}")

# 2. List all available endpoints (try common patterns)
print("\n2. Exploring API Endpoints...")
endpoints = [
    "/v2/repositories",
    "/v2/query", 
    "/v2/search",
    "/v2/reviews",
    "/v2/pull-requests",
    "/v2/webhooks",
    "/v2/integrations",
    "/v2/github-app",
    "/v2/users/me",
    "/v2/organizations",
    "/repositories",
    "/pull-request",
    "/review"
]

for endpoint in endpoints:
    response = requests.get(f"https://api.greptile.com{endpoint}", headers=headers)
    if response.status_code in [200, 400, 401, 404]:
        print(f"   {endpoint} -> {response.status_code}")
        if response.status_code == 200 and len(response.text) < 500:
            print(f"      Response: {response.text[:200]}")

# 3. Check repository operations
print("\n3. Repository Operations...")
test_repos = ["bigph00t/strainwise", "bigph00t/greptile-skill", "bigph00t/tiny-html-parser"]

for repo in test_repos:
    print(f"\n   Checking {repo}:")
    
    # Try different branch names
    for branch in ["main", "master"]:
        repo_id = f"github:{branch}:{repo}".replace('/', '%2F').replace(':', '%3A')
        response = requests.get(
            f"https://api.greptile.com/v2/repositories/{repo_id}",
            headers=headers
        )
        if response.status_code == 200:
            data = json.loads(response.text)
            print(f"      Branch '{branch}': {data.get('status', 'Unknown')}")
            break
        elif response.status_code == 404:
            continue

# 4. Try to trigger a review manually
print("\n4. Manual Review Trigger Attempts...")

# Method 1: Direct PR review endpoint
pr_payloads = [
    {
        "repository": "bigph00t/greptile-skill",
        "pull_request": 1,
        "remote": "github"
    },
    {
        "repository": "bigph00t/greptile-skill", 
        "pullRequestNumber": 1,
        "remote": "github",
        "branch": "master"
    },
    {
        "remote": "github",
        "repository": "bigph00t/greptile-skill",
        "branch": "master",
        "pr": {"number": 1}
    }
]

review_endpoints = [
    "/v2/reviews",
    "/v2/review", 
    "/v2/pull-request/review",
    "/review",
    "/pull-request"
]

for endpoint in review_endpoints:
    for payload in pr_payloads:
        response = requests.post(
            f"https://api.greptile.com{endpoint}",
            headers=headers,
            json=payload
        )
        if response.status_code != 404:
            print(f"   {endpoint} -> {response.status_code}")
            if response.text and len(response.text) < 300:
                print(f"      Response: {response.text}")
            break

# 5. Query API to understand PR review process
print("\n5. Querying About PR Reviews...")
query_payload = {
    "messages": [{
        "id": "0",
        "role": "user", 
        "content": "How do I trigger a code review on a pull request using the Greptile API?"
    }],
    "repositories": [{
        "remote": "github",
        "repository": "bigph00t/strainwise",
        "branch": "main"
    }],
    "stream": False
}

response = requests.post(
    "https://api.greptile.com/v2/query",
    headers=headers,
    json=query_payload
)
if response.status_code == 200:
    print("   Query successful!")
    data = json.loads(response.text)
    print(f"   Response: {data.get('message', '')[:500]}...")

# 6. Check if there's a user/account endpoint
print("\n6. Account/Integration Info...")
account_endpoints = ["/v2/user", "/v2/users/me", "/v2/account", "/v2/integrations"]
for endpoint in account_endpoints:
    response = requests.get(f"https://api.greptile.com{endpoint}", headers=headers)
    if response.status_code == 200:
        print(f"   {endpoint} -> {response.status_code}")
        try:
            data = json.loads(response.text)
            print(f"      Data: {json.dumps(data, indent=2)[:300]}")
        except:
            print(f"      Response: {response.text[:200]}")

print("\n=== END INVESTIGATION ===")
