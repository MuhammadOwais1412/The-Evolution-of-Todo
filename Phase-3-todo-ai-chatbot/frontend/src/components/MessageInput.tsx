/**
 * Message input component for sending chat messages
 */
'use client';

import { useState, KeyboardEvent } from 'react';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

export function MessageInput({ onSendMessage, isLoading, disabled }: MessageInputProps) {
  const [message, setMessage] = useState('');
  const maxLength = 1000;

  const handleSend = () => {
    if (message.trim() && !isLoading && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isOverLimit = message.length > maxLength;

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="flex flex-col space-y-2">
        <div className="flex space-x-2">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
            disabled={isLoading || disabled}
            className={`flex-1 resize-none rounded-lg border ${
              isOverLimit ? 'border-red-500' : 'border-gray-300'
            } p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed`}
            rows={3}
          />
          <button
            onClick={handleSend}
            disabled={!message.trim() || isLoading || disabled || isOverLimit}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors self-end"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        <div className="flex justify-between text-sm">
          <span className={`${isOverLimit ? 'text-red-500' : 'text-gray-500'}`}>
            {message.length} / {maxLength} characters
          </span>
          {isLoading && (
            <span className="text-blue-600">Processing...</span>
          )}
        </div>
      </div>
    </div>
  );
}
