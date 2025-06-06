# BlackPhoenix Red Team Toolkit - GitHub Upload Checklist

## 🎯 Essential Files for Clean GitHub Upload

This document lists all crucial files needed for a functional BlackPhoenix deployment on GitHub.

---

## ✅ CORE APPLICATION FILES (CRITICAL)

### **Main Application**
- ✅ `app.py` - Main Flask application with all routes and API endpoints
- ✅ `config.py` - Application configuration and settings

### **Core Modules** (modules/)
- ✅ `modules/__init__.py` - Package initialization
- ✅ `modules/api_manager.py` - API management and OpenAI integration
- ✅ `modules/fingerprinting_suite.py` - AI model fingerprinting capabilities
- ✅ `modules/multilingual.py` - Multilingual chain obfuscation engine
- ✅ `modules/prompt_extraction.py` - System prompt extraction attacks
- ✅ `modules/prompt_generator.py` - AI-powered prompt generation
- ✅ `modules/system_saturator.py` - System saturation testing
- ✅ `modules/token_obfuscation.py` - Token manipulation techniques
- ✅ `modules/token_obfuscator.py` - Enhanced token obfuscation

### **Database Models** (models/)
- ✅ `models/__init__.py` - Package initialization
- ✅ `models/prompt.py` - Database models and schemas

---

## ✅ WEB INTERFACE FILES (CRITICAL)

### **HTML Templates** (templates/)
- ✅ `templates/base.html` - Base template for all pages
- ✅ `templates/error.html` - Error page template
- ✅ `templates/prompt_generation_index.html` - Main dashboard/homepage
- ✅ `templates/fingerprinting_suite.html` - AI model fingerprinting interface
- ✅ `templates/mlco.html` - Multilingual Chain Obfuscation Laboratory
- ✅ `templates/prompt_extraction.html` - Prompt extraction testing interface
- ✅ `templates/system_prompts_enhanced.html` - System prompt library interface
- ✅ `templates/system_saturation.html` - System saturation testing interface
- ✅ `templates/token_obfuscation.html` - Token obfuscation generator interface

### **CSS Stylesheets** (static/css/)
- ✅ `static/css/modern-minimalist.css` - Main application styling
- ✅ `static/css/laboratory.css` - Laboratory-style interface styling

### **JavaScript** (static/js/)
- ✅ `static/js/prompt-library.js` - System prompt library functionality
- ✅ `static/js/modal-fallback.js` - Modal dialog fallback support

---

## ✅ CONFIGURATION & SETUP FILES (CRITICAL)

### **Environment & Dependencies**
- ✅ `.env.example` - Example environment variables file
- ✅ `.gitignore` - Git ignore patterns for security and cleanliness
- ✅ `requirements.txt` - Python package dependencies

### **Startup Scripts**
- ✅ `quick_start.sh` - Quick start script for easy deployment
- ✅ `setup.sh` - Initial setup and environment configuration
- ✅ `run.sh` - Standard application runner

---

## ✅ DOCUMENTATION FILES (IMPORTANT)

### **Primary Documentation**
- ✅ `README.md` - Main project documentation and setup instructions
- ✅ `PROJECT_CONTEXT.md` - Comprehensive project overview and status
- ✅ `QUICK_MEMORY.md` - Quick reference for developers and operators

### **Additional Documentation** (docs/)
- ✅ `docs/enhanced_segmented_translation.md` - Segmented translation documentation
- ✅ `docs/token_obfuscator_enhancement.md` - Token obfuscation documentation

---

## ✅ DEVELOPMENT & TESTING FILES (OPTIONAL)

### **Python Testing**
- ✅ `test_enhanced_token_obfuscator.py` - Token obfuscator tests
- ✅ `test_system_saturation.py` - System saturation tests
- ✅ `test_prompt_extraction.py` - Prompt extraction tests

### **Shell Testing Scripts**
- ✅ `test_api_key.sh` - API key validation testing

---

## ❌ FILES TO EXCLUDE FROM GITHUB

### **Security-Sensitive Files**
- ❌ `.env` - Contains actual API keys and secrets
- ❌ `*.log` - Log files may contain sensitive information
- ❌ `*.db` - Database files may contain user data

### **System-Generated Files**
- ❌ `__pycache__/` - Python bytecode cache (handled by .gitignore)
- ❌ `.DS_Store` - macOS system files (handled by .gitignore)
- ❌ `venv/` - Virtual environment (handled by .gitignore)

### **Development Artifacts**
- ❌ Development-specific shell scripts (fix_*, diagnose_*, etc.)
- ❌ Temporary files and debug scripts
- ❌ Personal notes and session handoff files

---

## 🚀 GITHUB UPLOAD PREPARATION CHECKLIST

### **Pre-Upload Security Check**
1. ✅ Ensure `.env` is not included (use `.env.example` instead)
2. ✅ Verify `.gitignore` includes all sensitive patterns
3. ✅ Remove any hardcoded API keys from source code
4. ✅ Clear any log files containing sensitive data
5. ✅ Remove personal development notes and session files

### **Functionality Check**
1. ✅ All 6 core modules present and functional
2. ✅ All essential templates and static files included
3. ✅ Database models properly defined
4. ✅ Requirements.txt is complete and up-to-date
5. ✅ Setup and startup scripts are functional

### **Documentation Check**
1. ✅ README.md provides clear setup instructions
2. ✅ API usage examples are included
3. ✅ Security warnings and disclaimers are present
4. ✅ License and usage terms are specified

---

## 📊 FILE COUNT SUMMARY

**Total Essential Files**: ~50 files
- **Core Application**: 12 files
- **Web Interface**: 15 files  
- **Configuration**: 5 files
- **Documentation**: 8 files
- **Testing**: 10 files

**Repository Size**: ~2-3 MB (excluding logs, cache, and virtual environment)

---

## 🎯 POST-UPLOAD VERIFICATION

After uploading to GitHub, verify:
1. ✅ Application starts successfully with `./quick_start.sh`
2. ✅ All 6 modules are accessible via web interface
3. ✅ API endpoints respond correctly
4. ✅ Documentation links work properly
5. ✅ No sensitive information is exposed

---

**🔥 BlackPhoenix Red Team Toolkit is ready for clean GitHub deployment!**

*Remember: Always review the uploaded repository to ensure no sensitive information has been accidentally included.*
