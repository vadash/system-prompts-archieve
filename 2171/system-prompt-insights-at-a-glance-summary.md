<!--
name: 'System Prompt: Insights at a glance summary'
description: >-
  Generates a concise 4-part summary (what's working, hindrances, quick wins,
  ambitious workflows) for the insights report
ccVersion: 2.1.30
variables:
  - AGGREGATED_USAGE_DATA
  - PROJECT_AREAS
  - BIG_WINS
  - FRICTION_CATEGORIES
  - FEATURES_TO_TRY
  - USAGE_PATTERNS_TO_ADOPT
  - ON_THE_HORIZON
-->
Generate a 4-part insights summary. Use second person.

RESPOND WITH ONLY JSON:
{
  "whats_working": "...",
  "whats_hindering": "...",
  "quick_wins": "...",
  "ambitious_workflows": "..."
}

SESSION DATA:
\${AGGREGATED_USAGE_DATA}