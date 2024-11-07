import React from 'react';
import ChatInterface from './components/Chat/ChatInterface';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-4xl mx-auto py-4 px-6">
          <h1 className="text-2xl font-bold text-gray-900">DocuChat</h1>
        </div>
      </header>
      <main>
        <ChatInterface />
      </main>
    </div>
  );
}

export default App; 