<!--
name: 'Tool Description: Edit'
description: Tool for performing exact string replacements in files
ccVersion: 2.1.20
variables:
  - MUST_READ_FIRST_FN
-->
Performs exact string replacements in files.

Usage:${MUST_READ_FIRST_FN()}
- When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix (spaces + line number + tab). Everything after that tab is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
- The edit will FAIL if `old_string` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use `replace_all` to change every instance of `old_string`.
- Use `replace_all` for replacing and renaming strings across the file.
