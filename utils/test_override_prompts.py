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
