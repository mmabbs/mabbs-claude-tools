"""Lightweight YAML frontmatter parser for SKILL.md files. Stdlib only.

Extracts name, description, and whenToUse from the --- delimited
frontmatter block. Handles single-line values, folded (>) and
literal (|) scalar styles.
"""

import re

_FIELDS = {"name", "description", "whenToUse"}

_KEY_RE = re.compile(r"^([a-zA-Z_][\w-]*)\s*:\s*(.*)?$")


def parse_skill_frontmatter(text: str) -> dict:
    """Parse SKILL.md frontmatter and return name, description, whenToUse.

    Returns dict with keys: name, description, whenToUse (each str | None).
    """
    result = {"name": None, "description": None, "whenToUse": None}

    if not text.startswith("---"):
        return result

    # Find closing ---
    end_idx = text.find("\n---", 3)
    if end_idx == -1:
        return result

    frontmatter = text[4:end_idx]
    lines = frontmatter.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i]
        match = _KEY_RE.match(line)
        if not match:
            i += 1
            continue

        key = match.group(1)
        value = (match.group(2) or "").strip()

        if key not in _FIELDS:
            i += 1
            continue

        # Strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]

        if value in (">", "|"):
            # Multiline scalar — collect indented continuation lines
            scalar_type = value
            parts = []
            i += 1
            while i < len(lines):
                cont = lines[i]
                if cont and not cont[0].isspace():
                    break
                parts.append(cont.strip())
                i += 1
            if scalar_type == ">":
                result[key] = " ".join(p for p in parts if p) or None
            else:
                result[key] = "\n".join(parts).strip() or None
            continue

        result[key] = value if value else None
        i += 1

    return result
