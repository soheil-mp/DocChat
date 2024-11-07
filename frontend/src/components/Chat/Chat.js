import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { useMutation, useQuery } from 'react-query';
import { sendMessage } from '../../services/api';

function Chat() {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const chatMutation = useMutation(sendMessage, {
    onSuccess: (response) => {
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: response.response.answer,
        sources: response.response.sources,
        timestamp: new Date().toISOString()
      }]);
    },
    onError: (error) => {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        type: 'error',
        content: 'Sorry, there was an error processing your message.',
        timestamp: new Date().toISOString()
      }]);
    }
  });

  const handleSendMessage = (message) => {
    // Add user message to chat
    setMessages(prev => [...prev, {
      type: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }]);
    
    // Send message to backend
    chatMutation.mutate({
      message,
      context_ids: [], // TODO: Add relevant document IDs
      chat_history: messages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }))
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {messages.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-gray-500">
          <div className="text-center">
            <h2 className="text-xl font-semibold mb-2">Welcome to DocuChat!</h2>
            <p>Upload documents and start asking questions about them.</p>
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} {...message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
      <div className="border-t p-4 bg-white">
        <ChatInput 
          onSend={handleSendMessage}
          isLoading={chatMutation.isLoading}
          placeholder="Ask a question about your documents..."
        />
      </div>
    </div>
  );
}

export default Chat;