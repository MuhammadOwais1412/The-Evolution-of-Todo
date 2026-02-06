# Research: MCP Server & Tool Layer

## MCP SDK Integration Research

### Decision: MCP SDK Selection and Setup
**Rationale**: Need to establish the correct SDK to implement the Model Context Protocol server that will expose our todo operations as tools.

**Details**:
- Anthropic MCP SDK is the official implementation for creating MCP servers
- MCP servers allow AI agents to access tools hosted on external services
- The SDK provides server setup, tool registration, and communication protocols
- Implementation requires defining tools with specific input/output schemas

**Alternatives considered**:
- Building custom API endpoints: Would not be MCP-compliant and wouldn't integrate with AI agents properly
- Third-party MCP implementations: Less reliable than official SDK

## Authentication Flow Analysis

### Decision: JWT Token Integration with MCP Tools
**Rationale**: The system must maintain security and user isolation while operating in a stateless manner.

**Details**:
- Better Auth provides JWT tokens that must be validated in MCP tools
- Each MCP tool call must include user authentication context
- Since the server must be stateless, authentication must be validated per request
- User_id must be passed as a parameter to ensure data isolation
- JWT validation can be implemented as a decorator or middleware function

**Alternatives considered**:
- Session-based authentication: Contradicts stateless architecture requirement
- Separate authentication service: Adds complexity without clear benefits

## Database Operation Patterns

### Decision: Stateless Database Operations
**Rationale**: The server must remain stateless while maintaining data persistence and integrity.

**Details**:
- Each MCP tool call establishes a fresh database connection
- Operations use SQLModel ORM with Neon PostgreSQL
- Transaction boundaries are defined per tool operation
- No caching or session state is maintained on the server
- Connection pooling can be managed by the database adapter

**Alternatives considered**:
- Server-side caching: Violates stateless architecture requirement
- Persistent connections: Still maintains stateless operations per request while optimizing performance