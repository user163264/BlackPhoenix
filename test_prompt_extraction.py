#!/usr/bin/env python3
"""
Test script for the new Prompt Extraction plugin
Verifies that the implementation works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_prompt_extraction_plugin():
    """Test the prompt extraction plugin functionality"""
    
    print("🔬 Testing Prompt Extraction Plugin")
    print("=" * 50)
    
    try:
        from modules.prompt_extraction import PromptExtractionTester, PromptExtractionPlugin
        from config import Config
        
        print("✅ Module imports successful")
        
        # Test plugin creation
        tester = PromptExtractionTester()
        print("✅ PromptExtractionTester initialized")
        
        # Test plugin instantiation
        plugin = tester.create_plugin(
            purpose="customer service assistant",
            config={"system_prompt": "You are a helpful customer service assistant."}
        )
        print("✅ Plugin created successfully")
        print(f"   Plugin ID: {plugin.get_plugin_id()}")
        
        # Test template generation
        template = plugin.get_template()
        print("✅ Template generation working")
        print(f"   Template length: {len(template)} characters")
        
        # Test assertions
        assertions = plugin.get_assertions("test prompt")
        print("✅ Assertions generated")
        print(f"   Number of assertions: {len(assertions)}")
        
        # Test fallback prompt generation (without API call)
        fallback_tests = plugin._generate_fallback_tests(3)
        print("✅ Fallback test generation working")
        print(f"   Generated {len(fallback_tests)} fallback tests")
        
        for i, test in enumerate(fallback_tests, 1):
            print(f"   {i}. {test.prompt}")
        
        print("\n🎯 Basic functionality tests passed!")
        print("📝 Note: Live API tests require OpenAI API key configuration")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_routes():
    """Test that the Flask routes are properly configured"""
    print("\n🌐 Testing Flask Route Configuration")
    print("=" * 50)
    
    try:
        # Read the app.py file to verify routes exist
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        # Check for prompt extraction routes
        routes_to_check = [
            '@app.route(\'/prompt-extraction\')',
            '@app.route(\'/api/prompt-extraction/generate\'',
            '@app.route(\'/api/prompt-extraction/test\''
        ]
        
        for route in routes_to_check:
            if route in app_content:
                print(f"✅ Route found: {route}")
            else:
                print(f"❌ Route missing: {route}")
                return False
        
        # Check for import statement
        if 'from modules.prompt_extraction import PromptExtractionTester' in app_content:
            print("✅ Import statement found in app.py")
        else:
            print("⚠️  Import statement not found in app.py (will be imported dynamically)")
        
        print("✅ Flask routes configured correctly")
        return True
        
    except Exception as e:
        print(f"❌ Route test failed: {e}")
        return False

def test_template_exists():
    """Test that the HTML template exists"""
    print("\n🎨 Testing Template Configuration")
    print("=" * 50)
    
    try:
        template_path = 'templates/prompt_extraction.html'
        
        if os.path.exists(template_path):
            print(f"✅ Template found: {template_path}")
            
            # Check template size
            size = os.path.getsize(template_path)
            print(f"   Template size: {size:,} bytes")
            
            # Quick content check
            with open(template_path, 'r') as f:
                content = f.read()
            
            if 'Prompt Extraction Testing' in content:
                print("✅ Template title found")
            if 'prompt-extraction' in content:
                print("✅ Template navigation found")
            if '/api/prompt-extraction/generate' in content:
                print("✅ API endpoint references found")
            
            return True
        else:
            print(f"❌ Template not found: {template_path}")
            return False
            
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def test_homepage_integration():
    """Test that the homepage includes the new module"""
    print("\n🏠 Testing Homepage Integration")
    print("=" * 50)
    
    try:
        homepage_path = 'templates/prompt_generation_index.html'
        
        if os.path.exists(homepage_path):
            with open(homepage_path, 'r') as f:
                content = f.read()
            
            if 'Prompt Extraction Testing' in content:
                print("✅ Module title found on homepage")
            if '/prompt-extraction' in content:
                print("✅ Module link found on homepage")
            if 'fa-search' in content:
                print("✅ Module icon found on homepage")
            
            print("✅ Homepage integration complete")
            return True
        else:
            print(f"❌ Homepage template not found: {homepage_path}")
            return False
            
    except Exception as e:
        print(f"❌ Homepage test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Red Team Toolkit - Prompt Extraction Plugin Tests")
    print("=" * 60)
    
    tests = [
        test_prompt_extraction_plugin,
        test_api_routes, 
        test_template_exists,
        test_homepage_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results Summary")
    print("=" * 30)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Prompt Extraction plugin is ready!")
        print("\n🚀 Next Steps:")
        print("1. Start the application: ./quick_start.sh")
        print("2. Navigate to: http://localhost:5001/prompt-extraction")
        print("3. Configure your OpenAI API key if not already set")
        print("4. Test prompt extraction attacks against target systems")
    else:
        print(f"⚠️  {total - passed} tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    success = main()
    sys.exit(0 if success else 1)
