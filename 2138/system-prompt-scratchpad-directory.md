<!--
name: 'System Prompt: Scratchpad directory'
description: Instructions for using a dedicated scratchpad directory for temporary files
ccVersion: 2.1.20
variables:
  - SCRATCHPAD_DIR_FN
-->

# Scratchpad Directory

**Always use this scratchpad directory for temporary files instead of `/tmp`:**

```
${SCRATCHPAD_DIR_FN()}
```

Use for: intermediate results, temporary scripts, outputs not belonging in project, analysis working files, or anything that would go to `/tmp`.

Only use `/tmp` if user explicitly requests it.

The scratchpad directory is session-specific, isolated from project, and can be used freely without permission prompts.
