<!--
name: 'Data: Claude model catalog'
description: >-
  Catalog of current and legacy Claude models with exact model IDs, aliases,
  context windows, and pricing
ccVersion: 2.1.63
-->
# Claude Model Catalog

**Only use exact model IDs listed here.** Do not guess IDs or append dates unless listed.

## Current Models (recommended)
| Friendly Name     | Alias | Context | Max Output |
|-------------------|-------|---------|------------|
| Claude Opus 4.6   | `claude-opus-4-6` | 200K (1M beta) | 128K |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | 64K |
| Claude Haiku 4.5  | `claude-haiku-4-5` | 200K | 64K |

## Legacy/Deprecated Models
Use aliases: `claude-opus-4-5`, `claude-opus-4-1`, `claude-sonnet-4-5`, `claude-sonnet-4-0`, `claude-opus-4-0`.

## Mapping User Requests
- "opus", "most powerful", "opus 4.6": `claude-opus-4-6`
- "sonnet", "balanced", "sonnet 4.6": `claude-sonnet-4-6`
- "haiku", "fast", "cheap", "haiku 4.5": `claude-haiku-4-5`
- "sonnet 3.5", "sonnet 3.7": Suggest `claude-sonnet-4-5` or `claude-sonnet-4-6`