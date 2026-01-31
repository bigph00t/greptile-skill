# Pre-Commit Hook Demo

Just saw it in action! Here's what happened:

## 1. Created a test file with security issues:
```python
# Hardcoded credentials
API_KEY = "sk-1234567890abcdef"

# SQL injection vulnerability  
query = f"SELECT * FROM users WHERE username='{username}'"

# No error handling
response = stripe.charge.create(...)
```

## 2. Tried to commit:
```bash
git add test-pre-commit.py
git commit -m "Add payment feature"
```

## 3. Hook caught EVERYTHING:

```
🔍 Running Greptile code review...

📝 Greptile Review:
------------------------------------------------------------
SEVERITY: CRITICAL

## 🔒 Security Issues (CRITICAL)

1. **Hardcoded API Credentials (Lines 7-9)**
   - API_KEY and DATABASE_PASSWORD exposed
   - Fix: Use environment variables

2. **SQL Injection Vulnerability (Line 14)**
   - Direct string interpolation in SQL
   - Fix: Use parameterized queries

## 🐛 Potential Bugs (HIGH)

3. **Missing Import Statement**
4. **No Error Handling**
5. **Unchecked Response Status**
6. **Resource Leak**

❌ Critical/High severity issues found!
Do you want to commit anyway? (y/N): n
Commit aborted.
```

## This is GANGSTER because:
- Caught security issues before they hit the repo
- Found bugs that would crash in production
- Even noticed the missing import
- Blocked the commit automatically

Now you'll never push vulnerable code again! 🖤