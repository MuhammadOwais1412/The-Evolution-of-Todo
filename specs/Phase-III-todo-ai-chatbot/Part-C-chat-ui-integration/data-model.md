# Data Model: Chat UI & End-to-End Integration

**Feature**: Phase III – Part C: Chat UI & End-to-End Integration
**Date**: 2026-02-12
**Status**: Complete

## Overview

This document defines the database schema for conversation and message persistence. The design follows normalized relational patterns with efficient indexing for query performance.

---

## Entity Definitions

### 1. Conversation

**Purpose**: Represents a chat session between a user and the AI agent.

**Table Name**: `conversations`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the conversation |
| user_id | VARCHAR(255) | FOREIGN KEY (users.id), NOT NULL, INDEX | Reference to the user who owns this conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When the conversation was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When the conversation was last updated (new message added) |

**Indexes**:
- Primary key on `id`
- Index on `user_id` for efficient user conversation queries
- Index on `updated_at` for sorting by most recent activity

**Relationships**:
- One-to-many with Message (one conversation has many messages)
- Many-to-one with User (many conversations belong to one user)

**Validation Rules**:
- `user_id` must reference an existing user in the `users` table
- `created_at` cannot be modified after creation
- `updated_at` automatically updates when messages are added

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

---

### 2. Message

**Purpose**: Represents an individual message within a conversation (either from user or AI assistant).

**Table Name**: `messages`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the message |
| conversation_id | UUID | FOREIGN KEY (conversations.id), NOT NULL, INDEX | Reference to the parent conversation |
| role | ENUM('user', 'assistant') | NOT NULL | Who sent the message (user or AI assistant) |
| content | TEXT | NOT NULL | The message content (max 10000 chars) |
| timestamp | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEX | When the message was created |
| metadata | JSON | NULLABLE | Optional metadata (e.g., tool calls, confirmation status) |

**Indexes**:
- Primary key on `id`
- Index on `conversation_id` for efficient conversation message queries
- Index on `timestamp` for chronological ordering
- Composite index on `(conversation_id, timestamp)` for optimized pagination queries

**Relationships**:
- Many-to-one with Conversation (many messages belong to one conversation)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `role` must be either 'user' or 'assistant'
- `content` cannot be empty
- `content` max length: 1000 characters for user messages, 10000 for assistant messages
- `timestamp` cannot be modified after creation
- `metadata` must be valid JSON if provided

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Enum as SQLEnum, JSON
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
import enum

class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        index=True,
        nullable=False
    )
    role: MessageRole = Field(
        sa_column=Column(SQLEnum(MessageRole)),
        nullable=False
    )
    content: str = Field(nullable=False, max_length=10000)
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

---

## Relationships Diagram

```
┌─────────────────┐
│     User        │
│  (existing)     │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│  Conversation   │
│                 │
│  - id           │
│  - user_id (FK) │
│  - created_at   │
│  - updated_at   │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│    Message      │
│                 │
│  - id           │
│  - conv_id (FK) │
│  - role         │
│  - content      │
│  - timestamp    │
│  - metadata     │
└─────────────────┘
```

---

## Query Patterns

### 1. Get User's Conversations (Most Recent First)

```python
async def get_user_conversations(
    session: AsyncSession,
    user_id: str,
    limit: int = 20,
    offset: int = 0
) -> List[Conversation]:
    """Retrieve user's conversations ordered by most recent activity."""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(statement)
    return result.scalars().all()
```

**Performance**: O(log n) with index on `user_id` and `updated_at`

---

### 2. Get Conversation Messages (Chronological Order)

```python
async def get_conversation_messages(
    session: AsyncSession,
    conversation_id: UUID,
    limit: int = 50,
    offset: int = 0
) -> List[Message]:
    """Retrieve messages for a conversation in chronological order."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(statement)
    return result.scalars().all()
```

**Performance**: O(log n) with composite index on `(conversation_id, timestamp)`

---

### 3. Create New Conversation

```python
async def create_conversation(
    session: AsyncSession,
    user_id: str
) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation
```

**Performance**: O(1) insert operation

---

### 4. Add Message to Conversation

```python
async def add_message(
    session: AsyncSession,
    conversation_id: UUID,
    role: MessageRole,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Message:
    """Add a message to a conversation and update conversation timestamp."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        metadata=metadata
    )
    session.add(message)

    # Update conversation's updated_at timestamp
    conversation = await session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(message)
    return message
```

