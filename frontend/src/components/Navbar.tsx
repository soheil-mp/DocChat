import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  return (
    <nav className="border-b transition-colors duration-300 backdrop-blur-lg bg-white/80 border-gray-200">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between max-w-7xl">
        <Link to="/" className="flex items-center space-x-2 group">
          <span className="text-2xl font-bold bg-gradient-to-r from-neon-blue via-neon-purple to-neon-pink bg-clip-text text-transparent">
            DocuChat
          </span>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar; 