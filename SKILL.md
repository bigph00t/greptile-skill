# Greptile Code Review Skill

Get AI-powered code reviews on your GitHub PRs using Greptile's query API.

## 🚀 Quick Start for AI Agents

### Simple Commands
```bash
# Enable a repo for analysis
python ~/greptile-skill/greptile_simple.py enable owner/repo

# Get PR review  
python ~/greptile-skill/greptile_simple.py review https://github.com/owner/repo/pull/123

# Get review AND post to PR
python ~/greptile-skill/greptile_simple.py review-post https://github.com/owner/repo/pull/123
```

## How It Works

Since Greptile doesn't provide a direct PR review API endpoint, we:
1. Fetch PR diffs using GitHub CLI
2. Send to Greptile's query API for analysis
3. Get comprehensive code reviews
4. Optionally post as PR comments

## Complete Workflow Example

```bash
# 1. Create repo and enable Greptile
gh repo create bigph00t/new-feature --private
python ~/greptile-skill/greptile_simple.py enable bigph00t/new-feature

# 2. Make changes and create PR
cd ~/new-feature
git checkout -b add-auth
# ... make changes ...
git add -A && git commit -m "Add authentication"
git push -u origin add-auth
gh pr create --title "Add authentication" --body "Implements JWT auth"

# 3. Get AI review
python ~/greptile-skill/greptile_simple.py review-post https://github.com/bigph00t/new-feature/pull/1
```

## Features

- ✅ Works without GitHub App installation
- ✅ Immediate reviews (no webhook waiting)
- ✅ Reviews saved to `~/greptile-reviews/`
- ✅ Auto-detects branch names
- ✅ Handles private repos
- ✅ Posts reviews as PR comments

## Advanced Usage

For more control, use the individual scripts:

```bash
# Just enable indexing
python ~/greptile-skill/greptile_api.py enable owner/repo

# Manual review with options
python ~/greptile-skill/greptile_review.py <pr-url> --post --repo bigph00t/strainwise

# Query a repo
python ~/greptile-skill/greptile_api.py query owner/repo "How does auth work?"
```

## Configuration

Store API key in one of:
- Environment: `export GREPTILE_API_KEY="your-key"`
- File: `echo "your-key" > ~/secrets/greptile_api_key`

## Limitations

- Repos must be indexed first (5-30 min)
- Empty repos cannot be indexed
- Reviews use query API, not official review endpoint

## Files

- `greptile_simple.py` - Main commands for AI agents
- `greptile_api.py` - Core API wrapper
- `greptile_review.py` - Advanced review features
- `greptile.py` - Original workflow (deprecated)
- `AI_AGENT_GUIDE.md` - Detailed explanation