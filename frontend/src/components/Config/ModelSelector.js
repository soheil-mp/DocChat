import React from 'react';

function ModelSelector({ onChange, options, value }) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Model Selection
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 
                 focus:outline-none focus:ring-blue-500 focus:border-blue-500 
                 rounded-md shadow-sm"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default ModelSelector; 