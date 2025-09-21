"""Test script to verify configuration and environment variable handling."""

import os
from app.config import settings

def test_configuration():
    """Test the configuration setup."""
    print("🔧 Testing Resume Evaluation System Configuration")
    print("=" * 60)
    
    print(f"✅ LLM Enabled: {settings.enable_llm}")
    print(f"✅ OpenAI API Key Set: {'Yes' if settings.openai_api_key else 'No'}")
    print(f"✅ Database URL: {settings.database_url}")
    print(f"✅ Host: {settings.host}")
    print(f"✅ Port: {settings.port}")
    print(f"✅ Debug Mode: {settings.debug}")
    
    print("\n🔍 Environment Variables:")
    print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}")
    print(f"DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not Set'}")
    print(f"PORT: {os.getenv('PORT', 'Not Set')}")
    
    print("\n📋 Configuration Status:")
    if settings.openai_api_key:
        print("🟢 OpenAI API key is configured - LLM features will work")
    else:
        print("🟡 OpenAI API key not set - LLM features will use mock responses")
        print("   To enable LLM features:")
        print("   1. Set OPENAI_API_KEY environment variable")
        print("   2. Or create a .env file with your API key")
        print("   3. Or use GitHub Secrets for deployment")
    
    print("\n🚀 System Ready for:")
    if settings.openai_api_key:
        print("   ✅ Full AI-powered resume evaluation")
        print("   ✅ OpenAI GPT integration")
        print("   ✅ Advanced semantic analysis")
    else:
        print("   ✅ Basic resume evaluation")
        print("   ✅ Rule-based matching")
        print("   ✅ Mock AI responses")
    
    return True

if __name__ == "__main__":
    test_configuration()
