<!--
name: 'Data: Claude API reference — TypeScript'
description: >-
  TypeScript SDK reference including installation, client initialization, basic
  requests, thinking, and multi-turn conversation
ccVersion: 2.1.71
-->
# Claude API — TypeScript

## Installation & Initialization
\`\`\`bash
npm install @anthropic-ai/sdk
\`\`\`
\`\`\`typescript
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();
\`\`\`

## Basic Request
\`\`\`typescript
const response = await client.messages.create({
  model: "{{OPUS_ID}}", max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
});
\`\`\`

## Vision (Images)
\`\`\`typescript
content: [
  { type: "image", source: { type: "base64", media_type: "image/png", data: b64 } },
  { type: "text", text: "Describe this" }
]
\`\`\`

## Prompt Caching
\`\`\`typescript
// Auto-caches the last cacheable block
cache_control: { type: "ephemeral" }
\`\`\`

## Extended Thinking
\`\`\`typescript
// Opus 4.6 / Sonnet 4.6: adaptive thinking
thinking: { type: "adaptive" },
output_config: { effort: "high" }, // low|medium|high|max
\`\`\`

## Error Handling
Use exact classes: \`Anthropic.RateLimitError\`, \`Anthropic.APIError\`. Avoid string-matching error messages.

## Multi-Turn Conversations
API is stateless. Maintain \`Anthropic.MessageParam[]\`. Always append full \`response.content\` to preserve tool blocks and compactions.

## Compaction (Beta, Opus 4.6)
Use \`betas: ["compact-2026-01-12"]\` and \`context_management: { edits: [{ type: "compact_20260112" }] }\`. Always append the compaction block back in history.