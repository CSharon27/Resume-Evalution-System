"""Main launcher for Resume Evaluation System - starts both frontend and backend."""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking system dependencies...")
    
    # Check if both frontend and backend folders exist
    if not os.path.exists("backend"):
        print("❌ Backend folder not found")
        return False
    
    if not os.path.exists("frontend"):
        print("❌ Frontend folder not found")
        return False
    
    print("✅ Project structure is correct")
    return True

def start_backend():
    """Start the backend server in a separate thread."""
    print("🚀 Starting backend server...")
    try:
        subprocess.run([
            sys.executable, "run_backend.py"
        ], cwd="backend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Backend stopped")

def start_frontend():
    """Start the frontend server in a separate thread."""
    print("🚀 Starting frontend server...")
    try:
        subprocess.run([
            sys.executable, "run_frontend.py"
        ], cwd="frontend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Frontend stopped")

def main():
    """Main function to start the complete system."""
    print("🚀 Starting Resume Evaluation System")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    print("\n🎉 System is ready!")
    print("=" * 60)
    print("📊 Frontend Dashboard: http://localhost:8501")
    print("🔌 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n✨ System Features:")
    print("• AI-powered resume evaluation")
    print("• Interactive web dashboard")
    print("• RESTful API backend")
    print("• Real-time processing")
    print("• Advanced analytics")
    print("\nPress Ctrl+C to stop the entire system")
    
    # Open browser to dashboard
    try:
        webbrowser.open("http://localhost:8501")
    except:
        pass
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start frontend in the main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 System stopped")
        return True

if __name__ == "__main__":
    main()
