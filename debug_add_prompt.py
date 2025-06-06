#!/usr/bin/env python3
"""
Debug script to test the Add Prompt functionality
"""

import requests
import json

# Test the API endpoint directly
def test_add_prompt_api():
    url = "http://localhost:5001/api/prompts"
    
    test_prompt = {
        "name": "Test Prompt Debug",
        "content": "This is a test prompt to debug the add functionality.",
        "category": "debug",
        "description": "Test prompt for debugging",
        "tags": "debug,test"
    }
    
    try:
        print("Testing API endpoint...")
        response = requests.post(url, json=test_prompt, headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ API endpoint working correctly!")
            data = response.json()
            print(f"Created prompt with ID: {data.get('prompt', {}).get('id')}")
        else:
            print("❌ API endpoint failed")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

def test_get_prompts():
    url = "http://localhost:5001/api/prompts"
    
    try:
        print("\nTesting GET prompts...")
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"✅ Found {len(data.get('prompts', []))} prompts")
            for prompt in data.get('prompts', [])[:3]:  # Show first 3
                print(f"  - {prompt.get('name')} (ID: {prompt.get('id')})")
        else:
            print("❌ GET prompts failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing GET: {e}")

if __name__ == "__main__":
    print("🔍 Debugging Add Prompt Functionality\n")
    test_get_prompts()
    test_add_prompt_api()
    test_get_prompts()
