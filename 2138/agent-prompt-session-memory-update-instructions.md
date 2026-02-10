<!--
name: 'Agent Prompt: Session memory update instructions'
description: Instructions for updating session memory files during conversations
ccVersion: 2.0.58
variables:
  - MAX_SECTION_TOKENS
-->
NOT part of user conversation. Update session notes file at {{notesPath}}.

Current contents:
<current_notes_content>
{{currentNotes}}
</current_notes_content>

ONLY task: use Edit tool to update notes file, then stop. Make multiple edits in parallel.

**CRITICAL RULES:**
- Maintain exact structure: all sections, headers, italic descriptions intact
- NEVER modify/delete section headers (# lines)
- NEVER modify/delete italic _section descriptions_ (template instructions)
- ONLY update content BELOW italic descriptions
- No references to note-taking process in notes
- Skip sections with no substantial new insights (no filler)
- Write DETAILED, INFO-DENSE content: file paths, function names, errors, commands
- For "Key results": include complete exact output requested
- Exclude info already in CLAUDE.md files
- Keep each section under ~${MAX_SECTION_TOKENS} tokens
- IMPORTANT: Always update "Current State" for continuity

Use Edit tool with file_path: {{notesPath}}

STRUCTURE: Each section has (1) header line, (2) italic description line. Preserve both exactly. Only update content after them.
