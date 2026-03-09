# Design: Patch Prompts Override Script

## 1. Problem Statement

Need a Python utility to override system prompt files with tweaked content while preserving original file headers (metadata). The script should:
- Copy content from a "tweak" folder to a "prompt" folder
- Always preserve original headers from prompt files
- Track what was patched in a markdown checklist
- Warn when file sets don't match 1:1

## 2. Goals & Non-Goals

**Must do:**
- Preserve original `<!--...-->` header blocks from prompt files
- Override body content from tweak files
- Support any file extension
- Output sorted checklist with checkboxes
- Warn on missing files (orphaned tweaks or missing tweaks)

**Won't do:**
- Modify tweak folder (read-only)
- Handle binary files
- Create new files in prompt folder from tweak folder

## 3. Proposed Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Entry                           │
│  - Ask for prompt folder path                               │
│  - Ask for tweak folder path                                │
│  - Validate both exist as directories                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    File Scanner                             │
│  - List all files in both folders (any extension)          │
│  - Identify: matching, orphaned tweaks, missing tweaks      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Header Extractor                         │
│  - Parse `<!--...-->` block from prompt file               │
│  - Extract body content from tweak file (skip its header)  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    File Patcher                             │
│  - Combine: original header + tweak body                    │
│  - Write back to prompt folder                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Report Generator                         │
│  - Print warnings for non-matching files                   │
│  - Generate/overwrite {folder_name}.md with checkbox list  │
│  - Sort: checked [x] first, then alphabetically            │
└─────────────────────────────────────────────────────────────┘
```

## 4. Data Models

```python
@dataclass
class FileInfo:
    """Represents a file found during scanning."""
    path: Path
    name: str  # filename with extension

@dataclass
class PatchResult:
    """Result of patching a single file."""
    filename: str
    was_patched: bool  # True if file was written
    original_header: str | None  # Extracted header from prompt file
    tweak_content: str  # Body content from tweak file

@dataclass
class ScanResult:
    """Result of scanning both folders."""
    matching: list[str]  # Filenames in both folders
    orphaned_tweaks: list[str]  # In tweak but not prompt
    missing_tweaks: list[str]  # In prompt but not tweak
```

## 5. Interface / API Design

```python
def extract_header(content: str) -> tuple[str, str]:
    """
    Extract the header and body from file content.

    Returns:
        (header, body) where header is the <!--...--> block (or empty),
        and body is everything after.
    """

def patch_file(prompt_path: Path, tweak_path: Path) -> PatchResult:
    """
    Patch a single prompt file with content from tweak file.

    1. Read prompt file, extract header
    2. Read tweak file, extract body (skip header if present)
    3. Combine and write back to prompt file
    """

def scan_folders(prompt_dir: Path, tweak_dir: Path) -> ScanResult:
    """
    Scan both directories and categorize files.

    Returns files that match, are only in tweak, or only in prompt.
    """

def generate_report(prompt_name: str, results: list[PatchResult],
                    scan: ScanResult) -> str:
    """
    Generate markdown report content.

    Format:
    - [x] filename.md  (for patched files)
    - [ ] filename.md  (for matching but unchanged - shouldn't happen)

    Sorted: checked first, then alphabetically.
    """
```

## 6. CLI Flow

```python
def main():
    # 1. Get prompt folder
    prompt_folder = input("Enter prompt folder (e.g., 2171): ").strip()
    prompt_path = Path(prompt_folder).resolve()

    # 2. Get tweak folder
    tweak_folder = input("Enter tweak folder (e.g., tmp): ").strip()
    tweak_path = Path(tweak_folder).resolve()

    # 3. Validate
    if not prompt_path.is_dir():
        sys.exit(f"Error: {prompt_path} is not a directory")
    if not tweak_path.is_dir():
        sys.exit(f"Error: {tweak_path} is not a directory")

    # 4. Scan
    scan = scan_folders(prompt_path, tweak_path)

    # 5. Warn on mismatches
    for f in scan.orphaned_tweaks:
        print(f"[WARNING] File in tweak but not prompt: {tweak_path / f}")
    for f in scan.missing_tweaks:
        print(f"[WARNING] File in prompt but not tweak: {prompt_path / f}")

    # 6. Patch matching files
    results = []
    for filename in scan.matching:
        result = patch_file(prompt_path / filename, tweak_path / filename)
        results.append(result)

    # 7. Generate report
    report_path = Path(f"{prompt_path.name}.md")
    content = generate_report(prompt_path.name, results, scan)
    report_path.write_text(content, encoding="utf-8")
    print(f"Report written to: {report_path}")
```

## 7. Risks & Edge Cases

| Scenario | Behavior |
|----------|----------|
| Prompt file has no header | Treat entire file as body, prepend empty header |
| Tweak file has no header | Use entire tweak content as body |
| Both files have no header | Tweak content replaces prompt content entirely |
| Tweak file has header we should ignore | Skip any `<!--...-->` block at start of tweak file |
| Empty tweak file | Write only header (empty body) |
| Empty prompt file | Error/warning - no header to preserve |
| Folder names with spaces | Path handling via pathlib should handle correctly |
| Unicode content | Explicit `encoding="utf-8"` for all I/O |
| Same content (no change) | Still write file, mark as [x] (user confirmed) |

## 8. Header Format

The header to preserve is the HTML/XML comment block at the start of prompt files:

```html
<!--
name: 'Display Name'
description: 'File description'
ccVersion: 2.1.3
-->
```

Detection pattern: Match from first `<!--` to first `-->` at start of file.

## 9. Output .md Format

```markdown
- [x] agent-prompt-explore.md
- [x] system-prompt-git-status.md
- [ ] some-file-not-patched.md
```

Sorted by:
1. Checkbox status: `[x]` before `[ ]`
2. Alphabetically within each group
