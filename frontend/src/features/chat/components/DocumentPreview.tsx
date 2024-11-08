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
      className="fixed right-0 top-0 h-screen w-[600px] bg-white shadow-lg border-l border-gray-200 z-50"
    >
      <div className="p-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h3 className="font-semibold text-gray-900">{document.title}</h3>
          <p className="text-sm text-gray-500">
            Added {new Date(document.created_at).toLocaleDateString()}
          </p>
        </div>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          aria-label="Close preview"
        >
          ✕
        </button>
      </div>
      
      <div className="h-[calc(100vh-88px)] overflow-hidden">
        {document.type === 'application/pdf' ? (
          <div className="w-full h-full">
            <iframe
              src={`http://localhost:8000/api/v1/documents/preview/${document.id}#toolbar=1&view=FitH`}
              className="w-full h-full border-0"
              title={`Preview of ${document.title}`}
            />
          </div>
        ) : (
          <div className="p-4 overflow-y-auto h-full">
            <div className="prose prose-sm max-w-none">
              {document.content || (
                <p className="text-gray-500 italic">No preview available</p>
              )}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default DocumentPreview;