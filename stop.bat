@echo off
echo ============================================
echo AI-Based LMS - Stop Application
echo ============================================
echo.
echo Stopping Flask application...

:: Kill Python processes running app.py
taskkill /F /IM python.exe /FI "WINDOWTITLE eq app.py*" 2>nul
if %errorlevel% equ 0 (
    echo Application stopped successfully
) else (
    echo No running application found
)

echo.
pause
