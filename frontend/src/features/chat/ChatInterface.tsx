import React, { useState, useRef, useEffect } from 'react';
import axios from '../../lib/axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Document } from '../../types/document';
import KnowledgeBase from './components/KnowledgeBase';
import DocumentPreview from './components/DocumentPreview';
import ParticlesBackground from '../../components/ParticlesBackground';
import magicPattern from '../../assets/magic-pattern.svg';

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
      {/* Background - Softer, more minimal */}
      <div className="absolute inset-0 bg-[#1a1b1e] rounded-3xl" />
      
      {/* Knowledge Base - Gemini style */}
      <KnowledgeBase
        documents={documents}
        selectedDocument={selectedDocument}
        onSelectDocument={setSelectedDocument}
        isLoading={isLoadingDocuments}
        error={error}
        className="z-10 relative w-[380px] bg-[#2d2e31] 
          rounded-3xl border border-[#404144]" 
      />

      {/* Main Chat Area */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex-1 flex flex-col relative z-10 max-w-[800px]"
      >
        <div className="rounded-3xl overflow-hidden bg-[#2d2e31] 
          border border-[#404144] flex flex-col h-[calc(100vh-150px)]">
          
          {/* Header - Simplified */}
          <div className="px-8 py-6 border-b border-[#404144]">
            <h2 className="text-[32px] font-bold text-white">
              DocuChat AI
            </h2>
            <div className="flex items-center gap-3 mt-2">
              <div className="w-2 h-2 rounded-full bg-[#00ffbb] animate-pulse" />
              <p className="text-sm text-[#a1a1aa]">
                Explore your documents with AI-powered magic ✨
              </p>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4 
            scrollbar-thin scrollbar-thumb-[#404144] scrollbar-track-transparent">
            <div className="max-w-3xl mx-auto">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex items-start gap-3 mb-8 ${message.isUser ? 'flex-row-reverse' : ''}`}
                >
                  {/* Avatar - Updated styling */}
                  <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm
                    ${message.isUser 
                      ? 'bg-[#8e85ff] text-white'
                      : 'bg-[#00ffbb] text-[#1a1b1e]'}`}
                  >
                    {message.isUser ? '👤' : '🤖'}
                  </div>
                  
                  {/* Message Bubble - Refined colors and contrast */}
                  <div className={`
                    relative max-w-[80%] px-5 py-3.5 rounded-2xl
                    ${message.isUser 
                      ? 'bg-[#35363a] ml-auto border border-[#8e85ff]/20'
                      : 'bg-[#35363a]'}
                  `}>
                    <p className="text-[15px] leading-relaxed text-[#e4e4e7]">
                      {message.content}
                    </p>
                    
                    {/* Sources - Better spacing and contrast */}
                    {!message.isUser && message.sources && Array.isArray(message.sources) && 
                     message.sources.length > 0 && message.sources.some(source => source.document_id) && (
                      <div className="mt-4 pt-4 border-t border-[#404144]">
                        <div className="flex items-center mb-3">
                          <span className="text-xs font-medium text-[#00ffbb]">
                            Referenced Documents
                          </span>
                        </div>

                        <div className="space-y-2">
                          {message.sources.map((source, index) => (
                            <motion.div 
                              key={index}
                              initial={{ opacity: 0, y: 5 }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ delay: index * 0.1 }}
                              whileHover={{ scale: 1.01 }}
                              onClick={() => setSelectedDocument(source.document_id)}
                              className="group cursor-pointer p-3 rounded-lg 
                                bg-[#2d2e31] hover:bg-[#404144]
                                border border-[#404144] hover:border-[#00ffbb]/20
                                transition-all duration-200"
                            >
                              <div className="flex items-center gap-3">
                                <div className="shrink-0 w-5 h-5 flex items-center justify-center">
                                  <svg 
                                    className="w-4 h-4 text-[#00ffbb]" 
                                    fill="none" 
                                    stroke="currentColor" 
                                    viewBox="0 0 24 24"
                                  >
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
                                    />
                                  </svg>
                                </div>
                                <div className="flex-1 min-w-0">
                                  <h4 className="text-xs font-medium text-[#e4e4e7] truncate">
                                    {source.title}
                                  </h4>
                                  <p className="mt-1 text-xs text-[#a1a1aa] line-clamp-2">
                                    {source.content}
                                  </p>
                                </div>
                                <div className="text-[#00ffbb] opacity-0 group-hover:opacity-100 transition-opacity">
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                                      d="M9 5l7 7-7 7" 
                                    />
                                  </svg>
                                </div>
                              </div>
                            </motion.div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Input Area - Enhanced hover and focus states */}
          <div className="p-4 border-t border-[#404144]">
            <div className="max-w-3xl mx-auto relative">
              <input 
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                placeholder="Ask me anything..."
                className="w-full px-5 py-3.5 rounded-2xl 
                  bg-[#35363a] hover:bg-[#404144]
                  border border-[#404144] hover:border-[#00ffbb]/20
                  focus:outline-none focus:border-[#00ffbb]/30 focus:ring-1 focus:ring-[#00ffbb]/20
                  transition-all duration-200
                  text-[#e4e4e7] placeholder-[#71717a] text-[15px]"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSendMessage}
                className="absolute right-3 top-1/2 -translate-y-1/2
                  p-2 rounded-lg text-[#00ffbb] hover:bg-[#00ffbb]/10
                  transition-all duration-200"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14m-7-7l7 7-7 7" />
                </svg>
              </motion.button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Document Preview */}
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