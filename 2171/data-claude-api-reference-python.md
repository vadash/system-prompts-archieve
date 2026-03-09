<!--
name: 'Data: Claude API reference — Python'
description: >-
  Python SDK reference including installation, client initialization, basic
  requests, thinking, and multi-turn conversation
ccVersion: 2.1.71
-->
# Claude API — Python

## Installation & Initialization
```bash
pip install anthropic
```
```python
import anthropic
client = anthropic.Anthropic()
async_client = anthropic.AsyncAnthropic()
```

## Basic Request
```python
response = client.messages.create(
    model="{{OPUS_ID}}", max_tokens=1024, system="...",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Vision (Images)
```python
# Pass base64 data
content=[
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_data}},
    {"type": "text", "text": "Describe this"}
]
```

## Prompt Caching
```python
# Auto-caches the last cacheable block
cache_control={"type": "ephemeral"} 
```

## Extended Thinking
```python
# Opus 4.6 / Sonnet 4.6: adaptive thinking
thinking={"type": "adaptive"}
output_config={"effort": "high"} # low|medium|high|max
```

## Error Handling
```python
try:
    client.messages.create(...)
except anthropic.RateLimitError:
    pass # SDK retries automatically by default
except anthropic.APIError as e:
    print(f"Error {e.status_code}")
```

## Multi-Turn Conversations
API is stateless. Append `response.content` (not just text!) to history to preserve tool blocks and server-side states.

## Compaction (Beta, Opus 4.6)
When approaching 200K window, use `betas=["compact-2026-01-12"]` and `context_management={"edits": [{"type": "compact_20260112"}]}`. You MUST pass the `compaction` block back on subsequent requests.