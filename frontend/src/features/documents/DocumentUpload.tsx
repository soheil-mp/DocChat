import React, { useState } from 'react';
import axios from 'axios';

const DocumentUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/api/v1/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      console.log('Upload successful', response.data);
      // Add success notification or UI update
    } catch (error) {
      console.error('Upload failed', error);
      // Add error handling
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Upload Document</h2>
      <div className="flex items-center space-x-4">
        <input 
          type="file" 
          onChange={handleFileSelect}
          className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button 
          onClick={handleUpload}
          disabled={!selectedFile}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          Upload
        </button>
      </div>
    </div>
  );
};

export default DocumentUpload; 