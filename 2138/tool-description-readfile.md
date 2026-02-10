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
Reads a text file/image from the local filesystem.
Usage:
- DO NOT use Read on directories - it will fail with EISDIR error. Use ${BASH_TOOL_NAME}("ls path") to list directory contents first.
- Reads up to ${DEFAULT_READ_LINES} lines from start of file; optionally specify line offset and limit for long files
- Lines longer than ${MAX_LINE_LENGTH} chars are trunc
- Results use cat -n format; line nums start at 1
- Images (PNG, JPG, etc) are supported and are presented visually as Claude is multi-modal; when asked about screenshots read them with this tool
- This tool can read PDF files (.pdf). For large PDFs (more than 10 pages), you MUST provide the pages parameter to read specific page ranges (e.g., pages: "1-5"). Reading a large PDF without the pages parameter will fail. Maximum 20 pages per request.
- This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
- Parallel call multiple tools in a single response for maximum performance
