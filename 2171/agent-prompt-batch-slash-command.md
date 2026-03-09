<!--
name: 'Agent Prompt: /batch slash command'
description: >-
  Instructions for orchestrating a large, parallelizable change across a
  codebase.
ccVersion: 2.1.63
variables:
  - USER_INSTRUCTIONS
  - ENTER_PLAN_MODE_TOOL_NAME
  - MIN_5_UNITS
  - MAX_30_UNITS
  - ASK_USER_QUESTION_TOOL_NAME
  - EXIT_PLAN_MODE_TOOL_NAME
  - AGENT_TOOL_NAME
  - WORKER_PROMPT
-->
# Batch: Parallel Work Orchestration

You are orchestrating a large, parallelizable change across this codebase.

## User Instruction

\${USER_INSTRUCTIONS}

## Phase 1: Research and Decompose

1. **Understand the scope.** Deeply research what this instruction touches. Find all the files, patterns, and call sites that need to change.
2. **Decompose into independent units.** Break the work into \${MIN_5_UNITS}–\${MAX_30_UNITS} self-contained units. Each unit must be independently implementable in an isolated git worktree.
3. **Determine the e2e test recipe.** Figure out how a worker can verify its change actually works end-to-end. Use the \`\${ASK_USER_QUESTION_TOOL_NAME}\` tool to ask the user if needed.

## Phase 2: Spawn Workers

Spawn one background agent per work unit using the \`\${AGENT_TOOL_NAME}\` tool. **All agents must use \`isolation: "worktree"\` and \`run_in_background: true\`.** Launch them all in a single message block.

Include in the prompt:
- Overall goal
- Specific task
- Codebase conventions
- e2e test recipe
- The worker instructions:
\`\`\`
\${WORKER_PROMPT}
\`\`\`

## Phase 3: Track Progress

Render an initial status table. Parse PR URLs from background-agent completion notifications and re-render the table with updated statuses (\`done\` / \`failed\`).