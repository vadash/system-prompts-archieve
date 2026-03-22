<!--
name: 'Data: GitHub App installation PR description'
description: Template for PR description when installing Claude Code GitHub App integration
ccVersion: 2.0.14
-->
## 🤖 Installing Claude Code GitHub App

This PR adds a GitHub Actions workflow enabling Claude Code integration.

### How it works
Mention @claude in a PR or issue comment. The workflow runs Claude with full PR/issue context.

### Security
- API key stored as GitHub Actions secret
- Only users with write access can trigger
- Tools limited to reading/writing files and PR/issue comments
- Additional tools can be configured via \`allowed_tools\` in the action.
