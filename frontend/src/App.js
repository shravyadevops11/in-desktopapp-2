import React, { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import DesktopApp from './components/DesktopApp';
import SettingsModal from './components/SettingsModal';
import HistoryModal from './components/HistoryModal';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';
import { sessionsAPI } from './services/api';

function App() {
  const [showDesktopApp, setShowDesktopApp] = useState(false);
  const [stealthMode, setStealthMode] = useState(false);
  const [opacity, setOpacity] = useState(95);
  const [showSettings, setShowSettings] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState(null);

  const handleStartSession = async () => {
    try {
      console.log('Starting new session...');
      const session = await sessionsAPI.create('New Interview Session', 'GPT-5.2');
      console.log('Session created successfully:', session);
      setCurrentSessionId(session.id);
      setShowDesktopApp(true);
      toast.success('Session started! AI Assistant is now active.');
    } catch (error) {
      console.error('Error creating session:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to connect to backend';
      toast.error(`Failed to start session: ${errorMessage}`);
    }
  };

  const handleCloseDesktopApp = () => {
    setShowDesktopApp(false);
    toast.info('Session ended. All conversations saved to history.');
  };

  const handleToggleStealth = () => {
    setStealthMode(!stealthMode);
    if (!stealthMode) {
      toast.success('Stealth Mode activated! App is now hidden from screen capture.');
    } else {
      toast.info('Stealth Mode deactivated.');
    }
  };

  const handleLoadSession = (sessionId) => {
    setCurrentSessionId(sessionId);
    setShowDesktopApp(true);
    toast.success('Session loaded successfully!');
  };

  return (
    <div className="App">
      <Toaster position="top-right" theme="dark" />
      
      <Navbar
        onOpenSettings={() => setShowSettings(true)}
        onOpenHistory={() => setShowHistory(true)}
        stealthMode={stealthMode}
        onToggleStealth={handleToggleStealth}
      />

      <Hero onStartSession={handleStartSession} />

      {showDesktopApp && (
        <DesktopApp
          sessionId={currentSessionId}
          opacity={opacity}
          onClose={handleCloseDesktopApp}
          onOpenSettings={() => setShowSettings(true)}
          onOpenHistory={() => setShowHistory(true)}
        />
      )}

      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        opacity={opacity}
        setOpacity={setOpacity}
      />

      <HistoryModal
        isOpen={showHistory}
        onClose={() => setShowHistory(false)}
        onLoadSession={handleLoadSession}
      />
    </div>
  );
}

export default App;
