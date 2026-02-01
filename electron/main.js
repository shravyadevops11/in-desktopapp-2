const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = require('electron-is-dev');

let mainWindow;
let backendProcess;

// Backend server configuration
const BACKEND_PORT = 8001;
const BACKEND_HOST = 'localhost';

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    icon: path.join(__dirname, 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    frame: true,
    backgroundColor: '#0f1115',
    title: 'In - AI Interview Assistant'
  });

  // Remove menu bar
  mainWindow.setMenuBarVisibility(false);

  // Load the app
  const startUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '../frontend/build/index.html')}`;

  mainWindow.loadURL(startUrl);
  
  // Handle loading errors
  mainWindow.webContents.on('did-fail-load', () => {
    console.log('Failed to load, trying built version...');
    mainWindow.loadFile(path.join(__dirname, '../frontend/build/index.html'));
  });

  // Open DevTools in development
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startBackend() {
  console.log('Checking backend server...');

  // Check if backend is already running
  const http = require('http');
  const options = {
    hostname: BACKEND_HOST,
    port: BACKEND_PORT,
    path: '/api/',
    method: 'GET',
    timeout: 1000
  };

  const req = http.request(options, (res) => {
    console.log('Backend already running on port', BACKEND_PORT);
  });

  req.on('error', (err) => {
    // Backend not running, start it
    console.log('Starting backend server...');

    const backendPath = isDev
      ? path.join(__dirname, '..', 'backend')
      : path.join(process.resourcesPath, 'backend');

    const pythonExecutable = isDev
      ? 'python'
      : path.join(process.resourcesPath, 'backend', 'server.exe');

    if (isDev) {
      // Development mode - run Python script
      backendProcess = spawn(pythonExecutable, [
        '-m',
        'uvicorn',
        'server:app',
        '--host',
        BACKEND_HOST,
        '--port',
        BACKEND_PORT.toString()
      ], {
        cwd: backendPath,
        stdio: 'inherit'
      });

      backendProcess.on('error', (err) => {
        console.error('Failed to start backend:', err);
      });

      backendProcess.on('close', (code) => {
        console.log(`Backend process exited with code ${code}`);
      });
    }
  });

  req.end();
}

function stopBackend() {
  if (backendProcess) {
    console.log('Stopping backend server...');
    backendProcess.kill();
    backendProcess = null;
  }
}

// App lifecycle
app.whenReady().then(() => {
  // Start backend first
  startBackend();

  // Wait a bit for backend to start, then create window
  setTimeout(() => {
    createWindow();
  }, 2000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  stopBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  stopBackend();
});

// IPC handlers
ipcMain.on('get-backend-url', (event) => {
  event.returnValue = `http://${BACKEND_HOST}:${BACKEND_PORT}`;
});
