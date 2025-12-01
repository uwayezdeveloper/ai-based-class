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

echo Step 5: Creating upload directories...
if not exist "uploads\pdfs" mkdir uploads\pdfs
echo Directories created!
echo.

echo Step 6: Checking if MySQL is running...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo MySQL is running - proceeding with database setup...
    echo.
    
    echo Step 7: Initializing database...
    python config\database.py
    echo.
    
    echo Step 8: Updating database schema...
    python update_database.py
    echo.
    
    echo Step 9: Verifying installation...
    python verify_installation.py
    echo.
) else (
    echo WARNING: MySQL is not running!
    echo Please start XAMPP MySQL, then run: python config\database.py
    echo.
)

echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Default Login Credentials:
echo - Admin: admin@example.com / admin123
echo - HOD: hod@example.com / hod123
echo - Students: Register through the registration page
echo.
echo To start the application:
echo   Double-click: start.bat
echo   OR run: python app.py
echo.
echo Access the system at: http://localhost:5000
echo.
pause
