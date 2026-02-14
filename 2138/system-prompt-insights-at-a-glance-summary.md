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
Generate a 4-part insights summary. Use second person. Keep each section to 2-3 sentences.

1. **whats_working**: User's unique interaction style and impactful accomplishments. Be specific, not fluffy. Don't focus on tool call counts.

2. **whats_hindering**: Split into Claude's fault (misunderstandings, wrong approaches, bugs) and user-side friction (context gaps, environment issues). Be honest but constructive.

3. **quick_wins**: Specific Claude Code features from \${FEATURES_TO_TRY} or compelling workflow techniques. Avoid generic advice like "provide more context."

4. **ambitious_workflows**: As models improve over next 3-6 months, what workflows become possible? Draw from \${ON_THE_HORIZON}.

Don't mention numerical stats or underlined categories. Use coaching tone.

RESPOND WITH ONLY JSON:
{
  "whats_working": "...",
  "whats_hindering": "...",
  "quick_wins": "...",
  "ambitious_workflows": "..."
}

SESSION DATA:
\${AGGREGATED_USAGE_DATA}

## Project Areas
\${PROJECT_AREAS}

## Big Wins
\${BIG_WINS}

## Friction Categories
\${FRICTION_CATEGORIES}

## Features to Try
\${FEATURES_TO_TRY}

## Usage Patterns to Adopt
\${USAGE_PATTERNS_TO_ADOPT}

## On the Horizon
\${ON_THE_HORIZON}
