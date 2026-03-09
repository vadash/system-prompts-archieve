<!--
name: 'Skill: Build with Claude API'
description: >-
  Main routing guide for building LLM-powered applications with Claude,
  including language detection, surface selection, and architecture overview
ccVersion: 2.1.63
-->
# Building LLM-Powered Applications with Claude

Default to model `{{OPUS_ID}}` unless explicitly requested. Use `thinking: {type: "adaptive"}` for complex requests. Use `.stream()` and `.finalMessage()` for reliability.

## Surface Selection
- **Single API Call:** Classification, Q&A, basic text.
- **Workflow:** Multi-step pipelines (API + tools).
- **Agent SDK:** Needs built-in file/web/terminal access or guardrails. Only available in Python/TS.

## Models
- `claude-opus-4-6` - Most intelligent. Adaptive thinking.
- `claude-sonnet-4-6` - Balanced. Adaptive thinking.
- `claude-haiku-4-5` - Fast, cheap.

**CRITICAL:** Never append dates to model names. Never use `budget_tokens` on 4.6 models. Use `thinking: {type: "adaptive"}`. Use `output_config: {format: {...}}` instead of deprecated `output_format`.

## Compaction (Opus 4.6 Beta)
For long conversations, use `compact-2026-01-12`. MUST append `response.content` (including compaction block) to history.