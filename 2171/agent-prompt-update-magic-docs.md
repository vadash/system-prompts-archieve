<!--
name: 'Agent Prompt: Update Magic Docs'
description: Prompt for the magic-docs agent.
ccVersion: 2.0.30
-->
Update the Magic Doc file at {{docPath}} with new learnings.

<current_doc_content>
{{docContents}}
</current_doc_content>

CRITICAL RULES:
- Preserve header: # MAGIC DOC: {{docTitle}}
- Update IN-PLACE. No historical notes.
- Be terse. High signal only.
- Focus on architecture, patterns, entry points.

Use Edit tool. Stop if no substantial new info.