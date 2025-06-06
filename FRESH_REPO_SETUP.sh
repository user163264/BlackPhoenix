#!/bin/bash

echo "🔥 BlackPhoenix Fresh Repository Setup"
echo "======================================"
echo ""
echo "⚠️  This creates a completely fresh git history"
echo "🗑️  All previous commits will be lost"
echo ""

read -p "🚨 Continue with fresh repository? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled."
    exit 1
fi

echo "🗑️  Removing old git history..."
rm -rf .git

echo "🆕 Initializing fresh repository..."
git init
git add .
git commit -m "🔥 BlackPhoenix Red Team Toolkit - Initial Release

✨ Features:
- Complete AI red team testing platform with 6 core modules
- AI Model Fingerprinting Suite
- Multilingual Chain Obfuscation Laboratory (MLCO)  
- System Prompt Extraction Testing
- System Saturation Testing
- Token Obfuscation Generator
- Modern web interface with laboratory-style UI

🛡️ Security:
- All API keys removed from source code
- Environment variable configuration
- Comprehensive .gitignore for sensitive files
- Security cleanup automation scripts

📚 Documentation:
- Complete setup and usage instructions
- GitHub upload checklist and guidelines
- Project context and quick reference guides

🎯 Purpose: Ethical AI security research and red team testing
⚡ Ready for: Immediate deployment and collaborative development"

echo "🌐 Adding remote repository..."
git remote add origin https://github.com/user163264/BlackPhoenix.git

echo "🚀 Force pushing clean repository..."
git push origin main --force

echo ""
echo "✅ Fresh repository created and pushed!"
echo "🔥 BlackPhoenix is now live with clean history!"
echo "🌐 Check: https://github.com/user163264/BlackPhoenix"
