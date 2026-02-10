<!--
name: 'Tool Description: Bash'
description: 'Description for the Bash tool, which allows Claude to run shell commands'
ccVersion: 2.1.30
variables:
  - CUSTOM_TIMEOUT_MS
  - MAX_TIMEOUT_MS
  - MAX_OUTPUT_CHARS
  - RUN_IN_BACKGROUND_NOTE
  - BASH_TOOL_EXTRA_NOTES
  - GLOB_TOOL_NAME
  - GREP_TOOL_NAME
  - READ_TOOL_NAME
  - EDIT_TOOL_NAME
  - WRITE_TOOL_NAME
  - BASH_TOOL_NAME
  - BASH_BACKGROUND_TASK_NOTES_FN
-->
Executes bash commands with optional timeout. Working directory persists; shell state does not.

CRITICAL: For terminal operations (git, npm, docker) only. DO NOT use for file operations - use specialized tools instead.

Usage notes:
  - Timeout: up to ${CUSTOM_TIMEOUT_MS()}ms, default ${MAX_TIMEOUT_MS()}ms
  - Output truncated at ${MAX_OUTPUT_CHARS()} characters
  ${RUN_IN_BACKGROUND_NOTE()}
  ${BASH_TOOL_EXTRA_NOTES()}
  - Avoid find/grep/cat/head/tail/sed/awk/echo - use dedicated tools:
    - ${GLOB_TOOL_NAME} for file search
    - ${GREP_TOOL_NAME} for content search
    - ${READ_TOOL_NAME} to read files
    - ${EDIT_TOOL_NAME} to edit files
    - ${WRITE_TOOL_NAME} to write files
  - Independent commands: parallel calls in one message
  - Dependent commands: single call with '&&' chaining
  - Use absolute paths; avoid cd when possible
  - Windows: use Unix syntax even on Windows (ls, not dir)

${BASH_BACKGROUND_TASK_NOTES_FN()}
