import React, { useState } from 'react';

function ParameterSlider({ 
  label, 
  value, 
  onChange, 
  min, 
  max, 
  step, 
  tooltip 
}) {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="space-y-2 relative">
      <div className="flex justify-between items-center">
        <label className="block text-sm font-medium text-gray-700">
          {label}
        </label>
        <div className="relative">
          <button
            type="button"
            className="text-gray-400 hover:text-gray-500"
            onMouseEnter={() => setShowTooltip(true)}
            onMouseLeave={() => setShowTooltip(false)}
          >
            <svg 
              className="h-5 w-5" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </button>
          {showTooltip && (
            <div className="absolute right-0 w-48 px-2 py-1 bg-gray-900 text-white 
                          text-xs rounded shadow-lg z-10 -mt-1 transform translate-x-2">
              {tooltip}
            </div>
          )}
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(parseFloat(e.target.value))}
          className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none 
                   cursor-pointer accent-blue-500"
        />
        <span className="w-12 text-sm text-gray-600">
          {value}
        </span>
      </div>
    </div>
  );
}

export default ParameterSlider; 