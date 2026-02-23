@echo off
echo ========================================================
echo RAG Pro: Running Test Suite
echo ========================================================

cd ..

IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found.
    echo Please run scripts\setup_environment.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate
pytest tests/ -v

echo ========================================================
echo Test execution finished.
echo ========================================================
pause
