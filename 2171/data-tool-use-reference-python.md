<!--
name: 'Data: Tool use reference — Python'
description: >-
  Python tool use reference including tool runner, manual agentic loop, code
  execution, and structured outputs
ccVersion: 2.1.69
-->
# Tool Use — Python

## Tool Runner (Beta)
\`\`\`python
from anthropic import beta_tool
@beta_tool
def get_weather(location: str) -> str: return f"Sunny in {location}"

runner = client.beta.messages.tool_runner(
    model="{{OPUS_ID}}", max_tokens=4096, tools=[get_weather],
    messages=[{"role": "user", "content": "Weather in Paris?"}]
)
for msg in runner: print(msg)
\`\`\`

## Manual Loop
Append \`response.content\`, construct \`tool_result\` blocks matching \`tool_use_id\`, handle \`pause_turn\`.

## Structured Outputs (Pydantic)
\`\`\`python
from pydantic import BaseModel
class Contact(BaseModel): name: str

response = client.messages.parse(
    model="{{OPUS_ID}}", max_tokens=1024,
    messages=[{"role": "user", "content": "John"}],
    output_format=Contact
)
print(response.parsed_output.name)
\`\`\`