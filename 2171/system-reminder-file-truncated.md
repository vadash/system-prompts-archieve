<!--
name: 'System Reminder: File truncated'
description: Notification that file was truncated due to size
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
  - MAX_LINES_CONSTANT
  - READ_TOOL_OBJECT
-->
Note: ${ATTACHMENT_OBJECT.filename} truncated to ${MAX_LINES_CONSTANT} lines. Use ${READ_TOOL_OBJECT.name} to read more.
