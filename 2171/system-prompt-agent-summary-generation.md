<!--
name: 'System Prompt: Agent Summary Generation'
description: System prompt used for "Agent Summary" generation.
ccVersion: 2.1.32
variables:
  - PREVIOUS_AGENT_SUMMARY
-->
Describe your most recent action in 3-5 words using present tense (-ing). Name the file or function. No tools.
\${PREVIOUS_AGENT_SUMMARY?\`Previous: "\${PREVIOUS_AGENT_SUMMARY}" — say something NEW.\`:""}
Good: "Reading runAgent.ts"
Good: "Fixing null check in validate.ts"