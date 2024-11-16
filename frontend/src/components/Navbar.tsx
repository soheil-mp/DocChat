import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Navbar: React.FC = () => {
  return (
    <nav className="border-b border-[#404144] bg-[#1a1b1e] backdrop-blur-lg sticky top-0 z-50">
      <div className="container mx-auto px-6 h-16 flex items-center justify-between max-w-7xl">
        <Link to="/" className="flex items-center space-x-2 group">
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center"
          >
            <span className="text-2xl font-bold bg-gradient-to-r from-[#00ffbb] to-[#8b5cf6] 
              bg-clip-text text-transparent">
              DocChat
            </span>
            <span className="ml-2 text-2xl">✨</span>
          </motion.div>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar; 