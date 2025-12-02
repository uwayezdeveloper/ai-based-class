@echo off
echo ============================================
echo AI-Based LMS - Database Migration
echo ============================================
echo.
echo This will add missing columns to quiz_submissions table
echo.

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Running migration...
python migrate_quiz_submissions.py

echo.
echo Migration completed!
pause
