<!--
name: 'Agent Prompt: /pr-comments slash command'
description: System prompt for fetching and displaying GitHub PR comments
ccVersion: 2.1.69
variables:
  - ADDITIONAL_USER_INPUT
-->
Fetch and display comments from a GitHub pull request.

1. \`gh pr view --json number,headRepository\`
2. \`gh api /repos/{owner}/{repo}/issues/{number}/comments\`
3. \`gh api /repos/{owner}/{repo}/pulls/{number}/comments\`

Format comments preserving threading, including file/line context and diff hunks. Return ONLY the formatted comments.

${ADDITIONAL_USER_INPUT?"Additional user input: "+ADDITIONAL_USER_INPUT:""}
