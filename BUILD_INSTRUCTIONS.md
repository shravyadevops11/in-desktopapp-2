# Building In AI Assistant as Windows .exe

This guide will help you create a standalone Windows executable (.exe) for the In AI Assistant.

## Prerequisites

### On Windows 11:

1. **Install Node.js 20.x LTS**
   - Download from: https://nodejs.org/
   - This includes npm

2. **Install Python 3.11+**
   - Download from: https://www.python.org/downloads/
   - **Important:** Check "Add Python to PATH" during installation

3. **Install Git** (optional, for cloning)
   - Download from: https://git-scm.com/download/win

---

## Build Steps

### Step 1: Prepare the Project

```cmd
# Navigate to your project directory
cd C:\path\to\in-app

# Install frontend dependencies
cd frontend
npm install

# Build the React frontend for production
npm run build
```

### Step 2: Prepare Backend for Bundling

```cmd
# Navigate to backend
cd ..\backend

# Install dependencies
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Install PyInstaller for creating executable
pip install pyinstaller

# Create standalone backend executable
pyinstaller --onefile --name server server.py

# This creates backend/dist/server.exe
```

### Step 3: Set Up Electron

```cmd
# Navigate to electron directory
cd ..\electron

# Install Electron dependencies
npm install
```

### Step 4: Build the Desktop App

```cmd
# Still in electron directory
npm run build

# This creates the installer in electron/dist/
# Look for: In AI Assistant Setup 1.0.0.exe
```

### Step 5: Install and Run

1. Navigate to `electron/dist/`
2. Find `In AI Assistant Setup 1.0.0.exe`
3. **Double-click to install**
4. The installer will:
   - Install the app to Program Files
   - Create a desktop shortcut
   - Add to Start Menu

---

## Alternative: Quick Build Script

Create a file called `build-windows.bat` in the project root:

```batch
@echo off
echo Building In AI Assistant for Windows...

echo Step 1: Building React Frontend...
cd frontend
call npm install
call npm run build
if errorlevel 1 goto error

echo Step 2: Building Python Backend...
cd ..\backend
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --name server server.py
if errorlevel 1 goto error

echo Step 3: Building Electron App...
cd ..\electron
call npm install
call npm run build
if errorlevel 1 goto error

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Installer location: electron\dist\In AI Assistant Setup 1.0.0.exe
echo.
pause
goto end

:error
echo.
echo ========================================
echo BUILD FAILED!
echo ========================================
echo.
pause

:end
```

Then just **double-click `build-windows.bat`** to build everything automatically!

---

## Troubleshooting

### Backend Bundling Issues

If PyInstaller has issues with emergentintegrations:

```cmd
pyinstaller --onefile --name server --hidden-import=emergentintegrations server.py
```

### Missing DLLs

If the app crashes due to missing DLLs:

```cmd
pyinstaller --onefile --name server --collect-all emergentintegrations server.py
```

### Large File Size

The final .exe will be 200-400MB because it includes:
- Python runtime
- All Python packages
- Node.js/Electron runtime
- React build

This is normal for bundled desktop apps.

---

## Development Mode

To test the Electron app without building:

```cmd
# Terminal 1: Start backend
cd backend
python -m uvicorn server:app --host localhost --port 8001

# Terminal 2: Start frontend
cd frontend
npm start

# Terminal 3: Start Electron
cd electron
npm start
```

---

## Distribution

The final installer will be at:
```
electron/dist/In AI Assistant Setup 1.0.0.exe
```

This is a **portable installer** that:
- ✅ Includes everything (no separate installations needed)
- ✅ Works offline (except for GPT-5.2 API calls)
- ✅ Can be shared with others
- ✅ Installs like any Windows application
- ✅ Auto-updates can be configured

---

## File Size Optimization (Optional)

To reduce the installer size:

1. Use UPX compression:
```cmd
pip install pyinstaller[upx]
pyinstaller --onefile --name server --upx-dir C:\path\to\upx server.py
```

2. Exclude unnecessary packages from PyInstaller

3. Use electron-builder compression options

---

You now have a standalone Windows .exe installer for the In AI Assistant! 🚀
