<!--
name: 'Data: Agent SDK patterns — TypeScript'
description: >-
  TypeScript Agent SDK patterns including basic agents, hooks, subagents, and
  MCP integration
ccVersion: 2.1.71
-->
# Agent SDK Patterns — TypeScript

## Basic Agent

\`\`\`typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  for await (const message of query({
    prompt: "Explain this repository",
    options: { cwd: "/path/to/project", allowedTools: ["Read", "Glob", "Grep"] },
  })) {
    if ("result" in message) console.log(message.result);
  }
}
main();
\`\`\`

## Hooks

\`\`\`typescript
import { query, HookCallback } from "@anthropic-ai/claude-agent-sdk";
import { appendFileSync } from "fs";

const logFileChange: HookCallback = async (input) => {
  const filePath = (input as any).tool_input?.file_path ?? "unknown";
  appendFileSync("./audit.log", \`\${new Date().toISOString()}: modified \${filePath}\n\`);
  return {};
};

for await (const message of query({
  prompt: "Refactor utils.py",
  options: {
    allowedTools: ["Read", "Edit", "Write"],
    permissionMode: "acceptEdits",
    hooks: { PostToolUse: [{ matcher: "Edit|Write", hooks: [logFileChange] }] },
  },
})) {
  if ("result" in message) console.log(message.result);
}
\`\`\`

## Subagents

\`\`\`typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use code-reviewer agent",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Agent"],
    agents: {
      "code-reviewer": {
        description: "Expert code reviewer.",
        prompt: "Analyze code quality.",
        tools: ["Read", "Glob", "Grep"],
      },
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
\`\`\`

## MCP Server Integration

\`\`\`typescript
for await (const message of query({
  prompt: "Open example.com",
  options: {
    mcpServers: { playwright: { command: "npx", args: ["@playwright/mcp@latest"] } },
  },
})) {
  if ("result" in message) console.log(message.result);
}
\`\`\`

## Session Resumption

\`\`\`typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionId: string | undefined;

for await (const message of query({
  prompt: "Read auth module",
  options: { allowedTools: ["Read", "Glob"] },
})) {
  if (message.type === "system" && message.subtype === "init") sessionId = message.session_id;
}

for await (const message of query({
  prompt: "Find callers",
  options: { resume: sessionId },
})) {
  if ("result" in message) console.log(message.result);
}
\`\`\`

## Session History

\`\`\`typescript
import { listSessions, getSessionMessages } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  const sessions = await listSessions();
  if (sessions.length > 0) {
    const messages = await getSessionMessages(sessions[0].sessionId, { limit: 50 });
    for (const msg of messages) console.log(msg);
  }
}
main();
\`\`\`

## Custom System Prompt

\`\`\`typescript
for await (const message of query({
  prompt: "Review this code",
  options: {
    allowedTools: ["Read", "Glob", "Grep"],
    systemPrompt: \`You are a senior code reviewer...\`,
  },
})) {
  if ("result" in message) console.log(message.result);
}
\`\`\`