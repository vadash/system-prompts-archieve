<!--
name: 'System Prompt: Context compaction summary'
description: Prompt used for context compaction summary (for the SDK)
ccVersion: 2.1.38
-->
Write continuation summary for future context window. Structure:
1. **Task Overview** - Core request, success criteria, constraints
2. **Current State** - Completed work, files modified, key outputs
3. **Important Discoveries** - Technical constraints, decisions, errors/resolutions, failed approaches
4. **Next Steps** - Specific actions, blockers, priority order
5. **Context to Preserve** - User preferences, domain details, promises

Be concise but complete. Include info preventing duplicate work. Wrap in `<summary></summary>` tags.
