#!/usr/bin/env python3
"""
GitHub Repository Setup Script for Resume Evaluation System
This script helps you prepare your repository for GitHub deployment with secure API key handling.
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header():
    """Print the setup header."""
    print("🚀 GitHub Repository Setup for Resume Evaluation System")
    print("=" * 60)
    print("This script will help you prepare your repository for GitHub deployment.")
    print()

def check_git_repo():
    """Check if this is a git repository."""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository detected")
            return True
        else:
            print("❌ Not a git repository")
            return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")
        return False

def initialize_git_repo():
    """Initialize a git repository if needed."""
    if not check_git_repo():
        print("\n🔧 Initializing Git repository...")
        try:
            subprocess.run(['git', 'init'], check=True)
            print("✅ Git repository initialized")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to initialize Git repository")
            return False
    return True

def create_gitignore():
    """Ensure .gitignore is properly configured."""
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        print("✅ .gitignore already exists")
    else:
        print("❌ .gitignore not found - this is required for security!")

def check_env_template():
    """Check if environment template exists."""
    env_template = Path('backend/env.template')
    if env_template.exists():
        print("✅ Environment template exists")
    else:
        print("❌ Environment template missing")

def show_github_setup_instructions():
    """Show instructions for GitHub setup."""
    print("\n📋 GitHub Repository Setup Instructions")
    print("=" * 50)
    
    print("\n1️⃣ Create GitHub Repository:")
    print("   - Go to https://github.com/new")
    print("   - Name your repository (e.g., 'resume-evaluation-system')")
    print("   - Make it public or private (your choice)")
    print("   - Don't initialize with README (we already have one)")
    
    print("\n2️⃣ Add Remote Origin:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git")
    
    print("\n3️⃣ Add and Commit Files:")
    print("   git add .")
    print("   git commit -m 'Initial commit: Resume Evaluation System with secure OpenAI integration'")
    
    print("\n4️⃣ Push to GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n5️⃣ Set up GitHub Secrets:")
    print("   - Go to your repository Settings")
    print("   - Navigate to 'Secrets and variables' → 'Actions'")
    print("   - Add these secrets:")
    print("     • OPENAI_API_KEY: your_actual_openai_api_key")
    print("     • DATABASE_URL: sqlite:///./resume_evaluation.db")
    print("     • PORT: 8000")
    
    print("\n6️⃣ Deploy to Cloud Platform:")
    print("   Choose one of these options:")
    print("   • Railway: https://railway.app (recommended)")
    print("   • Render: https://render.com")
    print("   • Heroku: https://heroku.com")
    print("   • Vercel: https://vercel.com")
    
    print("\n📚 For detailed deployment instructions, see:")
    print("   • GITHUB_DEPLOYMENT.md")
    print("   • backend/README.md")

def show_security_reminders():
    """Show important security reminders."""
    print("\n🔐 Security Reminders")
    print("=" * 30)
    print("✅ Never commit your actual .env file")
    print("✅ Use GitHub Secrets for API keys")
    print("✅ Keep your OpenAI API key private")
    print("✅ Review .gitignore before committing")
    print("✅ Test locally before deploying")

def main():
    """Main setup function."""
    print_header()
    
    # Check prerequisites
    if not initialize_git_repo():
        sys.exit(1)
    
    create_gitignore()
    check_env_template()
    
    # Show setup instructions
    show_github_setup_instructions()
    show_security_reminders()
    
    print("\n🎉 Setup Complete!")
    print("Your repository is ready for GitHub deployment with secure API key handling.")
    print("\nNext steps:")
    print("1. Create your GitHub repository")
    print("2. Add your OpenAI API key as a GitHub Secret")
    print("3. Deploy to your preferred cloud platform")
    print("4. Enjoy your secure Resume Evaluation System! 🚀")

if __name__ == "__main__":
    main()
