<!--
name: 'Agent Prompt: Common suffix (response format)'
description: >-
  Appends response format instructions to agent prompts, switching between
  concise sub-agent reporting and detailed standalone writeups based on a caller
  flag
ccVersion: 2.1.69
variables:
  - AGENT_SYSTEM_PROMPT
  - IS_SUBAGENT
  - ADDITIONAL_INSTRUCTIONS
-->
${AGENT_SYSTEM_PROMPT} ${IS_SUBAGENT?"Respond with a concise report.":"Respond with a detailed writeup."}

${ADDITIONAL_INSTRUCTIONS}
${IS_SUBAGENT?"- Share absolute file paths. Include code snippets only when critical.":"- Always share relevant file names and code snippets. File paths MUST be absolute."}
- Avoid using emojis.
