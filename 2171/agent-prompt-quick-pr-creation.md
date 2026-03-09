<!--
name: 'Agent Prompt: Quick PR creation'
description: >-
  Streamlined prompt for creating a commit and pull request with pre-populated
  context
ccVersion: 2.1.69
variables:
  - PREAMBLE_BLOCK
  - SAFE_USER_VALUE
  - WHOAMI_VALUE
  - DEFAULT_BRANCH
  - COMMIT_ATTRIBUTION_TEXT
  - PR_EDIT_OPTIONS_NOTE
  - PR_CREATE_OPTIONS_NOTE
  - PR_BODY_EXTRA_SECTIONS
  - PR_ATTRIBUTION_TEXT
  - ADDITIONAL_INSTRUCTIONS_NOTE
-->
\${PREAMBLE_BLOCK}## Context
- \`git status\`: !\`git status\`
- \`git diff \${DEFAULT_BRANCH}...HEAD\`: !\`git diff \${DEFAULT_BRANCH}...HEAD\`

## Task
1. Create new branch if on \${DEFAULT_BRANCH}.
2. Commit changes using HEREDOC.
3. Push to remote.
4. Update or create PR using \`gh pr create\` with HEREDOC for body. Keep title under 70 chars.

Do this in a single message. Return PR URL.