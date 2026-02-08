# Research Findings: AI Agent & Chat Orchestration

## R1: OpenAI Agents SDK Integration with FastAPI

**Decision**: Use OpenAI Assistant API for the AI agent functionality
**Rationale**: The OpenAI Assistant API provides a stateless way to create AI agents that can call tools. Combined with FastAPI, we can create an endpoint that handles each request independently without storing conversation state on the server.
**Alternatives considered**:
- LangChain Agents: More complex and requires state management
- OpenAI Functions: Limited compared to Assistant API's capabilities
- Self-hosted models: Would require more infrastructure and maintenance

## R2: Google Gemini Integration via OpenAI-Compatible API

**Decision**: Use a reverse proxy approach to connect to Google Gemini through an OpenAI-compatible API
**Rationale**: Google provides Vertex AI and Gemini API options. The Gemini API can be accessed through an OpenAI-compatible proxy like vellum-ai/gemini-openai-proxy or similar solutions.
**Alternatives considered**:
- Direct Gemini API calls: Would require changing the entire tool architecture
- OpenAI-compatible proxy services: Requires additional infrastructure but provides flexibility
- Gemini SDK directly: Would violate the MCP-first principle

## R3: Conversation Context Reconstruction Patterns

**Decision**: Fetch conversation history from the database on each request and construct the context using message history
**Rationale**: To maintain stateless architecture, we'll query the database for the user's recent conversation history and build the context dynamically. This avoids server-side state storage while providing the AI agent with necessary context.
**Alternatives considered**:
- Storing context in session/database per session: Would violate stateless principle
- Passing entire context in request: Could exceed payload limits
- Summarizing context: Would lose important details

## R4: Tool Call Logging Mechanisms

**Decision**: Create a ToolCallLog entity that records all AI-initiated tool calls with comprehensive metadata
**Rationale**: Each tool call made by the AI agent will be logged with user_id, tool_name, parameters, results, and timestamp to ensure full auditability.
**Alternatives considered**:
- Using standard application logs: Less structured and harder to query
- Database triggers: Would add complexity
- Separate logging service: Overkill for this use case

## R5: User Authentication in AI Agent Requests

**Decision**: Use JWT token validation in the API endpoint before processing any AI requests
**Rationale**: Follow the same authentication pattern as other API endpoints in the application, validating the JWT token from Better Auth before processing any AI requests.
**Alternatives considered**:
- Custom authentication scheme: Would add unnecessary complexity
- Session-based auth: Would violate stateless principle
- API keys: Would require additional infrastructure

## Additional Research: MCP Tool Integration Pattern

**Decision**: Create a wrapper that connects OpenAI Assistant tools to our existing MCP tools
**Rationale**: The OpenAI Assistant expects functions with specific signatures, but our MCP tools have different interfaces. We'll create adapters that map between the two systems while maintaining the MCP-first architecture.
**Implementation approach**:
1. Define OpenAI-compatible function schemas that correspond to MCP tools
2. Create wrapper functions that call the MCP tools with validated parameters
3. Return results in the expected format for the AI agent

## Technical Feasibility Confirmation

All components have been confirmed as technically feasible:
- ✅ OpenAI Assistant API works with FastAPI
- ✅ Google Gemini can be accessed via OpenAI-compatible proxy
- ✅ Database context reconstruction is achievable
- ✅ Tool call logging can be implemented
- ✅ JWT authentication validation is compatible
- ✅ MCP tool integration via adapters is possible