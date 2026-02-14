# Implementation Plan - 2138 Prompt Optimization

> **Reference:** \`docs/designs/2025-02-10-prompt-optimization-design.md\`
> **Execution:** Manual processing, up to 10 files per task/commit

---

## Style Reference (2101 Patterns)

- **Very concise** - No fluff, straight to point
- **No examples** - No illustrative usage examples
- **No greetings/niceties** - Technical content only
- **Bullet points for instructions** - Direct, actionable
- **CRITICAL/IMPORTANT markers** - For key warnings only
- **Extensive variable usage** - \`${VARIABLE_NAME}\` preserved
- **Platform notes** - Windows-specific where relevant

---

## Task 1: Pure Bloat Files (Clear to Headers Only)

**Goal:** Clear 10 files to header-only - these serve no functional purpose

**Files:**
1. \`system-reminder-malware-analysis-after-read-tool-call.md\`
2. \`system-reminder-hook-additional-context.md\`
3. \`system-reminder-hook-blocking-error.md\`
4. \`system-reminder-hook-stopped-continuation.md\`
5. \`system-reminder-hook-stopped-continuation-prefix.md\`
6. \`system-reminder-hook-success.md\`
7. \`system-reminder-invoked-skills.md\`
8. \`system-reminder-todo-list-changed.md\`
9. \`system-reminder-todo-list-empty.md\`
10. \`system-reminder-todowrite-reminder.md\`

**Action for each file:**
1. Read the file
2. Preserve header: \`<!-- name: description: ccVersion: variables: -->\`
3. Delete all content after \`-->\`
4. Write file with header only

**Git Commit:**
\`\`\`bash
git add 2138/system-reminder-*.md
git commit -m "opt: clear pure bloat system reminders to headers only"
\`\`\`

**Verification:**
- Headers intact (name, description, ccVersion, variables)
- No content after \`-->\`

---

## Task 2: System Reminders - Delete Content (Header Only)

**Goal:** Clear 8 more system reminder files to header-only

**Files:**
1. \`system-reminder-token-usage.md\`
2. \`system-reminder-usd-budget.md\`
3. \`system-reminder-output-token-limit-exceeded.md\`
4. \`system-reminder-team-coordination.md\`
5. \`system-reminder-team-shutdown.md\`
6. \`system-reminder-agent-mention.md\`
7. \`system-reminder-btw-side-question.md\`
8. \`system-reminder-delegate-mode-prompt.md\`

**Action:** Same as Task 1 - keep header only, delete all content

**Git Commit:**
\`\`\`bash
git add 2138/system-reminder-*.md
git commit -m "opt: clear token/budget/team system reminders to headers only"
\`\`\`

---

## Task 3: System Reminders - Keep Minimal One-Liners

**Goal:** Reduce 8 system reminders to single-line reminders

**Files:**
1. \`system-reminder-file-exists-but-empty.md\`
2. \`system-reminder-file-modified-externally.md\`
3. \`system-reminder-file-opened-in-ide.md\`
4. \`system-reminder-file-shorter-than-offset.md\`
5. \`system-reminder-file-truncated.md\`
6. \`system-reminder-new-diagnostics-detected.md\`
7. \`system-reminder-exited-delegate-mode.md\`
8. \`system-reminder-session-continuation.md\`

**Action for each file:**
1. Read the file
2. Preserve header
3. Reduce content to one-line reminder based on file purpose
4. Write file with minimal content

**Example transformation:**
\`\`\`markdown
<!-- name: 'System Reminder: File Exists But Empty' ... -->

File exists but is empty.
\`\`\`

**Git Commit:**
\`\`\`bash
git add 2138/system-reminder-*.md
git commit -m "opt: reduce system reminders to one-liners"
\`\`\`

---

## Task 4: Plan Mode Files (Minimal for Skill Override)

**Goal:** Reduce 9 plan mode files to minimal "Plan mode is active" text

**Files:**
1. \`tool-description-enterplanmode.md\`
2. \`tool-description-exitplanmode.md\`
3. \`system-reminder-plan-mode-is-active-5-phase.md\`
4. \`system-reminder-plan-mode-is-active-iterative.md\`
5. \`system-reminder-plan-mode-is-active-subagent.md\`
6. \`system-reminder-exited-plan-mode.md\`
7. \`system-reminder-plan-mode-re-entry.md\`
8. \`agent-prompt-plan-mode-enhanced.md\`
9. \`system-reminder-verify-plan-reminder.md\`

**Action for each file:**
1. Read the file
2. Preserve header and all variables
3. Replace content with minimal: "Plan mode is active."
4. Write file

**Git Commit:**
\`\`\`bash
git add 2138/tool-description-*planmode.md 2138/system-reminder-*plan*.md 2138/agent-prompt-plan-mode-enhanced.md
git commit -m "opt: minimize plan mode files for skill override"
\`\`\`

---

## Task 5: Main System Prompt

**Goal:** Optimize \`system-prompt-main-system-prompt.md\` - remove bloat, keep essentials

**File:**
1. \`system-prompt-main-system-prompt.md\`

**Remove:**
- Complex feedback section with multiple template variables
- Redundant security policy mentions
- Malware warning in system reminder
- Verbose explanations

**Keep:**
- Core identity: "You are an interactive CLI tool..."
- \`${OUTPUT_STYLE_CONFIG}\` template usage
- Simple feedback: \`/help\` and issue URL
- Essential tool usage notes
- Environment info format

**Action:**
1. Read current file and 2101 equivalent for reference
2. Analyze what's essential vs bloat
3. Write optimized version preserving all variables

**Git Commit:**
\`\`\`bash
git add 2138/system-prompt-main-system-prompt.md
git commit -m "opt: streamline main system prompt"
\`\`\`

---

## Task 6: Tool Descriptions - Read/Edit/Write/Glob/Grep

**Goal:** Simplify 5 core file tool descriptions

**Files:**
1. \`tool-description-readfile.md\`
2. \`tool-description-edit.md\`
3. \`tool-description-write.md\`
4. \`tool-description-glob.md\`
5. \`tool-description-grep.md\`

**Pattern to apply:**
- Remove excessive examples
- Remove verbose explanations of edge cases
- Keep: what it does, key params, critical warnings only
- Preserve all \`${VARIABLE}\` references

**Action for each file:**
1. Read current 2138 file
2. Read 2101 equivalent for style reference
3. Write optimized version:
  - One sentence description
  - Bullet points for key usage notes
  - CRITICAL warnings for important constraints
  - No examples

**Git Commit:**
\`\`\`bash
git add 2138/tool-description-readfile.md 2138/tool-description-edit.md 2138/tool-description-write.md 2138/tool-description-glob.md 2138/tool-description-grep.md
git commit -m "opt: simplify file tool descriptions"
\`\`\`

---

## Task 7: Tool Descriptions - Bash/Task/Web

**Goal:** Simplify execution and web tool descriptions

**Files:**
1. \`tool-description-bash.md\`
2. \`tool-description-task.md\`
3. \`tool-description-taskcreate.md\`
4. \`tool-description-webfetch.md\`
5. \`tool-description-websearch.md\`
6. \`tool-description-askuserquestion.md\`
7. \`tool-description-todowrite.md\`
8. \`tool-description-skill.md\`
9. \`tool-description-sleep.md\`
10. \`tool-description-notebookedit.md\`

**Pattern:**
- Bash: Remove quoting examples, directory verification steps
- Task: Remove 5-phase explanation, agent launch examples
- Web*: Remove cache explanations, keep core functionality
- All: Remove examples, keep concise usage notes

**Action:** Same pattern as Task 6

**Git Commit:**
\`\`\`bash
git add 2138/tool-description-{bash,task,taskcreate,webfetch,websearch,askuserquestion,todowrite,skill,sleep,notebookedit}.md
git commit -m "opt: simplify execution and web tool descriptions"
\`\`\`

---

## Task 8: Remaining Tool Descriptions

**Goal:** Simplify remaining tool descriptions

**Files:**
1. \`tool-description-bash-git-commit-and-pr-creation-instructions.md\`
2. \`tool-description-bash-sandbox-note.md\`
3. \`tool-description-computer.md\`
4. \`tool-description-lsp.md\`
5. \`tool-description-sendmessagetool.md\`
6. \`tool-description-tasklist-teammate-workflow.md\`
7. \`tool-description-teamdelete.md\`
8. \`tool-description-teammatetool.md\`
9. \`tool-description-toolsearch.md\`
10. \`tool-description-toolsearch-extended.md\`
11. \`tool-parameter-computer-action.md\`

**Action:** Simplify each following same pattern

**Git Commit:**
\`\`\`bash
git add 2138/tool-description-*.md
git commit -m "opt: simplify remaining tool descriptions"
\`\`\`

---

## Task 9: Agent Prompts - Explore/Task/Bash

**Goal:** Streamline core agent prompts

**Files:**
1. \`agent-prompt-explore.md\`
2. \`agent-prompt-task-tool.md\`
3. \`agent-prompt-task-tool-extra-notes.md\`
4. \`agent-prompt-command-execution-specialist.md\`
5. \`agent-prompt-bash-command-description-writer.md\`
6. \`agent-prompt-bash-command-file-path-extraction.md\`
7. \`agent-prompt-bash-command-prefix-detection.md\`
8. \`agent-prompt-session-search-assistant.md\`
9. \`agent-prompt-status-line-setup.md\`
10. \`agent-prompt-hook-condition-evaluator.md\`

**Pattern:**
- Remove verbose guidelines
- Keep core instructions
- No examples
- Concise bullet points

**Git Commit:**
\`\`\`bash
git add 2138/agent-prompt-{explore,task-tool,task-tool-extra-notes,command-execution-specialist,bash-*,session-search-assistant,status-line-setup,hook-condition-evaluator}.md
git commit -m "opt: streamline core agent prompts"
\`\`\`

---

## Task 10: Agent Prompts - Creation and Specialized

**Goal:** Streamline agent creation and specialized prompts

**Files:**
1. \`agent-prompt-agent-creation-architect.md\`
2. \`agent-prompt-agent-hook.md\`
3. \`agent-prompt-claude-guide-agent.md\`
4. \`agent-prompt-claudemd-creation.md\`
5. \`agent-prompt-conversation-summarization.md\`
6. \`agent-prompt-prompt-suggestion-generator-*.md\` (3 files)
7. \`agent-prompt-pr-comments-slash-command.md\`
8. \`agent-prompt-review-pr-slash-command.md\`
9. \`agent-prompt-security-review-slash-command.md\`
10. \`agent-prompt-update-magic-docs.md\`

**Git Commit:**
\`\`\`bash
git add 2138/agent-prompt-*.md
git commit -m "opt: streamline agent creation and specialized prompts"
\`\`\`

---

## Task 11: System Prompts - Memory and Learning

**Goal:** Streamline memory and learning related system prompts

**Files:**
1. \`system-prompt-agent-memory-instructions.md\`
2. \`system-prompt-agent-summary-generation.md\`
3. \`system-prompt-context-compaction-summary.md\`
4. \`system-prompt-learning-mode.md\`
5. \`system-prompt-learning-mode-insights.md\`
6. \`system-prompt-session-memory-update-instructions.md\`

**Git Commit:**
\`\`\`bash
git add 2138/system-prompt-agent-*.md 2138/system-prompt-context-*.md 2138/system-prompt-learning-*.md 2138/system-prompt-session-memory-*.md
git commit -m "opt: streamline memory and learning system prompts"
\`\`\`

---

## Task 12: System Prompts - Insights

**Goal:** Streamline insights-related system prompts

**Files:**
1. \`system-prompt-insights-at-a-glance-summary.md\`
2. \`system-prompt-insights-friction-analysis.md\`
3. \`system-prompt-insights-on-the-horizon.md\`
4. \`system-prompt-insights-session-facets-extraction.md\`
5. \`system-prompt-insights-suggestions.md\`
6. \`system-prompt-recent-message-summarization.md\`
7. \`system-prompt-session-title-and-branch-generation.md\`
8. \`system-prompt-user-sentiment-analysis.md\`
9. \`system-prompt-webfetch-summarizer.md\`

**Git Commit:**
\`\`\`bash
git add 2138/system-prompt-insights-*.md 2138/agent-prompt-recent-*.md 2138/agent-prompt-session-title-*.md 2138/agent-prompt-user-*.md 2138/agent-prompt-webfetch-*.md
git commit -m "opt: streamline insights system prompts"
\`\`\`

---

## Task 13: System Prompts - Task Execution

**Goal:** Streamline task execution related system prompts

**Files:**
1. \`system-prompt-doing-tasks.md\`
2. \`system-prompt-executing-actions-with-care.md\`
3. \`system-prompt-task-management.md\`
4. \`system-prompt-tool-execution-denied.md\`
5. \`system-prompt-tool-permission-mode.md\`
6. \`system-prompt-tool-usage-policy.md\`
7. \`system-prompt-tool-use-summary-generation.md\`
8. \`system-prompt-tone-and-style.md\`
9. \`system-prompt-parallel-tool-call-note.md\`

**Git Commit:**
\`\`\`bash
git add 2138/system-prompt-doing-tasks.md 2138/system-prompt-executing-*.md 2138/system-prompt-task-*.md 2138/system-prompt-tool-*.md 2138/system-prompt-tone-*.md 2138/system-prompt-parallel-*.md
git commit -m "opt: streamline task execution system prompts"
\`\`\`

---

## Task 14: System Prompts - MCP/Teammate/Other

**Goal:** Streamline remaining system prompts

**Files:**
1. \`system-prompt-chrome-browser-mcp-tools.md\`
2. \`system-prompt-claude-in-chrome-browser-automation.md\`
3. \`system-prompt-git-status.md\`
4. \`system-prompt-hooks-configuration.md\`
5. \`system-prompt-mcp-cli.md\`
6. \`system-prompt-scratchpad-directory.md\`
7. \`system-prompt-skillify-current-session.md\`
8. \`system-prompt-teammate-communication.md\`
9. \`system-prompt-censoring-assistance-with-malicious-activities.md\`

**Git Commit:**
\`\`\`bash
git add 2138/system-prompt-*.md
git commit -m "opt: streamline remaining system prompts"
\`\`\`

---

## Task 15: System Reminders - Remaining Files

**Goal:** Process remaining system reminders

**Files:**
1. \`system-reminder-compact-file-reference.md\`
2. \`system-reminder-lines-selected-in-ide.md\`
3. \`system-reminder-mcp-resource-*.md\` (2 files)
4. \`system-reminder-memory-file-contents.md\`
5. \`system-reminder-nested-memory-contents.md\`
6. \`system-reminder-output-style-active.md\`
7. \`system-reminder-plan-file-reference.md\`
8. \`system-reminder-task-status.md\`
9. \`system-reminder-task-tools-reminder.md\`

**Action:** Minimize to one-liners where possible

**Git Commit:**
\`\`\`bash
git add 2138/system-reminder-*.md
git commit -m "opt: minimize remaining system reminders"
\`\`\`

---

## Task 16: Skills

**Goal:** Review and optimize skill files (keep if they're actual implementations)

**Files:**
1. \`skill-debugging.md\`
2. \`skill-update-claude-code-config.md\`
3. \`skill-verification-specialist.md\`

**Action:** These are actual skill implementations - review but likely keep mostly intact, only removing excessive verbosity

**Git Commit:**
\`\`\`bash
git add 2138/skill-*.md
git commit -m "opt: streamline skill files"
\`\`\`

---

## Task 17: Data Files

**Goal:** Review and optimize data files

**Files:**
1. \`data-github-actions-workflow-for-claude-mentions.md\`
2. \`data-github-app-installation-pr-description.md\`
3. \`data-session-memory-template.md\`

**Action:** These may be reference data - review and minimize if verbose

**Git Commit:**
\`\`\`bash
git add 2138/data-*.md
git commit -m "opt: streamline data files"
\`\`\`

---

## File Count Summary

- **System Prompts:** 31 files
- **Tool Descriptions:** 28 files
- **System Reminders:** 40 files
- **Agent Prompts:** 29 files
- **Data Files:** 3 files
- **Skill Files:** 3 files
- **Total:** 134 files

---

## Validation Checklist

After all tasks complete:

- [ ] All headers intact (name, description, ccVersion, variables)
- [ ] All template variables preserved (\`${VARIABLE_NAME}\`)
- [ ] All special characters/escapes preserved (\`\\\\`, \`\\\"\`, etc.)
- [ ] Content is concise (no examples, minimal explanations)
- [ ] All files processed (134 total in 2138/)
- [ ] All commits pushed

---

## Notes

- 2101 is read-only reference only
- 2138 is read-write target
- Each task processes up to 10 related files
- Each task has its own git commit
- Use 2101 style guide: concise, no examples, direct instructions
