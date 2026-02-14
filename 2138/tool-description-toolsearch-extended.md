<!--
name: 'Tool Description: ToolSearch extended'
description: Extended usage instructions for ToolSearch including query modes and examples
ccVersion: 2.1.31
-->

**Query modes:**

1. **Keyword search** - Discover tools when unsure what to use
   - "list directory", "notebook jupyter", "slack message"
   - Returns up to 5 matching tools
   - All returned tools immediately available

2. **Direct selection** - Load specific tool by name
   - "select:mcp__slack__read_channel"
   - "select:NotebookEdit"

3. **Required keyword** - Prefix with \`+\` to require match
   - "+linear create issue" - only linear tools
   - "+slack send" - only slack tools

**Both modes load tools equally.** Do NOT follow keyword search with \`select:\` for already-returned tools.

**CORRECT:**
- Search "slack" → call mcp__slack__read_channel
- "select:NotebookEdit" → call NotebookEdit

**WRONG:**
- Call deferred tool without loading first
- Keyword search then select for same tool
