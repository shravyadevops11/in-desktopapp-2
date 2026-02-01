const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  getBackendUrl: () => ipcRenderer.sendSync('get-backend-url'),
  platform: process.platform,
  isDev: process.env.NODE_ENV === 'development'
});
