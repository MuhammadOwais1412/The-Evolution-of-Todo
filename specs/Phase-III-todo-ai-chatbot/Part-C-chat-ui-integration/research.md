# Research: Chat UI & End-to-End Integration

**Feature**: Phase III – Part C: Chat UI & End-to-End Integration
**Date**: 2026-02-12
**Status**: Complete

## Overview

This document consolidates research findings for integrating a chat UI with the existing AI Agent (Part B). All research questions from the plan have been investigated and decisions documented.

---

## 1. OpenAI ChatKit Integration with Next.js

### Decision
Use custom React components instead of OpenAI ChatKit for the chat interface.

### Rationale
After evaluating ChatKit (version 1.6.0), we discovered it requires backend protocol conformance:
- ChatKit requires implementing `chatkit.server.ChatKitServer` protocol on the backend
- Backend must use thread-based architecture and streaming event protocol
- Our existing backend (FastAPI with custom AI Agent from Part B) uses a different architecture
- Rewriting the backend to conform to ChatKit protocol would require:
  - Changing from conversation-based to thread-based data models
  - Implementing ChatKit's streaming event protocol
  - Restructuring endpoints to match ChatKit's expectations
  - Significant rework of Part B integration (~8-10 hours)
- Custom components provide simpler, more direct integration with our existing backend
- Full control over UI/UX without protocol constraints
- Easier to maintain and debug

### Alternatives Considered

1. **OpenAI ChatKit (Evaluated but Rejected)**
   - Pros: Pre-built, accessible chat UI components optimized for AI interactions
   - Cons: Requires backend protocol conformance, significant rework of existing architecture
   - Rejected: Protocol requirements incompatible with our custom backend design

2. **Custom Chat UI Components (Selected)**
   - Pros: Full control, direct integration with existing backend, simpler architecture
   - Cons: Need to implement UI patterns ourselves
   - Selected: Best fit for our custom backend and existing AI Agent integration

3. **Other Chat Libraries (react-chat-elements, stream-chat-react)**
   - Pros: Mature, feature-rich
   - Cons: Designed for multi-user chat, not AI interactions; heavier than needed
   - Rejected: Over-engineered for single-user AI chat use case

### Implementation Notes

**Installation**:
```bash
# ChatKit package installed for type definitions only
npm install @openai/chatkit
```

**Custom Components Created**:
- `MessageList.tsx` - Displays chat messages with auto-scroll
- `MessageInput.tsx` - Input field with character limit and multi-line support
- `ChatInterface.tsx` - Main container with error handling
- `useChat.ts` - Custom hook for state management and API integration
- `chatService.ts` - API client with retry logic

**Key Features**:
- Optimistic UI updates for immediate feedback
- Auto-scroll to latest messages
- Loading indicators and typing animations
- Error handling with user-friendly messages
- Retry logic with exponential backoff
- Character limit validation (1000 chars)
- Multi-line text support
- Responsive design for mobile and desktop

---

## 2. JWT Token Management in Chat Context

### Decision
Use Better Auth client SDK to automatically attach JWT tokens to all API requests via axios interceptor.

### Rationale
- Better Auth already manages token lifecycle (issuance, refresh, expiration)
- Interceptor pattern ensures tokens are always included without manual intervention
- Centralized error handling for authentication failures
- Automatic token refresh on expiration (if Better Auth supports it)
- Follows existing authentication patterns from Phase II

### Alternatives Considered

1. **Manual Token Attachment per Request**
   - Pros: Simple, explicit
   - Cons: Error-prone, repetitive, easy to forget
   - Rejected: Violates DRY principle, increases maintenance burden

2. **Context API for Token Storage**
   - Pros: React-native approach
   - Cons: Requires manual token refresh logic, more complex state management
   - Rejected: Better Auth already handles this

3. **Server-Side Token Management (cookies)**
   - Pros: More secure (httpOnly cookies)
   - Cons: Requires backend changes, complicates API design
   - Rejected: Better Auth uses JWT in headers (existing pattern)

### Implementation Notes

