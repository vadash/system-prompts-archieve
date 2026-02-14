<!--
name: 'Tool Description: TeamDelete'
description: Tool description for the TeamDelete tool
ccVersion: 2.1.33
-->

Remove team and task directories after swarm work completes.

Removes \`~/.claude/teams/{team-name}/\`, \`~/.claude/tasks/{team-name}/\`, clears team context.

**CRITICAL:** Fails if active teammates remain. Terminate teammates first, then delete.
