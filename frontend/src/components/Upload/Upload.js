import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { uploadDocument } from '../../services/api';

function Upload() {
  const [dragActive, setDragActive] = useState(false);
  
  const uploadMutation = useMutation(uploadDocument, {
    onSuccess: (response) => {
      console.log('Upload successful:', response);
      // TODO: Add success notification
    },
    onError: (error) => {
      console.error('Upload error:', error);
      // TODO: Add error notification
    }
  });

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files?.[0]) {
      uploadMutation.mutate(files[0]);
    }
  };

  const handleFileSelect = async (e) => {
    const files = e.target.files;
    if (files?.[0]) {
      uploadMutation.mutate(files[0]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div
        className={`
          border-2 border-dashed rounded-lg p-8
          text-center cursor-pointer
          ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${uploadMutation.isLoading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          onChange={handleFileSelect}
          accept=".pdf,.docx,.txt"
          disabled={uploadMutation.isLoading}
        />
        <label 
          htmlFor="file-upload"
          className="cursor-pointer"
        >
          <div className="text-gray-600">
            {uploadMutation.isLoading ? (
              <p>Uploading...</p>
            ) : (
              <>
                <p>Drag and drop your files here, or click to select files</p>
                <p className="text-sm mt-2">Supported formats: PDF, DOCX, TXT</p>
              </>
            )}
          </div>
        </label>
      </div>
    </div>
  );
}

export default Upload; 