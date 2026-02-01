# Quick Fix Guide for Build Errors

## Problem: Dependency Conflicts

The error you're seeing is caused by conflicting package versions in the Python dependencies.

---

## **Solution 1: Use Fixed Build Script (Recommended)**

I've updated the build script. Try again:

```powershell
# Make sure you're in the project root (in-desktopapp-2)
cd C:\Users\Sagar Pawadi N\Documents\WS\in-desktopapp-2

# Run the updated build script
.\build-windows.bat
```

The new script:
- ✅ Upgrades pip first
- ✅ Installs packages in correct order
- ✅ Handles conflicts automatically
- ✅ Skips problematic packages gracefully

---

## **Solution 2: Manual Build (If Script Still Fails)**

### Step A: Build Frontend

```powershell
cd frontend
yarn install
yarn build
```

### Step B: Install Backend Dependencies (Minimal)

```powershell
cd ..\backend

# Upgrade pip first
python -m pip install --upgrade pip

# Install only essential packages
pip install fastapi==0.110.1
pip install uvicorn==0.25.0
pip install python-dotenv
pip install pydantic
pip install motor==3.3.1
pip install pymongo==4.5.0
pip install aiohttp
pip install Pillow

# Install emergentintegrations
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Install PyInstaller
pip install pyinstaller
```

### Step C: Build Backend Executable

```powershell
# Still in backend directory
pyinstaller --onefile --name server server.py
```

### Step D: Build Electron App

```powershell
cd ..\electron
npm install
npm run build
```

---

## **Solution 3: Skip PyInstaller (Easiest for Testing)**

If PyInstaller keeps failing, you can run the app **without building .exe**:

### Create `start-app.bat` in project root:

```batch
@echo off
echo Starting In AI Assistant...
echo.

start "Backend" cmd /k "cd backend && python -m uvicorn server:app --host localhost --port 8001"
timeout /t 3

start "Frontend" cmd /k "cd electron && npm start"

echo.
echo App is starting...
echo Close all windows to quit.
echo.
```

Then just **double-click `start-app.bat`** to run the app!

---

## **Solution 4: Use Virtual Environment (Clean Install)**

```powershell
# In backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install packages
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv pydantic motor pymongo
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
pip install pyinstaller

# Build
pyinstaller --onefile --name server server.py

# Deactivate when done
deactivate
```

---

## **Common Errors & Fixes**

### Error: "grpcio-status conflict"

**Fix:**
```powershell
pip install --upgrade google-api-core
pip install grpcio-status==1.62.0
```

### Error: "requirements.txt not found"

**Fix:**
```powershell
# Make sure you're in backend directory
cd backend
dir  # Should show requirements.txt
```

### Error: "Python not found"

**Fix:**
1. Press `Win + R`
2. Type `sysdm.cpl` and press Enter
3. Advanced → Environment Variables
4. Add Python to PATH
5. Restart terminal

### Error: "npm not found"

**Fix:**
- Reinstall Node.js from https://nodejs.org/
- Restart terminal

---

## **Simplified Approach (No .exe Build)**

If you just want to **run the app locally** without creating installer:

### 1. Start Backend:
```powershell
cd backend
python -m uvicorn server:app --host localhost --port 8001
```

### 2. Start Frontend (New Terminal):
```powershell
cd frontend
npm start
```

### 3. Start Electron (New Terminal):
```powershell
cd electron
npm start
```

The app will open as a desktop window!

---

## **Quick Checklist**

Before building, verify:

```powershell
# Check Python
python --version
# Should show: Python 3.11.x or higher

# Check pip
pip --version

# Check Node.js
node --version
# Should show: v20.x.x or higher

# Check npm
npm --version

# Check yarn
yarn --version

# Check project structure
dir
# Should show: backend, frontend, electron folders
```

---

## **Still Having Issues?**

### Option 1: Skip Building, Use Web Version
Just run the backend and frontend without Electron:
```powershell
# Terminal 1
cd backend && python -m uvicorn server:app --reload

# Terminal 2
cd frontend && npm start
```

Access at: http://localhost:3000

### Option 2: Contact Me
Provide:
1. Full error message
2. Python version: `python --version`
3. Node version: `node --version`
4. Current directory: `pwd`
5. Output of: `pip list`

---

## **Recommended Next Steps**

1. **Try Solution 1** (updated build script) first
2. If fails, try **Solution 2** (manual build)
3. If still fails, use **Solution 3** (start-app.bat)
4. For testing only, use **simplified approach**

Let me know which solution works for you!
