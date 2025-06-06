"""
Token Obfuscation Module for Red Team Toolkit
Handles various token obfuscation techniques for testing AI model robustness
"""

import json
import random
import string
import base64
from typing import List, Dict, Any
import openai


class TokenObfuscator:
    """
    Handles token obfuscation techniques for adversarial testing
    """
    
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        self.client = openai.OpenAI(api_key=api_key)
        
    def simple_substitution(self, text: str) -> str:
        """Replace characters with similar looking alternatives"""
        substitutions = {
            'a': ['@', 'ă', 'α'],
            'e': ['3', 'ē', 'ε'],
            'i': ['1', '!', 'í'],
            'o': ['0', 'ō', 'ο'],
            'u': ['ū', 'μ'],
            's': ['$', '5', 'ş'],
            'l': ['1', '|', 'ļ'],
            't': ['7', '+', 'ţ']
        }
        
        result = ""
        for char in text.lower():
            if char in substitutions and random.random() < 0.3:
                result += random.choice(substitutions[char])
            else:
                result += char
        return result
    
    def unicode_obfuscation(self, text: str) -> str:
        """Use Unicode characters that look similar to ASCII"""
        unicode_map = {
            'a': 'а',  # Cyrillic a
            'c': 'с',  # Cyrillic c
            'e': 'е',  # Cyrillic e
            'o': 'о',  # Cyrillic o
            'p': 'р',  # Cyrillic p
            'x': 'х'   # Cyrillic x
        }
        
        result = ""
        for char in text:
            if char.lower() in unicode_map and random.random() < 0.4:
                if char.isupper():
                    result += unicode_map[char.lower()].upper()
                else:
                    result += unicode_map[char.lower()]
            else:
                result += char
        return result
    
    def base64_obfuscation(self, text: str) -> str:
        """Encode text in base64"""
        encoded = base64.b64encode(text.encode()).decode()
        return f"Decode this base64: {encoded}"
    
    def leetspeak(self, text: str) -> str:
        """Convert to leetspeak"""
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0',
            's': '5', 't': '7', 'l': '1', 'g': '9'
        }
        
        result = ""
        for char in text:
            if char.lower() in leet_map and random.random() < 0.5:
                result += leet_map[char.lower()]
            else:
                result += char
        return result
    
    def word_scrambling(self, text: str) -> str:
        """Scramble words while keeping first and last letters"""
        words = text.split()
        scrambled_words = []
        
        for word in words:
            if len(word) <= 3:
                scrambled_words.append(word)
            else:
                middle = list(word[1:-1])
                random.shuffle(middle)
                scrambled_word = word[0] + ''.join(middle) + word[-1]
                scrambled_words.append(scrambled_word)
        
        return ' '.join(scrambled_words)
    
    def token_insertion(self, text: str) -> str:
        """Insert random tokens between words"""
        words = text.split()
        noise_tokens = ['[NOISE]', '###', '***', '---', '|||']
        
        result = []
        for i, word in enumerate(words):
            result.append(word)
            if i < len(words) - 1 and random.random() < 0.3:
                result.append(random.choice(noise_tokens))
        
        return ' '.join(result)
    
    def apply_obfuscation(self, text: str, method: str) -> str:
        """Apply specified obfuscation method"""
        methods = {
            'substitution': self.simple_substitution,
            'unicode': self.unicode_obfuscation,
            'base64': self.base64_obfuscation,
            'leetspeak': self.leetspeak,
            'scrambling': self.word_scrambling,
            'insertion': self.token_insertion
        }
        
        if method in methods:
            return methods[method](text)
        else:
            raise ValueError(f"Unknown obfuscation method: {method}")
    
    def test_obfuscation(self, original_prompt: str, method: str, system_prompt: str = None) -> Dict[str, Any]:
        """Test obfuscated prompt against AI model"""
        obfuscated_prompt = self.apply_obfuscation(original_prompt, method)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": obfuscated_prompt})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500
            )
            
            return {
                'original': original_prompt,
                'obfuscated': obfuscated_prompt,
                'method': method,
                'response': response.choices[0].message.content,
                'success': True,
                'error': None
            }
        except Exception as e:
            return {
                'original': original_prompt,
                'obfuscated': obfuscated_prompt,
                'method': method,
                'response': None,
                'success': False,
                'error': str(e)
            }
    
    def batch_test(self, prompts: List[str], methods: List[str], system_prompt: str = None) -> List[Dict[str, Any]]:
        """Test multiple prompts with multiple obfuscation methods"""
        results = []
        
        for prompt in prompts:
            for method in methods:
                result = self.test_obfuscation(prompt, method, system_prompt)
                results.append(result)
        
        return results
