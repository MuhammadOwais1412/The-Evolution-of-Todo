/**
 * Custom hook for managing chat state and interactions
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { chatService, ChatMessage, SendMessageResponse } from '@/services/chatService';

interface UseChatOptions {
  userId: string;
  conversationId?: string;
}

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: string | null;
  sendMessage: (content: string) => Promise<void>;
  loadHistory: () => Promise<void>;
  clearError: () => void;
}

export function useChat({ userId, conversationId: initialConversationId }: UseChatOptions): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(initialConversationId || null);

  // Load conversation history on mount
  useEffect(() => {
    if (conversationId) {
      loadHistory();
    }
  }, [conversationId]);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    if (!conversationId) {
      const storedConversationId = localStorage.getItem(`chat_conversation_${userId}`);
      if (storedConversationId) {
        setConversationId(storedConversationId);
      }
    }
  }, [userId, conversationId]);

  // Save conversation ID to localStorage when it changes
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem(`chat_conversation_${userId}`, conversationId);
    }
  }, [conversationId, userId]);

  const loadHistory = useCallback(async () => {
    if (!conversationId) return;

    try {
      setIsLoading(true);
      setError(null);
      const response = await chatService.getConversationHistory(userId, conversationId, 50, 0);
      setMessages(response.messages);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversation history');
    } finally {
      setIsLoading(false);
    }
  }, [userId, conversationId]);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Optimistic update: add user message immediately
    const tempMessage: ChatMessage = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, tempMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response: SendMessageResponse = await chatService.sendMessage(userId, {
        message: content,
        conversation_id: conversationId || undefined,
      });

      // Update conversation ID if this is a new conversation
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Replace temp message with actual messages from server
      setMessages(prev => [
        ...prev.filter(m => m.id !== tempMessage.id),
        {
          id: response.message_id,
          role: 'user',
          content,
          timestamp: response.timestamp,
        },
        {
          id: `${response.message_id}-assistant`,
          role: 'assistant',
          content: response.response,
          timestamp: response.timestamp,
          metadata: {
            tool_calls: response.tool_calls,
            requires_confirmation: response.requires_confirmation,
          },
        },
      ]);
    } catch (err: any) {
      // Rollback optimistic update on error
      setMessages(prev => prev.filter(m => m.id !== tempMessage.id));
      setError(err.message || 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  }, [userId, conversationId]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    conversationId,
    sendMessage,
    loadHistory,
    clearError,
  };
}
