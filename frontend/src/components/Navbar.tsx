import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuthStore();

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">DocuChat</Link>
        {isAuthenticated && (
          <div className="space-x-4">
            <Link to="/chat" className="text-gray-800 hover:text-blue-600">Chat</Link>
            <Link to="/documents" className="text-gray-800 hover:text-blue-600">Documents</Link>
            <Link to="/upload" className="text-gray-800 hover:text-blue-600">Upload</Link>
            <button 
              onClick={logout} 
              className="text-red-600 hover:text-red-800"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 