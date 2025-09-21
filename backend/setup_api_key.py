#!/usr/bin/env python3
"""Setup script for OpenAI API key configuration."""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with API key configuration."""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("🔑 Setting up OpenAI API key...")
    print("\nTo get your API key:")
    print("1. Go to https://platform.openai.com/")
    print("2. Sign in to your account")
    print("3. Navigate to API Keys section")
    print("4. Create a new secret key")
    print("5. Copy the key (starts with 'sk-')")
    
    api_key = input("\nEnter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting...")
        return False
    
    if not api_key.startswith("sk-"):
        print("⚠️  Warning: API key doesn't start with 'sk-'. Please verify it's correct.")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            return False
    
    # Create .env file content
    env_content = f"""# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# Database Configuration
DATABASE_URL=sqlite:///./resume_evaluation.db

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=["pdf","docx","txt"]

# Scoring Weights
HARD_MATCH_WEIGHT=0.4
SEMANTIC_MATCH_WEIGHT=0.6
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        # Set file permissions (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(env_file, 0o600)
        
        print(f"✅ .env file created successfully!")
        print(f"📁 Location: {env_file.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_api_key():
    """Test if the API key is working."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ No API key found in .env file")
            return False
        
        if api_key == "your-openai-api-key-here":
            print("❌ Please update the API key in .env file")
            return False
        
        print("✅ API key found in .env file")
        print(f"🔑 Key: {api_key[:10]}...{api_key[-4:]}")
        return True
        
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Resume Evaluation System - API Key Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if Path(".env").exists():
        print("📁 .env file found")
        if test_api_key():
            print("✅ API key is configured and ready!")
            return
        else:
            print("⚠️  API key needs to be updated")
            recreate = input("Recreate .env file? (y/N): ").strip().lower()
            if recreate == 'y':
                os.remove(".env")
            else:
                print("Please manually update the .env file with your API key")
                return
    
    # Create .env file
    if create_env_file():
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Run: python run_system.py")
        print("2. Open: http://localhost:8501")
        print("3. Test the evaluation system")
        
        if test_api_key():
            print("\n✅ API key is working correctly!")
        else:
            print("\n⚠️  Please check your API key configuration")
    else:
        print("\n❌ Setup failed. Please try again.")

if __name__ == "__main__":
    main()
