import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ChatInterface from './features/chat/ChatInterface';
import Navbar from './components/Navbar';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#1a1b1e]">
      <Navbar />
      <main className="container mx-auto px-4 py-6 max-w-7xl relative">
        <Routes>
          <Route path="/" element={<ChatInterface />} />
          <Route path="/chat" element={<ChatInterface />} />
        </Routes>
      </main>
    </div>
  );
};

export default App; 