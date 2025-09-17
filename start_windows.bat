@echo off
REM IntelliFusion AI Document Assistant - Windows Startup Script
REM Bosch AI Hackathon 2025

echo ========================================
echo  IntelliFusion AI Document Assistant
echo  Bosch AI Hackathon 2025
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Copying .env.example to .env...
    copy ".env.example" ".env" >nul
    echo ✅ Created .env file
    echo Please edit .env with your Bosch credentials before running the app
    pause
)

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt --quiet

REM Launch the application
echo 🚀 Starting IntelliFusion...
echo.
echo The application will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

python run.py

pause
