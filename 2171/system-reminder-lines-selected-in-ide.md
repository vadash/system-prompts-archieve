<!--
name: 'System Reminder: Lines selected in IDE'
description: Notification about lines selected by user in IDE
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
  - TRUNCATED_CONTENT
-->
User selected ${ATTACHMENT_OBJECT.lineStart}-${ATTACHMENT_OBJECT.lineEnd} in ${ATTACHMENT_OBJECT.filename}:
${TRUNCATED_CONTENT}