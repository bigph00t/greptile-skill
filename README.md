# Greptile Integration

## What Greptile Actually Is

Greptile is NOT a direct API service. It's a GitHub/GitLab app that automatically reviews PRs.

## Setup Process

1. **Install the GitHub App**
   - Go to https://app.greptile.com
   - Sign in with GitHub
   - Install the Greptile GitHub app
   - Select repositories to enable

2. **Repository Indexing**
   - Greptile indexes your entire codebase (1-2 hours for large repos)
   - Once indexed, it automatically reviews all new PRs

3. **How It Works**
   - You create a PR normally
   - Greptile automatically reviews it within minutes
   - Reviews appear as GitHub comments from @greptile

## Our Workflow

### Create PR and Wait for Review
```bash
# Create PR and wait for Greptile review
python greptile_v2.py create-pr-wait "Fix: Handle edge cases" "This PR fixes..." 5

# Wait for review on existing PR
python greptile_v2.py wait https://github.com/owner/repo/pull/123 10
```

### Check Review Status
```bash
# Check all PRs with Greptile reviews
python greptile_v2.py check

# Check specific repo
python greptile_v2.py check bigph00t/tiny-html-parser
```

## Integration with Development Flow

1. Make changes on feature branch
2. Use `create-pr-wait` to create PR and wait for Greptile
3. Address Greptile's feedback
4. Merge when ready

## Repos to Enable

- bigph00t/tiny-html-parser ✓
- bigph00t/claude-mem-bridge ✓  
- bigph00t/clawdbot-skills
- bigph00t/doc-ingestion-pipeline

Visit https://app.greptile.com to enable Greptile on these repos!