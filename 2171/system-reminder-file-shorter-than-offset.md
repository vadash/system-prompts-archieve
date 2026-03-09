<!--
name: 'System Reminder: File shorter than offset'
description: Warning when file read offset exceeds file length
ccVersion: 2.1.18
variables:
  - RESULT_OBJECT
-->
<system-reminder>Warning: file shorter than offset (\${RESULT_OBJECT.file.startLine}). Lines: \${RESULT_OBJECT.file.totalLines}.</system-reminder>