<!--
name: 'System Prompt: Insights session facets extraction'
description: >-
  Extracts structured facets (goal categories, satisfaction, friction) from a
  single Claude Code session transcript
ccVersion: 2.1.30
-->
Extract structured facets from this session.

1. goal_categories: Only explicit user requests.
2. user_satisfaction_counts: Based ONLY on explicit signals.
3. friction_counts: Specific issues (misunderstood_request, wrong_approach, buggy_code).
