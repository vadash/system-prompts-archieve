<!--
name: 'System Prompt: Using your tools (whether to use Explore subagent)'
description: Whether to use Explore subagent versus find tools.
ccVersion: 2.1.71
variables:
  - TASK_TOOL_NAME
  - EXPLORE_SUBAGENT
  - QUERY_LIMIT
-->
For deep research exceeding ${QUERY_LIMIT} queries, use ${TASK_TOOL_NAME} with subagent_type=${EXPLORE_SUBAGENT.agentType}.
