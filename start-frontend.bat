@echo off
REM HireLens - Start Frontend Server
REM This serves the frontend files over HTTP to avoid browser security restrictions

echo.
echo ===============================================
echo    HireLens - Starting Frontend Server
echo ===============================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python first.
    pause
    exit /b 1
)

echo Starting HTTP server on http://localhost:3000
echo.
echo IMPORTANT:
echo - Open browser and go to: http://localhost:3000
echo - Make sure backend is running on http://localhost:8000
echo - Press Ctrl+C to stop this server
echo.
echo ===============================================
echo.

REM Change to frontend directory
cd frontend

REM Start Python HTTP server
python -m http.server 3000

pause
