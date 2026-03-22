<!--
name: 'Data: Agent SDK reference — TypeScript'
description: >-
  TypeScript Agent SDK reference including installation, quick start, custom
  tools, and hooks
ccVersion: 2.1.71
-->
# Agent SDK — TypeScript

## Installation
\`\`\`bash
npm install @anthropic-ai/claude-agent-sdk
\`\`\`

## Quick Start
\`\`\`typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Explain this codebase",
  options: { allowedTools: ["Read", "Glob", "Grep"] },
})) {
  if ("result" in message) console.log(message.result);
}
\`\`\`

## Built-in Tools
\`Read\`, \`Write\`, \`Edit\`, \`Bash\`, \`Glob\`, \`Grep\`, \`WebSearch\`, \`WebFetch\`, \`AskUserQuestion\`, \`Agent\`.

## Permission System
- \`"default"\`: Prompt for dangerous operations
- \`"acceptEdits"\`: Auto-accept file edits
- \`"dontAsk"\`: CI/CD mode
- \`"bypassPermissions"\`: Skip all prompts (\`allowDangerouslySkipPermissions: true\` required)

## Custom MCP Tools (In-Process)
\`\`\`typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const myTool = tool("my-tool", "Desc", { input: z.string() }, async (args) => {
  return { content: [{ type: "text", text: "result" }] };
});

const server = createSdkMcpServer({ name: "my-server", tools: [myTool] });
\`\`\`

## Hooks
Event inputs include \`agent_id\` and \`agent_type\`.
Events: \`PreToolUse\`, \`PostToolUse\`, \`PostToolUseFailure\`, \`Notification\`, \`UserPromptSubmit\`, \`SessionStart\`, \`SessionEnd\`, \`Stop\`, \`SubagentStart\`, \`SubagentStop\`, \`PreCompact\`, \`PermissionRequest\`, \`Setup\`, \`TeammateIdle\`, \`TaskCompleted\`, \`ConfigChange\`.

## Common Options
- \`cwd\`: Working directory
- \`allowedTools\`: Array of allowed tools
- \`permissionMode\`: Permission handling string
- \`mcpServers\`: MCP server configs
- \`maxTurns\`: Max loops
- \`model\`: Model ID
- \`agents\`: Record of subagent definitions

## Session History
\`\`\`typescript
import { listSessions, getSessionMessages } from "@anthropic-ai/claude-agent-sdk";
const sessions = await listSessions();
const messages = await getSessionMessages(sessionId, { limit: 50, offset: 0 });
\`\`\`

## MCP Server Management
Runtime management on a running query handle:
\`\`\`typescript
await queryHandle.reconnectMcpServer("my-server");
await queryHandle.toggleMcpServer("my-server");
const status = await queryHandle.mcpServerStatus();
\`\`\`
