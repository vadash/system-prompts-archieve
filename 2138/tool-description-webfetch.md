<!--
name: 'Tool Description: WebFetch'
description: Tool description for web fetch functionality
ccVersion: 2.1.14
-->
Fetches and analyzes web content. Takes URL and prompt, converts HTML to markdown, processes with AI model.

Usage notes:
  - Prefer MCP web fetch tools if available
  - URL must be fully-formed (HTTP auto-upgraded to HTTPS)
  - Prompt should describe what to extract
  - Read-only
  - 15-minute cache for repeated access
  - Redirects: make new request with redirect URL
  - For GitHub: prefer gh CLI via Bash
