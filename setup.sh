#!/bin/bash
# Setup Greptile integration

echo "🔧 Setting up Greptile integration..."

# Make script executable
chmod +x greptile.py

# Copy API key from secrets
if [ -f ~/secrets/greptile_api_key ]; then
    export GREPTILE_API_KEY=$(cat ~/secrets/greptile_api_key)
    echo "✓ API key loaded"
else
    echo "❌ API key not found in ~/secrets/greptile_api_key"
    exit 1
fi

# Create config directory
mkdir -p ~/.greptile

# Enable on all repos
echo "📦 Enabling Greptile on all repos..."
python3 greptile.py setup-all

# Add to HEARTBEAT.md
echo "
## Code Review Check
Check for pending Greptile reviews:
\`\`\`
python ~/skills/greptile/greptile.py status
\`\`\`
" >> ~/HEARTBEAT.md

echo "✅ Greptile integration complete!"
echo "
Next steps:
1. Trigger review on tiny-html-parser PR: python3 greptile.py review https://github.com/bigph00t/tiny-html-parser/pull/1
2. Check status: python3 greptile.py pending
"