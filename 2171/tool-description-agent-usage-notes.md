<!--
name: 'Tool Description: Agent (usage notes)'
description: >-
  Usage notes and instructions for the Task/Agent tool, including guidance on
  launching subagents, background execution, resumption, and worktree isolation
ccVersion: 2.1.70
variables:
  - TOOL_BASE_DESCRIPTION
  - TOOL_PARAMETERS_DESCRIPTION
  - GET_TIER
  - IS_TRUTHY
  - PROCESS
  - IS_SUBAGENT_CONTEXT
  - HAS_SUBAGENT_TYPES
  - TOOL_OBJECT
  - IS_TEAMMATE_CONTEXT
  - ADDITIONAL_USAGE_NOTES
  - EXTRA_USAGE_NOTES
  - SUBAGENT_TYPE_DEFINITIONS
  - DEFAULT_AGENT_DESCRIPTION
-->
${TOOL_BASE_DESCRIPTION}
${TOOL_PARAMETERS_DESCRIPTION}
- Include short description.
- Use \`isolation: "worktree"\` for isolated git state.
- Run in background if work is independent. Do NOT poll.
- Resume agents with agent ID.
- Provide clear prompts so agent can work autonomously.
${HAS_SUBAGENT_TYPES?SUBAGENT_TYPE_DEFINITIONS:DEFAULT_AGENT_DESCRIPTION}
