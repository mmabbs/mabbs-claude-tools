"""Tests for cc-health-memory scanner."""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "cc-health-memory.py"


def run_scanner(base_dir: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--base-dir", base_dir],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Scanner failed: {result.stderr}"
    return json.loads(result.stdout)


def test_empty_state_flags_info(tmp_path):
    """When no MEMORY.md files exist, report info about possible disabled memory."""
    claude_dir = tmp_path / ".claude"
    projects_dir = claude_dir / "projects"
    projects_dir.mkdir(parents=True)

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "memory-possibly-disabled" in checks
    assert report["findings"][0]["severity"] == "info"


def test_dead_file_reference(tmp_path):
    """Memory entries referencing non-existent paths are flagged."""
    claude_dir = tmp_path / ".claude"
    memory_dir = claude_dir / "projects" / "-test-project" / "memory"
    memory_dir.mkdir(parents=True)

    memory_md = memory_dir / "MEMORY.md"
    memory_md.write_text(
        "- Config file at ~/.claude/skills/deleted-skill/SKILL.md needs updating\n"
        "- The user prefers short responses\n"
    )

    # Create .claude dir but NOT the referenced skill
    (tmp_path / ".claude" / "skills").mkdir(parents=True)

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "dead-file-reference" in checks


def test_stale_as_of_entry(tmp_path):
    """Entries with old 'as of' dates are flagged."""
    claude_dir = tmp_path / ".claude"
    memory_dir = claude_dir / "projects" / "-test-project" / "memory"
    memory_dir.mkdir(parents=True)

    memory_md = memory_dir / "MEMORY.md"
    memory_md.write_text(
        "- The API key format changed (as of 2025-01-15)\n"
        "- User prefers dark mode\n"
    )

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "stale-as-of-entry" in checks


def test_clean_memory_no_findings(tmp_path):
    """Valid memory entries produce no findings."""
    claude_dir = tmp_path / ".claude"
    memory_dir = claude_dir / "projects" / "-test-project" / "memory"
    memory_dir.mkdir(parents=True)
    (tmp_path / ".claude" / "settings.json").write_text("{}")

    memory_md = memory_dir / "MEMORY.md"
    memory_md.write_text("- User prefers concise responses\n- Project uses Python 3.12\n")

    report = run_scanner(str(tmp_path))
    # Should not flag anything (no paths, no stale dates, memory exists)
    findings_without_info = [f for f in report["findings"] if f["severity"] != "info"]
    assert findings_without_info == []
