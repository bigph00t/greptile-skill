# Greptile Setup Guide

## ✅ What We Built

The Greptile skill now includes FULL API support for:
- **Enabling repositories** (via API!)
- **Checking indexing status**
- **Waiting for indexing completion**
- **Creating PRs and waiting for reviews**
- **Querying repositories with AI**

## 🚀 Complete Setup Process

### Step 1: Install Greptile GitHub App (REQUIRED FIRST!)
1. Go to https://app.greptile.com
2. Sign in with GitHub
3. Click "Install GitHub App"
4. **Select the repositories**:
   - bigph00t/tiny-html-parser
   - bigph00t/claude-mem-bridge
   - bigph00t/clawdbot-skills
   - bigph00t/doc-ingestion-pipeline

### Step 2: Enable Repos via API
Once the GitHub app has access, enable repos:
```bash
cd greptile-skill
python greptile_api.py enable-all
```

### Step 3: Wait for Indexing
Check status or wait for completion:
```bash
# Check status
python greptile_api.py status bigph00t/tiny-html-parser

# Wait for indexing (up to 60 minutes)
python greptile_api.py wait bigph00t/tiny-html-parser
```

### Step 4: Create PRs with Auto-Review
```bash
# Create PR and wait for Greptile review
python greptile_v2.py create-pr-wait "Fix: Handle edge cases" "This PR fixes..."

# Or wait for review on existing PR
python greptile_v2.py wait https://github.com/bigph00t/tiny-html-parser/pull/1
```

## 📊 Current Status

- **tiny-html-parser**: Currently indexing! ✅
- **Other repos**: Need GitHub app permissions first

## ⚠️ Important Notes

1. **Private Repos**: The Greptile GitHub app MUST have access to private repos
2. **API Key**: Your API key (stored in secrets/) only works for repos the app can access
3. **Indexing Time**: 
   - Small repos: 5-30 minutes
   - Large repos: 1-2 hours
4. **Auto Reviews**: Once indexed, ALL new PRs get reviewed automatically

## 🔍 Query Your Code

Once indexed, you can ask questions:
```bash
python greptile_api.py query bigph00t/tiny-html-parser "How does the HTML parser handle malformed tags?"
```

This is incredibly powerful for understanding codebases!