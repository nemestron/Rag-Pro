@echo off
echo ========================================================
echo RAG Pro: Launching Application
echo ========================================================

cd ..

IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found.
    echo Please run scripts\setup_environment.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate
echo Starting Streamlit server...
streamlit run app/main.py

pause
