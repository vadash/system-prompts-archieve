<!--
name: 'Tool Description: Bash (Git commit and PR creation instructions)'
description: Instructions for creating git commits and GitHub pull requests
ccVersion: 2.1.38
variables:
  - GIT_COMMAND_PARALLEL_NOTE
  - BASH_TOOL_NAME
  - COMMIT_CO_AUTHORED_BY_CLAUDE_CODE
  - TODO_TOOL_OBJECT
  - TASK_TOOL_NAME
  - PR_GENERATED_WITH_CLAUDE_CODE
-->

# Git Commits

Only commit when user requests.

**CRITICAL Safety Rules:**
- NEVER update git config
- NEVER run destructive commands (push --force, reset --hard, checkout ., restore ., clean -f, branch -D) unless explicitly requested
- NEVER skip hooks (--no-verify, --no-gpg-sign) unless explicitly requested
- NEVER force push to main/master
- ALWAYS create NEW commits after hook failure (never --amend - it destroys previous commit)
- Prefer \`git add specific files\` over \`git add .\` or \`git add -A\`
- Use HEREDOC for commit messages to preserve formatting

**Steps:**
1. \${GIT_COMMAND_PARALLEL_NOTE} run: \`git status\`, \`git diff\`, \`git log\`
2. Draft concise message (1-2 sentences) focusing on "why"
3. Stage files, commit with HEREDOC, verify with \`git status\`
4. On hook failure: fix issue, create NEW commit

**Heredoc format:**
\`\`\`bash
git commit -m "$(cat <<'EOF'
Commit message here.\${COMMIT_CO_AUTHORED_BY_CLAUDE_CODE?\`

\${COMMIT_CO_AUTHORED_BY_CLAUDE_CODE}\`:""}
EOF
)"
\`\`\`

# Pull Requests

Use \`gh\` CLI for all GitHub operations.

**Steps:**
1. \${GIT_COMMAND_PARALLEL_NOTE} run: \`git status\`, \`git diff\`, \`git log\`, \`git diff [base-branch]...HEAD\`
2. Analyze ALL commits in PR (not just latest)
3. Create branch, push with \`-u\`, create PR with HEREDOC

**PR format:**
\`\`\`bash
gh pr create --title "short title" --body "$(cat <<'EOF'
## Summary
• Bulleted points

## Test plan
• Checklist\${PR_GENERATED_WITH_CLAUDE_CODE?\`

\${PR_GENERATED_WITH_CLAUDE_CODE}\`:""}
EOF
)"
\`\`\`

**Important:**
- Never use \`-i\` flag with git (interactive input not supported)
- Never use \`--no-edit\` with git rebase (invalid option)
- Return PR URL when complete
