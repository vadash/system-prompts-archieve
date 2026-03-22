<!--
name: 'Data: Streaming reference — Python'
description: >-
  Python streaming reference including sync/async streaming and handling
  different content types
ccVersion: 2.1.63
-->
# Streaming — Python

\`\`\`python
with client.messages.stream(
    model="{{OPUS_ID}}", max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    
    # Get full message after streaming
    final_message = stream.get_final_message()
\`\`\`

## Handling Content Types (Thinking vs Text)
\`\`\`python
with client.messages.stream(
    model="{{OPUS_ID}}", max_tokens=16000, thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "Analyze"}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta": print(event.delta.thinking, end="")
            elif event.delta.type == "text_delta": print(event.delta.text, end="")
\`\`\`
