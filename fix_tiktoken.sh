#!/bin/bash

echo "🔧 FIXING TIKTOKEN LIBRARY ISSUE"
echo "================================"

cd /Users/admin/Documents/redteam-tools

# Activate virtual environment
source venv/bin/activate

echo "📦 Uninstalling conflicting tiktoken packages..."
pip uninstall -y tiktoken tiktoken-ext

echo "📦 Clearing pip cache..."
pip cache purge

echo "📦 Reinstalling tiktoken from scratch..."
pip install --no-cache-dir tiktoken==0.9.0

echo "🧪 Testing tiktoken installation..."
python3 -c "
try:
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')
    test_text = 'Hello world'
    tokens = enc.encode(test_text)
    print(f'✅ Tiktoken working: {test_text} -> {len(tokens)} tokens')
except Exception as e:
    print(f'❌ Tiktoken error: {e}')
"

echo "✅ Tiktoken fix complete!"
echo "🚀 Try running: python3 app.py"
