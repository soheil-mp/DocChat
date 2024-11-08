import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DocumentLibrary: React.FC = () => {
  const [documents, setDocuments] = useState<any[]>([]);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const response = await axios.get('/api/v1/documents');
        setDocuments(response.data);
      } catch (error) {
        console.error('Failed to fetch documents', error);
      }
    };

    fetchDocuments();
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Document Library</h2>
      <div className="grid gap-4">
        {documents.map((doc) => (
          <div 
            key={doc.id} 
            className="bg-white p-4 rounded-lg shadow-md flex justify-between items-center"
          >
            <div>
              <h3 className="font-semibold">{doc.title}</h3>
              <p className="text-gray-500">{doc.file_type}</p>
            </div>
            <span className="text-sm text-gray-500">{new Date(doc.created_at).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentLibrary; 