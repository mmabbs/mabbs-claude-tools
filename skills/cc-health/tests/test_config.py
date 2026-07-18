"""Tests for cc-health-config scanner."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "cc-health-config.py"


def run_scanner(base_dir: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--base-dir", base_dir],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Scanner failed: {result.stderr}"
    return json.loads(result.stdout)


def test_orphaned_project_entries(tmp_path):
    """Project entries pointing at non-existent directories are flagged."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    # Create a claude.json with a project entry for a non-existent path
    claude_json = tmp_path / ".claude.json"
    claude_json.write_text(json.dumps({
        "projects": {
            "-Users-jdoe-Documents-deleted-project": {
                "allowedTools": []
            }
        }
    }))

    report = run_scanner(str(tmp_path))
    assert report["domain"] == "config"
    checks = [f["check"] for f in report["findings"]]
    assert "orphaned-project-entry" in checks


def test_hyphenated_directory_not_flagged(tmp_path):
    """Directories with hyphens in the name must not be falsely flagged as orphaned."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    # Create a real directory with hyphens
    real_dir = tmp_path / "my-vault"
    real_dir.mkdir()

    # Encode it as CC would: /tmp_path/my-vault -> -<tmp_path>-my-vault
    encoded = str(tmp_path / "my-vault").replace("/", "-")

    claude_json = tmp_path / ".claude.json"
    claude_json.write_text(json.dumps({
        "projects": {encoded: {"allowedTools": []}}
    }))

    report = run_scanner(str(tmp_path))
    orphan_findings = [f for f in report["findings"] if f["check"] == "orphaned-project-entry"]
    assert orphan_findings == [], f"False positive: {orphan_findings}"


def test_duplicate_permissions(tmp_path):
    """Identical permissions in settings.json and settings.local.json are flagged."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    claude_json = tmp_path / ".claude.json"
    claude_json.write_text("{}")

    perm = "Bash(git:*)"
    settings = claude_dir / "settings.json"
    settings.write_text(json.dumps({"permissions": {"allow": [perm]}}))

    local_settings = claude_dir / "settings.local.json"
    local_settings.write_text(json.dumps({"permissions": {"allow": [perm]}}))

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "duplicate-permission" in checks


def test_empty_mcp_json(tmp_path):
    """Empty .mcp.json files are flagged."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    claude_json = tmp_path / ".claude.json"
    claude_json.write_text("{}")

    project_dir = tmp_path / "project" / ".claude"
    project_dir.mkdir(parents=True)
    mcp_file = tmp_path / "project" / ".mcp.json"
    mcp_file.write_text("{}")

    report = run_scanner(str(tmp_path))
    checks = [f["check"] for f in report["findings"]]
    assert "empty-mcp-json" in checks


def test_clean_config_no_findings(tmp_path):
    """A minimal clean config produces no findings."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    claude_json = tmp_path / ".claude.json"
    claude_json.write_text("{}")

    settings = claude_dir / "settings.json"
    settings.write_text(json.dumps({"permissions": {"allow": []}}))

    report = run_scanner(str(tmp_path))
    assert report["findings"] == []
