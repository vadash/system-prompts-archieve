<!--
name: 'Data: Files API reference — TypeScript'
description: >-
  TypeScript Files API reference including file upload, listing, deletion, and
  usage in messages
ccVersion: 2.1.63
-->
# Files API — TypeScript

Use `betas: ["files-api-2025-04-14"]`.

## Upload & Use
```typescript
import { toFile } from "@anthropic-ai/sdk";

const uploaded = await client.beta.files.upload({
  file: await toFile(fs.createReadStream("report.pdf"), undefined, { type: "application/pdf" }),
  betas: ["files-api-2025-04-14"]
});

await client.beta.messages.create({
  model: "{{OPUS_ID}}", max_tokens: 1024,
  messages: [{ role: "user", content: [
    { type: "text", text: "Summarize" },
    { type: "document", source: { type: "file", file_id: uploaded.id } }
  ]}],
  betas: ["files-api-2025-04-14"]
});
```