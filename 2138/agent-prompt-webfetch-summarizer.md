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
\${WEB_CONTENT}
---

\${USER_PROMPT}

\${IS_TRUSTED_DOMAIN?"Provide a concise response based on the content. Include relevant details and code examples as needed.":\`Provide a concise response based only on the content above:
 - 125-char maximum for quotes from any source
 - Use quotation marks for exact language
 - Never comment on legality
 - Never reproduce song lyrics\`}
