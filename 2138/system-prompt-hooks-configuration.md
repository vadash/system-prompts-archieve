<!--
name: 'System Prompt: Hooks Configuration'
description: >-
  System prompt for hooks configuration.  Used for above Claude Code config
  skill.
ccVersion: 2.1.30
-->

## Hooks Configuration

Hooks run commands at specific points in Claude Code's lifecycle.

### Hook Events

| Event | Matcher | Purpose |
|-------|---------|---------|
| PermissionRequest | Tool name | Run before permission prompt |
| PreToolUse | Tool name | Run before tool, can block |
| PostToolUse | Tool name | Run after successful tool |
| PostToolUseFailure | Tool name | Run after tool fails |
| Notification | Notification type | Run on notifications |
| Stop | - | Run when Claude stops (including clear, resume, compact) |
| PreCompact | "manual"/"auto" | Before compaction |
| UserPromptSubmit | - | When user submits |
| SessionStart | - | When session starts |

### Hook Types

**Command** - Runs a shell command:
```json
{ "type": "command", "command": "prettier --write $FILE", "timeout": 30 }
```

**Prompt** - Evaluates a condition with LLM (PreToolUse, PostToolUse, PermissionRequest only):
```json
{ "type": "prompt", "prompt": "Is this safe? $ARGUMENTS" }
```

**Agent** - Runs an agent with tools (PreToolUse, PostToolUse, PermissionRequest only):
```json
{ "type": "agent", "prompt": "Verify tests pass: $ARGUMENTS" }
```

### Hook Input (stdin JSON)
```json
{
  "session_id": "abc123",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path/to/file.txt", "content": "..." },
  "tool_response": { "success": true }
}
```

### Hook JSON Output Fields

- `systemMessage` - Display message to user
- `continue` - Set to `false` to block/stop (default: true)
- `stopReason` - Message shown when blocking
- `suppressOutput` - Hide stdout from transcript
- `hookSpecificOutput` - Event-specific output (must include `hookEventName`):
  - `additionalContext` - Text injected into model context
  - `permissionDecision` - "allow", "deny", or "ask" (PreToolUse)
  - `permissionDecisionReason` - Reason for decision (PreToolUse)
  - `updatedInput` - Modified tool input (PreToolUse)
