#!/usr/bin/env python3
"""
cc-health-chats.py - Claude Code conversation and disk audit helper (chats domain)

Usage:
    python3 cc-health-chats.py scan [--project PATH] [--exact] [--filter-command /exit,/clear] [--empty-only]
    python3 cc-health-chats.py clean [--project PATH] [--exact] [--filter-command /exit,/clear] [--empty-only] [--confirm]
    python3 cc-health-chats.py usage
    python3 cc-health-chats.py global
    python3 cc-health-chats.py orphans

Outputs JSON to stdout, progress to stderr.

--empty-only: Filter to conversations with no substantive content (real_user_messages == 0 AND real_assistant_messages == 0).
              This catches sessions like /ide -> cancelled -> /exit without needing to specify commands.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pathlib import Path as _Path
import sys as _sys
_sys.path.insert(0, str(_Path(__file__).parent))
from lib.schema import progress

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"

# Protection: skip files modified within this many seconds
ACTIVE_SESSION_THRESHOLD = 3600  # 1 hour


def decode_project_path(encoded: str) -> str:
    """Convert encoded path like '-Users-jdoe-Documents' to '/Users/jdoe/Documents'.

    Note: The encoding is lossy. Hyphens in folder names become indistinguishable
    from path separators. This function makes a best-effort decode.

    Special case: '--' represents '/.' (dotfiles like .claude)
    """
    if not encoded.startswith("-"):
        return encoded
    # Handle dotfiles: -- represents /.
    decoded = encoded[1:].replace("--", "/.")
    # Replace remaining single hyphens with /
    decoded = "/" + decoded.replace("-", "/")
    return decoded


def verify_path_exists(encoded: str) -> tuple[bool, str]:
    """Check if the decoded path exists, trying common corrections.

    Returns (exists, best_path) where best_path is the decoded path that exists,
    or the naive decode if none found.

    The encoding scheme converts both '/' and ' ' (space) to '-', making it
    ambiguous. Strategy: Walk path segments, trying both hyphens and spaces
    when a segment doesn't exist as-is.
    """
    naive_decode = decode_project_path(encoded)

    # First try the naive decode
    if os.path.exists(naive_decode):
        return True, naive_decode

    # Handle dotfiles: -- represents /.
    working_encoded = encoded[1:] if encoded.startswith("-") else encoded
    working_encoded = working_encoded.replace("--", "-.")

    parts = working_encoded.split("-")

    # Build up path segment by segment
    current = "/"
    i = 0
    while i < len(parts):
        part = parts[i]
        if not part:
            i += 1
            continue

        test_path = os.path.join(current, part)

        if os.path.exists(test_path):
            current = test_path
            i += 1
            continue

        # Segment doesn't exist - try combining with remaining segments
        # using either hyphens or spaces
        found = False
        for j in range(i + 1, len(parts) + 1):
            # Try with hyphens (original folder had hyphens)
            combined_hyphen = "-".join(parts[i:j])
            test_hyphen = os.path.join(current, combined_hyphen)
            if os.path.exists(test_hyphen):
                current = test_hyphen
                i = j
                found = True
                break

            # Try with spaces (original folder had spaces)
            combined_space = " ".join(parts[i:j])
            test_space = os.path.join(current, combined_space)
            if os.path.exists(test_space):
                current = test_space
                i = j
                found = True
                break

        if not found:
            # Couldn't find a match
            return False, naive_decode

    return os.path.exists(current), current


def encode_project_path(path: str) -> str:
    """Convert path like '/Users/jdoe/Documents' to '-Users-jdoe-Documents'."""
    return path.replace("/", "-")


def parse_timestamp(ts: str) -> datetime:
    """Parse ISO timestamp to datetime."""
    # Handle both 'Z' suffix and '+00:00' formats
    ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def is_recently_modified(path: Path, threshold_seconds: int = ACTIVE_SESSION_THRESHOLD) -> bool:
    """Check if file was modified within threshold (default 1 hour)."""
    try:
        mtime = path.stat().st_mtime
        age = datetime.now(timezone.utc).timestamp() - mtime
        return age < threshold_seconds
    except OSError:
        return False


COMMAND_NAME_RE = re.compile(r"<command-name>(.*?)</command-name>")

# Max length for a farewell message (responses to /exit are typically short)
MAX_FAREWELL_LENGTH = 200


def extract_content_text(entry: dict) -> str:
    """Extract plain text from a user message entry's content field.

    Content can be a string or a list of parts (each with a 'text' key).
    Returns the concatenated text.
    """
    msg = entry.get("message", {})
    if not isinstance(msg, dict):
        return ""
    content = msg.get("content", "")
    if isinstance(content, list):
        return " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content)


def classify_user_entry(entry: dict) -> str:
    """Classify a type='user' JSONL entry.

    Returns one of: 'meta', 'command', 'command_output', 'message'.
    - meta: system injections (isMeta=true)
    - command: CLI commands (contains <command-name> tags)
    - command_output: stdout from local commands (contains <local-command-stdout>)
    - message: real user input
    """
    if entry.get("isMeta"):
        return "meta"
    text = extract_content_text(entry)
    if COMMAND_NAME_RE.search(text):
        return "command"
    if "<local-command-stdout>" in text or "<local-command-caveat>" in text:
        return "command_output"
    return "message"


def extract_commands(text: str) -> list[str]:
    """Extract all <command-name> values from message text."""
    return COMMAND_NAME_RE.findall(text)


def is_farewell_response(entry: dict) -> bool:
    """Check if an assistant message is a farewell (response to /exit).

    Farewells are typically short messages. We use length as the primary heuristic
    since Claude's farewell messages vary in wording but are consistently brief.
    """
    msg = entry.get("message", {})
    if not isinstance(msg, dict):
        return False
    content = msg.get("content", "")

    # Handle list content (multiple parts)
    if isinstance(content, list):
        text = " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    else:
        text = str(content)

    return len(text.strip()) < MAX_FAREWELL_LENGTH


def analyze_conversation(jsonl_path: Path) -> dict[str, Any]:
    """Extract stats from a conversation JSONL file."""
    # Check if this is an active session (modified recently)
    is_active = is_recently_modified(jsonl_path)

    stats = {
        "session_id": jsonl_path.stem,
        "file_path": str(jsonl_path),
        "is_active": is_active,
        "file_size": jsonl_path.stat().st_size,
        "file_size_human": format_size(jsonl_path.stat().st_size),
        "user_messages": 0,
        "real_user_messages": 0,
        "assistant_messages": 0,
        "real_assistant_messages": 0,
        "commands": [],
        "total_lines": 0,
        "first_timestamp": None,
        "last_timestamp": None,
        "duration_seconds": 0,
        "cwd": None,
        "version": None,
        "first_user_message": None,
        "is_short_lived": False,
        "short_lived_reasons": [],
        "is_empty": False,
    }

    timestamps = []
    prev_was_exit = False  # Track if previous user entry was /exit

    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                stats["total_lines"] += 1
                try:
                    entry = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                # Extract timestamp
                if "timestamp" in entry:
                    try:
                        ts = parse_timestamp(entry["timestamp"])
                        timestamps.append(ts)
                    except (ValueError, TypeError):
                        pass

                # Extract metadata from first entry
                if stats["cwd"] is None and "cwd" in entry:
                    stats["cwd"] = entry.get("cwd")
                if stats["version"] is None and "version" in entry:
                    stats["version"] = entry.get("version")

                # Count message types
                entry_type = entry.get("type")
                if entry_type == "user":
                    stats["user_messages"] += 1
                    kind = classify_user_entry(entry)
                    if kind == "command":
                        text = extract_content_text(entry)
                        cmds = extract_commands(text)
                        stats["commands"].extend(cmds)
                        # Track if this was an /exit command
                        prev_was_exit = "/exit" in cmds
                    elif kind == "message":
                        # Only real user messages reset the /exit tracking
                        # (meta and command_output entries should not reset it)
                        prev_was_exit = False
                        stats["real_user_messages"] += 1
                        # Capture first real user message preview
                        if stats["first_user_message"] is None:
                            text = extract_content_text(entry)
                            if text:
                                stats["first_user_message"] = (
                                    text[:200] + "..." if len(text) > 200 else text
                                )
                    # meta and command_output entries don't affect prev_was_exit
                elif entry_type == "assistant":
                    stats["assistant_messages"] += 1
                    # Count as real if not a farewell following /exit
                    if not (prev_was_exit and is_farewell_response(entry)):
                        stats["real_assistant_messages"] += 1
                    prev_was_exit = False  # Reset after assistant response

    except Exception as e:
        stats["error"] = str(e)
        return stats

    # Calculate time stats
    if timestamps:
        timestamps.sort()
        stats["first_timestamp"] = timestamps[0].isoformat()
        stats["last_timestamp"] = timestamps[-1].isoformat()
        stats["duration_seconds"] = (timestamps[-1] - timestamps[0]).total_seconds()

        # Calculate age
        now = datetime.now(timezone.utc)
        age_seconds = (now - timestamps[-1]).total_seconds()
        stats["age_seconds"] = age_seconds
        stats["age_human"] = format_duration(age_seconds)

    stats["duration_human"] = format_duration(stats["duration_seconds"])

    # Determine if short-lived or false-positive
    reasons = []
    if stats["assistant_messages"] == 0:
        reasons.append("0 assistant messages (false positive)")
    if stats["user_messages"] < 3:
        reasons.append(f"<3 user messages ({stats['user_messages']})")
    if stats["duration_seconds"] < 60:
        reasons.append(f"<60s duration ({stats['duration_human']})")
    if stats["file_size"] < 2048:
        reasons.append(f"<2KB file ({stats['file_size_human']})")

    if reasons:
        stats["is_short_lived"] = True
        stats["short_lived_reasons"] = reasons

    # Empty session: no substantive user input AND no substantive assistant work
    stats["is_empty"] = (
        stats["real_user_messages"] == 0 and stats["real_assistant_messages"] == 0
    )

    return stats


def format_size(bytes_val: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(bytes_val) < 1024:
            return f"{bytes_val:.1f}{unit}" if unit != "B" else f"{bytes_val}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}TB"


def format_duration(seconds: float) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m{secs:02d}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h{mins:02d}m"


def audit_convos(project_filter: str | None = None,
                 command_filter: list[str] | None = None,
                 exact_match: bool = False,
                 empty_only: bool = False) -> dict[str, Any]:
    """Audit all conversations, optionally filtered by project and/or commands."""
    results = {
        "mode": "scan",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "conversations": [],
        "summary": {
            "total": 0,
            "short_lived": 0,
            "empty": 0,
            "total_size": 0,
            "total_user_messages": 0,
        },
    }

    if not PROJECTS_DIR.exists():
        results["error"] = f"Projects directory not found: {PROJECTS_DIR}"
        return results

    # Find all project directories
    project_dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()]

    if project_filter:
        encoded = encode_project_path(project_filter)
        if exact_match:
            project_dirs = [d for d in project_dirs if d.name == encoded]
        else:
            project_dirs = [d for d in project_dirs if encoded in d.name]

    for project_dir in project_dirs:
        progress(f"Scanning {project_dir.name}...")

        # Find all JSONL files
        for jsonl_file in project_dir.glob("*.jsonl"):
            stats = analyze_conversation(jsonl_file)
            stats["project"] = decode_project_path(project_dir.name)
            stats["project_encoded"] = project_dir.name
            results["conversations"].append(stats)

            results["summary"]["total"] += 1
            results["summary"]["total_size"] += stats["file_size"]
            results["summary"]["total_user_messages"] += stats["user_messages"]
            if stats["is_short_lived"]:
                results["summary"]["short_lived"] += 1
            if stats.get("is_empty"):
                results["summary"]["empty"] += 1

    # Apply command filter: keep only conversations containing ALL specified commands
    if command_filter:
        results["conversations"] = [
            c for c in results["conversations"]
            if all(cmd in c.get("commands", []) for cmd in command_filter)
        ]
        results["summary"]["filtered_by_commands"] = command_filter

    # Apply empty-only filter: keep only sessions with no substantive content
    if empty_only:
        results["conversations"] = [
            c for c in results["conversations"]
            if c.get("is_empty")
        ]
        results["summary"]["filtered_empty_only"] = True

    # Recount after filtering (if any filter was applied)
    if command_filter or empty_only:
        results["summary"]["total"] = len(results["conversations"])
        results["summary"]["total_size"] = sum(c["file_size"] for c in results["conversations"])
        results["summary"]["total_user_messages"] = sum(
            c["user_messages"] for c in results["conversations"]
        )
        results["summary"]["short_lived"] = sum(
            1 for c in results["conversations"] if c.get("is_short_lived")
        )
        results["summary"]["empty"] = sum(
            1 for c in results["conversations"] if c.get("is_empty")
        )

    # Sort by last_timestamp descending (most recent first)
    results["conversations"].sort(
        key=lambda x: x.get("last_timestamp") or "", reverse=True
    )

    results["summary"]["total_size_human"] = format_size(results["summary"]["total_size"])

    return results


def audit_projects() -> dict[str, Any]:
    """Audit disk usage by project."""
    results = {
        "mode": "usage",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "projects": [],
        "summary": {"total_projects": 0, "total_size": 0, "total_conversations": 0},
    }

    if not PROJECTS_DIR.exists():
        results["error"] = f"Projects directory not found: {PROJECTS_DIR}"
        return results

    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue

        # Use smart path verification for better decode
        exists, resolved_path = verify_path_exists(project_dir.name)

        project_info = {
            "encoded_path": project_dir.name,
            "decoded_path": resolved_path,
            "path_exists": exists,
            "size": 0,
            "conversation_count": 0,
            "last_activity": None,
        }

        # Calculate total size and count conversations
        latest_mtime = 0
        for item in project_dir.rglob("*"):
            if item.is_file():
                project_info["size"] += item.stat().st_size
                if item.suffix == ".jsonl":
                    project_info["conversation_count"] += 1
                mtime = item.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime

        if latest_mtime > 0:
            project_info["last_activity"] = datetime.fromtimestamp(
                latest_mtime, tz=timezone.utc
            ).isoformat()
            age = datetime.now(timezone.utc) - datetime.fromtimestamp(
                latest_mtime, tz=timezone.utc
            )
            project_info["last_activity_human"] = format_duration(age.total_seconds())

        project_info["size_human"] = format_size(project_info["size"])

        results["projects"].append(project_info)
        results["summary"]["total_projects"] += 1
        results["summary"]["total_size"] += project_info["size"]
        results["summary"]["total_conversations"] += project_info["conversation_count"]

    # Sort by size descending
    results["projects"].sort(key=lambda x: x["size"], reverse=True)
    results["summary"]["total_size_human"] = format_size(results["summary"]["total_size"])

    return results


def audit_disk() -> dict[str, Any]:
    """Audit full ~/.claude disk usage."""
    results = {
        "mode": "global",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "categories": [],
        "stale_files": [],
        "summary": {"total_size": 0},
    }

    if not CLAUDE_DIR.exists():
        results["error"] = f"Claude directory not found: {CLAUDE_DIR}"
        return results

    # Categorize subdirectories
    cleanable = {
        "debug": True,
        "telemetry": True,
        "usage-data": True,
        "file-history": "with caution",
        "cache": True,
        "paste-cache": True,
    }

    for item in sorted(CLAUDE_DIR.iterdir()):
        if item.is_dir():
            size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
            results["categories"].append({
                "name": item.name,
                "size": size,
                "size_human": format_size(size),
                "cleanable": cleanable.get(item.name, False),
            })
            results["summary"]["total_size"] += size

    # Sort by size descending
    results["categories"].sort(key=lambda x: x["size"], reverse=True)

    # Find stale context_state files
    thirty_days_ago = datetime.now(timezone.utc).timestamp() - (30 * 24 * 3600)
    for item in CLAUDE_DIR.glob("context_state_*.json"):
        if item.is_file() and item.stat().st_mtime < thirty_days_ago:
            results["stale_files"].append({
                "path": str(item),
                "size": item.stat().st_size,
                "age_days": int(
                    (datetime.now(timezone.utc).timestamp() - item.stat().st_mtime)
                    / 86400
                ),
            })

    results["summary"]["total_size_human"] = format_size(results["summary"]["total_size"])
    results["summary"]["stale_file_count"] = len(results["stale_files"])

    return results


def audit_orphans() -> dict[str, Any]:
    """Find conversations for project paths that no longer exist."""
    results = {
        "mode": "orphans",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "orphans": [],
        "verified_existing": [],
        "summary": {"total_orphaned_projects": 0, "total_orphaned_size": 0},
    }

    if not PROJECTS_DIR.exists():
        results["error"] = f"Projects directory not found: {PROJECTS_DIR}"
        return results

    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        # Use smart path verification
        exists, resolved_path = verify_path_exists(project_dir.name)
        naive_decode = decode_project_path(project_dir.name)

        if not exists:
            size = sum(f.stat().st_size for f in project_dir.rglob("*") if f.is_file())
            conv_count = len(list(project_dir.glob("*.jsonl")))

            results["orphans"].append({
                "encoded_path": project_dir.name,
                "decoded_path": naive_decode,
                "size": size,
                "size_human": format_size(size),
                "conversation_count": conv_count,
            })

            results["summary"]["total_orphaned_projects"] += 1
            results["summary"]["total_orphaned_size"] += size
        else:
            # Track verified paths for debugging
            if resolved_path != naive_decode:
                results["verified_existing"].append({
                    "encoded_path": project_dir.name,
                    "naive_decode": naive_decode,
                    "actual_path": resolved_path,
                })

    results["summary"]["total_orphaned_size_human"] = format_size(
        results["summary"]["total_orphaned_size"]
    )

    return results


def prune_short_lived(dry_run: bool = True,
                      project_filter: str | None = None,
                      command_filter: list[str] | None = None,
                      exact_match: bool = False,
                      empty_only: bool = False) -> dict[str, Any]:
    """Delete sessions matching filters, protecting active sessions."""
    results = {
        "mode": "clean",
        "dry_run": dry_run,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "deleted": [],
        "skipped_active": [],
        "errors": [],
        "summary": {"deleted_count": 0, "deleted_size": 0, "error_count": 0, "skipped_count": 0},
    }

    # Get conversations (filtered by project, commands, and/or empty-only)
    convos = audit_convos(project_filter, command_filter=command_filter,
                          exact_match=exact_match, empty_only=empty_only)
    # If any filter is active, all matched conversations are candidates;
    # otherwise fall back to short-lived heuristic
    if command_filter or empty_only:
        candidates = convos["conversations"]
    else:
        candidates = [c for c in convos["conversations"] if c.get("is_short_lived")]

    for convo in candidates:
        session_id = convo["session_id"]
        file_path = Path(convo["file_path"])
        file_size = convo["file_size"]

        # Skip active sessions
        if convo.get("is_active"):
            results["skipped_active"].append({
                "session_id": session_id,
                "reason": "modified within last hour",
            })
            results["summary"]["skipped_count"] += 1
            continue

        if dry_run:
            results["deleted"].append({
                "session_id": session_id,
                "file_path": str(file_path),
                "size": file_size,
                "would_delete": True,
            })
            results["summary"]["deleted_count"] += 1
            results["summary"]["deleted_size"] += file_size
        else:
            try:
                # Delete the jsonl file
                file_path.unlink()

                # Delete matching directory if exists
                session_dir = file_path.with_suffix("")
                if session_dir.is_dir():
                    import shutil
                    shutil.rmtree(session_dir)

                results["deleted"].append({
                    "session_id": session_id,
                    "file_path": str(file_path),
                    "size": file_size,
                })
                results["summary"]["deleted_count"] += 1
                results["summary"]["deleted_size"] += file_size

            except Exception as e:
                results["errors"].append({
                    "session_id": session_id,
                    "file_path": str(file_path),
                    "error": str(e),
                })
                results["summary"]["error_count"] += 1

    results["summary"]["deleted_size_human"] = format_size(results["summary"]["deleted_size"])
    return results


def run(args):
    """Route parsed args to the appropriate audit function and emit JSON."""
    # Parse command filter into a list (shared by scan and clean)
    command_filter = None
    if hasattr(args, "filter_command") and args.filter_command:
        command_filter = [c.strip() for c in args.filter_command.split(",")]

    if args.action == "scan":
        result = audit_convos(
            args.project,
            command_filter=command_filter,
            exact_match=args.exact,
            empty_only=args.empty_only,
        )
    elif args.action == "usage":
        result = audit_projects()
    elif args.action == "global":
        result = audit_disk()
    elif args.action == "orphans":
        result = audit_orphans()
    elif args.action == "clean":
        dry_run = not args.confirm
        result = prune_short_lived(
            dry_run=dry_run,
            project_filter=args.project,
            command_filter=command_filter,
            exact_match=args.exact,
            empty_only=args.empty_only,
        )
    else:
        result = {"error": f"Unknown action: {args.action}"}

    print(json.dumps(result, indent=2))


def main():
    # Default to "scan" when no subcommand given
    known = {"scan", "usage", "global", "clean", "orphans"}
    if len(sys.argv) == 1 or (sys.argv[1] not in known and sys.argv[1] not in ("-h", "--help")):
        sys.argv.insert(1, "scan")

    parser = argparse.ArgumentParser(description="cc-health chats domain — conversation hygiene")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Scan
    scan_parser = subparsers.add_parser("scan", help="List conversations with stats")
    scan_parser.add_argument("--project", help="Filter to project path (substring match)")
    scan_parser.add_argument("--exact", action="store_true", help="Exact project path match")
    scan_parser.add_argument("--filter-command", help="Filter by commands (comma-separated)")
    scan_parser.add_argument("--empty-only", action="store_true", help="Only empty sessions")

    # Usage
    subparsers.add_parser("usage", help="Size/count breakdown per project")

    # Global
    subparsers.add_parser("global", help="Full ~/.claude disk breakdown")

    # Clean
    clean_parser = subparsers.add_parser("clean", help="Interactive cleanup")
    clean_parser.add_argument("--project", help="Filter to project path")
    clean_parser.add_argument("--exact", action="store_true")
    clean_parser.add_argument("--filter-command", help="Filter by commands")
    clean_parser.add_argument("--empty-only", action="store_true")
    clean_parser.add_argument("--confirm", action="store_true", help="Execute deletions")

    # Orphans
    subparsers.add_parser("orphans", help="Find conversations for deleted projects")

    args = parser.parse_args()
    # Route to existing functions (unchanged logic)
    run(args)


if __name__ == "__main__":
    main()
