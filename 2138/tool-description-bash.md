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
Executes Bash commands. Working directory persists; shell variables do not.
**CRITICAL:** Use for system operations (git, npm) ONLY.
- **Forbidden:** `sed`, `awk`, `cat`, `grep`, `find`. Use ${EDIT_TOOL_NAME}, ${READ_TOOL_NAME}, ${GREP_TOOL_NAME}, ${GLOB_TOOL_NAME} instead.
- **Windows Context:** This tool is BASH (Git Bash/WSL), NOT PowerShell or cmd.exe. Use Unix syntax (`ls` not `dir`), forward slashes `C:/path` (not `C:\path`), and no cmd flags like `/d`.
- **Syntax:**
  - **Always** quote paths with spaces: `"path/to file"`.
  - Chain dependent commands with `&&` (e.g., `git add . && git commit`).
  - Run independent commands via parallel tool calls.
  - Use absolute paths; avoid `cd`.
- **Timeout:** Default ${MAX_TIMEOUT_MS()}ms.
- **Output:** Truncated at ${MAX_OUTPUT_CHARS()} chars.
${RUN_IN_BACKGROUND_NOTE()}
${BASH_TOOL_EXTRA_NOTES()}
${BASH_BACKGROUND_TASK_NOTES_FN()}
