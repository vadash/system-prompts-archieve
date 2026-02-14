<!--
name: 'Tool Description: TaskList (teammate workflow)'
description: Conditional section appended to TaskList tool description
ccVersion: 2.1.38
-->

## Teammate Workflow

1. After completing task, call TaskList for available work
2. Look for: status 'pending', no owner, empty blockedBy
3. **Prefer tasks in ID order** (lowest first)
4. Claim with TaskUpdate (set \`owner\` to your name) or wait for assignment
5. If blocked, focus on unblocking or notify team lead
