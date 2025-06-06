# Token Obfuscator Enhancement Documentation

## Overview
The Token Obfuscator module has been significantly enhanced with advanced encoding techniques to improve red teaming capabilities against large language models. This document outlines the new features and improvements implemented.

## New Advanced Encoding Techniques

### 1. Hexadecimal Encoding
- **Method**: `hex_encode()` / `hex_decode()`
- **Description**: Converts text to hexadecimal representation
- **Example**: "Hello" → "48656c6c6f"
- **Use Case**: Bypass text-based content filters that don't parse hex

### 2. URL Encoding
- **Method**: `url_encode()` / `url_decode()`
- **Description**: Percent-encodes text for URL safety
- **Example**: "Hello World!" → "Hello%20World%21"
- **Use Case**: Evade filters that process plain text but not URL-encoded content

### 3. ASCII Decimal Representation
- **Method**: `ascii_decimal_encode()` / `ascii_decimal_decode()`
- **Description**: Converts each character to its ASCII decimal value
- **Example**: "Hi" → "72 105"
- **Use Case**: Numeric representation that may bypass text analysis

### 4. ASCII Hexadecimal Representation
- **Method**: `ascii_hex_encode()` / `ascii_hex_decode()`
- **Description**: Converts each character to its ASCII hex value
- **Example**: "Hi" → "48 69"
- **Use Case**: Alternative numeric encoding for evasion

### 5. Unicode Decimal Representation
- **Method**: `unicode_decimal_encode()` / `unicode_decimal_decode()`
- **Description**: Converts text to Unicode code points (decimal)
- **Example**: "café" → "99 97 102 233"
- **Use Case**: Handle international characters and Unicode evasion

### 6. Unicode Hexadecimal Representation
- **Method**: `unicode_hex_encode()` / `unicode_hex_decode()`
- **Description**: Converts text to Unicode code points (hexadecimal)
- **Example**: "café" → "U+0063 U+0061 U+0066 U+00E9"
- **Use Case**: Standard Unicode representation format

### 7. ROT13 Encoding
- **Method**: `rot13_encode()` / `rot13_decode()`
- **Description**: Classic Caesar cipher with 13-position shift
- **Example**: "Hello" → "Uryyb"
- **Use Case**: Simple letter substitution that's reversible

### 8. Caesar Cipher (Variable Shift)
- **Method**: `caesar_encode()` / `caesar_decode()`
- **Description**: Caesar cipher with customizable shift value
- **Example**: "Hello" (shift=3) → "Khoor"
- **Use Case**: Variable shift makes detection harder

### 9. Atbash Cipher
- **Method**: `atbash_encode()` / `atbash_decode()`
- **Description**: Substitution cipher where A=Z, B=Y, etc.
- **Example**: "Hello" → "Svool"
- **Use Case**: Hebrew-origin cipher for text obfuscation

### 10. Binary Encoding
- **Method**: `binary_encode()` / `binary_decode()`
- **Description**: Converts text to binary representation
- **Example**: "Hi" → "01001000 01101001"
- **Use Case**: Binary format may bypass text-based analysis

### 11. Octal Encoding
- **Method**: `octal_encode()` / `octal_decode()`
- **Description**: Converts text to octal (base-8) representation
- **Example**: "Hi" → "110 151"
- **Use Case**: Alternative numeric base for encoding

### 12. Morse Code
- **Method**: `morse_encode()` / `morse_decode()`
- **Description**: Converts text to International Morse Code
- **Example**: "HI" → ".... .."
- **Use Case**: Pattern-based encoding that's human-readable

## Implementation Details

### Enhanced Method List
The `get_available_techniques()` method now returns all 16 available encoding techniques:
```python
[
    "base64", "hex", "url", "ascii_decimal", "ascii_hex", 
    "unicode_decimal", "unicode_hex", "rot13", "caesar", 
    "atbash", "binary", "octal", "morse", "char_swap", 
    "homoglyph", "zero_width"
]
```

