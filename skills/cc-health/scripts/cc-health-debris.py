#!/usr/bin/env python3
"""
cc-health debris domain — finds loose ends and broken references.

Checks:
1. Orphaned agent directories — never referenced by any active file
2. Leftover TODO/FIXME/HACK/XXX markers in config files

Usage:
    python3 cc-health-debris.py [--base-dir PATH]

Outputs AuditReport JSON to stdout.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.schema import AuditReport, Finding, progress

# Marker patterns
MARKER_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)

# Files to scan for markers (relative to .claude/)
MARKER_SCAN_DIRS = ["rules", "skills", "agents"]
MARKER_SCAN_FILES = ["CLAUDE.md", "AGENTS.md"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=str(Path.home()),
                        help="Base directory (defaults to $HOME, override for testing)")
    return parser.parse_args()


def check_orphaned_directories(claude_dir: Path, findings: list[Finding]):
    """Find agent directories that are never referenced by any file outside themselves."""

    for subdir_name in ("agents",):  # skills are user/description-triggered;
                                      # unreferenced is their normal state
        target_dir = claude_dir / subdir_name
        if not target_dir.exists():
            continue

        for item_dir in target_dir.iterdir():
            if not item_dir.is_dir():
                continue

            dir_name = item_dir.name

            # Check if this name appears in any file outside its own directory
            referenced_externally = False
            for md_file in claude_dir.rglob("*.md"):
                if "archive" in md_file.parts:
                    continue
                # Skip files inside this directory itself
                try:
                    md_file.relative_to(item_dir)
                    continue  # File is inside the directory — skip
                except ValueError:
                    pass  # File is outside — check it

                try:
                    content = md_file.read_text()
                except (OSError, UnicodeDecodeError):
                    continue

                if dir_name in content:
                    referenced_externally = True
                    break

            if not referenced_externally:
                findings.append(Finding(
                    severity="warning",
                    check="orphaned-directory",
                    message=f"{subdir_name.rstrip('s').title()} '{dir_name}' is never referenced by any file outside itself",
                    path=str(item_dir),
                    action=f"Archive to ~/.claude/archive/{dir_name}/ if no longer needed"
                ))


def check_leftover_markers(claude_dir: Path, findings: list[Finding]):
    """Find TODO/FIXME/HACK/XXX markers in config files."""
    scan_paths = []

    for dirname in MARKER_SCAN_DIRS:
        dirpath = claude_dir / dirname
        if dirpath.exists():
            scan_paths.extend(dirpath.rglob("*.md"))

    for filename in MARKER_SCAN_FILES:
        filepath = claude_dir / filename
        if filepath.exists():
            scan_paths.append(filepath)

    for filepath in scan_paths:
        # Skip archive and the cc-health plugin's own files (avoids self-flagging)
        if "archive" in filepath.parts:
            continue
        if "cc-health" in filepath.parts and "plugins" in filepath.parts:
            continue
        try:
            content = filepath.read_text()
        except (OSError, UnicodeDecodeError):
            continue

        for i, line in enumerate(content.split("\n"), 1):
            match = MARKER_RE.search(line)
            if match:
                marker = match.group(1).upper()
                context = line.strip()[:100]
                findings.append(Finding(
                    severity="info",
                    check="leftover-marker",
                    message=f"{marker} marker at line {i}: {context}",
                    path=str(filepath),
                    action=f"Resolve or remove the {marker} marker"
                ))


def main():
    args = parse_args()
    base_dir = Path(args.base_dir)
    claude_dir = base_dir / ".claude"
    findings: list[Finding] = []
    checks_run = 0

    if not claude_dir.exists():
        report = AuditReport(domain="debris", findings=[], meta={"checks_run": 0})
        report.emit()
        return

    progress("Checking for orphaned directories...")
    check_orphaned_directories(claude_dir, findings)
    checks_run += 1

    progress("Checking for leftover markers...")
    check_leftover_markers(claude_dir, findings)
    checks_run += 1

    report = AuditReport(
        domain="debris",
        findings=findings,
        meta={"checks_run": checks_run}
    )
    report.emit()


if __name__ == "__main__":
    main()
