import React from 'react';
import { Lock, Settings, History, Eye } from 'lucide-react';

const Navbar = ({ onOpenSettings, onOpenHistory, stealthMode, onToggleStealth }) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-cyan-500/20">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-cyan-400 rounded-full shadow-lg shadow-cyan-400/50"></div>
            <span className="text-2xl font-bold text-white">In</span>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center space-x-6">
            <button
              onClick={onToggleStealth}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                stealthMode
                  ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/50'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              <Eye className="w-4 h-4" />
              <span className="text-sm font-medium">
                {stealthMode ? 'Stealth Mode: ON' : 'Stealth Mode: OFF'}
              </span>
            </button>

            <button
              onClick={onOpenHistory}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-all"
            >
              <History className="w-4 h-4" />
              <span className="text-sm font-medium">History</span>
            </button>

            <button
              onClick={onOpenSettings}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-all"
            >
              <Settings className="w-4 h-4" />
              <span className="text-sm font-medium">Settings</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
