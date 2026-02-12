/**
 * Chat service for interacting with chat API endpoints
 */
import apiClient from './apiClient';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface SendMessageRequest {
  message: string;
  conversation_id?: string;
  requires_confirmation?: boolean;
}

export interface SendMessageResponse {
  success: boolean;
  response: string;
  conversation_id: string;
  message_id: string;
  tool_calls?: Array<Record<string, any>>;
  requires_confirmation?: boolean;
  timestamp: string;
}

export interface ConversationHistoryResponse {
  success: boolean;
  messages: ChatMessage[];
  total_count: number;
  has_more: boolean;
}

export interface ErrorResponse {
  success: false;
  error_code: string;
  error_message: string;
  details?: Record<string, any>;
}

class ChatService {
  /**
   * Send a chat message with retry logic
   */
  async sendMessage(
    userId: string,
    request: SendMessageRequest,
    maxRetries: number = 3
  ): Promise<SendMessageResponse> {
    let lastError: any;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const response = await apiClient.post<SendMessageResponse>(
          `/api/${userId}/chat`,
          request
        );
        return response.data;
      } catch (error: any) {
        lastError = error;

        // Only retry transient errors
        if (this.isTransientError(error)) {
          const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
          await this.sleep(delay);
          continue;
        }

        // Non-transient errors fail immediately
        throw this.handleError(error);
      }
    }

    throw this.handleError(lastError);
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(
    userId: string,
    conversationId: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<ConversationHistoryResponse> {
    try {
      const response = await apiClient.get<ConversationHistoryResponse>(
        `/api/${userId}/conversations/${conversationId}/messages`,
        {
          params: { limit, offset },
        }
      );
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  /**
   * Handle API errors and convert to user-friendly messages
   */
  private handleError(error: any): Error {
    if (error.response?.data) {
      const errorData = error.response.data as ErrorResponse;
      return new Error(errorData.error_message || 'An error occurred');
    }

    // Network errors
    if (error.code === 'ECONNABORTED' || error.message === 'Network Error') {
      return new Error('Connection lost. Please check your internet connection.');
    }

    // Timeout errors
    if (error.code === 'ETIMEDOUT') {
      return new Error('Request timed out. Please try again.');
    }

    if (error.message) {
      return new Error(error.message);
    }

    return new Error('An unexpected error occurred');
  }

  /**
   * Check if error is transient and should be retried
   */
  private isTransientError(error: any): boolean {
    // Network errors
    if (error.code === 'ECONNABORTED' || error.message === 'Network Error') {
      return true;
    }

    // Timeout errors
    if (error.code === 'ETIMEDOUT') {
      return true;
    }

    // 5xx server errors
    if (error.response?.status >= 500) {
      return true;
    }

    return false;
  }

  /**
   * Sleep utility for retry delays
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export const chatService = new ChatService();
