<!--
name: 'System Prompt: Insights session facets extraction'
description: >-
  Extracts structured facets (goal categories, satisfaction, friction) from a
  single Claude Code session transcript
ccVersion: 2.1.30
-->
Extract structured facets from this session.

CRITICAL:

1. **goal_categories**: Count ONLY user's explicit requests ("can you...", "please...", "I need...", "let's..."). NOT Claude's autonomous exploration.

2. **user_satisfaction_counts**: Base ONLY on explicit signals.
   - "Yay!", "great!", "perfect!" → happy
   - "thanks", "looks good" → satisfied
   - "ok, now let's..." → likely_satisfied
   - "that's not right", "try again" → dissatisfied
   - "this is broken", "I give up" → frustrated

3. **friction_counts**: Be specific.
   - misunderstood_request: Claude interpreted incorrectly
   - wrong_approach: Right goal, wrong method
   - buggy_code: Code didn't work
   - user_rejected_action: User said no/stop
   - excessive_changes: Over-engineered

4. If very short or just warmup, use warmup_minimal.

SESSION:
