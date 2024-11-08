import React, { useState, useRef, useEffect } from 'react';
import axios from '../../lib/axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Document } from '../../types/document';

interface Reaction {
  emoji: string;
  count: number;
}

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  sources?: any[];
  reactions?: Reaction[];
}

interface ChatInterfaceProps {}

const ChatInterface: React.FC<ChatInterfaceProps> = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      content: 'Hello! How can I assist you today?',
      isUser: false,
      sources: []
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);

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
        content: inputMessage,
        session_id: sessionId
      });

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        content: response.data.content,
        isUser: false,
        sources: response.data.sources || []
      };

      setMessages(prevMessages => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error. Please try again.',
        isUser: false
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddReaction = (messageId: string, emoji: string) => {
    setMessages(messages.map(message => {
      if (message.id === messageId) {
        const reactions = message.reactions || [];
        const existingReaction = reactions.find(r => r.emoji === emoji);
        
        if (existingReaction) {
          return {
            ...message,
            reactions: reactions.map(r => 
              r.emoji === emoji ? { ...r, count: r.count + 1 } : r
            )
          };
        }
        
        return {
          ...message,
          reactions: [...reactions, { emoji, count: 1 }]
        };
      }
      return message;
    }));
  };

  // Fetch documents from the backend
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const response = await fetch('/api/v1/documents');
        const data = await response.json();
        setDocuments(data);
      } catch (error) {
        console.error('Error fetching documents:', error);
      }
    };
    
    fetchDocuments();
  }, []);

  return (
    <div className="flex h-[calc(100vh-120px)]">
      {/* Knowledge Base Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-900">Knowledge Base</h3>
          <p className="text-sm text-gray-500 mt-1">Available documents</p>
        </div>
        
        <div className="px-3">
          {documents.map((doc) => (
            <button
              key={doc.id}
              onClick={() => setSelectedDocument(doc.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1
                ${selectedDocument === doc.id 
                  ? 'bg-[#4169E1] text-white' 
                  : 'text-gray-700 hover:bg-gray-100'
                }`}
            >
              <div className="font-medium">{doc.title}</div>
              <div className="text-xs mt-1 truncate">
                {selectedDocument === doc.id ? 'Selected' : doc.type}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Interface */}
      <div className="flex-1 flex flex-col">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative flex flex-col h-[calc(100vh-120px)] bg-white
            rounded-[32px] shadow-lg overflow-hidden"
        >
          <div className="absolute inset-0 -z-10 bg-gradient-to-br from-blue-500/20 via-purple-500/20 to-pink-500/20 animate-gradient-shift"></div>
          <div className="absolute inset-0 -z-10 before:absolute before:inset-0 before:bg-gradient-to-br before:from-blue-500/5 before:via-purple-500/5 before:to-pink-500/5 before:animate-gradient-shift"></div>

          <motion.div 
            className="relative z-10 px-8 py-6 bg-white"
          >
            <h2 className="text-[28px] font-bold text-[#4169E1]">
              Chat with DocuChat
            </h2>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              <p className="text-sm text-gray-500">
                Explore your documents with AI-powered insights ✨
              </p>
            </div>
          </motion.div>

          <div className="relative z-10 flex-grow overflow-y-auto p-6 space-y-6 bg-gradient-to-br from-[#F0F7FF] via-[#F6F0FF] to-[#FFF0F9]">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className={`flex items-start gap-3 ${message.isUser ? 'flex-row-reverse' : 'flex-row'}`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium
                    ${message.isUser ? 'bg-[#FF1493]' : 'bg-[#4169E1]'}`}
                  >
                    {message.isUser ? 'You' : 'AI'}
                  </div>
                  
                  <motion.div
                    className={`
                      relative max-w-[80%] px-4 py-3 rounded-[16px]
                      ${message.isUser 
                        ? 'bg-[#4169E1] text-white' 
                        : 'bg-white shadow-[0_2px_4px_rgba(0,0,0,0.05)]'}
                    `}
                  >
                    <p className="text-[15px] leading-relaxed">
                      {message.content}
                    </p>
                  </motion.div>
                </motion.div>
              ))}
            </AnimatePresence>

            <AnimatePresence>
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="flex items-start gap-3"
                >
                  <div className="w-8 h-8 rounded-full bg-[#4169E1] flex items-center justify-center text-white text-sm font-medium">
                    AI
                  </div>
                  <div className="px-4 py-2 rounded-full bg-white shadow-[0_2px_4px_rgba(0,0,0,0.05)]">
                    <div className="flex space-x-2">
                      {[0, 1, 2].map((i) => (
                        <div 
                          key={i}
                          className="w-2 h-2 bg-[#4169E1] rounded-full animate-bounce"
                          style={{ animationDelay: `${i * 0.1}s` }}
                        />
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="relative z-20 p-4 bg-white">
            <div className="flex gap-2">
              <input 
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type your message..."
                className="flex-grow px-4 py-3 rounded-full border border-[#4169E1]/30
                  focus:outline-none focus:ring-2 focus:ring-[#4169E1]/20 focus:border-[#4169E1]
                  hover:border-[#4169E1]/50 transition-colors text-gray-600 placeholder-gray-400"
              />
              <button 
                onClick={handleSendMessage}
                disabled={isLoading}
                className="px-6 py-3 bg-[#4169E1] text-white rounded-full
                  disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#4169E1]/90
                  transition-colors font-medium min-w-[100px]"
              >
                Send
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ChatInterface; 