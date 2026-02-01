# In AI Assistant - Electron Desktop App

## Quick Start Guide for Windows 11

### Option A: Build from Source (Recommended)

#### Prerequisites:
1. **Node.js 20.x LTS** - https://nodejs.org/
2. **Python 3.11+** - https://www.python.org/downloads/ (check "Add to PATH")
3. **Git** (optional) - https://git-scm.com/download/win

#### Build Steps:

1. **Download/Clone the Project**
   ```cmd
   # If using Git
   git clone https://github.com/YOUR_REPO/in-app.git
   cd in-app
   
   # Or extract the ZIP file you downloaded
   cd C:\path\to\in-app
   ```

2. **Run the Build Script**
   ```cmd
   # Simply double-click:
   build-windows.bat
   
   # Or run from command line:
   .\build-windows.bat
   ```

3. **Install the App**
   - After build completes, find: `electron\dist\In AI Assistant Setup 1.0.0.exe`
   - Double-click to install
   - Follow the installation wizard
   - App will be installed to `C:\Program Files\In AI Assistant`
   - Desktop shortcut will be created

4. **Run the App**
   - Double-click the desktop shortcut "In AI Assistant"
   - Or find it in Start Menu

---

### Option B: Development Mode (For Testing)

Run without building the .exe:

```cmd
# Terminal 1: Start Backend
cd backend
python -m uvicorn server:app --host localhost --port 8001

# Terminal 2: Start Frontend Dev Server
cd frontend
npm start

# Terminal 3: Start Electron
cd electron
npm start
```

---

## Features

✅ **Standalone Desktop App** - No browser needed
✅ **Stealth Mode** - Hidden from screen sharing
✅ **GPT-5.2 Integration** - Real AI interview assistance
✅ **Image Support** - Upload screenshots for help
✅ **Session History** - All conversations saved locally
✅ **Transparency Controls** - Adjust overlay visibility
✅ **Offline Database** - MongoDB embedded
✅ **Auto-Updates** - Stay up to date (can be configured)

---

## System Requirements

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 500MB free space
- **Internet:** Required for AI features (GPT-5.2)

---

## File Structure

```
in-app/
├── electron/              # Electron wrapper
│   ├── main.js            # Main process
│   ├── preload.js         # Preload script
│   ├── package.json       # Electron config
│   └── dist/              # Built installers
├── frontend/            # React app
│   ├── src/
│   ├── public/
│   └── build/             # Production build
├── backend/             # FastAPI server
│   ├── server.py
│   ├── models.py
│   └── dist/              # PyInstaller output
└── build-windows.bat    # Automated build script
```

---

## Troubleshooting

### Build Errors

**Python not found:**
```cmd
where python
# If nothing shows, reinstall Python with "Add to PATH" checked
```

**Node.js not found:**
```cmd
node --version
# If error, reinstall Node.js from nodejs.org
```

**PyInstaller issues:**
```cmd
pip install --upgrade pyinstaller
pip install --upgrade setuptools
```

### Runtime Errors

**App won't start:**
- Check Windows Defender isn't blocking it
- Run as Administrator
- Check `%APPDATA%\In AI Assistant\logs`

**Backend not connecting:**
- Check firewall settings
- Port 8001 might be in use
- Check backend logs

**AI responses not working:**
- Check internet connection
- Verify EMERGENT_LLM_KEY in backend/.env
- Check API quota

---

## Configuration

### Backend Configuration

Edit `backend/.env`:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=in_app
EMERGENT_LLM_KEY=sk-emergent-14f8cAd188e61AaA00
```

### Frontend Configuration

Edit `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## Distribution

### Sharing the App

The installer at `electron\dist\In AI Assistant Setup 1.0.0.exe` is:
- ✅ **Portable** - Everything bundled
- ✅ **Shareable** - Send to anyone
- ✅ **Installable** - Standard Windows installer
- ✅ **~250-400MB** - Includes all dependencies

### Code Signing (Optional)

For production distribution:
1. Get a code signing certificate
2. Update `electron/package.json` with certificate info
3. Rebuild

---

## Updates

### Manual Updates
1. Download new version
2. Run installer
3. Overwrites old version
4. Settings preserved

### Auto-Updates (Advanced)
Configure electron-builder auto-updater:
- Set up update server
- Add update check to main.js
- Users get notified of updates

---

## Uninstall

1. **Windows Settings** → Apps → "In AI Assistant" → Uninstall
2. Or use the uninstaller: `C:\Program Files\In AI Assistant\Uninstall.exe`

---

## Support

For issues:
1. Check logs: `%APPDATA%\In AI Assistant\logs`
2. Try reinstalling
3. Run in development mode to see detailed errors

---

## License

MIT License - Free to use and modify

---

**Enjoy your AI Interview Assistant!** 🚀
