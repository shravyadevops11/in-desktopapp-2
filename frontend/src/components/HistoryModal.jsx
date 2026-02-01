import React, { useState, useEffect } from 'react';
import { X, Clock, MessageSquare, Loader2 } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { ScrollArea } from './ui/scroll-area';
import { sessionsAPI } from '../services/api';
import { toast } from 'sonner';

const HistoryModal = ({ isOpen, onClose, onLoadSession }) => {
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadSessions();
    }
  }, [isOpen]);

  const loadSessions = async () => {
    setIsLoading(true);
    try {
      const data = await sessionsAPI.getAll();
      setSessions(data);
    } catch (error) {
      console.error('Error loading sessions:', error);
      toast.error('Failed to load session history');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="bg-gray-900 border border-cyan-500/30 text-white max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center space-x-2 text-white">
            <Clock className="w-5 h-5 text-cyan-400" />
            <span>Session History</span>
          </DialogTitle>
        </DialogHeader>

        <ScrollArea className="h-[500px] pr-4">
          {isLoading ? (
            <div className="flex items-center justify-center h-40">
              <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
            </div>
          ) : sessions.length === 0 ? (
            <div className="text-center text-gray-500 py-10">
              <p>No sessions yet</p>
              <p className="text-sm mt-2">Start your first interview preparation session!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  className="bg-gray-800 border border-gray-700 rounded-lg p-4 hover:border-cyan-500/50 transition-all cursor-pointer group"
                  onClick={() => {
                    onLoadSession(session.id);
                    onClose();
                  }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="text-white font-semibold group-hover:text-cyan-400 transition-colors">
                      {session.title}
                    </h4>
                    <span className="text-xs text-cyan-400 bg-cyan-500/10 px-2 py-1 rounded">
                      {session.model}
                    </span>
                  </div>

                  <div className="flex items-center space-x-4 text-xs text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{formatDate(session.date)}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <MessageSquare className="w-3 h-3" />
                      <span>{session.questionsAsked} questions</span>
                    </div>
                    <span>•</span>
                    <span>{session.duration}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        <div className="pt-4 border-t border-gray-800">
          <p className="text-xs text-gray-500 text-center">
            All sessions are encrypted and stored securely
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default HistoryModal;
