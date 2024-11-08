import React, { useState, useRef, useEffect } from 'react';
import axios from '../../lib/axios';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  sources?: any[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content: inputMessage,
      isUser: true
    };

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/v1/chat/message', { 
        message: inputMessage,
        session_id: sessionId
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!sessionId && response.data.id) {
        setSessionId(response.data.id);
      }

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        content: response.data.messages[response.data.messages.length - 1].content,
        isUser: false,
        sources: response.data.messages[response.data.messages.length - 1].sources || []
      };

      setMessages(prevMessages => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error('Full error details:', error);
      
      if (axios.isAxiosError(error)) {
        console.error('Response data:', error.response?.data);
        console.error('Response status:', error.response?.status);
        console.error('Response headers:', error.response?.headers);
      }
      
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: axios.isAxiosError(error) 
          ? error.response?.data?.detail || JSON.stringify(error.response?.data) || 'Sorry, something went wrong.'
          : 'Sorry, something went wrong.',
        isUser: false
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`
                max-w-[70%] p-3 rounded-lg 
                ${message.isUser 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-white text-gray-800 border'}
              `}
            >
              {message.content}
              {message.sources && message.sources.length > 0 && (
                <div className="text-xs text-gray-500 mt-2">
                  Sources:
                  {message.sources.map((source, index) => (
                    <div key={index}>
                      {source.title} (Relevance: {source.relevance_score.toFixed(2)})
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white p-3 rounded-lg">
              Typing...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-4 bg-white border-t flex">
        <input 
          type="text" 
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Type your message..."
          className="flex-grow p-2 border rounded-l-lg"
        />
        <button 
          onClick={handleSendMessage}
          disabled={isLoading}
          className="bg-blue-500 text-white p-2 rounded-r-lg hover:bg-blue-600 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface; 