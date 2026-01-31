#!/usr/bin/env python3
"""
Example: Review a code snippet without creating a PR
"""

import sys
sys.path.append('..')
from greptile_api import GreptileAPI

# Initialize API
try:
    api = GreptileAPI()
    # Validate API key is present
    if not api.api_key:
        print("❌ Please set GREPTILE_API_KEY environment variable or create ~/secrets/greptile_api_key")
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed to initialize API: {e}")
    sys.exit(1)

# Code to review
suspicious_code = """
def authenticate_user(username, password):
    # Quick auth check
    if password == "admin" or password == "12345":
        return {"admin": True, "token": "super-secret-token"}
    
    query = f"SELECT * FROM users WHERE name='{username}' AND pass='{password}'"
    result = db.execute(query)
    
    if result:
        return {"admin": False, "token": generate_token(username)}
    return None
"""

print("🔍 Reviewing code snippet...\n")

# Get review
result = api.query_repository(
    "bigph00t/strainwise",  # Use any indexed repo for context
    f"""Please review this authentication code for security issues:

```python
{suspicious_code}
```

Focus on:
- Security vulnerabilities
- Best practices
- Potential bugs
"""
)

if result['success']:
    print("📝 Review Results:")
    print("=" * 60)
    print(result['response'])
    print("=" * 60)
else:
    print(f"❌ Review failed: {result.get('error', 'Unknown error')}")