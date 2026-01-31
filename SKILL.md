# Greptile Code Review Skill

Get automated code reviews on your GitHub PRs using Greptile AI.

## Quick Start

### 1. Enable a repo (one-time setup)
```bash
python ~/greptile-skill/greptile.py enable owner/repo
```
This automatically:
- Detects the default branch
- Submits for indexing
- Waits for completion (~5-30 min depending on repo size)

### 2. Get PR reviews
```bash
python ~/greptile-skill/greptile.py review https://github.com/owner/repo/pull/123
```
This:
- Waits for Greptile to review the PR
- Shows the review when ready
- Saves notes to `~/greptile-reviews/`

### 3. Check recent reviews
```bash
python ~/greptile-skill/greptile.py status
```

## Example Workflow

1. **Create a new repo and enable it:**
   ```bash
   gh repo create bigph00t/my-app --private
   python ~/greptile-skill/greptile.py enable bigph00t/my-app
   ```

2. **Make changes and create PR:**
   ```bash
   cd ~/my-app
   git checkout -b feature
   # ... make changes ...
   git add -A && git commit -m "Add feature"
   git push -u origin feature
   gh pr create --title "Add new feature" --body "Description"
   ```

3. **Wait for review:**
   ```bash
   python ~/greptile-skill/greptile.py review https://github.com/bigph00t/my-app/pull/1
   ```

### One-Command PR + Review

After making changes and pushing:
```bash
cd ~/my-app
python ~/greptile-skill/create_pr_and_review.py "Add new feature" "Optional description"
```
This creates the PR and immediately waits for Greptile's review.

## Notes

- Reviews are saved to `~/greptile-reviews/` for future reference
- Empty repos can't be indexed - add code first
- Private repos work if your Greptile account has GitHub access
- API key stored in `~/secrets/greptile_api_key`

## Advanced Commands

For more control, use the API directly:
```bash
# Check specific repo status
python ~/greptile-skill/greptile_api.py status owner/repo

# Query a repo
python ~/greptile-skill/greptile_api.py query owner/repo "How does the auth work?"

# Enable with specific branch
python -c "from greptile_api import GreptileAPI; api = GreptileAPI(); print(api.enable_repo('owner/repo', branch='develop'))"
```