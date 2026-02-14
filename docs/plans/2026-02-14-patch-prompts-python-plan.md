# Implementation Plan - Port patch-prompts to Python

> **Reference:** `docs/designs/2026-02-14-patch-prompts-python-design.md`
> **Execution:** Use `executing-plans` skill.

---

### Task 1: Scaffold + Fixer dataclass + decorator registry

**Goal:** Create `patch_prompts.py` with the `Fixer` dataclass, `_fixers` registry, and `@fixer` decorator. Verify the decorator registers fixers correctly.

**Step 1: Write the Failing Test**
- File: `utils/test_patch_prompts.py`
- Code:
  ```python
  from patch_prompts import Fixer, fixer, _fixers


  def test_fixer_decorator_registers():
      """Decorator should append a Fixer to the global registry."""
      # _fixers is populated at import time by decorated functions.
      # At minimum, the two built-in fixers should be registered.
      assert len(_fixers) >= 2
      assert all(isinstance(f, Fixer) for f in _fixers)


  def test_fixer_dataclass_fields():
      names = [f.name for f in _fixers]
      assert "Escape backticks" in names
      assert "Fix line endings" in names
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_patch_prompts.py::test_fixer_decorator_registers utils/test_patch_prompts.py::test_fixer_dataclass_fields -v`
- Expect: `ModuleNotFoundError: No module named 'patch_prompts'`

**Step 3: Implementation (Green)**
- File: `utils/patch_prompts.py`
- Action: Create file with imports, `Fixer` dataclass, `_fixers` list, `@fixer` decorator, and two stub fixer functions that return `False`.
- Code:
  ```python
  #!/usr/bin/env python3
  """Patch system-prompt files: escape backticks, fix line endings."""

  from __future__ import annotations

  import fnmatch
  import re
  import sys
  from dataclasses import dataclass
  from pathlib import Path
  from typing import Callable


  # --- Data model & registry ---

  @dataclass
  class Fixer:
      name: str
      filter: str
      action: Callable[[Path], bool]

  _fixers: list[Fixer] = []


  def fixer(name: str, filter: str = "*"):
      """Register a fixer function into the global registry."""
      def decorator(fn: Callable[[Path], bool]) -> Callable[[Path], bool]:
          _fixers.append(Fixer(name=name, filter=filter, action=fn))
          return fn
      return decorator


  # --- Core text transforms ---

  def escape_backticks(text: str) -> str:
      ...

  def fix_line_endings(text: str) -> str:
      ...

  def get_patchable_files(path: Path) -> list[Path]:
      ...

  def run_fixers(path: Path) -> None:
      ...


  # --- Registered fixers ---

  @fixer("Escape backticks", filter="*.md")
  def _fixer_escape_backticks(file_path: Path) -> bool:
      return False

  @fixer("Fix line endings", filter="*")
  def _fixer_fix_line_endings(file_path: Path) -> bool:
      return False
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_patch_prompts.py::test_fixer_decorator_registers utils/test_patch_prompts.py::test_fixer_dataclass_fields -v`
- Expect: PASS (2 tests)

**Step 5: Git Commit**
- `git add utils/patch_prompts.py utils/test_patch_prompts.py`
- `git commit -m "feat: scaffold patch_prompts.py with Fixer dataclass and decorator registry"`

---

### Task 2: `escape_backticks` — pure text transform

**Goal:** Port `Invoke-EscapeBackticks` to Python. 6 test cases.

