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
