# Implementation Plan: Phase III – Part B: AI Agent & Chat Orchestration

## Technical Context

This plan implements an AI agent that interprets natural language todo commands, selects appropriate MCP tools, and confirms actions clearly to the user. The agent operates statelessly, reconstructing conversation context from the database per request and only acting via the 5 MCP tools (add_task, list_tasks, update_task, complete_task, delete_task).

**Key Dependencies:**
- MCP tools from Phase III Part A (completed and available)
- Backend uses FastAPI framework
- OpenAI Agents SDK for implementation
- Google Gemini models via OpenAI-compatible API
- Existing authentication system (Better Auth)
- SQLModel with Neon PostgreSQL for database operations

**Technical Constraints:**
- Agent must operate statelessly (no server-side session storage)
- Only MCP tools may be used for data operations
- All operations must pass through authentication validation
- Conversation context must be reconstructed from database per request
- All tool calls must be logged for audit trail
- Agent behavior must be deterministic and auditable

## Constitution Check

### Principles Adherence:
- ✅ **Principle IX (Stateless AI Architecture)**: Plan ensures conversation context is reconstructed from database per request, no server-side state maintained
- ✅ **Principle X (MCP-First AI Design)**: Plan restricts agent to only use MCP tools for data operations
- ✅ **Principle XI (Tool-Driven Intelligence)**: Plan ensures all task mutations correspond to explicit MCP tool calls
- ✅ **Principle XII (Safety & Determinism)**: Plan includes deterministic behavior and explicit success/failure states

### Scope Verification:
- ✅ **In Scope**: AI-powered conversational interface for todo management, MCP-first AI tool integration
- ✅ **Out of Scope**: Direct database access from AI agents, client-side AI processing

## Gates

### Gate 1: Architecture Compatibility
✅ MCP tools from Part A are available and tested
✅ OpenAI Agents SDK can be integrated with FastAPI backend
✅ Google Gemini integration via OpenAI-compatible API is feasible

### Gate 2: Technical Feasibility
✅ Stateless architecture achievable with database-reconstructed context
✅ Authentication system compatible with AI agent requests
✅ Tool call logging can be implemented with audit trail

### Gate 3: Constraint Compliance
✅ Agent will use only MCP tools (no direct database access)
✅ Conversation context will be reconstructed from database per request
✅ All operations will maintain user isolation

## Phase 0: Research & Resolution

### Research Tasks:
- **R1**: Investigate OpenAI Agents SDK integration with FastAPI backend for stateless operation
- **R2**: Research Google Gemini integration via OpenAI-compatible API patterns
- **R3**: Study best practices for reconstructing conversation context from database
- **R4**: Examine tool call logging patterns for audit trails
- **R5**: Review user authentication validation in AI agent requests

### Expected Outcomes:
- Confirmed integration patterns for OpenAI Agents SDK with FastAPI
- Verified Google Gemini API compatibility
- Defined conversation context reconstruction methodology
- Established tool call logging mechanism
- Confirmed authentication flow for AI requests

## Phase 1: Design & Architecture

### 1.1 Data Model Design

#### AI Agent Session Context
```
Entity: AISessionContext
- user_id (UUID) - Foreign key to user
- messages (JSON) - Conversation history stored as message objects
- created_at (DateTime) - Timestamp of session creation
- last_accessed_at (DateTime) - Last interaction timestamp
- metadata (JSON) - Additional context information

Entity: ToolCallLog
- id (UUID) - Unique identifier
- user_id (UUID) - Foreign key to user
- session_id (UUID) - Session identifier
- tool_name (String) - Name of the MCP tool called
- tool_params (JSON) - Parameters passed to the tool
- result (JSON) - Result returned from the tool
- timestamp (DateTime) - When the tool was called
- status (Enum) - success/error/pending
- error_details (JSON, optional) - Error information if applicable
```

### 1.2 System Architecture Components

#### Component 1: AI Agent Service
- Responsible for processing natural language input
- Maps user intent to appropriate MCP tools
- Handles conversation context reconstruction
- Manages user confirmation flows
- Logs all tool calls for audit trail

#### Component 2: Context Reconstruction Module
- Fetches user's conversation history from database
- Builds context for AI agent on each request
- Ensures stateless operation without server-side storage

#### Component 3: MCP Tool Orchestrator
- Validates user permissions for each tool call
- Executes appropriate MCP tool based on agent decision
- Returns results to AI agent for user feedback
- Ensures all operations go through MCP tools only

#### Component 4: Audit Logging Service
- Captures all tool calls made by AI agent
- Stores tool call metadata for audit purposes
- Maintains tamper-evident logs of AI actions

### 1.3 API Contract Design

#### Agent Endpoint
```
POST /api/ai/chat
Authentication: Bearer token required
Content-Type: application/json

Request Body:
{
  "user_id": "uuid-string",
  "message": "natural language command",
  "context": { // optional, for advanced scenarios
    "conversation_id": "optional session identifier",
    "previous_messages": [...]
  }
}

Response:
{
  "status": "success|error",
  "response": "ai-generated response to user",
  "tool_calls": [
    {
      "tool_name": "add_task|list_tasks|update_task|complete_task|delete_task",
      "params": {...},
      "result": {...}
    }
  ],
  "requires_confirmation": boolean,
  "next_message": "optional follow-up message"
}
```

