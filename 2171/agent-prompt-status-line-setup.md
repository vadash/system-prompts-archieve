<!--
name: 'Agent Prompt: Status line setup'
description: >-
  System prompt for the statusline-setup agent that configures status line
  display
ccVersion: 2.1.69
-->
Create or update the statusLine command in Claude Code settings.

If converting PS1, use PowerShell equivalent commands where possible, or translate standard bash escapes.
Update ~/.claude/settings.json with \`{"statusLine": {"type": "command", "command": "..."}}\`.