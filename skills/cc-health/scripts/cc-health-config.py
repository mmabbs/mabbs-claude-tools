#!/usr/bin/env python3
"""
cc-health config domain — checks Claude Code configuration for scope/hygiene issues.

Checks:
1. MCP scope mismatches (local-scoped servers keyed to non-existent dirs)
2. Orphaned project entries in .claude.json
3. Duplicate permissions across settings.json and settings.local.json
4. Empty/stale .mcp.json files
5. Stale env vars (known-removed vars still set)

Usage:
    python3 cc-health-config.py [--base-dir PATH]

Outputs AuditReport JSON to stdout.
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.schema import AuditReport, Finding, progress

# Env vars known to be removed in recent CC versions.
# Manually maintained — no automated sync from the version domain.
REMOVED_ENV_VARS = [
    "CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE",
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=str(Path.home()),
                        help="Base directory (defaults to $HOME, override for testing)")
    return parser.parse_args()


# Characters that Claude Code's project-path encoding collapses into "-".
# Cross-check against references/path-encoding.md and the decoder in the
# existing ~/.claude/scripts/cc-health.py before finalizing; extend if either
# documents additional collapsed characters.
LOSSY_CHARS = ("/", ".", "-", "_", " ")


def _resolve_dfs(tokens: list[str], idx: int, current: Path) -> "Path | None":
    """DFS: find a real path under `current` that consumes tokens[idx:].

    At each step, tries consuming tokens[idx..j] as a single filesystem entry
    name (joined with each non-slash lossy character). Filesystem existence
    prunes the search tree — the fan-out is bounded by what actually exists.
    """
    if idx == len(tokens):
        return current if current.exists() else None

    for j in range(idx, len(tokens)):
        if j == idx:
            # Single token: the name is exactly the token
            name = tokens[j]
            if not name:
                continue
            cand = current / name
            if cand.exists():
                result = _resolve_dfs(tokens, j + 1, cand)
                if result is not None:
                    return result
        else:
            # Multiple tokens: try joining idx..j with each non-slash lossy char
            segment = tokens[idx : j + 1]
            for ch in LOSSY_CHARS:
                if ch == "/":
                    continue
                name = ch.join(segment)
                if not name:
                    continue
                cand = current / name
                if cand.exists():
                    result = _resolve_dfs(tokens, j + 1, cand)
                    if result is not None:
                        return result

    return None


def resolve_encoded_path(encoded: str, root: Path = Path("/")) -> "Path | None":
    """Resolve a lossy hyphen-encoded project path against the real filesystem.

    Returns an existing Path that encodes to `encoded`, or None if no such
    path exists (the genuine orphan case). Candidates are bounded by real
    directory existence, so the search cannot explode.

    Uses DFS to handle multi-hyphen directory names (e.g. `pytest-of-jdoe`)
    that the naive single-token algorithm cannot resolve.
    """
    if not encoded.startswith("-"):
        return None
    tokens = encoded[1:].split("-")
    return _resolve_dfs(tokens, 0, root)


def check_orphaned_projects(claude_json_path: Path, findings: list[Finding], root: Path = Path("/")):
    """Check for project entries pointing at directories that no longer exist."""
    if not claude_json_path.exists():
        return

    try:
        data = json.loads(claude_json_path.read_text())
    except (json.JSONDecodeError, OSError):
        return

    projects = data.get("projects", {})
    for encoded_path in projects:
        if not encoded_path.startswith("-"):
            continue

        resolved = resolve_encoded_path(encoded_path, root)
        if resolved is None:
            findings.append(Finding(
                severity="warning",
                check="orphaned-project-entry",
                message=f"Project entry points to non-existent directory: {encoded_path}",
                path=str(claude_json_path),
                action="Remove the entry from .claude.json projects block"
            ))


def check_mcp_scope(claude_json_path: Path, findings: list[Finding], root: Path = Path("/")):
    """Check for local-scoped MCP servers keyed to non-existent directories."""
    if not claude_json_path.exists():
        return

    try:
        data = json.loads(claude_json_path.read_text())
    except (json.JSONDecodeError, OSError):
        return

    projects = data.get("projects", {})
    for encoded_path, project_data in projects.items():
        if not isinstance(project_data, dict):
            continue
        mcp_servers = project_data.get("mcpServers", {})
        if not mcp_servers:
            continue

        if not encoded_path.startswith("-"):
            continue

        resolved = resolve_encoded_path(encoded_path, root)
        if resolved is None:
            for server_name in mcp_servers:
                findings.append(Finding(
                    severity="warning",
                    check="mcp-scope-mismatch",
                    message=f"MCP server '{server_name}' is local-scoped to non-existent directory: {encoded_path}",
                    path=str(claude_json_path),
                    action="Remove the server entry or re-scope to 'user'"
                ))


def check_duplicate_permissions(claude_dir: Path, findings: list[Finding]):
    """Check for identical permission entries in settings.json and settings.local.json."""
    settings_path = claude_dir / "settings.json"
    local_path = claude_dir / "settings.local.json"

    if not settings_path.exists() or not local_path.exists():
        return

    try:
        settings = json.loads(settings_path.read_text())
        local = json.loads(local_path.read_text())
    except (json.JSONDecodeError, OSError):
        return

    settings_perms = settings.get("permissions", {}).get("allow", [])
    local_perms = local.get("permissions", {}).get("allow", [])

    # Normalize for comparison
    settings_set = {json.dumps(p, sort_keys=True) for p in settings_perms}
    local_set = {json.dumps(p, sort_keys=True) for p in local_perms}

    duplicates = settings_set & local_set
    for dup in duplicates:
        perm = json.loads(dup)
        if isinstance(perm, str):
            desc = perm
        else:
            desc = perm.get("tool", perm.get("permission", str(perm)))
        findings.append(Finding(
            severity="info",
            check="duplicate-permission",
            message=f"Permission '{desc}' appears in both settings.json and settings.local.json",
            path=str(claude_dir),
            action="Remove from one file (settings.local.json takes priority)"
        ))


# Directories to prune from the .mcp.json walk — avoid network mounts,
# large OS directories, and package trees that will never contain CC configs.
_MCP_PRUNE_DIRS = frozenset({
    "Library",       # macOS: app data, caches, CloudStorage (network mounts)
    "node_modules",  # JS dependency trees
    "plugins",       # CC-internal: ~/.claude/plugins/ contains CC-managed .mcp.json stubs
    ".Trash",
    ".git",
    ".hg",
    ".svn",
    "venv",
    ".venv",
    "__pycache__",
})


def _walk_for_mcp(root: Path):
    """Yield .mcp.json paths under root, pruning problem directories."""
    try:
        entries = list(root.iterdir())
    except (PermissionError, OSError, TimeoutError):
        return

    for entry in entries:
        try:
            if entry.is_file() and entry.name == ".mcp.json":
                yield entry
            elif entry.is_dir():
                name = entry.name
                # Skip hidden dirs (except .claude) and known-problem dirs
                if name.startswith(".") and name != ".claude":
                    continue
                if name in _MCP_PRUNE_DIRS:
                    continue
                yield from _walk_for_mcp(entry)
        except (PermissionError, OSError, TimeoutError):
            continue


def check_empty_mcp_json(base_dir: Path, findings: list[Finding]):
    """Find .mcp.json files that are empty or have no servers."""
    for mcp_file in _walk_for_mcp(base_dir):
        try:
            content = mcp_file.read_text().strip()
            if not content or content == "{}":
                findings.append(Finding(
                    severity="info",
                    check="empty-mcp-json",
                    message="Empty .mcp.json file",
                    path=str(mcp_file),
                    action="Remove if not needed, or add server configuration"
                ))
                continue

            data = json.loads(content)
            servers = data.get("mcpServers", {})
            if not servers:
                findings.append(Finding(
                    severity="info",
                    check="empty-mcp-json",
                    message=".mcp.json has no servers defined",
                    path=str(mcp_file),
                    action="Remove if not needed"
                ))
        except (json.JSONDecodeError, OSError):
            findings.append(Finding(
                severity="warning",
                check="malformed-mcp-json",
                message=".mcp.json contains invalid JSON",
                path=str(mcp_file),
                action="Fix or remove the file"
            ))


def check_stale_env_vars(claude_dir: Path, findings: list[Finding]):
    """Check for env vars in settings that CC no longer recognizes."""
    settings_path = claude_dir / "settings.json"
    local_path = claude_dir / "settings.local.json"

    for path in (settings_path, local_path):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        env_block = data.get("env", {})
        for var_name in env_block:
            if var_name in REMOVED_ENV_VARS:
                findings.append(Finding(
                    severity="warning",
                    check="stale-env-var",
                    message=f"Env var '{var_name}' was removed in a recent CC version (now a no-op)",
                    path=str(path),
                    action=f"Remove '{var_name}' from the env block"
                ))


def main():
    args = parse_args()
    base_dir = Path(args.base_dir)
    claude_dir = base_dir / ".claude"
    claude_json = base_dir / ".claude.json"

    findings: list[Finding] = []
    checks_run = 0

    progress("Checking orphaned project entries...")
    check_orphaned_projects(claude_json, findings)
    checks_run += 1

    progress("Checking MCP scope...")
    check_mcp_scope(claude_json, findings)
    checks_run += 1

    progress("Checking duplicate permissions...")
    check_duplicate_permissions(claude_dir, findings)
    checks_run += 1

    progress("Checking .mcp.json files...")
    check_empty_mcp_json(base_dir, findings)
    checks_run += 1

    progress("Checking stale env vars...")
    check_stale_env_vars(claude_dir, findings)
    checks_run += 1

    report = AuditReport(
        domain="config",
        findings=findings,
        meta={"checks_run": checks_run}
    )
    report.emit()


if __name__ == "__main__":
    main()
