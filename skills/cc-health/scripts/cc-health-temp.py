#!/usr/bin/env python3
"""
cc-health temp domain — finds scratch files and artifact droppings.

Checks:
1. Scratch directories — /tmp/claude-* and ~/tmp/ files older than 7 days
2. Artifact droppings — response.md, *.bak, *.tmp in project roots
3. Stale context files — context_state_*.json in ~/.claude/ older than 30 days

Usage:
    python3 cc-health-temp.py [--base-dir PATH] [--max-age-days N]

Outputs AuditReport JSON to stdout.
"""

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.schema import AuditReport, Finding, progress

SCRATCH_AGE_DAYS = 7
CONTEXT_AGE_DAYS = 30

ARTIFACT_PATTERNS = ["response.md", "*.bak", "*.tmp"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-dir",
        default=str(Path.home()),
        help="Base directory (defaults to $HOME, override for testing)",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=SCRATCH_AGE_DAYS,
        help="Days before scratch files are flagged (default: 7)",
    )
    return parser.parse_args()


def file_age_days(path: Path) -> float:
    """Return file age in days based on mtime."""
    try:
        return (time.time() - path.stat().st_mtime) / 86400
    except OSError:
        return 0


def check_scratch_dirs(tmp_dirs: list[Path], max_age: int, findings: list[Finding]):
    """Check scratch directories for old files."""
    for tmp_dir in tmp_dirs:
        if not tmp_dir.exists():
            continue
        for item in tmp_dir.iterdir():
            if not item.name.startswith("claude-"):
                continue
            if item.is_dir():
                for f in item.rglob("*"):
                    if f.is_file() and file_age_days(f) > max_age:
                        findings.append(
                            Finding(
                                severity="info",
                                check="old-scratch-file",
                                message=f"Scratch file older than {max_age} days: {f.name}",
                                path=str(f),
                                action="Delete if no longer needed",
                            )
                        )
            elif item.is_file() and file_age_days(item) > max_age:
                findings.append(
                    Finding(
                        severity="info",
                        check="old-scratch-file",
                        message=f"Scratch file older than {max_age} days",
                        path=str(item),
                        action="Delete if no longer needed",
                    )
                )


def check_artifact_droppings(base_dir: Path, findings: list[Finding]):
    """Check for artifact droppings in the base directory and .claude/."""
    search_dirs = [base_dir]
    claude_dir = base_dir / ".claude"
    if claude_dir.exists():
        search_dirs.append(claude_dir)

    for search_dir in search_dirs:
        for pattern in ARTIFACT_PATTERNS:
            for match in search_dir.glob(pattern):
                if match.is_file():
                    findings.append(
                        Finding(
                            severity="info",
                            check="artifact-dropping",
                            message=f"Artifact dropping: {match.name}",
                            path=str(match),
                            action="Delete if no longer needed",
                        )
                    )


def check_stale_context_files(claude_dir: Path, findings: list[Finding]):
    """Check for old context_state_*.json files."""
    if not claude_dir.exists():
        return

    for f in claude_dir.glob("context_state_*.json"):
        if f.is_file() and file_age_days(f) > CONTEXT_AGE_DAYS:
            age = int(file_age_days(f))
            findings.append(
                Finding(
                    severity="info",
                    check="stale-context-file",
                    message=f"Context state file is {age} days old",
                    path=str(f),
                    action="Safe to delete — leftover from an old session",
                )
            )


def main():
    args = parse_args()
    base_dir = Path(args.base_dir)
    claude_dir = base_dir / ".claude"
    findings: list[Finding] = []
    checks_run = 0

    # Determine tmp directories to scan.
    # CC_HEALTH_TMP_DIRS overrides the default for test isolation.
    tmp_dirs_env = os.environ.get("CC_HEALTH_TMP_DIRS")
    if tmp_dirs_env:
        tmp_dirs = [Path(p) for p in tmp_dirs_env.split(":") if p]
    else:
        tmp_dirs = [Path("/tmp"), base_dir / "tmp"]

    progress("Checking scratch directories...")
    check_scratch_dirs(tmp_dirs, args.max_age_days, findings)
    checks_run += 1

    progress("Checking for artifact droppings...")
    check_artifact_droppings(base_dir, findings)
    checks_run += 1

    progress("Checking stale context files...")
    check_stale_context_files(claude_dir, findings)
    checks_run += 1

    report = AuditReport(
        domain="temp",
        findings=findings,
        meta={"checks_run": checks_run},
    )
    report.emit()


if __name__ == "__main__":
    main()
