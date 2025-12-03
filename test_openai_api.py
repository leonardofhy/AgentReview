#!/usr/bin/env python3
"""
Script to load .env and test OpenAI API connection
"""
import os
import sys
from pathlib import Path

# Load environment variables from .env file
def load_env_file(env_path=".env"):
    """Load environment variables from .env file"""
    if not os.path.exists(env_path):
        print(f"Error: {env_path} file not found")
        return False
    
    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#"):
                    # Handle export statements
                    if line.startswith("export "):
                        line = line[7:]  # Remove 'export ' prefix
                    
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
                        print(f"✓ Loaded {key.strip()}")
        return True
    except Exception as e:
        print(f"Error loading .env file: {e}")
        return False


def test_openai_api():
    """Test OpenAI API connection"""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed")
        print("Install it with: pip install openai")
        return False
    
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment")
        return False
    
    print(f"\n✓ Found API key: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test with a simple request
        print("\nTesting OpenAI API with a simple request...")
        response = client.responses.create(
            model="gpt-5.1",
            input="Write a short bedtime story about a unicorn."
        )
        
        result = response.output_text
        print(f"✓ API Response: {result}")
        print(f"\n✓ OpenAI API test successful!")
        return True
        
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("OpenAI API Test Script")
    print("=" * 50)
    
    # Load .env file
    print("\n1. Loading .env file...")
    if not load_env_file(".env"):
        sys.exit(1)
    
    # Test OpenAI API
    print("\n2. Testing OpenAI API...")
    success = test_openai_api()
    
    print("\n" + "=" * 50)
    sys.exit(0 if success else 1)
