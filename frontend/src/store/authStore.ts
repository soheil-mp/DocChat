import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import axios from 'axios';

interface AuthState {
  isAuthenticated: boolean;
  user: any;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string, name: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      user: null,
      login: async (email, password) => {
        try {
          const response = await axios.post('/api/v1/auth/login', { email, password });
          set({ 
            isAuthenticated: true, 
            user: response.data.user 
          });
        } catch (error) {
          throw error;
        }
      },
      logout: () => {
        set({ isAuthenticated: false, user: null });
      },
      register: async (email, password, name) => {
        try {
          const response = await axios.post('/api/v1/auth/register', { 
            email, 
            password, 
            name 
          });
          set({ 
            isAuthenticated: true, 
            user: response.data.user 
          });
        } catch (error) {
          throw error;
        }
      }
    }),
    {
      name: 'auth-storage',
      getStorage: () => localStorage
    }
  )
); 