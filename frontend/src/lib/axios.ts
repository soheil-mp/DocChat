import axios from 'axios';
import type { AxiosError } from 'axios';

// Configure axios defaults
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add retry logic
axiosInstance.interceptors.response.use(
  response => response,
  async (error: AxiosError) => {
    const { config, response } = error;
    if (!config || !response) return Promise.reject(error);

    if (response.status === 429) {
      // Retry with exponential backoff
      const retryCount = (config as any).retryCount || 0;
      if (retryCount < 3) {
        const delay = Math.pow(2, retryCount) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        (config as any).retryCount = retryCount + 1;
        return axiosInstance(config);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance; 