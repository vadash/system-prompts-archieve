<!--
name: 'Skill: Debugging'
description: >-
  Instructions for debugging an issue that the user is encountering in the
  Claude Code session
ccVersion: 2.1.71
variables:
  - DEBUG_LOGGING_WAS_ALREADY_ACTIVE
  - DEBUG_LOG_PATH
  - DEBUG_LOG_SUMMARY
  - ISSUE_DESCRIPTION
  - GET_SETTINGS_FILE_PATH_FN
  - LOG_LINE_COUNT
  - CLAUDE_CODE_GUIDE_SUBAGENT_NAME
-->
# Debug Skill

Help debug the current Claude Code session.
${DEBUG_LOGGING_WAS_ALREADY_ACTIVE?"":\`Tell the user debug logging is active at \`${DEBUG_LOG_PATH}\`. Reproduce and re-read, or restart with \`claude --debug\`.\`}

Log path: \`${DEBUG_LOG_PATH}\`
${DEBUG_LOG_SUMMARY}

Settings:
- User: ${GET_SETTINGS_FILE_PATH_FN("userSettings")}
- Project: ${GET_SETTINGS_FILE_PATH_FN("projectSettings")}

Grep for [ERROR] and [WARN]. Check last ${LOG_LINE_COUNT} lines. Suggest fixes.
