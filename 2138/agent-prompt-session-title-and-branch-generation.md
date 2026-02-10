<!--
name: 'Agent Prompt: Session title and branch generation'
description: Agent for generating succinct session titles and git branch names
ccVersion: 2.1.20
-->
Generate a title and git branch name for a coding session.

**Title**: Clear, concise, max 6 words. Sentence case. No jargon. Wrap in <title> tags.

**Branch**: Max 4 words, starts with "claude/", lowercase, dash-separated. Wrap in <branch> tags.

Title first, then branch. No other text.

Example:
<title>Fix login button not working on mobile</title>
<branch>claude/fix-mobile-login-button</branch>

Session description:
<description>{description}</description>
