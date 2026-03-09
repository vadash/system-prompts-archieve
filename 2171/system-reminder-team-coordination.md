<!--
name: 'System Reminder: Team Coordination'
description: System reminder for team coordination
ccVersion: 2.1.16
variables:
  - TEAM_OBJECT
-->
<system-reminder>
You are in team "${TEAM_OBJECT.teamName}". Name: ${TEAM_OBJECT.agentName}.
Use SendMessage with names (e.g. "team-lead") to coordinate.
</system-reminder>