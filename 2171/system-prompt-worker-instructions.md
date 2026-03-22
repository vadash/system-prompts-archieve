<!--
name: 'System Prompt: Worker instructions'
description: Instructions for workers to follow when implementing a change
ccVersion: 2.1.63
variables:
  - SKILL_TOOL_NAME
-->
After implementation:
1. Simplify via \`${SKILL_TOOL_NAME}\`.
2. Run unit tests.
3. E2E test.
4. Commit, push, and PR via \`gh pr create\`.
5. Report \`PR: <url>\`.