### 1.4 Implementation Architecture

#### Directory Structure
```
Phase-3-todo-ai-chatbot/
├── backend/
│   ├── src/
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── agent_service.py          # Main AI agent service
│   │   │   ├── context_reconstructor.py  # Conversation context reconstruction
│   │   │   ├── tool_orchestrator.py      # MCP tool orchestration
│   │   │   └── audit_logger.py           # Tool call logging
│   │   ├── mcp/
│   │   │   └── (existing MCP components from Part A)
│   │   └── services/
│   │       └── (existing services)
└── frontend/
    └── (existing frontend)
```

## Phase 2: Implementation Plan

### 2.1 Development Environment Setup
- Set up Google Gemini API access via OpenAI-compatible endpoint
- Install OpenAI Agents SDK dependencies
- Configure environment variables for AI provider
- Integrate with existing authentication system

### 2.2 Core AI Agent Service
- Implement OpenAI Agents SDK integration with FastAPI
- Create agent that maps natural language to MCP tools
- Add Google Gemini model integration
- Implement tool calling patterns for the 5 MCP tools

### 2.3 Context Reconstruction
- Create module to fetch conversation history from database
- Implement stateless context building per request
- Handle conversation history serialization/deserialization

### 2.4 Tool Orchestration
- Develop orchestrator that validates user permissions
- Connect to existing MCP tools from Part A
- Ensure all operations pass through MCP layer
- Implement user isolation mechanisms

### 2.5 Audit Logging
- Create logging service for all tool calls
- Store tool call metadata with timestamps
- Ensure logs are tamper-evident and searchable

### 2.6 Confirmation Flows
- Implement user confirmation for destructive operations
- Create confirmation patterns for delete_task operations
- Add safety checks for critical operations

### 2.7 Error Handling
- Implement graceful error handling for API failures
- Create user-friendly error messages
- Add retry mechanisms for transient failures

### 2.8 Security & Validation
- Ensure all requests are properly authenticated
- Validate user permissions for each operation
- Implement rate limiting for AI requests
- Add input sanitization for security

## Phase 3: Testing Strategy

### 3.1 Unit Tests
- Test AI agent decision-making logic
- Test context reconstruction functionality
- Test tool call orchestration
- Test audit logging mechanisms

### 3.2 Integration Tests
- End-to-end conversation flow testing
- MCP tool integration verification
- Authentication flow validation
- Audit trail completeness verification

### 3.3 Functional Tests
- Natural language command interpretation
- Proper tool selection based on intent
- Confirmation prompting for destructive operations
- Error handling and recovery

### 3.4 Performance Tests
- Response time validation (target: <3s)
- Concurrent session handling
- Database query optimization
- API rate limiting effectiveness

## Phase 4: Quality Assurance

### 4.1 Code Quality
- Static analysis and linting
- Type checking compliance
- Security scanning
- Performance profiling

### 4.2 Architecture Validation
- Stateless operation verification
- MCP-first design compliance
- User isolation validation
- Audit trail completeness

### 4.3 Security Review
- Authentication validation
- Authorization verification
- Input sanitization checks
- Rate limiting effectiveness

## Success Criteria Verification

### Functional Requirements Met:
- [ ] R1: Natural Language Processing - AI agent interprets commands
- [ ] R2: MCP Tool Integration - Only MCP tools used for operations
- [ ] R3: Conversation Context Reconstruction - Context rebuilt per request
- [ ] R4: Tool Call Logging - All calls logged with metadata
- [ ] R5: Deterministic Behavior - Consistent responses for identical inputs
- [ ] R6: User Confirmation - Destructive operations confirmed
- [ ] R7: Error Handling - Graceful error handling implemented
- [ ] R8: Google Gemini Integration - Proper API integration

### Non-Functional Requirements Met:
- [ ] Performance - Response times under 3 seconds
- [ ] Security - User isolation maintained
- [ ] Reliability - Graceful degradation implemented

### Quality Measures:
- [ ] 90% of natural language commands correctly mapped to tools
- [ ] Under 3 seconds average response time
- [ ] 99% uptime for chat interface
- [ ] 100% of tool calls successfully logged

## Risk Mitigation

### Technical Risks:
- **API Limitations**: Google Gemini may have different capabilities than OpenAI - mitigation through thorough testing
- **Rate Limits**: AI provider may impose strict limits - mitigation through caching and request optimization
- **Context Length**: Conversation history may exceed model limits - mitigation through smart truncation

### Operational Risks:
- **Security**: AI may generate unsafe content - mitigation through content filtering
- **Performance**: Slow response times may affect user experience - mitigation through optimization
- **Reliability**: API outages may affect service availability - mitigation through fallbacks

## Deployment Strategy

### Staging Deployment:
1. Deploy to staging environment
2. Perform comprehensive testing
3. Validate with sample conversations
4. Verify audit logs

### Production Deployment:
1. Deploy to production environment
2. Monitor initial usage
3. Validate all functionality
4. Monitor performance metrics