"""
Helper script to check and guide OpenAI API key setup

Usage:
    python check_env_setup.py
"""

import os
from pathlib import Path

def check_env_setup():
    """Check if .env file exists and contains OPENAI_API_KEY"""
    
    print("="*70)
    print("Checking OpenAI API Key Configuration".center(70))
    print("="*70)
    print()
    
    # Check for .env file
    backend_dir = Path("backend")
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        print("[!] .env file not found!")
        print(f"   Expected location: {env_file.absolute()}")
        print()
        print("To set up your API key:")
        print("   1. Create a file named '.env' in the 'backend' directory")
        print("   2. Add your OpenAI API key to it:")
        print()
        print("      OPENAI_API_KEY=sk-proj-your-key-here")
        print()
        print("Get your API key from: https://platform.openai.com/api-keys")
        print("   (Free tier: $5 credit available)")
        print()
        return False
    
    print(f"[OK] .env file found: {env_file.absolute()}")
    print()
    
    # Try to load the .env file
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("[!] OPENAI_API_KEY not found in .env file!")
            print()
            print("Add this line to your .env file:")
            print("   OPENAI_API_KEY=sk-proj-your-key-here")
            print()
            print("Get your API key from: https://platform.openai.com/api-keys")
            return False
        
        # Check if key looks valid (starts with sk-)
        if not api_key.startswith("sk-"):
            print("[WARNING] API key doesn't start with 'sk-'")
            print(f"   Current value starts with: {api_key[:5]}...")
            print()
            print("   OpenAI API keys typically start with 'sk-proj-' or 'sk-'")
            print("   Make sure you copied the full key.")
            print()
        
        # Mask the key for display
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"[OK] OPENAI_API_KEY found: {masked_key}")
        print()
        print("Your API key is configured!")
        print()
        print("Next steps:")
        print("   1. Make sure your backend server is running")
        print("   2. Restart the backend if it was already running")
        print("   3. Run the test script: python test_ai_features.py")
        print()
        
        return True
        
    except ImportError:
        print("[!] python-dotenv not installed!")
        print("   Install it with: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"[!] Error reading .env file: {e}")
        return False


if __name__ == "__main__":
    success = check_env_setup()
    if not success:
        print()
        print("Quick setup guide:")
        print("   cd backend")
        print("   echo OPENAI_API_KEY=sk-proj-your-key-here > .env")
        print("   (Replace 'sk-proj-your-key-here' with your actual API key)")
        print()
    exit(0 if success else 1)

