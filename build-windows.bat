@echo off
echo ========================================
echo Building In AI Assistant for Windows
echo ========================================
echo.

echo [1/4] Installing Frontend Dependencies...
cd frontend
call yarn install
if errorlevel 1 goto error

echo.
echo [2/4] Building React Frontend...
call yarn build
if errorlevel 1 goto error

echo.
echo [3/4] Preparing Python Backend...
cd ..\backend
pip install -r requirements.txt
if errorlevel 1 goto error

pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
if errorlevel 1 goto error

pip install pyinstaller
if errorlevel 1 goto error

echo.
echo [3/4] Building Backend Executable...
pyinstaller --onefile --name server --hidden-import=emergentintegrations --hidden-import=motor --collect-all emergentintegrations server.py
if errorlevel 1 goto error

echo.
echo [4/4] Building Electron Desktop App...
cd ..\electron
call npm run build
if errorlevel 1 goto error

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your installer is ready at:
echo electron\dist\In AI Assistant Setup 1.0.0.exe
echo.
echo You can now:
echo 1. Install it on your Windows 11 machine
echo 2. Share it with others
echo 3. It includes everything needed to run
echo.
pause
goto end

:error
echo.
echo ========================================
echo BUILD FAILED!
echo ========================================
echo Please check the error messages above.
echo.
pause

:end
