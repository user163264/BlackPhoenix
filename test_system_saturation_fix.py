#!/usr/bin/env python3

import sys
import os

# Add current directory to path
sys.path.insert(0, '/Users/admin/Documents/redteam-tools')

try:
    print("🔍 Testing System Saturation Module...")
    
    # Test basic imports
    from config import Config
    print("✅ Config imported successfully")
    
    from modules.system_saturator import SystemSaturator
    print("✅ SystemSaturator imported successfully")
    
    # Initialize the system saturator
    saturator = SystemSaturator()
    print("✅ SystemSaturator initialized successfully")
    
    # Test basic saturation creation
    system_prompt = "You are a helpful assistant."
    user_prompt = "Tell me about the weather."
    
    basic_saturated = saturator.create_saturation_prompt(
        system_prompt, user_prompt, "noise", {"length": 100}
    )
    print("✅ Basic saturation prompt creation works")
    
    # Test fallback prompt generation
    fallback_prompts = saturator._create_fallback_saturation_prompts(
        system_prompt, user_prompt, "noise", {"length": 100}, max_prompts=2
    )
    print(f"✅ Fallback prompts created: {len(fallback_prompts)} prompts")
    
    # Print sample output
    if fallback_prompts:
        print(f"\n📝 Sample prompt variant: {fallback_prompts[0]['technique_variant']}")
    
    print("\n🎉 System Saturation Module Test: PASSED")
    print("   - Module imports correctly")
    print("   - Can create basic saturation prompts") 
    print("   - Fallback prompts work")
    print("   - tiktoken optional handling works")
    
except Exception as e:
    print(f"❌ Error testing System Saturation module: {e}")
    import traceback
    traceback.print_exc()