**Performance**: O(1) insert + O(1) update

---

### 5. Get Conversation with Message Count

```python
async def get_conversation_with_count(
    session: AsyncSession,
    conversation_id: UUID
) -> Tuple[Conversation, int]:
    """Get conversation and total message count."""
    conversation = await session.get(Conversation, conversation_id)

    count_statement = (
        select(func.count(Message.id))
        .where(Message.conversation_id == conversation_id)
    )
    result = await session.execute(count_statement)
    count = result.scalar()

    return conversation, count
```

**Performance**: O(1) for conversation lookup, O(n) for count (can be optimized with cached count)

---

## Migration Script

```python
"""Add conversation and message tables

Revision ID: 003_add_chat_tables
Revises: 002_add_ai_agent_tables
Create Date: 2026-02-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON, ENUM

# revision identifiers
revision = '003_add_chat_tables'
down_revision = '002_add_ai_agent_tables'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create message_role enum
    message_role_enum = ENUM('user', 'assistant', name='message_role', create_type=True)
    message_role_enum.create(op.get_bind(), checkfirst=True)

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create indexes for conversations
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', message_role_enum, nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('metadata', JSON(), nullable=True),
    )

    # Create indexes for messages
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('ix_messages_timestamp', 'messages', ['timestamp'])
    op.create_index('ix_messages_conversation_timestamp', 'messages', ['conversation_id', 'timestamp'])

def downgrade() -> None:
    # Drop tables
    op.drop_table('messages')
    op.drop_table('conversations')

    # Drop enum
    message_role_enum = ENUM('user', 'assistant', name='message_role')
    message_role_enum.drop(op.get_bind(), checkfirst=True)
```

---

## Data Integrity Constraints

### Foreign Key Constraints
- `conversations.user_id` → `users.id` (ON DELETE CASCADE)
- `messages.conversation_id` → `conversations.id` (ON DELETE CASCADE)

**Rationale**: When a user is deleted, all their conversations and messages should be deleted. When a conversation is deleted, all its messages should be deleted.

### Check Constraints
- `messages.content` length > 0 (no empty messages)
- `messages.role` IN ('user', 'assistant')

### Unique Constraints
None required (multiple conversations per user, multiple messages per conversation)

---

## Performance Considerations

### Index Strategy
1. **Primary Keys**: Clustered indexes on UUID primary keys
2. **Foreign Keys**: Non-clustered indexes on all foreign keys
3. **Sorting**: Index on `conversations.updated_at` for recent conversation queries
4. **Composite**: Index on `(conversation_id, timestamp)` for efficient message pagination

### Expected Query Performance
- Get user conversations: <50ms for 10k conversations
- Get conversation messages: <100ms for 1k messages
- Insert message: <10ms
- Update conversation timestamp: <5ms

### Scaling Considerations
- Partition messages table by timestamp if >10M messages
- Consider archiving old conversations (>1 year inactive)
- Monitor index size and rebuild if fragmented

---

## Security Considerations

### Data Access
- All queries must filter by `user_id` to enforce user isolation
- Never expose `conversation_id` without validating ownership
- Sanitize message content before storage (prevent XSS)

### Sensitive Data
- Message content may contain personal information
- Implement data retention policy (e.g., delete after 90 days)
- Consider encryption at rest for message content

---

## Testing Strategy

### Unit Tests
- Model validation (field constraints, relationships)
- Query functions (CRUD operations)
- Migration scripts (up and down)

### Integration Tests
- Multi-user isolation (user A cannot access user B's conversations)
- Cascade deletes (deleting conversation deletes messages)
- Concurrent message inserts (race conditions)

### Performance Tests
- Query performance with 10k conversations, 100k messages
- Index effectiveness (EXPLAIN ANALYZE)
- Concurrent user load (100 users)

---

## Summary

This data model provides:
- ✅ Normalized schema (no data duplication)
- ✅ Efficient queries (indexed foreign keys and timestamps)
- ✅ Data integrity (foreign key constraints, cascade deletes)
- ✅ Scalability (partition-ready design)
- ✅ Security (user isolation enforced at query level)

**Next Step**: Generate API contracts in `contracts/` directory.
