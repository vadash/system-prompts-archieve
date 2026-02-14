<!--
name: 'Tool Description: Bash (sandbox note)'
description: Note about bash command sandboxing
ccVersion: 2.0.34
variables:
  - CONDITIONAL_NEWLINE_IF_SANDBOX_ENABLED
-->

**CRITICAL:** Commands run in sandbox mode by default.
- Do NOT set \`dangerouslyDisableSandbox\` unless user explicitly requests OR command failed with sandbox-caused errors
- Sandbox-caused failure evidence: "Operation not permitted", access denied to allowed paths, network failures to non-whitelisted hosts
- On sandbox-caused failure: immediately retry with \`dangerouslyDisableSandbox: true\`, explain restriction, mention \`/sandbox\`
\${CONDITIONAL_NEWLINE_IF_SANDBOX_ENABLED}
