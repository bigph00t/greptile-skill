# Greptile Code Review Skill

Automatically manage Greptile code reviews for GitHub repos.

## Commands

### Setup & Enable Repos (via API!)
```bash
python greptile_api.py enable <repo>          # Enable single repo
python greptile_api.py enable-all             # Enable all 4 repos
python greptile_api.py status <repo>          # Check indexing status  
python greptile_api.py wait <repo>            # Wait for indexing to complete
```

### PR Reviews
```bash
python greptile_v2.py create-pr-wait <title> <body>  # Create PR and wait for review
python greptile_v2.py wait <pr-url>                  # Wait for review on existing PR
python greptile_v2.py check                           # List PRs with reviews
```

### Query Repository
```bash
python greptile_api.py query <repo> <question>  # Ask questions about code
```

## Configuration

Store API key in environment or secrets:
```bash
export GREPTILE_API_KEY="your-key"
```

## Automation

The skill includes:
- Auto-enable on new repos
- Reminder system for pending reviews
- Integration with GitHub webhooks
- Review status in PR comments