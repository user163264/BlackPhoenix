#!/bin/bash

# BlackPhoenix Security Cleanup Script
# Removes hardcoded API keys before GitHub upload

echo "🔥 BlackPhoenix Security Cleanup Script"
echo "======================================="

# 1. Revoke the exposed API key immediately
echo ""
echo "🚨 CRITICAL: Please revoke this API key in your OpenAI dashboard IMMEDIATELY:"
echo "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"
echo ""

# 2. Remove hardcoded API keys from files
echo "🧹 Cleaning hardcoded API keys from files..."

# Fix MLCO.py
if [ -f "MLCO.py" ]; then
    echo "  - Cleaning MLCO.py"
    sed -i.bak 's/OPENAI_API_KEY=sk-[a-zA-Z0-9_-]*/OPENAI_API_KEY=your_openai_api_key_here/g' MLCO.py
fi

# Fix Overview.txt
if [ -f "Overview.txt" ]; then
    echo "  - Cleaning Overview.txt"
    sed -i.bak 's/sk-[a-zA-Z0-9_-]*/[API_KEY_REMOVED_FOR_SECURITY]/g' Overview.txt
fi

# Fix test_mlco_integration.sh
if [ -f "test_mlco_integration.sh" ]; then
    echo "  - Cleaning test_mlco_integration.sh"
    sed -i.bak 's/OPENAI_API_KEY=sk-[a-zA-Z0-9_-]*/OPENAI_API_KEY=your_openai_api_key_here/g' test_mlco_integration.sh
fi

# Fix run.sh
if [ -f "run.sh" ]; then
    echo "  - Cleaning run.sh"
    sed -i.bak 's/OPENAI_API_KEY=sk-[a-zA-Z0-9_-]*/OPENAI_API_KEY=your_openai_api_key_here/g' run.sh
fi

# 3. Ensure .env is properly excluded
echo "🔒 Updating .gitignore to ensure security..."
if ! grep -q "^\.env$" .gitignore; then
    echo ".env" >> .gitignore
fi

# 4. Remove .env from tracking if it's being tracked
if git ls-files --error-unmatch .env > /dev/null 2>&1; then
    echo "  - Removing .env from git tracking"
    git rm --cached .env
fi

# 5. Clean up backup files
echo "🗑️  Cleaning up backup files..."
rm -f *.bak

# 6. Final verification
echo ""
echo "🔍 Final verification - scanning for remaining API keys..."
if grep -r "sk-" . --exclude-dir=venv --exclude-dir=.git --exclude-dir=__pycache__ | grep -v "your_openai_api_key_here" | grep -v "API_KEY_REMOVED_FOR_SECURITY"; then
    echo "⚠️  WARNING: API keys still found! Manual cleanup required."
else
    echo "✅ No API keys detected in tracked files."
fi

echo ""
echo "🎯 NEXT STEPS:"
echo "1. Generate a NEW OpenAI API key"
echo "2. Add it to .env (which is now properly excluded)"
echo "3. Test the application locally"
echo "4. Review all changes before committing"
echo ""
echo "🔥 BlackPhoenix is now ready for secure GitHub upload!"
