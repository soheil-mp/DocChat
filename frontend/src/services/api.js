import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add error interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    const errorMessage = error.response?.data?.detail || 'An unexpected error occurred';
    throw new Error(errorMessage);
  }
);

export const sendMessage = async ({ message, chat_history }) => {
  try {
    const response = await api.post('/api/chat', {
      message,
      chat_history,
    });
    
    if (!response.data || !response.data.message) {
      throw new Error('Invalid response format from server');
    }
    
    return response.data;
  } catch (error) {
    console.error('Send message error:', error);
    throw error;
  }
};

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const updateConfig = async (config) => {
  const response = await api.post('/api/config', config);
  return response.data;
};

export const getConfig = async () => {
  const response = await api.get('/api/config');
  return response.data;
}; 