import React from 'react';

function Chat() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Chat Interface</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="h-96 overflow-y-auto mb-4 border rounded p-4">
          {/* Chat messages will go here */}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded"
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat; 