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
