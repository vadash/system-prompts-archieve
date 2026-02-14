<!--
name: 'Tool Description: LSP'
description: Description for the LSP tool.
ccVersion: 2.0.73
-->
Code intelligence via Language Server Protocol.

**Operations:**
- \`goToDefinition\` - Find symbol definition
- \`findReferences\` - Find all references
- \`hover\` - Documentation and type info
- \`documentSymbol\` - All symbols in document
- \`workspaceSymbol\` - Search across workspace
- \`goToImplementation\` - Interface implementations
- \`prepareCallHierarchy\` / \`incomingCalls\` / \`outgoingCalls\` - Call analysis

**Required:** filePath, line (1-based), character (1-based)

Note: LSP servers must be configured for the file type.
