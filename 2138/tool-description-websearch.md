<!--
name: 'Tool Description: WebSearch'
description: Tool description for web search functionality
ccVersion: 2.1.30
variables:
  - GET_CURRENT_DATE_FN
  - CURRENT_YEAR
-->
Searches web and returns results as markdown hyperlinks.

CRITICAL: After answering, MUST include "Sources:" section with all relevant URLs.

Usage notes:
  - Domain filtering supported
  - US only
  - Today: \${GET_CURRENT_DATE_FN()}
  - Use \${CURRENT_YEAR} for recent searches (not \${CURRENT_YEAR-1})
