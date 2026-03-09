# Implementation Plan - Patch Prompts Override Script

> **Reference:** `docs/designs/2025-03-09-patch-prompts-override-design.md`
> **Execution:** Use `executing-plans` skill.

---

## Overview

Create a Python utility `utils/override_prompts.py` that patches prompt files with tweaked content while preserving original headers.

---

## Task 1: Create Test File Structure

**Goal:** Set up pytest test file with fixtures.

**Step 1: Create the test file**
- File: `utils/test_override_prompts.py`
- Code:
  ```python
  """Tests for override_prompts.py"""

  from pathlib import Path
  import pytest

  @pytest.fixture
  def sample_prompt_content():
      return """<!--
  name: 'Test Prompt'
  description: 'Test description'
  ccVersion: 2.1.0
  -->
  Original body content here."""

  @pytest.fixture
  def sample_tweak_content():
      return """<!--
  name: 'Different Name'
  description: 'Different description'
  ccVersion: 9.9.9
  -->
  New tweaked content here."""

  @pytest.fixture
  def tweak_content_no_header():
      return "Plain content without any header."
  ```

**Step 2: Run Test (Red)**
- Command: `cd /c/Users/vadash/.tweakcc/system-prompts-archieve && pytest utils/test_override_prompts.py -v`
- Expect: PASS (fixtures only, no tests yet)

**Step 3: Git Commit**
- Command: `git add utils/test_override_prompts.py && git commit -m "test: add test file structure for override_prompts"`

---

## Task 2: Implement Header Extraction

**Goal:** Extract `<!--...-->` header from file content.

**Step 1: Write the Failing Test**
- File: `utils/test_override_prompts.py`
- Add to file:
  ```python
  def test_extract_header_with_valid_header(sample_prompt_content):
      """Test extracting header from content with valid header."""
      from override_prompts import extract_header

      header, body = extract_header(sample_prompt_content)

      assert "<!--" in header
      assert "-->" in header
      assert "name: 'Test Prompt'" in header
      assert body.strip() == "Original body content here."

  def test_extract_header_no_header():
      """Test extracting header from content without header."""
      from override_prompts import extract_header

      header, body = extract_header("Just body content here")

      assert header == ""
      assert body == "Just body content here"
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_override_prompts.py::test_extract_header_with_valid_header -v`
- Expect: Fail: "ModuleNotFoundError: No module named 'override_prompts'"

**Step 3: Implementation (Green)**
- File: `utils/override_prompts.py`
- Code:
  ```python
  """Override prompt files with tweaked content while preserving headers."""

  import re
  from dataclasses import dataclass
  from pathlib import Path
  from typing import Callable


  @dataclass
  class PatchResult:
      """Result of patching a single file."""
      filename: str
      was_patched: bool
      original_header: str | None


  @dataclass
  class ScanResult:
      """Result of scanning both folders."""
      matching: list[str]
      orphaned_tweaks: list[str]
      missing_tweaks: list[str]


  def extract_header(content: str) -> tuple[str, str]:
      """
      Extract the header and body from file content.

      Returns:
          (header, body) where header is the <!--...--> block (or empty),
          and body is everything after.
      """
      header_pattern = r"^(<!--[\s\S]*?-->)\s*(.*)$"
      match = re.match(header_pattern, content, re.DOTALL)

      if match:
          header = match.group(1)
          body = match.group(2)
          return header, body

      return "", content
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_override_prompts.py::test_extract_header_with_valid_header -v`
- Expect: PASS

**Step 5: Git Commit**
- Command: `git add utils/override_prompts.py utils/test_override_prompts.py && git commit -m "feat: implement header extraction"`

---

## Task 3: Implement Folder Scanning

**Goal:** Scan both directories and categorize files.

