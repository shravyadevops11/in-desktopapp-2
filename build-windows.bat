@echo off
echo ========================================
echo Building In AI Assistant for Windows
echo ========================================
echo.

REM Check if running from project root
if not exist "frontend" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [1/5] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Could not upgrade pip, continuing...
)

echo.
echo [2/5] Installing Frontend Dependencies...
cd frontend
call yarn install
if errorlevel 1 goto error

echo.
echo [3/5] Building React Frontend...
call yarn build
if errorlevel 1 goto error

echo.
echo [4/5] Installing Backend Dependencies...
cd ..\backend

REM First install base packages
pip install --no-cache-dir fastapi==0.110.1 uvicorn==0.25.0 python-dotenv pydantic motor pymongo
if errorlevel 1 goto error

REM Install other requirements
pip install --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages failed, trying alternative approach...
    pip install --no-cache-dir fastapi uvicorn python-dotenv pydantic motor pymongo aiohttp Pillow
)

REM Install emergentintegrations separately
echo.
echo Installing emergentintegrations...
pip install --no-cache-dir emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
if errorlevel 1 (
    echo WARNING: emergentintegrations installation had issues, but continuing...
)

REM Install PyInstaller
echo.
echo Installing PyInstaller...
pip install --no-cache-dir pyinstaller
if errorlevel 1 goto error

echo.
echo [5/5] Building Backend Executable...
pyinstaller --onefile --name server --hidden-import=emergentintegrations --hidden-import=motor --hidden-import=pymongo --collect-all emergentintegrations server.py
if errorlevel 1 goto error

echo.
echo [6/6] Building Electron Desktop App...
cd ..\electron
call npm install
if errorlevel 1 goto error

call npm run build
if errorlevel 1 goto error

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your installer is ready at:
echo %CD%\dist\In AI Assistant Setup 1.0.0.exe
echo.
echo Installer size: ~300-400MB (includes everything)
echo.
echo You can now:
echo 1. Install it on your Windows 11 machine
echo 2. Share it with others
echo 3. It works offline (except AI features)
echo.
pause
goto end

:error
echo.
echo ========================================
echo BUILD FAILED!
echo ========================================
echo.
echo Common issues:
echo 1. Python not in PATH - Reinstall Python with "Add to PATH"
echo 2. Node.js not installed - Download from nodejs.org
echo 3. Not in project root - cd to in-app folder first
echo.
echo Current directory: %CD%
echo.
pause
exit /b 1

:end
