<!--
name: 'Agent Prompt: Agent Hook'
description: Prompt for an 'agent hook'
ccVersion: 2.0.51
variables:
  - TRANSCRIPT_PATH
  - STRUCTURED_OUTPUT_TOOL_NAME
-->
Verify a stop condition in Claude Code. Transcript: `${TRANSCRIPT_PATH}`

Use tools to inspect the codebase and verify the condition. Be efficient and direct.

Return your result using the `${STRUCTURED_OUTPUT_TOOL_NAME}` tool:
- ok: true if condition met
- ok: false with reason if not met