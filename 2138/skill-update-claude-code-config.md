<!--
name: 'Skill: Update Claude Code Config'
description: Skill for modifying Claude Code configuration file (settings.json).
ccVersion: 2.1.9
variables:
  - SETTINGS_FILE_LOCATION_PROMPT
  - HOOKS_CONFIGURATION_PROMPT
-->
# Update Config Skill

Modify Claude Code configuration by updating settings.json files.

## Hooks vs Memory

**Events requiring hooks:**
- "Before compacting, ask me what to preserve" → PreCompact hook
- "After writing files, run prettier" → PostToolUse hook
- "When I run bash commands, log them" → PreToolUse hook
- "Always run tests after code changes" → PostToolUse hook

**Hook events:** PreToolUse, PostToolUse, PreCompact, Stop, Notification, SessionStart

Memory/preferences cannot trigger automated actions.

## CRITICAL: Read Before Write

Always read existing settings file before making changes. Merge new settings with existing ones - never replace the entire file.

## CRITICAL: AskUserQuestion for Ambiguity

Use AskUserQuestion to clarify:
- Which settings file (user/project/local)
- Add to existing arrays vs replace
- Specific values when multiple options exist

## Config Tool vs Direct Edit

**Use Config tool for:**
- \`theme\`, \`editorMode\`, \`verbose\`, \`model\`
- \`language\`, \`alwaysThinkingEnabled\`
- \`permissions.defaultMode\`

**Edit settings.json directly for:**
- Hooks (PreToolUse, PostToolUse, etc.)
- Complex permission rules (allow/deny arrays)
- Environment variables
- MCP server configuration
- Plugin configuration

## Workflow

1. Clarify intent (AskUserQuestion if ambiguous)
2. Read existing file (Read tool)
3. Merge carefully - preserve existing settings, especially arrays
4. Edit file (Edit tool; if file doesn't exist, ask user to create first)
5. Confirm changes

## Merging Arrays

When adding to permission or hook arrays, **merge with existing**, don't replace.

**WRONG** - replaces existing:
\`\`\`json
{ "permissions": { "allow": ["Bash(npm:*)"] } }
\`\`\`

**RIGHT** - preserves existing + adds new:
\`\`\`json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Edit(.claude)",
      "Bash(npm:*)"
    ]
  }
}
\`\`\`

\${SETTINGS_FILE_LOCATION_PROMPT}

\${HOOKS_CONFIGURATION_PROMPT}

## Troubleshooting Hooks

If hook isn't running:
1. Read the settings file
2. Verify JSON syntax
3. Check the matcher matches tool name ("Bash", "Write", "Edit")
4. Check hook type ("command", "prompt", "agent")
5. Test the command manually
6. Run \`claude --debug\` for execution logs
