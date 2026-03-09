<!--
name: 'Agent Prompt: /security-review slash command'
description: >-
  Comprehensive security review prompt for analyzing code changes with focus on
  exploitable vulnerabilities
ccVersion: 2.1.70
-->
---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Bash(git show:*), Bash(git remote show:*), Read, Glob, Grep, LS, Task
description: Complete a security review of the pending changes on the current branch
---
Perform a security-focused code review to identify HIGH-CONFIDENCE security vulnerabilities. Do not comment on existing security concerns not touched by the PR.

Focus on:
- Input validation
- Auth issues
- Crypto/Secrets
- Code execution/Injection

Format output in markdown including file, line number, severity, description, and recommendation. Filter out false positives.