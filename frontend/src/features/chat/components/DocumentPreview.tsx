import React from 'react';
import { motion } from 'framer-motion';
import { Document } from '../../../types/document';

interface DocumentPreviewProps {
  document: Document | null;
  onClose: () => void;
}

const DocumentPreview = ({ document, onClose }: DocumentPreviewProps) => {
  if (!document) return null;

  return (
    <motion.div
      initial={{ opacity: 0, x: 300 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 300 }}
      className="fixed right-0 top-0 h-screen w-[600px] bg-[#2d2e31] 
        border-l border-[#404144] z-50"
    >
      <div className="p-4 border-b border-[#404144] flex justify-between items-center">
        <div>
          <h3 className="font-semibold text-[#e4e4e7]">{document.title}</h3>
          <p className="text-sm text-[#a1a1aa]">
            Added {new Date(document.created_at).toLocaleDateString()}
          </p>
        </div>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onClose}
          className="p-2 hover:bg-[#34353a] rounded-full transition-colors"
          aria-label="Close preview"
        >
          <svg 
            className="w-5 h-5 text-[#a1a1aa]" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </motion.button>
      </div>
      
      <div className="h-[calc(100vh-88px)] overflow-hidden">
        {document.type === 'application/pdf' ? (
          <div className="w-full h-full bg-[#1a1b1e]">
            <iframe
              src={`http://localhost:8000/api/v1/documents/preview/${document.id}#toolbar=1&view=FitH`}
              className="w-full h-full border-0"
              title={`Preview of ${document.title}`}
            />
          </div>
        ) : (
          <div className="p-4 overflow-y-auto h-full">
            <div className="prose prose-sm max-w-none prose-invert">
              {document.content || (
                <p className="text-[#a1a1aa] italic">No preview available</p>
              )}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default DocumentPreview;