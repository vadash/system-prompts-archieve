<!--
name: 'Tool Description: TodoWrite'
description: Tool description for creating and managing task lists
ccVersion: 2.0.14
variables:
  - EDIT_TOOL_NAME
-->
Create and manage structured task lists for tracking progress.

When to use:
- 3+ step tasks
- Complex operations
- User explicitly requests
- Multiple user tasks provided
- New instructions received

When NOT to use:
- Single straightforward task
- Trivial work (< 3 steps)
- Conversational/informational

Task states:
- pending: Not started
- in_progress: Working on (ONE at a time)
- completed: Finished successfully

CRITICAL: Each task needs content (imperative) + activeForm (present continuous). Mark completed IMMEDIATELY after finishing. ONE task in_progress at a time.
