"""Override prompt files with multi-file tweak format.

Tweak files contain <file path="..."> blocks with replacement content.
Each tweak file can have multiple file replacements.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PatchResult:
    """Result of patching a single file."""
    filename: str
    was_patched: bool
    original_header: str | None
    error: str | None = None


def extract_header(content: str) -> tuple[str, str]:
    """
    Extract the XML header and body from file content.

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


def parse_tweak_file(content: str) -> dict[str, str]:
    """
    Parse a tweak file containing <file path="..."> blocks.

    Returns:
        dict mapping filename -> replacement content (including header)
    """
    # Pattern: <file path="filename.md"> ...content... </file>
    # Using non-greedy match to capture each block
    pattern = r'<file path="([^"]+)">\s*([\s\S]*?)\s*</file>'

    patches = {}
    for match in re.finditer(pattern, content):
        filename = match.group(1)
        file_content = match.group(2).strip()
        patches[filename] = file_content

    return patches


def collect_all_tweaks(tweak_dir: Path) -> dict[str, str]:
    """
    Read all tweak files and collect patches.

    Returns:
        dict mapping filename -> replacement content
        (later files override earlier ones if same filename)
    """
    all_patches = {}

    for tweak_file in tweak_dir.iterdir():
        if not tweak_file.is_file():
            continue

        content = tweak_file.read_text(encoding="utf-8")
        patches = parse_tweak_file(content)

        # Merge, with later files taking precedence
        all_patches.update(patches)

    return all_patches


def patch_file(prompt_path: Path, tweak_content: str) -> PatchResult:
    """
    Patch a single prompt file with tweak content.

    Preserves original header, replaces body with tweak body.
    """
    prompt_content = prompt_path.read_text(encoding="utf-8")

    original_header, _ = extract_header(prompt_content)
    _, tweak_body = extract_header(tweak_content)

    new_content = f"{original_header}\n{tweak_body}"
    prompt_path.write_text(new_content, encoding="utf-8")

    return PatchResult(
        filename=prompt_path.name,
        was_patched=True,
        original_header=original_header or None,
    )


def scan_and_patch(prompt_dir: Path, tweak_dir: Path) -> tuple[list[PatchResult], list[str], list[str]]:
    """
    Scan both directories and apply patches.

    Returns:
        (results, not_found_in_prompt, not_found_in_tweak)
    """
    # Get all files in prompt directory
    prompt_files = {f.name for f in prompt_dir.iterdir() if f.is_file()}

    # Collect all tweaks
    all_tweaks = collect_all_tweaks(tweak_dir)

    # Categorize
    matching = set(prompt_files) & set(all_tweaks.keys())
    not_found_in_prompt = set(all_tweaks.keys()) - set(prompt_files)
    not_found_in_tweak = set(prompt_files) - set(all_tweaks.keys())

    # Patch matching files
    results = []
    for filename in sorted(matching):
        prompt_path = prompt_dir / filename
        tweak_content = all_tweaks[filename]

        try:
            result = patch_file(prompt_path, tweak_content)
            results.append(result)
        except Exception as e:
            results.append(PatchResult(
                filename=filename,
                was_patched=False,
                original_header=None,
                error=str(e),
            ))

    return results, sorted(not_found_in_prompt), sorted(not_found_in_tweak)


def generate_report(
    folder_name: str,
    results: list[PatchResult],
    not_found_in_prompt: list[str],
    not_found_in_tweak: list[str],
) -> str:
    """Generate markdown report content."""
    lines = []

    # Sort by was_patched (True first) then alphabetically
    sorted_results = sorted(results, key=lambda r: (not r.was_patched, r.filename))

    for r in sorted_results:
        checkbox = "[x]" if r.was_patched else "[ ]"
        line = f"- {checkbox} {r.filename}"
        if r.error:
            line += f" (ERROR: {r.error})"
        lines.append(line)

    # Add warnings section if any mismatches
    if not_found_in_prompt or not_found_in_tweak:
        lines.append("\n## Warnings")
        for f in not_found_in_prompt:
            lines.append(f"- [WARNING] Tweak file not in prompt folder: {f}")
        for f in not_found_in_tweak:
            lines.append(f"- [WARNING] Prompt file not in tweaks: {f}")

    return "\n".join(lines)


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

    results, not_found_in_prompt, not_found_in_tweak = scan_and_patch(prompt_path, tweak_path)

    for f in not_found_in_prompt:
        print(f"[WARNING] Tweak file not in prompt folder: {f}")
    for f in not_found_in_tweak:
        print(f"[WARNING] Prompt file not in tweaks: {f}")

    report_path = Path(f"{prompt_path.name}.md")
    content = generate_report(prompt_path.name, results, not_found_in_prompt, not_found_in_tweak)
    report_path.write_text(content, encoding="utf-8")
    print(f"Report written to: {report_path}")
    print(f"Patched {sum(1 for r in results if r.was_patched)} files.")


if __name__ == "__main__":
    main()
