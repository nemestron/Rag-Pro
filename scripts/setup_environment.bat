@echo off
echo ========================================================
echo RAG Pro: Environment Setup
echo ========================================================

echo [1/3] Checking for Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not added to PATH.
    echo Please install Python 3.10 or 3.11 and try again.
    pause
    exit /b 1
)

echo [2/3] Creating virtual environment (.venv)...
cd ..
python -m venv .venv

echo [3/3] Activating virtual environment and installing dependencies...
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo ========================================================
echo Setup Complete! 
echo You can now run the application using scripts\run_app.bat
echo ========================================================
pause
