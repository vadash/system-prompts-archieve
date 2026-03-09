<!--
name: 'Data: Claude API reference — Ruby'
description: >-
  Ruby SDK reference including installation, client initialization, basic
  requests, streaming, and beta tool runner
ccVersion: 2.1.71
-->
# Claude API — Ruby

## Installation & Initialization
```bash
gem install anthropic
```
```ruby
require "anthropic"
client = Anthropic::Client.new
```

## Basic Request
```ruby
msg = client.messages.create(
  model: :"{{OPUS_ID}}", max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }]
)
```

## Streaming
```ruby
stream = client.messages.stream(...)
stream.text.each { |text| print(text) }
```

## Tool Runner (Beta)
```ruby
class GetWeatherInput < Anthropic::BaseModel
  required :location, String
end

class GetWeather < Anthropic::BaseTool
  input_schema GetWeatherInput
  def call(input) "Sunny in #{input.location}" end
end

client.beta.messages.tool_runner(
  model: :"{{OPUS_ID}}", max_tokens: 1024,
  tools: [GetWeather.new],
  messages: [...]
).each_message { |m| puts m.content }
```