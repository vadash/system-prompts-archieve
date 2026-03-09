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
