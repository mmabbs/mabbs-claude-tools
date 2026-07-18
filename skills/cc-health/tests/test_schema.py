"""Tests for the shared schema module."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.schema import AuditReport, Finding


def test_finding_valid_severities():
    f = Finding(severity="error", check="test-check", message="test")
    assert f.severity == "error"

    f = Finding(severity="warning", check="test-check", message="test")
    assert f.severity == "warning"

    f = Finding(severity="info", check="test-check", message="test")
    assert f.severity == "info"


def test_finding_invalid_severity_raises():
    import pytest
    with pytest.raises(ValueError, match="severity must be one of"):
        Finding(severity="critical", check="test", message="test")


def test_report_to_json_structure():
    report = AuditReport(
        domain="config",
        findings=[
            Finding(
                severity="warning",
                check="orphaned-entry",
                message="Project entry points to deleted directory",
                path="~/.claude.json",
                action="Remove the entry"
            )
        ],
        meta={"files_scanned": 1, "checks_run": 1}
    )
    data = json.loads(report.to_json())
    assert data["domain"] == "config"
    assert len(data["findings"]) == 1
    assert data["findings"][0]["severity"] == "warning"
    assert data["findings"][0]["check"] == "orphaned-entry"
    assert "timestamp" in data
    assert data["meta"]["files_scanned"] == 1


def test_report_empty_findings():
    report = AuditReport(domain="temp", findings=[], meta={"checks_run": 4})
    data = json.loads(report.to_json())
    assert data["findings"] == []
    assert data["domain"] == "temp"
