<!--
name: 'Data: Tool use concepts'
description: >-
  Conceptual foundations of tool use with the Claude API including tool
  definitions, tool choice, and best practices
ccVersion: 2.1.69
-->
# Tool Use Concepts

## Tool Runner vs Manual Loop
- **Tool Runner (Recommended)**: SDK handles loop, parsing, execution automatically.
- **Manual Loop**: Loop \`while (stop_reason != "end_turn")\`. Must append \`response.content\` and send back \`tool_result\` blocks.
- **pause_turn**: If a server-side tool loops too long, it hits \`pause_turn\`. Resend full history (including last assistant block) to resume.

## Server-Side Tools
- **Code Execution**: Fully sandboxed python container. Declare \`{"type": "code_execution_20260120"}\`.
- **Web Search/Fetch**: Declare \`{"type": "web_search_20260209"}\`. Includes dynamic filtering automatically.

## Structured Outputs
Constrain JSON responses.
- JSON Outputs (\`output_config.format\`)
- Strict Tools (\`strict: true\` in tool definition)

Avoid manual JSON schema definitions if SDK provides Zod/Pydantic parsers (\`client.messages.parse()\`).