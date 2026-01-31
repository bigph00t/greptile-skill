---
name: greptile
description: Get AI-powered code reviews on GitHub PRs using Greptile. Use this skill when the user wants to review a PR, enable a repo for code analysis, query code understanding, or review code snippets for security issues.
version: 1.0.0
---

# Greptile Code Review Skill

Get AI-powered code reviews on your GitHub PRs using Greptile's query API.

## How to Use This Skill

The skill is installed at `~/.claude/skills/greptile/`. Use these commands:

### Review a PR

To review a pull request, run:

```bash
python ~/.claude/skills/greptile/greptile_simple.py review <PR_URL>
```

Example:
```bash
python ~/.claude/skills/greptile/greptile_simple.py review https://github.com/owner/repo/pull/123
```

### Review and Post Comment

To review AND post the review as a PR comment:

```bash
python ~/.claude/skills/greptile/greptile_simple.py review-post <PR_URL>
```

### Enable a Repo for Analysis

Before reviewing, repos need to be indexed (takes 5-30 min):

```bash
python ~/.claude/skills/greptile/greptile_simple.py enable owner/repo
```

### Query a Repo

Ask questions about any indexed codebase:

```bash
python ~/.claude/skills/greptile/greptile_api.py query owner/repo "How does authentication work?"
```

### Review Code Directly (No PR)

To review a code snippet for security issues without creating a PR:

```python
import sys
sys.path.insert(0, '/home/bigphoot/.claude/skills/greptile')
from greptile_api import GreptileAPI

api = GreptileAPI()
code = """your code here"""
result = api.query_repository('owner/repo', f'Review this code for security issues:\n{code}')
print(result['response'])
```

## Configuration

API key must be set in one of:
- Environment: `export GREPTILE_API_KEY="your-key"`
- File: `~/secrets/greptile_api_key`

## Features

- ✅ Works without GitHub App installation
- ✅ Immediate reviews (no webhook waiting)
- ✅ Reviews saved to `~/greptile-reviews/`
- ✅ Auto-detects branch names
- ✅ Handles private repos
- ✅ Posts reviews as PR comments

## Limitations

- Repos must be indexed first (5-30 min)
- Empty repos cannot be indexed