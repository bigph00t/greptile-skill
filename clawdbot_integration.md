# Greptile Clawdbot Integration

## Automatic Reminders

Add to your HEARTBEAT.md:
```markdown
## Code Review Check
Check for pending Greptile reviews every few heartbeats.
Run: python ~/skills/greptile/greptile.py pending
If any are pending, notify about them.
```

## Cron Job Setup

Create a cron job for regular checks:

```python
# Add via cron tool
cron add \
  --text "Check pending code reviews and notify if any exist" \
  --jobId "greptile-review-check" \
  --schedule "0 */4 * * *"  # Every 4 hours
```

## GitHub Webhook Integration

When a PR is created:
1. Automatically trigger Greptile review
2. Add to pending reviews list
3. Set reminder for follow-up

## Manual Commands

In chat:
- "check code reviews" → Run pending check
- "review PR <url>" → Trigger review
- "setup greptile on <repo>" → Enable on repo

## Memory Integration

The skill automatically captures:
- When reviews are triggered
- Review completion status
- Time to review metrics
- Common feedback patterns