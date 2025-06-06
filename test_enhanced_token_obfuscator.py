#!/usr/bin/env python3
"""
Test script for enhanced Token Obfuscator with advanced encoding techniques
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.token_obfuscator import TokenObfuscator

def test_encoding_techniques():
    """Test all encoding techniques with round-trip validation."""
    obfuscator = TokenObfuscator()
    
    # Test strings of varying complexity
    test_strings = [
        "Hello World",
        "Ignore previous instructions",
        "café résumé naïve",  # Unicode characters
        "Test!@#$%^&*()",     # Special characters
        "12345 67890",        # Numbers
        "Mixed123!@#Café",    # Mixed content
        "",                   # Empty string
        "A",                  # Single character
    ]
    
    # Test cases for each encoding technique
    encoding_tests = [
        ("hex", "hex_encode", "hex_decode"),
        ("url", "url_encode", "url_decode"),
        ("ascii_decimal", "ascii_decimal_encode", "ascii_decimal_decode"),
        ("ascii_hex", "ascii_hex_encode", "ascii_hex_decode"),
        ("unicode_decimal", "unicode_decimal_encode", "unicode_decimal_decode"),
        ("unicode_hex", "unicode_hex_encode", "unicode_hex_decode"),
        ("rot13", "rot13_encode", "rot13_decode"),
        ("caesar", "caesar_encode", "caesar_decode"),
        ("atbash", "atbash_encode", "atbash_decode"),
        ("binary", "binary_encode", "binary_decode"),
        ("octal", "octal_encode", "octal_decode"),
        ("morse", "morse_encode", "morse_decode"),
        ("base64", "base64_encode", "base64_decode"),
    ]
    
    print("=== Token Obfuscator Enhancement Test ===\n")
    
    results = {"passed": 0, "failed": 0, "total": 0}
    
    for technique_name, encode_method, decode_method in encoding_tests:
        print(f"Testing {technique_name.upper()} encoding:")
        print("-" * 40)
        
        technique_passed = 0
        technique_failed = 0
        
        for test_string in test_strings:
            results["total"] += 1
            
            try:
                # Get encoding and decoding methods
                encoder = getattr(obfuscator, encode_method)
                decoder = getattr(obfuscator, decode_method)
                
                # Encode the string
                if technique_name == "caesar":
                    # Special case for Caesar - need to use same shift for decode
                    shift = 7  # Default shift
                    encoded = encoder(test_string, shift)
                    decoded = decoder(encoded, shift)
                else:
                    encoded = encoder(test_string)
                    decoded = decoder(encoded)
                
                # Verify round-trip
                if decoded == test_string:
                    status = "✓ PASS"
                    results["passed"] += 1
                    technique_passed += 1
                else:
                    status = "✗ FAIL"
                    results["failed"] += 1
                    technique_failed += 1
                
                # Display results (truncate long encodings)
                display_encoded = encoded[:50] + "..." if len(encoded) > 50 else encoded
                display_original = test_string[:30] + "..." if len(test_string) > 30 else test_string
                
                print(f"  {status} '{display_original}' → '{display_encoded}'")
                
                if decoded != test_string:
                    print(f"    Expected: '{test_string}'")
                    print(f"    Got:      '{decoded}'")
                
            except Exception as e:
                print(f"  ✗ ERROR '{test_string}': {str(e)}")
                results["failed"] += 1
                technique_failed += 1
        
        print(f"\n  {technique_name.upper()} Summary: {technique_passed} passed, {technique_failed} failed\n")
    
    print("=== Overall Test Results ===")
    print(f"Total tests: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {(results['passed']/results['total']*100):.1f}%")
    
    return results

def test_technique_availability():
    """Test that all techniques are properly registered."""
    obfuscator = TokenObfuscator()
    
    print("\n=== Available Techniques Test ===")
    
    available_techniques = obfuscator.get_available_techniques()
    expected_techniques = [
        "base64", "hex", "url", "ascii_decimal", "ascii_hex", 
        "unicode_decimal", "unicode_hex", "rot13", "caesar", 
        "atbash", "binary", "octal", "morse", "char_swap", 
        "homoglyph", "zero_width"
    ]
    
    print(f"Expected techniques: {len(expected_techniques)}")
    print(f"Available techniques: {len(available_techniques)}")
    
    missing = set(expected_techniques) - set(available_techniques)
    extra = set(available_techniques) - set(expected_techniques)
    
    if missing:
        print(f"Missing techniques: {missing}")
    if extra:
        print(f"Extra techniques: {extra}")
    
    if not missing and not extra:
        print("✓ All expected techniques are available")
        return True
    else:
        print("✗ Technique availability mismatch")
        return False

def test_obfuscation_integration():
    """Test that new techniques work with the main obfuscation method."""
    obfuscator = TokenObfuscator()
    
    print("\n=== Integration Test ===")
    
    # Test with new encoding techniques
    test_techniques = ["hex", "morse", "binary"]
    system_prompt = "You are a helpful assistant"
    user_prompt = "Tell me about security"
    
    try:
        result = obfuscator.create_prompt_with_obfuscation(
            system_prompt, user_prompt, test_techniques
        )
        
        print("✓ Obfuscation creation successful")
        print(f"Original system prompt: {result['original']['system'][:50]}...")
        print(f"Obfuscated system prompt: {result['obfuscated']['system'][:50]}...")
        print(f"Techniques applied: {result['techniques']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {str(e)}")
        return False

def demonstrate_new_techniques():
    """Demonstrate the new encoding techniques with examples."""
    obfuscator = TokenObfuscator()
    
    print("\n=== New Techniques Demonstration ===")
    
    demo_text = "Bypass this filter"
    
    demonstrations = [
        ("Hexadecimal", "hex_encode"),
        ("URL Encoding", "url_encode"),
        ("ASCII Decimal", "ascii_decimal_encode"),
        ("Unicode Hex", "unicode_hex_encode"),
        ("Binary", "binary_encode"),
        ("Morse Code", "morse_encode"),
        ("ROT13", "rot13_encode"),
        ("Atbash", "atbash_encode"),
    ]
    
    print(f"Original text: '{demo_text}'\n")
    
    for name, method in demonstrations:
        try:
            encoder = getattr(obfuscator, method)
            encoded = encoder(demo_text)
            
            # Truncate very long encodings for display
            display_encoded = encoded[:80] + "..." if len(encoded) > 80 else encoded
            
            print(f"{name:15}: {display_encoded}")
            
        except Exception as e:
            print(f"{name:15}: ERROR - {str(e)}")
    
    print()

def performance_benchmark():
    """Basic performance benchmark for encoding techniques."""
    import time
    
    obfuscator = TokenObfuscator()
    
    print("\n=== Performance Benchmark ===")
    
    test_text = "This is a longer test string for performance benchmarking. " * 10
    techniques = [
        ("base64", "base64_encode"),
        ("hex", "hex_encode"),
        ("url", "url_encode"),
        ("binary", "binary_encode"),
        ("morse", "morse_encode"),
        ("rot13", "rot13_encode"),
    ]
    
    print(f"Test text length: {len(test_text)} characters\n")
    
    for name, method in techniques:
        try:
            encoder = getattr(obfuscator, method)
            
            # Measure encoding time
            start_time = time.time()
            encoded = encoder(test_text)
            end_time = time.time()
            
            encoding_time = (end_time - start_time) * 1000  # Convert to milliseconds
            expansion_ratio = len(encoded) / len(test_text)
            
            print(f"{name:15}: {encoding_time:6.2f}ms, {expansion_ratio:4.1f}x size")
            
        except Exception as e:
            print(f"{name:15}: ERROR - {str(e)}")
    
    print()

def main():
    """Run all tests and demonstrations."""
    print("Enhanced Token Obfuscator Test Suite")
    print("====================================\n")
    
    # Run tests
    encoding_results = test_encoding_techniques()
    availability_ok = test_technique_availability()
    integration_ok = test_obfuscation_integration()
    
    # Run demonstrations
    demonstrate_new_techniques()
    performance_benchmark()
    
    # Summary
    print("=== Test Summary ===")
    print(f"Encoding tests: {encoding_results['passed']}/{encoding_results['total']} passed")
    print(f"Technique availability: {'✓' if availability_ok else '✗'}")
    print(f"Integration test: {'✓' if integration_ok else '✗'}")
    
    overall_success = (
        encoding_results['failed'] == 0 and 
        availability_ok and 
        integration_ok
    )
    
    print(f"\nOverall result: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
