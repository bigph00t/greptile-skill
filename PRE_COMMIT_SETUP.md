# 🔥 Greptile Pre-Commit Hook - Never Push Shit Code Again!

## What It Does

Reviews your code BEFORE you commit, catching:
- 🔒 Security vulnerabilities 
- 🐛 Bugs before they hit the repo
- ⚡ Performance issues
- 📝 Best practice violations

## Quick Install (One Repo)

```bash
cd your-repo
~/greptile-skill/install-pre-commit.sh
```

## Global Install (ALL Repos)

```bash
# Install globally - review EVERY commit
bash ~/greptile-skill/setup-global-hook.sh
```

## How It Works

1. You run `git commit`
2. Hook reviews your staged changes
3. Shows you issues
4. Blocks commit if critical issues found (or lets you override)

## Example Output

```
🔍 Greptile Pre-Commit Review

Files to review:
M       auth.py
A       payment.py

⏳ Getting AI review...

📝 Review Complete:
------------------------------------------------------------
ISSUES: YES

CRITICAL Security Issue in auth.py:
- Line 15: Hardcoded JWT secret key
- Line 28: SQL injection vulnerability in user query

HIGH Bug Risk in payment.py:
- Line 45: No error handling for Stripe API calls
------------------------------------------------------------

❌ Issues found!
Commit anyway? (y/N): n
Commit aborted.
```

## Commands

### Bypass Review Once
```bash
git commit --no-verify -m "Emergency fix"
```

### Disable Globally
```bash
git config --global --unset core.hooksPath
```

### Check Status
```bash
# See if global hook is active
git config --global core.hooksPath
```

## Pro Tips

1. **Fast Mode** - The hook skips docs/config files automatically
2. **Large Diffs** - Auto-truncates huge diffs for speed
3. **Offline Mode** - Falls back gracefully if API is down

## Customize

Edit severity levels in the hook:
```python
# Only block on CRITICAL (not HIGH)
if "ISSUES: YES" in review and "CRITICAL" in review:
    # Block commit
```

## Why This Is Gangster

- **Clean History** - No more "fix typo" commits
- **Faster PR Reviews** - Issues caught before PR
- **Learn Fast** - Instant feedback makes you better
- **Team Consistency** - Everyone gets the same quality bar

Ready to never push broken code again? Install now! 🖤