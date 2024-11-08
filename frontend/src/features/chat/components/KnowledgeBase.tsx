import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Document } from '../../../types/document';

interface KnowledgeBaseProps {
  documents: Document[];
  selectedDocument: string | null;
  onSelectDocument: (id: string) => void;
  isLoading?: boolean;
  error?: string | null;
  className?: string;
}

const KnowledgeBase: React.FC<KnowledgeBaseProps> = ({
  documents,
  selectedDocument,
  onSelectDocument,
  isLoading = false,
  error = null,
  className = ''
}) => {
  return (
    <div className={`w-[380px] bg-white/95 backdrop-blur-xl rounded-[32px] 
      border border-white/50 shadow-lg overflow-hidden ${className}`}>
      <motion.div 
        className="p-6 border-b border-gray-100/50"
        whileHover={{ scale: 1.01 }}
      >
        <h3 className="text-xl font-bold text-[#4169E1]">
          Knowledge Base
        </h3>
        <div className="flex items-center gap-2 mt-1.5">
          <span className="flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-blue-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
          </span>
          <p className="text-sm text-gray-500">
            {documents.length} document{documents.length !== 1 ? 's' : ''} available
          </p>
        </div>
      </motion.div>
      
      <div className="p-4 max-h-[calc(100vh-220px)] overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="w-6 h-6 border-2 border-blue-500/20 border-t-blue-500 rounded-full"
            />
          </div>
        ) : error ? (
          <div className="text-red-500 p-4 text-center text-sm bg-red-50/50 rounded-xl">
            {error}
          </div>
        ) : documents.length === 0 ? (
          <div className="text-gray-500 p-4 text-center text-sm bg-gray-50/50 rounded-xl">
            No documents available
          </div>
        ) : (
          <AnimatePresence mode="popLayout">
            {documents.map((doc) => (
              <motion.button
                key={doc.id}
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                whileHover={{ scale: 1.02, x: 4 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onSelectDocument(doc.id)}
                className={`w-full text-left p-4 rounded-2xl mb-3 transition-all duration-200
                  ${selectedDocument === doc.id 
                    ? 'bg-blue-50/80 border border-blue-200/50 shadow-md' 
                    : 'hover:bg-gray-50/80 border border-transparent'
                  }
                  group backdrop-blur-sm`}
              >
                <div className="flex items-start gap-4">
                  <motion.div 
                    className="p-3 rounded-xl bg-gradient-to-br from-blue-500/5 to-purple-500/5
                      border border-blue-100/20 group-hover:border-blue-200/30 transition-colors"
                    whileHover={{ scale: 1.1, rotate: 5 }}
                  >
                    {doc.type === 'application/pdf' ? '📄' : '📝'}
                  </motion.div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-gray-900 truncate">
                      {doc.title}
                    </h4>
                    <p className="text-xs text-gray-500 mt-1">
                      Added {new Date(doc.created_at).toLocaleDateString()}
                    </p>
                    {doc.type === 'application/pdf' && (
                      <motion.div 
                        initial={false}
                        animate={{ height: selectedDocument === doc.id ? 'auto' : '0' }}
                        className="mt-3 relative w-full rounded-xl overflow-hidden bg-gray-100/50"
                      >
                        <div className="aspect-[4/3] relative">
                          <object
                            data={`http://localhost:8000/api/v1/documents/preview/${doc.id}#toolbar=0&view=FitH`}
                            type="application/pdf"
                            className="absolute inset-0 w-full h-full"
                          >
                            <div className="flex items-center justify-center h-full">
                              <a 
                                href={`http://localhost:8000/api/v1/documents/preview/${doc.id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:text-blue-600 text-sm font-medium
                                  flex items-center gap-2 px-4 py-2 rounded-lg bg-white/80 
                                  hover:bg-white transition-colors shadow-sm"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <span>Open PDF</span>
                                <span className="text-xs">↗</span>
                              </a>
                            </div>
                          </object>
                        </div>
                      </motion.div>
                    )}
                  </div>
                </div>
              </motion.button>
            ))}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
};

export default KnowledgeBase;