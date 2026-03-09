<!--
name: 'Data: Agent SDK patterns — Python'
description: >-
  Python Agent SDK patterns including custom tools, hooks, subagents, MCP
  integration, and session resumption
ccVersion: 2.1.71
-->
# Agent SDK Patterns — Python

## Basic Agent

\`\`\`python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="Explain what this repository does",
        options=ClaudeAgentOptions(
            cwd="/path/to/project",
            allowed_tools=["Read", "Glob", "Grep"]
        )
    ):
        if isinstance(message, ResultMessage):
            print(message.result)

anyio.run(main)
\`\`\`

## Custom Tools

\`\`\`python
import anyio
from claude_agent_sdk import (
    tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
)

@tool("get_weather", "Get current weather", {"location": str})
async def get_weather(args):
    return {"content": [{"type": "text", "text": f"Sunny and 72°F in {args['location']}."}]}

server = create_sdk_mcp_server("weather-tools", tools=[get_weather])

async def main():
    options = ClaudeAgentOptions(mcp_servers={"weather": server})
    async with ClaudeSDKClient(options=options) as client:
        await client.query("What's the weather in Paris?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock): print(block.text)

anyio.run(main)
\`\`\`

## Hooks

\`\`\`python
import anyio
from datetime import datetime
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, ResultMessage

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get('tool_input', {}).get('file_path', 'unknown')
    with open('./audit.log', 'a') as f: f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

async def main():
    async for message in query(
        prompt="Refactor utils.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Write"],
            permission_mode="acceptEdits",
            hooks={"PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]}
        )
    ):
        if isinstance(message, ResultMessage): print(message.result)

anyio.run(main)
\`\`\`

## Subagents

\`\`\`python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage

async def main():
    async for message in query(
        prompt="Use the code-reviewer agent",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code reviewer.",
                    prompt="Analyze code quality.",
                    tools=["Read", "Glob", "Grep"]
                )
            }
        )
    ):
        if isinstance(message, ResultMessage): print(message.result)

anyio.run(main)
\`\`\`

## MCP Server Integration

### Browser Automation (Playwright)
\`\`\`python
        options=ClaudeAgentOptions(
            mcp_servers={"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}
        )
\`\`\`

### Database Access (PostgreSQL)
\`\`\`python
        options=ClaudeAgentOptions(
            mcp_servers={
                "postgres": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-postgres"],
                    "env": {"DATABASE_URL": os.environ["DATABASE_URL"]}
                }
            }
        )
\`\`\`

## Permission Modes

\`\`\`python
        options=ClaudeAgentOptions(
            allowed_tools=["Bash"],
            permission_mode="default"  # Prompts for dangerous operations
        )

        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit"],
            permission_mode="acceptEdits" # Auto-accept file edits
        )

        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Write"],
            permission_mode="bypassPermissions", # Skip all prompts
            allow_dangerously_skip_permissions=True
        )
\`\`\`

## Error Recovery

\`\`\`python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, CLINotFoundError, CLIConnectionError, ProcessError, ResultMessage

async def run_with_recovery():
    try:
        async for message in query(
            prompt="Fix tests",
            options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"], max_turns=10)
        ):
            if isinstance(message, ResultMessage): print(message.result)
    except CLINotFoundError: print("CLI not found")
    except CLIConnectionError as e: print(f"Connection error: {e}")
    except ProcessError as e: print(f"Process error: {e}")

anyio.run(run_with_recovery)
\`\`\`

## Session Resumption

\`\`\`python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

async def main():
    session_id = None
    async for message in query(prompt="Read auth module", options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"])):
        if isinstance(message, SystemMessage) and message.subtype == "init": session_id = message.session_id

    async for message in query(prompt="Find callers", options=ClaudeAgentOptions(resume=session_id)):
        if isinstance(message, ResultMessage): print(message.result)

anyio.run(main)
\`\`\`

## Session History

\`\`\`python
import anyio
from claude_agent_sdk import list_sessions, get_session_messages

async def main():
    sessions = await list_sessions()
    if sessions:
        messages = await get_session_messages(session_id=sessions[0].session_id)
        for msg in messages: print(msg)

anyio.run(main)
\`\`\`

## Custom System Prompt

\`\`\`python
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep"],
            system_prompt="You are a senior code reviewer..."
        )
\`\`\`