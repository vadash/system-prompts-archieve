<!--
name: 'Data: Message Batches API reference — Python'
description: >-
  Python Batches API reference including batch creation, status polling, and
  result retrieval at 50% cost
ccVersion: 2.1.63
-->
# Message Batches API — Python

\`POST /v1/messages/batches\` processes API requests asynchronously at 50% of standard prices.
- Up to 100,000 requests or 256 MB per batch
- Results available for 29 days

## Create a Batch
\`\`\`python
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = anthropic.Anthropic()
batch = client.messages.batches.create(
    requests=[
        Request(
            custom_id="req-1",
            params=MessageCreateParamsNonStreaming(
                model="{{OPUS_ID}}", max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}]
            )
        )
    ]
)
print(batch.id)
\`\`\`

## Poll for Completion
\`\`\`python
import time
while True:
    batch = client.messages.batches.retrieve(batch.id)
    if batch.processing_status == "ended": break
    time.sleep(60)
\`\`\`

## Retrieve Results
\`\`\`python
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        print(f"[{result.custom_id}] {result.result.message.content[0].text[:100]}")
    elif result.result.type == "errored":
        print(f"[{result.custom_id}] Error: {result.result.error.type}")
\`\`\`

## Cancel a Batch
\`\`\`python
client.messages.batches.cancel(batch.id)
\`\`\`

## Batch with Prompt Caching
\`\`\`python
shared_system = [{"type": "text", "text": "...", "cache_control": {"type": "ephemeral"}}]
# Apply this system array to params for cost savings
\`\`\`