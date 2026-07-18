"""
Shared schema for cc-health scanner output.

All scanners produce an AuditReport as JSON to stdout.
"""

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# lib/schema.py lives at <plugin-root>/scripts/lib/schema.py
PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = PLUGIN_ROOT / "state" / ".cc-health-state.json"


@dataclass
class Finding:
    severity: str  # "error" | "warning" | "info"
    check: str  # kebab-case identifier for the check that fired
    message: str  # human-readable description of the finding
    path: str | None = None  # file/directory the finding relates to
    action: str | None = None  # suggested fix

    def __post_init__(self):
        valid = ("error", "warning", "info")
        if self.severity not in valid:
            raise ValueError(f"severity must be one of {valid}, got {self.severity!r}")


@dataclass
class AuditReport:
    domain: str
    findings: list[Finding] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    def emit(self):
        """Print report JSON to stdout."""
        print(self.to_json())


def to_json(report: AuditReport) -> str:
    """Module-level wrapper for AuditReport.to_json()."""
    return report.to_json()


def progress(msg: str):
    """Print progress message to stderr (not captured in JSON output)."""
    print(msg, file=sys.stderr)


def load_state() -> dict:
    """Load the state file. Returns empty dict if missing or corrupt."""
    try:
        return json.loads(STATE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state: dict):
    """Write state file atomically."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.rename(STATE_FILE)
