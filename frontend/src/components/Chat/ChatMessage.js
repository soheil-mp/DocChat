import React from 'react';
import { formatDistanceToNow } from 'date-fns';

function ChatMessage({ type, content, sources, timestamp }) {
  const isUser = type === 'user';
  const isError = type === 'error';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`
        max-w-[80%] rounded-lg p-4 relative
        ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-100'}
        ${isError ? 'bg-red-100 text-red-700' : ''}
      `}>
        <p className="text-sm whitespace-pre-wrap">{content}</p>
        {sources && sources.length > 0 && (
          <div className="mt-2 text-xs text-gray-500">
            <p className="font-semibold">Sources:</p>
            <ul className="list-disc list-inside">
              {sources.map((source, index) => (
                <li key={index}>{source.source}</li>
              ))}
            </ul>
          </div>
        )}
        {timestamp && (
          <div className="text-xs mt-1 opacity-70">
            {formatDistanceToNow(new Date(timestamp), { addSuffix: true })}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage; 