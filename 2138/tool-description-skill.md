<!--
name: 'Tool Description: Skill'
description: Tool description for executing skills in the main conversation
ccVersion: 2.1.23
variables:
  - SKILL_TAG_NAME
-->
Execute skills - specialized capabilities for specific tasks.

When user references "/<something>" (slash command), use this tool.

Invocation:
- skill: "name" or skill: "namespace:name"
- Optional args: skill: "commit", args: "-m 'message'"

CRITICAL:
- If skill matches request, MUST invoke BEFORE responding
- NEVER mention skill without calling tool
- Don't invoke already-running skill
- Not for built-in CLI commands (/help, /clear)
- If <${SKILL_TAG_NAME}> tag present, skill already loaded - follow instructions directly
