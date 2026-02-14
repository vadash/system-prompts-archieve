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
