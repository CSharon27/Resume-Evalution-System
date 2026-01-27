@echo off
REM HireLens Quick Setup - Step by Step Installation

echo ========================================
echo   HireLens - Quick Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [Step 1/6] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created!
    echo.
)

REM Activate virtual environment
echo [Step 2/6] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated!
echo.

REM Upgrade pip
echo [Step 3/6] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install basic packages first
echo [Step 4/6] Installing basic packages...
echo This may take 2-3 minutes...
pip install fastapi uvicorn pydantic python-multipart
echo ✓ Basic packages installed!
echo.

REM Install NLP packages (these are larger)
echo [Step 5/6] Installing NLP packages...
echo This may take 5-10 minutes (downloading ~500MB)...
echo Please be patient...
pip install spacy scikit-learn rapidfuzz
pip install sentence-transformers
echo ✓ NLP packages installed!
echo.

REM Install remaining packages
echo [Step 6/6] Installing remaining packages...
pip install PyPDF2 python-docx python-dotenv requests
echo ✓ All packages installed!
echo.

REM Download spaCy model
echo Downloading spaCy English model...
python -m spacy download en_core_web_sm
echo.

echo ========================================
echo   ✓ Installation Complete!
echo ========================================
echo.
echo You can now start the server with:
echo   venv\Scripts\activate
echo   uvicorn backend.main:app --reload
echo.
pause
