# Design: 2138 Prompt Optimization

## 1. Problem Statement

2138 prompts have excessive bloat:
- Verbose examples in tool descriptions
- Redundant explanations and corpo speak
- Malware/security warnings polluting context
- Plan mode files that should be handled by skill system

## 2. Goals & Non-Goals

**Must do:**
- Preserve all `<!-- name: description: ccVersion: variables: -->` headers
- Preserve template variables and special characters (backslash escapes, etc.)
- Clear file contents to essentials, don't delete files
- Process in batches of up to 10 files
- Use 2101 as style reference (concise, no examples), not 1:1 copy

**Won't do:**
- Delete any files (headers must stay)
- Modify metadata headers
- Copy 2101 content directly - analyze each 2138 file's purpose

## 3. File Groups (Process in Order)

### Group 1: Pure Bloat - Clear to Headers Only

These files serve no functional purpose - clear everything after header:

```
system-reminder-malware-analysis-after-read-tool-call.md
system-reminder-hook-additional-context.md
system-reminder-hook-blocking-error.md
system-reminder-hook-stopped-continuation.md
system-reminder-hook-stopped-continuation-prefix.md
system-reminder-hook-success.md
system-reminder-invoked-skills.md
system-reminder-todo-list-changed.md
system-reminder-todo-list-empty.md
system-reminder-todowrite-reminder.md
```

**Action:** Keep header only, delete all content after `-->`

### Group 2: Plan Mode Files (Replace with Skill)

These will be handled by new plan mode skill - clear to minimal:

```
tool-description-enterplanmode.md
tool-description-exitplanmode.md
system-reminder-plan-mode-is-active-5-phase.md
system-reminder-plan-mode-is-active-iterative.md
system-reminder-plan-mode-is-active-subagent.md
system-reminder-exited-plan-mode.md
system-reminder-plan-mode-re-entry.md
agent-prompt-plan-mode-enhanced.md
```

**Action:** Keep header, replace content with minimal reminder:
```markdown
Plan mode is active.
```

### Group 3: Main System Prompt

**File:** `system-prompt-main-system-prompt.md`

**Current bloat to remove:**
- Complex feedback section with multiple template variables
- Redundant security policy mentions
- Malware warning in system reminder

**Keep:**
- Core identity: "You are an interactive CLI tool..."
- `${OUTPUT_STYLE_CONFIG}` template usage
- Simple feedback: `/help` and issue URL

### Group 4: Tool Descriptions (Batch 1)

```
tool-description-readfile.md
tool-description-edit.md
tool-description-grep.md
tool-description-glob.md
tool-description-write.md
```

**Pattern to apply:**
- Remove excessive examples
- Remove verbose explanations of edge cases
- Keep: what it does, key params, critical warnings only
- Preserve all `${VARIABLE}` references

### Group 5: Tool Descriptions (Batch 2)

```
tool-description-bash.md
tool-description-task.md
tool-description-taskcreate.md
tool-description-webfetch.md
tool-description-websearch.md
```

**Pattern:**
- Bash: Remove quoting examples, directory verification steps
- Task: Remove 5-phase explanation, agent launch examples
- Web*: Remove cache explanations, keep core functionality

### Group 6: System Reminders - Delete Content

```
system-reminder-token-usage.md
system-reminder-usd-budget.md
system-reminder-output-token-limit-exceeded.md
system-reminder-team-coordination.md
system-reminder-team-shutdown.md
system-reminder-agent-mention.md
system-reminder-btw-side-question.md
```

**Action:** Header only, no content

### Group 7: System Reminders - Keep Minimal

```
system-reminder-file-exists-but-empty.md
system-reminder-file-modified-externally.md
system-reminder-file-opened-in-ide.md
system-reminder-file-shorter-than-offset.md
system-reminder-file-truncated.md
system-reminder-new-diagnostics-detected.md
```

**Action:** One-line reminder only

### Group 8: Agent Prompts

```
agent-prompt-explore.md
agent-prompt-task-tool.md
agent-prompt-task-tool-extra-notes.md
agent-prompt-command-execution-specialist.md
```

**Pattern:** Remove verbose guidelines, keep core instructions

### Group 9: Skills

```
skill-debugging.md
skill-update-claude-code-config.md
skill-verification-specialist.md
```

**Action:** Keep - these are actual skill implementations

### Group 10: Remaining Files

Process remaining agent prompts, data files, and tool descriptions not covered above.

## 4. Preservation Rules

**Must preserve exactly:**
- Template variable syntax: `${VARIABLE_NAME}`, `${FUNCTION()}`, `${CONDITION?true:false}`
- Backslash escapes: `\\`, `\"`, `\` (in code blocks)
- Header structure: `<!-- name: ... -->`
- Line number format references: "spaces + line number + tab"

## 5. Example Transformation

### Before (2138 tool-description-edit.md):
```markdown
<!--
name: 'Tool Description: Edit'
description: 'Performs exact string replacements in files'
variables:
  - READ_TOOL_NAME
-->

Performs exact string replacements in files.

Usage:
- You must use your `${READ_TOOL_NAME}` tool at least once in the conversation before editing.
- When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix (spaces + line number + tab). Everything after that tab is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
- This tool uses literal string matching. Case matters, spacing matters, indentation matters.
...
```

### After (optimized):
```markdown
<!--
name: 'Tool Description: Edit'
description: 'Performs exact string replacements in files'
variables:
  - READ_TOOL_NAME
-->

Performs exact string replacements in files.

Usage:
- You must use your `${READ_TOOL_NAME}` tool at least once in the conversation before editing.
- When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix (spaces + line number + tab).
```

## 6. Implementation Order

1. **Group 1** - Pure bloat files (clear to header only)
2. **Group 2** - Plan mode files (minimal for skill override)
3. **Group 3** - Main system prompt
4. **Group 4-5** - Tool descriptions (simplify)
5. **Group 6-7** - System reminders (clear or minimize)
6. **Group 8-10** - Remaining files

## 7. Validation

After each group:
- [ ] Headers intact (name, description, ccVersion, variables)
- [ ] Template variables preserved
- [ ] Special characters/escapes preserved
- [ ] Content is concise (no examples, minimal explanations)
