<!--
name: 'Agent Prompt: Recent Message Summarization'
description: Agent prompt used for summarizing recent messages.
ccVersion: 2.1.32
-->
Summarize the RECENT messages only. Earlier context is preserved - don't summarize it.

Include:
1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections (names, snippets, why important)
4. Errors and fixes
5. Problem Solving
6. All user messages (non-tool results)
7. Pending Tasks
8. Current Work
9. Optional Next Step

Wrap analysis in <analysis> tags. Output in <summary> tags.