**Step 1: Write the Failing Tests**
- File: `utils/test_patch_prompts.py` (append)
- Code:
  ```python
  from patch_prompts import escape_backticks


  class TestEscapeBackticks:
      def test_escapes_single_unescaped_backtick(self):
          assert escape_backticks("Hello `world`") == r"Hello \`world\`"

      def test_no_double_escape_already_escaped(self):
          assert escape_backticks(r"Already \`escaped\`") == r"Already \`escaped\`"

      def test_escapes_triple_backticks(self):
          assert escape_backticks("```python") == r"\`\`\`python"

      def test_mixed_escaped_and_unescaped(self):
          assert escape_backticks(r"mix \`ok` and `raw\`") == r"mix \`ok\` and \`raw\`"

      def test_no_backticks_unchanged(self):
          assert escape_backticks("no backticks here") == "no backticks here"

      def test_empty_string(self):
          assert escape_backticks("") == ""

      def test_escapes_template_literal_syntax(self):
          assert escape_backticks('`${K?"test":"fail"}') == r'\`\${K?"test":"fail"}'

      def test_no_double_escape_template_literal(self):
          assert escape_backticks(r'\`\${already}') == r'\`\${already}'
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_patch_prompts.py::TestEscapeBackticks -v`
- Expect: Failures — `escape_backticks` returns `None` (stub `...`)

**Step 3: Implementation (Green)**
- File: `utils/patch_prompts.py`
- Action: Replace the `escape_backticks` stub:
  ```python
  def escape_backticks(text: str) -> str:
      if not text:
          return text
      # Escape unescaped backticks (not preceded by \)
      result = re.sub(r'(?<!\\)`', r'\\`', text)
      # Escape unescaped template literal ${ (not preceded by \)
      result = re.sub(r'(?<!\\)\$\{', r'\\${', result)
      return result
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_patch_prompts.py::TestEscapeBackticks -v`
- Expect: PASS (8 tests)

**Step 5: Git Commit**
- `git add utils/patch_prompts.py utils/test_patch_prompts.py`
- `git commit -m "feat: add escape_backticks with 8 test cases"`

---

### Task 3: `fix_line_endings` — pure text transform

**Goal:** Port `Invoke-FixLineEndings` to Python. 4 test cases.

**Step 1: Write the Failing Tests**
- File: `utils/test_patch_prompts.py` (append)
- Code:
  ```python
  from patch_prompts import fix_line_endings


  class TestFixLineEndings:
      def test_converts_crlf_to_lf(self):
          assert fix_line_endings("line1\r\nline2\r\n") == "line1\nline2\n"

      def test_lf_only_unchanged(self):
          assert fix_line_endings("line1\nline2\n") == "line1\nline2\n"

      def test_mixed_crlf_and_lf(self):
          assert fix_line_endings("crlf\r\nlf\nmore\r\n") == "crlf\nlf\nmore\n"

      def test_empty_string(self):
          assert fix_line_endings("") == ""
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_patch_prompts.py::TestFixLineEndings -v`
- Expect: Failures — `fix_line_endings` returns `None`

**Step 3: Implementation (Green)**
- File: `utils/patch_prompts.py`
- Action: Replace the `fix_line_endings` stub:
  ```python
  def fix_line_endings(text: str) -> str:
      if not text:
          return text
      return text.replace("\r\n", "\n")
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_patch_prompts.py::TestFixLineEndings -v`
- Expect: PASS (4 tests)

**Step 5: Git Commit**
- `git add utils/patch_prompts.py utils/test_patch_prompts.py`
- `git commit -m "feat: add fix_line_endings with 4 test cases"`

---

### Task 4: `get_patchable_files` — file discovery

**Goal:** Port `Get-PatchableFiles` to Python. 3 test cases using `tmp_path`.

**Step 1: Write the Failing Tests**
- File: `utils/test_patch_prompts.py` (append)
- Code:
  ```python
  from patch_prompts import get_patchable_files


  class TestGetPatchableFiles:
      def _setup_tree(self, tmp_path):
          """Create test directory structure."""
          (tmp_path / ".git").mkdir()
          (tmp_path / "sub").mkdir()
          (tmp_path / "readme.md").write_text("hello", encoding="utf-8")
          (tmp_path / "sub" / "notes.txt").write_text("world", encoding="utf-8")
          (tmp_path / "image.png").write_bytes(bytes([0, 1, 2]))
          (tmp_path / ".git" / "config").write_text("gitfile", encoding="utf-8")

      def test_finds_text_files_recursively(self, tmp_path):
          self._setup_tree(tmp_path)
          files = get_patchable_files(tmp_path)
          assert len(files) == 2

      def test_skips_git_directory(self, tmp_path):
          self._setup_tree(tmp_path)
          files = get_patchable_files(tmp_path)
          assert not any(".git" in str(f) for f in files)

      def test_skips_binary_extensions(self, tmp_path):
          self._setup_tree(tmp_path)
          files = get_patchable_files(tmp_path)
          assert not any(f.suffix == ".png" for f in files)
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_patch_prompts.py::TestGetPatchableFiles -v`
- Expect: Failures — `get_patchable_files` returns `None`

