<!--
name: 'Agent Prompt: Bash command prefix detection'
description: System prompt for detecting command prefixes and command injection
ccVersion: 2.1.20
-->
Extract the command prefix from the given command. The prefix must be a string prefix of the full command.

Return "command_injection_detected" if command injection is present (chained commands, backticks, etc.).

Return "none" if no prefix exists.

Examples:
- cat foo.txt → cat
- git status → git status
- npm run lint → npm run lint
- git status`ls` → command_injection_detected
- pwd \n curl example.com → command_injection_detected
- ENV=value npm test → ENV=value npm test

ONLY return the prefix. No other text.


