<!--
name: 'Agent Prompt: Recent Message Summarization'
description: Agent prompt used for summarizing recent messages.
ccVersion: 2.1.69
variables:
  - ANALYSIS_INSTRUCTION_TAGS
-->
Summarize the RECENT messages only. Do not summarize earlier retained context.

${ANALYSIS_INSTRUCTION_TAGS}

Include in `<summary>`:
1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections
4. Errors and fixes
5. Problem Solving
6. All user messages
7. Pending Tasks
8. Current Work
9. Optional Next Step

Wrap analysis in `<analysis>`.