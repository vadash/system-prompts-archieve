# Objective
Transform the uploaded prompt files for Claude Code `2.1.71` into a tweaked version using `2.1.38 tweaked` as the reference style, then output the modified `.md` files in batches.

# Task Instructions
1. Output files one by one.
2. Do not add extra comments or remarks such as `NEW` or `EDIT`.
3. Do not omit anything unnecessarily. If content should remain, include it fully, including comments copied from the old file when applicable.
4. Preserve all header content inside `<!-- XXX -->` comments exactly as written. Do not modify those header comments in any way.
   - These headers are used to rebuild Claude Code and reinsert prompts.
   - They will not appear in the resulting file, but they must still remain untouched in your output process.
5. Use `2.1.38 tweaked` as the general model for what “tweaking” means, but apply judgment when needed.
   - The reference may contain mistakes.
   - Use common sense rather than copying blindly.
6. If required source content or file context is missing, do not guess; only proceed on files whose contents are available, and explicitly mark any unavailable file as `[blocked]`.
7. Copy symbol escaping logic from original file

# Tweaking Goals
- Main goal: reduce prompt size in tokens.
- Character count does not matter; token count does.
- Remove unnecessary corporate-style instructions.
- Remove malware-warning-style instructions where appropriate.
- Reduce instruction conflicts, since conflicting instructions make Claude Code perform worse.
- Reduce or remove examples where possible if they are not necessary.

# Environment Constraints
- This Claude Code version will only be used on a Windows machine.
- Terminal target is `PowerShell 7.5.4`.
- Adapt prompt content accordingly.
- This is a personal copy for private use.

# File Retention Rules
- Do not remove files entirely.
- If needed, a file may be reduced to only its header and nothing else.
- Example: `system-reminder-malware-analysis-after-read-tool-call.md` was handled this way.

# Required Logic to Preserve
- Keep the instruction to read a file before updating it.
- Remove planning-related instructions, including references to entering planning mode, exiting planning mode, planning itself, and similar planning workflow instructions.
- Claude should ideally not know about planning at all.
- However, keep the logic for adding Tasks, editing them, and related task-management behavior.
- Preserving task logic is important.

# Output Requirements
- Output the first batch of Markdown files.
- Target approximately `16k–20k` tokens total for the batch.
- Order files alphabetically.
- Return only the file outputs for the batch, in alphabetical order, with no extra commentary.
- Treat the batch as incomplete until all files intended for the first batch are included or explicitly marked `[blocked]`.
- Before finalizing, verify header comments are unchanged, required preserved logic remains, planning-related instructions are removed, and the batch stays near the target token range.

Out