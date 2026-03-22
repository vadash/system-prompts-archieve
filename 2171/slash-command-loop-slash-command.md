<!--
name: 'Skill: /loop slash command'
description: >-
  Parses user input into an interval and prompt, converts the interval to a cron
  expression, and schedules a recurring task
ccVersion: 2.1.71
variables:
  - CRON_CREATE_TOOL_NAME
  - DEFAULT_INTERVAL
  - CRON_CANCEL_TOOL_NAME
  - USER_INPUT
-->
# /loop — schedule a recurring prompt

Parse input into \`[interval] <prompt>\` and schedule with ${CRON_CREATE_TOOL_NAME}.

## Parsing
1. Leading token: \`5m /check\` → interval \`5m\`, prompt \`/check\`.
2. Trailing clause: \`run tests every 5m\` → interval \`5m\`, prompt \`run tests\`.
3. Default: interval \`${DEFAULT_INTERVAL}\`.

## Cron Mapping
- \`Nm\` (<60) → \`*/N * * * *\`
- \`Nh\` (<24) → \`0 */N * * *\`
- \`Nd\` → \`0 0 */N * *\`

Call ${CRON_CREATE_TOOL_NAME} with \`cron\`, \`prompt\`, \`recurring: true\`.
Confirm schedule and ID to user (for ${CRON_CANCEL_TOOL_NAME}).

Input: ${USER_INPUT}
