import React, { useState } from 'react';
import { X, Sliders } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Slider } from './ui/slider';

const SettingsModal = ({ isOpen, onClose, opacity, setOpacity }) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="bg-gray-900 border border-cyan-500/30 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center space-x-2 text-white">
            <Sliders className="w-5 h-5 text-cyan-400" />
            <span>Settings</span>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Transparency Control */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-300">Transparency</label>
              <span className="text-sm text-cyan-400 font-semibold">{opacity}%</span>
            </div>
            <Slider
              value={[opacity]}
              onValueChange={(value) => setOpacity(value[0])}
              min={20}
              max={100}
              step={5}
              className="w-full"
            />
            <p className="text-xs text-gray-500">
              Adjust the opacity of the AI assistant overlay for perfect visibility.
            </p>
          </div>

          {/* Model Selection */}
          <div className="space-y-3">
            <label className="text-sm font-medium text-gray-300">AI Model</label>
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-white">GPT-5.2</span>
                <span className="text-xs text-cyan-400 bg-cyan-500/10 px-2 py-1 rounded">Active</span>
              </div>
            </div>
          </div>

          {/* Stealth Mode Info */}
          <div className="bg-cyan-500/10 border border-cyan-500/30 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-cyan-400 mb-2">Stealth Mode Features</h4>
            <ul className="space-y-1 text-xs text-gray-400">
              <li>• Hidden from taskbar and task manager</li>
              <li>• Invisible during screen sharing</li>
              <li>• No system notifications</li>
              <li>• Click-through overlay mode</li>
            </ul>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default SettingsModal;
