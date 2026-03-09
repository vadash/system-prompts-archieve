<!--
name: 'Data: Claude API reference — C#'
description: >-
  C# SDK reference including installation, client initialization, basic
  requests, streaming, and tool use
ccVersion: 2.1.51
-->
# Claude API — C#

## Installation
\`\`\`bash
dotnet add package Anthropic
\`\`\`

## Initialization
\`\`\`csharp
using Anthropic;
AnthropicClient client = new(); // Uses ANTHROPIC_API_KEY
\`\`\`

## Basic Request
\`\`\`csharp
using Anthropic.Models.Messages;

var msg = await client.Messages.Create(new MessageCreateParams {
    Model = Model.ClaudeOpus4_6,
    MaxTokens = 1024,
    Messages = [new() { Role = Role.User, Content = "Hello" }]
});
Console.WriteLine(msg);
\`\`\`

## Streaming
\`\`\`csharp
await foreach (var streamEvent in client.Messages.CreateStreaming(params)) {
    if (streamEvent.TryPickContentBlockDelta(out var delta) && delta.Delta.TryPickText(out var text)) {
        Console.Write(text.Text);
    }
}
\`\`\`

## Tool Use
The C# SDK supports manual loops and JSON schema tool definitions. Use Microsoft.Extensions.AI IChatClient for advanced function invocation.