**Step 1: Write the Failing Test**
- File: `utils/test_override_prompts.py`
- Add to file:
  ```python
  def test_scan_folders(tmp_path):
      """Test scanning two folders for file matching."""
      from override_prompts import scan_folders

      # Create prompt folder with files
      prompt_dir = tmp_path / "prompt"
      prompt_dir.mkdir()
      (prompt_dir / "file1.md").write_text("prompt1")
      (prompt_dir / "file2.md").write_text("prompt2")
      (prompt_dir / "only_in_prompt.md").write_text("only_prompt")

      # Create tweak folder with files
      tweak_dir = tmp_path / "tweak"
      tweak_dir.mkdir()
      (tweak_dir / "file1.md").write_text("tweak1")
      (tweak_dir / "file2.md").write_text("tweak2")
      (tweak_dir / "only_in_tweak.txt").write_text("only_tweak")

      result = scan_folders(prompt_dir, tweak_dir)

      assert sorted(result.matching) == ["file1.md", "file2.md"]
      assert result.orphaned_tweaks == ["only_in_tweak.txt"]
      assert result.missing_tweaks == ["only_in_prompt.md"]
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_override_prompts.py::test_scan_folders -v`
- Expect: Fail: "function not found"

**Step 3: Implementation (Green)**
- File: `utils/override_prompts.py`
- Add function after `extract_header`:
  ```python
  def scan_folders(prompt_dir: Path, tweak_dir: Path) -> ScanResult:
      """
      Scan both directories and categorize files.

      Returns files that match, are only in tweak, or only in prompt.
      """
      prompt_files = {f.name for f in prompt_dir.iterdir() if f.is_file()}
      tweak_files = {f.name for f in tweak_dir.iterdir() if f.is_file()}

      matching = sorted(prompt_files & tweak_files)
      orphaned_tweaks = sorted(tweak_files - prompt_files)
      missing_tweaks = sorted(prompt_files - tweak_files)

      return ScanResult(
          matching=matching,
          orphaned_tweaks=orphaned_tweaks,
          missing_tweaks=missing_tweaks,
      )
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_override_prompts.py::test_scan_folders -v`
- Expect: PASS

**Step 5: Git Commit**
- Command: `git add utils/override_prompts.py utils/test_override_prompts.py && git commit -m "feat: implement folder scanning"`

---

## Task 4: Implement File Patching

**Goal:** Patch single file with header preservation.

**Step 1: Write the Failing Test**
- File: `utils/test_override_prompts.py`
- Add to file:
  ```python
  def test_patch_file_preserves_header(tmp_path, sample_prompt_content, sample_tweak_content):
      """Test that patching preserves original header."""
      from override_prompts import patch_file

      # Create prompt and tweak files
      prompt_file = tmp_path / "test.md"
      prompt_file.write_text(sample_prompt_content, encoding="utf-8")

      tweak_file = tmp_path / "tweak.md"
      tweak_file.write_text(sample_tweak_content, encoding="utf-8")

      # Patch
      result = patch_file(prompt_file, tweak_file)

      # Verify
      assert result.was_patched is True
      assert result.filename == "test.md"
      assert "name: 'Test Prompt'" in result.original_header

      patched_content = prompt_file.read_text(encoding="utf-8")
      assert patched_content.startswith("<!--")
      assert "name: 'Test Prompt'" in patched_content  # Original header
      assert "New tweaked content here" in patched_content  # Tweak body
      assert "Different Name" not in patched_content  # Tweak header removed

  def test_patch_file_tweak_no_header(tmp_path, sample_prompt_content, tweak_content_no_header):
      """Test patching when tweak has no header."""
      from override_prompts import patch_file

      prompt_file = tmp_path / "test.md"
      prompt_file.write_text(sample_prompt_content, encoding="utf-8")

      tweak_file = tmp_path / "tweak.md"
      tweak_file.write_text(tweak_content_no_header, encoding="utf-8")

      result = patch_file(prompt_file, tweak_file)

      patched_content = prompt_file.read_text(encoding="utf-8")
      assert "name: 'Test Prompt'" in patched_content
      assert "Plain content without any header" in patched_content
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_override_prompts.py::test_patch_file_preserves_header -v`
- Expect: Fail: "function not found"

