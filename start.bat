@echo off
REM HireLens Startup Script

echo ========================================
echo   HireLens - Resume Evaluation System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo [3/4] Installing dependencies...
 

REM Download spaCy model
echo [4/4] Downloading NLP models...
python -m spacy download en_core_web_sm

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Starting HireLens backend...
echo API will be available at: http://localhost:8000
echo Frontend will be available at: frontend/index.html
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000
