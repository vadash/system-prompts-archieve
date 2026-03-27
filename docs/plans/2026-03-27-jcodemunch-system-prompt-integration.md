# jCodeMunch System Prompt Integration — Implementation Plan

**Goal:** Rewrite 8 Claude Code system prompt files to route code exploration through jCodeMunch MCP tools, keep only the PostToolUse index hook, drop CLAUDE.md policy and PreToolUse hooks.

**Architecture:** The 8 files live in `2174/` (the tweakcc prompt archive). Each file has a YAML frontmatter header in `<!-- -->` comments that must be preserved exactly. Only the content below the closing `-->` is replaced. After rewriting, the user copies the files to wherever tweakcc expects them and restarts Claude Code.

**Tech Stack:** Plain markdown files with tweakcc template variables (`${READ_TOOL_NAME}`, `${GREP_TOOL_NAME}`, etc.)

**Common Pitfalls:**
- Do NOT modify anything inside `<!-- -->` headers — tweakcc uses these for identification and hashing
- Template variables like `${READ_TOOL_NAME}` must appear literally — they are resolved at runtime by Claude Code, not by you
- The `${EXPLORE_SUBAGENT.agentType}` variable uses dot notation — preserve it exactly including the dot
- Files must end with a single newline after the content — no trailing blank lines
- When copying to the active prompts directory, ensure the filename is identical

---

### Task 1: Rewrite `system-prompt-tool-usage-read-files.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-read-files.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (read files)'
description: Prefer Read tool instead of cat/head/tail/sed
ccVersion: 2.1.53
variables:
  - READ_TOOL_NAME
-->
Before reading any source code file, call jCodeMunch get_file_outline to see its structure first. To read specific symbols, use get_symbol_source (single symbol_id or batch symbol_ids[]) or get_context_bundle (symbol + its imports) instead of reading the whole file. Use ${READ_TOOL_NAME} for non-code files (.md, .json, .yaml, .toml, .env, .txt, .html, images, PDFs) and when you need complete file content before editing. Never use cat, head, tail, or sed to read any file.
```

- [ ] Step 2: Verify header is unchanged and `${READ_TOOL_NAME}` appears literally

---

### Task 2: Rewrite `system-prompt-tool-usage-search-content.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-search-content.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (search content)'
description: Prefer Grep tool instead of grep or rg
ccVersion: 2.1.53
variables:
  - GREP_TOOL_NAME
-->
To search code by symbol name (function, class, method, variable), use jCodeMunch search_symbols — narrow with kind=, language=, file_pattern=. To search for strings, comments, TODOs, or patterns in source code, use jCodeMunch search_text (supports regex via is_regex, context_lines for surrounding code). For database columns in dbt/SQLMesh projects, use search_columns. Use ${GREP_TOOL_NAME} only for searching non-code file content (.md, .json, .yaml, .txt, .env, config files). Never invoke grep or rg via Bash.
```

- [ ] Step 2: Verify header is unchanged and `${GREP_TOOL_NAME}` appears literally

---

### Task 3: Rewrite `system-prompt-tool-usage-search-files.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-search-files.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (search files)'
description: Prefer Glob tool instead of find or ls
ccVersion: 2.1.53
variables:
  - GLOB_TOOL_NAME
-->
To browse code project structure, use jCodeMunch get_file_tree (filter with path_prefix) or get_repo_outline for a high-level overview of directories, languages, and symbol counts. Use ${GLOB_TOOL_NAME} when finding files by name pattern. Never use find or ls via Bash for file discovery.
```

- [ ] Step 2: Verify header is unchanged and `${GLOB_TOOL_NAME}` appears literally

---

### Task 4: Rewrite `system-prompt-tool-usage-reserve-bash.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-reserve-bash.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (reserve Bash)'
description: Reserve Bash tool exclusively for system commands and terminal operations
ccVersion: 2.1.53
variables:
  - BASH_TOOL_NAME
-->
Reserve ${BASH_TOOL_NAME} exclusively for system commands and terminal operations: builds, tests, git, package managers, docker, kubectl, and similar. Never use ${BASH_TOOL_NAME} for code exploration — do not run grep, rg, find, cat, head, or tail on source code files through it. Use jCodeMunch MCP tools for all code reading and searching. If unsure whether a dedicated tool exists, default to the dedicated tool.
```

- [ ] Step 2: Verify header is unchanged and both `${BASH_TOOL_NAME}` references appear literally

---

### Task 5: Rewrite `system-prompt-tool-usage-direct-search.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-direct-search.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (direct search)'
description: 'Use Glob/Grep directly for simple, directed searches'
ccVersion: 2.1.72
variables:
  - SEARCH_TOOLS
