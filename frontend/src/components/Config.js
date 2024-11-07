import React from 'react';

function Config() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Model Selection</label>
            <select className="mt-1 block w-full p-2 border rounded">
              <option>OpenAI</option>
              <option>Cohere</option>
              <option>Hugging Face</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Temperature</label>
            <input 
              type="range" 
              min="0.1" 
              max="1.0" 
              step="0.1" 
              className="w-full"
              defaultValue="0.7"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Max Tokens</label>
            <input 
              type="number" 
              min="0" 
              max="2048" 
              className="mt-1 block w-full p-2 border rounded"
              defaultValue="1000"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Config; 