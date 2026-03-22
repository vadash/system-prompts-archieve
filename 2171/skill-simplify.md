<!--
name: 'Skill: Simplify'
description: Instructions for simplifying code
ccVersion: 2.1.71
variables:
  - AGENT_TOOL_NAME
-->
# Simplify: Code Review and Cleanup

Review changed files for reuse, quality, and efficiency. Fix issues.

1. **Identify Changes:** Run \`git diff HEAD\`.
2. **Review Agents:** Use ${AGENT_TOOL_NAME} to launch 3 agents in parallel:
   - **Reuse:** Replace duplicated code with existing utilities.
   - **Quality:** Fix redundant state, leaky abstractions, raw strings.
   - **Efficiency:** Remove redundant computation, hot-path bloat, TOCTOU patterns.
3. **Fix:** Aggregate findings and fix directly. Skip false positives. Summarize changes.
