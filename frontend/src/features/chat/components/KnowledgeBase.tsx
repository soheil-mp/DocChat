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
  isLoading,
  error,
  className
}) => {
  return (
    <div className={`${className}`}>
      <div className="p-6 border-b border-[#404144]">
        <h2 className="text-xl font-bold text-[#00ffbb]">
          Knowledge Base
        </h2>
        <p className="text-sm text-[#a1a1aa] mt-1 flex items-center">
          <svg 
            className="w-4 h-4 mr-2 text-[#00ffbb]" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
            />
          </svg>
          {documents.length} document{documents.length !== 1 ? 's' : ''} available
        </p>
      </div>

      <div className="p-4 space-y-3 max-h-[calc(100vh-220px)] overflow-y-auto
        scrollbar-thin scrollbar-thumb-[#404144] scrollbar-track-transparent">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="w-6 h-6 border-2 border-[#00ffbb] border-t-transparent 
              rounded-full animate-spin" />
          </div>
        ) : error ? (
          <div className="text-center py-8 text-red-400">{error}</div>
        ) : (
          documents.map((doc) => (
            <motion.div
              key={doc.id}
              whileHover={{ scale: 1.02, x: 4 }}
              whileTap={{ scale: 0.98 }}
              className={`p-4 rounded-xl cursor-pointer transition-all
                ${selectedDocument === doc.id 
                  ? 'bg-[#00ffbb]/10 border-[#00ffbb]' 
                  : 'hover:bg-[#34353a] border-transparent'
                } border`}
              onClick={() => onSelectDocument(doc.id)}
            >
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-[#00ffbb]/10">
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
                <div>
                  <h3 className="font-medium text-[#e4e4e7]">{doc.title}</h3>
                  <p className="text-sm text-[#a1a1aa] mt-1">
                    Added {new Date(doc.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
};

export default KnowledgeBase;