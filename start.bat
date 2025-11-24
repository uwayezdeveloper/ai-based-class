@echo off
echo ================================================
echo AI-LMS - Complete Setup and Run
echo ================================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Running setup first...
    echo.
    call setup.bat
    echo.
    echo Setup complete! Now starting the application...
    echo.
)

REM Activate venv and run
call venv\Scripts\activate.bat
echo.
echo Starting AI-Powered Learning Management System...
echo.
echo Make sure XAMPP MySQL is running!
echo.
python app.py
pause
