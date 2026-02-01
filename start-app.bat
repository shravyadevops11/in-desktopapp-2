@echo off
title In AI Assistant - Launcher
color 0B
echo.
echo ========================================
echo   In AI Assistant - Desktop App
echo ========================================
echo.
echo Starting application components...
echo.

REM Check if in correct directory
if not exist "backend" (
    echo ERROR: Please run from project root directory
    echo Current: %CD%
    pause
    exit /b 1
)

echo [1/2] Starting Backend Server...
start "In - Backend Server" cmd /k "cd backend && python -m uvicorn server:app --host localhost --port 8001"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting Desktop App...
start "In - Desktop App" cmd /k "cd electron && npm start"

echo.
echo ========================================
echo   App is starting...
echo ========================================
echo.
echo The desktop app window will open shortly.
echo.
echo To close the app:
echo 1. Close the desktop app window
echo 2. Close the backend server window
echo.
echo This window can be closed now.
echo.
pause
