<!--
name: 'System Reminder: File modified by user or linter'
description: Notification that a file was modified externally
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
-->
Note: ${ATTACHMENT_OBJECT.filename} modified externally. Do not revert.
${ATTACHMENT_OBJECT.snippet}
