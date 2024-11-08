import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Document } from '../types/document';

interface KnowledgeBaseProps {
  documents: Document[];
  selectedDocument: string | null;
  onSelectDocument: (id: string) => void;
}

const KnowledgeBase: React.FC<KnowledgeBaseProps> = ({
  documents,
  selectedDocument,
  onSelectDocument,
}) => {
  return (
    <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Knowledge Base</h3>
        <p className="text-sm text-gray-500 mt-1">
          {documents.length} document{documents.length !== 1 ? 's' : ''} available
        </p>
      </div>
      
      <div className="p-3">
        <AnimatePresence>
          {documents.map((doc) => (
            <motion.button
              key={doc.id}
              layout
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              onClick={() => onSelectDocument(doc.id)}
              className={`w-full text-left p-3 rounded-xl mb-2 transition-all
                ${selectedDocument === doc.id 
                  ? 'bg-blue-50 border-blue-200 shadow-sm' 
                  : 'hover:bg-gray-50 border border-transparent'
                }`}
            >
              <div className="flex items-start gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  📄
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 line-clamp-1">
                    {doc.title}
                  </h4>
                  <p className="text-xs text-gray-500 mt-1">
                    Added {new Date(doc.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </motion.button>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default KnowledgeBase; 