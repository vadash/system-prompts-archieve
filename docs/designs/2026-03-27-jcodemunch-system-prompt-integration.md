# jCodeMunch System Prompt Integration

Replace CLAUDE.md policy and PreToolUse hook enforcement with direct system prompt rewrites.
Keep only the PostToolUse index hook for automatic re-indexing after edits.

---

## Architecture

### Before (3 enforcement layers)

```
CLAUDE.md (soft)  -->  PreToolUse hooks (hard)  -->  PostToolUse hook (auto)
  routing policy       read guard, edit guard        index_file after edit
```

### After (2 enforcement layers)

```
System prompts (deep)  -->  PostToolUse hook (auto)
  routing built into         index_file after edit
  core instructions          (unchanged)
```

### What gets dropped

| Component | Reason |
|---|---|
| `~/.claude/CLAUDE.md` jCodeMunch policy | Replaced by system prompt rewrites |
| PreToolUse read guard (`jcodemunch_read_guard.sh`) | Replaced by prompt routing |
| PreToolUse edit guard (`jcodemunch_edit_guard.sh`) | Replaced by prompt routing |

### What stays

| Component | Reason |
|---|---|
| PostToolUse index hook (`jcodemunch_index_hook.sh`) | Auto re-index is free — no model load, no tool call, never forgets |

---

## Design Principles

1. **Code files** (.ts .js .tsx .jsx .py .go .rs .java .rb .php .cs .cpp .c .h .swift .kt .scala .sql etc.) route to jCodeMunch
2. **Non-code files** (.md .json .yaml .toml .env .txt .html .xml .csv images PDFs) use native tools (Read, Grep, Glob)
3. **Read is not blocked** — Edit/Write need file content in context, and Read is the standard way to get it
4. **Read is deprioritized for code exploration** — model should reach for get_file_outline / get_symbol_source first
5. **Session lifecycle** (resolve_repo, suggest_queries) lives in the "read first" fragment
6. **Post-edit indexing** handled by hook, not by prompt instruction — zero model overhead
7. **Preserve all `<!-- -->` headers** exactly — only rewrite content below them
8. **Preserve all template variables** (`${READ_TOOL_NAME}`, `${GREP_TOOL_NAME}`, etc.) — they resolve at runtime

---

## Files to Rewrite (8 total)

All files are in `2174/`. Headers (YAML frontmatter in `<!-- -->`) are preserved exactly as-is.
Only the content below the closing `-->` is replaced.

---

### 1. `system-prompt-tool-usage-read-files.md`

**Original:**
```
To read files use ${READ_TOOL_NAME} instead of cat, head, tail, or sed
```

**New:**
```
Before reading any source code file, call jCodeMunch get_file_outline to see its structure first. To read specific symbols, use get_symbol_source (single symbol_id or batch symbol_ids[]) or get_context_bundle (symbol + its imports) instead of reading the whole file. Use ${READ_TOOL_NAME} for non-code files (.md, .json, .yaml, .toml, .env, .txt, .html, images, PDFs) and when you need complete file content before editing. Never use cat, head, tail, or sed to read any file.
```

**Why:** Redirect code exploration to jCodeMunch while keeping Read available for non-code and pre-edit reads.

---

### 2. `system-prompt-tool-usage-search-content.md`

**Original:**
```
To search the content of files, use ${GREP_TOOL_NAME} instead of grep or rg
```

**New:**
```
To search code by symbol name (function, class, method, variable), use jCodeMunch search_symbols — narrow with kind=, language=, file_pattern=. To search for strings, comments, TODOs, or patterns in source code, use jCodeMunch search_text (supports regex via is_regex, context_lines for surrounding code). For database columns in dbt/SQLMesh projects, use search_columns. Use ${GREP_TOOL_NAME} only for searching non-code file content (.md, .json, .yaml, .txt, .env, config files). Never invoke grep or rg via Bash.
```

**Why:** Grep becomes the non-code fallback. jCodeMunch handles all code content search.

---

### 3. `system-prompt-tool-usage-search-files.md`

**Original:**
```
To search for files use ${GLOB_TOOL_NAME} instead of find or ls
```

**New:**
```
To browse code project structure, use jCodeMunch get_file_tree (filter with path_prefix) or get_repo_outline for a high-level overview of directories, languages, and symbol counts. Use ${GLOB_TOOL_NAME} when finding files by name pattern. Never use find or ls via Bash for file discovery.
```

**Why:** Glob stays for pattern matching (e.g. "find all *.test.ts files"). Structure browsing routes to jCodeMunch.

---

### 4. `system-prompt-tool-usage-reserve-bash.md`

**Original:**
```
Reserve using the ${BASH_TOOL_NAME} exclusively for system commands and terminal operations that require shell execution. If you are unsure and there is a relevant dedicated tool, default to using the dedicated tool and only fallback on using the ${BASH_TOOL_NAME} tool for these if it is absolutely necessary.
```

**New:**
```
Reserve ${BASH_TOOL_NAME} exclusively for system commands and terminal operations: builds, tests, git, package managers, docker, kubectl, and similar. Never use ${BASH_TOOL_NAME} for code exploration — do not run grep, rg, find, cat, head, or tail on source code files through it. Use jCodeMunch MCP tools for all code reading and searching. If unsure whether a dedicated tool exists, default to the dedicated tool.
```

**Why:** Explicit prohibition of code exploration via Bash. The original was vague ("if you are unsure..."); this names the specific commands to avoid.

---

### 5. `system-prompt-tool-usage-direct-search.md`

**Original:**
```
For simple, directed codebase searches (e.g. for a specific file/class/function) use ${SEARCH_TOOLS} directly.
```

