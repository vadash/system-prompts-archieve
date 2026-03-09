<!--
name: 'Agent Prompt: CLAUDE.md creation'
description: >-
  System prompt for analyzing codebases and creating CLAUDE.md documentation
  files
ccVersion: 2.0.14
-->
Analyze this codebase and create a CLAUDE.md file for future instances of Claude Code to operate in this repository.

Include:
1. Common commands (build, lint, test).
2. High-level code architecture and structure.

Notes:
- Do not include obvious instructions.
- Avoid generic development practices.
- Prefix the file with:
\`\`\`
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
\`\`\`