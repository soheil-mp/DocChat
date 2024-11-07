import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="text-xl font-semibold text-gray-700">
            <Link to="/">DocuChat</Link>
          </div>
          <div className="flex space-x-4">
            <Link to="/" className="text-gray-700 hover:text-blue-500">Chat</Link>
            <Link to="/upload" className="text-gray-700 hover:text-blue-500">Upload</Link>
            <Link to="/config" className="text-gray-700 hover:text-blue-500">Settings</Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navigation; 