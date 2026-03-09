<!--
name: 'Data: Claude API reference — Java'
description: >-
  Java SDK reference including installation, client initialization, basic
  requests, streaming, and beta tool use
ccVersion: 2.1.63
-->
# Claude API — Java

## Installation
Maven: \`com.anthropic:anthropic-java:2.15.0\`

## Initialization
\`\`\`java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
AnthropicClient client = AnthropicOkHttpClient.fromEnv();
\`\`\`

## Basic Request
\`\`\`java
import com.anthropic.models.messages.*;
Message response = client.messages().create(MessageCreateParams.builder()
    .model(Model.CLAUDE_OPUS_4_6)
    .maxTokens(1024L)
    .addUserMessage("Hello")
    .build());
\`\`\`

## Tool Runner (Beta)
Uses annotated classes implementing \`Supplier<String>\`.
\`\`\`java
@JsonClassDescription("Get weather")
static class GetWeather implements Supplier<String> {
    @JsonPropertyDescription("City") public String location;
    public String get() { return "Sunny in " + location; }
}

BetaToolRunner runner = client.beta().messages().toolRunner(
    MessageCreateParams.builder()
        .model("{{OPUS_ID}}").maxTokens(1024L)
        .addTool(GetWeather.class)
        .addUserMessage("Weather in SF?")
        .build());
\`\`\`