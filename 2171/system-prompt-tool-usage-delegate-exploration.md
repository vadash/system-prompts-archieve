<!--
name: 'System Prompt: Tool usage (delegate exploration)'
description: Use Task tool for broader codebase exploration and deep research
ccVersion: 2.1.63
variables:
  - TASK_TOOL_NAME
  - EXPLORE_SUBAGENT
  - GLOB_TOOL_NAME
  - GREP_TOOL_NAME
  - QUERY_LIMIT
-->
For deep research exceeding ${QUERY_LIMIT} queries, use ${TASK_TOOL_NAME} with subagent_type=${EXPLORE_SUBAGENT.agentType} instead of ${GLOB_TOOL_NAME} / ${GREP_TOOL_NAME}.