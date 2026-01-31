# Greptile Integration Guide for AI Agents

This guide explains how to use Greptile for code reviews in your automated workflows.

## Key Discovery: Two Separate Systems

1. **Greptile API** - What we use (indexing + querying)
2. **Greptile GitHub App** - Automatic reviews (requires dashboard setup)

We use the API approach which works perfectly for AI agents!

## Workflow for AI Agents

### 1. Create Repo & Enable Greptile
```bash
# Create new repo
gh repo create owner/new-repo --private

# Enable Greptile indexing
python ~/greptile-skill/greptile_simple.py enable owner/new-repo
```

### 2. Make Changes & Create PR
```bash
cd ~/new-repo
git checkout -b feature
# ... make changes ...
git add -A && git commit -m "Add feature"
git push -u origin feature
gh pr create --title "Add feature" --body "Description"
```

### 3. Get AI Code Review
```bash
# Just get review
python ~/greptile-skill/greptile_simple.py review https://github.com/owner/repo/pull/123

# Get review AND post as PR comment
python ~/greptile-skill/greptile_simple.py review-post https://github.com/owner/repo/pull/123
```

## How It Works

Since Greptile doesn't expose a direct "trigger review" API endpoint, we:
1. Fetch the PR diff using GitHub CLI
2. Send it to Greptile's query API with review instructions
3. Get back a comprehensive code review
4. Optionally post it as a PR comment

## Example Output

```
📝 CODE REVIEW:
============================================================
I'll review this pull request...

## Summary of Changes
- Added user authentication system
- Implemented JWT token handling
- Added password hashing with bcrypt

## Security Considerations
✅ Good: Using bcrypt for password hashing
⚠️ Issue: JWT secret should be in environment variable

## Suggestions
1. Move JWT_SECRET to .env file
2. Add input validation for email format
3. Consider rate limiting for login attempts

## Overall: APPROVE with minor changes
============================================================
```

## Benefits for AI Agents

- **No Dashboard Setup** - Works purely via API
- **Immediate Reviews** - No waiting for webhooks
- **Full Control** - Trigger reviews when YOU want
- **Works Anywhere** - Public or private repos

## Quick Reference

```bash
# Enable repo (one time)
greptile_simple enable owner/repo

# Review PR
greptile_simple review <pr-url>

# Review + Post comment
greptile_simple review-post <pr-url>
```

## Notes

- Reviews are saved to `~/greptile-reviews/`
- Repos must be indexed before reviewing (takes 5-30 min)
- Uses the indexed repo's codebase as context for reviews
- If PR's repo isn't indexed, falls back to another indexed repo