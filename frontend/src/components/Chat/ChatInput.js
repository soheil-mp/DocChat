import React, { useState } from 'react';

function ChatInput({ onSend, isLoading, placeholder }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex space-x-2">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={placeholder || "Type your message..."}
        className="flex-1 rounded-lg border p-2 focus:outline-none focus:border-blue-500"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !message.trim()}
        className={`
          px-4 py-2 rounded-lg text-white transition-colors
          ${isLoading || !message.trim() 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-blue-500 hover:bg-blue-600'}
        `}
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <span className="animate-spin">⏳</span>
            <span>Sending...</span>
          </div>
        ) : (
          'Send'
        )}
      </button>
    </form>
  );
}

export default ChatInput; 