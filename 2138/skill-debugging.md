<!--
name: 'Skill: Debugging'
description: >-
  Instructions for debugging an issue that the user is encountering in the
  Claude Code session
ccVersion: 2.1.30
variables:
  - DEBUG_LOG_PATH
  - DEBUG_LOG_SUMMARY
  - ISSUE_DESCRIPTION
  - SETTINGS_FILE_PATH
  - LOG_LINE_COUNT
  - CLAUDE_CODE_GUIDE_SUBAGENT_NAME
-->
# Debug Skill

Help the user debug an issue in the current Claude Code session.

## Debug Log

Location: \`\${DEBUG_LOG_PATH}\`

\${DEBUG_LOG_SUMMARY}

Grep for \`[ERROR]\` and \`[WARN]\` lines across the full file.

## Issue

\${ISSUE_DESCRIPTION||"The user did not describe a specific issue. Read the debug log and summarize any errors, warnings, or notable issues."}

## Settings Locations

- User: \`\${SETTINGS_FILE_PATH("userSettings")}\`
- Project: \`\${SETTINGS_FILE_PATH("projectSettings")}\`
- Local: \`\${SETTINGS_FILE_PATH("localSettings")}\`

## Instructions

1. Review the issue description
2. Check the last \`\${LOG_LINE_COUNT}\` lines for debug file format
3. Search for \`[ERROR]\` and \`[WARN]\` entries, stack traces, failure patterns
4. Consider launching the \`\${CLAUDE_CODE_GUIDE_SUBAGENT_NAME}\` subagent for feature context
5. Explain findings in plain language
6. Suggest concrete fixes or next steps
