@echo off
echo ================================================
echo AI-Powered Learning Management System
echo ================================================
echo.

REM Check if MySQL is running
echo Checking if MySQL is running...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL is running
) else (
    echo [WARNING] MySQL is not running!
    echo Please start XAMPP MySQL first.
    pause
    exit /b 1
)
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Starting the application...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
