<!--
name: 'Tool Description: SendMessageTool'
description: Tool for sending messages to teammates and handling protocol requests/responses in a swarm
ccVersion: 2.1.32
-->

# SendMessageTool

Team communication and protocol handling.

## Types

**message** - Send to specific teammate
- recipient, content, summary (5-10 words) required
- IMPORTANT: Plain text output NOT visible to team - MUST use this tool

**broadcast** - Send to ALL teammates
- WARNING: Expensive (N teammates = N messages)
- Use only for critical blocking issues or major announcements
- Default to "message" for normal communication

**shutdown_request** - Ask teammate to gracefully shut down
- recipient, content required

**shutdown_response** - MUST respond to shutdown requests
- Extract \`requestId\` from JSON, pass as \`request_id\`
- approve: true to exit, false to continue

**plan_approval_response** - Approve/reject teammate's plan
- Extract \`request_id\`, set approve true/false
- Optional content for rejection feedback

**Important:**
- Messages deliver automatically - don't manually check inbox
- Refer to teammates by NAME, not UUID
- Use TaskUpdate to mark tasks completed
