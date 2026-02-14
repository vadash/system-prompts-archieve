# Python Script Testing Guidelines

## Running tests

```bash
pytest utils/test_patch_prompts.py -v
```

## Temporary directories in tests

Use pytest's `tmp_path` fixture (auto-cleanup):
```python
def test_example(tmp_path):
    (tmp_path / "file.md").write_text("content", encoding="utf-8")
```

## File I/O

Always specify encoding explicitly:
```python
path.read_text(encoding="utf-8")
path.write_text(content, encoding="utf-8")
path.write_bytes(b"\x00\x01")  # for binary test fixtures
```

## Debugging string issues

```python
print([hex(b) for b in content.encode("utf-8")])
```