**Step 3: Implementation (Green)**
- File: `utils/patch_prompts.py`
- Action: Replace the `get_patchable_files` stub:
  ```python
  _BINARY_EXTENSIONS: set[str] = {
      ".exe", ".dll", ".so", ".dylib", ".bin", ".dat",
      ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
      ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
      ".zip", ".tar", ".gz", ".rar", ".7z",
      ".mp3", ".mp4", ".avi", ".mov", ".wav", ".flac",
      ".ttf", ".otf", ".woff", ".woff2", ".eot",
      ".pyc", ".class", ".jar", ".war", ".ear",
  }

  _SKIP_DIRS: set[str] = {".git", ".svn", "node_modules", "vendor", "target", "bin", "obj"}


  def get_patchable_files(path: Path) -> list[Path]:
      results: list[Path] = []
      for item in path.rglob("*"):
          if not item.is_file():
              continue
          if any(part in _SKIP_DIRS for part in item.relative_to(path).parts):
              continue
          if item.suffix.lower() in _BINARY_EXTENSIONS:
              continue
          results.append(item)
      return results
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_patch_prompts.py::TestGetPatchableFiles -v`
- Expect: PASS (3 tests)

**Step 5: Git Commit**
- `git add utils/patch_prompts.py utils/test_patch_prompts.py`
- `git commit -m "feat: add get_patchable_files with 3 test cases"`

---

### Task 5: `run_fixers` — integration + fixer wiring

**Goal:** Wire up `run_fixers` and the two `@fixer`-decorated functions. 3 integration tests.

