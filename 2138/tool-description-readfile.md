<!--
name: 'Tool Description: ReadFile'
description: Tool description for reading files
ccVersion: 2.1.30
variables:
  - DEFAULT_READ_LINES
  - MAX_LINE_LENGTH
  - CAN_READ_PDF_FILES
  - BASH_TOOL_NAME
-->
Reads files/images (absolute paths only).
- **Output Format:** Returns content using \`cat -n\` (line numbers start at 1).
- **Supports:** Images (visual), Notebooks (.ipynb executed cells), PDFs (max 20 pages${CAN_READ_PDF_FILES()?", requires \`pages\` param if >10 pages":""}).
- **Restrictions:** No directories (use \`${BASH_TOOL_NAME} ls\`).
- Parallel tool calls encouraged for performance.
- Truncates lines >${MAX_LINE_LENGTH} chars and files >${DEFAULT_READ_LINES} lines.
