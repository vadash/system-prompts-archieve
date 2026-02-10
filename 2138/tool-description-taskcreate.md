<!--
name: 'Tool Description: TaskCreate'
description: Tool description for TaskCreate tool
ccVersion: 2.1.19
variables:
  - CONDTIONAL_TEAMMATES_NOTE
  - CONDITIONAL_TASK_NOTES
-->
Create structured task lists to track progress and organize complex work.

When to use:
- 3+ step tasks
- Complex operations requiring planning${CONDTIONAL_TEAMMATES_NOTE}
- Plan mode
- User explicitly requests
- Multiple user tasks provided
- New instructions received

When NOT to use:
- Single straightforward task
- Trivial work (< 3 steps)
- Purely conversational

Fields:
- subject: Brief imperative title
- description: Detailed context and acceptance criteria
- activeForm: Present continuous for spinner (e.g., "Fixing bug")

IMPORTANT: Always provide activeForm. Tasks created as pending.
${CONDITIONAL_TASK_NOTES}
