# Path Encoding Reference

Claude Code encodes project paths as directory names in `~/.claude/projects/`.

## Encoding Scheme

| Original | Encoded As |
|----------|------------|
| `/` (path separator) | `-` |
| ` ` (space) | `-` |
| `.` (leading dot for dotfiles) | `--` (double hyphen) |

**Examples:**

| Original Path | Encoded |
|---------------|---------|
| `/Users/jdoe` | `-Users-jdoe` |
| `/Users/jdoe/.claude` | `-Users-jdoe--claude` |
| `/Users/jdoe/My Project` | `-Users-jdoe-My-Project` |

## The Ambiguity Problem

The encoding is **lossy**. These three different paths encode identically:

```
/Users/jdoe/foo/bar        → -Users-jdoe-foo-bar
/Users/jdoe/foo bar        → -Users-jdoe-foo-bar
/Users/jdoe/foo-bar        → -Users-jdoe-foo-bar
```

There is no way to decode unambiguously without checking the filesystem.

## Smart Decoding Strategy

The `cc-health.py` script uses a verification approach:

1. Try naive decode (all `-` → `/`)
2. If path doesn't exist, walk segments and try:
   - Combining adjacent segments with hyphens (`foo-bar`)
   - Combining adjacent segments with spaces (`foo bar`)
3. Return the first combination that exists on disk

This correctly resolves most real-world paths, but may fail for:
- Deleted directories (no way to verify)
- Paths with mixed hyphens/spaces in same segment

## In Python

```python
def decode_project_path(encoded: str) -> str:
    """Naive decode — may be wrong for hyphenated/spaced names."""
    if not encoded.startswith("-"):
        return encoded
    decoded = encoded[1:].replace("--", "/.")
    return "/" + decoded.replace("-", "/")

def verify_path_exists(encoded: str) -> tuple[bool, str]:
    """Smart decode with filesystem verification."""
    # See cc-health.py for full implementation
    pass
```
