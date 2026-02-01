import axios from 'axios';

// Use localhost for Electron app
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

console.log('Backend URL:', BACKEND_URL);
console.log('API URL:', API);

// Sessions API
export const sessionsAPI = {
  create: async (title, model = 'GPT-5.2') => {
    try {
      console.log('Creating session:', { title, model });
      const response = await axios.post(`${API}/sessions`, { title, model });
      console.log('Session created:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  },
  
  getAll: async () => {
    const response = await axios.get(`${API}/sessions`);
    return response.data;
  },
  
  getById: async (sessionId) => {
    const response = await axios.get(`${API}/sessions/${sessionId}`);
    return response.data;
  },
  
  delete: async (sessionId) => {
    const response = await axios.delete(`${API}/sessions/${sessionId}`);
    return response.data;
  },
  
  updateStats: async (sessionId, questionsAsked, duration) => {
    const response = await axios.patch(`${API}/sessions/${sessionId}/update-stats`, {
      questions_asked: questionsAsked,
      duration
    });
    return response.data;
  }
};

// Chat API
export const chatAPI = {
  sendMessage: async (sessionId, message, model = 'GPT-5.2', messageType = 'text', imageData = null, audioData = null) => {
    const response = await axios.post(`${API}/chat`, {
      sessionId,
      message,
      model,
      messageType,
      imageData,
      audioData
    });
    return response.data;
  },
  
  getMessages: async (sessionId) => {
    const response = await axios.get(`${API}/chat/${sessionId}`);
    return response.data;
  },
  
  deleteMessages: async (sessionId) => {
    const response = await axios.delete(`${API}/chat/${sessionId}`);
    return response.data;
  }
};

// Input History API
export const inputHistoryAPI = {
  save: async (sessionId, input) => {
    const response = await axios.post(`${API}/input-history`, {
      sessionId,
      input
    });
    return response.data;
  },
  
  getAll: async () => {
    const response = await axios.get(`${API}/input-history`);
    return response.data;
  },
  
  getBySession: async (sessionId) => {
    const response = await axios.get(`${API}/input-history/${sessionId}`);
    return response.data;
  }
};
