@echo off
title Test Rigor Failure Reporter

echo ========================================
echo   Test Rigor Failure Reporter
echo ========================================
echo.
echo Starting the application...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Start Python app in the background
start /B python app.py

REM Wait for the server to start (5 seconds)
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Open Chrome browser with the application URL
echo Opening application in Chrome browser...
start chrome http://localhost:5000

echo.
echo ========================================
echo Application is running!
echo.
echo The app is running in the background.
echo Chrome browser should open automatically.
echo.
echo To stop the application, close this window
echo or press Ctrl+C
echo ========================================
echo.

REM Keep the window open so the app keeps running
pause
