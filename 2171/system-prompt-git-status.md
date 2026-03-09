<!--
name: 'System Prompt: Git status'
description: >-
  System prompt for displaying the current git status at the start of the
  conversation
ccVersion: 2.1.30
variables:
  - CURRENT_BRANCH
  - MAIN_BRANCH
  - GIT_STATUS
  - RECENT_COMMITS
-->
Git status snapshot:
Branch: \${CURRENT_BRANCH}
Main: \${MAIN_BRANCH}
Status: \${GIT_STATUS||"(clean)"}
Recent commits: \${RECENT_COMMITS}