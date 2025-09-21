"""Script to run the Resume Evaluation System."""

import subprocess
import sys
import os
import time
import threading
import requests
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    # Mapping of package names to actual import names
    package_imports = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'streamlit': 'streamlit',
        'sqlalchemy': 'sqlalchemy',
        'pymupdf': 'fitz',          # PyMuPDF is imported as fitz
        'python-docx': 'docx',      # python-docx is imported as docx
        'spacy': 'spacy',
        'langchain': 'langchain',
        'sentence-transformers': 'sentence_transformers',
        'scikit-learn': 'sklearn',  # scikit-learn is imported as sklearn
        'pandas': 'pandas',
        'plotly': 'plotly',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
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

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = [
        "data",
        "data/uploads",
        "app",
        "app/models",
        "app/parsers",
        "app/evaluators",
        "app/services",
        "app/frontend"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created")

def start_api_server():
    """Start the FastAPI server."""
    print("🚀 Starting API server...")
    
    try:
        # Change to the project directory
        os.chdir(Path(__file__).parent)
        
        # Start the server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
        # Wait for server to start
        time.sleep(5)
        
        # Check if server is running
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ API server is running on http://localhost:8000")
                return process
            else:
                print("❌ API server failed to start")
                return None
        except requests.exceptions.RequestException:
            print("❌ API server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def start_dashboard():
    """Start the Streamlit dashboard."""
    print("🚀 Starting dashboard...")
    
    try:
        # Change to the project directory
        os.chdir(Path(__file__).parent)
        
        # Start the dashboard
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "app/frontend/dashboard.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        
        # Wait for dashboard to start
        time.sleep(3)
        
        print("✅ Dashboard is running on http://localhost:8501")
        return process
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return None

def main():
    """Main function to run the system."""
    print("🚀 Resume Evaluation System Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies first")
        return
    
    # Download spaCy model
    if not download_spacy_model():
        print("❌ Please install spaCy model first")
        return
    
    # Create directories
    create_directories()
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server")
        return
    
    # Start dashboard
    dashboard_process = start_dashboard()
    if not dashboard_process:
        print("❌ Failed to start dashboard")
        api_process.terminate()
        return
    
    print("\n🎉 System is running!")
    print("=" * 50)
    print("📊 Dashboard: http://localhost:8501")
    print("🔌 API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the system")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        
        # Terminate processes
        if api_process:
            api_process.terminate()
        if dashboard_process:
            dashboard_process.terminate()
        
        print("✅ System stopped")

if __name__ == "__main__":
    main()
