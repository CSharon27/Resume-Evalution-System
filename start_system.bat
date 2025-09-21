@echo off
echo Starting Resume Evaluation System...
echo =====================================
echo.
echo This will start both the backend API server and frontend dashboard.
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:8501
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul
echo.
echo Starting system...
python run_system.py
pause
