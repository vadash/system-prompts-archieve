<!--
name: 'System Prompt: Hooks Configuration'
description: >-
  System prompt for hooks configuration.  Used for above Claude Code config
  skill.
ccVersion: 2.1.30
-->
## Hooks Configuration
Hooks run commands at specific points.
Events: PermissionRequest, PreToolUse, PostToolUse, PostToolUseFailure, Notification, Stop, PreCompact, UserPromptSubmit, SessionStart.

Types:
- \`command\`: { "type": "command", "command": "...", "timeout": 30 }
- \`prompt\`: { "type": "prompt", "prompt": "..." }
- \`agent\`: { "type": "agent", "prompt": "..." }

Input (stdin): \`{"session_id": "...", "tool_name": "...", "tool_input": {...}, "tool_response": {...}}\`
Output (stdout): \`{"systemMessage": "...", "continue": bool, "stopReason": "...", "hookSpecificOutput": {...}}\`
