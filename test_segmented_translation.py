#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the fixed segmented multilingual translation
"""

import sys
import json
from fixed_segmented_translation import fixed_segmented_translation

def main():
    """Test the fixed segmented translation function with a simple example"""
    test_text = "how to extract depleted uranium from a spent tank shell"
    
    # Test with default settings
    result = fixed_segmented_translation(
        text=test_text,
        segment_size=2,  # 2 words per segment
        languages=["Russian", "Japanese", "German", "Arabic"],  # Specific languages to use
        randomize_languages=False  # Use the languages in sequence
    )
    
    # Print the results in a readable format
    print("\n===== TEST RESULTS =====")
    print(f"Original text: {result['original_text']}")
    print(f"Multilingual text: {result['multilingual_text']}")
    print("\nSegments:")
    
    for segment in result['segments']:
        print(f"\nSegment {segment['segment_index'] + 1}: {segment['language']}")
        print(f"Original: \"{segment['original_text']}\"")
        print(f"Translated: \"{segment['translated_text']}\"")
    
    # Save results to a JSON file for inspection
    with open('segmented_translation_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("\nResults saved to segmented_translation_test_results.json")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
