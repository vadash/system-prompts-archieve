<!--
name: 'Data: Claude API reference — PHP'
description: PHP SDK reference
ccVersion: 2.1.63
-->
# Claude API — PHP

## Installation
\`\`\`bash
composer require "anthropic-ai/sdk"
\`\`\`

## Initialization
\`\`\`php
use Anthropic\Client;
$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));
// Also supports BedrockClient, VertexClient, FoundryClient
\`\`\`

## Basic Request
\`\`\`php
$message = $client->messages->create(
    model: '{{OPUS_ID}}',
    maxTokens: 1024,
    messages: [['role' => 'user', 'content' => 'Hello']],
);
echo $message->content[0]->text;
\`\`\`

## Streaming
\`\`\`php
$stream = $client->messages->createStream([...]);
foreach ($stream as $event) { echo $event; }
\`\`\`
