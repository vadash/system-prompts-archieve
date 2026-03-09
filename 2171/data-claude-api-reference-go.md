<!--
name: 'Data: Claude API reference — Go'
description: Go SDK reference
ccVersion: 2.1.71
-->
# Claude API — Go

## Installation
```bash
go get github.com/anthropics/anthropic-sdk-go
```

## Initialization
```go
import "github.com/anthropics/anthropic-sdk-go"
client := anthropic.NewClient() // Uses ANTHROPIC_API_KEY
```

## Basic Request
```go
resp, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaudeOpus4_6,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
    },
})
```

## Streaming
```go
stream := client.Messages.NewStreaming(context.Background(), params)
for stream.Next() {
    // Process stream.Current().AsAny()
}
```

## Tool Runner (Beta)
Automatically handles tool loops. Tool schemas generate automatically via `jsonschema` struct tags.
```go
import "github.com/anthropics/anthropic-sdk-go/toolrunner"

type Input struct { City string `json:"city" jsonschema:"required"` }
tool, _ := toolrunner.NewBetaToolFromJSONSchema("get_weather", "Desc", func(ctx context.Context, in Input) (...) { ... })

runner := client.Beta.Messages.NewToolRunner([]anthropic.BetaTool{tool}, params)
msg, _ := runner.RunToCompletion(context.Background())
```

## Extended Thinking
```go
Thinking: anthropic.ThinkingConfigParamOfEnabled(5000) // Budget tokens for older models
// Use anthropic.NewThinkingConfigAdaptiveParam() for Opus 4.6 / Sonnet 4.6
```