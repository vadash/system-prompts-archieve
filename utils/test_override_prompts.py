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
