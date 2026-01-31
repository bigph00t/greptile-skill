# Greptile Code Review Automation

Automated AI code reviews for your GitHub PRs using Greptile's API. Get instant, intelligent feedback on your code changes without manual setup.

## Features

- 🚀 **One-command repo indexing** - Auto-detects branch names and handles all setup
- 🔍 **Instant PR reviews** - Get AI-powered code reviews in seconds
- 📝 **Review history** - All reviews saved locally for future reference
- 🔐 **Private repo support** - Works with both public and private repositories
- ⚡ **Simple workflow** - Just three commands to remember

## Installation

1. Clone this repository:
```bash
git clone https://github.com/bigph00t/greptile-skill.git
cd greptile-skill
```

2. Set up your Greptile API key:
```bash
mkdir -p ~/secrets
echo "YOUR_API_KEY" > ~/secrets/greptile_api_key
```

3. Ensure you have GitHub CLI installed:
```bash
gh auth login
```

## Usage

### Enable a repository
```bash
python greptile.py enable owner/repo
```

This command:
- Automatically detects the default branch
- Submits the repository for indexing
- Waits for indexing to complete (5-30 minutes depending on size)

### Get PR review
```bash
python greptile.py review https://github.com/owner/repo/pull/123
```

This command:
- Waits for Greptile to analyze the PR
- Displays the review in your terminal
- Saves the review to `~/greptile-reviews/`

### Check recent reviews
```bash
python greptile.py status
```

## Example Workflow

Here's a complete workflow from repo creation to PR review:

```bash
# Create and enable a new repo
gh repo create mycompany/new-feature --private
python greptile.py enable mycompany/new-feature

# Make your changes
cd ~/new-feature
git checkout -b add-authentication
# ... edit files ...
git add -A
git commit -m "Add JWT authentication"
git push -u origin add-authentication

# Create PR and get review in one command
python ~/greptile-skill/create_pr_and_review.py "Add JWT authentication" "Implements secure token-based auth"
```

## API Reference

### Direct API usage

For advanced use cases, you can use the API wrapper directly:

```python
from greptile_api import GreptileAPI

api = GreptileAPI()

# Enable a repo with a specific branch
api.enable_repo('owner/repo', branch='develop')

# Check indexing status
status = api.check_repo_status('owner/repo')

# Query repository
response = api.query_repository('owner/repo', 'How does the authentication work?')
```

## Requirements

- Python 3.6+
- GitHub CLI (`gh`)
- Greptile API key
- `requests` library

## Configuration

The tool looks for your API key in the following order:
1. `GREPTILE_API_KEY` environment variable
2. `~/secrets/greptile_api_key` file

## Troubleshooting

### "Repository not found"
- Ensure your Greptile account has access to the GitHub repository
- For private repos, verify GitHub permissions in your Greptile dashboard

### "Repository is empty"
- Greptile cannot index empty repositories
- Add at least one file before enabling

### Review not appearing
- Reviews typically appear within 30 seconds
- Check that Greptile bot has access to comment on your PRs

## Contributing

Pull requests are welcome! The review bot will automatically analyze your contributions.

## License

MIT License - see LICENSE file for details