-->
For directed codebase searches (finding a specific function, class, or method), use jCodeMunch search_symbols directly — it is faster and more precise than text search. For text pattern searches in code, use jCodeMunch search_text. Use ${SEARCH_TOOLS} only when searching non-code file content.
```

- [ ] Step 2: Verify header is unchanged (note: description has single quotes around the value) and `${SEARCH_TOOLS}` appears literally

---

### Task 6: Rewrite `system-prompt-tool-usage-delegate-exploration.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-delegate-exploration.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (delegate exploration)'
description: Use Task tool for broader codebase exploration and deep research
ccVersion: 2.1.72
variables:
  - TASK_TOOL_NAME
  - EXPLORE_SUBAGENT
  - SEARCH_TOOLS
  - QUERY_LIMIT
-->
For broader codebase exploration, start with jCodeMunch: get_repo_outline for project overview, get_file_tree to browse structure, suggest_queries when the repo is unfamiliar. For deep research requiring more than ${QUERY_LIMIT} queries, use the ${TASK_TOOL_NAME} tool with subagent_type=${EXPLORE_SUBAGENT.agentType} — instruct subagents to prefer jCodeMunch over ${SEARCH_TOOLS} for source code exploration.
```

- [ ] Step 2: Verify header is unchanged and all four template variables appear literally: `${QUERY_LIMIT}`, `${TASK_TOOL_NAME}`, `${EXPLORE_SUBAGENT.agentType}`, `${SEARCH_TOOLS}`

---

### Task 7: Rewrite `system-prompt-tool-usage-subagent-guidance.md`

**Files:**
- Modify: `2174/system-prompt-tool-usage-subagent-guidance.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Tool usage (subagent guidance)'
description: Guidance on when and how to use subagents effectively
ccVersion: 2.1.53
variables:
  - TASK_TOOL_NAME
-->
Use the ${TASK_TOOL_NAME} tool with specialized agents when the task matches the agent's description. Subagents are valuable for parallelizing independent queries or for protecting the main context window from excessive results, but should not be used excessively. When delegating code exploration to subagents, instruct them to use jCodeMunch MCP tools (search_symbols, get_symbol_source, get_file_outline) rather than Read, Grep, or Glob for source code. Avoid duplicating work that subagents are already doing.
```

- [ ] Step 2: Verify header is unchanged and `${TASK_TOOL_NAME}` appears literally

---

### Task 8: Rewrite `system-prompt-doing-tasks-read-first.md`

**Files:**
- Modify: `2174/system-prompt-doing-tasks-read-first.md`

- [ ] Step 1: Overwrite the file with this exact content

```markdown
<!--
name: 'System Prompt: Doing tasks (read before modifying)'
description: Read and understand existing code before suggesting modifications
ccVersion: 2.1.53
-->
Do not propose changes to code you haven't understood. Before modifying code, use jCodeMunch to build context: get_file_outline to see the file's structure, get_symbol_source or get_context_bundle to read the relevant symbols, and get_blast_radius or find_references to understand the impact of your changes.

At the start of a coding session, call resolve_repo with the current directory to confirm the project is indexed. If not indexed, call index_folder. When a repo is unfamiliar, call suggest_queries for orientation.

For non-code files (.md, .json, .yaml, .toml, .env, .txt, .html), use Read directly.
```

- [ ] Step 2: Verify header is unchanged (note: this file has no variables section)

---

### Task 9: Commit all prompt rewrites

- [ ] Step 1: Review the diff to confirm only content below `-->` changed in each file

```bash
cd /c/Users/vadash/.tweakcc/system-prompts-archieve && git diff --stat
```

Expected: 8 files changed

- [ ] Step 2: Inspect one file to spot-check header preservation

```bash
git diff 2174/system-prompt-tool-usage-read-files.md
```

Expected: lines inside `<!-- -->` show NO changes, only content below

- [ ] Step 3: Commit

```bash
git add 2174/system-prompt-tool-usage-read-files.md 2174/system-prompt-tool-usage-search-content.md 2174/system-prompt-tool-usage-search-files.md 2174/system-prompt-tool-usage-reserve-bash.md 2174/system-prompt-tool-usage-direct-search.md 2174/system-prompt-tool-usage-delegate-exploration.md 2174/system-prompt-tool-usage-subagent-guidance.md 2174/system-prompt-doing-tasks-read-first.md && git commit -m "$(cat <<'EOF'
Rewrite 8 system prompts to route code exploration through jCodeMunch

- tool-usage-read-files: code → get_file_outline/get_symbol_source, non-code → Read
- tool-usage-search-content: code → search_symbols/search_text, non-code → Grep
- tool-usage-search-files: code structure → get_file_tree, patterns → Glob
- tool-usage-reserve-bash: explicit ban on grep/rg/find/cat for code via Bash
- tool-usage-direct-search: code → jCodeMunch, non-code → Glob/Grep
- tool-usage-delegate-exploration: jCodeMunch first, then subagent for deep research
- tool-usage-subagent-guidance: instruct subagents to use jCodeMunch for code
- doing-tasks-read-first: session start ritual + understand-before-edit workflow
EOF
)"
```

---
