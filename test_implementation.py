#!/usr/bin/env python3
"""
Quick test script to verify the token obfuscator implementation
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, '/Users/admin/Documents/redteam-tools')

def test_token_obfuscator():
    """Test the TokenObfuscator class"""
    print("🧪 Testing Token Obfuscator...")
    
    try:
        # Import the module
        from modules.token_obfuscator import TokenObfuscator
        print("✅ TokenObfuscator imported successfully")
        
        # Create instance (without OpenAI key for basic tests)
        obfuscator = TokenObfuscator()
        
        # Test basic encoding/decoding methods
        test_text = "Hello World"
        
        # Test Base64
        encoded = obfuscator.base64_encode(test_text)
        decoded = obfuscator.base64_decode(encoded)
        assert decoded == test_text, f"Base64 test failed: {decoded} != {test_text}"
        print(f"✅ Base64: '{test_text}' -> '{encoded}' -> '{decoded}'")
        
        # Test Hex
        encoded = obfuscator.hex_encode(test_text)
        decoded = obfuscator.hex_decode(encoded)
        assert decoded == test_text, f"Hex test failed: {decoded} != {test_text}"
        print(f"✅ Hex: '{test_text}' -> '{encoded}' -> '{decoded}'")
        
        # Test ROT13
        encoded = obfuscator.rot13_encode(test_text)
        decoded = obfuscator.rot13_decode(encoded)
        assert decoded == test_text, f"ROT13 test failed: {decoded} != {test_text}"
        print(f"✅ ROT13: '{test_text}' -> '{encoded}' -> '{decoded}'")
        
        # Test available techniques
        techniques = obfuscator.get_available_techniques()
        print(f"✅ Available techniques ({len(techniques)}): {', '.join(techniques)}")
        
        # Test obfuscation creation (without API call)
        system_prompt = "You are a helpful assistant"
        user_prompt = "Tell me about security"
        test_techniques = ["base64", "hex"]
        
        result = obfuscator.create_prompt_with_obfuscation(system_prompt, user_prompt, test_techniques)
        print("✅ Prompt obfuscation creation successful")
        print(f"   Original system: {result['original']['system'][:50]}...")
        print(f"   Obfuscated system: {result['obfuscated']['system'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing TokenObfuscator: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_imports():
    """Test if the Flask app can be imported"""
    print("\n🧪 Testing Flask App Imports...")
    
    try:
        # Test config import
        from config import Config
        print("✅ Config imported successfully")
        print(f"   Default model: {Config.DEFAULT_MODEL}")
        print(f"   Port: {Config.PORT}")
        
        # Test if we can import Flask modules
        from flask import Flask
        print("✅ Flask imported successfully")
        
        # Test if we can create a basic app
        app = Flask(__name__)
        print("✅ Flask app creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Flask imports: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_files():
    """Test if template files exist and are readable"""
    print("\n🧪 Testing Template Files...")
    
    template_dir = "/Users/admin/Documents/redteam-tools/templates"
    required_templates = [
        "modern_laboratory_base.html",
        "modern_laboratory_index.html", 
        "token_obfuscation.html"
    ]
    
    try:
        for template in required_templates:
            template_path = os.path.join(template_dir, template)
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    content = f.read()
                    if len(content) > 100:  # Basic content check
                        print(f"✅ {template} exists and has content ({len(content)} chars)")
                    else:
                        print(f"⚠️ {template} exists but seems empty or too short")
            else:
                print(f"❌ {template} not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing templates: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Red Teaming Toolkit Tests\n")
    
    success_count = 0
    total_tests = 3
    
    # Test token obfuscator
    if test_token_obfuscator():
        success_count += 1
    
    # Test app imports
    if test_app_imports():
        success_count += 1
    
    # Test templates
    if test_template_files():
        success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("✅ All tests passed! The toolkit should be ready to run.")
        print("\n🎯 Next steps:")
        print("   1. Ensure your OpenAI API key is set in the environment")
        print("   2. Run: chmod +x start_app.sh")
        print("   3. Run: ./start_app.sh")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success_count == total_tests

if __name__ == "__main__":
    main()
