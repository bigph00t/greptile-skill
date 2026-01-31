# Greptile Code Review Skill

Automatically manage Greptile code reviews for GitHub repos.

## Commands

### Setup
```bash
greptile setup <repo> - Enable Greptile on a repository
greptile setup-all - Enable on all configured repos
```

### Reviews
```bash
greptile review <pr-url> - Trigger code review on PR
greptile status <repo> - Check review status
greptile pending - List all pending reviews
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