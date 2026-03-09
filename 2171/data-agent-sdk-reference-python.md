<!--
name: 'Data: Agent SDK reference — Python'
description: >-
  Python Agent SDK reference including installation, quick start, custom tools
  via MCP, and hooks
ccVersion: 2.1.71
-->
# Agent SDK — Python

## Installation
```bash
pip install claude-agent-sdk
```

## Quick Start
```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="Explain this codebase",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
    ):
        if isinstance(message, ResultMessage): print(message.result)

anyio.run(main)
```

## Built-in Tools
`Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `WebSearch`, `WebFetch`, `AskUserQuestion`, `Agent`.

## Primary Interfaces

### `query()`
Simple async iterator for one-shot usage.

### `ClaudeSDKClient`
Full control over lifecycle, required for custom tools (via SDK MCP servers).
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    options = ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Explain this codebase")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock): print(block.text)
```

## Permission System
- `"default"`: Prompt for dangerous operations
- `"acceptEdits"`: Auto-accept file edits
- `"dontAsk"`: CI/CD mode
- `"bypassPermissions"`: Skip all prompts (`allow_dangerously_skip_permissions=True` required)

## Hooks
Customize behavior via callbacks. Available events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest`, `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`.

## Common Options (`ClaudeAgentOptions`)
- `cwd`: Working directory
- `allowed_tools`: List of allowed tools
- `permission_mode`: Permission handling string
- `mcp_servers`: Dict of MCP server configs
- `max_turns`: Max agent loops
- `model`: Model ID
- `agents`: Subagent definitions
- `env`: Environment variables

## Subagents
```python
from claude_agent_sdk import AgentDefinition
agents={"code-reviewer": AgentDefinition(description="...", prompt="...", tools=["Read"])}
```