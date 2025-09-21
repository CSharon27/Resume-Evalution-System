"""Backend launcher for Resume Evaluation System."""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking backend dependencies...")
    
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn', 
        'sqlalchemy': 'sqlalchemy',
        'pymupdf': 'fitz',
        'python-docx': 'docx',
        'spacy': 'spacy',
        'langchain': 'langchain',
        'sentence-transformers': 'sentence_transformers',
        'scikit-learn': 'sklearn',
        'pandas': 'pandas',
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
    
    print("✅ All backend dependencies are installed")
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

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting Resume Evaluation System Backend")
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
    
    print("\n🎉 Backend is ready!")
    print("=" * 60)
    print("🔌 API Server: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Interactive API: http://localhost:8000/redoc")
    print("\n✨ Backend Features:")
    print("• FastAPI REST API")
    print("• Resume parsing and evaluation")
    print("• AI-powered semantic matching")
    print("• Database management")
    print("• File upload handling")
    print("\nPress Ctrl+C to stop the backend server")
    
    # Open browser to API docs
    try:
        webbrowser.open("http://localhost:8000/docs")
    except:
        pass
    
    # Start the FastAPI server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

if __name__ == "__main__":
    start_backend()
