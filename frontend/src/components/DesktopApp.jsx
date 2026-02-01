import React, { useState, useRef, useEffect } from 'react';
import { Send, Minimize2, X, Settings as SettingsIcon, History as HistoryIcon } from 'lucide-react';
import { mockChatHistory } from '../mockData';

const DesktopApp = ({ sessionId, opacity, onClose, onOpenSettings, onOpenHistory }) => {
  const [messages, setMessages] = useState(mockChatHistory['1'] || []);
  const [inputValue, setInputValue] = useState('');
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const newUserMessage = {
      id: `msg${Date.now()}`,
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages([...messages, newUserMessage]);
    setInputValue('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: `msg${Date.now()}`,
        type: 'assistant',
        content: 'This is a mock response. Backend integration will provide real AI responses from GPT-5.2.',
        timestamp: new Date().toISOString()
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  if (isMinimized) {
    return (
      <div
        style={{ opacity: opacity / 100 }}
        className="fixed bottom-6 right-6 z-50"
      >
        <button
          onClick={() => setIsMinimized(false)}
          className="w-16 h-16 bg-cyan-500 rounded-full shadow-lg shadow-cyan-500/50 flex items-center justify-center hover:scale-110 transition-transform"
        >
          <div className="w-3 h-3 bg-white rounded-full"></div>
        </button>
      </div>
    );
  }

  return (
    <div
      style={{ opacity: opacity / 100 }}
      className="fixed top-24 right-6 z-50 w-96 h-[600px] bg-gray-900 border border-cyan-500/30 rounded-xl shadow-2xl shadow-cyan-500/20 flex flex-col"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-800">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
          <span className="text-white font-semibold">AI Assistant</span>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={onOpenHistory}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-all"
          >
            <HistoryIcon className="w-4 h-4" />
          </button>
          <button
            onClick={onOpenSettings}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-all"
          >
            <SettingsIcon className="w-4 h-4" />
          </button>
          <button
            onClick={() => setIsMinimized(true)}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded transition-all"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-red-400 hover:bg-gray-800 rounded transition-all"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.type === 'user'
                  ? 'bg-cyan-500 text-white'
                  : 'bg-gray-800 text-gray-200'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              <span className="text-xs opacity-70 mt-1 block">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask anything..."
            className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 text-sm"
          />
          <button
            onClick={handleSendMessage}
            className="p-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600 transition-all"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default DesktopApp;
