<!--
name: 'Data: Streaming reference — TypeScript'
description: >-
  TypeScript streaming reference including basic streaming and handling
  different content types
ccVersion: 2.1.63
-->
# Streaming — TypeScript

```typescript
const stream = client.messages.stream({
  model: "{{OPUS_ID}}", max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
});

stream.on("text", (text) => process.stdout.write(text));

// Handle completions and errors reliably
const finalMessage = await stream.finalMessage();
```

## Handling Content Types
```typescript
for await (const event of stream) {
  if (event.type === "content_block_delta") {
    if (event.delta.type === "thinking_delta") process.stdout.write(event.delta.thinking);
    if (event.delta.type === "text_delta") process.stdout.write(event.delta.text);
  }
}
```

## Tool Runner Streaming
Use `stream: true` in `toolRunner`. Iterate through message streams.