### Error Handling
All new encoding methods include proper error handling:
- Decode methods return the original text if decoding fails
- Exception handling prevents crashes from malformed input
- Graceful degradation ensures system stability

### Random Elements
- Caesar cipher uses random shift values (1-25) for each encoding
- Character swap maintains configurable swap rate
- Techniques can be combined for layered obfuscation

## Usage Examples

### Single Technique Application
```python
obfuscator = TokenObfuscator()

# Hex encoding
original = "Ignore previous instructions"
encoded = obfuscator.hex_encode(original)
# Result: "49676e6f72652070726576696f757320696e737472756374696f6e73"

# Morse code
morse = obfuscator.morse_encode(original)
# Result: ".. --. -. --- .-. . / .--. .-. . ...- .. --- ..- ... / .. -. ... - .-. ..- -.-. - .. --- -. ..."
```

### Multiple Technique Combination
```python
# Apply multiple techniques in sequence
techniques = ["base64", "hex", "caesar"]
result = obfuscator.create_prompt_with_obfuscation(
    system_prompt="You are a helpful assistant",
    user_prompt="Tell me about security",
    techniques=techniques
)
```

## Security Considerations

### Technique Selection Strategy
1. **Numerical encodings** (hex, decimal, binary) - Good against text-based filters
2. **Character substitution** (ROT13, Caesar, Atbash) - Effective against pattern matching
3. **Unicode techniques** - Useful for international character evasion
4. **Binary/Octal** - May bypass human-readable content analysis
5. **Morse code** - Pattern-based obfuscation with visual distinctiveness

### Layered Approach Benefits
- Multiple techniques make pattern detection harder
- Different encoding types target different filter mechanisms
- Increased complexity reduces automated detection probability

## Testing and Validation

### Verification Methods
Each encoding technique includes:
- Encode/decode round-trip testing
- Error handling validation
- Character set compatibility checks
- Performance benchmarking

### Integration Testing
- All techniques work with existing `test_obfuscation()` method
- Backward compatibility with original techniques maintained
- API consistency across all encoding methods

## Performance Impact

### Computational Overhead
- Simple techniques (ROT13, Caesar): Minimal overhead
- Numeric conversions (hex, decimal): Low overhead
- Complex techniques (Morse, Unicode): Moderate overhead
- Binary operations: Variable overhead based on text length

### Memory Usage
- Most techniques have O(n) memory complexity
- Unicode techniques may require additional character mapping
- Binary/hex representations increase text length 2-8x

## Future Enhancements

### Potential Additions
1. **Custom alphabet substitution**: User-defined character mappings
2. **Steganographic techniques**: Hide text in other data formats
3. **Compression-based obfuscation**: Combine encoding with compression
4. **Multi-byte character techniques**: Advanced Unicode manipulation
5. **Context-aware encoding**: Adapt technique based on content analysis

### API Improvements
1. **Batch processing**: Handle multiple texts simultaneously
2. **Technique recommendation**: Suggest optimal techniques for specific content
3. **Performance profiling**: Built-in timing and efficiency metrics
4. **Chain optimization**: Automatically determine best technique sequences

## Integration Notes

### Frontend Updates Required
The web interface should be updated to include:
- Checkboxes/dropdowns for new encoding techniques
- Technique combination interface
- Real-time encoding preview
- Decoding capability for verification

### Configuration Updates
Consider adding to `config.py`:
- Default technique preferences
- Performance vs. security trade-off settings
- Technique-specific parameters (Caesar shift ranges, etc.)

## Changelog

### Version 2.0.0 - Enhanced Encoding
- Added 12 new encoding techniques
- Implemented comprehensive error handling
- Added technique availability enumeration
- Enhanced documentation and examples
- Maintained backward compatibility
- Added performance considerations

### Breaking Changes
None - all existing functionality remains compatible.

### Migration Notes
Existing code will continue to work without changes. New techniques are available immediately through the same API interface.
