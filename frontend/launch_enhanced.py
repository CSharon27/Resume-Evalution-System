"""Enhanced launcher for the Resume Evaluation System."""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn', 
        'streamlit': 'streamlit',
        'sqlalchemy': 'sqlalchemy',
        'pymupdf': 'fitz',
        'python-docx': 'docx',
        'spacy': 'spacy',
        'langchain': 'langchain',
        'sentence-transformers': 'sentence_transformers',
        'scikit-learn': 'sklearn',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def download_spacy_model():
    """Download required spaCy model."""
    print("🔍 Checking spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model is available")
        return True
    except OSError:
        print("📥 Downloading spaCy model...")
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
            print("✅ spaCy model downloaded successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to download spaCy model")
            return False

def start_system():
    """Start the enhanced system."""
    print("🚀 Starting Enhanced Resume Evaluation System")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Download spaCy model
    if not download_spacy_model():
        return False
    
    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/uploads", exist_ok=True)
    
    print("\n🎉 System is ready!")
    print("=" * 60)
    print("📊 Dashboard: http://localhost:8501")
    print("🔌 API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n✨ Enhanced Features:")
    print("• Interactive UI with animations")
    print("• Real-time progress tracking")
    print("• Advanced filtering and search")
    print("• Export functionality")
    print("• Responsive design")
    print("\nPress Ctrl+C to stop the system")
    
    # Open browser
    try:
        webbrowser.open("http://localhost:8501")
    except:
        pass
    
    return True

if __name__ == "__main__":
    start_system()
