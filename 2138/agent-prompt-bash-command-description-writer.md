<!--
name: 'Agent Prompt: Bash command description writer'
description: Instructions for generating command descriptions
ccVersion: 2.1.3
-->
Clear, concise description of what this command does in active voice. Never use "complex" or "risk".

Simple commands (5-10 words):
- ls → "List files in current directory"
- git status → "Show working tree status"
- npm install → "Install package dependencies"

Complex commands need context:
- find . -name "*.tmp" -exec rm {} \; → "Find and delete all .tmp files recursively"
- git reset --hard origin/main → "Discard all local changes and match remote main"


