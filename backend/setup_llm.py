"""Setup script for enabling LLM features in Resume Evaluation System."""

import os
from pathlib import Path

def setup_llm_features():
    """Setup LLM features with OpenAI API key."""
    print("🤖 LLM Features Setup for Resume Evaluation System")
    print("=" * 60)
    
    print("\n📋 Prerequisites:")
    print("1. Get an OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Make sure you have credits in your OpenAI account")
    print("3. Install LLM dependencies: pip install openai langchain")
    
    print("\n🔐 Security Note:")
    print("For GitHub deployment, use GitHub Secrets instead of .env files!")
    print("See GITHUB_DEPLOYMENT.md for detailed instructions.")
    
    print("\n🔧 Setup Options:")
    print("1. Set environment variable (recommended for production)")
    print("2. Create .env file (for local development)")
    print("3. Update config.py directly (not recommended)")
    
    choice = input("\nChoose setup method (1/2/3): ").strip()
    
    if choice == "1":
        setup_environment_variable()
    elif choice == "2":
        setup_env_file()
    elif choice == "3":
        update_config_directly()
    else:
        print("❌ Invalid choice. Please run the script again.")
        return False
    
    print("\n✅ Setup complete!")
    print("\n📝 Next steps:")
    print("1. Set enable_llm = True in config.py")
    print("2. Restart the backend server")
    print("3. Test the LLM features in the frontend")
    
    return True

def setup_environment_variable():
    """Setup environment variable for API key."""
    print("\n🔑 Environment Variable Setup:")
    print("Set the following environment variable:")
    print("OPENAI_API_KEY=your_actual_api_key_here")
    print("\nWindows (PowerShell):")
    print('$env:OPENAI_API_KEY="your_actual_api_key_here"')
    print("\nWindows (Command Prompt):")
    print('set OPENAI_API_KEY=your_actual_api_key_here')
    print("\nLinux/Mac:")
    print('export OPENAI_API_KEY="your_actual_api_key_here"')

def setup_env_file():
    """Setup .env file for API key."""
    print("\n📄 .env File Setup:")
    
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ API key cannot be empty.")
        return False
    
    env_content = f"""# Resume Evaluation System Configuration
OPENAI_API_KEY={api_key}
DATABASE_URL=sqlite:///./resume_evaluation.db
DEBUG=true
HOST=0.0.0.0
PORT=8000
"""
    
    env_file = Path(".env")
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"✅ Created .env file with API key")
        print("⚠️  Remember to add .env to .gitignore to keep your API key secure!")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    return True

def update_config_directly():
    """Update config.py directly with API key."""
    print("\n⚠️  Warning: This method is not recommended for production!")
    print("Your API key will be visible in the source code.")
    
    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Setup cancelled.")
        return False
    
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ API key cannot be empty.")
        return False
    
    config_file = Path("app/config.py")
    try:
        with open(config_file, "r") as f:
            content = f.read()
        
        # Replace the placeholder API key
        content = content.replace('openai_api_key: str = ""', f'openai_api_key: str = "{api_key}"')
        content = content.replace('enable_llm: bool = False', 'enable_llm: bool = True')
        
        with open(config_file, "w") as f:
            f.write(content)
        
        print("✅ Updated config.py with API key and enabled LLM features")
        print("⚠️  Remember to keep your API key secure!")
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")
        return False
    
    return True

def check_llm_dependencies():
    """Check if LLM dependencies are installed."""
    print("\n🔍 Checking LLM dependencies...")
    
    required_packages = ['openai', 'langchain']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is not installed")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Resume Evaluation System - LLM Setup")
    
    # Check dependencies first
    if not check_llm_dependencies():
        print("\n❌ Please install the required dependencies first.")
        exit(1)
    
    # Run setup
    setup_llm_features()
