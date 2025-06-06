#!/usr/bin/env python3
"""
🚑 FLASK INSTALLATION DIAGNOSTIC
===============================
Complete diagnostic check for Flask installation issues
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print("🐍 Python Version Check")
    print("=" * 30)
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    print()

def check_virtual_environment():
    """Check if we're in a virtual environment"""
    print("🏠 Virtual Environment Check")
    print("=" * 35)
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ Running in virtual environment")
        print(f"   Virtual env path: {sys.prefix}")
    else:
        print("⚠️  Not in virtual environment")
        print("   Recommendation: Activate venv first")
    print()

def test_flask_import():
    """Test Flask import and functionality"""
    print("🌶️  Flask Import Test")
    print("=" * 25)
    
    try:
        import flask
        print(f"✅ Flask imported successfully")
        print(f"   Version: {flask.__version__}")
        print(f"   Location: {flask.__file__}")
        
        # Test Flask app creation
        from flask import Flask, render_template, request, jsonify
        app = Flask(__name__)
        print("✅ Flask app creation successful")
        
        # Check Flask components
        print("✅ Flask components (render_template, request, jsonify) imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Flask error: {e}")
        return False

def test_dependencies():
    """Test other required dependencies"""
    print("📦 Dependencies Test")
    print("=" * 25)
    
    dependencies = [
        ('openai', 'OpenAI client'),
        ('requests', 'HTTP requests'),
        ('dotenv', 'Environment variables'),
        ('langdetect', 'Language detection'),
        ('flask_wtf', 'Flask-WTF forms')
    ]
    
    for module, description in dependencies:
        try:
            if module == 'dotenv':
                from dotenv import load_dotenv
            elif module == 'flask_wtf':
                import flask_wtf
            else:
                __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - Missing")
        except Exception as e:
            print(f"⚠️  {description} - Error: {e}")
    
    print()

def check_flask_init_file():
    """Check if Flask's __init__.py file is corrupt"""
    print("🔍 Flask Installation Integrity")
    print("=" * 35)
    
    try:
        import flask
        flask_init_path = os.path.join(os.path.dirname(flask.__file__), '__init__.py')
        
        if os.path.exists(flask_init_path):
            with open(flask_init_path, 'r') as f:
                content = f.read().strip()
                if content:
                    print("✅ Flask __init__.py file exists and has content")
                    print(f"   Size: {len(content)} characters")
                else:
                    print("❌ Flask __init__.py file is empty - CORRUPTION DETECTED")
                    return False
        else:
            print("❌ Flask __init__.py file missing - CORRUPTION DETECTED")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Cannot check Flask files: {e}")
        return False

def provide_recommendations():
    """Provide fix recommendations"""
    print("🚑 RECOMMENDATIONS")
    print("=" * 20)
    print("If Flask import failed or corruption detected:")
    print("1. Run: ./complete_flask_fix.sh")
    print("2. Or manually: ./rebuild_env.sh")
    print("3. Then: source venv/bin/activate")
    print("4. Finally: python3 app.py")
    print()

def main():
    """Main diagnostic function"""
    print("🚑 FLASK INSTALLATION DIAGNOSTIC")
    print("=" * 40)
    print()
    
    check_python_version()
    check_virtual_environment()
    
    flask_ok = test_flask_import()
    print()
    
    if flask_ok:
        integrity_ok = check_flask_init_file()
        print()
        
        if integrity_ok:
            test_dependencies()
            print("🎉 FLASK INSTALLATION APPEARS HEALTHY!")
            print("🚀 You should be able to run your application")
        else:
            print("❌ FLASK CORRUPTION DETECTED")
            provide_recommendations()
    else:
        print("❌ FLASK INSTALLATION PROBLEM DETECTED")
        provide_recommendations()

if __name__ == "__main__":
    main()
