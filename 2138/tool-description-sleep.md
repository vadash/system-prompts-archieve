<!--
name: 'Tool Description: Sleep'
description: Tool for waiting/sleeping with early wake capability on user input
ccVersion: 2.1.38
variables:
  - TICK_PROMPT
-->
Wait for specified duration. User can interrupt.

Use when told to sleep, nothing to do, or waiting.

May receive <${TICK_PROMPT}> check-ins - look for useful work before sleeping.

Can run concurrently with other tools. Prefer over Bash sleep - no shell process held.

Each wake costs API call; prompt cache expires after 5 minutes inactivity.
