<!--
name: 'Tool Description: NotebookEdit'
description: Tool description for editing Jupyter notebook cells
ccVersion: 2.0.14
-->
Replace cell contents in Jupyter notebook (.ipynb). notebook_path must be absolute. cell_number is 0-indexed.

edit_mode:
- replace: default
- insert: add new cell at index
- delete: remove cell at index
