import React, { useRef, useMemo } from 'react';
import { motion } from 'framer-motion';
import axios from '../../../lib/axios';
import { isAxiosError } from 'axios';
import type { AxiosError } from 'axios';

interface Document {
  id: string;
  title: string;
  created_at: string;
}

interface KnowledgeBaseProps {
  documents: Document[];
  selectedDocument: Document | null;
  onSelectDocument: (doc: Document | null) => void;
  isLoading: boolean;
  error: string | null;
  className?: string;
  onDocumentsChange?: () => void;
}

const KnowledgeBase: React.FC<KnowledgeBaseProps> = ({
  documents,
  selectedDocument,
  onSelectDocument,
  isLoading,
  error,
  className = '',
  onDocumentsChange
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Memoize document filtering and sorting
  const sortedDocuments = useMemo(() => 
    [...documents].sort((a, b) => 
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    ),
    [documents]
  );

  // Optimize file upload with chunking
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const CHUNK_SIZE = 1024 * 1024; // 1MB chunks
    const chunks = Math.ceil(file.size / CHUNK_SIZE);
    
    try {
      for (let i = 0; i < chunks; i++) {
        const chunk = file.slice(
          i * CHUNK_SIZE,
          Math.min((i + 1) * CHUNK_SIZE, file.size)
        );
        const formData = new FormData();
        formData.append('file', chunk);
        formData.append('chunk', String(i));
        formData.append('chunks', String(chunks));
        
        await axios.post('/api/v1/documents/upload/chunk', formData);
      }
      onDocumentsChange?.();
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleRemoveDocument = async (docId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    event.preventDefault();
    
    try {
      console.log('Full delete URL:', `${axios.defaults.baseURL}/api/v1/documents/${docId}`);
      
      const response = await axios.delete(`/api/v1/documents/${docId}`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        transformResponse: [function (data) {
          try {
            return JSON.parse(data);
          } catch (e) {
            return data;
          }
        }]
      });

      console.log('Delete response:', response);
      
      if (response.status === 200 || response.status === 204) {
        if (selectedDocument?.id === docId) {
          onSelectDocument(null);
        }
        
        onDocumentsChange?.();
      } else {
        throw new Error(`Unexpected response status: ${response.status}`);
      }
    } catch (error: unknown) {
      console.error('Detailed error removing document:', error);
      
      if (isAxiosError(error)) {
        console.log('Error details:', {
          response: error.response,
          request: error.request,
          message: error.message
        });

        if (error.response) {
          alert(`Failed to delete document: ${error.response.data?.detail || 'Unknown error'}`);
        } else if (error.request) {
          alert('No response from server. Please check your connection.');
        } else {
          alert(`Error: ${error.message}`);
        }
      } else {
        alert('An unexpected error occurred. Please try again.');
      }
    }
  };

  return (
    <div className={`p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-white">Knowledge Base</h2>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => fileInputRef.current?.click()}
          className="px-4 py-2 bg-[#00ffbb] text-[#1a1b1e] rounded-lg 
            hover:bg-[#00ffbb]/90 transition-all duration-200"
        >
          Add PDF
        </motion.button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileUpload}
          accept=".pdf"
          className="hidden"
        />
      </div>

      {/* Documents List */}
      <div className="space-y-2">
        {sortedDocuments.map((doc) => (
          <div
            key={doc.id}
            className={`p-4 rounded-lg border border-[#404144] 
              ${selectedDocument?.id === doc.id ? 'bg-[#34353a]' : 'bg-[#2d2e31]'}
              hover:bg-[#34353a] transition-colors cursor-pointer
              flex justify-between items-center group`}
            onClick={() => onSelectDocument(doc)}
          >
            <div>
              <h3 className="text-[#e4e4e7] font-medium">{doc.title}</h3>
              <p className="text-sm text-[#a1a1aa]">
                {new Date(doc.created_at).toLocaleDateString()}
              </p>
            </div>
            
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => handleRemoveDocument(doc.id, e)}
              className="p-2 text-[#a1a1aa] hover:text-red-400 
                rounded-full hover:bg-[#404144] transition-colors
                opacity-0 group-hover:opacity-100"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </motion.button>
          </div>
        ))}

        {isLoading && (
          <div className="text-center py-4 text-[#a1a1aa]">
            Loading documents...
          </div>
        )}

        {error && (
          <div className="text-center py-4 text-red-400">
            Error: {error}
          </div>
        )}

        {!isLoading && !error && documents.length === 0 && (
          <div className="text-center py-4 text-[#a1a1aa]">
            No documents yet. Add your first PDF!
          </div>
        )}
      </div>
    </div>
  );
};

export default KnowledgeBase;