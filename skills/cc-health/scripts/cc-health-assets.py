#!/usr/bin/env python3
"""
cc-health assets domain — checks skill/agent/plugin/workflow definitions for consistency.

Checks:
1. Broken Skill() calls — references to skills that don't exist
2. Broken agent references — Agent() calls with non-existent subagent_type
3. Dead @-imports — CLAUDE.md @-import chains pointing at missing files
4. Deprecated duplicates — archived skills still in active directory
5. (--deep only, handled by SKILL.md) Description drift
6. Model/effort validity — bare aliases or invalid effort values
7. Trigger clashes -- overlapping skill trigger descriptions

Usage:
    python3 cc-health-assets.py [--base-dir PATH] [--clash-threshold FLOAT]

Outputs AuditReport JSON to stdout.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.schema import AuditReport, Finding, progress, load_state, save_state
from lib.frontmatter import parse_skill_frontmatter
from lib.tfidf import tokenize, build_tfidf, cosine_similarity, top_shared_terms

# Valid full model IDs (pattern: claude-<name>-<version> with optional suffix)
MODEL_ID_PATTERN = re.compile(r"^claude-[a-z]+-\d+(-\d+)?(-\d{8})?(\[\d+[a-z]?\])?$")

# Valid effort levels
VALID_EFFORTS = {"low", "medium", "high", "xhigh", "max"}

# Patterns to find Skill() calls
SKILL_CALL_RE = re.compile(r'Skill\s*\(\s*(?:skill:\s*)?["\']([^"\']+)["\']')

# Patterns to find Agent() calls with subagent_type
AGENT_TYPE_RE = re.compile(r'subagent_type:\s*["\']([^"\']+)["\']')

# @-import pattern (lines starting with @)
AT_IMPORT_RE = re.compile(r"^@(.+)$", re.MULTILINE)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=str(Path.home()),
                        help="Base directory (defaults to $HOME, override for testing)")
    parser.add_argument("--clash-threshold", type=float, default=0.35,
                        help="Cosine similarity threshold for trigger clash detection (default: 0.35)")
    parser.add_argument("--all-clashes", action="store_true",
                        help="Show all trigger clashes, including previously seen ones")
    return parser.parse_args()


def find_all_skill_names(base_dir: Path) -> set[str]:
    """Collect all available skill names from known locations."""
    names = set()
    claude_dir = base_dir / ".claude"

    # Global skills
    skills_dir = claude_dir / "skills"
    if skills_dir.exists():
        for d in skills_dir.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists() and "archive" not in d.parts:
                names.add(d.name)

    # Plugin skills
    plugins_dir = claude_dir / "plugins"
    if plugins_dir.exists():
        for plugin_root in plugins_dir.rglob("skills"):
            if plugin_root.is_dir() and "archive" not in plugin_root.parts:
                for d in plugin_root.iterdir():
                    if d.is_dir() and (d / "SKILL.md").exists():
                        names.add(d.name)

    return names


def find_all_agent_names(base_dir: Path) -> set[str]:
    """Collect all available agent names from known locations."""
    names = set()
    claude_dir = base_dir / ".claude"

    # Global agents (subdirectory format: name/AGENT.md)
    agents_dir = claude_dir / "agents"
    if agents_dir.exists():
        for d in agents_dir.iterdir():
            if d.is_dir() and (d / "AGENT.md").exists() and "archive" not in d.parts:
                names.add(d.name)
        # Flat file format: name.md directly in agents/
        for f in agents_dir.iterdir():
            if f.is_file() and f.suffix == ".md" and "archive" not in f.parts:
                names.add(f.stem)

    # Plugin agents
    plugins_dir = claude_dir / "plugins"
    if plugins_dir.exists():
        for plugin_root in plugins_dir.rglob("agents"):
            if plugin_root.is_dir():
                for d in plugin_root.iterdir():
                    if d.is_dir() and (d / "AGENT.md").exists():
                        names.add(d.name)

    return names


def check_broken_skill_refs(base_dir: Path, available_skills: set[str], findings: list[Finding]):
    """Find Skill() calls that reference non-existent skills."""
    claude_dir = base_dir / ".claude"

    # Search all SKILL.md files
    for skill_md in claude_dir.rglob("SKILL.md"):
        if "archive" in skill_md.parts:
            continue
        content = skill_md.read_text()
        for match in SKILL_CALL_RE.finditer(content):
            ref_name = match.group(1)
            # Handle colon-scoped names like "superpowers:brainstorming"
            base_name = ref_name.split(":")[-1] if ":" in ref_name else ref_name
            if base_name not in available_skills and ref_name not in available_skills:
                findings.append(Finding(
                    severity="error",
                    check="broken-skill-reference",
                    message=f"Skill() references non-existent skill '{ref_name}'",
                    path=str(skill_md),
                    action=f"Remove or update the reference to '{ref_name}'"
                ))


def check_broken_agent_refs(base_dir: Path, available_agents: set[str], findings: list[Finding]):
    """Find Agent() calls with subagent_type pointing at non-existent agents."""
    claude_dir = base_dir / ".claude"

    # Built-in agent types that don't need a definition file
    builtins = {"fork", "general-purpose"}

    for skill_md in claude_dir.rglob("SKILL.md"):
        if "archive" in skill_md.parts:
            continue
        content = skill_md.read_text()
        for match in AGENT_TYPE_RE.finditer(content):
            agent_name = match.group(1)
            if agent_name not in available_agents and agent_name not in builtins:
                findings.append(Finding(
                    severity="error",
                    check="broken-agent-reference",
                    message=f"Agent() references non-existent agent type '{agent_name}'",
                    path=str(skill_md),
                    action=f"Create agent definition at .claude/agents/{agent_name}/AGENT.md or fix the reference"
                ))


def check_dead_at_imports(base_dir: Path, findings: list[Finding], max_depth: int = 4):
    """Check @-imports in all CLAUDE.md files under .claude/, following
    chains of existing imports up to max_depth.

    Note: covers CLAUDE.md files under ~/.claude/ only; project-root
    CLAUDE.md files elsewhere on disk are out of scope for v2.0.
    """
    claude_dir = base_dir / ".claude"
    roots = [p for p in claude_dir.rglob("CLAUDE.md") if "archive" not in p.parts]

    visited: set[Path] = set()

    def scan_file(md_path: Path, depth: int):
        if depth > max_depth or md_path in visited:
            return
        visited.add(md_path)
        try:
            content = md_path.read_text()
        except (OSError, UnicodeDecodeError):
            return
        for match in AT_IMPORT_RE.finditer(content):
            import_path = match.group(1).strip()
            if import_path.startswith("~"):
                resolved = Path(import_path).expanduser()
            elif import_path.startswith("/"):
                resolved = Path(import_path)
            else:
                resolved = md_path.parent / import_path
            if not resolved.exists():
                findings.append(Finding(
                    severity="error",
                    check="dead-at-import",
                    message=f"@-import points at non-existent file: {import_path}",
                    path=str(md_path),
                    action=f"Remove the @{import_path} line or create the target file",
                ))
            elif resolved.suffix == ".md":
                scan_file(resolved, depth + 1)

    for root in roots:
        scan_file(root, 1)


def check_deprecated_duplicates(base_dir: Path, findings: list[Finding]):
    """Check for skills in archive that still have active counterparts."""
    claude_dir = base_dir / ".claude"
    archive_dir = claude_dir / "archive"
    skills_dir = claude_dir / "skills"

    if not archive_dir.exists() or not skills_dir.exists():
        return

    # Get active skill names
    active_skills = {d.name for d in skills_dir.iterdir() if d.is_dir()}

    # Check archive for counterparts
    for item in archive_dir.iterdir():
        if not item.is_dir():
            continue
        # Archive entries may have suffixes like "-pre-plugin" or "-v1"
        # Check if the base name matches an active skill
        name = item.name
        if name in active_skills:
            findings.append(Finding(
                severity="info",
                check="deprecated-duplicate",
                message=f"Archived skill '{name}' still has an active counterpart in skills/",
                path=str(item),
                action="Verify the active version is current; remove archive copy if superseded"
            ))


def check_model_effort_validity(base_dir: Path, findings: list[Finding]):
    """Check agent definitions for bare model aliases and invalid effort values."""
    claude_dir = base_dir / ".claude"
    agents_dir = claude_dir / "agents"

    if not agents_dir.exists():
        return

    for agent_dir in agents_dir.iterdir():
        if "archive" in agent_dir.parts:
            continue
        agent_md = agent_dir / "AGENT.md"
        if not agent_md.exists():
            continue

        content = agent_md.read_text()
        # Parse frontmatter (between --- markers)
        if not content.startswith("---"):
            continue
        try:
            end = content.index("---", 3)
        except ValueError:
            continue
        frontmatter = content[3:end]

        for line in frontmatter.split("\n"):
            line = line.strip()
            if line.startswith("model:"):
                model_val = line.split(":", 1)[1].strip().strip("'\"")
                if model_val and not MODEL_ID_PATTERN.match(model_val):
                    findings.append(Finding(
                        severity="warning",
                        check="invalid-model-id",
                        message=f"Agent uses bare model alias '{model_val}' instead of full ID",
                        path=str(agent_md),
                        action=f"Use full model ID (e.g., 'claude-opus-4-6' instead of '{model_val}')"
                    ))
            elif line.startswith("effort:"):
                effort_val = line.split(":", 1)[1].strip().strip("'\"")
                if effort_val and effort_val not in VALID_EFFORTS:
                    findings.append(Finding(
                        severity="warning",
                        check="invalid-effort",
                        message=f"Agent uses invalid effort level '{effort_val}'",
                        path=str(agent_md),
                        action=f"Use one of: {', '.join(sorted(VALID_EFFORTS))}"
                    ))


_ROUTING_TABLE_RE = re.compile(
    r"^\|\s*(?P<context>[^|]+)\s*\|\s*(?P<route_to>[^|]+)\s*\|\s*(?P<not_skill>[^|]+)\s*\|\s*(?P<why>[^|]+)\s*\|",
    re.MULTILINE,
)


def parse_routing_overrides(base_dir: Path) -> list[tuple[str, str]]:
    """Parse skill-routing.md and return list of (route_to, not_skill) pairs."""
    routing_md = base_dir / ".claude" / "rules" / "skill-routing.md"
    if not routing_md.exists():
        return []
    content = routing_md.read_text()
    pairs = []
    for match in _ROUTING_TABLE_RE.finditer(content):
        route_to = match.group("route_to").strip().lower()
        not_skill = match.group("not_skill").strip().lower()
        # Skip the header separator row
        if route_to.startswith("---") or not_skill.startswith("---"):
            continue
        # Strip parenthetical annotations: "brainstorming (after ideation)" → "brainstorming"
        route_to = re.sub(r"\s*\(.*?\)\s*$", "", route_to).strip()
        not_skill = re.sub(r"\s*\(.*?\)\s*$", "", not_skill).strip()
        pairs.append((route_to, not_skill))
    return pairs


def _is_managed(name_a: str, name_b: str, overrides: list[tuple[str, str]]) -> bool:
    """Check if a skill pair has a routing override (either ordering)."""
    a_low = name_a.lower()
    b_low = name_b.lower()
    # Also match partial scoped names: "brainstorming" matches "superpowers:brainstorming"
    for route_to, not_skill in overrides:
        candidates_a = {a_low, a_low.split(":")[-1]} if ":" in a_low else {a_low}
        candidates_b = {b_low, b_low.split(":")[-1]} if ":" in b_low else {b_low}
        # Check both orderings
        if (candidates_a & {route_to, route_to.split(":")[-1] if ":" in route_to else route_to}
                and candidates_b & {not_skill, not_skill.split(":")[-1] if ":" in not_skill else not_skill}):
            return True
        if (candidates_b & {route_to, route_to.split(":")[-1] if ":" in route_to else route_to}
                and candidates_a & {not_skill, not_skill.split(":")[-1] if ":" in not_skill else not_skill}):
            return True
    return False


def collect_skill_profiles(base_dir: Path) -> list[dict]:
    """Collect trigger profiles for all active skills.

    Returns list of dicts with keys: name, path, description, tokens.
    """
    claude_dir = base_dir / ".claude"
    profiles = []

    def scan_dir(skills_root: Path):
        if not skills_root.exists():
            return
        for skill_dir in skills_root.iterdir():
            if not skill_dir.is_dir() or "archive" in skill_dir.parts:
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            fm = parse_skill_frontmatter(skill_md.read_text())
            desc_parts = []
            if fm["description"]:
                desc_parts.append(fm["description"])
            if fm["whenToUse"]:
                desc_parts.append(fm["whenToUse"])
            trigger_text = " ".join(desc_parts)
            if not trigger_text.strip():
                continue
            profiles.append({
                "name": fm["name"] or skill_dir.name,
                "path": str(skill_md),
                "description": trigger_text,
                "tokens": tokenize(trigger_text),
            })

    # Global skills
    scan_dir(claude_dir / "skills")

    # Plugin skills — local plugins only (skip cache/ and marketplaces/)
    local_plugins = claude_dir / "plugins" / "local"
    if local_plugins.exists():
        for skills_root in local_plugins.rglob("skills"):
            if skills_root.is_dir() and "archive" not in skills_root.parts:
                scan_dir(skills_root)

    return profiles


def check_trigger_clashes(
    base_dir: Path, findings: list, threshold: float = 0.35, all_clashes: bool = False
) -> int:
    """Check for overlapping skill trigger descriptions.

    Returns the number of pairs checked.
    """
    profiles = collect_skill_profiles(base_dir)
    if len(profiles) < 2:
        return 0

    progress(f"  Comparing {len(profiles)} skill trigger profiles...")

    # Build TF-IDF vectors
    token_lists = [p["tokens"] for p in profiles]
    vectors = build_tfidf(token_lists)

    # Load routing overrides
    overrides = parse_routing_overrides(base_dir)

    # Collect clashing pairs first (before appending to findings)
    clashing_pairs = []
    pairs_checked = 0
    for i in range(len(profiles)):
        for j in range(i + 1, len(profiles)):
            pairs_checked += 1
            sim = cosine_similarity(vectors[i], vectors[j])
            if sim < threshold:
                continue

            name_a = profiles[i]["name"]
            name_b = profiles[j]["name"]
            shared = top_shared_terms(vectors[i], vectors[j], n=3)
            shared_str = ", ".join(shared) if shared else "none"
            path_str = f"{profiles[i]['path']} + {profiles[j]['path']}"
            managed = _is_managed(name_a, name_b, overrides)
            fingerprint = tuple(sorted([name_a, name_b]))

            clashing_pairs.append({
                "name_a": name_a,
                "name_b": name_b,
                "sim": sim,
                "shared_str": shared_str,
                "path_str": path_str,
                "managed": managed,
                "fingerprint": fingerprint,
            })

    # Build set of current fingerprints (all clashing pairs this run)
    current_fingerprints: set[tuple[str, str]] = {p["fingerprint"] for p in clashing_pairs}

    # Load previously seen fingerprints from state
    state = load_state()
    seen_raw = state.get("trigger_clashes", {}).get("seen", [])
    seen_fingerprints: set[tuple[str, str]] = {tuple(fp) for fp in seen_raw}

    # Emit findings
    known_count = 0
    for pair in clashing_pairs:
        fp = pair["fingerprint"]
        is_known = fp in seen_fingerprints

        if not all_clashes and is_known:
            known_count += 1
            continue

        if pair["managed"]:
            findings.append(Finding(
                severity="info",
                check="managed-trigger-clash",
                message=(
                    f"Skills '{pair['name_a']}' and '{pair['name_b']}' have overlapping triggers "
                    f"(similarity: {pair['sim']:.2f}, shared terms: {pair['shared_str']}) "
                    f"— routed in skill-routing.md"
                ),
                path=pair["path_str"],
                action=None,
            ))
        else:
            findings.append(Finding(
                severity="warning",
                check="unmanaged-trigger-clash",
                message=(
                    f"Skills '{pair['name_a']}' and '{pair['name_b']}' have overlapping triggers "
                    f"(similarity: {pair['sim']:.2f}, shared terms: {pair['shared_str']})"
                ),
                path=pair["path_str"],
                action="Add a routing override to ~/.claude/rules/skill-routing.md or differentiate the descriptions",
            ))

    if known_count > 0:
        findings.append(Finding(
            severity="info",
            check="suppressed-trigger-clashes",
            message=f"{known_count} previously-seen trigger clash(es) suppressed (use --all-clashes to show)",
            path=None,
            action=None,
        ))

    # Save the full current set of fingerprints as the new baseline
    state["trigger_clashes"] = {
        "seen": [list(fp) for fp in current_fingerprints]
    }
    save_state(state)

    return pairs_checked


def main():
    args = parse_args()
    base_dir = Path(args.base_dir)
    findings: list[Finding] = []
    checks_run = 0

    progress("Collecting available skills...")
    available_skills = find_all_skill_names(base_dir)
    progress(f"  Found {len(available_skills)} skills")

    progress("Collecting available agents...")
    available_agents = find_all_agent_names(base_dir)
    progress(f"  Found {len(available_agents)} agents")

    progress("Checking Skill() references...")
    check_broken_skill_refs(base_dir, available_skills, findings)
    checks_run += 1

    progress("Checking Agent() references...")
    check_broken_agent_refs(base_dir, available_agents, findings)
    checks_run += 1

    progress("Checking @-imports...")
    check_dead_at_imports(base_dir, findings)
    checks_run += 1

    progress("Checking model/effort validity...")
    check_model_effort_validity(base_dir, findings)
    checks_run += 1

    progress("Checking for deprecated duplicates...")
    check_deprecated_duplicates(base_dir, findings)
    checks_run += 1

    progress("Checking trigger clashes...")
    pairs_checked = check_trigger_clashes(base_dir, findings, threshold=args.clash_threshold, all_clashes=args.all_clashes)
    checks_run += 1

    report = AuditReport(
        domain="assets",
        findings=findings,
        meta={
            "checks_run": checks_run,
            "skills_found": len(available_skills),
            "agents_found": len(available_agents),
            "trigger_clashes_checked": pairs_checked,
        }
    )
    report.emit()


if __name__ == "__main__":
    main()
