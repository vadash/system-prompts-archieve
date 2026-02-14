# Design: patch-prompts.ps1

## 1. Problem Statement

\`tweakcc --apply\` fails when system prompt \`.md\` files contain unescaped backticks.
Files may also have Windows CRLF line endings that cause issues.
A patcher script is needed to fix these problems in bulk before applying.

## 2. Goals & Non-Goals

**Must do:**
- Accept a directory path (prompt interactively if not provided via \`-Path\`)
- Escape unescaped backticks in \`.md\` files (\`\` \` \`\` → \`\` \` \`\`)
- Convert CRLF to LF line endings in all text files
- Extensible design: easy to add new fixers
- Print summary of changes per fixer
- Don't overfix: skip already-escaped backticks, skip files that are already LF

**Won't do:**
- Dry-run mode (apply immediately)
- Recursive plugin discovery
- Backup/rollback mechanism

## 3. Proposed Architecture

Single script \`utils/patch-prompts.ps1\` with an ordered array of fixer objects.

\`\`\`
Script startup
  → Resolve -Path (or prompt user)
  → Validate path exists
  → Collect files (skip binary extensions, skip .git/node_modules)
  → Run each fixer in order against matching files
  → Print per-fixer and total summary
\`\`\`

**Fixer pipeline:**
1. **Escape backticks** — \`.md\` files only. Regex: replace \`\` \` \`\` not preceded by \`\`.
2. **Fix line endings** — All text files. Replace \`\r\n\` with \`\n\`.

The old \`utils/fix-line-endings.ps1\` is deleted — its logic is absorbed into fixer #2.

## 4. Data Models

Each fixer is a \`[PSCustomObject]\`:

\`\`\`powershell
[PSCustomObject]@{
    Name   = [string]    # Display name for summary
    Filter = [string]    # File extension filter ("*.md" or "*")
    Action = [scriptblock] # Receives file path, returns $true if file was modified
}
\`\`\`

## 5. Interface / API Design

\`\`\`powershell
# With parameter
.\utils\patch-prompts.ps1 -Path "C:\Users\vadash\.tweakcc\system-prompts"

# Interactive (prompts for path)
.\utils\patch-prompts.ps1
\`\`\`

**Parameters:**
- \`-Path [string]\` — Target directory. If omitted, script prompts via \`Read-Host\`.

**Output:**
\`\`\`
Scanning 'C:\...\system-prompts' ...
Found 42 files.

[Escape backticks] Processing 28 .md files...
  [FIXED] skill-debugging.md (14 backticks escaped)
  [FIXED] agent-prompt-bash-command-prefix-detection.md (2 backticks escaped)

[Fix line endings] Processing 42 files...
  [FIXED] skill-debugging.md
  [FIXED] README.md

Summary:
  Escape backticks:  2 files fixed
  Fix line endings:  5 files fixed
  Total files:       42
\`\`\`

## 6. Risks & Edge Cases

- **Already-escaped backticks**: Regex uses negative lookbehind \`(?<!\\)\` to skip \`\`\` — prevents double-escaping.
- **Backticks inside code blocks**: These still get escaped. tweakcc requires ALL backticks escaped, including those in fenced code blocks (the log confirms \`\`\` \`\`\` \`\`\` itself triggers errors). This is correct behavior.
- **Binary files**: Skipped via extension list (same as fix-line-endings.ps1).
- **Empty files**: Read returns empty string — no modification needed, skip gracefully.
- **Read-only files**: \`$ErrorActionPreference = "Continue"\` — log error, continue to next file.
