import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ChatInterface from './features/chat/ChatInterface';
import Navbar from './components/Navbar';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Configure the query client with some defaults
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-[#1a1b1e]">
        <Navbar />
        <main className="container mx-auto px-4 py-6 max-w-7xl relative">
          <Routes>
            <Route path="/" element={<ChatInterface />} />
            <Route path="/chat" element={<ChatInterface />} />
          </Routes>
        </main>
      </div>
    </QueryClientProvider>
  );
};

export default App; 