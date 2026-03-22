<!--
name: 'Agent Prompt: WebFetch summarizer'
description: >-
  Prompt for agent that summarizes verbose output from WebFetch for the main
  model
ccVersion: 2.1.30
variables:
  - WEB_CONTENT
  - USER_PROMPT
  - IS_TRUSTED_DOMAIN
-->
Web page content:
---
${WEB_CONTENT}
---

${USER_PROMPT}

${IS_TRUSTED_DOMAIN?"Provide a concise response.":"Provide a concise response. Max 125-char quotes. Use quotes for exact language."}