**Step 1: Write the Failing Tests**
- File: `utils/test_patch_prompts.py` (append)
- Code:
  ```python
  from patch_prompts import run_fixers


  class TestRunFixers:
      def _write_test_files(self, tmp_path):
          # MD with unescaped backtick + CRLF
          (tmp_path / "test.md").write_bytes(
              "inline `code` here\r\n".encode("utf-8")
          )
          # TXT with CRLF only
          (tmp_path / "plain.txt").write_bytes(
              "line1\r\nline2\r\n".encode("utf-8")
          )

      def test_escapes_backticks_in_md(self, tmp_path):
          self._write_test_files(tmp_path)
          run_fixers(tmp_path)
          content = (tmp_path / "test.md").read_text(encoding="utf-8")
          assert r"\`" in content
          # No unescaped backticks remain
          import re
          assert not re.search(r'(?<!\\)`', content)

      def test_fixes_line_endings_in_all_files(self, tmp_path):
          self._write_test_files(tmp_path)
          run_fixers(tmp_path)
          md = (tmp_path / "test.md").read_text(encoding="utf-8")
          txt = (tmp_path / "plain.txt").read_text(encoding="utf-8")
          assert "\r" not in md
          assert "\r" not in txt

      def test_idempotent_no_double_escape(self, tmp_path):
          self._write_test_files(tmp_path)
          run_fixers(tmp_path)
          run_fixers(tmp_path)  # second pass
          content = (tmp_path / "test.md").read_text(encoding="utf-8")
          assert r"\\`" not in content
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_patch_prompts.py::TestRunFixers -v`
- Expect: Failures — `run_fixers` is a stub, fixer functions return `False`

**Step 3: Implementation (Green)**
- File: `utils/patch_prompts.py`
- Action: Implement `run_fixers` and the two fixer function bodies.

  Replace `run_fixers` stub:
  ```python
  def run_fixers(path: Path) -> None:
      all_files = get_patchable_files(path)
      print(f"Found {len(all_files)} files.", flush=True)

      for fx in _fixers:
          matching = [f for f in all_files if fnmatch.fnmatch(f.name, fx.filter)]
          fixed_count = 0
          print(f"\n[{fx.name}] Processing {len(matching)} files...", flush=True)

          for file in matching:
              try:
                  if fx.action(file):
                      fixed_count += 1
                      print(f"  [FIXED] {file.relative_to(path)}", flush=True)
              except Exception as e:
                  print(f"  [ERROR] {file}: {e}", flush=True)

          print(f"  {fixed_count} file(s) fixed.", flush=True)
  ```

  Replace `_fixer_escape_backticks` stub:
  ```python
  @fixer("Escape backticks", filter="*.md")
  def _fixer_escape_backticks(file_path: Path) -> bool:
      content = file_path.read_text(encoding="utf-8")
      fixed = escape_backticks(content)
      if fixed != content:
          file_path.write_text(fixed, encoding="utf-8")
          return True
      return False
  ```

  Replace `_fixer_fix_line_endings` stub:
  ```python
  @fixer("Fix line endings", filter="*")
  def _fixer_fix_line_endings(file_path: Path) -> bool:
      raw = file_path.read_bytes()
      if b"\r\n" not in raw:
          return False
      content = raw.decode("utf-8")
      fixed = fix_line_endings(content)
      file_path.write_text(fixed, encoding="utf-8", newline="\n")
      return True
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_patch_prompts.py -v`
- Expect: ALL 20 tests PASS

**Step 5: Git Commit**
- `git add utils/patch_prompts.py utils/test_patch_prompts.py`
- `git commit -m "feat: add run_fixers integration with fixer wiring"`

---

### Task 6: CLI `__main__` block

**Goal:** Add the CLI entry point. No automated test — manual verification.

**Step 1: Implementation**
- File: `utils/patch_prompts.py` (append at end)
- Code:
  ```python
  if __name__ == "__main__":
      if len(sys.argv) < 2:
          target = input("Enter directory path to patch: ")
      else:
          target = sys.argv[1]

      target_path = Path(target).resolve()
      if not target_path.is_dir():
          print(f"Error: '{target}' is not a valid directory.", file=sys.stderr)
          sys.exit(1)

      print(f"Scanning '{target_path}'...", flush=True)
      run_fixers(target_path)
      print("\nDone.", flush=True)
  ```

**Step 2: Verify**
- Command: `pytest utils/test_patch_prompts.py -v` (regression — all 20 still pass)
- Command: `python utils/patch_prompts.py .` (smoke test on repo root)

**Step 3: Git Commit**
- `git add utils/patch_prompts.py`
- `git commit -m "feat: add CLI entry point for patch_prompts.py"`

---

### Task 7: Update CLAUDE.md + delete PowerShell files

**Goal:** Replace `utils/CLAUDE.md` with Python-focused guidelines. Delete `.ps1` files.

**Step 1: Rewrite `utils/CLAUDE.md`**
- File: `utils/CLAUDE.md`
- Content:
  ```markdown
  # Python Script Testing Guidelines

  ## Running tests

  ```bash
  pytest utils/test_patch_prompts.py -v
  ```

  ## Temporary directories in tests

  Use pytest's `tmp_path` fixture (auto-cleanup):
  ```python
  def test_example(tmp_path):
      (tmp_path / "file.md").write_text("content", encoding="utf-8")
  ```

  ## File I/O

  Always specify encoding explicitly:
  ```python
  path.read_text(encoding="utf-8")
  path.write_text(content, encoding="utf-8")
  path.write_bytes(b"\x00\x01")  # for binary test fixtures
  ```

  ## Debugging string issues

  ```python
  print([hex(b) for b in content.encode("utf-8")])
  ```
  ```

**Step 2: Delete PowerShell files**
- `git rm utils/patch-prompts.ps1 utils/patch-prompts.Tests.ps1`

**Step 3: Final regression**
- Command: `pytest utils/test_patch_prompts.py -v`
- Expect: ALL 20 tests PASS

**Step 4: Git Commit**
- `git add utils/CLAUDE.md`
- `git commit -m "refactor: replace PowerShell with Python, update CLAUDE.md"`
