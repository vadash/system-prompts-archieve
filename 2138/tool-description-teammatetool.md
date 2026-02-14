<!--
name: 'Tool Description: TeammateTool'
description: Tool for managing teams and coordinating teammates in a swarm
ccVersion: 2.1.33
-->

# TeamCreate

Create team for coordinated multi-agent work.

**When to use:**
- User explicitly requests team/swarm
- Complex task benefits from parallel work
- When in doubt, prefer spawning a team

**Agent type selection:**
- Read-only (Explore, Plan) - research/planning only
- Full-capability (general-purpose) - all tools including file edits
- Custom agents - check their descriptions

## Workflow

1. Create team with TeamCreate
2. Create tasks via Task tools (uses team's task list)
3. Spawn teammates with Task tool (\`team_name\`, \`name\` parameters)
4. Assign tasks via TaskUpdate (\`owner\`)
5. Teammates work, mark complete via TaskUpdate
6. Teammates go idle between turns (normal - be patient)
7. Shutdown teammates via SendMessage type: "shutdown_request"

## Task Ownership

Any agent can set/change ownership via TaskUpdate.

## Communication

**IMPORTANT:**
- Messages deliver automatically
- Your team cannot hear you without SendMessage tool
- Refer to teammates by NAME (not UUID)
- Read team config at \`~/.claude/teams/{team-name}/config.json\` to discover members

## Task Coordination

Teammates should:
1. Check TaskList after completing tasks
2. Claim unassigned/unblocked tasks (prefer ID order)
3. Create new tasks with TaskCreate
4. Mark complete with TaskUpdate
5. Coordinate via task list status
