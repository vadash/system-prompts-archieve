<!--
name: 'Data: Files API reference — Python'
description: >-
  Python Files API reference including file upload, listing, deletion, and usage
  in messages
ccVersion: 2.1.63
-->
# Files API — Python

Use `betas=["files-api-2025-04-14"]`. Max 500MB per file.

## Upload & Use
```python
uploaded = client.beta.files.upload(
    file=("report.pdf", open("report.pdf", "rb"), "application/pdf")
)

response = client.beta.messages.create(
    model="{{OPUS_ID}}", max_tokens=1024,
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Summarize"},
        {"type": "document", "source": {"type": "file", "file_id": uploaded.id}}
    ]}],
    betas=["files-api-2025-04-14"]
)
```

## Manage
```python
files = client.beta.files.list()
client.beta.files.delete(uploaded.id)
file_content = client.beta.files.download(file_id) # Only for code-execution outputs
```