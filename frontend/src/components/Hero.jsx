import React from 'react';
import { ArrowRight, Lock, Eye, Mic, Monitor } from 'lucide-react';

const Hero = ({ onStartSession }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-900 to-gray-800 pt-24">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center space-y-6">
          <div className="inline-block px-4 py-2 bg-cyan-500/10 border border-cyan-500/30 rounded-full">
            <span className="text-cyan-400 text-sm font-medium flex items-center space-x-2">
              <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
              <span>Trusted by 10,000+ Professionals</span>
            </span>
          </div>

          <h1 className="text-6xl md:text-7xl font-bold text-white leading-tight">
            Fully Hidden & Undetectable
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
              AI Interview Assistant
            </span>
          </h1>

          <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Take control of your interviews with the only desktop app designed to deliver
            private, real-time AI support—without anyone knowing it's there.
          </p>

          <div className="flex items-center justify-center space-x-4 pt-8">
            <button
              onClick={onStartSession}
              className="group flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-cyan-500 to-cyan-400 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-cyan-500/50 transition-all"
            >
              <span>Start New Session</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          <div className="group bg-gray-800/50 backdrop-blur border border-gray-700 rounded-xl p-6 hover:border-cyan-500/50 transition-all">
            <div className="w-12 h-12 bg-cyan-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-cyan-500/20 transition-all">
              <Lock className="w-6 h-6 text-cyan-400" />
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Stealth Mode</h3>
            <p className="text-gray-400 text-sm">
              Complete privacy during screen sharing with invisible AI assistance.
            </p>
          </div>

          <div className="group bg-gray-800/50 backdrop-blur border border-gray-700 rounded-xl p-6 hover:border-cyan-500/50 transition-all">
            <div className="w-12 h-12 bg-cyan-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-cyan-500/20 transition-all">
              <Eye className="w-6 h-6 text-cyan-400" />
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Transparency Controls</h3>
            <p className="text-gray-400 text-sm">
              Customize app opacity for the perfect balance of visibility and discretion.
            </p>
          </div>

          <div className="group bg-gray-800/50 backdrop-blur border border-gray-700 rounded-xl p-6 hover:border-cyan-500/50 transition-all">
            <div className="w-12 h-12 bg-cyan-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-cyan-500/20 transition-all">
              <Monitor className="w-6 h-6 text-cyan-400" />
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">Smart Area Selection</h3>
            <p className="text-gray-400 text-sm">
              Precision drag tool to analyze any region of your screen instantly.
            </p>
          </div>

          <div className="group bg-gray-800/50 backdrop-blur border border-gray-700 rounded-xl p-6 hover:border-cyan-500/50 transition-all">
            <div className="w-12 h-12 bg-cyan-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-cyan-500/20 transition-all">
              <Mic className="w-6 h-6 text-cyan-400" />
            </div>
            <h3 className="text-white font-semibold text-lg mb-2">System Audio Capture</h3>
            <p className="text-gray-400 text-sm">
              Record and analyze system audio with crystal-clear quality.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
