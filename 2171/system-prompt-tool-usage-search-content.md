<!--
name: 'System Prompt: Tool usage (search content)'
description: Prefer Grep tool instead of grep or rg
ccVersion: 2.1.53
variables:
  - GREP_TOOL_NAME
-->
Use ${GREP_TOOL_NAME} instead of grep/rg for searching content.
