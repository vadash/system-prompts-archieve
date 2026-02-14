<!--
name: 'Tool Description: ToolSearch'
description: Tool description for loading and searching deferred tools before use
ccVersion: 2.1.31
variables:
  - EXTENDED_TOOL_SEARCH_PROMPT
-->

**CRITICAL:** MUST use this tool BEFORE calling deferred tools. Deferred tools are NOT available until loaded via this tool.

Check \`<available-deferred-tools>\` messages for discoverable tools.\${EXTENDED_TOOL_SEARCH_PROMPT}
