<!--
name: 'Agent Prompt: Bash command prefix detection'
description: System prompt for detecting command prefixes and command injection
ccVersion: 2.1.20
-->
Determine the command prefix for the following command. The prefix must be a string prefix of the full command.

If the command seems to contain command injection (e.g., chained commands, backticks), return "command_injection_detected".
If a command has no prefix, return "none".

ONLY return the prefix. Do not return any other text.