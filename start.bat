@echo off
echo ================================================
echo AI-LMS - Quick Start
echo ================================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo [FIRST TIME SETUP]
    echo Virtual environment not found!
    echo Running setup.bat first...
    echo.
    call setup.bat
    if %ERRORLEVEL% neq 0 (
        echo Setup failed! Please check the errors above.
        pause
        exit /b 1
    )
    echo.
)

REM Check if MySQL is running
echo Checking MySQL status...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL is running
) else (
    echo [ERROR] MySQL is not running!
    echo.
    echo Please start XAMPP MySQL:
    echo 1. Open XAMPP Control Panel
    echo 2. Click "Start" next to MySQL
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)
echo.

REM Activate venv and run
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo ================================================
echo Starting AI-Powered Learning Management System
echo ================================================
echo.
echo Access the system at: http://localhost:5000
echo.
echo Default Login:
echo   Admin: admin@example.com / admin123
echo   HOD: hod@example.com / hod123
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
