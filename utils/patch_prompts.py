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
    if not text:
        return text
    # Escape unescaped backticks (not preceded by \)
    result = re.sub(r'(?<!\\)`', r'\`', text)
    # Escape unescaped template literal ${ (not preceded by \)
    result = re.sub(r'(?<!\\)\$\{', r'\${', result)
    return result

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
    ...


# --- Registered fixers ---

@fixer("Escape backticks", filter="*.md")
def _fixer_escape_backticks(file_path: Path) -> bool:
    return False

@fixer("Fix line endings", filter="*")
def _fixer_fix_line_endings(file_path: Path) -> bool:
    return False
