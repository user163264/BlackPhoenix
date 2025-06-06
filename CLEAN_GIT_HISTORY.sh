#!/bin/bash

echo "🔥 BlackPhoenix Git History Cleanup"
echo "===================================="
echo ""
echo "🚨 GitHub detected API keys in commit history."
echo "📝 This script will clean ALL commits to remove API key references."
echo ""

# The exposed API key pattern
API_KEY_PATTERN="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"

echo "🔍 Files containing API keys in history:"
echo "  - Overview.txt:65"
echo "  - SECURITY_CLEANUP_SCRIPT.sh:12" 
echo "  - run.sh:27"
echo "  - test_mlco_integration.sh:36"
echo ""

read -p "⚠️  This will rewrite git history. Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled."
    exit 1
fi

echo "🧹 Cleaning git history..."

# Method 1: BFG Repo-Cleaner (if available)
if command -v bfg &> /dev/null; then
    echo "📦 Using BFG Repo-Cleaner..."
    echo "$API_KEY_PATTERN" > api-keys.txt
    bfg --replace-text api-keys.txt .
    rm api-keys.txt
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
else
    echo "📦 Using git filter-branch..."
    
    # Method 2: git filter-branch
    git filter-branch --force --index-filter \
        'git ls-files -z | xargs -0 sed -i "s/'$API_KEY_PATTERN'/[API_KEY_REMOVED_FOR_SECURITY]/g"' \
        --prune-empty --tag-name-filter cat -- --all
    
    # Clean up
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
fi

echo ""
echo "✅ Git history cleaned!"
echo "🚀 Now trying to push again..."

# Force push to overwrite remote history
git push origin main --force

echo ""
echo "🔥 BlackPhoenix should now be live on GitHub!"
echo "🌐 Check: https://github.com/user163264/BlackPhoenix"
