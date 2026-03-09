<!--
name: 'Skill: Create verifier skills'
description: >-
  Prompt for creating verifier skills for the Verify agent to automatically
  verify code changes
ccVersion: 2.1.69
-->
Use TodoWrite tool to track progress.

**Goal:** Create verification scripts (skills) for testing web UI, CLI, or API functionality. Do not create unit test verifiers.

**Phase 1:** Auto-detect project areas (web, CLI, API), frameworks, test tools.
**Phase 2:** Ask user about installing tools (Playwright, Chrome MCP). Run install if agreed.
**Phase 3:** Ask user for specific commands, URLs, ready-signals, auth requirements. Suggest name like `verifier-frontend-playwright`.
**Phase 4:** Write skill to `.claude/skills/<name>/SKILL.md`.

**Template:**
```markdown
---
name: <verifier-name>
description: <description based on type>
allowed-tools: <tools list>
---
# <Title>
Execute verification exactly as written.

## Setup Instructions
<How to start services>

## Authentication
<Login steps/secrets>

## Cleanup
<Close processes>
```