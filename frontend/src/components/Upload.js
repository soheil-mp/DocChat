import React from 'react';

function Upload() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Document Upload</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
          <p className="text-gray-600 mb-4">
            Drag and drop files here, or click to select files
          </p>
          <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Select Files
          </button>
          <p className="text-sm text-gray-500 mt-2">
            Supported formats: PDF, DOCX, TXT
          </p>
        </div>
      </div>
    </div>
  );
}

export default Upload; 