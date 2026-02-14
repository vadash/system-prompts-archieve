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
