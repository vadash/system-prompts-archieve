<!--
name: 'System Reminder: Plan file reference'
description: Reference to an existing plan file
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
-->
Plan exists at: \${ATTACHMENT_OBJECT.planFilePath}

\${ATTACHMENT_OBJECT.planContent}

Continue if relevant and incomplete.
