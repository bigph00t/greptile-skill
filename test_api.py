#!/usr/bin/env python3
import requests
import os
from pathlib import Path

# Get API key
api_key = os.environ.get('GREPTILE_API_KEY')
if not api_key:
    secret_path = Path.home() / 'secrets' / 'greptile_api_key'
    if secret_path.exists():
        api_key = secret_path.read_text().strip()

print(f"API Key (first 10 chars): {api_key[:10]}...")

# Test the API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Try to query a repo you said was already enabled
test_repo = input("Enter a repo you've already enabled in Greptile (e.g. owner/name): ")

# Try different endpoints
print(f"\nTesting repo: {test_repo}")

# Method 1: Direct status check
repo_id = f"github:main:{test_repo}".replace('/', '%2F').replace(':', '%3A')
response = requests.get(
    f"https://api.greptile.com/v2/repositories/{repo_id}",
    headers=headers
)
print(f"\nStatus check: {response.status_code}")
print(response.text[:200])

# Method 2: Try a simple query
payload = {
    "messages": [{"id": "0", "role": "user", "content": "What is this repo about?"}],
    "repositories": [{"remote": "github", "repository": test_repo, "branch": "main"}],
    "stream": False
}
response = requests.post(
    "https://api.greptile.com/v2/query",
    headers=headers,
    json=payload
)
print(f"\nQuery test: {response.status_code}")
print(response.text[:200])
