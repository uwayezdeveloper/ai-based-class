@echo off
echo ================================================
echo AI-Powered Learning Management System
echo Installation Script
echo ================================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit
)
echo Python is installed!
echo.

echo Step 2: Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists!
)
echo.

echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 4: Installing Python dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit
)
echo.

echo Step 3: Creating upload directories...
if not exist "uploads\pdfs" mkdir uploads\pdfs
echo Directories created!
echo.

echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo NEXT STEPS:
echo 1. Start XAMPP and run MySQL service
echo 2. Run: python app.py
echo    OR double-click: run.bat
echo.
echo The database and default users will be created automatically on first run.
echo.
echo Default Login Credentials:
echo - Admin: admin@gmail.com / admin@gmail.com
echo - HOD: hod@gmail.com / hod@gmail.com
echo - Student: student@gmail.com / student@gmail.com
echo.
echo Access the system at: http://localhost:5000
echo.
pause
