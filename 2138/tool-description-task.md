<!--
name: 'Tool Description: Task'
description: Tool description for launching specialized sub-agents to handle complex tasks
ccVersion: 2.1.38
variables:
  - TASK_TOOL_PREAMBLE
  - TASK_TOOL
  - READ_TOOL
  - GLOB_TOOL
  - GET_SUBSCRIPTION_TYPE_FN
  - IS_TRUTHY_FN
  - PROCESS_OBJECT
  - 'FALSE'
  - BASH_TOOL
  - TASK_TOOL_OBJECT
  - WRITE_TOOL
-->
${TASK_TOOL_PREAMBLE}

When NOT to use:
- Reading specific file paths: use ${READ_TOOL} or ${GLOB_TOOL}
- Searching for specific class definitions: use ${GLOB_TOOL}
- Searching within 2-3 files: use ${READ_TOOL}

Usage notes:
- Short description (3-5 words) required${GET_SUBSCRIPTION_TYPE_FN()!=="pro"?\`
- Launch multiple agents concurrently when possible\`:""}
- Agent returns result + agent ID
- Resume agents with resume parameter to preserve context
- "Access to current context" agents see full history
- Specify if agent should write code or do research${!IS_TRUTHY_FN(PROCESS_OBJECT.env.CLAUDE_CODE_DISABLE_BACKGROUND_TASKS)&&!FALSE()?\`
- run_in_background: returns output_file path, check with ${READ_TOOL} or ${BASH_TOOL} tail\`:""}${FALSE()?\`
- Only synchronous subagents supported\`:""}