**Axios Interceptor Setup**:
```typescript
// src/services/chatService.ts
import axios from 'axios';
import { auth } from '@/lib/auth-client'; // Better Auth client

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  async (config) => {
    const session = await auth.getSession();
    if (session?.token) {
      config.headers.Authorization = `Bearer ${session.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for auth errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**Token Expiration Handling**:
- Better Auth handles token refresh automatically
- If token expires during chat, 401 response triggers redirect to login
- User sees friendly message: "Your session has expired. Please log in again."
- Conversation persists in database, user can resume after re-authentication

---

## 3. Conversation Persistence Patterns

### Decision
Use two-table schema (Conversation + Message) with indexed queries and pagination for efficient history retrieval.

### Rationale
- Separates conversation metadata from message content (normalized design)
- Enables efficient querying by user_id (find all conversations) and conversation_id (find all messages)
- Supports pagination for large conversation histories
- Indexes on foreign keys and timestamps ensure fast queries
- Follows standard chat application database patterns

### Alternatives Considered

1. **Single Table (Denormalized)**
   - Pros: Simpler schema, fewer joins
   - Cons: Data duplication (user_id repeated for every message), harder to query conversation metadata
   - Rejected: Violates normalization principles, inefficient storage

2. **Document Store (JSON column)**
   - Pros: Flexible schema, all messages in one document
   - Cons: Difficult to query individual messages, poor performance for large conversations, no relational integrity
   - Rejected: PostgreSQL is relational database, not optimized for document storage

3. **Event Sourcing Pattern**
   - Pros: Complete audit trail, time-travel capabilities
   - Cons: Over-engineered for this use case, complex to implement
   - Rejected: Violates "smallest viable change" principle

### Implementation Notes

**Database Schema**:

```python
# models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")

# models/message.py
from sqlmodel import SQLModel, Field, Relationship, Enum
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
import enum

class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(Enum(MessageRole)))
    content: str = Field(max_length=10000)  # Allow longer for assistant responses
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")
```

**Indexes**:
- `conversations.user_id` - for finding user's conversations
- `messages.conversation_id` - for finding conversation's messages
- `messages.timestamp` - for ordering messages chronologically
- Composite index on `(conversation_id, timestamp)` for efficient pagination

**Query Patterns**:
```python
# Get user's conversations
conversations = await session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
).all()

# Get conversation messages with pagination
messages = await session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.timestamp.asc())
    .offset(offset)
    .limit(limit)
).all()
```

---

## 4. Real-time UI Updates

### Decision
Use optimistic UI updates for user messages with rollback on error, and loading states for AI responses.

### Rationale
- Optimistic updates provide immediate feedback, improving perceived performance
- Loading indicators set clear expectations during AI processing
- Error recovery with retry maintains user control
- Auto-scroll ensures latest messages are visible
- Follows modern chat application UX patterns

### Alternatives Considered

1. **Wait for Server Confirmation Before Displaying**
   - Pros: Simpler, no rollback logic needed
   - Cons: Feels slow, poor user experience
   - Rejected: Violates "immediate visual feedback" UX standard from constitution

2. **WebSocket for Real-time Updates**
   - Pros: True real-time, bidirectional communication
   - Cons: Adds complexity, requires WebSocket server, overkill for single-user chat
   - Rejected: HTTP polling sufficient for this use case, violates "smallest viable change"

3. **Server-Sent Events (SSE)**
   - Pros: Simpler than WebSocket, good for streaming AI responses
   - Cons: One-way only, requires server changes
   - Rejected: Not needed for current requirements, can add later if streaming responses desired

### Implementation Notes

**Optimistic Update Pattern**:
```typescript
// hooks/useChat.ts
const sendMessage = async (content: string) => {
  // 1. Optimistically add user message to UI
  const tempMessage = {
    id: `temp-${Date.now()}`,
    role: 'user',
    content,
    timestamp: new Date().toISOString(),
  };
  setMessages(prev => [...prev, tempMessage]);

  // 2. Show loading indicator
  setIsLoading(true);

  try {
    // 3. Send to server
    const response = await chatService.sendMessage(userId, {
      message: content,
      conversation_id: conversationId,
    });

    // 4. Replace temp message with server response
    setMessages(prev => [
      ...prev.filter(m => m.id !== tempMessage.id),
      {
        id: response.message_id,
        role: 'user',
        content,
        timestamp: response.timestamp,
      },
      {
        id: response.message_id + '-assistant',
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
      },
    ]);

    // 5. Update conversation ID if new
    if (!conversationId) {
      setConversationId(response.conversation_id);
    }
  } catch (error) {
    // 6. Rollback on error
    setMessages(prev => prev.filter(m => m.id !== tempMessage.id));
    setError('Failed to send message. Please try again.');
  } finally {
    setIsLoading(false);
  }
};
```

**Auto-scroll Implementation**:
```typescript
// Scroll to bottom when new messages arrive
useEffect(() => {
  if (messagesEndRef.current) {
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
  }
}, [messages]);
```

**Loading States**:
- User message: Show immediately (optimistic)
- AI processing: Show typing indicator
- Network request: Show "Sending..." on message
- Error: Show error message with retry button

---

## 5. Chat-Specific Error Handling

### Decision
Implement tiered error handling with user-friendly messages, automatic retry for transient errors, and graceful degradation.

### Rationale
- Users should never see technical error messages
- Different error types require different handling strategies
- Transient errors (network issues) should retry automatically
- Permanent errors (authentication) should redirect or prompt user action
- Error messages should be actionable and clear

### Alternatives Considered

1. **Generic Error Messages**
   - Pros: Simple to implement
   - Cons: Unhelpful to users, doesn't guide recovery
   - Rejected: Violates UX standards from constitution

2. **Technical Error Messages**
   - Pros: Useful for debugging
   - Cons: Confusing for users, may leak sensitive information
   - Rejected: Security and UX concerns

3. **Silent Failures**
   - Pros: Doesn't interrupt user flow
   - Cons: User doesn't know what happened, can't recover
   - Rejected: Explicitly forbidden by constitution (Principle XII)

### Implementation Notes

**Error Classification**:

```typescript
// services/chatService.ts
enum ErrorType {
  AUTHENTICATION = 'AUTH_FAILED',
  AUTHORIZATION = 'UNAUTHORIZED',
  RATE_LIMIT = 'RATE_LIMIT',
  INVALID_INPUT = 'INVALID_INPUT',
  AI_ERROR = 'AI_ERROR',
  DATABASE_ERROR = 'DATABASE_ERROR',
  NETWORK_ERROR = 'NETWORK_ERROR',
  TIMEOUT = 'TIMEOUT',
}

const ERROR_MESSAGES: Record<ErrorType, string> = {
  [ErrorType.AUTHENTICATION]: 'Your session has expired. Please log in again.',
  [ErrorType.AUTHORIZATION]: 'You do not have permission to access this conversation.',
  [ErrorType.RATE_LIMIT]: 'You are sending messages too quickly. Please wait a moment.',
  [ErrorType.INVALID_INPUT]: 'Your message could not be processed. Please check and try again.',
  [ErrorType.AI_ERROR]: 'I encountered an error processing your request. Please try rephrasing or try again.',
  [ErrorType.DATABASE_ERROR]: 'Service temporarily unavailable. Please try again later.',
  [ErrorType.NETWORK_ERROR]: 'Connection lost. Retrying...',
  [ErrorType.TIMEOUT]: 'Request timed out. Please try again.',
};
```

**Error Handling Strategy**:

| Error Type | Strategy | User Action |
|------------|----------|-------------|
| Authentication | Redirect to login | Re-authenticate |
| Authorization | Show error, redirect | Contact support |
| Rate Limit | Show countdown, disable input | Wait |
| Invalid Input | Show validation error | Fix input |
| AI Error | Show error, enable retry | Retry or rephrase |
| Database Error | Show error, enable retry | Retry later |
| Network Error | Auto-retry (3x), then manual | Wait or retry |
| Timeout | Show error, enable retry | Retry |

**Retry Logic**:
```typescript
const sendMessageWithRetry = async (
  message: string,
  maxRetries = 3
): Promise<ChatResponse> => {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await chatService.sendMessage(userId, { message });
    } catch (error) {
      lastError = error;

      // Only retry transient errors
      if (isTransientError(error)) {
        const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
        await sleep(delay);
        continue;
      }

      // Non-transient errors fail immediately
      throw error;
    }
  }

  throw lastError;
};

const isTransientError = (error: any): boolean => {
  return [
    ErrorType.NETWORK_ERROR,
    ErrorType.TIMEOUT,
    ErrorType.DATABASE_ERROR,
  ].includes(error.code);
};
```

**Error Display**:
- Inline errors: Show in chat as system messages
- Toast notifications: For transient errors that auto-dismiss
- Modal dialogs: For critical errors requiring user action
- Input validation: Show below input field

---

## Summary of Decisions

| Research Area | Decision | Key Benefit |
|---------------|----------|-------------|
| Chat UI Library | OpenAI ChatKit | Pre-built, accessible, AI-optimized components |
| Token Management | Better Auth + Axios Interceptor | Automatic, centralized, follows existing patterns |
| Data Persistence | Two-table schema with indexes | Efficient queries, normalized design |
| UI Updates | Optimistic updates + loading states | Immediate feedback, clear expectations |
| Error Handling | Tiered strategy with user-friendly messages | Clear guidance, automatic recovery |

---

## Implementation Readiness

All research questions have been resolved. The following artifacts are ready for Phase 1:

- ✅ Technology choices validated
- ✅ Integration patterns defined
- ✅ Database schema designed
- ✅ Error handling strategy established
- ✅ UX patterns documented

**Next Step**: Proceed to Phase 1 (Design & Contracts) to generate:
- `data-model.md`
- `contracts/chat-endpoint.json`
- `contracts/conversation-history-endpoint.json`
- `quickstart.md`
