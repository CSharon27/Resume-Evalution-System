"""Frontend launcher for Resume Evaluation System."""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking frontend dependencies...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'requests': 'requests',
        'pandas': 'pandas',
        'plotly': 'plotly'
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
    
    print("✅ All frontend dependencies are installed")
    return True

def check_backend_connection():
    """Check if backend is running."""
    print("🔍 Checking backend connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            return True
        else:
            print("⚠️ Backend responded with status code:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start the backend first.")
        print("   Run: python run_backend.py from the backend folder")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend dashboard."""
    print("🚀 Starting Resume Evaluation System Frontend")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check backend connection
    if not check_backend_connection():
        print("\n⚠️ Warning: Backend is not running!")
        print("   The frontend will start but may not work properly.")
        print("   Please start the backend server first.")
        
        user_input = input("\nDo you want to continue anyway? (y/n): ")
        if user_input.lower() != 'y':
            print("❌ Frontend startup cancelled")
            return False
    
    print("\n🎉 Frontend is ready!")
    print("=" * 60)
    print("📊 Dashboard: http://localhost:8501")
    print("🔌 Backend API: http://localhost:8000")
    print("\n✨ Frontend Features:")
    print("• Interactive Streamlit dashboard")
    print("• Resume upload and management")
    print("• Job description upload")
    print("• Real-time evaluation results")
    print("• Advanced analytics and reporting")
    print("• Professional UI with animations")
    print("\nPress Ctrl+C to stop the frontend server")
    
    # Open browser to dashboard
    try:
        webbrowser.open("http://localhost:8501")
    except:
        pass
    
    # Start the Streamlit server
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

if __name__ == "__main__":
    start_frontend()
