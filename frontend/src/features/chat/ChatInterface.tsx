import React, { useState, useRef, useEffect } from 'react';
import axios from '../../lib/axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Document } from '../../types/document';
import KnowledgeBase from './components/KnowledgeBase';
import DocumentPreview from './components/DocumentPreview';
import ParticlesBackground from '../../components/ParticlesBackground';

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
  const [sessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoadingDocuments, setIsLoadingDocuments] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);
  const [previewDocument, setPreviewDocument] = useState<Document | null>(null);

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

  // Fetch documents from the backend
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        setIsLoadingDocuments(true);
        const response = await fetch('http://localhost:8000/api/v1/documents/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setDocuments(data);
      } catch (error) {
        console.error('Error fetching documents:', error);
        setError('Failed to load documents');
      } finally {
        setIsLoadingDocuments(false);
      }
    };
    
    fetchDocuments();
  }, []);

  // Update preview document when selection changes
  useEffect(() => {
    if (selectedDocument) {
      const doc = documents.find(d => d.id === selectedDocument);
      setPreviewDocument(doc || null);
    } else {
      setPreviewDocument(null);
    }
  }, [selectedDocument, documents]);

  const handleClosePreview = () => {
    setSelectedDocument(null);
    setPreviewDocument(null);
  };

  return (
    <div className="relative flex h-[calc(100vh-120px)] overflow-hidden p-6 gap-6">
      {/* Background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 opacity-70" />
      <div className="absolute inset-0 bg-wave-pattern opacity-10" />
      
      {/* Knowledge Base - Fixed width */}
      <KnowledgeBase
        documents={documents}
        selectedDocument={selectedDocument}
        onSelectDocument={setSelectedDocument}
        isLoading={isLoadingDocuments}
        error={error}
        className="z-10 relative w-[380px] shadow-xl" 
      />

      {/* Main Chat Area - Fixed height with scroll */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex-1 flex flex-col relative z-10 max-w-[800px]"
      >
        <div className="rounded-[32px] shadow-2xl overflow-hidden 
          bg-white/90 backdrop-blur-xl border border-white/50
          flex flex-col h-[calc(100vh-150px)]"> {/* Fixed height container */}
          
          {/* Header - Fixed */}
          <motion.div 
            className="px-8 py-6 bg-gradient-to-r from-blue-500/5 via-purple-500/5 to-pink-500/5
              border-b border-white/20 flex-shrink-0" // Added flex-shrink-0 to prevent header from shrinking
          >
            <h2 className="text-[32px] font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600
              bg-clip-text text-transparent">
              DocuChat AI
            </h2>
            <div className="flex items-center gap-3 mt-2">
              <span className="flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-2.5 w-2.5 rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
              </span>
              <p className="text-sm text-gray-600">
                Explore your documents with AI-powered insights ✨
              </p>
            </div>
          </motion.div>

          {/* Messages Area - Scrollable */}
          <div className="flex-1 overflow-y-auto overflow-x-hidden p-6 space-y-6
            bg-gradient-to-br from-blue-50/50 via-purple-50/50 to-pink-50/50">
            <div className="max-w-3xl mx-auto"> {/* Content width constraint */}
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className={`flex items-start gap-3 ${message.isUser ? 'flex-row-reverse' : 'flex-row'}`}
                  >
                    {/* Avatar */}
                    <motion.div 
                      whileHover={{ scale: 1.1 }}
                      className={`w-10 h-10 rounded-2xl flex items-center justify-center text-white text-sm font-medium
                        shadow-lg backdrop-blur-sm
                        ${message.isUser 
                          ? 'bg-gradient-to-br from-pink-500 to-purple-500' 
                          : 'bg-gradient-to-br from-blue-500 to-indigo-500'}`}
                    >
                      {message.isUser ? '👤' : '🤖'}
                    </motion.div>
                    
                    {/* Message Bubble */}
                    <motion.div
                      whileHover={{ scale: 1.01 }}
                      className={`
                        relative max-w-[80%] px-5 py-4 rounded-2xl
                        ${message.isUser 
                          ? 'bg-gradient-to-br from-pink-500 to-purple-500 text-white shadow-lg' 
                          : 'bg-white/90 backdrop-blur-sm shadow-xl border border-white/50'}
                      `}
                    >
                      <p className={`text-[15px] leading-relaxed ${!message.isUser ? 'text-gray-700' : ''}`}>
                        {message.content}
                      </p>
                      
                      {/* Sources section with enhanced styling */}
                      {!message.isUser && message.sources && message.sources.length > 0 && (
                        <div className="mt-4 pt-3 border-t border-gray-200/20">
                          <p className="text-xs font-semibold mb-2 flex items-center gap-2 text-gray-600">
                            <span className="animate-bounce-subtle">📚</span> 
                            Referenced Documents
                          </p>
                          {message.sources.map((source, index) => (
                            <motion.div 
                              key={index}
                              whileHover={{ scale: 1.02, x: 4 }}
                              whileTap={{ scale: 0.98 }}
                              className="text-xs p-3 rounded-xl bg-blue-50/50 mb-2 
                                hover:bg-blue-100/50 transition-all cursor-pointer
                                border border-blue-100/50 backdrop-blur-sm"
                              onClick={() => setSelectedDocument(source.document_id)}
                            >
                              <p className="font-medium text-blue-700">{source.title}</p>
                              <p className="text-gray-600 line-clamp-2 mt-1">{source.content}</p>
                            </motion.div>
                          ))}
                        </div>
                      )}
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
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-500 
                      flex items-center justify-center text-white shadow-lg">
                      🤖
                    </div>
                    <div className="px-5 py-3 rounded-2xl bg-white/90 shadow-xl border border-white/50 backdrop-blur-sm">
                      <div className="flex space-x-2">
                        {[0, 1, 2].map((i) => (
                          <motion.div 
                            key={i}
                            animate={{
                              scale: [1, 1.2, 1],
                              opacity: [0.5, 1, 0.5]
                            }}
                            transition={{
                              duration: 1,
                              repeat: Infinity,
                              delay: i * 0.2
                            }}
                            className="w-2.5 h-2.5 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-full"
                          />
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Input Area - Fixed */}
          <div className="relative z-20 p-6 bg-white/90 backdrop-blur-xl border-t border-white/50 flex-shrink-0">
            <div className="flex gap-3 items-center max-w-3xl mx-auto">
              <motion.div 
                className="flex-grow relative group"
                whileHover={{ scale: 1.01 }}
              >
                <input 
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  placeholder="Type your message..."
                  className="w-full px-6 py-4 rounded-2xl border border-gray-200
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    hover:border-blue-500/50 transition-all text-gray-600 placeholder-gray-400
                    bg-white/80 backdrop-blur-sm pr-12"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400 pointer-events-none">
                  Press Enter ↵
                </span>
              </motion.div>
              <motion.button 
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`px-8 py-4 rounded-2xl font-medium min-w-[120px]
                  transition-all duration-200 flex items-center justify-center gap-2
                  ${isLoading || !inputMessage.trim() 
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg hover:shadow-xl'
                  }`}
              >
                Send
                <motion.span 
                  animate={{ x: [0, 4, 0] }}
                  transition={{ repeat: Infinity, duration: 1.5 }}
                >
                  ✨
                </motion.span>
              </motion.button>
            </div>
          </div>
        </div>
      </motion.div>

      <AnimatePresence>
        {previewDocument && (
          <DocumentPreview
            document={previewDocument}
            onClose={handleClosePreview}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatInterface; 