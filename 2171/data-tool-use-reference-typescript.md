<!--
name: 'Data: Tool use reference — TypeScript'
description: >-
  TypeScript tool use reference including tool runner, manual agentic loop, code
  execution, and structured outputs
ccVersion: 2.1.63
-->
# Tool Use — TypeScript

## Tool Runner (Beta)
\`\`\`typescript
import { betaZodTool } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

const getWeather = betaZodTool({
  name: "get_weather", description: "Desc",
  inputSchema: z.object({ location: z.string() }),
  run: async (input) => \`Sunny in \${input.location}\`
});

const msg = await client.beta.messages.toolRunner({
  model: "{{OPUS_ID}}", max_tokens: 4096, tools: [getWeather],
  messages: [{ role: "user", content: "Weather?" }]
});
\`\`\`

## Manual Loop
Keep \`Anthropic.MessageParam[]\` history. Extract \`tool_use\`, push \`tool_result\` with matching ID.

## Structured Outputs (Zod)
\`\`\`typescript
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
const Schema = z.object({ name: z.string() });

const response = await client.messages.parse({
  model: "{{OPUS_ID}}", max_tokens: 1024,
  messages: [{ role: "user", content: "John" }],
  output_config: { format: zodOutputFormat(Schema) }
});
console.log(response.parsed_output.name);
\`\`\`