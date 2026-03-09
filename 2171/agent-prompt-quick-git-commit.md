<!--
name: 'Agent Prompt: Quick git commit'
description: Streamlined prompt for creating a single git commit with pre-populated context
ccVersion: 2.1.69
variables:
  - ATTRIBUTION_TEXT
-->
## Context
- Status: !\`git status\`
- Diff: !\`git diff HEAD\`
- Branch: !\`git branch --show-current\`

## Git Safety Protocol
- NEVER run destructive/irreversible git commands.
- ALWAYS create NEW commits. NEVER --amend unless requested.
- Do not commit secret files.

## Task
1. Draft a concise commit message.
2. Stage files and commit using HEREDOC:
\`\`\`
git commit -m "$(cat <<'EOF'
Commit message here.\${ATTRIBUTION_TEXT?\`\n\n\${ATTRIBUTION_TEXT}\`:""}
EOF
)"
\`\`\`
Do this in a single tool call message.