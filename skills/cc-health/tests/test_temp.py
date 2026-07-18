"""Tests for cc-health-temp scanner."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "cc-health-temp.py"


def run_scanner(base_dir: str, tmp_dirs: str = "") -> dict:
    env = os.environ.copy()
    # Always isolate: default to a guaranteed-empty dir inside base_dir
    env["CC_HEALTH_TMP_DIRS"] = tmp_dirs or str(Path(base_dir) / "isolated-tmp")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--base-dir", base_dir, "--max-age-days", "0"],
        capture_output=True, text=True, env=env
    )
    assert result.returncode == 0, f"Scanner failed: {result.stderr}"
    return json.loads(result.stdout)


def test_old_scratch_files(tmp_path):
    """Scratch files in tmp dirs are flagged."""
    scratch_dir = tmp_path / "tmp" / "claude-501"
    scratch_dir.mkdir(parents=True)
    scratch_file = scratch_dir / "output.txt"
    scratch_file.write_text("scratch data")
    # Set mtime to 8 days ago
    old_time = time.time() - (8 * 86400)
    os.utime(scratch_file, (old_time, old_time))

    report = run_scanner(str(tmp_path), tmp_dirs=str(tmp_path / "tmp"))
    checks = [f["check"] for f in report["findings"]]
    assert "old-scratch-file" in checks


def test_artifact_droppings(tmp_path):
    """response.md and .bak files in project roots are flagged."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    (tmp_path / "response.md").write_text("Some copied output")
    (tmp_path / "backup.bak").write_text("old backup")

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "artifact-dropping" in checks


def test_stale_context_files(tmp_path):
    """context_state_*.json files older than 30 days are flagged."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    stale_file = claude_dir / "context_state_abc123.json"
    stale_file.write_text("{}")
    old_time = time.time() - (31 * 86400)
    os.utime(stale_file, (old_time, old_time))

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "stale-context-file" in checks


def test_clean_setup_no_findings(tmp_path):
    """A clean directory produces no findings."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    report = run_scanner(str(tmp_path))
    assert report["findings"] == []
