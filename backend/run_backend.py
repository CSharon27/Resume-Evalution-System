# backend/run_backend.py
"""
Launcher for local development of Resume Evaluation System backend.
This file is not used for Render deployment.
"""

import uvicorn
from app.config import DEBUG

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",      # path to FastAPI instance
        host="0.0.0.0",      # listen on all interfaces
        port=8000,           # local development port
        reload=DEBUG         # auto-reload for dev, disable in production
    )
