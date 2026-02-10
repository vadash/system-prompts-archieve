<!--
name: 'System Reminder: Plan mode re-entry'
description: >-
  System reminder sent when the user enters Plan mode after having previously
  exited it either via shift+tab or by approving Claude's plan.
ccVersion: 2.0.52
variables:
  - SYSTEM_REMINDER
  - EXIT_PLAN_MODE_TOOL_OBJECT
-->
Re-entering plan mode. Read existing plan, evaluate against current request, update or overwrite accordingly.

