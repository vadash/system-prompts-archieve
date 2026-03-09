<!--
name: 'Tool Description: Agent (when to launch subagents)'
description: >-
  Describes _when_ to use the Agent tool - for launching specialized subagent
  subprocesses to autonomously handle complex multi-step tasks
ccVersion: 2.1.70
variables:
  - AGENT_TOOL_NAME
  - AVAILABLE_AGENT_TYPES
  - CAN_FORK_CONTEXT
-->
Launch subagents for complex multi-step tasks.
\${AVAILABLE_AGENT_TYPES}
\${CAN_FORK_CONTEXT?\`Specify subagent_type, or omit to fork and inherit context.\`:\`Specify subagent_type.\`}