**Step 3: Implementation (Green)**
- File: `utils/override_prompts.py`
- Add function after `scan_folders`:
  ```python
  def patch_file(prompt_path: Path, tweak_path: Path) -> PatchResult:
      """
      Patch a single prompt file with content from tweak file.

      1. Read prompt file, extract header
      2. Read tweak file, extract body (skip header if present)
      3. Combine and write back to prompt file
      """
      prompt_content = prompt_path.read_text(encoding="utf-8")
      tweak_content = tweak_path.read_text(encoding="utf-8")

      original_header, _ = extract_header(prompt_content)
      _, tweak_body = extract_header(tweak_content)

      new_content = f"{original_header}\n{tweak_body}"
      prompt_path.write_text(new_content, encoding="utf-8")

      return PatchResult(
          filename=prompt_path.name,
          was_patched=True,
          original_header=original_header or None,
      )
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_override_prompts.py::test_patch_file_preserves_header -v`
- Expect: PASS

**Step 5: Git Commit**
- Command: `git add utils/override_prompts.py utils/test_override_prompts.py && git commit -m "feat: implement file patching"`

---

## Task 5: Implement Report Generation

**Goal:** Generate sorted markdown checklist.

**Step 1: Write the Failing Test**
- File: `utils/test_override_prompts.py`
- Add to file:
  ```python
  def test_generate_report_sorted():
      """Test that report is sorted by checkbox then alphabetically."""
      from override_prompts import generate_report, ScanResult, PatchResult

      scan = ScanResult(
          matching=["zebra.md", "apple.md", "middle.md"],
          orphaned_tweaks=["orphan.txt"],
          missing_tweaks=["missing.md"],
      )

      results = [
          PatchResult(filename="zebra.md", was_patched=True, original_header="<!-- -->"),
          PatchResult(filename="apple.md", was_patched=True, original_header="<!-- -->"),
          PatchResult(filename="middle.md", was_patched=False, original_header=None),
      ]

      report = generate_report("test_folder", results, scan)
      lines = report.strip().split("\n")

      # Check order: checked items first, alphabetically, then unchecked
      assert lines[0] == "- [x] apple.md"
      assert lines[1] == "- [x] zebra.md"
      assert lines[2] == "- [ ] middle.md"

      # Check that orphaned and missing are in report
      assert "orphan.txt" in report
      assert "missing.md" in report
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_override_prompts.py::test_generate_report_sorted -v`
- Expect: Fail: "function not found"

**Step 3: Implementation (Green)**
- File: `utils/override_prompts.py`
- Add function after `patch_file`:
  ```python
  def generate_report(folder_name: str, results: list[PatchResult], scan: ScanResult) -> str:
      """
      Generate markdown report content.

      Format:
      - [x] filename.md  (for patched files)
      - [ ] filename.md  (for not patched)

      Sorted: checked first, then alphabetically.
      """
      lines = []

      # Sort by was_patched (True first) then alphabetically
      sorted_results = sorted(results, key=lambda r: (not r.was_patched, r.filename))

      for r in sorted_results:
          checkbox = "[x]" if r.was_patched else "[ ]"
          lines.append(f"- {checkbox} {r.filename}")

      # Add warnings section if any mismatches
      if scan.orphaned_tweaks or scan.missing_tweaks:
          lines.append("\n## Warnings")
          for f in scan.orphaned_tweaks:
              lines.append(f"- [WARNING] File in tweak but not prompt: {f}")
          for f in scan.missing_tweaks:
              lines.append(f"- [WARNING] File in prompt but not tweak: {f}")

      return "\n".join(lines)
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_override_prompts.py::test_generate_report_sorted -v`
- Expect: PASS

**Step 5: Git Commit**
- Command: `git add utils/override_prompts.py utils/test_override_prompts.py && git commit -m "feat: implement report generation"`

---

## Task 6: Implement Main CLI

**Goal:** Wire up CLI entry point.

