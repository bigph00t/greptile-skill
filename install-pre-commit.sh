#!/bin/bash
# Greptile Pre-Commit Hook Installer

echo "🔧 Installing Greptile pre-commit hook..."

# Get the repo directory
if [ -z "$1" ]; then
    REPO_DIR="."
else
    REPO_DIR="$1"
fi

# Check if it's a git repo
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "❌ Error: $REPO_DIR is not a git repository"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$REPO_DIR/.git/hooks"

# Install the pre-commit hook
cat > "$REPO_DIR/.git/hooks/pre-commit" << 'EOF'
#!/bin/bash
# Greptile Pre-Commit Review Hook

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔍 Running Greptile code review...${NC}"

# Get the diff of staged changes
DIFF=$(git diff --staged)

if [ -z "$DIFF" ]; then
    echo "✅ No staged changes to review"
    exit 0
fi

# Run the review
REVIEW=$(python -c "
import sys
sys.path.insert(0, '$HOME/greptile-skill')
from greptile_api import GreptileAPI

try:
    api = GreptileAPI()
    diff = '''$DIFF'''
    
    # Query for review
    result = api.query_repository('bigph00t/strainwise', f'''
Please review this git diff for potential issues:

{diff}

Focus on:
- 🔒 Security vulnerabilities
- 🐛 Potential bugs
- ⚡ Performance issues
- 📝 Code style and best practices
- 🧪 Missing tests

Format your response as:
SEVERITY: [CRITICAL|HIGH|MEDIUM|LOW|PASS]
Then provide details.
''')
    
    if result['success']:
        print(result['response'])
    else:
        print(f\"ERROR: {result.get('error', 'Review failed')}\"")
        sys.exit(1)
except Exception as e:
    print(f\"ERROR: {str(e)}\"")
    sys.exit(1)
" 2>&1)

# Check if review ran successfully
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Review failed:${NC}"
    echo "$REVIEW"
    echo -e "\n${YELLOW}Commit anyway? (y/N):${NC} "
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Parse severity from review
echo -e "\n${GREEN}📝 Greptile Review:${NC}"
echo "$REVIEW"

# Check for critical issues
if echo "$REVIEW" | grep -q "SEVERITY: CRITICAL\|SEVERITY: HIGH"; then
    echo -e "\n${RED}❌ Critical/High severity issues found!${NC}"
    echo -e "${YELLOW}Do you want to commit anyway? (y/N):${NC} "
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Commit aborted. Fix the issues and try again."
        exit 1
    fi
elif echo "$REVIEW" | grep -q "SEVERITY: MEDIUM"; then
    echo -e "\n${YELLOW}⚠️  Medium severity issues found.${NC}"
    echo -e "${YELLOW}Continue with commit? (Y/n):${NC} "
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✅ Proceeding with commit${NC}"
EOF

# Make it executable
chmod +x "$REPO_DIR/.git/hooks/pre-commit"

echo "✅ Pre-commit hook installed in $REPO_DIR"
echo ""
echo "The hook will:"
echo "  - Review all staged changes before commit"
echo "  - Block commits with CRITICAL/HIGH issues (unless overridden)"
echo "  - Warn about MEDIUM issues"
echo "  - Let LOW/PASS issues through"
echo ""
echo "To bypass the hook once: git commit --no-verify"
echo "To disable permanently: rm $REPO_DIR/.git/hooks/pre-commit"