**New:**
```
For directed codebase searches (finding a specific function, class, or method), use jCodeMunch search_symbols directly — it is faster and more precise than text search. For text pattern searches in code, use jCodeMunch search_text. Use ${SEARCH_TOOLS} only when searching non-code file content.
```

**Why:** This is the "quick search" instruction. jCodeMunch search_symbols is the direct replacement for Grep-based symbol hunting.

---

### 6. `system-prompt-tool-usage-delegate-exploration.md`

**Original:**
```
For broader codebase exploration and deep research, use the ${TASK_TOOL_NAME} tool with subagent_type=${EXPLORE_SUBAGENT.agentType}. This is slower than using ${SEARCH_TOOLS} directly, so use this only when a simple, directed search proves to be insufficient or when your task will clearly require more than ${QUERY_LIMIT} queries.
```

**New:**
```
For broader codebase exploration, start with jCodeMunch: get_repo_outline for project overview, get_file_tree to browse structure, suggest_queries when the repo is unfamiliar. For deep research requiring more than ${QUERY_LIMIT} queries, use the ${TASK_TOOL_NAME} tool with subagent_type=${EXPLORE_SUBAGENT.agentType} — instruct subagents to prefer jCodeMunch over ${SEARCH_TOOLS} for source code exploration.
```

**Why:** jCodeMunch becomes the first step for broad exploration. Subagents are the second step, and they should also use jCodeMunch.

---

### 7. `system-prompt-tool-usage-subagent-guidance.md`

**Original:**
```
Use the ${TASK_TOOL_NAME} tool with specialized agents when the task at hand matches the agent's description. Subagents are valuable for parallelizing independent queries or for protecting the main context window from excessive results, but they should not be used excessively when not needed. Importantly, avoid duplicating work that subagents are already doing - if you delegate research to a subagent, do not also perform the same searches yourself.
```

**New:**
```
Use the ${TASK_TOOL_NAME} tool with specialized agents when the task matches the agent's description. Subagents are valuable for parallelizing independent queries or for protecting the main context window from excessive results, but should not be used excessively. When delegating code exploration to subagents, instruct them to use jCodeMunch MCP tools (search_symbols, get_symbol_source, get_file_outline) rather than Read, Grep, or Glob for source code. Avoid duplicating work that subagents are already doing.
```

**Why:** Subagents inherit no prompt context about jCodeMunch — the delegation instruction must tell them explicitly.

---

### 8. `system-prompt-doing-tasks-read-first.md`

**Original:**
```
In general, do not propose changes to code you haven't read. If a user asks about or wants you to modify a file, read it first. Understand existing code before suggesting modifications.
```

**New:**
```
Do not propose changes to code you haven't understood. Before modifying code, use jCodeMunch to build context: get_file_outline to see the file's structure, get_symbol_source or get_context_bundle to read the relevant symbols, and get_blast_radius or find_references to understand the impact of your changes.

At the start of a coding session, call resolve_repo with the current directory to confirm the project is indexed. If not indexed, call index_folder. When a repo is unfamiliar, call suggest_queries for orientation.

For non-code files (.md, .json, .yaml, .toml, .env, .txt, .html), use Read directly.
```

**Why:** This is the natural home for the session start ritual and the "understand before editing" workflow. The original said "read it first" — the new version says "understand it first" with specific jCodeMunch tools for impact analysis.

---

## Files NOT Modified

| File | Why untouched |
|---|---|
| `tool-usage-edit-files` | Post-edit indexing handled by hook, not prompt |
| `tool-usage-create-files` | Write tool routing unchanged |
| `tool-usage-skill-invocation` | Unrelated to code exploration |
| `tool-usage-task-management` | Unrelated to code exploration |
| `tool-description-readfile` | Heavier template variables, version-sensitive, not worth the risk |
| `tool-description-grep` | Same |
| `tool-description-glob` | Same |
| All `tool-description-bash-*` | Same — 30+ fragments, high churn risk |

---

## Hook Configuration

### Keep: PostToolUse index hook

The `jcodemunch_index_hook.sh` script stays as documented in AGENT_HOOKS.md.
No changes to the script itself.

### Simplified `~/.claude/settings.json` hooks section

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{
          "type": "command",
          "command": "CLAUDE_TOOL_NAME={{tool_name}} ~/.claude/hooks/jcodemunch_index_hook.sh"
        }]
      }
    ]
  }
}
```

All `PreToolUse` entries are removed. The read guard and edit guard scripts can be deleted from `~/.claude/hooks/`.

---

## Verification

### Manual check: prompt rendering

After copying the rewritten files and restarting Claude Code, the system prompt should contain the new text. Verify by asking Claude Code to explain its code exploration approach — it should describe jCodeMunch tools, not native Read/Grep/Glob.

### Behavioral tests

| Test | Expected behavior |
|---|---|
| "Find the main function in this project" | Uses search_symbols, not Grep |
| "What does UserService do?" | Uses get_file_outline + get_symbol_source, not Read |
| "Show me the project structure" | Uses get_file_tree, not Glob or ls |
| "Search for TODO comments" | Uses search_text, not Grep |
| "Read the README" | Uses Read (non-code file) |
| "Search package.json for the version" | Uses Grep or Read (non-code file) |
| Edit a .ts file | PostToolUse hook fires, re-indexes automatically |
| Start a new session | Calls resolve_repo first |

### Failure mode

If the model still reaches for native tools on code files, the prompt rewrites aren't strong enough. Options:
1. Strengthen wording (add "NEVER" / "ALWAYS")
2. Add tool description modifications (Approach C from the design phase)
3. Re-enable the PreToolUse read guard hook as a safety net

---

## Rollback

To revert: restore original files from any prior archive snapshot, remove the rewritten versions, restore CLAUDE.md and hook scripts. The 2174/ archive serves as the baseline.
