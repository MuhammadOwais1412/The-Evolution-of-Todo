/**
 * Chat page - Main entry point for chat interface
 */
'use client';

import { useEffect, useState } from 'react';
import { AuthGuard } from '@/components/AuthGuard';
import { ChatInterface } from '@/components/ChatInterface';

export default function ChatPage() {
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // Get user ID from localStorage (set by Better Auth during login)
    const storedUserId = localStorage.getItem('user_id');
    if (storedUserId) {
      setUserId(storedUserId);
    }
  }, []);

  if (!userId) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <AuthGuard>
      <ChatInterface userId={userId} />
    </AuthGuard>
  );
}