**Step 1: Write the Integration Test**
- File: `utils/test_override_prompts.py`
- Add to file:
  ```python
  def test_main_integration(tmp_path, monkeypatch, capsys):
      """Test full CLI flow with mocked input."""
      from override_prompts import main

      # Setup directories
      prompt_dir = tmp_path / "2171"
      prompt_dir.mkdir()
      (prompt_dir / "file1.md").write_text("<!--Header1-->\nbody1", encoding="utf-8")
      (prompt_dir / "file2.md").write_text("<!--Header2-->\nbody2", encoding="utf-8")

      tweak_dir = tmp_path / "tmp"
      tweak_dir.mkdir()
      (tweak_dir / "file1.md").write_text("<!--TweakHeader-->\nnew_body1", encoding="utf-8")
      (tweak_dir / "file2.md").write_text("new_body2", encoding="utf-8")

      # Change to tmp_path so report file is created there
      monkeypatch.chdir(tmp_path)

      # Mock input to return our test directories
      inputs = iter([str(prompt_dir), str(tweak_dir)])
      monkeypatch.setattr("builtins.input", lambda _: next(inputs))

      # Run
      main()

      # Capture output
      captured = capsys.readouterr()

      # Check warnings printed
      assert "Report written to:" in captured.out

      # Check report file exists
      report_file = tmp_path / "2171.md"
      assert report_file.exists()

      report_content = report_file.read_text(encoding="utf-8")
      assert "- [x] file1.md" in report_content
      assert "- [x] file2.md" in report_content

      # Check file1 was patched correctly
      file1_content = (prompt_dir / "file1.md").read_text(encoding="utf-8")
      assert "Header1" in file1_content  # Original header preserved
      assert "new_body1" in file1_content  # Tweak body applied
      assert "TweakHeader" not in file1_content  # Tweak header removed
  ```

**Step 2: Run Test (Red)**
- Command: `pytest utils/test_override_prompts.py::test_main_integration -v`
- Expect: Fail (function incomplete or errors)

**Step 3: Implementation (Green)**
- File: `utils/override_prompts.py`
- Add to end of file:
  ```python
  def main() -> None:
      """CLI entry point."""
      prompt_folder = input("Enter prompt folder (e.g., 2171): ").strip()
      prompt_path = Path(prompt_folder).resolve()

      tweak_folder = input("Enter tweak folder (e.g., tmp): ").strip()
      tweak_path = Path(tweak_folder).resolve()

      if not prompt_path.is_dir():
          print(f"Error: '{prompt_path}' is not a directory.", file=sys.stderr)
          sys.exit(1)
      if not tweak_path.is_dir():
          print(f"Error: '{tweak_path}' is not a directory.", file=sys.stderr)
          sys.exit(1)

      scan = scan_folders(prompt_path, tweak_path)

      for f in scan.orphaned_tweaks:
          print(f"[WARNING] File in tweak but not prompt: {tweak_path / f}")
      for f in scan.missing_tweaks:
          print(f"[WARNING] File in prompt but not tweak: {prompt_path / f}")

      results = []
      for filename in scan.matching:
          result = patch_file(prompt_path / filename, tweak_path / filename)
          results.append(result)

      report_path = Path(f"{prompt_path.name}.md")
      content = generate_report(prompt_path.name, results, scan)
      report_path.write_text(content, encoding="utf-8")
      print(f"Report written to: {report_path}")


  if __name__ == "__main__":
      import sys
      main()
  ```

**Step 4: Verify (Green)**
- Command: `pytest utils/test_override_prompts.py::test_main_integration -v`
- Expect: PASS

**Step 5: Git Commit**
- Command: `git add utils/override_prompts.py utils/test_override_prompts.py && git commit -m "feat: implement main CLI"`

---

## Task 7: Run Full Test Suite

**Goal:** Verify all tests pass.

**Step 1: Run All Tests**
- Command: `pytest utils/test_override_prompts.py -v`
- Expect: All tests PASS

**Step 2: Git Commit**
- Command: `git add utils/test_override_prompts.py && git commit -m "test: all tests passing for override_prompts"`

---

## Completion Checklist

- [ ] All tests pass
- [ ] Script can be run: `python utils/override_prompts.py`
- [ ] Report file generated with correct sorting
- [ ] Headers preserved from original files
- [ ] Warnings printed for non-matching files
