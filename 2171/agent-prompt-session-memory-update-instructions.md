<!--
name: 'Agent Prompt: Session memory update instructions'
description: Instructions for updating session memory files during conversations
ccVersion: 2.0.58
variables:
  - MAX_SECTION_TOKENS
-->
Update the session notes file at {{notesPath}}.

Current contents:
<current_notes_content>
{{currentNotes}}
</current_notes_content>

CRITICAL RULES:
- Maintain exact structure: NEVER modify section headers or italic descriptions.
- ONLY update content BELOW italic descriptions.
- Skip sections with no new insights.
- Write detailed, info-dense content.
- Always update "Current State".
- Keep sections under ~${MAX_SECTION_TOKENS} tokens.

Use the Edit tool in parallel and stop.