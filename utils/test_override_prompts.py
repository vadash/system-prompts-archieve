"""Tests for override_prompts.py - multi-file tweak format."""

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
def multi_file_tweak_content():
    return """<file path="file1.md">
<!--
name: 'File 1'
-->
New content for file 1.
</file>

<file path="file2.md">
Plain content without header for file 2.
</file>

<file path="subdir/file3.md">
<!--
name: 'File 3'
-->
Content for file 3 in subdirectory.
</file>"""


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


def test_parse_tweak_file(multi_file_tweak_content):
    """Test parsing multi-file tweak format."""
    from override_prompts import parse_tweak_file

    patches = parse_tweak_file(multi_file_tweak_content)

    assert len(patches) == 3
    assert "file1.md" in patches
    assert "file2.md" in patches
    assert "subdir/file3.md" in patches

    # Check content preservation
    assert "New content for file 1" in patches["file1.md"]
    assert "Plain content without header" in patches["file2.md"]
    assert "Content for file 3 in subdirectory" in patches["subdir/file3.md"]


def test_parse_tweak_file_empty():
    """Test parsing empty tweak file."""
    from override_prompts import parse_tweak_file

    patches = parse_tweak_file("")
    assert patches == {}


def test_patch_file_preserves_header(tmp_path, sample_prompt_content):
    """Test that patching preserves original header."""
    from override_prompts import patch_file

    prompt_file = tmp_path / "test.md"
    prompt_file.write_text(sample_prompt_content, encoding="utf-8")

    tweak_content = """<!--
name: 'Different Name'
-->
New body content."""

    result = patch_file(prompt_file, tweak_content)

    assert result.was_patched is True
    assert result.filename == "test.md"
    assert "name: 'Test Prompt'" in result.original_header

    patched_content = prompt_file.read_text(encoding="utf-8")
    assert patched_content.startswith("<!--")
    assert "name: 'Test Prompt'" in patched_content  # Original header
    assert "New body content" in patched_content  # Tweak body
    assert "Different Name" not in patched_content  # Tweak header removed


def test_collect_all_tweaks(tmp_path):
    """Test collecting tweaks from multiple files."""
    from override_prompts import collect_all_tweaks

    # Create multiple tweak files
    (tmp_path / "tweak1.txt").write_text("""<file path="file1.md">Content 1</file>
<file path="file2.md">Content 2</file>""", encoding="utf-8")

    (tmp_path / "tweak2.txt").write_text("""<file path="file3.md">Content 3</file>
<file path="file1.md">Content 1 overridden</file>""", encoding="utf-8")

    patches = collect_all_tweaks(tmp_path)

    assert len(patches) == 3
    assert patches["file1.md"] == "Content 1 overridden"  # Later file wins
    assert patches["file2.md"] == "Content 2"
    assert patches["file3.md"] == "Content 3"


def test_scan_and_patch(tmp_path, sample_prompt_content):
    """Test full scan and patch workflow."""
    from override_prompts import scan_and_patch

    # Setup prompt directory
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "file1.md").write_text(sample_prompt_content, encoding="utf-8")
    (prompt_dir / "file2.md").write_text("<!--Header2-->\nbody2", encoding="utf-8")
    (prompt_dir / "only_in_prompt.md").write_text("content", encoding="utf-8")

    # Setup tweak directory
    tweak_dir = tmp_path / "tweaks"
    tweak_dir.mkdir()
    (tweak_dir / "tweaks.txt").write_text("""<file path="file1.md">New content 1</file>
<file path="file2.md">New content 2</file>
<file path="not_in_prompt.md">Orphan tweak</file>""", encoding="utf-8")

    results, not_found_in_prompt, not_found_in_tweak = scan_and_patch(prompt_dir, tweak_dir)

    # Check results
    assert len(results) == 2
    assert all(r.was_patched for r in results)
    assert [r.filename for r in results] == ["file1.md", "file2.md"]

    # Check not found
    assert not_found_in_prompt == ["not_in_prompt.md"]
    assert not_found_in_tweak == ["only_in_prompt.md"]

    # Verify file1 was patched correctly
    file1_content = (prompt_dir / "file1.md").read_text(encoding="utf-8")
    assert "name: 'Test Prompt'" in file1_content  # Original header
    assert "New content 1" in file1_content  # Tweak body


def test_generate_report():
    """Test report generation."""
    from override_prompts import generate_report, PatchResult

    results = [
        PatchResult(filename="zebra.md", was_patched=True, original_header="<!-- -->"),
        PatchResult(filename="apple.md", was_patched=True, original_header="<!-- -->"),
        PatchResult(filename="middle.md", was_patched=False, original_header=None, error="Some error"),
    ]

    report = generate_report("test", results, ["orphan.md"], ["missing.md"])
    lines = report.strip().split("\n")

    # Check order: patched first, alphabetically
    assert lines[0] == "- [x] apple.md"
    assert lines[1] == "- [x] zebra.md"
    assert "- [ ] middle.md (ERROR: Some error)" in lines[2]

    # Check warnings
    assert "orphan.md" in report
    assert "missing.md" in report


def test_main_integration(tmp_path, monkeypatch, capsys):
    """Test full CLI flow."""
    from override_prompts import main

    # Setup directories
    prompt_dir = tmp_path / "2171"
    prompt_dir.mkdir()
    (prompt_dir / "file1.md").write_text("<!--Header1-->\nbody1", encoding="utf-8")

    tweak_dir = tmp_path / "tmp"
    tweak_dir.mkdir()
    (tweak_dir / "tweaks.txt").write_text('<file path="file1.md">new_body1</file>', encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    inputs = iter([str(prompt_dir), str(tweak_dir)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    assert "Report written to:" in captured.out
    assert "Patched 1 files" in captured.out

    # Check report file exists
    report_file = tmp_path / "2171.md"
    assert report_file.exists()

    report_content = report_file.read_text(encoding="utf-8")
    assert "- [x] file1.md" in report_content

    # Check file was patched
    file1_content = (prompt_dir / "file1.md").read_text(encoding="utf-8")
    assert "Header1" in file1_content
    assert "new_body1" in file1_content
