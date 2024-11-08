import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ChatInterface from './features/chat/ChatInterface';
import Navbar from './components/Navbar';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 animate-gradient-shift">
      <div className="absolute inset-0 bg-[linear-gradient(90deg,#fff2_0%,#fff1_50%,#fff2_100%)] bg-[size:400%_100%] animate-gradient-shift" />
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