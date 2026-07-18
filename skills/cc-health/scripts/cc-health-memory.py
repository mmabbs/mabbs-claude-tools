#!/usr/bin/env python3
"""
cc-health memory domain — validates MEMORY.md entries for stale references.

Checks:
1. Dead file references — paths named in memory that no longer exist
2. Stale "as of" entries — date-stamped entries older than 60 days

Empty-state handling: if no MEMORY.md files are found, reports info severity
"memory may be disabled" rather than a false clean bill of health.

Usage:
    python3 cc-health-memory.py [--base-dir PATH] [--stale-days N]

Outputs AuditReport JSON to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.schema import AuditReport, Finding, progress

# Pattern to match file paths in memory entries
# Matches: ~/..., ~/.claude/..., /Users/..., relative paths with /
PATH_PATTERN = re.compile(r"(~/?[\w./-]+|/Users/[\w./-]+|\.claude/[\w./-]+)")

# Pattern to match "as of YYYY-MM-DD" or "(as of YYYY-MM-DD)" or "since YYYY-MM-DD"
DATE_PATTERN = re.compile(r"(?:as of|since)\s+(\d{4}-\d{2}-\d{2})", re.IGNORECASE)

# Pattern to match version references like "since v2.1.150" or "as of v2.1.x"
VERSION_DATE_PATTERN = re.compile(r"(?:as of|since)\s+v?(\d+\.\d+\.\d+)", re.IGNORECASE)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=str(Path.home()),
                        help="Base directory (defaults to $HOME, override for testing)")
    parser.add_argument("--stale-days", type=int, default=60,
                        help="Days before an 'as of' entry is considered stale (default: 60)")
    return parser.parse_args()


def expand_path(path_str: str, base_dir: Path) -> Path:
    """Expand ~ and resolve a path string relative to base_dir."""
    if path_str.startswith("~/"):
        return base_dir / path_str[2:]
    elif path_str.startswith("~"):
        return base_dir / path_str[1:]
    elif path_str.startswith("/"):
        return Path(path_str)
    else:
        return base_dir / path_str


def find_memory_files(base_dir: Path) -> list[Path]:
    """Find all MEMORY.md files in ~/.claude/projects/*/memory/."""
    claude_dir = base_dir / ".claude"
    projects_dir = claude_dir / "projects"
    memory_files = []

    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                memory_file = project_dir / "memory" / "MEMORY.md"
                if memory_file.exists():
                    memory_files.append(memory_file)

    return memory_files


def check_dead_file_refs(memory_file: Path, base_dir: Path, findings: list[Finding]):
    """Check for path references in memory that don't exist on disk."""
    content = memory_file.read_text()

    for line in content.split("\n"):
        for match in PATH_PATTERN.finditer(line):
            path_str = match.group(1)
            expanded = expand_path(path_str, base_dir)

            if str(expanded).endswith("/"):
                continue  # generic pattern, not a specific reference
            if not expanded.exists():
                findings.append(Finding(
                    severity="warning",
                    check="dead-file-reference",
                    message=f"Memory references non-existent path: {path_str}",
                    path=str(memory_file),
                    action=f"Update or remove the memory entry referencing '{path_str}'",
                ))


def check_stale_dates(memory_file: Path, stale_days: int, findings: list[Finding]):
    """Check for 'as of' or 'since' date entries older than threshold."""
    content = memory_file.read_text()
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(days=stale_days)

    for line in content.split("\n"):
        for match in DATE_PATTERN.finditer(line):
            date_str = match.group(1)
            try:
                entry_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if entry_date < threshold:
                    findings.append(Finding(
                        severity="info",
                        check="stale-as-of-entry",
                        message=f"Entry dated '{date_str}' is over {stale_days} days old — may need re-verification",
                        path=str(memory_file),
                        action=f"Verify this entry is still accurate: {line.strip()[:100]}"
                    ))
            except ValueError:
                pass


def main():
    args = parse_args()
    base_dir = Path(args.base_dir)
    findings: list[Finding] = []
    checks_run = 0

    progress("Finding MEMORY.md files...")
    memory_files = find_memory_files(base_dir)

    if not memory_files:
        findings.append(Finding(
            severity="info",
            check="memory-possibly-disabled",
            message="No memory entries found — memory may be disabled. If intentional, ignore this finding.",
            path=str(base_dir / ".claude" / "projects"),
            action=None
        ))
        report = AuditReport(domain="memory", findings=findings, meta={"memory_files_found": 0, "checks_run": 0})
        report.emit()
        return

    progress(f"  Found {len(memory_files)} MEMORY.md file(s)")

    progress("Checking for dead file references...")
    for mf in memory_files:
        check_dead_file_refs(mf, base_dir, findings)
    checks_run += 1

    progress("Checking for stale date entries...")
    for mf in memory_files:
        check_stale_dates(mf, args.stale_days, findings)
    checks_run += 1

    report = AuditReport(
        domain="memory",
        findings=findings,
        meta={
            "memory_files_found": len(memory_files),
            "checks_run": checks_run,
        }
    )
    report.emit()


if __name__ == "__main__":
    main()
