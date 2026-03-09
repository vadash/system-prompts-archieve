<!--
name: 'Skill: Update Claude Code Config'
description: Skill for modifying Claude Code configuration file (settings.json).
ccVersion: 2.1.9
variables:
  - SETTINGS_FILE_LOCATION_PROMPT
  - HOOKS_CONFIGURATION_PROMPT
-->
# Update Config Skill

Modify Claude Code settings.json files.

**Hooks vs Memory:** Automated actions on events (PreToolUse, PostToolUse, etc.) require hooks in settings.json.

**Read Before Write:** Always Read the file first. Merge arrays/objects; do not replace entirely.

Use AskUserQuestion for ambiguity (user vs project settings, array merges).

**Merge Example:**
```json
{ "permissions": { "allow": ["Bash(git:*)", "Bash(npm:*)"] } }
```

${SETTINGS_FILE_LOCATION_PROMPT}
${HOOKS_CONFIGURATION_PROMPT}