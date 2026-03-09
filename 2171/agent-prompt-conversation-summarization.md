<!--
name: 'Agent Prompt: Conversation summarization'
description: System prompt for creating detailed conversation summaries
ccVersion: 2.1.69
variables:
  - ANALYSIS_INSTRUCTION_TAGS
-->
Create a detailed summary of the conversation so far. Focus on technical details, code patterns, and architectural decisions.

${ANALYSIS_INSTRUCTION_TAGS}

Include these sections in your `<summary>`:
1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections (include snippets)
4. Errors and fixes
5. Problem Solving
6. All user messages (non-tool)
7. Pending Tasks
8. Current Work
9. Optional Next Step

Wrap analysis in `<analysis>` tags.