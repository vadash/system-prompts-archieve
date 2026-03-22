#!/usr/bin/env python3
"""Patch system-prompt files: minimal backtick escape, fix line endings."""

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

def escape_backticks_in_content(text: str) -> str:
    """Escape backticks that appear in content (not in code blocks).

    Only escapes backticks that:
    - Are not already escaped (not preceded by \\)
    - Appear after a blank line or at start of content (not inside ``` blocks)
    """
    if not text:
        return text

    # Split into frontmatter and content
    lines = text.split('\n')
    result_lines = []
    in_frontmatter = False
    in_code_block = False
    frontmatter_started = False

    for line in lines:
        # Handle frontmatter
        if line == '---':
            if not frontmatter_started:
                in_frontmatter = True
                frontmatter_started = True
            else:
                in_frontmatter = False
            result_lines.append(line)
            continue

        if in_frontmatter:
            result_lines.append(line)
            continue

        # Handle code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result_lines.append(line)
            continue

        if in_code_block:
            result_lines.append(line)
            continue

        # In regular content: escape unescaped backticks
        # Only escape backticks that are standalone (not part of ${...})
        result = re.sub(r'(?<!\\)(?<!\$)`', r'\`', line)
        result_lines.append(result)

    return '\n'.join(result_lines)


def unescape_template_vars(text: str) -> str:
    """Remove unnecessary escaping from ${...} template variables."""
    if not text:
        return text
    # Convert \${ back to ${
    return re.sub(r'\\\$\{', r'${', text)


def ensure_trailing_newline(text: str) -> str:
    """Ensure file ends with a newline."""
    if not text:
        return text
    if not text.endswith('\n'):
        return text + '\n'
    return text


def fix_line_endings(text: str) -> str:
    if not text:
        return text
    return text.replace("\r\n", "\n")

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


# --- Registered fixers ---

@fixer("Fix template variables", filter="*.md")
def _fixer_unescape_templates(file_path: Path) -> bool:
    r"""Remove \ escaping from ${...} variables."""
    content = file_path.read_text(encoding="utf-8")
    fixed = unescape_template_vars(content)
    if fixed != content:
        file_path.write_text(fixed, encoding="utf-8")
        return True
    return False


@fixer("Ensure trailing newline", filter="*.md")
def _fixer_trailing_newline(file_path: Path) -> bool:
    """Ensure files end with a newline."""
    content = file_path.read_text(encoding="utf-8")
    fixed = ensure_trailing_newline(content)
    if fixed != content:
        file_path.write_text(fixed, encoding="utf-8")
        return True
    return False


@fixer("Fix line endings", filter="*")
def _fixer_fix_line_endings(file_path: Path) -> bool:
    raw = file_path.read_bytes()
    if b"\r\n" not in raw:
        return False
    content = raw.decode("utf-8")
    fixed = fix_line_endings(content)
    file_path.write_text(fixed, encoding="utf-8", newline="\n")
    return True


# --- CLI entry point ---

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
