#!/usr/bin/env python3
"""
Structural validation for Claude Code skills.

Checks: frontmatter validity, naming conventions, description length,
body word count, referenced file existence, orphaned resources,
bundled agent coverage.
"""

import sys
import re
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    print("pyyaml not installed — run 'pip install pyyaml' to enable structural validation. Skipping.")
    sys.exit(0)

RESOURCE_DIRS = ("references", "scripts", "assets")
IGNORED_FILES = {"__init__.py", ".DS_Store"}
IGNORED_DIRS = {"__pycache__"}
BODY_WORD_LIMIT = 2000
DESC_DISPLAY_CAP = 250
DESC_HARD_CAP = 1024
NAME_MAX_LEN = 64
COMPAT_MAX_LEN = 500
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata", "compatibility", "argument-hint", "effort", "when_to_use"}


def check_frontmatter(content, skill_path):
    """Validate YAML frontmatter. Returns (frontmatter_dict, body_text, errors, warnings)."""
    errors = []
    warnings = []

    if not content.startswith("---"):
        return None, content, ["No YAML frontmatter found"], warnings

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, content, ["Invalid frontmatter format"], warnings

    frontmatter_text = match.group(1)
    body = content[match.end():]

    try:
        fm = yaml.safe_load(frontmatter_text)
        if not isinstance(fm, dict):
            return None, body, ["Frontmatter must be a YAML dictionary"], warnings
    except yaml.YAMLError as e:
        return None, body, [f"Invalid YAML in frontmatter: {e}"], warnings

    unexpected = set(fm.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if "name" not in fm:
        errors.append("Missing 'name' in frontmatter")
    else:
        name = fm["name"]
        if not isinstance(name, str):
            errors.append(f"Name must be a string, got {type(name).__name__}")
        else:
            name = name.strip()
            if name:
                if not re.match(r"^[a-z0-9-]+$", name):
                    errors.append(f"Name '{name}' should be kebab-case (lowercase letters, digits, hyphens)")
                if name.startswith("-") or name.endswith("-") or "--" in name:
                    errors.append(f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens")
                if len(name) > NAME_MAX_LEN:
                    errors.append(f"Name is too long ({len(name)} chars). Maximum is {NAME_MAX_LEN}.")

    if "description" not in fm:
        errors.append("Missing 'description' in frontmatter")
    else:
        desc = fm["description"]
        if not isinstance(desc, str):
            errors.append(f"Description must be a string, got {type(desc).__name__}")
        else:
            desc = desc.strip()
            if desc:
                if "<" in desc or ">" in desc:
                    errors.append("Description cannot contain angle brackets (< or >)")
                if len(desc) > DESC_HARD_CAP:
                    errors.append(f"Description is too long ({len(desc)} chars). Maximum is {DESC_HARD_CAP}.")
                elif len(desc) > DESC_DISPLAY_CAP:
                    warnings.append(
                        f"Description is {len(desc)} chars. "
                        f"The /skills listing truncates at {DESC_DISPLAY_CAP} — the last "
                        f"{len(desc) - DESC_DISPLAY_CAP} characters are invisible during skill selection."
                    )

    compat = fm.get("compatibility", "")
    if compat:
        if not isinstance(compat, str):
            errors.append(f"Compatibility must be a string, got {type(compat).__name__}")
        elif len(compat) > COMPAT_MAX_LEN:
            errors.append(f"Compatibility is too long ({len(compat)} chars). Maximum is {COMPAT_MAX_LEN}.")

    return fm, body, errors, warnings


def check_body_word_count(body):
    """Warn if body exceeds word limit."""
    words = body.split()
    if len(words) > BODY_WORD_LIMIT:
        return [f"Body is {len(words)} words (limit: {BODY_WORD_LIMIT}). Move detailed content to references/."]
    return []


def find_resource_references(body):
    """Extract referenced resource paths from SKILL.md body."""
    refs = set()
    for resource_dir in RESOURCE_DIRS:
        pattern = rf"`?{resource_dir}/([a-zA-Z0-9_][a-zA-Z0-9_.\-]*)`?"
        for m in re.finditer(pattern, body):
            refs.add(f"{resource_dir}/{m.group(1)}")
    return refs


def check_referenced_files(body, skill_path):
    """Fail if any referenced resource file doesn't exist."""
    refs = find_resource_references(body)
    missing = []
    for ref in sorted(refs):
        if not (skill_path / ref).exists():
            missing.append(ref)
    if missing:
        return [f"Referenced file not found: {f}" for f in missing]
    return []


def check_orphaned_resources(body, skill_path):
    """Warn about resource files that exist but are never referenced."""
    refs = find_resource_references(body)
    orphans = []
    for resource_dir in RESOURCE_DIRS:
        dir_path = skill_path / resource_dir
        if not dir_path.is_dir():
            continue
        for f in sorted(dir_path.rglob("*")):
            if not f.is_file():
                continue
            if f.name in IGNORED_FILES:
                continue
            if any(part in IGNORED_DIRS for part in f.parts):
                continue
            relative = f.relative_to(skill_path).as_posix()
            if relative not in refs:
                orphans.append(relative)
    if orphans:
        return [f"Unreferenced resource (orphan): {f}" for f in orphans]
    return []


def check_agent_files(body, skill_path):
    """Cross-check agent types spawned in the body against bundled agents/ files.

    Only runs when the skill bundles an agents/ directory — skills may
    legitimately spawn agents that are installed separately.
    """
    errors = []
    warnings = []
    agents_dir = skill_path / "agents"
    if not agents_dir.is_dir():
        return errors, warnings
    referenced = set(re.findall(r"(?:subagent_type|agent type):?\s*`([a-z0-9-]+)`", body))
    bundled = {f.stem for f in agents_dir.glob("*.md")}
    for name in sorted(referenced - bundled):
        errors.append(f"Spawned agent type '{name}' has no matching agents/{name}.md")
    for name in sorted(bundled - referenced):
        warnings.append(f"Bundled agent never spawned in SKILL.md (orphan): agents/{name}.md")
    return errors, warnings


def validate_skill(skill_path):
    """Validate a skill directory. Returns (valid, messages, warnings)."""
    skill_path = Path(skill_path)
    all_errors = []
    all_warnings = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found", []

    content = skill_md.read_text()

    fm, body, fm_errors, fm_warnings = check_frontmatter(content, skill_path)
    all_errors.extend(fm_errors)
    all_warnings.extend(fm_warnings)

    if fm is not None:
        all_warnings.extend(check_body_word_count(body))
        all_errors.extend(check_referenced_files(body, skill_path))
        all_warnings.extend(check_orphaned_resources(body, skill_path))
        agent_errors, agent_warnings = check_agent_files(body, skill_path)
        all_errors.extend(agent_errors)
        all_warnings.extend(agent_warnings)

    if all_errors:
        return False, "; ".join(all_errors), all_warnings

    return True, "Skill is valid!", all_warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <skill_directory>")
        sys.exit(1)

    valid, message, warnings = validate_skill(sys.argv[1])
    print(message)
    for w in warnings:
        print(f"  WARNING: {w}")
    sys.exit(0 if valid else 1)
