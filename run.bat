@echo off
echo ================================================
echo AI-Powered Learning Management System
echo ================================================
echo.
echo Activating virtual environment...
echo.
call venv\Scripts\activate.bat
echo.
echo Starting the application...
echo.
echo Make sure XAMPP MySQL is running!
echo.
python app.py
pause
