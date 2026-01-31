#!/bin/bash
# Set up Greptile pre-commit as a global Git hook

echo "🚀 Setting up Greptile pre-commit globally..."

# Create global hooks directory
HOOKS_DIR="$HOME/.git-hooks"
mkdir -p "$HOOKS_DIR"

# Copy the fast pre-commit script
cp ~/skills/greptile/greptile-pre-commit-fast.py "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

# Configure git to use global hooks
git config --global core.hooksPath "$HOOKS_DIR"

echo "✅ Global pre-commit hook installed!"
echo ""
echo "Now EVERY git commit will be reviewed by Greptile!"
echo ""
echo "Commands:"
echo "  - Bypass once: git commit --no-verify"
echo "  - Disable globally: git config --global --unset core.hooksPath"
echo "  - Re-enable: git config --global core.hooksPath ~/.git-hooks"