#!/usr/bin/env python3
"""
Test System Saturation Module
Quick test to verify the system-saturation functionality is working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.system_saturator import SystemSaturator
from config import Config

def test_system_saturator():
    """Test the SystemSaturator module functionality"""
    print("🔬 Testing System Saturation Module")
    print("=" * 50)
    
    try:
        # Initialize the system saturator
        print("📦 Initializing SystemSaturator...")
        saturator = SystemSaturator()
        print("✅ SystemSaturator initialized successfully")
        
        # Test token counting
        print("\n🔢 Testing token counting...")
        test_text = "Hello world, this is a test prompt for token counting."
        token_count = saturator.count_tokens(test_text)
        print(f"✅ Token count for test text: {token_count}")
        
        # Test noise generation
        print("\n🎭 Testing noise generation...")
        noise = saturator.generate_noise(100)
        print(f"✅ Generated noise (length: {len(noise)}): {noise[:50]}...")
        
        # Test repetitive text generation
        print("\n🔄 Testing repetitive text generation...")
        repetitive = saturator.generate_repetitive_text("Test phrase", 5)
        print(f"✅ Generated repetitive text: {repetitive[:100]}...")
        
        # Test nested structure generation
        print("\n🏗️ Testing nested structure generation...")
        nested = saturator.generate_nested_structure(3, 3)
        print(f"✅ Generated nested structure: {str(nested)[:100]}...")
        
        # Test basic saturation prompt creation
        print("\n💉 Testing saturation prompt creation...")
        system_prompt = "You are a helpful assistant."
        user_prompt = "Tell me about the weather."
        params = {"length": 200, "target": "system"}
        
        saturated = saturator.create_saturation_prompt(
            system_prompt, user_prompt, "noise", params
        )
        
        print(f"✅ Created saturated prompt with {len(saturated['saturated']['system'])} chars in system prompt")
        print(f"   Original system length: {len(saturated['original']['system'])}")
        print(f"   Saturated system length: {len(saturated['saturated']['system'])}")
        
        print("\n🎉 All System Saturation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system_saturator()
    if success:
        print("\n🚀 System Saturation module is ready for use!")
        print("   You can now start the web application:")
        print("   ./quick_start.sh")
        print("   or")
        print("   python app.py")
    else:
        print("\n💥 System Saturation module has issues that need to be resolved.")
    
    sys.exit(0 if success else 1)
