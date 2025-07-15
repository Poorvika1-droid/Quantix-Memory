@echo off
echo.
echo ========================================
echo    Quantix Memory AI - Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; print('Python version:', sys.version.split()[0])"

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting Quantix Memory AI...
echo.
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

python app.py

pause 