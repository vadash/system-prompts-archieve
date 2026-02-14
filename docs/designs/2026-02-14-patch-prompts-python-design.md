# Design: Port patch-prompts to Python

## 1. Problem Statement

`patch-prompts.ps1` works but PowerShell has painful shell-escaping issues when testing
(documented in `utils/CLAUDE.md`). Python eliminates these problems and is more portable.

## 2. Goals & Non-Goals

**Must do:**
- Port all 4 functions to Python with equivalent behavior
- Use Pythonic patterns: dataclasses, pathlib, type hints, decorator-based fixer registration
- pytest test suite covering all 16 existing Pester test cases
- Update `utils/CLAUDE.md` to reflect Python tooling
- Delete the `.ps1` files after port is validated

**Won't do:**
- Add new fixers beyond the existing two
- Change the fixer logic (regex patterns stay identical)
- Add external dependencies (stdlib + pytest only)

## 3. Proposed Architecture

Pythonic redesign with decorator-based fixer registration:

```
utils/
├── patch_prompts.py          # Main script (replaces .ps1)
├── test_patch_prompts.py     # pytest tests (replaces .Tests.ps1)
└── CLAUDE.md                 # Updated for Python
```

### Key components:
- **`@fixer` decorator** — registers fixer functions into a global registry
- **`Fixer` dataclass** — holds name, glob filter, and action callable
- **`pathlib.Path`** throughout — no `os.path` string manipulation
- **`__main__` guard** — equivalent to PowerShell's `$MyInvocation.InvocationName` check

## 4. Data Models

```python
from dataclasses import dataclass
from typing import Callable
from pathlib import Path

@dataclass
class Fixer:
    name: str
    filter: str       # glob pattern, e.g. "*.md" or "*"
    action: Callable[[Path], bool]  # returns True if file was modified

# Global registry
_fixers: list[Fixer] = []
```

## 5. Interface / API Design

```python
# --- Decorator for fixer registration ---
def fixer(name: str, filter: str = "*"):
    """Register a fixer function. Decorated fn takes Path, returns bool."""
    def decorator(fn: Callable[[Path], bool]) -> Callable[[Path], bool]:
        _fixers.append(Fixer(name=name, filter=filter, action=fn))
        return fn
    return decorator

# --- Core functions ---
def escape_backticks(text: str) -> str:
    """Escape unescaped backticks and template literal ${} syntax."""

def fix_line_endings(text: str) -> str:
    """Convert CRLF to LF."""

def get_patchable_files(path: Path) -> list[Path]:
    """Recursively find text files, skipping binary extensions and VCS dirs."""

def run_fixers(path: Path) -> None:
    """Execute all registered fixers against patchable files."""

# --- Registered fixers ---
@fixer("Escape backticks", filter="*.md")
def _fixer_escape_backticks(file_path: Path) -> bool: ...

@fixer("Fix line endings", filter="*")
def _fixer_fix_line_endings(file_path: Path) -> bool: ...
```

### CLI usage (unchanged UX):
```bash
python utils/patch_prompts.py <directory>
```

## 6. Risks & Edge Cases

| Risk | Mitigation |
|------|-----------|
| Regex behavior differs between .NET and Python `re` | Both use PCRE-like syntax; negative lookbehind `(?<!\\)` works identically |
| File encoding differences | Use `encoding="utf-8"` explicitly; write without BOM (Python default) |
| `pathlib.match()` vs PowerShell `-like` | Use `fnmatch` for glob matching on filenames |
| Line ending detection | Read bytes to check for `\r\n` before converting (same as .ps1) |
| Idempotency | Same regex approach — already-escaped sequences won't double-escape |

## 7. CLAUDE.md Updates

Replace PowerShell-specific content with:
- pytest invocation patterns
- No shell-escaping caveats needed (Python handles strings natively)
- Temp directory patterns (`tmp_path` fixture vs `$TestDrive`)

## 8. Migration Steps

1. Create `patch_prompts.py` with all functions + decorator registry
2. Create `test_patch_prompts.py` with all 16 test cases ported to pytest
3. Run tests, validate parity
4. Update `utils/CLAUDE.md`
5. Delete `patch-prompts.ps1` and `patch-prompts.Tests.ps1`
6. Commit
