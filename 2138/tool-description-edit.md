<!--
name: 'Tool Description: Edit'
description: Tool for performing exact string replacements in files
ccVersion: 2.1.20
variables:
  - MUST_READ_FIRST_FN
-->
Performs exact string replacements.\${MUST_READ_FIRST_FN()}
- **Unique Match:** \`old_string\` must be unique in the file. If duplicates exist, include more surrounding context lines or use \`replace_all\`.
- **Formatting:** \`Read\` output includes line prefixes (spaces + number + tab). You MUST strip this prefix. NEVER include line numbers in \`old_string\`.
- **Whitespace:** You MUST preserve the exact indentation (tabs/spaces) of the content *after* the line number tab.
- Use \`replace_all\` for global renames.
