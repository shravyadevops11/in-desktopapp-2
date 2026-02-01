import React, { useState, useRef, useEffect } from 'react';
import { Send, Minimize2, X, Settings as SettingsIcon, History as HistoryIcon, Image as ImageIcon, Mic, Loader2 } from 'lucide-react';
import { chatAPI, inputHistoryAPI } from '../services/api';
import { toast } from 'sonner';

const DesktopApp = ({ sessionId, opacity, onClose, onOpenSettings, onOpenHistory }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isMinimized, setIsMinimized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (sessionId) {
      loadMessages();
    }
  }, [sessionId]);

  const loadMessages = async () => {
    try {
      const msgs = await chatAPI.getMessages(sessionId);
      setMessages(msgs);
    } catch (error) {
      console.error('Error loading messages:', error);
      toast.error('Failed to load conversation history');
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
        toast.success('Image selected! Add your question and send.');
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() && !selectedImage) return;

    const messageText = inputValue.trim() || 'Please analyze this image';
    setIsLoading(true);

    try {
      // Save to input history
      await inputHistoryAPI.save(sessionId, messageText);

      // Create user message for display
      const newUserMessage = {
        id: `msg${Date.now()}`,
        type: 'user',
        content: messageText,
        timestamp: new Date().toISOString(),
        imageUrl: selectedImage
      };

      setMessages((prev) => [...prev, newUserMessage]);
      setInputValue('');
      
      // Send to API
      const aiResponse = await chatAPI.sendMessage(
        sessionId,
        messageText,
        'GPT-5.2',
        selectedImage ? 'image' : 'text',
        selectedImage,
        null
      );

      setMessages((prev) => [...prev, aiResponse]);
      setSelectedImage(null);
      toast.success('AI response received!');
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
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
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-10">
            <p className="text-sm">Start your interview preparation session</p>
            <p className="text-xs mt-2">Ask questions, share images, or practice answers</p>
          </div>
        )}
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
              {message.imageUrl && (
                <img 
                  src={message.imageUrl} 
                  alt="Uploaded" 
                  className="rounded mb-2 max-w-full h-auto"
                />
              )}
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              <span className="text-xs opacity-70 mt-1 block">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-gray-200 rounded-lg p-3">
              <Loader2 className="w-5 h-5 animate-spin" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-800">
        {selectedImage && (
          <div className="mb-2 relative inline-block">
            <img src={selectedImage} alt="Selected" className="h-16 rounded" />
            <button
              onClick={() => setSelectedImage(null)}
              className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs"
            >
              ×
            </button>
          </div>
        )}
        <div className="flex space-x-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleImageSelect}
            accept="image/*"
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="p-2 bg-gray-800 text-gray-400 hover:text-white rounded-lg transition-all"
            title="Upload image"
          >
            <ImageIcon className="w-5 h-5" />
          </button>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
            placeholder="Ask anything..."
            disabled={isLoading}
            className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 text-sm disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || (!inputValue.trim() && !selectedImage)}
            className="p-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DesktopApp;
